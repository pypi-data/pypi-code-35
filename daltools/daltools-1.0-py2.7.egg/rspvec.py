#!/usr/bin/env python
"""Module for reading response vector data from RSPVEC"""

THRESHOLD = 1e-5

import sys
import numpy as np
import time
from util import full
from fortran_binary import FortranBinary

class RspVecError(Exception): pass

def read(*args, **kwargs):
    """Read response vector given property"""
    if 'freqs' in kwargs:
        #linear response/one frequency
        bfreqs = kwargs.get('freqs')
    else:
        #non-linear response/two frequencies
        bfreqs = kwargs.get('bfreqs', (0.0,))
    cfreqs = kwargs.get('cfreqs', (0.0,))
    propfile = kwargs.get('propfile', 'RSPVEC')
    lr_vecs = kwargs.get('lr_vecs', False)

    rspvec = FortranBinary(propfile)
    vecs = {}

    
    for rec in rspvec:
        for lab in args:
            try:
                lab1 = bytes(lab.ljust(16), 'utf-8')
            except TypeError:
                lab1 = bytes(lab.ljust(16))
            #alternative label with permuted labels
            lab2 = lab1[8:] + lab1[:8]
            if lab1 in rec or lab2 in rec:
                if lab1 in rec:
                    rec.read(16,'c')
                    bfreq, cfreq = rec.read(2, 'd')
                elif lab2 in rec:
                    rec.read(16,'c')
                    cfreq, bfreq = rec.read(2, 'd')
                if bfreq in bfreqs and cfreq in cfreqs:
                    rspvec.next()
                    kzyvar = rspvec.reclen // 8
                    buffer_ = rspvec.readbuf(kzyvar,'d')
                    vecs[(lab, bfreq, cfreq)] = \
                       np.array(buffer_).view(full.matrix)
                    vecs[(lab1, bfreq, bfreq)] = vecs[(lab, bfreq, cfreq)]
                    vecs[(lab2, cfreq, bfreq)] = vecs[(lab, bfreq, cfreq)]


    # now check that all required vectors are saved
    for l in args:
        for b in bfreqs:
            for c in cfreqs:
                if (l, b, c) not in vecs:
                    raise RspVecError(
                        "Response vector N(%s,%g,%g) not found on file %s" %
                        (l, b, c, propfile)
                    )

    # complement dict with lr pointers
    if cfreqs == (0.0,):
        vecs.update({(l,b):vecs[(l,b,0.0)]  for l in args for b in bfreqs})
        if bfreqs == (0.0,):
            vecs.update({l:vecs[(l,0.0,0.0)]  for l in args})
    if lr_vecs:
        keys = ((a, w) for a in args for w in bfreqs)
        return {k: vecs[k] for k in keys}
    else:
        return vecs
    #return [[vecs[(l, b, c)] for l in args] for b in bfreqs for c in cfreqs]

def readall(property_label, propfile="RSPVEC"):
    """Read response all vectors given property"""
    import time, numpy
    _rspvec = FortranBinary(propfile)
    found=[]
    while _rspvec.find(property_label) is not None:
        veclabs = _rspvec.rec.read(16,'c')
        vfreq = _rspvec.rec.read(1, 'd')[0]
        _rspvec.next()
        kzyvar = _rspvec.reclen // 8
        buffer_ = _rspvec.readbuf(kzyvar,'d')
        mat = numpy.array(buffer_).view(full.matrix)
        found.append((mat, vfreq))
    return found

def tomat(N, ifc, tmpdir='/tmp'):
    """Vector to matrix"""
    import os
    norbt = ifc.norbt
    new = full.matrix((norbt, norbt))
    lwop = len(N)//2
    ij = 0
    for i, j in jwop(ifc):
        new[i, j] = N[ij]
        new[j, i] = N[ij+lwop]
        ij += 1
    return new

def tovec(mat, ifc, tmpdir='/tmp'):
    """Vector to matrix"""
    import os
    lwop = ifc.nisht*ifc.nasht + ifc.nocct*(ifc.norbt-ifc.nocct)
    N = full.matrix((2*lwop,))
    ij = 0
    for i, j in  jwop(ifc):
        N[ij] = mat[i, j]
        N[ij+lwop] = mat[j, i]
        ij += 1
    return N

def jwop(ifc):
    """Generate  orbital excitation list"""
    for i in range(ifc.nisht):
        for j in range(ifc.nisht, ifc.nocct):
            yield (i, j)
    for i in range(ifc.nisht):
        for j in range(ifc.nocct, ifc.norbt):
            yield (i, j)
    for i in range(ifc.nisht,ifc.nocct):
        for j in range(ifc.nocct, ifc.norbt):
            yield (i, j)

def main():#pragma: no cover
    import sys
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('prop', help='Response property')
    parser.add_argument('filename', help='File of response vectors(RSPVEC)')
    parser.add_argument('--w', type=float, default=0., help='Frequency')
    args = parser.parse_args()
    rvec = read(args.prop, propfile=args.filename, freqs=(args.w,))
    print(rvec.keys())

if __name__ == "__main__":#pragma: no cover
    sys.exit(main())
