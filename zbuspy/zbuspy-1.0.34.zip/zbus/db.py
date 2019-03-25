from zbus import Dict
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy import MetaData, text 
from sqlalchemy.sql.expression import select  , delete 

class Db:
    def __init__(self, engine, reflect=True): 
        self.engine = engine
        self.tables = {}
        self.models = {}
        self.meta = MetaData()
        if reflect:
            self._reflect()
        self.Session = sessionmaker(bind=self.engine)
    
    def _reflect(self): 
        self.meta.reflect(bind=self.engine)
        self.tables = self.meta.tables
        self.models = {}
        
    
    def query(self, sql, converter=None, **kvargs):  
        sql = text(sql)
        return self._query(sql, converter, **kvargs)
        
    def _query(self, s, converter=None, **kvargs):   
        rs = self.engine.execute(s, **kvargs)
        def c(row):
            if not converter: 
                r = Dict(row)  
                for name in r:   
                    c = r[name]
                    if isinstance(c, bytes): 
                        c = c.decode("utf-8")  
                    r[name] = c   
                return r
            return converter(r)
        return [c(row) for row in rs]  
        
    def query_one(self, sql, converter=None, **kvargs): 
        res = self.query(sql, converter, **kvargs)
        if len(res) > 0: return res[0]  
        
        
    def execute(self, sql, **kvargs):  
        sql = text(sql)
        return self.engine.execute(sql, **kvargs)
    
    def _check_table(self, table):
        if table not in self.tables:
            raise Exception('Table(%s) Not Found'%table)  
        return self.tables[table]
    
    def _primary_key(self, table):
        t = self._check_table(table)
        if len(t.primary_key) != 1:
            raise Exception('Table(%s) primary key not single'%table)  
        for c in t.primary_key:
            return (t, c)
        
    def _table_and_column(self, s):
        bb = s.split('.')
        if len(bb) != 2:
            raise Exception('Invalid table and column string: %s'%s)
        t = self._check_table(bb[0])
        if bb[1] not in t.c:
            raise Exception('Column(%s) not in Table(%s)'%(bb[1], bb[0]))
        return (t, bb[1])
    
    def link(self, data, left=None, right=None, link_col=None, middle=None, to_one=False):
        '''
        @param data: row or list of rows, represents left table object(s)
        @param left: "${table}.${left_column}", e.g. "paper.id"
        @param right: "${table}.${right_column}", e.g. "question.paper_id"
        @param middle: {left: '${middle_table}.${left_table_join_column}', right: '${middle_table}.${right_table_join_column}' }
        @param to_one: is mapping to just one record, such as one2one or many2one 
        @param link_col: link column name to add in data 
        '''
        if not data: return
        
        if left is None:
            raise Exception("left required")
        if right is None:
            raise Exception("right required")
        
        if not isinstance(data, (tuple, list)):
            data = [data]
        
        _, c1 = self._table_and_column(left)
        t2, c2 = self._table_and_column(right)
        
        if not link_col:
            link_col = "%ss"%c2
        
        left_key_values = set([row[c1] for row in data if c1 in row])
        link_table = self._batch_query(t2, c2, left_key_values)
        
        for row in data: 
            if c1 not in row: continue 
            left_key = row[c1]
            if left_key not in link_table:
                continue 
            link_data = link_table[left_key]
            if to_one:
                if len(link_data) > 1:
                    raise Exception("More than record found in Table(%s)"%t2.name)
                if len(link_data) == 1:
                    link_data = link_data[0]
                else:
                    link_data = None
            row[link_col] = link_data
    
    def _batch_query(self, t, col_name, value_set):
        value_set = list(value_set)
        if len(value_set) == 1: 
            s = select([t]).where(t.c[col_name] == value_set[0])  
        else:
            s = select([t]).where(t.c[col_name].in_(value_set))  
        data = self._query(s)
        res = {}
        for row in data:
            k = row[col_name]
            if k not in res:
                res[k] = [row]
            else:
                res[k].append(row)
        return res
    
    def delete(self, table, key):
        t, c_key = self._primary_key(table) 
        s = delete(t).where(t.c[c_key.name]==key)
        self.engine.execute(s)
    
    def one(self, table, key, c=None):
        res = self.list(table, key=[key], c=c)
        if res and len(res) >= 1:
            return res[0] 
        
    
    def list(self, table, p=0, n=100, c=None, key=None, key_name=None): 
        '''
        @param table: table mapping name(table raw name by default)
        @param p: page index
        @param n: size of page
        @param c: column list
        @param key: key list or single key
        @param key_name: replace the primary key if set 
        '''
        t = self._check_table(table) 
        c_list = [t]
        if c:
            if not isinstance(c, (list, tuple)):
                c = [c]
            c_list = [t.c[name] for name in c if name in t.c] 
                
        s = select(c_list)
        if key: 
            if not key_name:
                _, k = self._primary_key(table) 
                key_name = k.name 
            if not isinstance(key, (list, tuple)):
                key = [key]
                
            if len(key) == 1:
                s = s.where(t.c[key_name].op('=')(key[0]))
            else:
                s = s.where(t.c[key_name].in_(key))
        else:
            if n:
                page = int(p)
                page_size = int(n) 
                s = s.limit(page_size)
                s = s.offset(page*page_size)
        
        return self._query(s) 
    
        
    def save(self, table, json_data, session=None, commit=True): 
        '''
        @param table: json_data's table name
        @param json_data: json format of json_data
        @param session: shared if given, otherwise creation inside
        @param commit: commit by default 
        '''  
        self._check_table(table)
        
         
        model_class = self.models.get(table) 
        t = self.tables[table]  
        if not model_class: 
            class Model: pass
            model_class = Model
            mapper(Model, t)
            self.models[table] = Model  
        
        m = model_class() 
        for key in json_data:  
            setattr(m, key, json_data[key])   
        
        pk_populated = True
        for c in t.primary_key:
            if c.name not in json_data:
                pk_populated = False
                break
        
        own_session = False
        if not session:
            own_session = True
            session = self.Session() 
        try: 
            if pk_populated:
                session.merge(m)
            else:
                session.add(m) 
            if commit:
                session.commit()
            else:
                session.flush()
            res = {}
            for c in t.primary_key:
                res[c.name] = getattr(m, c.name)
            return res
        finally:
            if session and own_session:
                session.close()   
                
                
                