"""
============================== 핵심일 ==============================
주어지는 트위터 계정명에 대해, 팔로어, 팔로잉, 프로파일을
- 수집저장(.jsonl-type)
- 파일로 저장된 데이터를 파싱 후 데이터베이스에 저장.
"""
# 패키지 라이브러리
from twitter import *

#doc#


# 나의 패키지

# 오픈 패키지
import json
import pandas as pd
from datetime import datetime, date

# 클래스들 내부 서브클래스들

# 클래스들 내부 함수들

# 전역변수
from Twitter_ import *
TBL명 = '트위터_유저'


"""
============================== 수집 ==============================
"""
# 오픈 패키지
import json
import math
import os
import time


# 나의 패키지
import __pymongo as mg

# 패키지 모듈
from twitter import client

"""
============================== 수집저장 ==============================
"""
def collect_all(MAX_FRIENDS=15000, dbgon=False):
    whoami = dbg.whoami(sys.modules[__name__].__file__, inspect.stack()[0][3], dbgon)
    inputs = dbg.inputs(inspect.currentframe(), dbgon)
    """
    ===== 용어정의 =====
    ===== 사용법 =====
    user.collect_all
    ===== 작업순서 =====
    """
    client = client.auth(dbgon)
    collect_followers(client, screen_name, MAX_FRIENDS, dbgon)
    collect_friends(client, screen_name, MAX_FRIENDS, dbgon)
    collect_profile(client, screen_name, MAX_FRIENDS, dbgon)


def collect_followers(client, screen_name, MAX_FRIENDS=15000, dbgon=False):
    whoami = dbg.whoami(sys.modules[__name__].__file__, inspect.stack()[0][3], dbgon)
    inputs = dbg.inputs(inspect.currentframe(), dbgon)
    """
    ===== 용어정의 =====
    collect : 수집저장.
    screen_name : given user
    ===== 사용법 =====
    user.collect_followers
    ===== 작업순서 =====
    """
    A = "get user's profile"
    B = "get followers for a given user"
    C = "get friends for a given user"

    start_t = datetime.now()

    max_pages = math.ceil(MAX_FRIENDS / 5000)
    if dbgon == True: print('\n max_pages : {}\n'.format(max_pages))

    dirname = get_dirname(screen_name, dbgon)
    filepath = dirname + "/followers.jsonl"
    with open(filepath, 'w') as f:
        for followers in Cursor(client.followers_ids, screen_name=screen_name).pages(max_pages):
            for chunk in paginate(followers, 100):
                users = client.lookup_users(user_ids=chunk)
                for user in users:
                    dbg_userobj(user)
                    f.write(json.dumps(user._json)+"\n")
            if len(followers) == 5000:
                print("More results available. Sleeping for 60 seconds to avoid rate limit")
                time.sleep(60)


def collect_friends(client, screen_name, MAX_FRIENDS=15000, dbgon=False):
    whoami = dbg.whoami(sys.modules[__name__].__file__, inspect.stack()[0][3], dbgon)
    inputs = dbg.inputs(inspect.currentframe(), dbgon)
    """
    screen_name : given user
    ===== 작업순서 =====
    """
    A = "get user's profile"
    B = "get followers for a given user"
    C = "get friends for a given user"

    start_t = datetime.now()

    max_pages = math.ceil(MAX_FRIENDS / 5000)
    if dbgon == True: print('\n max_pages : {}\n'.format(max_pages))

    dirname = get_dirname(screen_name, dbgon)
    filepath = dirname + "/friends.jsonl"
    with open(filepath, 'w') as f:
        for friends in Cursor(client.friends_ids, screen_name=screen_name).pages(max_pages):
            for chunk in paginate(friends, 100):
                users = client.lookup_users(user_ids=chunk)
                for user in users:
                    dbg_userobj(user)
                    f.write(json.dumps(user._json)+"\n")
            if len(friends) == 5000:
                print("More results available. Sleeping for 60 seconds to avoid rate limit")
                time.sleep(60)


def collect_profile(client, screen_name, MAX_FRIENDS=15000, dbgon=False):
    whoami = dbg.whoami(sys.modules[__name__].__file__, inspect.stack()[0][3], dbgon)
    inputs = dbg.inputs(inspect.currentframe(), dbgon)
    """
    given user : screen_name
    ===== 작업순서 =====
    """
    A = "get user's profile"
    B = "get followers for a given user"
    C = "get friends for a given user"

    start_t = datetime.now()

    dirname = get_dirname(screen_name, dbgon)
    filepath = dirname + "/user_profile.json"
    with open(filepath, 'w') as f:
        profile = client.get_user(screen_name=screen_name)
        f.write(json.dumps(profile._json, indent=4))
"""
============================== 파싱저장 ==============================
"""
def save_in_db(tbl, user, start_t, user_relation, dbgon=False):
    whoami = dbg.whoami(sys.modules[__name__].__file__, inspect.stack()[0][3], dbgon)
    inputs = dbg.inputs(inspect.currentframe(), dbgon)
    """
    ===== 용어정의 =====
    tbl : 객체
    =====  =====
    user_type : follower, friend, ...
    ===== 작업순서 =====
    """
    dic = {
        'user_relation':user_relation,
        '수집일시':start_t,
        'json_dump':json.dumps(user_js)
    }
    tbl.insert_one(document=dic)
"""
============================== 내부 함수 ==============================
"""
def get_dirname(screen_name, dbgon):
    from datetime import date
    """."""
    today_str = date.today().isoformat()
    dirname = TW_DATA_PATH + "/users/{}/{}".format(screen_name, today_str)
    if dbgon == True: print('\n dirname : {}\n'.format(dirname))
    try:
        os.makedirs(dirname, mode=0o755, exist_ok=True)
    except OSError:
        print("Directory '{}' already exists.".format(dirname))
    except Exception as e:
        print("Error while creating directory '{}'".format(dirname))
        print("\n Exception :\n\n {}".format(e))
        sys.exit(1)
    else:
        return dirname


def paginate(items, n):
    """Generate n-sized chunks from items"""
    for i in range(0, len(items), n):
        yield items[i:i+n]


def dbg_userobj(user):
    print('\n' + '= '*30 + inspect.stack()[0][3])
    """"""
    print('\n type(user) : \n\n {}'.format(type(user)))
    print('\n user : \n\n {}'.format(user))

    user_js = user._json
    print('\n type(user._json) : \n\n {}'.format(type(user_js)))
    print('\n user._json : \n\n {}'.format(user_js))
"""
============================== 로딩 ==============================
"""
def load(수집구분조건col명='직업', 유저명=None, dbgon=False):
    print('\n' + '='*60 + inspect.stack()[0][3])
    """
    주요_트위터유저_정보_로딩
    별도 함수로 왜 만들어야 되지?
    """
    query = {수집구분조건col명:{'$ne':None}, 'name':{'$nin':u_name_li}}
    if 유저명 is not None:
        query.update({'name':{'$regex':유저명, '$options':'i'}})
    projection = {'_id':0, 'screen_name':1, 'name':1}
    df = mg.find(db명=DB명, tbl명=CORE_TRGT_TBL, query=query, projection=projection, dbgon=dbgon, 컬럼순서li=[], df보고형태='df')
    if dbgon == Trje: pp.pprint(sorted(df['name'].unique()))
    print(df.dtypes)
    return df
