""" axishell module
to creat axy symmetric shells for scientific computations
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import json

import numpy as np
from scipy import interpolate, spatial

MESH_CTRL_POINTS = "axishell.json"
MAX_SPLINE_ORDER = 3
SPLINE_SMOOTHNESS = 0

MATRIX_ELEMENTS = ["xyz", "r", "theta",
                   "n_x", "n_y", "n_z", "n_r"]

AXIS_NAMES = ['time', 'theta', 'r']


class AxiShell():
    """ base clase for axysymmetric computationnal shells"""

    def __init__(self, n_longi, n_azi):
        """ startup method"""

        self.shape = (n_azi, n_longi)
        # dict for the definition of the shell
        self.geom = {}

        # numpy array for the node based geometric elements
        self.matrix = {}

        self.cake = {}

        # a matrix registering different width curvilinear based.
        self.matrix_widths = {}

    def init_mockup(self):
        """ initialize with a mockup mesh"""
        self.geom["angle"] = 40.0

        # by nodes trapvtx
        self.geom["crtl_pts_x"] = (0.0,
                                   0.2)
        self.geom["crtl_pts_r"] = (0.12,
                                   0.12)

        # # sphere
        # self.geom["crtl_pts_x"] = 0.1 + 0.1* np.sin(
        #     np.linspace(-np.pi*0.5, np.pi*0.5, 4))
        # self.geom["crtl_pts_r"] = 0.1*np.cos(
        #     np.linspace(-np.pi*0.5, np.pi*0.5, 4))

        # by nodes curved shape
        # self.geom["crtl_pts_x"] = (0.0,
        #                            0.1,
        #                            0.2,
        #                            0.15)
        # self.geom["crtl_pts_r"] = (0.1,
        #                            0.15,
        #                            0.1,
        #                            0.03)

        self.build_shell()

    def load(self):
        """ load axishell from json"""
        with open(MESH_CTRL_POINTS, "w") as fin:
            self.geom = json.load(fin)

        self.build_shell()

    def dump(self):
        """ dump axishell from json"""
        with open(MESH_CTRL_POINTS, "w") as fout:
            json.dump(self.geom, fout)

    def build_shell(self):
        """ build shell from geometry """

        # Build crest
        spline_order = min(len(self.geom["crtl_pts_x"]) - 1, MAX_SPLINE_ORDER)
        tck, _ = interpolate.splprep([self.geom["crtl_pts_x"],
                                      self.geom["crtl_pts_r"]],
                                     s=SPLINE_SMOOTHNESS,
                                     k=spline_order)
        unew = np.linspace(0,
                           1,
                           num=self.shape[1])
        shell_crest = np.asarray(interpolate.splev(unew, tck))

        normal_vects = np.roll(np.diff(shell_crest), 1, axis=0)
        normal_vects /= np.linalg.norm(normal_vects, axis=0)
        normal_vects[0, :] *= -1
        normal_vects2 = np.ones((2, self.shape[1]))
        normal_vects2[:, :self.shape[1] - 1] = normal_vects
        normal_vects2[:, -1] = normal_vects[:, -1]

        for item in MATRIX_ELEMENTS:
            self.matrix[item] = np.ones(self.shape)

        tmp_x = np.tile(shell_crest[0], (self.shape[0], 1))
        self.matrix["r"] = np.tile(shell_crest[1], (self.shape[0], 1))
        self.matrix["n_x"] = np.tile(normal_vects2[0], (self.shape[0], 1))
        self.matrix["n_r"] = np.tile(normal_vects2[1], (self.shape[0], 1))
        self.matrix["theta"] = np.transpose(
            np.tile(np.linspace(-0.5 * self.geom["angle"] * np.pi / 180,
                                0.5 * self.geom["angle"] * np.pi / 180,
                                num=self.shape[0]),
                    (self.shape[1], 1)))

        tmp_y = (self.matrix["r"] * np.cos(self.matrix["theta"]))
        tmp_z = (self.matrix["r"] * np.sin(self.matrix["theta"]))

        self.matrix["xyz"] = np.stack((tmp_x, tmp_y, tmp_z),
                                      axis=2)

        self.matrix["n_y"] = (self.matrix["n_r"]
                              * np.cos(self.matrix["theta"]))
        self.matrix["n_z"] = (self.matrix["n_r"]
                              * np.sin(self.matrix["theta"]))

    def width_mockup(self):
        """ create a mockup tuple of tuple for widths"""

        width_mockup = ((0.0, -0.04),
                        (0.2, -0.04),
                        (0.3, -0.07),
                        (0.4, -0.07),
                        (0.5, -0.04),
                        (0.8, -0.04))

        return width_mockup

    def add_curviwidth(self, title, data):
        """ add a curvilinear with fiel to shell """

        (x_tuple, y_tuple) = tuple(zip(*data))

        # extend bounds
        xlist = [0] + list(x_tuple) + [1]
        ylist = [y_tuple[0]] + list(y_tuple) + [y_tuple[-1]]
        f_int = interpolate.interp1d(xlist, ylist)
        xnew = np.linspace(0, 1, num=self.shape[1])
        ynew = f_int(xnew)

        self.matrix[title] = np.tile(ynew, (self.shape[0], 1))

    def set_mask_on_shell(self, cloud, tol):
        """ create a mask on the shell from a cloud
        """
        kdtree = spatial.KDTree(cloud)
        dists, _ = kdtree.query(self.matrix["xyz"], k=1)
        self.matrix["mask"] = np.where(
            dists.reshape(self.shape) > tol,
            np.zeros(self.shape),
            np.ones(self.shape))

    def bake_millefeuille(self, mwidth, n_layers, shift=0):
        """Create a milefeuille.

        extruding a shell
        in the normal direction
        scaled by matrix 'mwidth'
        on 'nlayers"
        shift : additionall depth
        "Bon appetit!"
        """
        cake = {}
        cake["xyz"] = np.empty((self.shape[0],
                                self.shape[1],
                                n_layers,
                                3))
        cake["dz"] = np.empty((self.shape[0],
                               self.shape[1],
                               n_layers))

        for j, dim in enumerate(["x", "y", "z"]):
            for i in range(n_layers):
                cake["xyz"][:, :, i, j] = (self.matrix["xyz"][:, :, j]
                                           + (1.0 * i / n_layers
                                              * self.matrix[mwidth] +
                                              shift)
                                           * self.matrix["n_" + dim])

        for i in range(n_layers):
            cake["dz"][:, :, i] = abs(self.matrix[mwidth] / n_layers)
        cake["dz"][:, :, 0] /= 2
        cake["dz"][:, :, -1] /= 2
        return cake


    def average_on_shell_over_dirs(self, variable, directions):
        """Performs an integration (averaging) over one or
            multiple directions : time, theta and r


            Parameters:
            ==========
            variable  : the array to be averaged of shape
                        (n_time, n_theta, n_r)
            directions : list of directions on which average is
                         to be performed should contain keywords from
                         ['time','theta', 'r']

            Returns:
            =======
            averaged_variable : integrated(averaged) array on the given
                                directions
        """

        scaled = np.copy(variable)
        if self.matrix.get("surf") is not None:
            scaled = np.multiply(variable, self.matrix.get("surf"))

        dirs = AXIS_NAMES.copy()
        cond = directions and len(directions) <= 3
        cond = cond and all(d in dirs for d in directions)
        if not cond:
            mess = 'Averaging directions do not conform to criteria\n'
            mess = mess +'It should be a list containing one of or all items\n'
            mess = mess +'"time", "theta", "r"'
            raise ValueError(mess)
        else:
            averaged_variable = scaled
            for dir_ in directions:
                index = dirs.index(dir_)
                averaged_variable = np.mean(averaged_variable, axis=index)
                dirs.pop(index)
        return averaged_variable
