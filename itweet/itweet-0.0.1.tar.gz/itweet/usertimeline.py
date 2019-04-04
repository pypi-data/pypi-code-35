"""
============================== 핵심일 ==============================
클래스.
"""
# 패키지 라이브러리
from twitter import *

#doc#

# 나의 패키지
import __Twitter as twitter
import __pymongo as mg

# 오픈 패키지
import json
from datetime import datetime
# 직접적 라이브러리
from tweepy import Cursor

# 패키지 모듈
from twitter import auth
import Twitter_Timeline as tline

# 전역변수
from Twitter_ import *
PARSED_TBL = '트위터_유저타임라인'
RD_TBL = PARSED_TBL + '_원본'
CORE_TRGT_TBL = '트위터_유저_수집주요타겟'
CORE_COLS = ['u_name', 'u_screen_name', 'created_at', 'text']

"""
============================== 흐름제어 ==============================
"""
def 유저타임라인_흐름제어(dbgon=False, 사전검증=False):
    정치인등_주요핵심_트위터유저들의_유저타임라인_수집(수집구분조건col명='직업', 유저명=None, count=100, pages=10, dbgon=dbgon)
    #UserTimeline_파싱(dbgon, 사전검증)

"""
============================== 수집 ==============================
"""
def 정치인등_주요핵심_트위터유저들의_유저타임라인_수집(수집구분조건col명='직업', 유저명=None, count=200, pages=16, dbgon=False):
    print('\n' + '='*60 + inspect.stack()[0][3])
    """
    sorted(df['직업'].unique())
    - TypeError: '<' not supported between instances of 'float' and 'str'
    - TypeError: '<' not supported between instances of 'NoneType' and 'str'
    """
    입력 = {'수집구분조건col명':수집구분조건col명, '유저명':유저명, 'count':count, 'pages':pages}
    if dbgon == True: pp.pprint({'입력':입력})
    """
    = = = = = = = = = = = = = = = 수집타겟_트위터유저_정보_및_AUTH_로딩 = = = = = = = = = = = = = = =
    """
    print('\n' + '= '*30 + '수집타겟_트위터유저_정보_및_AUTH_로딩')
    df = 주요_트위터유저_정보_로딩(수집구분조건col명='직업', 유저명=None, dbgon=False)


    tw_clnt = auth.twitter_client(dbgon)
    """
    = = = = = = = = = = = = = = = screen_name별_반복수집 = = = = = = = = = = = = = = =
    """
    print('\n' + '= '*30 + 'screen_name별_반복수집')
    screen_name_li = list(df['screen_name'])
    sn_li_len = len(screen_name_li)
    i=1
    for sn in screen_name_li:
        print('\n' + '-'*60 + '{}/{}, screen_name:{}'.format(i, sn_li_len, sn))
        get_user_timeline(tw_clnt, sn, count, pages, dbgon)
        i+=1
        #break


def get_user_timeline(tw_clnt, screen_name, count=200, pages=16, dbgon=False):
    print('\n' + '='*60 + inspect.stack()[0][3])
    시작시간 = datetime.now()
    입력 = {'screen_name':screen_name, 'count':count, 'pages':pages}
    pp.pprint({'입력':입력})

    json_dump_li = []
    i=1
    for page in Cursor(tw_clnt.user_timeline, screen_name=screen_name, count=count).pages(pages):
        print('\n' + '-'*60 + 'page_i:{}'.format(i))
        j=1
        for status in page:
            print('\n' + '-'*60 + 'status_j:{}'.format(j))
            if dbgon == True: tline.timeline_status_Inspection(status=status)
            json_dump_li.append( json.dumps(status._json) )
            j+=1
            #break
        i+=1
        #break

    dic = {
        'screen_name':screen_name,
        'json_dump_li':json_dump_li,
        '수집일시':시작시간,
    }
    mg.insert_one(db명=DB명, tbl명=RD_TBL, dic=dic, dbgon=dbgon, 사전검증=False)
    if dbgon == True: dbg.funclog(caller=inspect.stack()[0][3], 시작시간=시작시간, 추가정보_dic=입력)
"""
============================== 로딩 ==============================
"""
def UserTimeline_로딩(AssmblMan=True, prjct_cols=None, dbgon=False):
    import People as ppl
    print('\n' + '='*60 + inspect.stack()[0][3])

    core_cols = ['u_screen_name', 'created_at', 'text']

    query = {'created_at':{'$gte':datetime(2018, 1, 1)}}
    if AssmblMan == True:
        pol_df = ppl.assem.국회의원현황_로딩(dbgon=dbgon)
        이름_li = list(pol_df['이름'])
        query.update({'u_name':{'$in':이름_li}})
    projection = None if prjct_cols==None else {e:1 for e in prjct_cols}
    #projection = {'_id':1, 'text':1, 'created_at':1, 'u_screen_name':1}
    df = mg.find(db명=DB명, tbl명=PARSED_TBL, query=query, projection=projection, dbgon=dbgon, 컬럼순서li=[], df보고형태='df')

    """
    """

    return df
"""
============================== 파싱 ==============================
"""
def UserTimeline_파싱(dbgon=False, 사전검증=False):
    print('\n' + '='*60 + inspect.stack()[0][3])
    """
    = = = = = = = = = = = = = = = RD_TBL의_파싱대상_선정 = = = = = = = = = = = = = = =
    """
    print('\n' + '= '*30 + 'RD_TBL의_파싱대상_선정')
    #query = {'파싱완료':{'$ne':None}}
    #df = mg.find(db명=DB명, tbl명=RD_TBL, query=query, projection=None, dbgon=dbgon, 컬럼순서li=[], df보고형태='df')
    tline.Timeline_파싱_v2(RD_tbl명=RD_TBL, tbl명=PARSED_TBL, dbgon=dbgon, 사전검증=사전검증)

"""
============================== Handler ==============================
"""
def 삭제():
    from datetime import datetime
    query = {'수집일시':{'$gte':datetime(2018, 9, 12)}}
    mg.delete_many(db명=DB명, tbl명='트위터_유저타임라인_원본', query=query, dbgon=True, 사전검증=False)

def UserTimelineTBL_중복제거(action='검사', dbgon=False):
    print('\n' + '='*60 + inspect.stack()[0][3])
    """
    pymongo.errors.OperationFailure: distinct too big, 16mb cap
    """
    """
    = = = = = = = = = = = = = = = 핵심컬럼별_유일값_개수_검사 = = = = = = = = = = = = = = =
    """
    print('\n' + '= '*30 + '핵심컬럼별_유일값_개수_검사')
    cols = ['u_name', 'u_screen_name', 'created_at']
    cols_len = len(cols)
    i=1
    dic = {}
    for col in cols:
        print('\n' + '-'*60 + '{}/{}, 컬럼명:{}'.format(i, cols_len, col))
        uq_ColVal_li = mg.distinct(db명=DB명, tbl명=PARSED_TBL, col명=col, query=None, dbgon=dbgon, shown_cnt=1)
        dic[col] = len(uq_ColVal_li)
        i+=1

    pp.pprint(dic)
    """
    = = = = = = = = = = = = = = = 핵심컬럼으로_중복_검사 = = = = = = = = = = = = = = =
    first : Mark duplicates as True except for the first occurrence.
    """
    print('\n' + '= '*30 + '핵심컬럼으로_중복_검사')
    subset = cols + ['text']
    projection = {col:1 for col in subset}
    df = mg.find(db명=DB명, tbl명=PARSED_TBL, query=None, projection=projection, dbgon=dbgon, 컬럼순서li=[], df보고형태='df')
    pp.pprint({'원본 df_len':len(df)})
    df_ = df[ df.duplicated(subset=subset, keep='first') ]
    pp.pprint({'중복된 df_len':len(df_)})

    if action == '삭제':
        """
        = = = = = = = = = = = = = = = 중복_문서를_id조건으로_삭제 = = = = = = = = = = = = = = =
        first : Mark duplicates as True except for the first occurrence.
        """
        print('\n' + '= '*30 + '중복_문서를_id조건으로_삭제')
        dupl_id_li = df_['_id']
        query = {'_id':{'$in':dupl_id_li}}
        mg.delete_many(db명=DB명, tbl명=PARSED_TBL, query=query, dbgon=dbgon, 사전검증=False)




if __name__ == '__main__':
    print('\n' + '='*60 + sys.modules[__name__].__file__)
    #pp.pprint({'sys.path':sys.path})
    #pp.pprint({'dir()':dir()})

    #UserTimeline_파싱(dbgon=False, 사전검증=False)
    #유저타임라인_흐름제어(dbgon=False, 사전검증=False)
    #정치인등_주요핵심_트위터유저들의_유저타임라인_수집(수집구분조건col명='직업', 유저명=None, count=50, pages=5, dbgon=False)
    #UserTimeline_로딩(AssmblMan=True, prjct_cols=['_id', 'text'], dbgon=False)

    #UserTimeline_파싱(dbgon=False, 사전검증=False)
    """
    ============================== Handler ==============================
    """
    #UserTimelineTBL_중복제거(action='삭제', dbgon=False)
