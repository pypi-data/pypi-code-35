#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `wis` package."""

# -----------------------------------------
# Third-party imports
# -----------------------------------------
import spiceypy as sp
import pytest
import os
import shutil
import numpy as np
from astropy.time import Time

# -----------------------------------------
# Local imports
# -----------------------------------------
from wis import wis

# -----------------------------------------
# Test Functions
# -----------------------------------------


def test_obscodeDict_A():
    
    """Test obscodeDict exists and has content."""
    assert isinstance(wis.obscodeDict, dict), 'Problem with wis.obscodeDict: not a dict? '
    assert len(wis.obscodeDict) > 0 ,         'Problem with wis.obscodeDict: no entries? %r' % wis.obscodeDict

def test_obscodeDict_B():

    """Test obscodeDict has all expected entries"""
    assert '-95' in wis.obscodeDict,          'TESS key (-95) not in wis.obscodeDict'
    assert '-227' in wis.obscodeDict,         'K2  key (-227) not in wis.obscodeDict'
    assert '-82' in wis.obscodeDict,         'CASSINI  key (-82) not in wis.obscodeDict'

def test_obscodeDict_C():
    """Test obscodeDict values are Instructions-objects"""
    for k,v in wis.obscodeDict.items():
        assert isinstance(v, wis.Instructions), '[%r] for [%r] not an Instructions-object' % (v,k)

def test_obscodeDict_D():
    """Test Instructions-objects contain minimum requirements"""
    for k,v in wis.obscodeDict.items():
        for requiredKey in ['obscode','name', 'files']:
            assert hasattr(v, requiredKey), 'requiredKey [%r] not in (%r, %r)' % (requiredKey,k,v)


'''
    
def test_Manager_download_dir_A():
    """Test that a download directory can be created/accessed"""
    dd = wis.Manager().define_download_dir()
    assert os.path.isdir(dd), 'Results of _define_download_dir [%r] not a path' % dd


def test_Manager_download_dir_B():
    """Test that a download sub-directory can be created/accessed"""
    obscode = '-95'
    # Need to define an obscode & JD to allow the Manager-object to be created
    M = wis.Manager()
    dd = M.define_download_dir()
    # Use the method to get the subdirectory
    sd = M.define_download_subdir(obscode)
    # Assert that the returned subdirectory has the expected name
    expectedName = os.path.join(dd,obscode)
    assert sd == expectedName, ' Sub-dir names not the same: [%r],[%r]' % (sd , expectedName)

    # Deliberately delete the subdirectory
    if os.path.isdir(sd):
        shutil.rmtree(sd)
    assert not os.path.isdir(sd), 'Unexpectedly could not remove path [%r]' % sd

    # Now call the define_download_subdir method again and check that the directory is created
    sd = M.define_download_subdir(obscode)
    assert os.path.isdir(sd), 'download_subdir [%r] not a path' % sd





def test_Instructions_download_A():
    """ Test that direct file download works (using 'download_data()' )  """
    """ N.B. This also tests underlying 'kernels_have_been_downloaded()' """
    
    # *** SET-UP : CREATE EMPTY SUB-DIRECTORY ********************
    # Need to define an obscode to allow the objects to be created
    obscode = '-95'
    sd = convenience_function_to_create_empty_subdirectory(obscode)
    
    # *** SET-UP Instructions-Object *****************************
    I = wis.obscodeDict[obscode]
    
    # *** TEST "download_data()" *********************************
    # Assert that the required files exist
    downloadedKernelFiles =  I.download_data(sd)
    for f in I.files :
        assert f[f.rfind("/")+1:] in downloadedKernelFiles
        
    # *** TEST "kernels_have_been_downloaded()"*******************
    # Assert that the required files exist
    downloaded, downloadedKernelFiles =  I.kernels_have_been_downloaded(sd)
    assert downloaded , ' Expected downloaded to be True, but : [%r]'% downloaded
    for f in I.files:
        assert f[f.rfind("/")+1:] in downloadedKernelFiles
    
    
'''




def test_Satellite_A():
    """Test that a Satellite-object can be created/accessed"""
    time    = Time([2458337.8283571], format='jd', scale='tdb')
    obscode = '-95'
    returnedOC     = wis.Satellite(obscode, time).obscode
    assert returnedOC == obscode, 'Returned obscode [%r] does not match input [%r]' % (returnedOC , obscode)
    returnedOC     = wis.Satellite(obscode, time, center = 'SUN').obscode
    assert returnedOC == obscode, 'Returned obscode [%r] does not match input [%r]' % (returnedOC , obscode)





def test_Satellite_B():
    """Test that a Satellite-object correctly calculates internal epochs (consistent with sp.utc2et() )"""
    # Make a Satellite-object and get the epochs
    time    = Time([2458337.8283571, 2458337.9], format='jd', scale='tdb')
    obscode = '-95'
    returnedEpochs = wis.Satellite(obscode, time).epochs
    
    # Check epoch calcs are correct
    for i, jd in enumerate(time.utc.jd):
        assert returnedEpochs[i] == sp.utc2et('JD'+str(jd)), \
            'Returned epoch [%r] does not match calculation from spiceypy [%r]' % (returnedEpochs[i] , jd)


def test_Satellite_C():
    """Test that a Satellite-object returns posns and ltts"""
    # Make a Satellite-object
    time    = Time([2458337.8283571, 2458337.9], format='jd', scale='tdb')
    obscode = '-95'
    S = wis.Satellite(obscode, time)
    # Assert that the returned quantities are of the correct shape and type
    assert S.posns.shape == (2,3), 'Returned posns not of expected shape: [%r]' % S.posns
    assert S.ltts.shape  == (2,),  'Returned ltts  not of expected shape: [%r]' % S.ltts


    
def test_Satellite_D():
    """Test that a Satellite-object returns the expected positions"""
    # Make a Satellite-object
    time    = Time([2458337.829157830], format='jd', scale='tdb')
    obscode = '-95'
    S = wis.Satellite(obscode, time)
    
    # *** DATA FROM EXPLICIT HORIZONS QUERY -------------
    '''
    Target body name: TESS (spacecraft) (-95)         {source: TESS_merged}
    Center body name: Sun (10)                        {source: TESS_merged}
    Center-site name: BODY CENTER
    *******************************************************************************
    Start time      : A.D. 2018-Aug-07 07:52:50.0534 TDB
    Stop  time      : A.D. 2018-Aug-07 09:36:00.0000 TDB
    Step-size       : 0 steps
    *******************************************************************************
    Center geodetic : 0.00000000,0.00000000,0.0000000 {E-lon(deg),Lat(deg),Alt(km)}
    Center cylindric: 0.00000000,0.00000000,0.0000000 {E-lon(deg),Dxy(km),Dz(km)}
    Center radii    : 696000.0 x 696000.0 x 696000.0 k{Equator, meridian, pole}
    Output units    : KM-D
    Output type     : GEOMETRIC cartesian states
    Output format   : 3 (position, velocity, LT, range, range-rate)
    Reference frame : ICRF/J2000.0
    Coordinate systm: Ecliptic and Mean Equinox of Reference Epoch
    *******************************************************************************
    JDTDB
    X     Y     Z
    VX    VY    VZ
    LT    RG    RR
    *******************************************************************************
    $$SOE
    2458337.829157830 = A.D. 2018-Aug-07 07:53:59.2365 TDB [del_T=     69.183095 s]
    X = 1.062342805938861E+08 Y =-1.082364019892699E+08 Z =-7.200821989670396E+04
    VX= 1.881858820191574E+06 VY= 1.709241625576401E+06 VZ= 7.348832462143537E+04
    LT= 5.855142406579759E-03 RG= 1.516602989383414E+08 RR= 9.831486948508087E+04
    2458338.829157830 = A.D. 2018-Aug-08 07:53:59.2365 TDB [del_T=     69.183072 s]
    X = 1.081418885028859E+08 Y =-1.064747162599978E+08 Z = 1.748584038066864E+04
    VX= 1.930452574054366E+06 VY= 1.842854960163861E+06 VZ= 9.692709021812357E+04
    LT= 5.859047013409530E-03 RG= 1.517614363314088E+08 RR= 8.267596292346843E+04
    $$EOE    
    '''
    # ---------------------------------------------------
    
    # Assert that the returned quantities have the expected numerical values
    # -->> We query horizons using tdb=2458337.82915783
    expectedPosns = np.array([
          [1.062342805938861E+08 ,-1.082364019892699E+08 ,-7.200821989670396E+04]                              ] )
    assert np.allclose(S.posns , expectedPosns, rtol=1e-05, atol=1e+02), \
        ' Not close enough to expected values: returned=[%r], expected=[%r]' % (S.posns , expectedPosns)


def test_Satellite_E():
    """Test that a Satellite-object returns the expected positions for multiple jdutc's """
    # Make a Satellite-object
    time    = Time([2458337.829157830, 2458338.829157830], format='jd', scale='tdb')
    obscode = '-95'
    S = wis.Satellite(obscode, time)

    # Assert that the returned quantities have the expected numerical values
    # -->> We input                   jdutc = [2458337.8283571, 2458337.8283571]
    # -->> So we query horizons using tdb   = [2458338.82915783,2458338.82915783]
    expectedPosns = np.array([
                              [1.062342805938861E+08 ,-1.082364019892699E+08 ,-7.200821989670396E+04],
                              [1.081418885028859E+08 ,-1.064747162599978E+08 ,1.748584038066864E+04]
                              ] )
    assert np.allclose(S.posns , expectedPosns, rtol=1e-05, atol=1e+02), \
        ' Not close enough to expected values: returned=[%r], expected=[%r]' % (S.posns , expectedPosns)



def test_Satellite_F():
    """Test that the position of K2 is as expected """
    # Make a Satellite-object
    time    = Time([2458337.829157830 , 2458338.829157830], format='jd', scale='tdb')
    obscode = '-227'
    S = wis.Satellite(obscode, time)

    # *** DATA FROM EXPLICIT HORIZONS QUERY -------------
    '''
        *******************************************************************************
        Ephemeris / WWW_USER Sat Apr  6 16:48:37 2019 Pasadena, USA      / Horizons
        *******************************************************************************
        Target body name: Kepler (spacecraft) (-227)      {source: KEPLER_FINAL_56_traj}
        Center body name: Sun (10)                        {source: DE431mx}
        Center-site name: BODY CENTER
        *******************************************************************************
        Start time      : A.D. 2018-Aug-07 07:53:59.2365 TDB
        Stop  time      : A.D. 2018-Aug-08 07:53:59.2365 TDB
        Step-size       : 0 steps
        *******************************************************************************
        Center geodetic : 0.00000000,0.00000000,0.0000000 {E-lon(deg),Lat(deg),Alt(km)}
        Center cylindric: 0.00000000,0.00000000,0.0000000 {E-lon(deg),Dxy(km),Dz(km)}
        Center radii    : 696000.0 x 696000.0 x 696000.0 k{Equator, meridian, pole}
        Output units    : KM-D
        Output type     : GEOMETRIC cartesian states
        Output format   : 3 (position, velocity, LT, range, range-rate)
        Reference frame : ICRF/J2000.0
        Coordinate systm: Earth Mean Equator and Equinox of Reference Epoch
        *******************************************************************************
        JDTDB
        X     Y     Z
        VX    VY    VZ
        LT    RG    RR
        *******************************************************************************
        $$SOE
        2458337.829157830 = A.D. 2018-Aug-07 07:53:59.2365 TDB [del_T=     69.183095 s]
        X =-4.858100540844912E+07 Y =-1.372859005990007E+08 Z =-5.819772565136361E+07
        VX= 2.340000498026259E+06 VY=-7.234023419283163E+05 VZ=-3.162890228925920E+05
        LT= 6.054588378363853E-03 RG= 1.568263621358534E+08 RR= 2.576522774919989E+04
        2458338.829157830 = A.D. 2018-Aug-08 07:53:59.2365 TDB [del_T=     69.183072 s]
        X =-4.623486717679888E+07 Y =-1.379916441006971E+08 Z =-5.850652841841828E+07
        VX= 2.352174577160001E+06 VY=-6.880572825335978E+05 VZ=-3.013044929887279E+05
        LT= 6.055556118005271E-03 RG= 1.568514285942110E+08 RR= 2.436672981897528E+04
        $$EOE
        *******************************************************************************
    '''

    # Assert that the returned quantities have the expected numerical values
    # -->> We input                   jdutc = [2458337.8283571, 2458337.8283571]
    # -->> So we query horizons using tdb   = [2458338.82915783,2458338.82915783]
    expectedPosns = np.array([
                              [-4.858100540844912E+07 ,-1.491070769659011E+08 , 1.213825751472302E+06],
                              [-4.623486717679888E+07 ,-1.498774186555523E+08 , 1.211233394904539E+06]
                              ] )
    assert np.allclose(S.posns , expectedPosns, rtol=1e-05, atol=1e+02), \
        ' Not close enough to expected values: returned=[%r], expected=[%r]' % (S.posns , expectedPosns)


def test_Satellite_G():
    """ Test that the position of CASSINI is as expected """
    """ Here I am repeating some of the numbers/tests from ... """
    """ ... https://spiceypy.readthedocs.io/en/master/exampleone.html """

    # Input dates ...
    time    = Time([2453176.5], format='jd', scale='utc')
    et    = sp.str2et('JD'+str(time.utc.jd[0]) )
    assert np.allclose(et, 140961664.18440723), 'time transformation inaccurate: [%r]' % et0

    # Make a Satellite-object (implicitly calculates positions):
    # - *** NOTE THE USE OF A DIFFERENT BARYCENTER & A DIFFERENT FRAME (NOT ECLIPTIC)***
    obscode ='-82'
    S = wis.Satellite(obscode, time, center='SATURN BARYCENTER', frame = "J2000")

    # Expected posnitions & ltts :
    # positions, lightTimes = spice.spkpos('Cassini', times, 'J2000', 'NONE', 'SATURN BARYCENTER')
    expectedPositions   = [-5461446.61080924, -4434793.40785864, -1200385.93315424]
    expectedLTT         = 23.8062238783
    

    # Assert calculated is close to expected ...
    assert np.allclose(S.posns , expectedPositions, rtol=1e-05, atol=1e+02), \
        ' Not close enough to expected values: returned=[%r], expected=[%r]' % (S.posns , expectedPositions)
    assert np.allclose(S.ltts  , expectedLTT, rtol=1e-05, atol=1e+02), \
    ' Not close enough to expected values: returned=[%r], expected=[%r]' % (S.ltts , expectedLTT)





# -----------------------------------------
# Convenience Functions
# -----------------------------------------

def convenience_function_to_create_empty_subdirectory(obscode):
    """ A few of the tests need an empty directory. This creates a correctly named directory"""
    # Manager-object
    M = wis.Manager()
    # Main directory
    dd = M.define_download_dir()
    # subdirectory
    sd = M.define_download_subdir(obscode)
    # Assert that the returned subdirectory has the expected name
    expectedName = os.path.join(dd,obscode)
    assert sd == expectedName, ' Sub-dir names not the same: [%r],[%r]' % (sd , expectedName)
    
    # Deliberately delete the subdirectory
    if os.path.isdir(sd):
        shutil.rmtree(sd)
    assert not os.path.isdir(sd), 'Unexpectedly could not remove path [%r]' % sd

    # Now call the define_download_subdir method again and check that the directory is created
    sd = M.define_download_subdir(obscode)
    assert os.path.isdir(sd), 'download_subdir [%r] not a path' % sd
    
    # return the filepath to the subdirectory
    return sd

def convenience_function_for_loading_spicepy_kernels():
    kernelFilepaths = []
    sp.furnsh(kernelFilepaths)


