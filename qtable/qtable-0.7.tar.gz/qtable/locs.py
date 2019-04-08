def get_tr(tl,br):
    tr = (tl[0],br[1])
    return(tr)

def get_bl(tl,br):
    bl = (br[0],tl[1])
    return(bl)

def init_block():
    blk = {
        "tl":None,
        "br":None,
        "pblk":None,
        "spt":None
    }
    return(blk)

def new_block(tl,br,pblk,spt):
    blk = init_block()
    blk["tl"] = tl
    blk["br"] = br
    blk["pblk"] = pblk
    blk["spt"] = spt
    return(blk)

def is_root(blk):
    return(blk["pblk"] == {})

def is_leaf(blk):
    return(blk["spt"] == tuple(()))

def creat_root_block(tl,br,spt):
    blk = new_block(tl,br,{},spt)
    return(blk)

def creat_leaf_block(tl,br,pblk):
    blk = new_block(tl,br,pblk,tuple(()))
    return(blk)

def extract_blk(blk):
    tl = blk["tl"]
    br = blk["br"]
    tr = get_tr(tl,br)
    bl = get_bl(tl,br)
    spt = blk["spt"]
    return((tl,tr,bl,br,spt))

def inzotl(pt,tl):
    r,c = pt
    return((r<tl[0])&(c<tl[1]))

def inzol(pt,tl,bl):
    r,c = pt
    return((r>=tl[0])&(r<=bl[0])&(c<tl[1]))

def inzobl(pt,bl):
    r,c = pt
    return((r>bl[0])&(c<bl[1]))

def inzobot(pt,bl,br):
    r,c = pt
    return((r>bl[0])&(c>=bl[1])&(c<=br[1]))

def inzobr(pt,br):
    r,c = pt
    return((r>br[0])&(c>br[1]))

def inzor(pt,tr,br):
    r,c = pt
    return((r>=tr[0])&(r<=br[0])&(c>tr[1]))

def inzotr(pt,tr):
    r,c = pt
    return((r<tr[0])&(c>tr[1]))

def inzotop(pt,tl,tr):
    r,c = pt
    return((r<tl[0])&(c>=tl[1])&(c<=tr[1]))

def inzetl(pt,tl):
    return(pt==tl)

def inzel(pt,tl,bl):
    r,c = pt
    return((r>=(tl[0]+1))&(r<=(bl[0]-1))&(c==tl[1]))

def inzebl(pt,bl):
    return(pt==bl)

def inzebot(pt,bl,br):
    r,c = pt
    return((r==bl[0])&(c>=(bl[1]+1))&(c<=(br[0]-1)))

def inzebr(pt,br):
    return((pt==br))

def inzer(pt,tr,br):
    r,c = pt
    return((r>=(tr[0]+1))&(r<=(br[0]-1))&(c==tr[1]))

def inzetr(pt,tr):
    return((pt==tr))

def inzetop(pt,tl,tr):
    r,c = pt
    return((r==tl[0])&(c>=(tl[1]+1))&(c<=(tr[1]-1)))

def inzinner(pt,tl,br):
    r,c = pt
    return((r>tl[0])&(r<br[0])&(c>tl[1])&(c<br[1]))


def get_pt_zone(blk,pt):
    tl,tr,bl,br,spt= extract_blk(blk)
    if(inzinner(pt,tl,br)):
        return("zinner")
    elif(inzetop(pt,tl,tr)):
        return("zetop")
    elif(inzetr(pt,tr)):
        return("zetr")
    elif(inzer(pt,tr,br)):
        return("zer")
    elif(inzebr(pt,br)):
        return("zebr")
    elif(inzebot(pt,bl,br)):
        return("zebot")
    elif(inzebl(pt,bl)):
        return("zebl")
    elif(inzel(pt,tl,bl)):
        return("zel")
    elif(inzetl(pt,tl)):
        return("zetl")
    elif(inzotop(pt,tl,tr)):
        return("ztop")
    elif(inzotr(pt,tr)):
        return("zotr")
    elif(inzor(pt,tr,br)):
        return("zor")
    elif(inzobr(pt,br)):
        return("zobr")
    elif(inzobot(pt,bl,br)):
        return("zobot")
    elif(inzobl(pt,bl)):
        return("zobl")
    elif(inzol(pt,tl,bl)):
        return("zol")
    elif(inzotl(pt,tl)):
        return("zotl")
    else:
        print("impossible!")


def get_spt_zone(blk):
    tl,tr,bl,br,spt= extract_blk(blk)
    return(get_pt_zone(blk,spt))


def is_pt_inside(blk,pt):
    return(get_pt_zone(blk,pt)=="zinner")

def is_pt_outside(blk,pt):
    return(("inzo" in get_pt_zone(blk,pt)))


##

def get_sblktl(blk):
    tl,tr,bl,br,spt= extract_blk(blk)
    z = get_pt_zone(blk,spt)
    if((z == "zotl")|(z == "zol")|(z == "zobl")|(z == "zotop")|(z == "zotr")):
        stl = tuple(())
        sbr = tuple(())
    elif(z == "zobot"):
        r = bl[0]
        c = spt[1]
        stl = tl
        sbr = (r,c)
    elif(z == "zobr"):
        stl = tl
        sbr = br
    elif(z == "zor"):
        r = spt[0]
        c = tr[1]
        stl = tl
        sbr = (r,c)
    else:
        stl = tl
        sbr = spt
    sblktl = new_block(stl,sbr,blk,None)
    return(sblktl)

def get_sblktr(blk):
    tl,tr,bl,br,spt= extract_blk(blk)
    z = get_pt_zone(blk,spt)
    if((z == "zotl")|(z == "zotop")|(z == "zotr")|(z == "zor")|(z == "zobr")):
        stl = tuple(())
        sbr = tuple(())
    elif(z == "zobot"):
        r = tl[0]
        c = spt[1]
        stl = (r,c)
        sbr = br
    elif(z == "zobl"):
        stl = tl
        sbr = br
    elif(z == "zol"):
        r = spt[0]
        c = tr[1]
        stl = tl
        sbr = (r,c)
    else:
        r,c = spt
        stl = (tl[0],c+1)
        sbr = (r,tr[1])
    sblktr = new_block(stl,sbr,blk,None)
    return(sblktr)

def get_sblkbl(blk):
    tl,tr,bl,br,spt= extract_blk(blk)
    z = get_pt_zone(blk,spt)
    if((z == "zotl")|(z == "zol")|(z == "zobl")|(z == "zobot")|(z == "zobr")):
        stl = tuple(())
        sbr = tuple(())
    elif(z == "zotop"):
        r = tl[0]
        c = spt[1]
        stl = tl
        sbr = (bl[0],c)
    elif(z == "zotr"):
        stl = tl
        sbr = br
    elif(z == "zor"):
        r = spt[0]
        c = tr[1]
        stl = tl
        sbr = (r,c)
    else:
        r,c = spt
        stl = (r+1,tl[1])
        sbr = (bl[0],c)
    sblkbl = new_block(stl,sbr,blk,None)
    return(sblkbl)

def get_sblkbr(blk):
    tl,tr,bl,br,spt= extract_blk(blk)
    z = get_pt_zone(blk,spt)
    if((z == "zotr")|(z == "zor")|(z == "zobr")|(z == "zobot")|(z == "zobl")):
        stl = tuple(())
        sbr = tuple(())
    elif(z == "zotop"):
        r = tl[0]
        c = spt[1]
        stl = (r,c)
        sbr = br
    elif(z == "zotl"):
        stl = tl
        sbr = br
    elif(z == "zol"):
        r = spt[0]
        c = tl[1]
        stl = (r,c)
        sbr = br
    else:
        r,c = spt
        stl = (r+1,c+1)
        sbr = br
    sblkbr = new_block(stl,sbr,blk,None)
    return(sblkbr)

def quad_split(blk):
    sblktl = get_sblktl(blk)
    sblktr = get_sblktr(blk)
    sblkbl = get_sblkbl(blk)
    sblkbr = get_sblkbr(blk)
    sblks = (sblktl,sblktr,sblkbl,sblkbr)
    return((sblks))
##





##

def index2loc(index,colnums):
    colseq = index % colnums
    rowseq = index // colnums
    return((rowseq,colseq))

def loc2index(loc,colnums):
    rowseq = loc[0]
    colseq = loc[1]
    if(rowseq - 1 <0):
        r = 0
    else:
        r = rowseq - 1
    return(colnums*(r+1) + colseq)

##blkinblk
