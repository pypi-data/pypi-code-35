# Copyright © 2018 Battelle Memorial Institute
# All rights reserved.

import warnings
import hypernetx as hnx
import networkx as nx
import numpy as np
from hypernetx.exception import HyperNetXError
import numpy as np
import itertools as it

## Create logger to test performance
import logging, time, os
import os, sys

BASEDIR='/Users/prag717/documents/tdm/hnxgithub'

logdir = f'{BASEDIR}/logfiles'

if not os.path.isdir(logdir):
	os.makedirs(logdir)

logger = logging.getLogger('homology_log')
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler(f'{logdir}/homology_log.log')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)

logger.addHandler(fh)

logger.info('message goes here')

## Include numbas to optimize perfomance
import numba
from numba import jit

import json, csv, ast, sys
import pandas as pd
import numpy as np
from numpy import linalg as npla
import networkx as nx
from networkx.algorithms import bipartite
import scipy.sparse as sparse
from scipy.sparse import csr_matrix as csr
import itertools as it
import scipy.stats as stat
from collections import Counter
import datetime
import matplotlib.pyplot as plt
import random
from math import log

def timeit(method):
    def timed(*args, **kw):
        logger.info(f'{time.time()}')
        result = method(*args, **kw)
        logger.info(f'{time.time()}')
        return result
    return timed

@jit(noPython=True)
@timeit
def powerset(seq):
    """
    Returns all the subsets of this set. This is a generator.
    Impractical for large sets.
    """
    if len(seq) <= 1:
        yield seq
        yield []
    else:
        for item in powerset(seq[1:]):
            yield [seq[0]]+item
            yield item 

@jit(noPython=True)
@timeit
def asc_maker(tops):
    '''use with powerset for small hypergraphs to compute the asc
    Really SLOW!!! for big hypergraphs'''
    pset = list()
    for top in list(tops):
        x = [tuple(sorted(y)) for y in powerset(list(top))]
        pset.extend(x)
    pset = set(pset)
    pset.discard(())
    return pset

@jit(noPython=True)
@timeit
def display_s_comps(h,s=1):
    scomps = dict()
    for idx in range(20):
        scomps[idx+1] = list(h.s_component_subgraphs(s=idx+1,edges=True))
        scomps[idx+1].sort(key=lambda x: x.shape[1], reverse=True)
        
    n = len(scomps[s])
    ncols=3
    
    nrowstemp = n//ncols 
    nrows = nrowstemp + 1*(n > nrowstemp*ncols)
    fig,ax = plt.subplots(nrows,ncols,figsize=(15,4*nrows+5))
    if nrows != 1 and ncols != 1:
        for idx in range(nrows):
            for jdx in range(ncols):
                ax[idx][jdx].axis('off')
        for i in range(n):
            r = i//ncols
            c = i%ncols
            ax[r][c].axis('off')
            infodict = hnx.info_dict(scomps[s][i])
            d = infodict['density']
            ax[r][c].set_title(f'component={i + 1}\n density:{d:.2f}')
            hnx.draw(scomps[s][i],ax=ax[r][c],with_node_labels=False,with_edge_labels=True)

    else:
        for i in range(3):
            ax[i].axis('off')            
            if i < n:
                infodict = hnx.info_dict(scomps[s][i])
                d = infodict['density']
                ax[i].set_title(f'component={i + 1}\n density:{d:.2f}')
                hnx.draw(scomps[s][i],ax=ax[i],with_node_labels=False,with_edge_labels=True)
    fig.suptitle(f's-connected components for s={s}', fontsize=16)
    plt.show()


@jit(noPython=True)
@timeit
def kernel(A, tol=1e-10):
    """ returns a matrix whose column vectors form a basis for the null space of A """
    """ (in our context Z_k) """
    _, s, vh = np.linalg.svd(A)
    sing=np.zeros(vh.shape[0],dtype=np.complex)
    sing[:s.size]=s
    null_mask = (sing <= tol)   #we only want the rows in vh corresponding to sing <= tol == true
    null_space = np.compress(null_mask, vh, axis=0)
    return null_space.conj().T

@jit(noPython=True)
@timeit
def cokernel(A, tol=1e-10):
    """ returns a matrix whose column vectors form a basis for the space """
    """ orthogonal to the image of A (in our context B_k)"""
    """ This is where the generators for H_k will live."""
    """ By projecting kernel(b_(k)) onto the cokernel(b_(k+1)) we """
    """ obtain a basis for H_k. """
    u, s, _ = np.linalg.svd(A)
    sing=np.zeros(u.shape[1],dtype=np.complex)
    sing[:s.size]=s
    null_mask = (sing <= tol)
    return np.compress(null_mask, u, axis=1)


@jit(noPython=True)
@timeit
def ksublists(lst,n,sublist=[]):
    """Iterate over all ordered n-sublists of a list lst"""
    if n==0:
        yield sublist
    else:
        for idx in range(len(lst)):
            item=lst[idx]
            for tmp in ksublists(lst[idx+1:],n-1,sublist+[item]):
                yield tmp
@jit(noPython=True)
@timeit
def vertexList(subcomplx):
    """ returns a list of vertices found in the subcomplex, not a list of lists """
    m =  {}
    for e in subcomplx:
        for v in list(e):
            m[v] = 1
    verts = list(m.keys())
    verts.sort()
    return verts

@jit(noPython=True)
@timeit
def flag(edgeList,maxdim=None):
    """Construct the flag complex based on a given ordered edge list"""
    """Returns a list of tuples"""
    subcomplx = []
    for e in edgeList:
        e.sort()
        subcomplx += [tuple(e)]
    vertices = vertexList(subcomplx)
    flag = [tuple([v]) for v in vertices] + subcomplx

    k = 2
    while (len(vertices) > 0) and ((maxdim == None) or (k <= maxdim)):

        pChains = it.combinations(vertices,k+1)
        possibleChains = list(map(list,pChains))
        newChains = []
        for chain in possibleChains:
            if all([edge in edgeList for edge in ksublists(chain,2)]):
                newChains += [tuple(chain)]
        vertices = vertexList(newChains)
        flag += newChains
        k +=1
    return flag

@jit(noPython=True)
@timeit
def orientCells(complx, ordering = []):
    """ returns the elements in complx according to a canonical ordering """
    """ complx is a list of tuples with entries in 0 to n for some n """
    """ ordering is an ordered list of the entries which could be found in complx """
    """ it is assumed the vertices in complx are referenced by non-negative integers"""
    newcomplx = []
    if len(ordering) == 0:
        n = max(max(list(cpx)) for cpx in complx)
        ordering = list(range(n+1))  ####### this induces a default ordering from the whole numbers
    for compx in complx:
        compxfilter = -1 * np.ones((len(ordering),), dtype=np.int)
        for entry in compx:
            compxfilter[ordering.index(entry)] = entry
        #         newcomplx.append([entry for entry in compxfilter if entry != -1])
        newcomplx.append(tuple(it.ifilter(lambda x: x != -1, compxfilter)))
        return newcomplx

@jit(noPython=True)
@timeit
def closure(complexes):
    """ returns sub-complexes as tuples with order inherited from complx - an iterable """
    """ used for generating an asc from toplexes  """
    n = max([len(lst) for lst in complexes])
    temp = {}
    for k in range(1,n+1):
        for lst in complexes:
            for comb in it.combinations(lst,k):
                temp[comb] = 1
    return list(temp.keys())

@jit(noPython=True)
@timeit
def ascClosure(allcomplx, complx):
    """ returns tuples of allcomplx which are subsets of elements in complx """
    """ methods with allcomplx parameter assume allcomplx is closed under taking subcomplexes"""
    temp = {}
    for face in complx:
        for lst in allcomplx:
            if set(lst).issubset(face):
                temp[tuple(lst)] = 1
    return list(temp.keys())

@jit(noPython=True)
@timeit
def nzero(allcomplx, complx, closed = False):
    """ returns the star of complx """
    star = {}
    if closed:
        complx = ascClosure(allcomplx, complx)
    for lst in complx:
        for cell in allcomplx:
            if set(lst).issubset(cell):
                star[tuple(cell)] = 1
    return list(star.keys())

@jit(noPython=True)
@timeit
def nkneigh(allcomplx, complx, k=0, closed = False):
    """ returns the kth neighborhood of a complex within allcomplx """
    """ where by definition n_k(complx) = n0(n_(k-1)(complx)) """
    if k == 0:
        return nzero(allcomplx, complx, closed)
    else:
        #         return nzero(allcomplx, nkneigh(allcomplx,complx,k-1))
        return nzero(allcomplx, ascClosure(allcomplx, nkneigh(allcomplx,complx,k-1)))

@jit(noPython=True)
@timeit
def complement(allcomplx, complx, k=0, closed = False):
    """ returns the complement of the n_k neighborhood of complex in the allcomplx """
    roi = nkneigh(allcomplx, complx, k, closed)
    acp = list(allcomplx)
    for cell in roi:
        acp[acp.index(cell)]=0
    return list(it.ifilter(lambda x: x != 0, acp))

@jit(noPython=True)
@timeit
def kchainBasis(allcomplx,k,rel=[]):
    """ returns a basis for C_k in allcomplx excluding the rel set """
    """ assumes rel is a subset of allcomplx"""
    temp = list(allcomplx)
    for item in rel:
        temp[allcomplx.index(item)] = ()
    comp = [(len(entry) == k+1)*1 for entry in temp]
    return list(it.compress(allcomplx,comp))

@jit(noPython=True)
@timeit
def bkMatrix(km1basis,kbasis,k=1):
    """ Compute the boundary matrix from C_k chains to C_(k-1) chains within allcomplx"""
    """ assumes rel is a subset of allcomplx"""
    bk = np.zeros((len(km1basis),len(kbasis)))
    for cell in kbasis:
        for idx in range(len(cell)):
            face = cell[:idx]+cell[idx+1:]
            row = km1basis.index(face)
            col = kbasis.index(cell)
            bk[row][col]= (-1)**idx
    return bk

@jit(noPython=True)
@timeit
def relbkMatrix(km1basis,kbasis,bk,k,rel=[]):
    """ removes rows and columns from the boundary matrix corresponding """
    """ to the rel set """
    """ not as efficient as bksubMatrix which computes the matrix directly """
    newbk = bk
    if len(rel)>0:
        krel = list[it.ifilter(lambda x: len(x) == k+1, rel)]
        km1rel = list[it.ifilter(lambda x: len(x == k), rel)]
        kfilter = np.ones(len(kbasis))
        km1filter = np.ones(len(km1basis))
        for item in krel:
            kfilter[kbasis.index(item)] = 0
        for item in km1rel:
            km1filter[km1basis.index(item)] = 0
        newbk = np.compress(kfilter,newbk,axis=1)
        newbk = np.compress(km1filter,newbk,axis=0)
    return bk

@jit(noPython=True)
@timeit
def bksubMatrix(km1subbasis,ksubbasis,km1basis,kbasis,bk):
    """ generates a submatrix of bk using only the basis elements from the """
    """ neighborhood of interest"""
    """ reference to the kbasis and km1basis requires a consistency between the row and """
    """ col assignments and the ordering of the elements in the bases"""
    mrows = len(km1subbasis)
    ncols = len(ksubbasis)
    newbk = np.zeros((mrows,ncols))
    for row in range(mrows):
        for col in range(ncols):
            newbk[row][col] = bk[km1basis.index(km1subbasis[row])][kbasis.index(ksubbasis[col])]
    return newbk

@jit(noPython=True)
@timeit
def homology(b1,b2,tol=1e-5):
    """Compute homology from two matrices whose product b1*b2=0"""
    # let b2:Ck+1 -> Ck and b1: Ck -> Ck-1
    b2p=np.compress(np.any(abs(b2)>tol,axis=0),b2,axis=1)
    # np.any() returns a boolean vector indicating which cols of b2 (axis=0) have nonzero entries
    # np.compress removes the zero columns
    # The resulting columns form a basis for the image of b2

    # Compute kernel
    if b1.size:
        ker=kernel(b1,tol);     # returns a matrix whose columns form a basis of the null space of b1
    else:
        ker=np.eye(b1.shape[1]) # returns an identity matrix of dimension = dim(C1) (if b1 is identically 0 so that the whole space is in the kernel)

    # Remove image
    if b2.any():                              # checks if there are any non zero elements in b2?
        map,j1,j2,j3=np.linalg.lstsq(ker,b2p)  # the columns of map form a subspace of the kernel given by the image(b2) -- the least squares decomposition finds the vectors in the span of ker which best approximate the columns of b2p.
        Hk=np.dot(ker,cokernel(map,tol));  # cokernel of map is the subspace of the kernel that is orthogonal to the image(b2)
    # the dot product of the ker and coker will return a matrix whose columns will be a basis for the ker(b1)/im(b2)
    # this is just the projection of each column of the kernel onto the space spanned by the cokernel
    # we obtain im(b2) + Hk as a direct sum isomorphic to ker(b1)
    else:
        Hk=ker
    # if b2 = 0 then there is no non trivial image and Hk is just the kernel (or null space of b1)
    return Hk

@jit(noPython=True)
@timeit
def homologyDim(b1,b2,tol=1e-5):
    """Compute homology"""
    rankB1 = 0
    rankB2 = 0

    if (b1.size > 0):
        rankB1 = np.linalg.matrix_rank(b1, tol)

    if (b2.size > 0):
        rankB2 = np.linalg.matrix_rank(b2, tol)

    Hk = b1.shape[1] - rankB1 - rankB2

    return Hk

@jit(noPython=True)
@timeit
def chainComplex(toplexes, k):
    """ Compute the k-chains and boundary map for the closure of a collection of toplexes """
    """ returns ascClosure(toplexes), Ckm1,Ck,Ckp1,bk,bkp1 """
    if k<=0:
        print("Error; k must be greater than 0")
        return
    #toplexes = orientCells(toplexes) ## I think there is a bug here so require toplexes to be oriented
    allcomplx = closure(toplexes)
    Ckm1 = kchainBasis(allcomplx, k-1)
    Ck = kchainBasis(allcomplx,k)
    Ckp1 = kchainBasis(allcomplx,k+1)
    bk = bkMatrix(Ckm1,Ck)
    bkp1 = bkMatrix(Ck,Ckp1)
    return allcomplx,Ckm1,Ck,Ckp1,bk,bkp1

@jit(noPython=True)
@timeit
def localhomology4(simplices, nk, k, allcomplx, Ckm1,Ck,Ckp1,bk,bkp1, closed = False, dim = True):
    """ compute the kth local homology in an nk neighborhood of simplices """
    Y = complement(allcomplx, simplices, nk, closed)
    Ckm1sub = kchainBasis(allcomplx,k-1,Y)
    Cksub = kchainBasis(allcomplx,k,Y)
    Ckp1sub = kchainBasis(allcomplx,k+1,Y)
    bksub = bksubMatrix(Ckm1sub,Cksub,Ckm1,Ck,bk)
    bkp1sub = bksubMatrix(Cksub,Ckp1sub,Ck,Ckp1,bkp1)
    if dim:
        return homologyDim(bksub,bkp1sub)
    else:
        return homology(bksub,bkp1sub)

@jit(noPython=True)
@timeit
def localhomology(toplexes, k, simplices, dim = False):
    """ Intended to match the parameters of the original simplicialHomology code"""
    """ sets up: localhomology4(simplices, nk = neigh size, k = homo dim, allcomplx, Ckm1,Ck,Ckp1,bk,bkp1, closed = False) """
    """ uses excision: computes relative homology of simplices with respect to its closure"""
    #     simplices = orientCells(simplices)
    #     allcomplx = closure(simplices) ## this is effectively an excision as we are in an asc we just take the closure of the simplices
    #     #### this also eliminated the need for toplexes, it is assumed simplices are closed in toplexes
    #     #### so allcomplx can just be the closure of the simplices
    #     Ckm1 = kchainBasis(allcomplx,k-1)
    #     Ck = kchainBasis(allcomplx,k)
    #     Ckp1 = kchainBasis(allcomplx,k+1)
    #     bk = bkMatrix(Ckm1,Ck,k)
    #     bkp1 = bkMatrix(Ck,Ckp1,k+1)

    allcomplx,Ckm1,Ck,Ckp1,bk,bkp1 =  chainComplex(simplices, k)

    Y = complement(allcomplx, simplices, 0)  ### complement of star of simplices
    Ckm1sub = kchainBasis(allcomplx,k-1,Y)
    Cksub = kchainBasis(allcomplx,k,Y)
    Ckp1sub = kchainBasis(allcomplx,k+1,Y)
    bksub = bksubMatrix(Ckm1sub,Cksub,Ckm1,Ck,bk)
    bkp1sub = bksubMatrix(Cksub,Ckp1sub,Ck,Ckp1,bkp1)

    return localhomology4(simplices, 0, k, allcomplx, Ckm1, Ck, Ckp1, bk, bkp1, closed = False, dim = True)

###################
"""
    Basic workflow to construct local homology tables for all n0 neighborhoods of a Cell Complex:
    1. Impose an Orientation: It is assumed that the vertices of the complex are given in a specific order and all complexes inherit an orientation
    from this ordering. All cells will be referenced in this order. Use orientCells to impose this on an unordered list of cells.

    2. Generate the full ASC from toplexes: From  a set of ordered toplexes for X construct allcomplx = ascClosure(toplexes) = Cell Complex on X.

    3. Construct basis elements for C_k on the full graph: From allcomplx construct a canonical basis for the C_k chains
    for all k's of interest using kchainBasis(allcomplx,k).
    Using these canonical bases construct a boundary matrix bk using bk = bkMatrix(kbasis,km1basis,k). This
    will be used to generate all submatrices for local homology calculations. Rows and columns are indexed by the basis elements.

    4. Using the full basis compute local homology for a collection of cells:
    Given a collection of cells A in the Cell Complex.
    Compute the complement of the nkth neighborhood of A in the Cell Complex: Y = complement(allcomplx, complx, k)
    Construct the C_k chain subbases for this neighborhood using ksubbasis =  kchainBasis(allcomplx,k,Y)
    Then the relative boundary matrices = bksubMatrix(ksubbasis,km1subbasis,kbasis,km1basis,bk)
    Then compute the homology groups with respect to the sub basis elements:
    Hk = homology(b_(k-1), b_k)

    The last two steps are captured in localHomology(simplices, nk, k, allcomplx, Ckm1,Ck,Ckp1,bk,bkp1).
    In lhTable(toplexes) the lh dimension is computed for the nzero neighborhood of each element of the cell complex.

    """
def name(splx,ascdict={}):
    """ returns a string representative for the splx in terms of the ascdict """
    sname = ""
    if ascdict != {}:
        tname = [ascdict[x] for x in splx]
        sname = ''.join(map(str,tname))

    if sname == "":
        sname = ','.join(map(str,splx))
    return sname

def lhTable(allcomplx, ascdict={}, nk = 0 , closed = False, output_file = None, graph_file = "default"):
    """ Construct a table of LH_1,2,3 dimensions for the faces in allcomplx. """
    """ Computed on the nkth neighborhood of each face """
    """ ascdict assigns a name to each vertex """
    count = 1
    C0 = kchainBasis(allcomplx,0)
    C1 = kchainBasis(allcomplx,1)
    C2 = kchainBasis(allcomplx,2)
    C3 = kchainBasis(allcomplx,3)
    C4 = kchainBasis(allcomplx,4)
    b1 = bkMatrix(C0,C1,1)
    b2 = bkMatrix(C1,C2,2)
    b3 = bkMatrix(C2,C3,3)
    b4 = bkMatrix(C3,C4,4)


    if output_file == None:
        print(("Local Homology (neighborhood=%d closed=%s) of flag complex generated by %s\n\n" % (nk, closed, graph_file)))
        print(" ", " \t\t", "H1" , "\t" , "H2", "\t", "H3", "\t\t", "FACE")
        print("-"*50)
    else:
        ofile = open(output_file, "w")
        graph = graph_file.split("/")[-1]
        ofile.write("Local Homology (neighborhood=%d closed=%s) of flag complex generated by %s\n\n" % (nk, closed, graph))
        ofile.write(" \t\t" + "H1" + "\t" + "H2" + "\t" + "H3" + "\t\t" + "name" + "\n")
    basis = [C4,C3,C2,C1,C0]
    for b in basis:
        for splx in b:
            H1 = localhomology4([splx], nk, 1, allcomplx, C0,C1,C2,b1,b2, closed).shape[1]
            H2 = localhomology4([splx], nk, 2, allcomplx, C1,C2,C3,b2,b3, closed).shape[1]
            H3 = localhomology4([splx], nk, 3, allcomplx, C2,C3,C4,b3,b4, closed).shape[1]
            if output_file == None:
                print(count, "\t\t", H1 , "\t" , H2, "\t", H3, "\t\t", name(splx,ascdict))
                count += 1
            else:
                ofile.write(str(count) + "\t\t" + str(H1) + "\t" + str(H2) + "\t" + str(H3) + "\t\t" + name(splx,ascdict) + "\n")
                count += 1
    return
