import pandas as pd
import numpy as np


def dlt_reconstruct(coeff, campts, z=None):
    """
    This function reconstructs the 3D position of a coordinate based on a set
    of DLT coefficients and [u,v] pixel coordinates from 2 or more cameras

   :param coeff: - 11 DLT coefficients for all n cameras, [11,n] array
   :param campts: - [u,v] pixel coordinates from all n cameras over f frames
   :param z: the z coordinate of all points for reconstruction \
from a single camera
   :returns: xyz - the xyz location in each frame, an [f,3] array\
rmse - the root mean square error for each xyz point, and [f,1] array,\
units are [u,v] i.e. camera coordinates or pixels
    """
    # number of cameras
    ncams = campts.columns.levels[0].shape[0]
    if (ncams == 1) and (z is None):
        raise NameError('reconstruction from a single camera require z')

    # setup output variables
    xyz = pd.DataFrame(index=campts.index, columns=[
                       'x', 'y', 'z'], dtype=float)
    rmse = pd.Series(index=campts.index)
    # process each frame
    for ii, frame_i in enumerate(campts.index):
        # get a list of cameras with non-NaN [u,v]
        row = campts.loc[frame_i, :].unstack()
        validcam = row.dropna(how='any')
        cdx = validcam.index
        if validcam.shape[0] >= 2:
            # Two or more cameras
            u = campts.loc[frame_i, cdx].swaplevel().u
            v = campts.loc[frame_i, cdx].swaplevel().v

            # initialize least-square solution matrices
            m1 = np.zeros((cdx.shape[0]*2, 3))
            m2 = np.zeros((cdx.shape[0]*2, 1))

            m1[0: cdx.size*2: 2, 0] = u*coeff.loc[8, cdx]-coeff.loc[0, cdx]
            m1[0: cdx.size*2: 2, 1] = u*coeff.loc[9, cdx]-coeff.loc[1, cdx]
            m1[0: cdx.size*2: 2, 2] = u*coeff.loc[10, cdx]-coeff.loc[2, cdx]
            m1[1: cdx.size*2: 2, 0] = v*coeff.loc[8, cdx]-coeff.loc[4, cdx]
            m1[1: cdx.size*2: 2, 1] = v*coeff.loc[9, cdx]-coeff.loc[5, cdx]
            m1[1: cdx.size*2: 2, 2] = v*coeff.loc[10, cdx]-coeff.loc[6, cdx]
            m2[0: cdx.size*2: 2, 0] = coeff.loc[3, cdx]-u
            m2[1: cdx.size*2: 2, 0] = coeff.loc[7, cdx]-v

            # get the least squares solution to the reconstruction
            xyz.loc[frame_i, ['x', 'y', 'z']] = \
                np.linalg.lstsq(m1, m2, rcond=None)[0][:, 0]

            # compute ideal [u,v] for each camera
            uv = m1.dot(xyz.loc[frame_i, ['x', 'y', 'z']].transpose())
            uv = uv[:, np.newaxis]  # because m2 has size n,1
            # compute the number of degrees of freedom in the reconstruction
            dof = m2.size-3

            # estimate the root mean square reconstruction error
            rmse.loc[frame_i] = (np.sum((m2-uv) ** 2)/dof) ** 0.5

        elif (validcam.shape[0] == 1) and (z is not None):
            # http://www.kwon3d.com/theory/dlt/dlt.html
            # equation 19 with z = constant
            # the term with z can be move to right side
            # then equation 21 can be solved as follow:
            u = campts.loc[frame_i, cdx].unstack().u
            v = campts.loc[frame_i, cdx].unstack().v

            # initialize least-square solution matrices
            m1 = np.zeros((cdx.shape[0]*2, 2))
            m2 = np.zeros((cdx.shape[0]*2, 1))

            m1[0: cdx.size*2: 2, 0] = u*coeff.loc[8, cdx]-coeff.loc[0, cdx]
            m1[0: cdx.size*2: 2, 1] = u*coeff.loc[9, cdx]-coeff.loc[1, cdx]
            m1[1: cdx.size*2: 2, 0] = v*coeff.loc[8, cdx]-coeff.loc[4, cdx]
            m1[1: cdx.size*2: 2, 1] = v*coeff.loc[9, cdx]-coeff.loc[5, cdx]
            m2[0: cdx.size*2: 2, 0] = coeff.loc[3, cdx]-u
            m2[1: cdx.size*2: 2, 0] = coeff.loc[7, cdx]-v

            m2[0: cdx.size*2: 2, 0] -= \
                (u*coeff.loc[10, cdx] - coeff.loc[2, cdx])*z.loc[frame_i]
            m2[1: cdx.size*2: 2, 0] -= \
                (v*coeff.loc[10, cdx] - coeff.loc[6, cdx])*z.loc[frame_i]

            # get the least squares solution to the reconstruction
            xyz.loc[frame_i, ['x', 'y']] = \
                np.squeeze(np.linalg.lstsq(m1, m2, rcond=None)[0])
            xyz.loc[frame_i, 'z'] = z.loc[frame_i]

            # compute ideal [u,v] for each camera
            uv = m1.dot(xyz.loc[frame_i, ['x', 'y']].transpose())
            uv = uv[:, np.newaxis]  # because m2 has size n,1
            # compute the number of degrees of freedom in the reconstruction
            dof = m2.size-3

            # estimate the root mean square reconstruction error
            rmse.loc[frame_i] = (np.sum((m2-uv) ** 2)/dof) ** 0.5
    return xyz, rmse


def dlt_principal_point(coeff):
    normalisation = np.sum(coeff[8:11]**2)
    u_0 = np.sum(coeff[0:3]*coeff[8:11])/normalisation
    v_0 = np.sum(coeff[4:7]*coeff[8:11])/normalisation
    return u_0, v_0


def dlt_principal_distance(coeff):
    normalisation = np.sum(coeff[8:11]**2)
    return 1/np.sqrt(normalisation)


def dlt_scale_factors(coeff):
    u_0, v_0 = dlt_principal_point(coeff)

    normalisation = np.sum(coeff[8:11]**2)
    du = (u_0*coeff[8] - coeff[0])**2
    du += (u_0*coeff[9] - coeff[1])**2
    du += (u_0*coeff[10] - coeff[2])**2
    du /= normalisation

    dv = (v_0*coeff[8] - coeff[4])**2
    dv += (v_0*coeff[9] - coeff[5])**2
    dv += (v_0*coeff[10] - coeff[6])**2
    dv /= normalisation
    return du, dv


def dlt_transformation_matrix(coeff):
    u_0, v_0 = dlt_principal_point(coeff)
    d = dlt_principal_distance(coeff)
    du, dv = dlt_scale_factors(coeff)
    transform = np.zeros((3, 3))
    transform[0, 0] = (u_0*coeff[8]-coeff[0])/du
    transform[0, 1] = (u_0*coeff[9]-coeff[1])/du
    transform[0, 2] = (u_0*coeff[10]-coeff[2])/du

    transform[1, 0] = (v_0*coeff[8]-coeff[4])/dv
    transform[1, 1] = (v_0*coeff[9]-coeff[5])/dv
    transform[1, 2] = (v_0*coeff[10]-coeff[6])/dv

    transform[2, 0] = coeff[8]
    transform[2, 1] = coeff[9]
    transform[2, 2] = coeff[10]
    return d*transform


def dlt_position(coeff):
    #
    # From Eq 25
    # http://www.kwon3d.com/theory/dlt/dlt.html
    #
    vect = np.array([[-coeff[3], -coeff[7], -1]]).transpose()
    mat = np.array([[coeff[0], coeff[1], coeff[2]],
                    [coeff[4], coeff[5], coeff[6]],
                    [coeff[8], coeff[9], coeff[10]]])
    return np.linalg.inv(mat).dot(vect)


def dlt_inverse(coeff, frames):
    """
    This function reconstructs the pixel coordinates of a 3D coordinate as
    seen by the camera specificed by DLT coefficients c

   :param coeff: - 11 DLT coefficients for the camera, [11,1] array
   :param frames: - [x,y,z] coordinates over f frames,[f,3] array
   :returns: uv - pixel coordinates in each frame, [f,2] array
    """
    # write the matrix solution out longhand for vector operation over
    # all pointsat once
    uv = np.zeros((frames.shape[0], 2))
    frames = frames.loc[:, ['x', 'y', 'z']].values

    normalisation = frames[:, 0]*coeff[8] + \
        frames[:, 1]*coeff[9]+frames[:, 2]*coeff[10] + 1
    uv[:, 0] = frames[:, 0]*coeff[0]+frames[:, 1] * \
        coeff[1]+frames[:, 2]*coeff[2]+coeff[3]
    uv[:, 1] = frames[:, 0]*coeff[4]+frames[:, 1] * \
        coeff[5]+frames[:, 2]*coeff[6]+coeff[7]
    uv[:, 0] /= normalisation
    uv[:, 1] /= normalisation
    # Apply distortion
    delta_uv = np.zeros((frames.shape[0], 2))
    u_0, v_0 = dlt_principal_point(coeff)
    zeta = uv[:, 0] - u_0
    eta = uv[:, 1] - v_0
    rsq = zeta**2 + eta**2
    if coeff.shape[0] > 11:
        delta_uv[:, 0] += zeta*(coeff[11]*rsq)
        delta_uv[:, 1] += eta*(coeff[11]*rsq)
    if coeff.shape[0] > 13:
        delta_uv[:, 0] += zeta*(coeff[12]*(rsq**2) + coeff[13]*(rsq**3))
        delta_uv[:, 1] += eta*(coeff[12]*(rsq**2) + coeff[13]*(rsq**3))
    if coeff.shape[0] > 15:
        delta_uv[:, 0] += coeff[14]*(rsq + 2*(zeta**2)) + coeff[15]*eta*zeta
        delta_uv[:, 1] += coeff[15]*(rsq + 2*(eta**2)) + coeff[14]*eta*zeta
    # print(eta, zeta, rsq)
    uv += delta_uv
    return uv


def _dlt_matrices_calib(vframes, vcampts, nparams=11, l1to11=np.zeros(11)):
    # re arange the frame matrix to facilitate the linear least
    # sqaures solution
    if nparams < 11:
        nparams = 11
    matrix = np.zeros((vframes.shape[0]*2, 16))  # 16 for the dlt
    u_0, v_0 = dlt_principal_point(l1to11)
    for num_i, index_i in enumerate(vframes.index):
        # eta, zeta, Rsq depends on L9to11
        zeta = vcampts.loc[index_i, 'u'] - u_0  # -u_0 = 0 ??
        eta = vcampts.loc[index_i, 'v'] - v_0  # -v_0 = 0
        R = np.sum(l1to11[-3:] * vframes.loc[index_i, ['x', 'y', 'z']])+1
        rsq = eta**2 + zeta**2
        # populate matrix
        matrix[2*num_i, 0:3] = vframes.loc[index_i, ['x', 'y', 'z']]
        matrix[2*num_i+1, 4:7] = vframes.loc[index_i, ['x', 'y', 'z']]
        matrix[2*num_i, 3] = 1
        matrix[2*num_i+1, 7] = 1
        matrix[2*num_i, 8:11] = vframes.loc[index_i,
                                            ['x', 'y', 'z']]*(-vcampts.loc[index_i, 'u'])
        matrix[2*num_i+1, 8: 11] = vframes.loc[index_i,
                                               ['x', 'y', 'z']]*(-vcampts.loc[index_i, 'v'])
        # 12th parameter
        matrix[2*num_i, 11] = zeta*rsq*R
        matrix[2*num_i+1, 11] = eta*rsq*R
        # 13th and 14th parameters
        matrix[2*num_i, 12] = zeta*(rsq**2)*R
        matrix[2*num_i+1, 12] = eta*(rsq**2)*R
        matrix[2*num_i, 13] = zeta*(rsq**3)*R
        matrix[2*num_i+1, 13] = eta*(rsq**3)*R
        # 15th and 16th parameters
        matrix[2*num_i, 12] = (rsq + 2*(zeta**2))*R
        matrix[2*num_i+1, 12] = eta*zeta*R
        matrix[2*num_i, 13] = eta*zeta*R
        matrix[2*num_i+1, 13] = (rsq + 2*(eta**2))*R

        matrix[2*num_i, :] /= R
        matrix[2*num_i+1, :] /= R
    return matrix[:, : nparams]


def dlt_compute_coeffs(frames, campts, nparams=11, niter=100):
    """
    A basic implementation of 11 parameters DLT

    : param frames: an array of x, y, z calibration point coordinates
    : param campts: an array of u, v pixel coordinates from the camera
    : returns: dlt coefficients and root mean square error

    Notes: frame and camera points must have the same number of rows and at \
least contains six rows. Also the frame points must not all lie within a \
single plane.
    """

    # remove NaNs
    valid_idx = frames.dropna(how='any').index
    valid_idx = campts.loc[valid_idx, :].dropna(how='any').index
    # valid df
    vframes = frames.loc[valid_idx, :]
    vcampts = campts.loc[valid_idx, :]
    # Get the matrices for calib
    matrix = _dlt_matrices_calib(vframes, vcampts)
    vcampts_f = vcampts.values.flatten()  # [u_1, v_1, ... u_n, v_n]
    # get the linear solution the 11 parameters
    coeff = np.linalg.lstsq(matrix, vcampts_f, rcond=None)[0]
    # compute the position of the frame in u,v coordinates given the linear
    # solution from the previous line
    matrix_uv = dlt_inverse(coeff, vframes)
    # compute the rmse between the ideal frame u,v and the
    # recorded frame u,v
    rmse = np.sqrt(np.mean(np.sum((matrix_uv-vcampts)**2)))
    if nparams == 11:
        return coeff, rmse
    # Now we can try to guess the other coefficients
    if nparams in [12, 14, 16]:
        for _ in range(niter):
            # 9th to 11th parameters are index 8 to 10 (0 being the 1st param)
            l1to11 = coeff[: 11]
            # Get the matrices for calib
            matrix = _dlt_matrices_calib(vframes, vcampts,
                                         nparams=nparams, l1to11=l1to11)
            vcampts_normed = vcampts_f.copy()
            for num_i, index_i in enumerate(vframes.index):
                normalisation = np.sum(
                    l1to11[-3:] * vframes.loc[index_i, ['x', 'y', 'z']])+1
                vcampts_normed[2*num_i] /= normalisation
                vcampts_normed[2*num_i + 1] /= normalisation
            coeff = np.linalg.lstsq(matrix, vcampts_normed, rcond=None)[0]
            print(coeff)
        # compute the position of the frame in u,v coordinates given the linear
        # solution from the previous line
        matrix_uv = dlt_inverse(coeff, vframes)
        # compute the rmse between the ideal frame u,v and the
        # recorded frame u,v
        rmse = np.sqrt(np.mean(np.sum((matrix_uv-vcampts)**2)))
        return coeff, rmse
    else:
        raise ValueError('nparams can be either [11,12,14,16]')
