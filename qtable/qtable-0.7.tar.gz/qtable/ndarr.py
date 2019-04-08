import numpy as np
import copy
import elist.elist as elel
from qtable import utils
from qtable import locs


def swap_dimension(ndarr):
    return(np.reshape(ndarr,ndarr.size,order='F').reshape(utils.swap_tuple_ele(ndarr.shape)))

def swap_row(ndarr,rowseq1,rowseq2):
    ndarr[[rowseq1,rowseq2],:] = ndarr[[rowseq2,rowseq1],:]
    return(ndarr)

def swap_rows(ndarr,rowseqs1,rowseqs2):
    tmp = ndarr[rowseqs1,:]
    ndarr[rowseqs1,:] = ndarr[rowseqs2,:]
    ndarr[rowseqs2,:] = tmp
    return(ndarr)

def swap_col(ndarr,colseq1,colseq2):
    ndarr[:,[colseq1,colseq2]] = ndarr[:,[colseq2,colseq1]]
    return(ndarr)

def swap_cols(ndarr,colseqs1,colseqs2):
    tmp = copy.deepcopy(ndarr[:,colseqs1])
    ndarr[:,colseqs1] = ndarr[:,colseqs2]
    ndarr[:,colseqs2] = tmp 
    return(ndarr)

def insert_row(ndarr,rowseq,row):
    ndarr = np.insert(ndarr,rowseq,row,0)
    return(ndarr)

def insert_rows(ndarr,rowseq,rows,**kwargs):
    ndarr = np.insert(ndarr,rowseq,rows,0)
    return(ndarr)

def insert_col(ndarr,colseq,col,**kwargs):
    ndarr = np.insert(ndarr,colseq,col,1)
    return(ndarr)

def insert_cols(ndarr,colseq,cols,**kwargs):
    ndarr = np.insert(ndarr,colseq,cols,1)
    return(ndarr)

def append_col(ndarr,col):
    return(np.c_[ndarr,col])

def append_cols(ndarr,cols):
    return(np.c_[ndarr,np.array(cols).transpose()])

def append_row(ndarr,row):
    return(np.r_[ndarr,[row]])

def append_rows(ndarr,rows):
    return(np.r_[ndarr,rows])

def prepend_col(ndarr,col):
    return(np.c_[col,ndarr])

def prepend_cols(ndarr,cols):
    return(np.c_[np.array(cols).transpose(),ndarr])

def prepend_row(ndarr,row):
    return(np.r_[[row],ndarr])

def prepend_rows(ndarr,rows):
    return(np.r_[rows,ndarr])

def crop(ndarr,top,left,bot,right):
    ndarr = ndarr[top:bot+1,:][:,left:right+1]
    return(ndarr)

def copr_tlbr(ndarr,tl,br):
    ndarr = crop(ndarr,tl[0],tl[1],br[0],br[1])
    return(ndarr)


def slct(ndarr,rowseqs,colseqs):
    ndarr = ndarr[rowseqs,:][:,colseqs]
    return(ndarr)

def slct_col(ndarr,colseq):
    ndarr = ndarr[:,colseq]
    return(ndarr)

def slct_cols(ndarr,colseqs):
    ndarr = ndarr[:,colseqs]
    return(ndarr)

def slct_row(ndarr,rowseq):
    ndarr = ndarr[rowseq,:]
    return(ndarr)

def slct_rows(ndarr,rowseqs):
    ndarr = ndarr[rowseqs,:]
    return(ndarr)

def rows(ndarr):
    return(ndarr)

def cols(ndarr):
    return(ndarr.transpose())


def rplc_col(ndarr,colseq,col):
    ndarr[:,colseq] = col
    return(ndarr)

def rplc_cols(ndarr,colseqs,cols):
    cols = np.array(cols)
    ndarr[:,colseqs] = cols.transpose()
    return(ndarr)

def rplc_row(ndarr,rowseq,row):
    ndarr[rowseq,:] = row
    return(ndarr)

def rplc_rows(ndarr,rowseqs,rows):
    rows = np.array(rows)
    ndarr[rowseqs,:] = rows
    return(ndarr)

def rplc_blk(ndarr,top,left,bot,right,blk):
    rowseqs = elel.init_range(top,bot+1,1)
    rows_ndarr = copy.deepcopy(ndarr[rowseqs,:])
    colseqs = elel.init_range(left,right+1,1)
    #cols = blk.transpose()
    cols = blk
    rows_ndarr[:,colseqs] = cols
    ndarr[rowseqs,:] = rows_ndarr
    return(ndarr)

def rm_col(ndarr,colseq):
    ndarr = np.delete(ndarr,[colseq],axis=1)
    return(ndarr)

def rm_cols(ndarr,colseqs):
    ndarr = np.delete(ndarr,colseqs,axis=1)
    return(ndarr)

def rm_row(ndarr,rowseq):
    ndarr = np.delete(ndarr,[rowseq],axis=0)
    return(ndarr)

def rm_rows(ndarr,rowseqs):
    ndarr = np.delete(ndarr,rowseqs,axis=0)
    return(ndarr)

def fliplr(ndarr):
    return(np.fliplr(ndarr))

def flipud(ndarr):
    return(np.flipud(ndarr))

def ccwrot90(ndarr):
    ndarr = np.rot90(ndarr)
    return(ndarr)

def ccwrot180(ndarr):
    ndarr = np.rot90(ndarr,2)
    return(ndarr)

def ccwrot270(ndarr):
    ndarr = np.rot90(ndarr,3)
    return(ndarr)

def cwrot90(ndarr):
    ndarr = np.rot90(ndarr,-1)
    return(ndarr)

def cwrot180(ndarr):
    ndarr = np.rot90(ndarr,-2)
    return(ndarr)

def cwrot270(ndarr):
    ndarr = np.rot90(ndarr,-3)
    return(ndarr)

def rowtop_colleft(ndarr):
    return(ndarr)

def rowtop_colright(ndarr):
    return(fliplr(ndarr))

def rowbot_colright(ndarr):
    ndarr = flipud(ndarr)
    return(fliplr(ndarr))

def rowbot_colleft(ndarr):
    return(flipud(ndarr))

def rowleft_coltop(ndarr):
    ndarr = cwrot90(ndarr)
    return(fliplr(ndarr))

def rowright_coltop(ndarr):
    return(cwrot90(ndarr))

def rowright_colbot(ndarr):
    ndarr = ccwrot90(ndarr)
    return(fliplr(ndarr))

def rowleft_colbot(ndarr):
    return(ccwrot90(ndarr))


def creat_action(fn,*other_args):
    action = {
        "func":fn,
        "other_args":list(other_args)
    }
    return(action)

def creat_action_list(func_list,**kwargs):
    if("other_args_list" in kwargs):
        other_args_list = kwargs['other_args_list']
    else:
        other_args_list = elel.init(func_list.__len__(),[])
    actions = elel.mapvo(func_list,creat_action,map_func_args_array=other_args_list)
    return(actions)

def filter(ndarr,actions):
    for i in range(actions.__len__()):
        ndarr = actions[i]["func"](ndarr,*actions[i]["other_args"])
    return(ndarr)


#move

def get_locmat(ndarr,**kwargs):
    if('left' in kwargs):
        left = kwargs["left"]
    else:
        left = 0
    if('top' in kwargs):
        top = kwargs["top"]
    else:
        top = 0
    height = ndarr.shape[0]
    width = ndarr.shape[1]
    vfunc = np.vectorize(locs.index2loc)
    rowseqs,colseqs = vfunc(np.arange(ndarr.size),width)
    rowseqs = rowseqs + top
    colseqs = colseqs + left
    locmat = np.c_[rowseqs,colseqs].reshape((height,width,2))
    return(locmat)


def get_corner_coord(ndarr,**kwargs):
    if('left' in kwargs):
        left = kwargs["left"]
    else:
        left = 0
    if('top' in kwargs):
        top = kwargs["top"]
    else:
        top = 0
    height = ndarr.shape[0]
    width = ndarr.shape[1]
    top_left = (top,left)
    top_right = (top,left+width-1)
    bot_left = (top+height-1,left)
    bot_right = (top+height-1,left+width-1)
    return([top_left,top_right,bot_left,bot_right])

def get_tlbr(ndarr,**kwargs):
    top_left,top_right,bot_left,bot_right = get_corner_coord(ndarr,**kwargs)
    return([top_left,bot_right])


def quad_split(ndarr,spt):
    tl,br = get_tlbr(ndarr)
    blk = locs.creat_root_block(tl,br,spt)
    sblktl,sblktr,sblkbl,sblkbr = locs.quad_split(blk)
    tlndarr = copr_tlbr(ndarr,sblktl['tl'],sblktl['br'])
    trndarr = copr_tlbr(ndarr,sblktr['tl'],sblktr['br'])
    blndarr = copr_tlbr(ndarr,sblkbl['tl'],sblkbl['br'])
    brndarr = copr_tlbr(ndarr,sblkbr['tl'],sblkbr['br'])
    return([tlndarr,trndarr,blndarr,brndarr])

#####
