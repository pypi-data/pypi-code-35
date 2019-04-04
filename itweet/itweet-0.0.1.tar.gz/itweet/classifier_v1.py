"""
============================== 핵심일 ==============================
클래스다.

===== 용어 정의 =====
SP_TBL : spread_tbl
clf : classifier

===== 자료구조 : TBL 구조 =====
_id            object  -> 조건id
클러스터id -> trainset_id
분류기_알고리즘       object
분류예측값_dicli    object
실험자료tbl명       object
실험자료col명       object

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
훈련자료col명='뉴스제목'
훈련분류tbl명='뉴스_클러스터'
훈련분류col명 = 'label'
클러스터_알고리즘 = 'KMeans'

실험자료tbl명 = '트위터_유저타임라인' -> 거의 고정
실험자료col명 = 'text' -> 거의 고정
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

# 전역변수
TBL명 = 'XX_분류기'
#TBL명 = '트위터_분류기_예측결과'
#SP_TBL명 = TBL명 + '_확장'



"""
==============================  ==============================
"""

def Classifier(train_df, 타겟tbl명='뉴스_ETRI언어분석', 타겟col명='뉴스본문srl_WSDNNGli', algorithm='KMeans', sampling=10000, n_clusters=2000, dbgon=False):
    print('\n' + '='*60 + inspect.stack()[0][3])
    """
    분류기 훈련
    """

    keyid_li = list(train_df['keyid'])
    query = {d['키col명']:{'$in':keyid_li}}
    projection = {'_id':0, d['키col명']:1, d['타겟col명']:1}
    df2 = mg.find(db명=DB명, tbl명=d['타겟tbl명'], query=query, projection=projection, dbgon=False, 컬럼순서li=[], df보고형태='df')


def 트윗_분류기():
    트윗_단위분류기(훈련자료col명='뉴스제목', 분류기_알고리즘='MultinomialNB')
    TBL에_저장된_하나의_문서를_SP_TBL에_풀어헤치기(실험자료tbl명='트위터_유저타임라인', 실험자료col명='text', 분류기_알고리즘='MultinomialNB', dbgon=False, 사전검증=False)



def 트윗_단위분류기(훈련자료col명='뉴스제목', 분류기_알고리즘='MultinomialNB', dbgon=False, 사전검증=False):
    print('\n'+'='*60+inspect.stack()[0][3])
    """
    ===== 작업순서 =====
    훈련자료모음(훈련자료 + 그 분류값) 로딩 -> 뉴스XX와 그로부터 클러스터된 라벨
    실험자료 로딩
    분류기_예측
    실험자료의 분류예측결과 저장
    """
    #if dbgon == True: print(설명)
    #입력 = {'tbl명':tbl명, 'clst타겟col명':clst타겟col명, 'algorithm':algorithm, 'n_clusters':n_clusters}
    #if dbgon == True: pp.pprint({'입력':입력})

    훈련자료tbl명 = '뉴스'
    훈련분류col명 = 'label'
    실험자료tbl명 = '트위터_유저타임라인'
    실험자료col명 = 'text'
    실험분류col명 = 'predicted'
    #분류기_알고리즘 = 'MultinomialNB'


    clf결과저장_dic = {
        '실험자료tbl명':실험자료tbl명,
        '실험자료col명':실험자료col명,
        '분류기_알고리즘':분류기_알고리즘,
        '분류예측값_dicli':[],
    }
    train_df = 훈련자료모음_로딩(훈련자료tbl명, 훈련자료col명, 훈련분류col명, dbgon)
    train_df = 훈련자료col_dtype_검사조작(train_df, 훈련자료col명)
    if train_df is not None:
        test_df = 실험자료_로딩(실험자료tbl명, 실험자료col명, dbgon)


        훈련자료 = train_df[훈련자료col명]
        훈련분류값 = train_df[훈련분류col명]
        실험자료 = test_df[실험자료col명]
        실험자료_분류예측값_li = 분류기_예측(분류기_알고리즘, 훈련자료, 훈련분류값, 실험자료, dbgon)
        test_df[실험분류col명] = 실험자료_분류예측값_li

        return test_df
        #분류기_결과보고(df, 키col명)
        분류기_결과저장(test_df, 실험분류col명, clf결과저장_dic, dbgon, 사전검증)


def 훈련자료모음_로딩(훈련자료tbl명, 훈련자료col명, 훈련분류col명, dbgon):
    print('\n'+'='*60+inspect.stack()[0][3])

    df = news.ClstReport.clst결과로_타겟자료를_결합해서_df로딩(타겟tbl명=훈련자료tbl명, 타겟col명=훈련자료col명, clst타겟col명=훈련자료col명, dbgon=False)
    df = df.loc[:,['_id', 훈련자료col명, 훈련분류col명]]
    return df


def 훈련자료col_dtype_검사조작(df, 훈련자료col명):
    print('\n'+'='*60+inspect.stack()[0][3])

    훈련자료_dtype = type(list(df[훈련자료col명])[0])
    pp.pprint({'훈련자료_dtype':훈련자료_dtype})
    if 훈련자료_dtype is str:
        return df
    elif 훈련자료_dtype is list:
        s = datetime.now()
        df[훈련자료col명] = df[훈련자료col명].apply(lambda x: ' '.join(x))
        pp.pprint({'실행시간_sec':(datetime.now() - s).total_seconds()})
        return df
    else:
        print('\n clst타겟col명의 값은 문자열/리스트 여야 한다.\n')
        return None


def 실험자료_로딩(실험자료tbl명, 실험자료col명, dbgon):
    print('\n'+'='*60+inspect.stack()[0][3])

    projection = {'_id':1, 실험자료col명:1, 'u_created_at':1, 'u_screen_name':1}
    df = mg.find(db명=DB명, tbl명=실험자료tbl명, query=None, projection=projection, dbgon=dbgon, 컬럼순서li=[], df보고형태='df')
    print('\n df 중복제거.\n')
    pp.pprint(len(df))
    df = df.drop_duplicates(subset=[실험자료col명,'u_created_at','u_screen_name'], keep='first', inplace=False)
    pp.pprint(len(df))
    return df


def 분류기_예측(분류기_알고리즘, 훈련자료, 훈련분류값, 실험자료, dbgon):
    print('\n'+'='*60+inspect.stack()[0][3])

    if 분류기_알고리즘 == 'MultinomialNB':
        실험자료_분류예측값_li = skl.supervised_TextData_classifier(trainset_data=훈련자료, trainset_target=훈련분류값, testset_data=실험자료, dbgon=dbgon)
    elif 분류기_알고리즘 == 'Perceptron':
        실험자료_분류예측값_li = skl.language_train_model(train_docs=훈련자료, train_label=훈련분류값, test_docs=실험자료)

    return 실험자료_분류예측값_li


def 분류기_결과보고(df, 키col명):
    print('\n'+'='*60+inspect.stack()[0][3])


    g = df.groupby('label').count().sort_values(키col명, ascending=False)
    print(g)


def 분류기_결과저장(df, 실험분류col명, clf결과저장_dic, dbgon, 사전검증):
    print('\n'+'='*60+inspect.stack()[0][3])
    """
    insert_one 이라도 데이타가 커서 dbgon 강제 False
    """

    df = df.loc[:,['_id', 실험분류col명]]
    clf결과저장_dic['분류예측값_dicli'] = df.to_dict('records')
    mg.insert_one(db명=DB명, tbl명=TBL명, dic=clf결과저장_dic, dbgon=False, 사전검증=사전검증)


def TBL에_저장된_하나의_문서를_SP_TBL에_풀어헤치기(실험자료tbl명='트위터_유저타임라인', 실험자료col명='text', 분류기_알고리즘='MultinomialNB', dbgon=False, 사전검증=False):
    from pandas.io.json import json_normalize
    print('\n'+'='*60+inspect.stack()[0][3])
    """
    ===== 작업순서 =====
    TBL에서 특정조건으로, _id과 분류예측값_dicli 컬럼만, 문서를 로딩
    _id 명을 "조건id" 로 이름을 바꿈.
    중복을 제거 -> 최초만 남기나?
    풀어헤쳐서,
    분류예측값_dicli 을 json_normalize
    여기의 _id를 "XXid" 로 이름을 변경.
    조건id 를 신규컬럼으로 추가.
    저장.
    """
    실험자료id명 = 'UTL_id'

    query = {'실험자료tbl명':실험자료tbl명, '실험자료col명':실험자료col명, '분류기_알고리즘':분류기_알고리즘}
    df = mg.find(db명=DB명, tbl명=TBL명, query=query, projection=None, dbgon=dbgon, 컬럼순서li=[], df보고형태='df')
    df = df.drop_duplicates(subset=['실험자료tbl명', '실험자료col명', '분류기_알고리즘'], keep='first', inplace=False)
    df = df.rename(columns={'_id':'조건id'})
    #print(df.dtypes)


    print('\n'+'= '*30+'풀어헤치기')
    if len(df) == 1:
        dic = df.to_dict('records')[0]
        조건id = dic['조건id']
        분류예측값_dicli = dic['분류예측값_dicli']
        #return None
        df1 = json_normalize(data=분류예측값_dicli, record_path=None, meta=None, meta_prefix=None, record_prefix=None, errors='raise', sep='.')
        df1 = df1.rename(columns={'_id':실험자료id명})
        df1 = df1.assign(조건id= 조건id)
        print(df1.dtypes)
        print(len(df1))
        dicli = df1.to_dict('records')
        mg.insert_many(db명=DB명, tbl명=SP_TBL명, dicli=dicli, dbgon=dbgon, 사전검증=사전검증)

    else:
        print('\n 이럴리 없자나? \n')


def 트위터_분류된_트윗을_사건번호_조건으로_로딩(event_num, 실험자료tbl명='트위터_유저타임라인', 실험자료col명='text', 분류기_알고리즘='MultinomialNB', dbgon=False):
    print('\n'+'='*60+inspect.stack()[0][3])
    """
    데이터 양이 엄청나기 때문에(30만 이상) event_num는 필수 파라미터다.
    TBL과 SP_TBL 간의 확장/reduce 특수성으로 인해 로딩 함수가 반드시 필요하다.

    ===== 용어정의 =====
    event_num : label, predicted, 사건번호, 사건id ....다 같은 말.
    """

    query = {'실험자료tbl명':실험자료tbl명, '실험자료col명':실험자료col명, '분류기_알고리즘':분류기_알고리즘}
    _id_li = mg.distinct(db명=DB명, tbl명=TBL명, col명='_id', query=query, dbgon=dbgon, shown_cnt=1)
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

    #트윗_단위분류기(훈련자료col명='뉴스제목', dbgon=True, 사전검증=False)
    #TBL에_저장된_하나의_문서를_SP_TBL에_풀어헤치기(실험자료tbl명='트위터_유저타임라인', 실험자료col명='text', 분류기_알고리즘='MultinomialNB', dbgon=False, 사전검증=False)
    #트윗_분류기()

    #트위터_분류된_트윗을_사건번호_조건으로_로딩(event_num=109, 실험자료tbl명='트위터_유저타임라인', 실험자료col명='text', 분류기_알고리즘='MultinomialNB', dbgon=True)
    유일한_사건번호_보고(dbgon=True)
