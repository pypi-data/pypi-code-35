import navipy.arenatools.cam_dlt as dlt
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# from mpl_toolkits.mplot3d import Axes3D

# Calibration
csvfile = '../resources/sample_experiment/Bertrand_2019/20180910_1500_refined_calib.csv'
calib = pd.read_csv(csvfile, index_col=0)

# trajectory
trajfile = '../resources/sample_experiment/Bertrand_2019/20180910_1555_bee11b_Trial04L.csv'
traj = pd.read_csv(trajfile, index_col=0)
print(traj.head())

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.plot(traj.x, traj.y, traj.z)

for cam, coeff in calib.transpose().iterrows():
    coeff_val = coeff.values
    u_0, v_0 = dlt.dlt_principal_point(coeff_val)
    d = dlt.dlt_principal_distance(coeff_val)
    du, dv = dlt.dlt_scale_factors(coeff_val)
    mat = dlt.dlt_transformation_matrix(coeff_val)
    x, y, z = dlt.dlt_position(coeff_val)
    print('Camera: ', cam)
    print('Principal point:', u_0, v_0)
    print('Principal distance:', d)
    print('Scale factors:', du, dv)
    print('Transformation matrix:')
    print(mat)
    print('Camera position:', x, y, z)

    s = 100
    x_cam = mat.dot([1, 0, 0])
    y_cam = mat.dot([0, 1, 0])
    z_cam = mat.dot([0, 0, 1])
    print(x_cam, y_cam, z_cam)
    ax.plot(x, y, z, 'ko')
    for cam_axis, col in zip([x_cam, y_cam, z_cam], ['r', 'g', 'b']):
        cam_axis *= s/np.linalg.norm(cam_axis)
        ax.plot([x[0], x[0]+cam_axis[0]],
                [y[0], y[0]+cam_axis[1]],
                [z[0], z[0]+cam_axis[2]], '-', color=col)

plt.show()
