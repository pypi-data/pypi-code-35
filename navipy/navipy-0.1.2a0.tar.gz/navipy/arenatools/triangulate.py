"""
Function for triangulation of points projected on cameras
"""

import cv2
import numpy as np
from scipy.sparse.linalg import svds
from functools import partial


def emsvd(Y, k=None, tol=1E-3, maxiter=None):
    """
    Approximate SVD on data with missing values via expectation-maximization

    :param Y: (nobs, ndim) data matrix, missing values denoted by NaN/Inf
    :param k: number of singular values/vectors to find (default: k=ndim)
    :param tol: convergence tolerance on change in trace norm
    :param maxiter: maximum number of EM steps to perform (default: no limit)
    :returns: Y_hat, mu_hat, U, s, Vt
    Y_hat:      (nobs, ndim) reconstructed data matrix
    mu_hat:     (ndim,) estimated column means for reconstructed data
    U, s, Vt:   singular values and vectors (see np.linalg.svd and
                scipy.sparse.linalg.svds for details)

    Methods for large scale SVD with missing values
    Miklós Kurucz, András A. Benczúr, Károly Csalogány, 2007
    """

    if k is None:
        svdmethod = partial(np.linalg.svd, full_matrices=False)
    else:
        svdmethod = partial(svds, k=k)
    if maxiter is None:
        maxiter = np.inf

    # initialize the missing values to their respective column means
    mu_hat = np.nanmean(Y, axis=0, keepdims=1)
    valid = np.isfinite(Y)
    Y_hat = np.where(valid, Y, mu_hat)

    halt = False
    ii = 1
    v_prev = 0

    while not halt:

        # SVD on filled-in data
        U, s, Vt = svdmethod(Y_hat - mu_hat)

        # impute missing values
        Y_hat[~valid] = (U.dot(np.diag(s)).dot(Vt) + mu_hat)[~valid]

        # update bias parameter
        mu_hat = Y_hat.mean(axis=0, keepdims=1)

        # test convergence using relative change in trace norm
        v = s.sum()
        if ii >= maxiter or ((v - v_prev) / v_prev) < tol:
            halt = True
        ii += 1
        v_prev = v

    return Y_hat, mu_hat, U, s, Vt


def projects_points(pts_3d, cameras_calib):
    ncameras = len(cameras_calib)
    pts_cam = list()
    for cam_i in range(ncameras):
        cam_pose = cameras_calib[cam_i]['pose']
        cam_mat = cameras_calib[cam_i]['intrinsic_matrix']
        cam_dist = cameras_calib[cam_i]['distortion']
        rvec, jacobian = cv2.Rodrigues(cam_pose[:3, :3])
        tvec = cam_pose[:3, 3]
        impoints, jacobian = cv2.projectPoints(
            pts_3d, rvec, tvec, cam_mat, cam_dist)
        pts_cam.append(np.squeeze(impoints))
    pts_cam = np.array(pts_cam)
    return pts_cam


def random_projects_points(npoints, edge_length, cameras_calib):
    pts_3d = (np.random.rand(npoints, 3) - 0.5) * 2
    pts_3d[:, 2] += 1
    pts_3d[:, 2] *= edge_length
    pts_3d[:, 1] *= edge_length
    pts_3d[:, 0] *= edge_length

    pts_cam = projects_points(pts_3d, cameras_calib)
    return pts_cam, pts_3d


def undistord_ncam_points(cameras_calib, pts_cam):
    ncameras = len(cameras_calib)
    if np.shape(pts_cam)[0] != ncameras:
        raise IndexError(
            'Cameras points should have the same length than cameras_calib')
    if len(pts_cam.shape) == 2:
        pts_cam = pts_cam[:, np.newaxis, :]
    if len(pts_cam.shape) != 3:
        raise IndexError('Camera points should be of shape 3')
    for cam_i in range(ncameras):
        dst = cv2.undistortPoints(pts_cam[cam_i, ...][np.newaxis, ...],
                                  cameras_calib[cam_i]['intrinsic_matrix'],
                                  cameras_calib[cam_i]['distortion'])
        pts_cam[cam_i, ...] = np.squeeze(dst)

    return pts_cam


def triangulate_pair(cameras_calib, pts_cam, cam_indeces):
    """
    Triangulate two points on two cameras
    """
    cam_i = cam_indeces[0]
    cam_j = cam_indeces[1]
    point_4d_hom = cv2.triangulatePoints(cameras_calib[cam_i]['pose'][:3],
                                         cameras_calib[cam_j]['pose'][:3],
                                         pts_cam[cam_i][:, np.newaxis, :],
                                         pts_cam[cam_j][:, np.newaxis, :])

    point_4d = point_4d_hom / np.tile(point_4d_hom[-1, :], (4, 1))
    return point_4d[:3, :].T


def triangulate_multiview_single_pts(cameras_calib, pts_cam):
    """
    Methods for large scale SVD with missing values
    Miklós Kurucz, András A. Benczúr, Károly Csalogány, 2007
    """
    ncameras = len(cameras_calib)
    if len(pts_cam) != ncameras:
        raise IndexError(
            'Cameras points should have the same length than cameras_calib')
    # Undistord the camera point via the camera model
    pts_cam = np.squeeze(undistord_ncam_points(cameras_calib, pts_cam))
    #
    A = np.zeros((4, ncameras * 2))

    for cam_i in range(ncameras):
        pose = cameras_calib[cam_i]['pose'][:3]
        idx = 2 * cam_i
        A[:, idx: (idx + 2)] = \
            pts_cam[cam_i, :][np.newaxis, :] * pose[2, :][:, np.newaxis] -\
            pose[0:2].transpose()

    _, _, _, _, values = emsvd(A.transpose())
    X = values[-1, :]
    X = X / X[-1]
    point3d = X[:3]
    return point3d


def triangulate_multiview(cameras_calib, pts_cam):
    npoints = np.shape(pts_cam)[1]
    point3d = np.zeros((npoints, 3))
    for p_i in range(npoints):
        point3d[p_i, :] = triangulate_multiview_single_pts(
            cameras_calib, pts_cam[:, p_i, :])
    return point3d


def triangulate_ncam_pairwise(cameras_calib, pts_cam):
    ncameras = len(cameras_calib)
    if pts_cam.shape[0] != ncameras:
        msg = 'Cameras points should have the same '
        msg += 'length than cameras_calib {}!={}'.format(pts_cam.shape[0],
                                                         ncameras)
        raise IndexError(msg)
    # Undistord the camera point via the camera model
    pts_cam = undistord_ncam_points(cameras_calib, pts_cam)

    # Init variables
    n_points = pts_cam.shape[1]
    max_comb = int(ncameras * (ncameras - 1) / 2)
    point_3d = np.nan * np.zeros((max_comb, 3, n_points))
    nvalid_comb = np.zeros((1, n_points))
    comb_i = 0

    # Reconstruct pairwise (every combination)
    for cam_i in range(ncameras):
        for cam_j in range(cam_i + 1, ncameras):
            cpoint_3d = triangulate_pair(
                cameras_calib, pts_cam, [cam_i, cam_j])

            cvalid_id = np.any(np.isnan(cpoint_3d) != 1, axis=1)
            nvalid_comb[:, cvalid_id] += 1
            point_3d[comb_i, :, cvalid_id] = cpoint_3d[cvalid_id, :]
            comb_i += 1

    return ((np.nansum(point_3d, axis=0) / np.tile(nvalid_comb, (3, 1))).T,
            point_3d, nvalid_comb)
