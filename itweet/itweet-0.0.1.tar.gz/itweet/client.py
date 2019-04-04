"""
============================== 핵심일 ==============================
"""
# 패키지 라이브러리
from twitter import *

#doc#

# 나의 패키지

# 오픈 패키지

# 직접적 라이브러리

def auth(dbgon=False):
    whoami = dbg.whoami(sys.modules[__name__].__file__, inspect.stack()[0][3], dbgon)
    inputs = dbg.inputs(inspect.currentframe(), dbgon)
    from tweepy import API, OAuthHandler
    """
    """
    query = {'제공자명':'twitter'}
    tbl = db['오픈API_인증정보']
    curosr = tbl.find(filter=query)
    keys_access_token_dicli = list(cursor)
    #keys_access_token_dicli = mg.find(db명='lib', tbl명='오픈API_인증정보', query=query, projection=None, dbgon=dbgon, 컬럼순서li=[], df보고형태='dicli')
    dic = keys_access_token_dicli[0]
    if dbgon == True: print('\n keys_access_token_dic :\n\n {}'.format(dic))

    auth = OAuthHandler(dic['아이디'], dic['비밀번호'])
    auth.set_access_token(dic['접속토큰'], dic['접속토큰비번'])
    if dbgon == True: print('\n auth :\n\n {}'.format(auth))

    client = API(auth)
    if dbgon == True: print('\n API(auth) :\n\n {}'.format(client))
    return client
