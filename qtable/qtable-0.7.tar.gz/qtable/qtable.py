from qtable.engine import *
import pandas as pd
import numpy as np
import copy


class Qtable():
    def __init__(self,**kwargs):
        if('allow_duplicates' in kwargs):
            self.allow_duplicates = kwargs['allow_duplicates']
        else:
            self.allow_duplicates = True
        if('df' in kwargs):
            self.df = kwargs['df']
            self.columns = self.df.columns
            self.index = self.df.index
            self.colnums = self.columns.__len__()
            self.rownums = self.index.__len__()
        else:
            self.columns = kwargs['columns']
            self.index = kwargs['index']
            self.colnums = self.columns.__len__()
            self.rownums = self.index.__len__()
            if("mat" in kwargs):
                mat = kwargs['mat']
            else:
                mat = np.full((self.rownums,self.colnums),None)
            self.df = pd.DataFrame(mat, columns=self.columns,index=self.index)
        self.index_map = _index_map(self.df)
        self.columns_map = _columns_map(self.df)
    def __repr__(self):
        return(self.df.__repr__())
    def __getitem__(self,*args):
        args = list(args)[0]
        rowname,colname = args[:2]
        if(self.allow_duplicates):
            return(_getitem(self.df,rowname,colname,*args[2:],index_map=self.index_map,columns_map=self.columns_map))
        else:
            return(_getitem(self.df,rowname,colname,0,0,index_map=self.index_map,columns_map=self.columns_map))
    def __setitem__(self,*args):
        value = list(args)[1]
        args = list(args)[0]
        rowname,colname = args[:2]
        if(self.allow_duplicates):
            _setitem(self.df,rowname,colname,value,*args[2:],index_map=self.index_map,columns_map=self.columns_map)
        else:
            _setitem(self.df,rowname,colname,value,0,0,index_map=self.index_map,columns_map=self.columns_map)
    def row(self,rowname,*args):
        if(self.allow_duplicates):
            df = _row(self.df,rowname,*args,index_map=self.index_map,columns_map=self.columns_map)
        else:
            df = _row(self.df,rowname,0,index_map=self.index_map,columns_map=self.columns_map)
        return(Qtable(df=df))
    def col(self,colname,*args):
        if(self.allow_duplicates):
            df = _col(self.df,colname,*args,index_map=self.index_map,columns_map=self.columns_map)
        else:
            df = _col(self.df,colname,0,index_map=self.index_map,columns_map=self.columns_map)
        return(Qtable(df=df))
    def rows(self,*rownames):
        df = _rows(self.df,*rownames,index_map=self.index_map,columns_map=self.columns_map)
        return(Qtable(df=df))
    def cols(self,*colnames):
        df = _cols(self.df,*colnames,index_map=self.index_map,columns_map=self.columns_map)
        return(Qtable(df=df))
    def subtb(self,rownames,colnames):
        df = _subtb(self.df,rownames,colnames,index_map=self.index_map,columns_map=self.columns_map)
        return(Qtable(df=df))
    def crop(self,top,left,bot,right):
        df = _crop(self.df,top,left,bot,right,index_map=self.index_map,columns_map=self.columns_map)
        return(Qtable(df=df))
    def swapcol(self,colname1,colname2,*args):
        if(self.allow_duplicates):
            df = _swapcol(self.df,colname1,colname2,*args,index_map=self.index_map,columns_map=self.columns_map)
        else:
            df = _swapcol(self.df,colname1,colname2,index_map=self.index_map,columns_map=self.columns_map)
        return(Qtable(df=df))
    def reindex_cols(self,*columns,**kwargs):
        df = _reindex_cols(self.df,*columns,index_map=self.index_map,columns_map=self.columns_map,**kwargs)
        return(Qtable(df=df))
    def swaprow(self,rowname1,rowname2,*args):
        if(self.allow_duplicates):
            df = _swaprow(self.df,rowname1,rowname2,*args,index_map=self.index_map,columns_map=self.columns_map)
        else:
            df = _swaprow(self.df,rowname1,rowname2,index_map=self.index_map,columns_map=self.columns_map)
        return(Qtable(df=df))
    def reindex_rows(self,*index,**kwargs):
        df = _reindex_rows(self.df,*index,index_map=self.index_map,columns_map=self.columns_map,**kwargs)
        return(Qtable(df=df))
    def rmcol(self,colname,*whiches):
        df = _rmcol(self.df,colname,*whiches,index_map=self.index_map,columns_map=self.columns_map)
        return(Qtable(df=df))
    def rmcols(self,*colnames,**kwargs):
        df = _rmcols(self.df,*colnames,index_map=self.index_map,columns_map=self.columns_map,**kwargs)
        return(Qtable(df=df))
    def rmrow(self,colname,*whiches):
        df = _rmrow(self.df,colname,*whiches,index_map=self.index_map,columns_map=self.columns_map)
        return(Qtable(df=df))
    def rmrows(self,*colnames,**kwargs):
        df = _rmrows(self.df,*colnames,index_map=self.index_map,columns_map=self.columns_map,**kwargs)
        return(Qtable(df=df))
    def append_col(self,*args,**kwargs):
        df = _append_col(self.df,*args,index_map=self.index_map,columns_map=self.columns_map,allow_duplicates=self.allow_duplicates,**kwargs)
        return(Qtable(df=df))
    def append_cols(self,*args,**kwargs):
        df = _append_cols(self.df,*args,index_map=self.index_map,columns_map=self.columns_map,allow_duplicates=self.allow_duplicates,**kwargs)
        return(Qtable(df=df))
    def append_row(self,*args,**kwargs):
        df = _append_row(self.df,*args,index_map=self.columns_map,columns_map=self.index_map,allow_duplicates=self.allow_duplicates,**kwargs)
        return(Qtable(df=df))
    def append_rows(self,*args,**kwargs):
        df = _append_rows(self.df,*args,index_map=self.columns_map,columns_map=self.index_map,allow_duplicates=self.allow_duplicates,**kwargs)
        return(Qtable(df=df))
    def prepend_col(self,*args,**kwargs):
        df = _prepend_col(self.df,*args,index_map=self.index_map,columns_map=self.columns_map,allow_duplicates=self.allow_duplicates,**kwargs)
        return(Qtable(df=df))
    def prepend_cols(self,*args,**kwargs):
        df = _prepend_cols(self.df,*args,index_map=self.index_map,columns_map=self.columns_map,allow_duplicates=self.allow_duplicates,**kwargs)
        return(Qtable(df=df))
    def prepend_row(self,*args,**kwargs):
        df = _prepend_row(self.df,*args,index_map=self.columns_map,columns_map=self.index_map,allow_duplicates=self.allow_duplicates,**kwargs)
        return(Qtable(df=df))
    def prepend_rows(self,*args,**kwargs):
        df = _prepend_rows(self.df,*args,index_map=self.columns_map,columns_map=self.index_map,allow_duplicates=self.allow_duplicates,**kwargs)
        return(Qtable(df=df))
    def insert_col(self,pos,*args,**kwargs):
        df = _insert_col(self.df,pos,*args,index_map=self.index_map,columns_map=self.columns_map,allow_duplicates=self.allow_duplicates,**kwargs)
        return(Qtable(df=df))
    def insert_cols(self,pos,*args,**kwargs):
        df = _insert_cols(self.df,pos,*args,index_map=self.index_map,columns_map=self.columns_map,allow_duplicates=self.allow_duplicates,**kwargs)
        return(Qtable(df=df))
    def insert_row(self,pos,*args,**kwargs):
        df = _insert_row(self.df,pos,*args,index_map=self.columns_map,columns_map=self.index_map,allow_duplicates=self.allow_duplicates,**kwargs)
        return(Qtable(df=df))
    def insert_rows(self,pos,*args,**kwargs):
        df = _insert_rows(self.df,pos,*args,index_map=self.columns_map,columns_map=self.index_map,allow_duplicates=self.allow_duplicates,**kwargs)
        return(Qtable(df=df))
    def rename_cols(self,*colnames):
        df = _rename_cols(self.df,*colnames)
        return(Qtable(df=df))
    def rename_rows(self,*rownames):
        df = _rename_rows(self.df,*rownames)
        return(Qtable(df=df))
    def repl_col(self,pos,*args,**kwargs):
        df = _repl_col(self.df,pos,*args,index_map=self.index_map,columns_map=self.columns_map,allow_duplicates=self.allow_duplicates,**kwargs)
        return(Qtable(df=df))
    def repl_cols(self,poses,*args,**kwargs):
        df = _repl_cols(self.df,poses,*args,index_map=self.index_map,columns_map=self.columns_map,allow_duplicates=self.allow_duplicates,**kwargs)
        return(Qtable(df=df))
    def repl_row(self,pos,*args,**kwargs):
        df = _repl_row(self.df,pos,*args,index_map=self.columns_map,columns_map=self.index_map,allow_duplicates=self.allow_duplicates,**kwargs)
        return(Qtable(df=df))
    def repl_rows(self,poses,*args,**kwargs):
        df = _repl_rows(self.df,poses,*args,index_map=self.columns_map,columns_map=self.index_map,allow_duplicates=self.allow_duplicates,**kwargs)
        return(Qtable(df=df))
    def transpose(self):
        return(_transpose(self.df))
    def fliplr(self):
        df = _fliplr(self.df,index_map=self.index_map,columns_map=self.columns_map)
        return(Qtable(df=df))
    def flipud(self):
        df = _flipud(self.df,index_map=self.index_map,columns_map=self.columns_map)
        return(Qtable(df=df))
    def to_mat(self):
        m = self.df.values.tolist()
        m = copy.deepcopy(m)
        return(m)


