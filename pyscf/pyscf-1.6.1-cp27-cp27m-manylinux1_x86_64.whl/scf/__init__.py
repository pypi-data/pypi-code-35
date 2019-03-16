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

'''
Hartree-Fock
============

Simple usage::

    >>> from pyscf import gto, scf
    >>> mol = gto.M(atom='H 0 0 0; H 0 0 1')
    >>> mf = scf.RHF(mol).run()

:func:`scf.RHF` returns an instance of SCF class.  There are some parameters
to control the SCF method.

    verbose : int
        Print level.  Default value equals to :class:`Mole.verbose`
    max_memory : float or int
        Allowed memory in MB.  Default value equals to :class:`Mole.max_memory`
    chkfile : str
        checkpoint file to save MOs, orbital energies etc.
    conv_tol : float
        converge threshold.  Default is 1e-10
    max_cycle : int
        max number of iterations.  Default is 50
    init_guess : str
        initial guess method.  It can be one of 'minao', 'atom', '1e', 'chkfile'.
        Default is 'minao'
    DIIS : class listed in :mod:`scf.diis`
        Default is :class:`diis.SCF_DIIS`. Set it to None/False to turn off DIIS.
    diis : bool
        whether to do DIIS.  Default is True.
    diis_space : int
        DIIS space size.  By default, 8 Fock matrices and errors vector are stored.
    diis_start_cycle : int
        The step to start DIIS.  Default is 0.
    level_shift_factor : float or int
        Level shift (in AU) for virtual space.  Default is 0.
    direct_scf : bool
        Direct SCF is used by default.
    direct_scf_tol : float
        Direct SCF cutoff threshold.  Default is 1e-13.
    callback : function
        callback function takes one dict as the argument which is
        generated by the builtin function :func:`locals`, so that the
        callback function can access all local variables in the current
        envrionment.
    conv_check : bool
        An extra cycle to check convergence after SCF iterations.

    nelec : (int,int), for UHF/ROHF class
        freeze the number of (alpha,beta) electrons.

    irrep_nelec : dict, for symmetry- RHF/ROHF/UHF class only
        to indicate the number of electrons for each irreps.
        In RHF, give {'ir_name':int, ...} ;
        In ROHF/UHF, give {'ir_name':(int,int), ...} .
        It is effective when :attr:`Mole.symmetry` is set ``True``.

    auxbasis : str, for density fitting SCF only
        Auxiliary basis for density fitting.

        >>> mf = scf.density_fit(scf.UHF(mol))
        >>> mf.scf()

        Density fitting can be applied to all non-relativistic HF class.

    with_ssss : bool, for Dirac-Hartree-Fock only
        If False, ignore small component integrals (SS|SS).  Default is True.
    with_gaunt : bool, for Dirac-Hartree-Fock only
        If False, ignore Gaunt interaction.  Default is False.

Saved results

    converged : bool
        SCF converged or not
    e_tot : float
        Total HF energy (electronic energy plus nuclear repulsion)
    mo_energy : 
        Orbital energies
    mo_occ
        Orbital occupancy
    mo_coeff
        Orbital coefficients

'''

from pyscf.scf import hf
rhf = hf
from pyscf.scf import rohf
from pyscf.scf import hf_symm
rhf_symm = hf_symm
from pyscf.scf import uhf
from pyscf.scf import uhf_symm
from pyscf.scf import ghf
from pyscf.scf import ghf_symm
from pyscf.scf import dhf
from pyscf.scf import chkfile
from pyscf.scf import addons
from pyscf.scf import diis
from pyscf.scf.diis import DIIS, CDIIS, EDIIS, ADIIS
from pyscf.scf.uhf import spin_square
from pyscf.scf.hf import get_init_guess
from pyscf.scf.addons import *


def HF(mol, *args):
    __doc__ = '''This is a wrap function to decide which SCF class to use, RHF or UHF\n
    ''' + hf.SCF.__doc__
    if mol.nelectron == 1 or mol.spin == 0:
        return RHF(mol, *args)
    else:
        return UHF(mol, *args)

def RHF(mol, *args):
    __doc__ = '''This is a wrap function to decide which SCF class to use, RHF or ROHF\n
    ''' + hf.RHF.__doc__
    if mol.nelectron == 1:
        if mol.symmetry:
            return rhf_symm.HF1e(mol)
        else:
            return rohf.HF1e(mol)
    elif not mol.symmetry or mol.groupname is 'C1':
        if mol.spin > 0:
            return rohf.ROHF(mol, *args)
        else:
            return rhf.RHF(mol, *args)
    else:
        if mol.spin > 0:
            return rhf_symm.ROHF(mol, *args)
        else:
            return rhf_symm.RHF(mol, *args)

def ROHF(mol, *args):
    __doc__ = '''This is a wrap function to decide which ROHF class to use.\n
    ''' + rohf.ROHF.__doc__
    if not mol.symmetry or mol.groupname is 'C1':
        return rohf.ROHF(mol, *args)
    else:
        return hf_symm.ROHF(mol, *args)

def UHF(mol, *args):
    __doc__ = '''This is a wrap function to decide which UHF class to use.\n
    ''' + uhf.UHF.__doc__
    if mol.nelectron == 1:
        if not mol.symmetry or mol.groupname is 'C1':
            return uhf.HF1e(mol, *args)
        else:
            return uhf_symm.HF1e(mol, *args)
    elif not mol.symmetry or mol.groupname is 'C1':
        return uhf.UHF(mol, *args)
    else:
        return uhf_symm.UHF(mol, *args)

def GHF(mol, *args):
    __doc__ = '''Non-relativistic generalized Hartree-Fock class.\n
    ''' + ghf.GHF.__doc__
    if not mol.symmetry or mol.groupname is 'C1':
        return ghf.GHF(mol, *args)
    else:
        return ghf_symm.GHF(mol, *args)

def DHF(mol, *args):
    '''This is a wrap function to decide which Dirac-Hartree-Fock class to use.\n
    ''' + dhf.UHF.__doc__
    if mol.nelectron == 1:
        return dhf.HF1e(mol)
    else:
        return dhf.UHF(mol, *args)


def X2C(mol, *args):
    '''X2C UHF (in testing)'''
    from pyscf.x2c import x2c
    return x2c.UHF(mol, *args)

def sfx2c1e(mf):
    return mf.sfx2c1e()
sfx2c = sfx2c1e

def density_fit(mf, auxbasis=None, with_df=None):
    return mf.density_fit(auxbasis, with_df)

def newton(mf):
    from pyscf.soscf import newton_ah
    return newton_ah.newton(mf)

def fast_newton(mf, mo_coeff=None, mo_occ=None, dm0=None,
                auxbasis=None, dual_basis=None, **newton_kwargs):
    '''This is a wrap function which combines several operations. This
    function first setup the initial guess
    from density fitting calculation then use  for
    Newton solver and call Newton solver.
    Newton solver attributes [max_cycle_inner, max_stepsize, ah_start_tol,
    ah_conv_tol, ah_grad_trust_region, ...] can be passed through **newton_kwargs.
    '''
    import copy
    from pyscf.lib import logger
    from pyscf import df
    from pyscf.soscf import newton_ah
    if auxbasis is None:
        auxbasis = df.addons.aug_etb_for_dfbasis(mf.mol, 'ahlrichs', beta=2.5)
    if dual_basis:
        mf1 = newton(mf)
        pmol = mf1.mol = newton_ah.project_mol(mf.mol, dual_basis)
        mf1 = density_fit(mf1, auxbasis)
    else:
        mf1 = density_fit(newton(mf), auxbasis)
    mf1.direct_scf_tol = 1e-7

    if getattr(mf, 'grids', None):
        from pyscf.dft import gen_grid
        approx_grids = gen_grid.Grids(mf.mol)
        approx_grids.verbose = 0
        approx_grids.level = max(0, mf.grids.level-2)
        mf1.grids = approx_grids

        approx_numint = copy.copy(mf._numint)
        mf1._numint = approx_numint
    for key in newton_kwargs:
        setattr(mf1, key, newton_kwargs[key])

    if mo_coeff is None or mo_occ is None:
        mo_coeff, mo_occ = mf.mo_coeff, mf.mo_occ

    if dm0 is not None:
        mo_coeff, mo_occ = mf1.from_dm(dm0)
    elif mo_coeff is None or mo_occ is None:
        logger.note(mf, '========================================================')
        logger.note(mf, 'Generating initial guess with DIIS-SCF for newton solver')
        logger.note(mf, '========================================================')
        if dual_basis:
            mf0 = copy.copy(mf)
            mf0.mol = pmol
            mf0 = density_fit(mf0, auxbasis)
        else:
            mf0 = density_fit(mf, auxbasis)
        mf0.direct_scf_tol = 1e-7
        mf0.conv_tol = 3.
        mf0.conv_tol_grad = 1.
        if mf0.level_shift == 0:
            mf0.level_shift = .2
        if getattr(mf, 'grids', None):
            mf0.grids = approx_grids
            mf0._numint = approx_numint
# Note: by setting small_rho_cutoff, dft.get_veff function may overwrite
# approx_grids and approx_numint.  It will further changes the corresponding
# mf1 grids and _numint.  If inital guess dm0 or mo_coeff/mo_occ were given,
# dft.get_veff are not executed so that more grid points may be found in
# approx_grids.
            mf0.small_rho_cutoff = mf.small_rho_cutoff * 10
        mf0.kernel()
        mf1.with_df = mf0.with_df
        mo_coeff, mo_occ = mf0.mo_coeff, mf0.mo_occ

        if dual_basis:
            if mo_occ.ndim == 2:
                mo_coeff =(project_mo_nr2nr(pmol, mo_coeff[0], mf.mol),
                           project_mo_nr2nr(pmol, mo_coeff[1], mf.mol))
            else:
                mo_coeff = project_mo_nr2nr(pmol, mo_coeff, mf.mol)
            mo_coeff, mo_occ = mf1.from_dm(mf.make_rdm1(mo_coeff,mo_occ))
        mf0 = None

        logger.note(mf, '============================')
        logger.note(mf, 'Generating initial guess end')
        logger.note(mf, '============================')

    mf1.kernel(mo_coeff, mo_occ)
    mf.converged = mf1.converged
    mf.e_tot     = mf1.e_tot
    mf.mo_energy = mf1.mo_energy
    mf.mo_coeff  = mf1.mo_coeff
    mf.mo_occ    = mf1.mo_occ

#    mf = copy.copy(mf)
#    def mf_kernel(*args, **kwargs):
#        logger.warn(mf, "fast_newton is a wrap function to quickly setup and call Newton solver. "
#                    "There's no need to call kernel function again for fast_newton.")
#        del(mf.kernel)  # warn once and remove circular depdence
#        return mf.e_tot
#    mf.kernel = mf_kernel
    return mf

def fast_scf(mf):  # pragma: no cover
    from pyscf.lib import logger
    logger.warn(mf, 'NOTE function fast_scf will be removed in the next release. '
                'Use function fast_newton instead')
    return fast_newton(mf)


def KS(mol, *args):
    from pyscf import dft
    return dft.KS(mol)

def RKS(mol, *args):
    from pyscf import dft
    return dft.RKS(mol)

def ROKS(mol, *args):
    from pyscf import dft
    return dft.ROKS(mol, *args)

def UKS(mol, *args):
    from pyscf import dft
    return dft.UKS(mol, *args)

def GKS(mol, *args):
    from pyscf import dft
    return dft.GKS(mol, *args)


