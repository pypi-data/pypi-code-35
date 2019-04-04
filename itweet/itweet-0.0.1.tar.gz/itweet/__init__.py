
"""
============================== 핵심일 ==============================
패키지 만들기.
자료구조 정의.
패키지 기본 라이브러리 제공.
"""
import sys



# 패키지 전역변수
PKG_NAME = 'twiiter'
DEFAULT_PATH = '/Users/sambong/p'
LIB_PATH = DEFAULT_PATH + '/lib'
PKG_PATH = LIB_PATH + '/' + PKG_NAME
DATA_PATH = PKG_PATH + '/data'

SCREEN_NAME = '1nnovata'
DEDUPLICATE_COLS = ['u_name', 'u_screen_name', 'created_at', 'text']

# 나의 패키지
sys.path.append(LIB_PATH)
import __debug as dbg

# 오픈 패키지
import inspect
import pprint
pp = pprint.PrettyPrinter(indent=2)
from datetime import datetime
