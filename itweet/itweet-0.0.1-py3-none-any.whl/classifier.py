"""
============================== 핵심일 ==============================
클래스다.

===== 용어 정의 =====
훈련자료모음(훈련자료 + 그 분류값) 로딩 -> 뉴스XX와 그로부터 클러스터된 라벨, train_df
훈련자료 : trainset_data, train_docs
훈련분류 : label, target
훈련tbl명 : 클러스터(훈련된) 자료를 보유한 테이블명
훈련col명 : 클러스터(훈련된) 컬럼명
실험자료모음 : test_df
실험자료 : testset_data, test_docs
실험분류 : predicted
실험tbl명 : 분류예측할 자료가 존재하는 테이블명
실험col명 : 분류예측할 컬럼명

SP_TBL : spread_tbl
clf : classifier

===== 자료구조 : TBL 구조 =====
_id            object  -> 조건id
클러스터id -> trainset_id
분류기_알고리즘       object
KeyidPredict_dicli    object
실험tbl명       object
실험col명       object

===== 자료구조 : SP_TBL 구조 =====
_id          object
UTL_id       object  -> 훈련tbl명에 따라 변동
predicted     int64
조건id         object

TBL명 에는 여러 조건을 같이 저장할 때 쓰고,
SP_TBL명 에는 하나의 문서에 포함된 엄청난 데이터를 풀어헤쳐 놓는다.
이유는, 사건별(label / predicted)로 빠르게 로딩하기 위해서다.

===== 자료구조 =====
훈련자료tbl명='뉴스' -> 고정
훈련col명='뉴스제목'
훈련분류tbl명='뉴스_클러스터'
훈련분류col명 = 'label'
클러스터_알고리즘 = 'KMeans'

실험tbl명 = '트위터_유저타임라인' -> 거의 고정
실험col명 = 'text' -> 거의 고정
분류기_알고리즘 = MultinomialNB, Perceptron, etc.
분류예측값li
"""

# 패키지 라이브러리
from twitter import *

#doc#

# 나의 패키지
import __pymongo as mg
import __sklearn as skl

# 오픈 패키지
import pandas as pd
from datetime import datetime

# 모듈 라이브러리
import News as news
import ML

# 패키지 모듈
import Twitter_UserTimeline as userTL

# 전역변수
CLF_TBL = ML.classifier.CLF_TBL
#CLF_TBL = 'XX_분류'
CLF_REPORT_TBL = ML.classifier.CLF_REPORT_TBL
#CLF_REPORT_TBL = 'XX_분류결과_분석보고'

#TBL명 = '트위터_분류기_예측결과'
#SP_TBL명 = TBL명 + '_확장'



"""
def 트윗_분류기():
    트윗_단위분류기(훈련col명='뉴스제목', 분류기_알고리즘='MultinomialNB')
    TBL에_저장된_하나의_문서를_SP_TBL에_풀어헤치기(실험tbl명='트위터_유저타임라인', 실험col명='text', 분류기_알고리즘='MultinomialNB', dbgon=False, 사전검증=False)

============================== Classifier ==============================
"""
def TW_Classifier(실험tbl명=userTL.PARSED_TBL, key_col='_id', 실험col명='text', 분류기_알고리즘='MultinomialNB', 훈련tbl명=None, 훈련col명=None, algorithm=None, sampling=None, n_clusters=None, dbgon=False, 사전검증=False):
    print('\n' + '='*60 + inspect.stack()[0][3])
    """
    "어떤 클러스터"를 사용한 "어떤 훈련자료"를 이용해서 "어떤 분류기"를 훈련시킨다.

    ===== 사용법 =====
    TW_Classifier(실험tbl명=userTL.PARSED_TBL, key_col='_id', 실험col명='text', 분류기_알고리즘='MultinomialNB', 훈련tbl명='뉴스_ETRI언어분석', 훈련col명='뉴스본문srl_WSDNNGli', algorithm='KMeans', sampling=10000, n_clusters=2000, dbgon=False, 사전검증=False)
    TW_Classifier(실험tbl명=userTL.PARSED_TBL, key_col='_id', 실험col명='text', 분류기_알고리즘='MultinomialNB', 훈련tbl명=None, 훈련col명=None, algorithm=None, sampling=None, n_clusters=None, dbgon=False, 사전검증=False)

    ===== 작업순서 =====
    실험자료 로딩
    머신러닝_분류기
    """
    #if dbgon == True: print(설명)
    #입력 = {'tbl명':tbl명, 'clst타겟col명':clst타겟col명, 'algorithm':algorithm, 'n_clusters':n_clusters}
    #if dbgon == True: pp.pprint({'입력':입력})

    test_df = userTL.UserTimeline_로딩(AssmblMan=True, prjct_cols=['_id', 실험col명], dbgon=False)
    ML.classifier.뉴스클러스터기준_분류(test_df=test_df, 실험tbl명=실험tbl명, key_col=key_col, 실험col명=실험col명, 분류기_알고리즘=분류기_알고리즘, 훈련tbl명=훈련tbl명, 훈련col명=훈련col명, algorithm=algorithm, sampling=sampling, n_clusters=n_clusters, dbgon=dbgon, 사전검증=사전검증)


def TW_Classifier_UpdatedData(실험tbl명=userTL.PARSED_TBL, key_col='_id', 실험col명='text', 분류기_알고리즘='MultinomialNB', 훈련tbl명=None, 훈련col명=None, algorithm=None, sampling=None, n_clusters=None, dbgon=False, 사전검증=False):
    print('\n' + '='*60 + inspect.stack()[0][3])

"""
============================== ClassifierAnalyzer ==============================
"""
def TW_Predicted_df_결과저장(실험tbl명, 실험col명, 분류기_알고리즘, dbgon=False):
    print('\n' + '='*60 + inspect.stack()[0][3])
    """
    ===== 사용법 =====
    TW_Predicted_df_결과저장(실험tbl명=userTL.PARSED_TBL, 실험col명='text', 분류기_알고리즘='MultinomialNB', dbgon=False)

    clf_tbl='트위터_유저타임라인', clf_col='text'
    Predicted_Orig_df로딩(실험tbl명, 실험col명, 분류기_알고리즘, 클러스터id, dbgon=False)
    """
    clf_df = ML.classifier.XX_분류_검색로딩(실험tbl명, 실험col명, 분류기_알고리즘, meta_only=True, dbgon=dbgon)
    clf_dicli = clf_df.to_dict('records')
    clf_dicli_len = len(clf_dicli)
    i=1
    for d in clf_dicli:
        print('\n' + '-'*60 + '{}/{}'.format(i, clf_dicli_len))
        predicted_df, g = ML.classifier.Predicted_Orig_df로딩(실험tbl명=d['실험tbl명'], 실험col명=d['실험col명'], 분류기_알고리즘=d['분류기_알고리즘'], 클러스터id=d['클러스터id'], dbgon=dbgon)
        """
        ============================== 분류결과_저장 ==============================
        """
        print('\n' + '= '*30 + '분류결과_저장')
        cnt_col = list(g.columns)[0]
        report_dic = {
            'clf_id':d['_id'],
            'predicted_li':list(g.index),
            'predicted_cnt_li':list(g[cnt_col]),
        }
        print('\n report_dic :\n')
        if dbgon == True: pp.pprint(report_dic)
        mg.insert_one(db명=DB명, tbl명=CLF_REPORT_TBL, dic=report_dic, dbgon=dbgon, 사전검증=False)
        i+=1
        #break
"""
============================== ClassifierLoader ==============================
"""
def TW_Predicted_Orig_df로딩(test_tbl='트위터_유저타임라인', test_col='text', dbgon=False):
    print('\n' + '='*60 + inspect.stack()[0][3])
    """
    clf_tbl명='트위터_유저타임라인', clf_col명='text'
    """
    df = ML.classifier.CLF_TBL자료에_CLST_TBL메타정보를_결합해서_df로딩(dbgon=dbgon)
    """
    핵심부분
    """
    df = df[ df['실험tbl명']==test_tbl ]
    df = df[ df['분류기_알고리즘']=='Perceptron' ]
    #df = df.iloc[:1, ]
    print('\n df_len :\n', len(df))
    print('\n df :\n', df)
    d = df.to_dict('records')[0]
    """"""
    predicted_tw_df = ML.classifier.Predicted_Orig_df로딩(실험tbl명=d['실험tbl명'], 실험col명=d['실험col명'], 분류기_알고리즘=d['분류기_알고리즘'], 클러스터id=d['clst_id'], dbgon=dbgon)
    return predicted_tw_df

"""
==============================  ==============================
"""
def TBL에_저장된_하나의_문서를_SP_TBL에_풀어헤치기(실험tbl명='트위터_유저타임라인', 실험col명='text', 분류기_알고리즘='MultinomialNB', dbgon=False, 사전검증=False):
    from pandas.io.json import json_normalize
    print('\n' + '='*60 + inspect.stack()[0][3])
    """
    ===== 작업순서 =====
    TBL에서 특정조건으로, _id과 KeyidPredict_dicli 컬럼만, 문서를 로딩
    _id 명을 "조건id" 로 이름을 바꿈.
    중복을 제거 -> 최초만 남기나?
    풀어헤쳐서,
    KeyidPredict_dicli 을 json_normalize
    여기의 _id를 "XXid" 로 이름을 변경.
    조건id 를 신규컬럼으로 추가.
    저장.
    """
    실험자료id명 = 'UTL_id'

    query = {'실험tbl명':실험tbl명, '실험col명':실험col명, '분류기_알고리즘':분류기_알고리즘}
    df = mg.find(db명=DB명, tbl명=CLF_TBL, query=query, projection=None, dbgon=dbgon, 컬럼순서li=[], df보고형태='df')
    df = df.drop_duplicates(subset=['실험tbl명', '실험col명', '분류기_알고리즘'], keep='first', inplace=False)
    df = df.rename(columns={'_id':'조건id'})
    #print(df.dtypes)


    print('\n'+'= '*30+'풀어헤치기')
    if len(df) == 1:
        dic = df.to_dict('records')[0]
        조건id = dic['조건id']
        KeyidPredict_dicli = dic['KeyidPredict_dicli']
        #return None
        df1 = json_normalize(data=KeyidPredict_dicli, record_path=None, meta=None, meta_prefix=None, record_prefix=None, errors='raise', sep='.')
        df1 = df1.rename(columns={'_id':실험자료id명})
        df1 = df1.assign(조건id= 조건id)
        print(df1.dtypes)
        print(len(df1))
        dicli = df1.to_dict('records')
        mg.insert_many(db명=DB명, tbl명=SP_TBL명, dicli=dicli, dbgon=dbgon, 사전검증=사전검증)

    else:
        print('\n 이럴리 없자나? \n')


def 트위터_분류된_트윗을_사건번호_조건으로_로딩(event_num, 실험tbl명='트위터_유저타임라인', 실험col명='text', 분류기_알고리즘='MultinomialNB', dbgon=False):
    print('\n' + '='*60 + inspect.stack()[0][3])
    """
    데이터 양이 엄청나기 때문에(30만 이상) event_num는 필수 파라미터다.
    TBL과 SP_TBL 간의 확장/reduce 특수성으로 인해 로딩 함수가 반드시 필요하다.

    ===== 용어정의 =====
    event_num : label, predicted, 사건번호, 사건id ....다 같은 말.
    """

    query = {'실험tbl명':실험tbl명, '실험col명':실험col명, '분류기_알고리즘':분류기_알고리즘}
    _id_li = mg.distinct(db명=DB명, tbl명=CLF_TBL, col명='_id', query=query, dbgon=dbgon, shown_cnt=1)
    if len(_id_li) == 1:
        query = {'조건id':_id_li[0], 'predicted':event_num}
        projection = {'_id':0, '조건id':0}
        df = mg.find(db명=DB명, tbl명=SP_TBL명, query=query, projection=projection, dbgon=dbgon, 컬럼순서li=[], df보고형태='df')
        print(df.dtypes)
        return df
    else:
        print('\n 테이블 중복이네...씨발.\n')

def 유일한_사건번호_보고(dbgon=False):
    UTL_id_li = mg.distinct(db명=DB명, tbl명=SP_TBL명, col명='predicted', query=None, dbgon=dbgon, shown_cnt=1)




if __name__ == '__main__':
    print('\n' + '='*60 + sys.modules[__name__].__file__)
    #pp.pprint({'sys.path':sys.path})
    #pp.pprint({'dir()':dir()})

    #TW_Classifier(실험tbl명=userTL.PARSED_TBL, key_col='_id', 실험col명='text', 분류기_알고리즘='Perceptron', 훈련tbl명=None, 훈련col명=None, algorithm=None, sampling=None, n_clusters=None, dbgon=False, 사전검증=False)
    #TW_Classifier(실험tbl명=userTL.PARSED_TBL, key_col='_id', 실험col명='text', 분류기_알고리즘='MultinomialNB', 훈련tbl명='뉴스_ETRI언어분석', 훈련col명='뉴스본문srl_WSDNNGli', algorithm='KMeans', sampling=10000, n_clusters=2000, dbgon=False, 사전검증=False)

    #TW_Predicted_df_결과저장(실험tbl명=userTL.PARSED_TBL, 실험col명='text', 분류기_알고리즘='Perceptron', dbgon=False)

    #TW_Predicted_Orig_df로딩(test_tbl='트위터_유저타임라인', test_col='text', dbgon=False)





    #Classifier(훈련tbl명='뉴스_ETRI언어분석', 훈련col명='뉴스본문srl_WSDNNGli', algorithm='KMeans', sampling=10000, n_clusters=2000, 실험tbl명='트위터_유저타임라인', 실험col명='text', 분류기_알고리즘='MultinomialNB', dbgon=False, 사전검증=False)

    #트위터_분류예측값_결합()

    #XX_분류의_클러스터id_업뎃()

    #트윗_단위분류기(훈련col명='뉴스제목', dbgon=True, 사전검증=False)
    #TBL에_저장된_하나의_문서를_SP_TBL에_풀어헤치기(실험tbl명='트위터_유저타임라인', 실험col명='text', 분류기_알고리즘='MultinomialNB', dbgon=False, 사전검증=False)
    #트윗_분류기()

    #트위터_분류된_트윗을_사건번호_조건으로_로딩(event_num=109, 실험tbl명='트위터_유저타임라인', 실험col명='text', 분류기_알고리즘='MultinomialNB', dbgon=True)
    #유일한_사건번호_보고(dbgon=True)
