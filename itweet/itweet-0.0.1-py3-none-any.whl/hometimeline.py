"""
============================== 핵심일 ==============================
클래스.
"""
# 패키지 라이브러리
from twitter import *

#doc#

# 오픈 패키지
import json
from datetime import datetime
# 직접적 라이브러리
from tweepy import Cursor

# 패키지 모듈
from twitter import auth
import Twitter_Timeline as tline
from Twitter_ import *

# 전역변수
PARSED_TBL = '트위터_홈타임라인'
RD_TBL = PARSED_TBL + '_원본'


"""
============================== 수집 ==============================
"""

def get_home_timeline(count=200, 페이지수=100, dbgon=False):
    print('\n'+'='*60+inspect.stack()[0][3])
    """
    ===== 에러 =====
    1.
    tweepy.error.TweepError: Twitter error response: status code = 429

    2. pp.pprint({'status.keys()':status.keys()})
    AttributeError: 'Status' object has no attribute 'keys'

    3. mg.insert_one
    TypeError: Object of type 'ObjectId' is not JSON serializable
    """
    시작시간 = datetime.now()
    입력 = {'count':count, '페이지수':페이지수}
    if dbgon == True: pp.pprint({'입력':입력})


    tw_clnt = auth.twitter_client(dbgon=dbgon)
    file_path = TW_DATA_PATH + '/home_timeline.jsonl'
    if dbgon == True: pp.pprint({'file_path':file_path})


    with open(file_path, 'w') as f:
        i=1
        for page in Cursor(tw_clnt.home_timeline, count=count, include_rts=True).pages(페이지수):
            print('\n'+'-'*60+' i:{}'.format(i))
            j=1
            for status in page:
                """# Process a single status"""
                print('\n'+'- '*30+' j:{}'.format(j))
                if dbgon == True: tline.timeline_status_InspectionSave(tbl명=RD_TBL, status=status, 시작시간=시작시간, dbgon=dbgon)
                f.write(json.dumps(status._json)+"\n")
                j+=1
            i+=1

        if dbgon == True: dbg.funclog(caller=inspect.stack()[0][3], 시작시간=시작시간, 추가정보_dic=입력)


"""
============================== 파싱 ==============================
"""
import Twitter_Timeline as tline

def HomeTimeline_파싱(dbgon=False, 사전검증=False):
    print('\n'+'='*60+inspect.stack()[0][3])
    tline.Timeline_파싱(RD_tbl명=RD_TBL, tbl명=PARSED_TBL, dbgon=dbgon, 사전검증=사전검증)


if __name__ == '__main__':
    print('\n' + '='*60 + sys.modules[__name__].__file__)
    pp.pprint({'sys.path':sys.path})
    pp.pprint({'dir()':dir()})
