import pandas as pd
import numpy as np
import elist.elist as elel
import edict.edict as eded
import tlist.tlist as tltl
import copy

__all__ = [
 '_append_col',
 '_append_cols',
 '_append_row',
 '_append_rows',
 '_cn2clocs',
 '_col',
 '_cols',
 '_columns_map',
 '_crop',
 '_get_clocs',
 '_get_rlocs',
 '_getitem',
 '_index_map',
 '_insert_col',
 '_insert_cols',
 '_insert_row',
 '_insert_rows',
 '_ltd_index_first',
 '_ltd_index_last',
 '_name2ilocs',
 '_prepend_col',
 '_prepend_cols',
 '_prepend_row',
 '_prepend_rows',
 '_reindex_cols',
 '_reindex_rows',
 '_rename_cols',
 '_rename_rows',
 '_repl_col',
 '_repl_cols',
 '_repl_row',
 '_repl_rows',
 '_rmcol',
 '_rmcols',
 '_rmrow',
 '_rmrows',
 '_rn2rlocs',
 '_row',
 '_rows',
 '_setitem',
 '_subtb',
 '_swapcol',
 '_swaprow',
 '_transpose',
 '_fliplr',
 '_flipud'
]


#all operations will generate a new Qtable(copy.deepcopy), and will not change the original Qtable 
#columns   col-names-list      no-duplicate-names-permitted
#index     rowname-names-list  no-duplicate-names-permitted

#df                      pd.DataFrame

def _index_map(df):
    d = elel.ivdict(list(df.index))
    return(d)

def _columns_map(df):
    d = elel.ivdict(list(df.columns))
    return(d)

def _name2ilocs(rowname,colname,**kwargs):
    if('index_map' in kwargs):
        index_map = kwargs['index_map']
    else:
        df = kwargs['DF']
        index_map = _index_map(df)
    if('columns_map' in kwargs):
        columns_map = kwargs['columns_map']
    else:
        df = kwargs['DF']
        columns_map = _columns_map(df)
    kl,vl =   eded.d2kvlist(index_map)
    rlocs = elel.indexes_all(vl,rowname)
    kl,vl =   eded.d2kvlist(columns_map)
    clocs = elel.indexes_all(vl,colname)
    return((rlocs,clocs))

# index_map = _index_map(df)
# columns_map = _columns_map(df)
# _getitem(df,rowname,colname,rloc=0,cloc=0)
# rloc relative-row-position
# cloc relative-col-position


def _getitem(df,rowname,colname,*args,**kwargs):
    rlocs,clocs = _name2ilocs(rowname,colname,index_map=kwargs['index_map'],columns_map=kwargs['columns_map'])
    rslt = df.iloc[rlocs,clocs]
    args = list(args)
    if(args.__len__()==0):
        pass
    else:
        rloc = args[0]
        cloc = args[1]
        rslt = rslt.iloc[rloc,cloc]
    return(rslt)

def _setitem(df,rowname,colname,value,*args,**kwargs):
    rlocs,clocs = _name2ilocs(rowname,colname,index_map=kwargs['index_map'],columns_map=kwargs['columns_map'])
    rslt = df.iloc[rlocs,clocs]
    args = list(args)
    if(args.__len__()==0):
        rslt = value
    else:
        rloc = args[0]
        cloc = args[1]
        rslt.iloc[rloc,cloc] = value
    df.iloc[rlocs,clocs] = rslt

#rn ---------------------rowname

def _rn2rlocs(rowname,**kwargs):
    if('index_map' in kwargs):
        index_map = kwargs['index_map']
    else:
        df = kwargs['DF']
        index_map = _index_map(df)
    kl,vl =   eded.d2kvlist(index_map)
    rlocs = elel.indexes_all(vl,rowname)
    rlocs.sort()
    return(rlocs)

def _row(df,rowname,*args,**kwargs):
    rlocs = _rn2rlocs(rowname,**kwargs)
    args = list(args)
    if(args.__len__()==0):
        pass
    else:
        rlocs = elel.select_seqs(rlocs,args)
    return(df.iloc[rlocs])

#cn ---------------------colname

def _cn2clocs(colname,**kwargs):
    if('columns_map' in kwargs):
        columns_map = kwargs['columns_map']
    else:
        df = kwargs['DF']
        columns_map = _columns_map(df)
    kl,vl =   eded.d2kvlist(columns_map)
    clocs = elel.indexes_all(vl,colname)
    clocs.sort()
    return(clocs)

def _col(df,colname,*args,**kwargs):
    clocs = _cn2clocs(colname,**kwargs)
    args = list(args)
    if(args.__len__()==0):
        pass
    else:
        clocs = elel.select_seqs(clocs,args)
    return(df.iloc[:,clocs])

def _get_rlocs(rownames,**kwargs):
    rlocs = []
    for i in range(rownames.__len__()):
        rowname = rownames[i]
        tmp = _rn2rlocs(rowname,**kwargs)
        rlocs = elel.concat(rlocs,tmp)
    rlocs.sort()
    return(rlocs)

def _get_clocs(colnames,**kwargs):
    clocs = []
    for i in range(colnames.__len__()):
        colname = colnames[i]
        tmp = _cn2clocs(colname,**kwargs)
        clocs = elel.concat(clocs,tmp)
    clocs.sort()
    return(clocs)

def _rows(df,*rownames,**kwargs):
    rownames = list(rownames)
    if(isinstance(rownames[0],list)):
        rownames = rownames[0]
    else:
        pass
    rlocs = _get_rlocs(rownames,**kwargs)
    return(df.iloc[rlocs])

def _cols(df,*colnames,**kwargs):
    colnames = list(colnames)
    if(isinstance(colnames[0],list)):
        colnames = colnames[0]
    else:
        pass
    clocs = _get_clocs(colnames,**kwargs)
    return(df.iloc[:,clocs])

def _subtb(df,rownames,colnames,**kwargs):
    rownames = elel.uniqualize(rownames)
    colnames = elel.uniqualize(colnames)
    rlocs = _get_rlocs(rownames,**kwargs)
    clocs = _get_clocs(colnames,**kwargs)
    return(df.iloc[rlocs,clocs])

def _ltd_index_first(ltd,value):
    for i in range(ltd.__len__()):
        if(ltd[i] == value):
            return(i)
        else:
            pass
    raise ValueError("value not exist")

def _ltd_index_last(ltd,value):
    for i in range(ltd.__len__()-1,-1,-1):
        if(ltd[i] == value):
            return(i)
        else:
            pass
    raise ValueError("value not exist")

def _crop(df,top,left,bot,right,**kwargs):
    imd = kwargs['index_map']
    top = _ltd_index_first(imd,top)
    bot = _ltd_index_last(imd,bot)
    cmd = kwargs['columns_map']
    left = _ltd_index_first(cmd,left)
    right = _ltd_index_last(cmd,right)
    rownames = list(df.index[top:bot+1])
    colnames = list(df.columns[left:right+1])
    return(_subtb(df,rownames,colnames,**kwargs))

def _swapcol(df,colname1,colname2,*args,**kwargs):
    df = copy.deepcopy(df)
    clocs1 = _cn2clocs(colname1,**kwargs)
    clocs2 = _cn2clocs(colname2,**kwargs)
    args = list(args)
    if(args.__len__()==0):
        which1 = 0
        which2 = 0
    elif(args.__len__()==1):
        which1 = args[0]
        which2 = 0
    else:
        which1 = args[0]
        which2 = args[1]
    cloc1 = clocs1[which1]
    cloc2 = clocs2[which2]
    clocs = elel.init_range(0,df.columns.__len__(),1)
    clocs = elel.iswap(clocs,cloc1,cloc2)
    return(df.iloc[:,clocs])

def _reindex_cols(df,*columns,**kwargs):
    df = copy.deepcopy(df)
    columns = list(columns)
    if(isinstance(columns[0],list)):
        columns = columns[0]
    else:
        pass
    clocs_array = []
    for i in range(columns.__len__()):
        clocs = _cn2clocs(columns[i],**kwargs)
        clocs_array.append(clocs)
    if("whiches" in kwargs):
        whiches = kwargs['whiches']
    else:
        whiches = elel.init(clocs_array.__len__(),0)
    clocs = elel.batexec(lambda clocs,which:clocs[which],clocs_array,whiches)
    return(df.iloc[:,clocs])

def _swaprow(df,rowname1,rowname2,*args,**kwargs):
    df = copy.deepcopy(df)
    rlocs1 = _rn2rlocs(rowname1,**kwargs)
    rlocs2 = _rn2rlocs(rowname2,**kwargs)
    args = list(args)
    if(args.__len__()==0):
        which1 = 0
        which2 = 0
    elif(args.__len__()==1):
        which1 = args[0]
        which2 = 0
    else:
        which1 = args[0]
        which2 = args[1]
    rloc1 = rlocs1[which1]
    rloc2 = rlocs2[which2]
    rlocs = elel.init_range(0,df.columns.__len__(),1)
    rlocs = elel.iswap(rlocs,rloc1,rloc2)
    return(df.iloc[rlocs])

def _reindex_rows(df,*index,**kwargs):
    df = copy.deepcopy(df)
    index = list(index)
    if(isinstance(index[0],list)):
        index = index[0]
    else:
        pass
    rlocs_array = []
    for i in range(index.__len__()):
        rlocs = _rn2rlocs(index[i],**kwargs)
        rlocs_array.append(rlocs)
    if("whiches" in kwargs):
        whiches = kwargs['whiches']
    else:
        whiches = elel.init(rlocs_array.__len__(),0)
    rlocs = elel.batexec(lambda rlocs,which:rlocs[which],rlocs_array,whiches)
    return(df.iloc[rlocs])

def _rmcol(df,colname,*args,**kwargs):
    df = copy.deepcopy(df)
    clocs = _cn2clocs(colname,**kwargs)
    if(args.__len__()==0):
        whiches = elel.init_range(0,clocs.__len__(),1)
    else:
        whiches = list(args)
    clocs = elel.select_seqs(clocs,whiches)
    all_clocs = elel.init_range(0,df.columns.__len__(),1)
    lefted_clocs = elel.select_seqs_not(all_clocs,clocs)
    return(df.iloc[:,lefted_clocs])

def _rmcols(df,*colnames,**kwargs):
    df = copy.deepcopy(df)
    colnames = list(colnames)
    if(isinstance(colnames[0],list)):
        colnames = colnames[0]
    else:
        pass
    clocs_array = []
    for i in range(colnames.__len__()):
        clocs = _cn2clocs(colnames[i],**kwargs)
        clocs_array.append(clocs)
    if("whiches" in kwargs):
        whiches = kwargs['whiches']
        clocs = elel.batexec(lambda clocs,which:clocs[which],clocs_array,whiches)
    else:
        #by default remove all
        clocs = elel.concat(*clocs_array)
    all_clocs = elel.init_range(0,df.columns.__len__(),1)
    lefted_clocs = elel.select_seqs_not(all_clocs,clocs)
    return(df.iloc[:,lefted_clocs])

def _rmrow(df,rowname,*args,**kwargs):
    df = copy.deepcopy(df)
    rlocs = _rn2rlocs(rowname,**kwargs)
    if(args.__len__()==0):
        whiches = elel.init_range(0,rlocs.__len__(),1)
    else:
        whiches = list(args)
    rlocs = elel.select_seqs(rlocs,whiches)
    all_rlocs = elel.init_range(0,df.index.__len__(),1)
    lefted_rlocs = elel.select_seqs_not(all_rlocs,rlocs)
    return(df.iloc[lefted_rlocs])

def _rmrows(df,*rownames,**kwargs):
    df = copy.deepcopy(df)
    rownames = list(rownames)
    if(isinstance(rownames[0],list)):
        rownames = rownames[0]
    else:
        pass
    rlocs_array = []
    for i in range(rownames.__len__()):
        rlocs = _rn2rlocs(rownames[i],**kwargs)
        rlocs_array.append(rlocs)
    if("whiches" in kwargs):
        whiches = kwargs['whiches']
        rlocs = elel.batexec(lambda rlocs,which:rlocs[which],rlocs_array,whiches)
    else:
        #by default remove all
        rlocs = elel.concat(*rlocs_array)
    all_rlocs = elel.init_range(0,df.index.__len__(),1)
    lefted_rlocs = elel.select_seqs_not(all_rlocs,rlocs)
    return(df.iloc[lefted_rlocs])

def _insert_col(df,pos,*args,**kwargs):
    df = copy.deepcopy(df)
    if(isinstance(pos,int)):
        pass
    else:
        clocs = _cn2clocs(pos,**kwargs)
        if('which' in kwargs):
            which = kwargs['which']
        else:
            which = 0
        pos = clocs[which] + 1
    args = list(args)
    if(args.__len__() == 1):
        colname = list(args[0].keys())[0]
        values = list(args[0].values())[0]
    else:
        colname = args[0]
        if(isinstance(args[1],list)):
            values = args[1]
        else:
            values = args[1:]
    ####
    ####
    df.insert(pos,colname,values,kwargs['allow_duplicates'])
    return(df)

def _insert_cols(df,pos,*args,**kwargs):
    df = copy.deepcopy(df)
    if(isinstance(pos,int)):
        pass
    else:
        clocs = _cn2clocs(pos,**kwargs)
        if('which' in kwargs):
            which = kwargs['which']
        else:
            which = 0
        pos = clocs[which] + 1
    args = list(args)
    if(isinstance(args[0],dict)):
        kl,vl = eded.d2kvlist(args[0])
    else:
        if(isinstance(args[1],list)):
            kl =  elel.select_evens(args)
            vl =  elel.select_odds(args)
        else:
            kl,vl = elel.brkl2kvlist(args,df.index.__len__()+1)
    for i in range(kl.__len__()):
        colname = kl[i]
        values = vl[i]
        df.insert(pos+i,colname,values,kwargs['allow_duplicates'])
    return(df)

def _insert_row(df,pos,*args,**kwargs):
    df = df.T
    df = _insert_col(df,pos,*args,**kwargs)
    df = df.T
    return(df)

def _insert_rows(df,pos,*args,**kwargs):
    df = df.T
    df = _insert_cols(df,pos,*args,**kwargs)
    df = df.T
    return(df)

def _append_col(df,*args,**kwargs):
    pos = df.columns.__len__()
    return(_insert_col(df,pos,*args,**kwargs))

def _append_cols(df,*args,**kwargs):
    pos = df.columns.__len__()
    return(_insert_cols(df,pos,*args,**kwargs))

def _append_row(df,*args,**kwargs):
    pos = df.index.__len__()
    return(_insert_row(df,pos,*args,**kwargs))

def _append_rows(df,*args,**kwargs):
    pos = df.index.__len__()
    return(_insert_rows(df,pos,*args,**kwargs))

def _prepend_col(df,*args,**kwargs):
    return(_insert_col(df,0,*args,**kwargs))

def _prepend_cols(df,*args,**kwargs):
    return(_insert_cols(df,0,*args,**kwargs))

def _prepend_row(df,*args,**kwargs):
    return(_insert_row(df,0,*args,**kwargs))

def _prepend_rows(df,*args,**kwargs):
    return(_insert_rows(df,0,*args,**kwargs))

def _rename_cols(df,*colnames):
    df = copy.deepcopy(df)
    colnames = list(colnames)
    if(isinstance(colnames[0],list)):
        colnames = colnames[0]
    else:
        pass
    df.columns = colnames
    return(df)

def _rename_rows(df,*rownames):
    df = copy.deepcopy(df)
    rownames = list(rownames)
    if(isinstance(rownames[0],list)):
        rownames = rownames[0]
    else:
        pass
    df.index = rownames
    return(df)

def _repl_col(df,pos,*args,**kwargs):
    df = copy.deepcopy(df)
    if(isinstance(pos,int)):
        pos = pos + 1
    else:
        clocs = _cn2clocs(pos,**kwargs)
        if('which' in kwargs):
            which = kwargs['which']
        else:
            which = 0
        pos = clocs[which] + 1
    args = list(args)
    if(args.__len__() == 1):
        colname = list(args[0].keys())[0]
        values = list(args[0].values())[0]
    else:
        colname = args[0]
        if(isinstance(args[1],list)):
            values = args[1]
        else:
            values = args[1:]
    df.insert(pos,colname,values,kwargs['allow_duplicates'])
    pos = pos -1
    all_clocs = elel.init_range(0,df.columns.__len__(),1)
    all_clocs.remove(pos)
    return(df.iloc[:,all_clocs])

def _repl_cols(df,poses,*args,**kwargs):
    df = copy.deepcopy(df)
    args = list(args)
    if(isinstance(args[0],dict)):
        kl,vl = eded.d2kvlist(args[0])
    else:
        if(isinstance(args[1],list)):
            kl =  elel.select_evens(args)
            vl =  elel.select_odds(args)
        else:
            kl,vl = elel.brkl2kvlist(args,df.index.__len__()+1)
    if(isinstance(poses[0],int)):
        pass
    else:
        colnames = poses 
        clocs_array = []
        for i in range(colnames.__len__()):
            clocs = _cn2clocs(colnames[i],**kwargs)
            clocs_array.append((clocs,i))
        if("whiches" in kwargs):
            whiches = kwargs['whiches']
            clocs_array = elel.mapv(clocs_array,lambda ele:ele[0])
            clocs = elel.batexec(lambda clocs,which:clocs[which],clocs_array,whiches)
            poses = clocs
        else:
            #by default replace all
            nkl = []
            nvl = []
            nclocs = []
            for i in range(clocs_array.__len__()):
                clocs = clocs_array[i][0]
                index = clocs_array[i][1]
                tmpkl = elel.init(clocs.__len__(),kl[i])
                tmpvl = elel.init(clocs.__len__(),vl[i])
                nkl = elel.concat(nkl,tmpkl)
                nvl = elel.concat(nvl,tmpvl)
                nclocs = elel.concat(nclocs,clocs)
            #batsort
            poses = nclocs
            kl,vl = elel.batsorted(nclocs,nkl,nvl)
    poses = elel.mapv(poses,lambda pos:pos+1)
    poses.sort()
    for i in range(0,poses.__len__()):
        pos = poses[i]
        df.insert(pos,kl[i],vl[i],kwargs['allow_duplicates'])
        pos = pos -1
        all_clocs = elel.init_range(0,df.columns.__len__(),1)
        all_clocs.remove(pos)
        df = df.iloc[:,all_clocs]
    return(df)

def _repl_row(df,pos,*args,**kwargs):
    df = df.T
    df = _repl_col(df,pos,*args,**kwargs)
    df = df.T
    return(df)

def _repl_rows(df,poses,*args,**kwargs):
    df = df.T
    df = _repl_cols(df,poses,*args,**kwargs)
    df = df.T
    return(df)

def _transpose(df):
    df = copy.deepcopy(df)
    df = df.T
    return(df)

def _fliplr(df,**kwargs):
    columns = list(df.columns)
    columns.reverse()
    df = _reindex_cols(df,columns,**kwargs)
    return(df)

def _flipud(df,**kwargs):
    index = list(df.index)
    index.reverse()
    df = _reindex_rows(df,index,**kwargs)
    return(df)



