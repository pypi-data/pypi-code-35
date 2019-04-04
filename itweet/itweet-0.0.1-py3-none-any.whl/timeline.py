"""
============================== 핵심일 ==============================
클래스.
"""
# 패키지 라이브러리
from twitter import *

#doc#

# 나의 패키지
import __pymongo as mg
import __Twitter as twitter

# 오픈 패키지
import pandas as pd
import json
from datetime import datetime

# 직접적 라이브러리
from tweepy import Cursor

# 패키지 모듈
from twitter import auth


# 클래스들 내부 함수들
"""
from Twitter_TimelineCollector import *
from Twitter_TimelineParser import *
"""


def timeline_status_Inspection(status):
    print('\n' + '='*60 + inspect.stack()[0][3])
    """
    # Process a single status
    for status in page:
    """
    print('#'*60 + 'status')
    #pp.pprint({'type(status)':type(status)})
    #pp.pprint({'status':status})
    """<class 'tweepy.models.Status'>"""
    print('#'*60 + 'status._json')
    status_js = status._json
    pp.pprint({'status_js':status_js})
    pp.pprint({'type(status_js)':type(status_js)})
    """<class 'dict'>"""


def Timeline_파싱(RD_tbl명, tbl명, dbgon=False, 사전검증=False):
    import pandas as pd
    from pandas.io.json import json_normalize
    print('\n' + '='*60 + inspect.stack()[0][3])
    """
    ===== 작업순서 =====
    RD_TBL 로딩
    json_dump 컬럼값을 json화
    필요한 컬럼 추출

    ===== 자료구조 =====
    누가, 언제, 어디서, 무엇을, 어떻게, 왜, 기타
    ['user', 'created_at', 'place', 'geo', 'text', 'favorite_count', 'retweet_count']

    """
    입력 = {'사전검증':사전검증}
    if dbgon == True: pp.pprint({'입력':입력})

    트윗_주요컬럼 = ['user', 'created_at', 'place', 'geo', 'text', 'favorite_count', 'retweet_count']

    df = mg.find(db명=DB명, tbl명=RD_tbl명, query=None, projection=None, dbgon=dbgon, 컬럼순서li=[], df보고형태='df')
    dicli = df.to_dict('records')
    dicli_len = len(dicli)
    i=1
    for d in dicli:
        print('\n' + '-'*60 + '{}/{}'.format(i, dicli_len))
        """
        = = = = = = = = = = = = = = = 1차_파싱 = = = = = = = = = = = = = = =
        """
        print('\n' + '= '*30 + '1차_파싱')
        #js_str = d['json_dump']
        js_str = d['json_dump_li']
        dic = json.loads(js_str)
        dic['수집일시'] = d['수집일시']
        df = pd.DataFrame([dic])
        #print(df)
        """
        = = = = = = = = = = = = = = = 2차_파싱 = = = = = = = = = = = = = = =
        """
        print('\n' + '= '*30 + '2차_파싱')
        cols = 트윗_주요컬럼.copy()
        cols.append('수집일시')
        df1 = df.loc[:,cols]
        meta_cols = cols.copy()
        meta_cols.remove('user')
        df1['user'] = df1['user'].apply(lambda x: [x])
        df2 = json_normalize(data=df1.to_dict('records'), record_path='user', meta=meta_cols, meta_prefix=None, record_prefix='u_', errors='raise', sep='.')
        #print(df2)
        """
        = = = = = = = = = = = = = = = DateStr컬럼을_Datetime64로_변환 = = = = = = = = = = = = = = =
        """
        for col in ['created_at', 'u_created_at']:
            df2[col] = pd.to_datetime(arg=df2[col], errors='raise', dayfirst=False, yearfirst=False, utc=None, box=True, format=None, exact=True, unit=None, infer_datetime_format=False, origin='unix', cache=False)
        print('\n df.dtypes :\n', df.dtypes)


        dicli2 = df2.to_dict('records')
        """실제 dicli2 길이는 1. """
        #mg.insert_many(db명=DB명, tbl명=tbl명, dicli=dicli2, dbgon=dbgon, 사전검증=사전검증)

        i+=1
        #break


def Timeline_파싱_v2(RD_tbl명, tbl명, dbgon=False, 사전검증=False):
    import pandas as pd
    from pandas.io.json import json_normalize
    print('\n' + '='*60 + inspect.stack()[0][3])
    """
    ===== 작업순서 =====
    RD_TBL 로딩
    json_dump 컬럼값을 json화
    필요한 컬럼 추출

    ===== 자료구조 =====
    누가, 언제, 어디서, 무엇을, 어떻게, 왜, 기타
    ['user', 'created_at', 'place', 'geo', 'text', 'favorite_count', 'retweet_count']
    """
    입력 = {'RD_tbl명':RD_tbl명, 'tbl명':tbl명, '사전검증':사전검증}
    pp.pprint({'입력':입력})

    one_depth_cols = ['user', 'created_at', 'place', 'geo', 'text', 'favorite_count', 'retweet_count']

    df = mg.find(db명=DB명, tbl명=RD_tbl명, query=None, projection=None, dbgon=dbgon, 컬럼순서li=[], df보고형태='df')
    dicli = df.to_dict('records')
    dicli_len = len(dicli)
    i=1
    for d in dicli:
        print('\n' + '-'*60 + '{}/{}'.format(i, dicli_len))
        """
        = = = = = = = = = = = = = = = json_dump_파싱 = = = = = = = = = = = = = = =
        """
        print('\n' + '= '*30 + 'json_dump_파싱')
        js_str_li = d['json_dump_li']
        js_str_li_len = len(js_str_li)
        j=1
        dicli1 = []
        for js_str in js_str_li:
            print('\n' + '- '*30 + '{}/{}'.format(j, js_str_li_len))
            dic = json.loads(js_str)
            #dic['수집일시'] = d['수집일시']
            df_1 = pd.DataFrame([dic])
            #print(df)
            """
            = = = = = = = = = = = = = = = json_normalize_파싱 = = = = = = = = = = = = = = =
            """
            print('\n' + '= '*30 + 'json_normalize_파싱')
            #df_2 = df_1.loc[:, ['user']]
            df_2 = df_1.copy()
            df_2['user'] = df_2['user'].apply(lambda x: [x])
            meta_cols = one_depth_cols.copy()
            meta_cols.remove('user')
            df_3 = json_normalize(data=df_2.to_dict('records'), record_path='user', meta=meta_cols, meta_prefix=None, record_prefix='u_', errors='raise', sep='.')
            #print(df2)
            """
            = = = = = = = = = = = = = = = DateStr컬럼을_Datetime64로_변환 = = = = = = = = = = = = = = =
            """
            print('\n' + '= '*30 + 'DateStr컬럼을_Datetime64로_변환')
            for col in ['created_at', 'u_created_at']:
                df_3[col] = pd.to_datetime(arg=df_3[col], errors='raise', dayfirst=False, yearfirst=False, utc=None, box=True, format=None, exact=True, unit=None, infer_datetime_format=False, origin='unix', cache=False)
            #print('\n df2.dtypes :\n', df2.dtypes)
            """
            = = = = = = = = = = = = = = = 저장 = = = = = = = = = = = = = = =
            """
            dic_3 = df_3.to_dict('records')[0]
            print(len(df_3))
            """실제 dicli2 길이는 1. """
            dicli1.append(dic_3)
            j+=1
            #break
        """
        = = = = = = = = = = = = = = = 한사람당_df1_저장 = = = = = = = = = = = = = = =
        """
        print('\n' + '= '*30 + '한사람당_df1_저장')
        df1 = pd.DataFrame(dicli1)
        if dbgon == True:
            shown_cols = one_depth_cols.copy()
            shown_cols.remove('user')
            shown_cols = shown_cols + ['u_name', 'u_screen_name']
            print('\n shown_cols :\n')
            pp.pprint(shown_cols)
            df11 = df1.loc[:, shown_cols]
            print(df11)
            print('\n df11.dtypes :\n', df11.dtypes)

        pp.pprint({'저장할 df1_len':len(df1)})
        mg.insert_many(db명=DB명, tbl명=tbl명, dicli=df1.to_dict('records'), dbgon=dbgon, 사전검증=사전검증)
        i+=1
        #break
"""
============================== Handler ==============================
"""
def DateTypeCols_transform(dbgon=False, 사전검증=False):
    """
    수동 작업
    """
    projection = {'_id':1, 'created_at':1, 'u_created_at':1}
    if 사전검증 == True:
        df = mg.find_limit(db명=DB명, tbl명='트위터_유저타임라인', query=None, projection=projection, limit_cnt=1, dbgon=dbgon, 컬럼순서li=[], df보고형태='df')
    else:
        df = mg.find(db명=DB명, tbl명='트위터_유저타임라인', query=None, projection=projection, dbgon=dbgon, 컬럼순서li=[], df보고형태='df')

    for col in ['created_at', 'u_created_at']:
        df[col] = pd.to_datetime(arg=df[col], errors='raise', dayfirst=False, yearfirst=False, utc=None, box=True, format=None, exact=True, unit=None, infer_datetime_format=False, origin='unix', cache=False)
    print('\n df.dtypes :\n', df.dtypes)
    #print(df)

    dicli = df.to_dict('records')
    for d in dicli:
        query = {'_id':d['_id']}
        update = {'$set':d}
        mg.update_one(db명=DB명, tbl명='트위터_유저타임라인', query=query, update=update, upsert=False, dbgon=dbgon, 사전검증=사전검증)



if __name__ == '__main__':
    print('\n' + '='*60 + sys.modules[__name__].__file__)
    #pp.pprint({'sys.path':sys.path})
    #pp.pprint({'dir()':dir()})

    DateTypeCols_transform(dbgon=False, 사전검증=False)
