# Implement Cloud-In-Cell deposition (i.e. linear weights) for histogramming
# by Remi Rehe
# https://github.com/openPMD/openPMD-viewer/pull/185


import numba
import math
import numpy as np


@numba.njit
def particle_energy( q1, q2, q3 ):
    """
    calcuate particle gamma
    """
    energy = np.sqrt(1.+q1**2+q2**2+q3**2)-1.
    return( energy )


@numba.njit
def histogram_cic_1d( q1, w, nbins, bins_start, bins_end ):
    """
    Return an 1D histogram of the values in `q1` weighted by `w`,
    consisting of `nbins` evenly-spaced bins between `bins_start`
    and `bins_end`. Contribution to each bins is determined by the
    CIC weighting scheme (i.e. linear weights).
    """
    # Define various scalars
    bin_spacing = (bins_end-bins_start)/nbins
    inv_spacing = 1./bin_spacing
    n_ptcl = len(w)

    # Allocate array for histogrammed data
    hist_data = np.zeros( nbins, dtype=np.float64 )

    # Go through particle array and bin the data
    for i in range(n_ptcl):
        # Calculate the index of lower bin to which this particle contributes
        q1_cell = (q1[i] - bins_start) * inv_spacing
        i_low_bin = int(math.floor( q1_cell ))
        # Calculate corresponding CIC shape and deposit the weight
        S_low = 1. - (q1_cell - i_low_bin)
        if (i_low_bin >= 0) and (i_low_bin < nbins):
            hist_data[ i_low_bin ] += w[i] * S_low
        if (i_low_bin + 1 >= 0) and (i_low_bin + 1 < nbins):
            hist_data[ i_low_bin + 1 ] += w[i] * (1. - S_low)

    return( hist_data )


@numba.njit
def histogram_cic_2d( q1, q2, w, nbins_1, bins_start_1, bins_end_1, nbins_2, bins_start_2, bins_end_2 ):
    """
    Return an 2D histogram of the values in `q1` and `q2` weighted by `w`,
    consisting of `nbins_1` bins in the first dimension and `nbins_2` bins
    in the second dimension.
    Contribution to each bins is determined by the
    CIC weighting scheme (i.e. linear weights).
    """
    # Define various scalars
    bin_spacing_1 = (bins_end_1-bins_start_1)/nbins_1
    inv_spacing_1 = 1./bin_spacing_1
    bin_spacing_2 = (bins_end_2-bins_start_2)/nbins_2
    inv_spacing_2 = 1./bin_spacing_2
    n_ptcl = len(w)

    # Allocate array for histogrammed data
    hist_data = np.zeros( (nbins_1, nbins_2), dtype=np.float64 )

    # Go through particle array and bin the datae
    for i in range(n_ptcl):

        # Calculate the index of lower bin to which this particle contributes
        q1_cell = (q1[i] - bins_start_1) * inv_spacing_1
        q2_cell = (q2[i] - bins_start_2) * inv_spacing_2
        i1_low_bin = int(math.floor( q1_cell ))
        i2_low_bin = int(math.floor( q2_cell ))

        # Calculate corresponding CIC shape and deposit the weight
        S1_low = 1. - (q1_cell - i1_low_bin)
        S2_low = 1. - (q2_cell - i2_low_bin)
        if (i1_low_bin >= 0) and (i1_low_bin < nbins_1):
            if (i2_low_bin >= 0) and (i2_low_bin < nbins_2):
                hist_data[ i1_low_bin, i2_low_bin ] += w[i]*S1_low*S2_low
            if (i2_low_bin+1 >= 0) and (i2_low_bin+1 < nbins_2):
                hist_data[ i1_low_bin, i2_low_bin+1 ] += w[i]*S1_low*(1.-S2_low)
        if (i1_low_bin+1 >= 0) and (i1_low_bin+1 < nbins_1):
            if (i2_low_bin >= 0) and (i2_low_bin < nbins_2):
                hist_data[ i1_low_bin+1, i2_low_bin ] += w[i]*(1.-S1_low)*S2_low
            if (i2_low_bin+1 >= 0) and (i2_low_bin+1 < nbins_2):
                hist_data[ i1_low_bin+1, i2_low_bin+1 ] += w[i]*(1.-S1_low)*(1.-S2_low)


    return( hist_data )

@numba.njit
def histogram_cic_3d( q1, q2, q3, w, nbins_1, bins_start_1, bins_end_1,
        nbins_2, bins_start_2, bins_end_2, nbins_3, bins_start_3, bins_end_3 ):
    """
    Return an 2D histogram of the values in `q1` and `q2` weighted by `w`,
    consisting of `nbins_1` bins in the first dimension and `nbins_2` bins
    in the second dimension.
    Contribution to each bins is determined by the
    CIC weighting scheme (i.e. linear weights).
    """
    # Define various scalars
    bin_spacing_1 = (bins_end_1-bins_start_1)/nbins_1
    inv_spacing_1 = 1./bin_spacing_1
    bin_spacing_2 = (bins_end_2-bins_start_2)/nbins_2
    inv_spacing_2 = 1./bin_spacing_2
    bin_spacing_3 = (bins_end_3-bins_start_3)/nbins_3
    inv_spacing_3 = 1./bin_spacing_3
    n_ptcl = len(w)

    # Allocate array for histogrammed data
    hist_data = np.zeros( (nbins_1, nbins_2, nbins_3), dtype=np.float32 )

    # Go through particle array and bin the datae
    for i in range(n_ptcl):

        # Calculate the index of lower bin to which this particle contributes
        q1_cell = (q1[i] - bins_start_1) * inv_spacing_1
        q2_cell = (q2[i] - bins_start_2) * inv_spacing_2
        q3_cell = (q3[i] - bins_start_3) * inv_spacing_3
        i1_low_bin = int(math.floor( q1_cell ))
        i2_low_bin = int(math.floor( q2_cell ))
        i3_low_bin = int(math.floor( q3_cell ))

        # Calculate corresponding CIC shape and deposit the weight
        S1_low = 1. - (q1_cell - i1_low_bin)
        S2_low = 1. - (q2_cell - i2_low_bin)
        S3_low = 1. - (q3_cell - i3_low_bin)
        if (i1_low_bin >= 0) and (i1_low_bin < nbins_1):
            if (i2_low_bin >= 0) and (i2_low_bin < nbins_2):
                if (i3_low_bin >= 0) and (i3_low_bin < nbins_3):
                    hist_data[ i1_low_bin, i2_low_bin, i3_low_bin ] += w[i]*S1_low*S2_low*S3_low
                elif (i3_low_bin+1 >= 0) and (i3_low_bin+1 < nbins_3):
                    hist_data[ i1_low_bin, i2_low_bin, i3_low_bin ] += w[i]*S1_low*S2_low*(1.-S3_low)
            elif (i2_low_bin+1 >= 0) and (i2_low_bin+1 < nbins_2):
                if (i3_low_bin >= 0) and (i3_low_bin < nbins_3):
                    hist_data[ i1_low_bin, i2_low_bin, i3_low_bin ] += w[i]*S1_low*(1.-S2_low)*S3_low
                elif (i3_low_bin+1 >= 0) and (i3_low_bin+1 < nbins_3):
                    hist_data[ i1_low_bin, i2_low_bin, i3_low_bin ] += w[i]*S1_low*(1.-S2_low)*(1.-S3_low)
        elif (i1_low_bin+1 >= 0) and (i1_low_bin+1 < nbins_1):
            if (i2_low_bin >= 0) and (i2_low_bin < nbins_2):
                if (i3_low_bin >= 0) and (i3_low_bin < nbins_3):
                    hist_data[ i1_low_bin, i2_low_bin, i3_low_bin ] += w[i]*(1.-S1_low)*S2_low*S3_low
                elif (i3_low_bin+1 >= 0) and (i3_low_bin+1 < nbins_3):
                    hist_data[ i1_low_bin, i2_low_bin, i3_low_bin ] += w[i]*(1.-S1_low)*S2_low*(1.-S3_low)
            elif (i2_low_bin+1 >= 0) and (i2_low_bin+1 < nbins_2):
                if (i3_low_bin >= 0) and (i3_low_bin < nbins_3):
                    hist_data[ i1_low_bin, i2_low_bin, i3_low_bin ] += w[i]*(1.-S1_low)*(1.-S2_low)*S3_low
                elif (i3_low_bin+1 >= 0) and (i3_low_bin+1 < nbins_3):
                    hist_data[ i1_low_bin, i2_low_bin, i3_low_bin ] += w[i]*(1.-S1_low)*(1.-S2_low)*(1.-S3_low)


    return( hist_data )

@numba.njit
def velocity_2d( q1, q2, p1, p2, p3, w, nbins_1, bins_start_1, bins_end_1, nbins_2, bins_start_2, bins_end_2 ):

    bin_spacing_1 = (bins_end_1-bins_start_1)/nbins_1
    inv_spacing_1 = 1./bin_spacing_1
    bin_spacing_2 = (bins_end_2-bins_start_2)/nbins_2
    inv_spacing_2 = 1./bin_spacing_2
    n_ptcl = len(w)

    idx=2; idy=2

    hist_data = np.zeros((nbins_1, nbins_2), dtype=np.float64 )
    hist_data2 = np.zeros((nbins_1, nbins_2), dtype=np.float64 )
    for n in range(n_ptcl):
        # Calculate the index of lower bin to which this particle contributes
        q1_cell = (q1[n] - bins_start_1) * inv_spacing_1
        q2_cell = (q2[n] - bins_start_2) * inv_spacing_2
        i = int(math.floor( q1_cell ))
        j = int(math.floor( q2_cell ))

        gamprt = np.sqrt(1.+p1[n]**2+p2[n]**2+p3[n]**2)
        addprtx = p1[n]*w[n]/gamprt
        addprty = w[n]

        if i-idx > 0:
            lx1 = i-idx
        else:
            lx1 = 0
        if i+idx < nbins_1:
            lx2 = i+idx
        else:
            lx2 = nbins_1

        if j-idy > 0:
            ly1 = j-idy
        else:
            ly1 = 0
        if j+idy < nbins_2:
            ly2 = j+idy
        else:
            ly2 = nbins_2

        #lx1 = max([i-idx,0])
        #lx2 =min([i+idx,nbins_1])

        #ly1 = np.max([j-idy,0])
        #ly2 = np.min([j+idy,nbins_2])

        for j in range(ly1,ly2):
            for i in range(lx1,lx2):
                hist_data[i,j] = hist_data[i,j] + addprtx
                hist_data2[i,j] = hist_data2[i,j] + addprty

        #hist_data = hist_data/hist_data2
        ##hist_data[hist_data2 ==0] =0


    return( hist_data, hist_data2)


@numba.njit
def energy_2d( q1, q2, p1, p2, p3, w, nbins_1, bins_start_1, bins_end_1, nbins_2, bins_start_2, bins_end_2 ):

    bin_spacing_1 = (bins_end_1-bins_start_1)/nbins_1
    inv_spacing_1 = 1./bin_spacing_1
    bin_spacing_2 = (bins_end_2-bins_start_2)/nbins_2
    inv_spacing_2 = 1./bin_spacing_2
    n_ptcl = len(w)

    idx=2; idy=2

    hist_data = np.zeros((nbins_1, nbins_2), dtype=np.float64 )
    hist_data2 = np.zeros((nbins_1, nbins_2), dtype=np.float64 )
    for n in range(n_ptcl):
        # Calculate the index of lower bin to which this particle contributes
        q1_cell = (q1[n] - bins_start_1) * inv_spacing_1
        q2_cell = (q2[n] - bins_start_2) * inv_spacing_2
        i = int(math.floor( q1_cell ))
        j = int(math.floor( q2_cell ))

        gamprt = np.sqrt(1.+p1[n]**2+p2[n]**2+p3[n]**2)
        addprtx = (gamprt-1.)*w[n]
        addprty = w[n]

        if i-idx > 0:
            lx1 = i-idx
        else:
            lx1 = 0
        if i+idx < nbins_1:
            lx2 = i+idx
        else:
            lx2 = nbins_1

        if j-idy > 0:
            ly1 = j-idy
        else:
            ly1 = 0
        if j+idy < nbins_2:
            ly2 = j+idy
        else:
            ly2 = nbins_2

        #lx1 = max([i-idx,0])
        #lx2 =min([i+idx,nbins_1])

        #ly1 = np.max([j-idy,0])
        #ly2 = np.min([j+idy,nbins_2])

        for j in range(ly1,ly2):
            for i in range(lx1,lx2):
                hist_data[i,j] = hist_data[i,j] + addprtx
                hist_data2[i,j] = hist_data2[i,j] + addprty

        #hist_data = hist_data/hist_data2
        ##hist_data[hist_data2 ==0] =0


    return( hist_data, hist_data2)


@numba.njit
def velsqure_2d( q1, q2, p1, p2, p3, w, nbins_1, bins_start_1, bins_end_1, nbins_2, bins_start_2, bins_end_2 ):

    bin_spacing_1 = (bins_end_1-bins_start_1)/nbins_1
    inv_spacing_1 = 1./bin_spacing_1
    bin_spacing_2 = (bins_end_2-bins_start_2)/nbins_2
    inv_spacing_2 = 1./bin_spacing_2
    n_ptcl = len(w)

    idx=2; idy=2

    hist_data = np.zeros((nbins_1, nbins_2), dtype=np.float64 )
    hist_data2 = np.zeros((nbins_1, nbins_2), dtype=np.float64 )
    for n in range(n_ptcl):
        # Calculate the index of lower bin to which this particle contributes
        q1_cell = (q1[n] - bins_start_1) * inv_spacing_1
        q2_cell = (q2[n] - bins_start_2) * inv_spacing_2
        i = int(math.floor( q1_cell ))
        j = int(math.floor( q2_cell ))

        gamprt = np.sqrt(1.+p1[n]**2+p2[n]**2+p3[n]**2)
        addprtx = (p1[n]/gamprt)**2*w[n]
        addprty = w[n]

        if i-idx > 0:
            lx1 = i-idx
        else:
            lx1 = 0
        if i+idx < nbins_1:
            lx2 = i+idx
        else:
            lx2 = nbins_1

        if j-idy > 0:
            ly1 = j-idy
        else:
            ly1 = 0
        if j+idy < nbins_2:
            ly2 = j+idy
        else:
            ly2 = nbins_2

        #lx1 = max([i-idx,0])
        #lx2 =min([i+idx,nbins_1])

        #ly1 = np.max([j-idy,0])
        #ly2 = np.min([j+idy,nbins_2])

        for j in range(ly1,ly2):
            for i in range(lx1,lx2):
                hist_data[i,j] = hist_data[i,j] + addprtx
                hist_data2[i,j] = hist_data2[i,j] + addprty

        #hist_data = hist_data/hist_data2
        ##hist_data[hist_data2 ==0] =0


    return( hist_data, hist_data2)
