from idebug import *

"""
def tbl_structure(tbl, query=None, projection=None):
    print('\n' + '='*60 + whoami(sys.modules[__name__].__file__, inspect.stack()[0][3]))
    inputs = inputs(inspect.currentframe(), dbgon=True)

    테이블에 대한 자료구조를 확인한다.
    tbl : collection_obj.
    find_one : {'반복1회_평균실행시간_초': 0.003278, '잔여반복_예상실행시간_초': 0.0, '전체반복_예상실행시간_초': 0.003278}
    find.limit : {'반복1회_평균실행시간_초': 0.005471, '잔여반복_예상실행시간_초': 0.0, '전체반복_예상실행시간_초': 0.005471}
    ===== 사용법 =====
    tbl_structure(db=DB, tbl=TBL, query=None, projection=None, dbgon=True)

    start_t = datetime.now()

    #df = mg.find_limit(db=DB, tbl=tbl, query=query, projection=projection, limit_cnt=1, dbgon=dbgon, 컬럼순서li=[], df보고형태='df')
    cursor = tbl.find(filter=None).limit(1)
    df = pd.DataFrame(list(cursor))
    #df = pd.DataFrame(list( db[tbl].find_one(filter=None) ))
    caller = sys.modules[__name__].__file__ + '_:_' + inspect.stack()[0][3]
    funclog(caller=caller, start_t=start_t, addt_i={}, RunTimeout=10)
    df_structure(df)
"""


def cursor_explain(cursor):
    """https://api.mongodb.com/python/current/api/pymongo/cursor.html"""
    cursor.explain()

def filter_update(filter, update, title='_None'):
    print(f"\n{'*'*60}\n Debug filter, update params  : {title}\n\n\n filter :")
    pp.pprint(filter)
    print(f"\n update :")
    pp.pprint(update)

#============================================================
# https://api.mongodb.com/python/current/api/pymongo/results.html#pymongo.results.UpdateResult
#============================================================

def UpdateResult(clss):
    print(f"\n{'*'*60}\n UpdateResult.acknowledged : {clss.acknowledged}")
    print(f"\n UpdateResult.matched_count : {clss.matched_count}")
    print(f"\n UpdateResult.modified_count : {clss.modified_count}")
    print(f"\n UpdateResult.raw_result : {clss.raw_result}")
    print(f"\n UpdateResult.upserted_id : {clss.upserted_id}")

def UpdateResults(obj):
    docs = []
    for UpdateResult in obj.UpdateResults:
        doc = {
            'acknowledged':UpdateResult.acknowledged,
            'matched_count':UpdateResult.matched_count,
            'modified_count':UpdateResult.modified_count,
            'raw_result':UpdateResult.raw_result,
            'upserted_id':UpdateResult.upserted_id
        }
        docs.append(doc)
    df = pd.DataFrame(docs)
    print_df(df)
    g = df.groupby('modified_count').count()
    print_df(g)

#============================================================
# https://api.mongodb.com/python/current/api/pymongo/results.html#pymongo.results.InsertManyResult
#============================================================

def InsertManyResult(clss):
    print(f"\n{'*'*60}\n InsertManyResult.acknowledged : {clss.acknowledged}")
    print(f"\n InsertManyResult.inserted_ids : {clss.inserted_ids}")

def InsertOneResult(clss):
    print(f"\n{'*'*60}\n InsertOneResult.acknowledged : {clss.acknowledged}")
    print(f"\n InsertOneResult.inserted_id : {clss.inserted_id}")

def DeleteResult(clss):
    print(f"\n{'*'*60}\n DeleteResult.acknowledged : {clss.acknowledged}")
    print(f"\n DeleteResult.deleted_count : {clss.deleted_count}")
    print(f"\n DeleteResult.raw_result : {clss.raw_result}")
