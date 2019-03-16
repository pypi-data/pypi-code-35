#!/usr/bin/env python
# Copyright 2014-2018 The PySCF Developers. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Author: Qiming Sun <osirpt.sun@gmail.com>
#

import copy
from functools import reduce
import numpy
import scipy.linalg
from pyscf.lib import param
from pyscf.lib import logger
from pyscf import gto
from pyscf import __config__

REF_BASIS = getattr(__config__, 'lo_orth_pre_orth_ao_method', 'ANO')
ORTH_METHOD = getattr(__config__, 'lo_orth_orth_ao_method', 'meta_lowdin')
PROJECT_ECP_BASIS = getattr(__config__, 'lo_orth_project_ecp_basis', True)


def lowdin(s):
    ''' new basis is |mu> c^{lowdin}_{mu i} '''
    e, v = scipy.linalg.eigh(s)
    idx = e > 1e-15
    return numpy.dot(v[:,idx]/numpy.sqrt(e[idx]), v[:,idx].conj().T)

def schmidt(s):
    c = numpy.linalg.cholesky(s)
    return scipy.linalg.solve_triangular(c, numpy.eye(c.shape[1]), lower=True,
                                         overwrite_b=False).conj().T

def vec_lowdin(c, s=1):
    ''' lowdin orth for the metric c.T*s*c and get x, then c*x'''
    #u, w, vh = numpy.linalg.svd(c)
    #return numpy.dot(u, vh)
    # svd is slower than eigh
    return numpy.dot(c, lowdin(reduce(numpy.dot, (c.conj().T,s,c))))

def vec_schmidt(c, s=1):
    ''' schmidt orth for the metric c.T*s*c and get x, then c*x'''
    if isinstance(s, numpy.ndarray):
        return numpy.dot(c, schmidt(reduce(numpy.dot, (c.conj().T,s,c))))
    else:
        return numpy.linalg.qr(c)[0]

def weight_orth(s, weight):
    ''' new basis is |mu> c_{mu i}, c = w[(wsw)^{-1/2}]'''
    s1 = weight[:,None] * s * weight
    c = lowdin(s1)
    return weight[:,None] * c


def pre_orth_ao(mol, method=REF_BASIS):
    '''Restore AO characters.  Possible methods include the ANO/MINAO
    projection or fraction-averaged atomic RHF calculation'''
    if method.upper() in ('ANO', 'MINAO'):
# Use ANO/MINAO basis to define the strongly occupied set
        return project_to_atomic_orbitals(mol, method)
    else:
        return pre_orth_ao_atm_scf(mol)
restore_ao_character = pre_orth_ao

def project_to_atomic_orbitals(mol, basname):
    '''projected AO = |bas><bas|ANO>
    '''
    from pyscf.scf.addons import project_mo_nr2nr
    from pyscf.scf import atom_hf
    from pyscf.gto.ecp import core_configuration
    def search_atm_l(atm, l):
        bas_ang = atm._bas[:,gto.ANG_OF]
        ao_loc = atm.ao_loc_nr()
        idx = []
        for ib in numpy.where(bas_ang == l)[0]:
            idx.extend(range(ao_loc[ib], ao_loc[ib+1]))
        return idx

    # Overlap of ANO and ECP basis
    def ecp_ano_det_ovlp(atm_ecp, atm_ano, ecpcore):
        ecp_ao_loc = atm_ecp.ao_loc_nr()
        ano_ao_loc = atm_ano.ao_loc_nr()
        ecp_ao_dim = ecp_ao_loc[1:] - ecp_ao_loc[:-1]
        ano_ao_dim = ano_ao_loc[1:] - ano_ao_loc[:-1]
        ecp_bas_l = [[atm_ecp.bas_angular(i)]*d for i,d in enumerate(ecp_ao_dim)]
        ano_bas_l = [[atm_ano.bas_angular(i)]*d for i,d in enumerate(ano_ao_dim)]
        ecp_bas_l = numpy.hstack(ecp_bas_l)
        ano_bas_l = numpy.hstack(ano_bas_l)

        nelec_core = 0
        ecp_occ_tmp = []
        ecp_idx = []
        ano_idx = []
        for l in range(4):
            nocc, frac = atom_hf.frac_occ(stdsymb, l)
            l_occ = [2] * ((nocc-ecpcore[l])*(2*l+1))
            if frac > 1e-15:
                l_occ.extend([frac] * (2*l+1))
                nocc += 1
            if nocc == 0:
                break
            nelec_core += 2 * ecpcore[l] * (2*l+1)
            i0 = ecpcore[l] * (2*l+1)
            i1 = nocc * (2*l+1)
            ecp_idx.append(numpy.where(ecp_bas_l==l)[0][:i1-i0])
            ano_idx.append(numpy.where(ano_bas_l==l)[0][i0:i1])
            ecp_occ_tmp.append(l_occ[:i1-i0])
        ecp_idx = numpy.hstack(ecp_idx)
        ano_idx = numpy.hstack(ano_idx)
        ecp_occ = numpy.zeros(atm_ecp.nao_nr())
        ecp_occ[ecp_idx] = numpy.hstack(ecp_occ_tmp)
        nelec_valence_left = int(gto.mole.charge(stdsymb) - nelec_core
                                 - sum(ecp_occ[ecp_idx]))
        if nelec_valence_left > 0:
            logger.warn(mol, 'Characters of %d valence electrons are not identified.\n'
                        'It can affect the "meta-lowdin" localization method '
                        'and the population analysis of SCF method.\n'
                        'Adjustment to the core/valence partition may be needed '
                        '(see function lo.nao.set_atom_conf)\nto get reasonable '
                        'local orbitals or Mulliken population.\n',
                        nelec_valence_left)
            # Return 0 to force the projection to ANO basis
            return 0
        else:
            s12 = gto.intor_cross('int1e_ovlp', atm_ecp, atm_ano)[ecp_idx][:,ano_idx]
            return numpy.linalg.det(s12)

    nelec_ecp_dic = {}
    for ia in range(mol.natm):
        symb = mol.atom_symbol(ia)
        if symb not in nelec_ecp_dic:
            nelec_ecp_dic[symb] = mol.atom_nelec_core(ia)

    aos = {}
    atm = gto.Mole()
    atmp = gto.Mole()
    for symb in mol._basis.keys():
        stdsymb = gto.mole._std_symbol(symb)
        atm._atm, atm._bas, atm._env = \
                atm.make_env([[stdsymb,(0,0,0)]], {stdsymb:mol._basis[symb]}, [])
        atm.cart = mol.cart
        atm._built = True
        s0 = atm.intor_symmetric('int1e_ovlp')

        if gto.is_ghost_atom(symb):
            aos[symb] = numpy.diag(1./numpy.sqrt(s0.diagonal()))
            continue

        basis_add = gto.basis.load(basname, stdsymb)
        atmp._atm, atmp._bas, atmp._env = \
                atmp.make_env([[stdsymb,(0,0,0)]], {stdsymb:basis_add}, [])
        atmp.cart = mol.cart
        atmp._built = True

        if symb in nelec_ecp_dic and nelec_ecp_dic[symb] > 0:
            if not PROJECT_ECP_BASIS:
# If ECP basis has good atomic character, ECP basis can be used in the
# localization/population analysis directly. Otherwise project ECP basis to
# ANO basis.
                continue

            ecpcore = core_configuration(nelec_ecp_dic[symb])
# Comparing to ANO valence basis, to check whether the ECP basis set has
# reasonable AO-character contraction.  The ANO valence AO should have
# significant overlap to ECP basis if the ECP basis has AO-character.
            if abs(ecp_ano_det_ovlp(atm, atmp, ecpcore)) > .1:
                aos[symb] = numpy.diag(1./numpy.sqrt(s0.diagonal()))
                continue
        else:
            ecpcore = [0] * 4

        ano = project_mo_nr2nr(atmp, numpy.eye(atmp.nao_nr()), atm)
        rm_ano = numpy.eye(ano.shape[0]) - reduce(numpy.dot, (ano, ano.T, s0))
        c = rm_ano.copy()
        for l in range(param.L_MAX):
            idx = numpy.asarray(search_atm_l(atm, l))
            nbf_atm_l = len(idx)
            if nbf_atm_l == 0:
                break

            idxp = numpy.asarray(search_atm_l(atmp, l))
            if l < 4:
                idxp = idxp[ecpcore[l]:]
            nbf_ano_l = len(idxp)

            if mol.cart:
                degen = (l + 1) * (l + 2) // 2
            else:
                degen = l * 2 + 1

            if nbf_atm_l > nbf_ano_l > 0:
# For angular l, first place the projected ANO, then the rest AOs.
                sdiag = reduce(numpy.dot, (rm_ano[:,idx].T, s0, rm_ano[:,idx])).diagonal()
                nleft = (nbf_atm_l - nbf_ano_l) // degen
                shell_average = numpy.einsum('ij->i', sdiag.reshape(-1,degen))
                shell_rest = numpy.argsort(-shell_average)[:nleft]
                idx_rest = []
                for k in shell_rest:
                    idx_rest.extend(idx[k*degen:(k+1)*degen])
                c[:,idx[:nbf_ano_l]] = ano[:,idxp]
                c[:,idx[nbf_ano_l:]] = rm_ano[:,idx_rest]
            elif nbf_ano_l >= nbf_atm_l > 0:  # More ANOs than the mol basis functions
                c[:,idx] = ano[:,idxp[:nbf_atm_l]]
        sdiag = numpy.einsum('pi,pq,qi->i', c, s0, c)
        c *= 1./numpy.sqrt(sdiag)
        aos[symb] = c

    nao = mol.nao_nr()
    c = numpy.zeros((nao,nao))
    p1 = 0
    for ia in range(mol.natm):
        symb = mol.atom_symbol(ia)
        if symb in mol._basis:
            ano = aos[symb]
        else:
            ano = aos[mol.atom_pure_symbol(ia)]
        p0, p1 = p1, p1 + ano.shape[1]
        c[p0:p1,p0:p1] = ano
    return c
pre_orth_project_ano = project_to_atomic_orbitals

def pre_orth_ao_atm_scf(mol):
    assert(not mol.cart)
    from pyscf.scf import atom_hf
    atm_scf = atom_hf.get_atm_nrhf(mol)
    nbf = mol.nao_nr()
    c = numpy.zeros((nbf,nbf))
    p0 = 0
    for ia in range(mol.natm):
        symb = mol.atom_symbol(ia)
        if symb in atm_scf:
            e_hf, mo_e, mo_c, mo_occ = atm_scf[symb]
        else:
            symb = mol.atom_pure_symbol(ia)
            e_hf, mo_e, mo_c, mo_occ = atm_scf[symb]
        p1 = p0 + mo_e.size
        c[p0:p1,p0:p1] = mo_c
        p0 = p1
    return c


def orth_ao(mf_or_mol, method=ORTH_METHOD, pre_orth_ao=None, scf_method=None,
            s=None):
    '''Orthogonalize AOs

    Kwargs:
        method : str
            One of
            | lowdin : Symmetric orthogonalization
            | meta-lowdin : Lowdin orth within core, valence, virtual space separately (JCTC, 10, 3784)
            | NAO
    '''
    from pyscf.lo import nao
    mf = scf_method
    if isinstance(mf_or_mol, gto.Mole):
        mol = mf_or_mol
    else:
        mol = mf_or_mol.mol
        if mf is None:
            mf = mf_or_mol

    if s is None:
        if getattr(mol, 'pbc_intor', None):  # whether mol object is a cell
            s = mol.pbc_intor('int1e_ovlp', hermi=1)
        else:
            s = mol.intor_symmetric('int1e_ovlp')

    if pre_orth_ao is None:
#        pre_orth_ao = numpy.eye(mol.nao_nr())
        pre_orth_ao = project_to_atomic_orbitals(mol, REF_BASIS)

    if method.lower() == 'lowdin':
        s1 = reduce(numpy.dot, (pre_orth_ao.conj().T, s, pre_orth_ao))
        c_orth = numpy.dot(pre_orth_ao, lowdin(s1))
    elif method.lower() == 'nao':
        assert(mf is not None)
        c_orth = nao.nao(mol, mf, s)
    else: # meta_lowdin: divide ao into core, valence and Rydberg sets,
          # orthogonalizing within each set
        weight = numpy.ones(pre_orth_ao.shape[0])
        c_orth = nao._nao_sub(mol, weight, pre_orth_ao, s)
    # adjust phase
    for i in range(c_orth.shape[1]):
        if c_orth[i,i] < 0:
            c_orth[:,i] *= -1
    return c_orth

del(ORTH_METHOD)


if __name__ == '__main__':
    from pyscf import gto
    from pyscf import scf
    from pyscf.lo import nao
    mol = gto.Mole()
    mol.verbose = 1
    mol.output = 'out_orth'
    mol.atom.extend([
        ['O' , (0. , 0.     , 0.)],
        [1   , (0. , -0.757 , 0.587)],
        [1   , (0. , 0.757  , 0.587)] ])
    mol.basis = {'H': '6-31g',
                 'O': '6-31g',}
    mol.build()

    mf = scf.RHF(mol)
    mf.scf()

    c0 = nao.prenao(mol, mf.make_rdm1())
    c = orth_ao(mol, 'meta_lowdin', c0)

    s = mol.intor_symmetric('int1e_ovlp_sph')
    p = reduce(numpy.dot, (s, mf.make_rdm1(), s))
    print(reduce(numpy.dot, (c.T, p, c)).diagonal())
