import pandas as pd
import numpy as np
import os
import requests
import time
import pkg_resources

#load icd 9 to icd 10 mapping file
#https://www.cms.gov/Medicare/Coding/ICD10/2018-ICD-10-CM-and-GEMs.html
def load_icd9to10():
    icd9to10 = pd.read_csv(pkg_resources.resource_filename(__name__,'2018_I9gem.txt'),delim_whitespace=True,header=None,dtype=str)
    icd9to10.columns=['icd9','icd10','flag']
    return icd9to10

#load icd 10 to icd 9 mapping file
#https://www.cms.gov/Medicare/Coding/ICD10/2018-ICD-10-CM-and-GEMs.html
def load_icd10to9():
    icd10to9 = pd.read_csv(pkg_resources.resource_filename(__name__,'2018_I10gem.txt'),delim_whitespace=True,header=None,dtype=str)
    icd10to9.columns=['icd10','icd9','flag']
    return icd10to9

#convert icd 9 to 10, or 10 to 9
#https://www.cms.gov/Medicare/Coding/ICD10/2018-ICD-10-CM-and-GEMs.html
def icdconvert(df,col_icd='icd',icd_version=9):
    if icd_version==9:
        source='icd9'
        target='icd10'
        df_gem=load_icd9to10()
    elif icd_version==10:
        source='icd10'
        target='icd9'
        df_gem=load_icd10to9()
    else:
        print('invalid icd version {}, please set curicd to 9 or 10'.format(icd_version))
        return None
    
    print('Comment: because of the discrepancy between icd9 and icd10, diagnosis codes may be mapped to many codes or no codes')
    
    output=df.merge(df_gem,how='left',left_on=col_icd,right_on=source)
    print('{:.2f}% mapped'.format(output[target].notnull().mean()*100))
    if 'flag' in output.columns:
        output.drop('flag',axis=1,inplace=True)
    if col_icd!=source in output.columns:
        output.drop(source,axis=1,inplace=True)
    
    return output

def loadphecodes():
    phecode9 = pd.read_csv(pkg_resources.resource_filename(__name__,'phecode_icd9_rolled.csv'),dtype=str).iloc[:,0:4]
    phecode10 = pd.read_csv(pkg_resources.resource_filename(__name__,'Phecode_map_v1_2_icd10cm_beta.csv'),dtype=str).iloc[:,0:4]
    phemap = pd.read_csv(pkg_resources.resource_filename(__name__,'phecode_definitions1.2.csv'),dtype=str)
    phecode9.columns = ['ICD Code','ICD Description','PheCode','PheCode Description']
    phecode9['Type']='9'
    phecode10.columns = ['ICD Code','ICD Description','PheCode','PheCode Description']
    phecode10['Type']='10'
    phecode = pd.concat([phecode9,phecode10],axis=0)
    phecode['ICD Code'] = phecode['ICD Code'].str.replace('.','')
    phemap.columns = ["PheCode","phenotype","phecode_exclude_range","sex","rollup","leaf","category_number","category"]
    phecode = phecode.merge(phemap.loc[:,['PheCode','category']],how='left',on='PheCode')
    return phecode

def icdtophecode(df,col_icd):
    phecode = loadphecodes()
    df = df.copy()
    df[col_icd] = df[col_icd].str.replace(' ','').str.replace('.','')
    df = df.merge(phecode,how='left',left_on=col_icd,right_on='ICD Code')
    return df

# load Elixhauser comorbidities mapping file
#Quan H, Sundararajan V, Halfon P, Fong A, Burnand B, Luthi JC, Saunders LD, Beck CA, Feasby TE, Ghali WA. 
#Coding algorithms for defining comorbidities in ICD-9-CM and ICD-10 administrative data. 
#Medical care. 2005 Nov 1:1130-9.
def loadelixcomo():
    elixcomo = pd.read_csv(pkg_resources.resource_filename(__name__,'Elixhauser_Comorbidities.csv')).iloc[:,1:]
    return elixcomo

#convert icd 9 or 10 to Elixhauser Comorbidities
def icdtoelixcomo(df,col_icd):
    elixcomo = loadelixcomo()
    unqcomos = elixcomo['Comorbidity'].unique()
    df['ElixComo']=None
    df['ElixComoScore']=None
    for como in unqcomos:
        icdlist = tuple(elixcomo.loc[elixcomo['Comorbidity']==como,'ICD'])
        comoidx = df[col_icd].str.startswith(icdlist,na=False)
        df.loc[comoidx,'ElixComo']=como
        df.loc[comoidx,'ElixComoScore']=elixcomo.loc[elixcomo.Comorbidity==como,'Score'].values[0]
    return df
  

# score patients based on elixhauser comorbidities
#van Walraven C, Austin PC, Jennings A, Quan H, Forster AJ. 
#A modification of the Elixhauser comorbidity measures into a point system for hospital death using administrative data. 
#Medical care. 2009 Jun 1:626-33.
def elixcomoscore(df,col_icd,col_id):
    output = icdtoelixcomo(df,col_icd)
    output = output.loc[output['ElixComo'].notnull(),:]
    output = output.loc[:,[col_id,'ElixComo','ElixComoScore']]
    output = output.drop_duplicates()
    output = pd.DataFrame(output.groupby(col_id)['ElixComoScore'].sum()).reset_index()
    output = output.merge(df.loc[:,[col_id]].drop_duplicates(),how='outer',left_on=col_id,right_on=col_id).fillna(0.)
    return output
    
    
# load mapping file from icd9 to Chronic Condition Indicator (CCI)
#https://www.hcup-us.ahrq.gov/toolssoftware/chronic/chronic.jsp
def load_cci9():
    cci9 = pd.read_csv(pkg_resources.resource_filename(__name__,'cci2015.csv'),skiprows=1)
    cci9.columns = [i.strip('\'') for i in cci9.columns]
    
    for col in cci9.columns:
        cci9.loc[:,col] = cci9[col].str.strip('\'')
    cci9 = cci9.replace(r'^\s*$', np.nan, regex=True)
    cci9.columns=[i.replace('CATEGORY DESCRIPTION','CHRONIC') for i in cci9.columns]

    dict_bodysystem=[
        ('1' ,'Infectious and parasitic disease'),
        ('2' ,'Neoplasms'),
        ('3' ,'Endocrine, nutritional, and metabolic diseases and immunity disorders'),
        ('4' ,'Diseases of blood and blood-forming organs'),
        ('5' ,'Mental disorders'),
        ('6' ,'Diseases of the nervous system and sense organs'),
        ('7' ,'Diseases of the circulatory system'),
        ('8' ,'Diseases of the respiratory system'),
        ('9' ,'Diseases of the digestive system'),
        ('10','Diseases of the genitourinary system'),
        ('11','Complications of pregnancy, childbirth, and the puerperium'),
        ('12','Diseases of the skin and subcutaneous tissue'),
        ('13','Diseases of the musculoskeletal system'),
        ('14','Congenital anomalies'),
        ('15','Certain conditions originating in the perinatal period'),
        ('16','Symptoms, signs, and ill-defined conditions'),
        ('17','Injury and poisoning'),
        ('18','Factors influencing health status and contact with health service'),
    ]
    
    cci9 = cci9.merge(pd.DataFrame(dict_bodysystem,columns=['BODY SYSTEM','BODY SYSTEM DESCRIPTION']),how='left',on='BODY SYSTEM')
    
    cci9.loc[:,'ICD-9-CM CODE'] = cci9['ICD-9-CM CODE'].str.replace(' ','')
    
    return cci9

#convert icd9 to CCI
def icd9tocci(df,col_icd='icd9'):
    cci9 = load_cci9()
    return df.merge(cci9,how='left',left_on=col_icd,right_on='ICD-9-CM CODE')
    
    
    

# load mapping file from icd10 to Chronic Condition Indicator (CCI)
#https://www.hcup-us.ahrq.gov/toolssoftware/chronic_icd10/chronic_icd10.jsp
def load_cci10():
    
    cci10 = pd.read_csv(pkg_resources.resource_filename(__name__,'cci_icd10cm_2019_1.csv'))
    
    cci10.columns = [i.strip('\'') for i in cci10.columns]
    
    for col in cci10.columns:
        cci10.loc[:,col] = cci10[col].str.strip('\'')
    cci10 = cci10.replace(r'^\s*$', np.nan, regex=True)
    cci10.columns = [i.replace('CHRONIC INDICATOR','CHRONIC') for i in cci10.columns]
    
    dict_bodysystem = [
        ('1','Infectious and parasitic disease'),
        ('2','Neoplasms'),
        ('3','Endocrine, nutritional, and metabolic diseases and immunity disorders'),
        ('4','Diseases of blood and blood-forming organs'),
        ('5','Mental disorders'),
        ('6','Diseases of the nervous system and sense organs'),
        ('7','Diseases of the circulatory system'),
        ('8','Diseases of the respiratory system'),
        ('9','Diseases of the digestive system'),
        ('10','Diseases of the genitourinary system'),
        ('11','Complications of pregnancy, childbirth, and the puerperium'),
        ('12','Diseases of the skin and subcutaneous tissue'),
        ('13','Diseases of the musculoskeletal system'),
        ('14','Congenital anomalies'),
        ('15','Certain conditions originating in the perinatal period'),
        ('16','Symptoms, signs, and ill-defined conditions'),
        ('17','Injury and poisoning'),
        ('18','Factors influencing health status and contact with health services'),
    ]
    
    cci10 = cci10.merge(pd.DataFrame(dict_bodysystem,columns=['BODY SYSTEM','BODY SYSTEM DESCRIPTION']),how='left',on='BODY SYSTEM')
    
    cci10.loc[:,'ICD-10-CM CODE'] = cci10['ICD-10-CM CODE'].str.replace(' ','')
    
    return cci10

#convert icd10 to CCI
def icd10tocci(df,col_icd='icd10'):
    cci10 = load_cci10()
    return df.merge(cci10,how='left',left_on=col_icd,right_on='ICD-10-CM CODE')

# load mapping file from icd9 to Clinical Classification Software (CCS)
#https://www.hcup-us.ahrq.gov/toolssoftware/ccs/ccs.jsp
def load_ccs9():
    ccs9 = pd.read_csv(pkg_resources.resource_filename(__name__,'$dxref 2015.csv'))
    ccs9 = ccs9.reset_index()
    for col in ccs9.columns:
        ccs9.loc[:,col]=ccs9[col].str.strip('\'')
    ccs9.columns=ccs9.iloc[0,:]
    ccs9 = ccs9.iloc[1:,:]
    ccs9 = ccs9.replace(r'^\s*$', np.nan, regex=True)
    ccs9 = ccs9.loc[ccs9['ICD-9-CM CODE'].notnull(),:]
    ccs9.loc[:,'ICD-9-CM CODE'] = ccs9['ICD-9-CM CODE'].str.replace(' ','')
    ccs9.loc[:,'CCS CATEGORY'] = ccs9['CCS CATEGORY'].str.replace(' ','')
    ccs9 = ccs9.iloc[:,0:4]    
    ccs9_labels = pd.read_csv(pkg_resources.resource_filename(__name__,'dxlabel 2015.csv'))
    ccs9 = ccs9.merge(ccs9_labels,how='left',left_on='CCS CATEGORY',right_on='CCS DIAGNOSIS CATEGORIES')
    ccs9.drop('CCS CATEGORY DESCRIPTION',axis=1,inplace=True)
    ccs9.drop('CCS DIAGNOSIS CATEGORIES',axis=1,inplace=True)
    ccs9.columns = [i.replace('CCS DIAGNOSIS CATEGORIES LABELS','CCS CATEGORY DESCRIPTION') for i in ccs9.columns]
    return ccs9

#convert icd9 to CCS
def icd9toccs(df,col_icd='icd9'):
    ccs9 = load_ccs9()
    output = df.merge(ccs9,how='left',left_on=col_icd,right_on='ICD-9-CM CODE')
    if col_icd!='ICD-9-CM CODE':
        output.drop('ICD-9-CM CODE',axis=1,inplace=True)
    return output

# load mapping file from icd10 to Clinical Classification Software (CCS)
#https://www.hcup-us.ahrq.gov/toolssoftware/ccs10/ccs10.jsp
def load_ccs10():
    ccs10 = pd.read_csv(pkg_resources.resource_filename(__name__,'ccs_dx_icd10cm_2019_1.csv'))
    ccs10.columns=[i.strip('\'') for i in ccs10.columns]
    for col in ccs10.columns:
        ccs10.loc[:,col]=ccs10[col].str.strip('\'')
    ccs10 = ccs10.replace(r'^\s*$', np.nan, regex=True)
    ccs10.loc[:,'ICD-10-CM CODE'] = ccs10['ICD-10-CM CODE'].str.replace(' ','')
    ccs10=ccs10.iloc[:,0:4]
    return ccs10
    

#convert icd10toccs    
def icd10toccs(df,col_icd='icd10'):
    ccs10 = load_ccs10()
    output = df.merge(ccs10,how='left',left_on=col_icd,right_on='ICD-10-CM CODE')
    if col_icd!='ICD-10-CM CODE':
        output.drop('ICD-10-CM CODE',axis=1,inplace=True)
    return output

#parse diagnosis dataset and include Clinical Classification Software, Chronic Glag, and Elixhauser Comorbidity
def parsediag(dfin,col_icd,col_id,icd_version):
    df = dfin.copy()
    
    if icd_version==9:
        toccs = icd9toccs
    elif icd_version==10:
        toccs = icd10toccs
    else:
        print('ERROR: Please set icd_version to 9 or 10')
        return None
    
    df = toccs(df,col_icd=col_icd)
    
    if icd_version==9:
        tocci = icd9tocci
    elif icd_version==10:
        tocci = icd10tocci
    
    df = tocci(df,col_icd=col_icd)
    
    df = icdtoelixcomo(df,col_icd=col_icd)
    
    df = df.loc[:,list(dfin.columns)+['CCS CATEGORY','CCS CATEGORY DESCRIPTION','CHRONIC','ElixComo','ElixComoScore']]
    
    
    return df

# onehotifying categorical columns
def onehotify(df,col_id,col_val):
    return pd.concat([df.loc[:,[col_id]],pd.get_dummies(df[col_val])],axis=1).groupby(col_id).max()

#convert NDC codes to RXCUI
def ndc2rxcui(df_med,col_ndc='ndc'):
    print('Converting NDC to RXCUI')
    output=[]
    ndclist=df_med[col_ndc].unique()
    lenndc = len(ndclist)
    for i in range(0,len(ndclist)):
        print('{}/{}, {:.2f}% complete'.format((i+1),lenndc,(i+1)/lenndc*100), end='\r', flush=True)
        curndc=ndclist[i]
        r=requests.get('https://rxnav.nlm.nih.gov/REST/ndcstatus.json?ndc='+str(curndc)).json()['ndcStatus']
        if 'ndcHistory' in r:
            for entry in r['ndcHistory']:
                output.append({
                    'ndc':curndc,
                    'rxcui':entry['activeRxcui'],
                    'start':pd.to_datetime(entry['startDate']+'01'),
                    'end':pd.to_datetime(entry['endDate']+'01'),
                })
        else:
            print('NDC code [{}] was not able to be mapped to rxcui'.format(curndc))
        time.sleep(1/20)
    output=pd.DataFrame(output).replace({r'^\s*$':None}, regex=True).dropna()
    return output

#convert RXCUI to drug classes
def rxcui2class(df_mapin,getname=True):
    print('Converting rxcui to drug class')
    rxcuilist=df_mapin['rxcui'].unique()
    lenrxcui=len(rxcuilist)
    output=[]
    
    identifier='classId'
    if getname:
        identifier='className'
    
    for i in range(0,lenrxcui):
        print('{}/{}, {:.2f}% complete'.format((i+1),lenrxcui,(i+1)/lenrxcui*100), end='\r', flush=True)
        currxcui=rxcuilist[i]
        r=requests.get('https://rxnav.nlm.nih.gov/REST/rxclass/class/byRxcui.json?rxcui='+str(currxcui)).json()

        if 'rxclassDrugInfoList' in r:
            tempdict={'rxcui':currxcui}
            for curclass in r['rxclassDrugInfoList']['rxclassDrugInfo']:
                classtype=curclass['relaSource']+'_'+curclass['rxclassMinConceptItem']['classType']
                if classtype not in tempdict:
                    tempdict[classtype]=set([curclass['rxclassMinConceptItem'][identifier]])
                else:
                    tempdict[classtype].add(curclass['rxclassMinConceptItem'][identifier])
            output.append(tempdict)
        else:
            print('rxcui [{}] was not able to be mapped to drug class'.format(currxcui))
        time.sleep(1/20)
    return pd.DataFrame(output)

#combine NDC2RXCUI and RXCUI2CLASS to go from NDC to CLASS
def ndc2class(df_med,col_ndc='ndc',getname=True,indexcol='ROWID',timecol='TIME'):
    map1=ndc2rxcui(df_med,col_ndc=col_ndc)
    map2=rxcui2class(map1,getname=getname)

    newmed=df_med.copy()
    
    #merge maps to go from ndc to rxnorm to class
    fullmap=map1.merge(map2,how='left',on='rxcui')
    
    #merge medication dataframe to full map
    temp=newmed.merge(fullmap,how='left',left_on=col_ndc,right_on='ndc')
    
    #filter based on start and end date
    temp=temp.loc[(temp[timecol]>=temp.start) & (temp[timecol] <=temp.end),:]
    
    #if multiple rxcui per ndc, take the one with the later end date
    temp=temp.sort_values('end')
    temp=temp.drop_duplicates(subset=df_med.columns,keep='last')

    #if no rxcui exist for ndc given the time range, try to just take the latest rxcui
    temp=pd.concat([temp,newmed.loc[~newmed[indexcol].isin(temp[indexcol]),:].merge(fullmap.sort_values(by='end').drop_duplicates(subset='ndc',keep='last'),how='left',left_on=col_ndc,right_on='ndc')],axis=0)
    temp=temp.sort_values(by=indexcol)
    return temp