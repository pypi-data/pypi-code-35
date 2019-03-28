import argparse
import pandas as pd
import numpy as np
import cv2
import os
from navipy.arenatools.cam_dlt import dlt_inverse
from navipy.arenatools.cam_dlt import dlt_compute_coeffs
from navipy.arenatools.cam_dlt import dlt_principal_point
from navipy.arenatools.cam_dlt import dlt_principal_distance
from navipy.arenatools.cam_dlt import dlt_scale_factors
from navipy.arenatools.cam_dlt import dlt_transformation_matrix


keybinding = dict()
keybinding['Quit without saving'] = 'q'
keybinding['Save and quite'] = 'e'
keybinding['Forward'] = 'f'
keybinding['Backward'] = 'b'
keybinding['Skip'] = 's'
keybinding['Calculate coeff'] = 'c'


def parser_dlt_calibrator():
    # Create command line options

    description = 'DLT calibrator provide a elementary user '
    description += 'interface to determine the dlt coeffs of '
    description += 'a camera from an image and calibration'
    description += '\n\n'
    description += 'Key bindings:\n'
    description += '-------------\n'
    for key, val in keybinding.items():
        description += '{} : {}\n'.format(val, key)
    parser = argparse.ArgumentParser(
        description=description,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    arghelp = 'Path to the calibration image'
    parser.add_argument('-i', '--image',
                        required=True,
                        help=arghelp)
    arghelp = 'Path to the csv files containing calibration points'
    parser.add_argument('-p', '--points',
                        required=True,
                        help=arghelp)
    arghelp = 'Scaling of the image'
    parser.add_argument('-s', '--scale',
                        default=0.5,
                        help=arghelp)
    arghelp = 'number of dlt parameters (coeff)'
    parser.add_argument('-c', '--ndltcoeff',
                        type=int,
                        default=11,
                        help=arghelp)
    arghelp = 'number of iteration for calibration'
    parser.add_argument('-e', '--epoque',
                        type=int,
                        default=100,
                        help=arghelp)
    return parser


def click(event, x, y, flags, param):
    # grab references to the global variables
    global campts, index_i, scale
    # if the left mouse button was clicked, record the starting
    # (x, y) coordinates and indicate that cropping is being
    # performed
    if event == cv2.EVENT_LBUTTONDOWN:
        campts.loc[index_i, ['u', 'v']] = [x/scale, y/scale]


def main():
    # Fetch arguments
    args = vars(parser_dlt_calibrator().parse_args())
    # Load the u,v points if any, otherwise
    # set all u,v for each frame to nan, because
    # we do not know the position of x,y,z points on cam
    frames = pd.read_csv(args['points'])
    if ('u' in frames.columns) and ('v' in frames.columns):
        campts = frames.loc[:, ['u', 'v']]
        frames = frames.drop('u', axis=1)
        frames = frames.drop('v', axis=1)
    else:
        campts = pd.DataFrame(index=frames.index, columns=['u', 'v'])
    # The image may need to be scale because screen may have
    # less pixel than the image
    scale = args['scale']
    ndlt_coeff = args['ndltcoeff']
    niter = args['epoque']
    imageref = cv2.imread(args['image'])
    # define some constants
    showframe_ref = 50
    showframe = showframe_ref
    font = cv2.FONT_HERSHEY_SIMPLEX
    coeff = None

    # create an image window
    cv2.namedWindow("image")
    cv2.setMouseCallback("image", click)
    # Loop until users quit
    idx = 0  # User will control it during the loop
    while True:
        # Make sure the idx do not go outof bound
        idx = np.clip(idx, 0, frames.shape[0]-1)
        # load image
        index_i = frames.index[idx]
        mimage = imageref.copy()
        # Display stuff at given time
        if showframe > 0:
            cv2.putText(mimage, str(index_i), (50, 50),
                        font, 2, (0, 0, 255), 3, cv2.LINE_AA)
            showframe -= 1
        for nbi, row in campts.dropna().iterrows():
            cv2.circle(mimage, (row.u.astype(int), row.v.astype(int)),
                       5, (0, 0, 255), 1)
            cv2.putText(mimage, str(nbi),
                        (row.u.astype(int), row.v.astype(int)),
                        font, 1, (0, 0, 255), 2, cv2.LINE_AA)
        if coeff is not None:
            matrix_uv = dlt_inverse(coeff, frames)
            # print(matrix_uv)
            matrix_uv = pd.DataFrame(data=matrix_uv,
                                     index=frames.index,
                                     columns=['u', 'v'])
            matrix_uv[matrix_uv < 0] = np.nan
            matrix_uv[matrix_uv.u > mimage.shape[0]] = np.nan
            matrix_uv[matrix_uv.v > mimage.shape[1]] = np.nan
            for nbi, row in matrix_uv.dropna().iterrows():
                cv2.circle(mimage, (row.u.astype(int), row.v.astype(int)),
                           5, (0, 255, 0), 1)
                cv2.putText(mimage, str(nbi),
                            (row.u.astype(int), row.v.astype(int)),
                            font, 1, (0, 255, 0), 2, cv2.LINE_AA)
        mimage = cv2.resize(mimage, (0, 0), fx=scale, fy=scale)
        cv2.imshow("image", mimage)
        # Wait for keys
        key = cv2.waitKey(20) & 0xFF  # 20ms
        # Key binding
        if key == ord("q"):
            print('quit without saving')
            break
        if key == ord("f"):
            # forward
            showframe = showframe_ref
            idx += 1
        if key == ord("s"):
            # skip
            showframe = showframe_ref
            campts.loc[index_i, :] = np.nan
            idx += 1
        if key == ord("b"):
            # backward
            showframe = showframe_ref
            idx -= 1
        if key == ord("e"):
            print('save and quit')
            frames['u'] = campts.u
            frames['v'] = campts.v
            frames.to_csv(args['points'])
            break
        if key == ord("c"):
            print('calibrate')
            coeff, rmse = dlt_compute_coeffs(
                frames, campts, nparams=ndlt_coeff,
                niter=niter)
            print(rmse)
            print(coeff)
            print('principal points: {}'.format(dlt_principal_point(coeff)))
            print('principal distance: {}'.format(
                dlt_principal_distance(coeff)))
            print('scale factor: {}'.format(dlt_scale_factors(coeff)))
            print('transform:')
            print(dlt_transformation_matrix(coeff))
            coeff = pd.Series(data=coeff)
            coeff.to_csv(os.path.splitext(args['points'])[0]+'_coeff.csv')

    # close all open windows
    cv2.destroyAllWindows()
    print('End')


if __name__ == "__main__":
    # execute only if run as a script
    main()
