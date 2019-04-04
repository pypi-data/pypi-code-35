""" Module to test the heat transfer
resolution on grids curvilinear 2D grids """

from __future__ import absolute_import, division
import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as sciopt
import scipy.sparse as scp
from arnica.utils.nparray2xmf import NpArray2Xmf


class Metrics(object):
    """ metrics class """

    def __init__(self, x_coor, y_coor):
        """ startup class
        x_coor : numpy array (n,m) , x_coordinates
        y_coor : numpy array (n,m) , y_coordinates
        """
        self.x_coor = x_coor
        self.y_coor = y_coor

        self.size_i, self.size_j = x_coor.shape

        self.shp2d = x_coor.shape
        self.shp1d = x_coor.ravel().shape

        self.order = 2
        self.periodic_xi = False
        self.periodic_eta = False
        self._compute_metric()
        # self._compute_matrixes()
        self._compute_matrixes_csr()

    def _compute_metric(self):
        """ compute the metric elements """
        diff_x_xi = self.diff_xi2(self.x_coor)
        diff_x_eta = self.diff_eta2(self.x_coor)
        diff_y_xi = self.diff_xi2(self.y_coor)
        diff_y_eta = self.diff_eta2(self.y_coor)
        inv_det_j = np.reciprocal(diff_x_xi*diff_y_eta
                                  - diff_x_eta*diff_y_xi)

        self.jacob_x_xi = inv_det_j*diff_x_xi
        self.jacob_x_eta = inv_det_j*diff_x_eta
        self.jacob_y_xi = inv_det_j*diff_y_xi
        self.jacob_y_eta = inv_det_j*diff_y_eta

    # def _compute_matrixes(self):
    #     """ compute the matrix form of operatoirs """
    #     size = self.size_i * self.size_j
    #     self.mat_gx = np.zeros((size, size))
    #     self.mat_gy = np.zeros((size, size))

    #     def ijc(i, j):
    #         """ Give indexes in 1D version """
    #         return j + self.size_j*i

    #     def iters(k, size_k, perio, order=1):
    #         """Provide terators , taking boundaries into account """
    #         if self.order == 1:
    #             cfk = 1.
    #             km1 = int(k)
    #             kp1 = k+1
    #             if k == size_k-1:
    #                 if perio:
    #                     kp1 = 0
    #                 else:
    #                     km1 = size_k-2
    #                     kp1 = size_k-1

    #         if self.order == 2:
    #             cfk = 0.5
    #             km1 = k-1
    #             kp1 = k+1
    #             if k == 0:
    #                 if perio:
    #                     km1 = size_k-1
    #                 else:
    #                     cfk = 1.
    #                     km1 = 0

    #             if k == size_k-1:
    #                 if perio:
    #                     kp1 = 0
    #                 else:
    #                     cfk = 1.
    #                     kp1 = size_k-1

    #         return km1, kp1, cfk

    #     for i in range(self.size_i):
    #         im1, ip1, cfi = iters(i, self.size_i, self.periodic_eta)
    #         for j in range(self.size_j):
    #             jm1, jp1, cfj = iters(j, self.size_j, self.periodic_xi)
    #             self.mat_gx[ijc(i, j), ijc(i, jp1)] += cfj*self.jacob_y_eta[i, j]
    #             self.mat_gx[ijc(i, j), ijc(i, jm1)] += -cfj*self.jacob_y_eta[i, j]
    #             self.mat_gx[ijc(i, j), ijc(ip1, j)] += -cfi*self.jacob_y_xi[i, j]
    #             self.mat_gx[ijc(i, j), ijc(im1, j)] += +cfi*self.jacob_y_xi[i, j]

    #             self.mat_gy[ijc(i, j), ijc(ip1, j)] += cfi*self.jacob_x_xi[i, j]
    #             self.mat_gy[ijc(i, j), ijc(im1, j)] += -cfi*self.jacob_x_xi[i, j]
    #             self.mat_gy[ijc(i, j), ijc(i, jp1)] += -cfj*self.jacob_x_eta[i, j]
    #             self.mat_gy[ijc(i, j), ijc(i, jm1)] += +cfj*self.jacob_x_eta[i, j]

    #     self.matlap = np.dot(self.mat_gx, self.mat_gx) + np.dot(self.mat_gy, self.mat_gy)

    def _compute_matrixes_csr(self):
        """ compute the matrix form of operators """
        size = self.size_i * self.size_j
        self.mat_gx = np.zeros((size, size))
        self.mat_gy = np.zeros((size, size))

        # Option 1
        ijc_array = np.arange(self.size_i * self.size_j)
        iters_i = np.repeat(np.arange(self.size_i), self.size_j)
        iters_j = np.tile(np.arange(self.size_j), self.size_i)
        ip1 = np.arange(1, self.size_i + 1)
        jp1 = np.arange(1, self.size_j + 1)
        im1 = np.arange(-1, self.size_i - 1)
        jm1 = np.arange(-1, self.size_j - 1)

        cfi_sb = np.ones(self.size_i) * 0.5
        cfj_sb = np.ones(self.size_j) * 0.5
        if self.periodic_xi:
            im1[0], ip1[-1] = self.size_i - 1, 0
        else:
            im1[0], ip1[-1] = 0, self.size_i - 1
            cfi_sb[0], cfi_sb[-1] = 1., 1.

        if self.periodic_eta:
            jm1[0], jp1[-1] = self.size_j - 1, 0
        else:
            jm1[0], jp1[-1] = 0, self.size_j - 1
            cfj_sb[0], cfj_sb[-1] = 1., 1.

        cfi = np.repeat(cfi_sb, self.size_j)
        cfj = np.tile(cfj_sb, self.size_i)

        iters_ip1 = np.repeat(ip1, self.size_j)
        iters_im1 = np.repeat(im1, self.size_j)
        iters_jp1 = np.tile(jp1, self.size_i)
        iters_jm1 = np.tile(jm1, self.size_i)
        point_jp1 = ijc_array[iters_i * self.size_i + iters_jp1]
        point_jm1 = ijc_array[iters_i * self.size_i + iters_jm1]
        point_ip1 = ijc_array[iters_j + iters_ip1 * self.size_i]
        point_im1 = ijc_array[iters_j + iters_im1 * self.size_i]

        column_x = np.concatenate(
            (
                point_jp1[:, None],
                point_jm1[:, None],
                point_ip1[:, None],
                point_im1[:, None],
            ),
            axis=1,
        ).ravel()
        column_y = np.concatenate(
            (
                point_ip1[:, None],
                point_im1[:, None],
                point_jp1[:, None],
                point_jm1[:, None],
            ),
            axis=1,
        ).ravel()
        array_x = np.concatenate(
            (
                (cfj * self.jacob_y_eta.ravel())[:, None],
                (-cfj * self.jacob_y_eta.ravel())[:, None],
                (-cfi * self.jacob_y_xi.ravel())[:, None],
                (cfi * self.jacob_y_xi.ravel())[:, None],
            ),
            axis=1,
        ).ravel()
        array_y = np.concatenate(
            (
                (cfi * self.jacob_x_xi.ravel())[:, None],
                (-cfi * self.jacob_x_xi.ravel())[:, None],
                (-cfj * self.jacob_x_eta.ravel())[:, None],
                (cfj * self.jacob_x_eta.ravel())[:, None],
            ),
            axis=1,
        ).ravel()

        grad_x = scp.csr_matrix(
            (array_x, (np.repeat(ijc_array, 4), column_x)),
            shape=(size, size)
        )
        grad_y = scp.csr_matrix(
            (array_y, (np.repeat(ijc_array, 4), column_y)),
            shape=(size, size)
        )
        self.lapl = (grad_x.dot(grad_x) + grad_y.dot(grad_y)) # .tolil()

    def diff_xi2(self, array_):
        """ compute differenciation in direction xi (j-direction)"""
        out = np.zeros_like(array_)
        size_j = out.shape[1]

        if self.order == 1:
            out[:, range(0, size_j - 1)] = (
                array_[:, range(1, size_j)] - array_[:, range(0, size_j - 1)])

            if self.periodic_xi:
                out[:, size_j-1] = (
                    array_[:, 0] - array_[:, size_j - 1])
            else:
                out[:, size_j-1] = array_[:, size_j-1] - array_[:, size_j-2]

        if self.order == 2:
            out[:, range(1, size_j - 1)] = 0.5 * (
                array_[:, range(2, size_j)] - array_[:, range(0, size_j - 2)])

            if self.periodic_xi:
                out[:, 0] = 0.5 * (
                    array_[:, 1] - array_[:, size_j-1])

                out[:, size_j-1] = 0.5 * (
                    array_[:, 0] - array_[:, size_j-2])
            else:
                out[:, 0] = array_[:, 1] - array_[:, 0]
                out[:, size_j-1] = array_[:, size_j-1] - array_[:, size_j-2]

        return out

    def diff_eta2(self, array_):
        """ compute differenciation in direction eta (i-direction)"""
        out = np.zeros_like(array_)
        size_i = out.shape[0]

        if self.order == 1:
            out[range(0, size_i-1), :] = (
                array_[range(1, size_i), :] - array_[range(0, size_i-1), :])

            if self.periodic_eta:
                out[size_i-1, :] = (
                    array_[0, :] - array_[size_i-1, :])
            else:
                out[size_i-1, :] = array_[size_i-1, :] - array_[size_i-2, :]

        if self.order == 2:
            out[range(1, size_i-1), :] = 0.5 * (
                array_[range(2, size_i), :] - array_[range(0, size_i-2), :])

            if self.periodic_eta:
                out[0, :] = 0.5 * (
                    array_[1, :] - array_[size_i-1, :])

                out[size_i-1, :] = 0.5 * (
                    array_[0, :] - array_[size_i-2, :])
            else:
                out[0, :] = array_[1, :] - array_[0, :]
                out[size_i-1, :] = array_[size_i-1, :] - array_[size_i-2, :]
        return out

    def compute_gradient(self, field):
        """ Compute the gradient of a field

        Parameters :
        -----------
        field : numpy array (n,m) , field

        Returns :
        ---------
        (gradient_x  gradient_y),: set of gradients in each direction

        """
        diff_f_xi = self.diff_xi2(field)
        diff_f_eta = self.diff_eta2(field)
        grad_x = diff_f_xi*self.jacob_y_eta - diff_f_eta*self.jacob_y_xi
        grad_y = diff_f_eta*self.jacob_x_xi - diff_f_xi*self.jacob_x_eta
        return grad_x, grad_y

    def compute_laplacian(self, field):
        """ Compute the diagonal elements of the hessian of a field

        Parameters :
        -----------
        field : numpy array (n,m) , field

        Returns :
        ---------
        (hess_xx  hess_yy),:  hessiang diagonal for each direction

        """
        #grad_x, grad_y = self.compute_gradient(field)
        laplacian = ((self.diff_xi2(self.diff_xi2(field)
                                    * self.jacob_y_eta
                                    - self.diff_eta2(field)
                                    * self.jacob_y_xi) * self.jacob_y_eta
                      - self.diff_eta2(self.diff_xi2(field)
                                       * self.jacob_y_eta
                                       - self.diff_eta2(field)
                                       * self.jacob_y_xi) * self.jacob_y_xi)
                     + (self.diff_eta2(self.diff_eta2(field)
                                       * self.jacob_x_xi
                                       - self.diff_xi2(field)
                                       * self.jacob_x_eta)*self.jacob_x_xi
                        - self.diff_xi2(self.diff_eta2(field)
                                        * self.jacob_x_xi
                                        - self.diff_xi2(field)
                                        * self.jacob_x_eta)*self.jacob_x_eta))
        return laplacian


def gen_cart_grid(gridrange,
                  gridpoints):
    """ Generate cartesian grid.

    Parameters :
    ------------
    gridrange : tuple of foats, dimensions of the grid
    gridpoints : tuple of ints (n,m), sampling on the grid

    Returns :
    ---------

    x_coor, y_coor : numpy arrays (n,m) with coordiantes
    """
    x_vec = np.linspace(0, gridrange[0], gridpoints[0], endpoint=True)
    y_vec = np.linspace(0, gridrange[1], gridpoints[1], endpoint=True)
    x_coor, y_coor = np.meshgrid(x_vec, y_vec)
    return x_coor, y_coor


def dilate_center(x_coor, y_coor, perturbation=1.0):
    """ pertubate cartesian mesh dilatation in the center

    Parameters :
    -----------
    x_coor : numpy array (n,m) , x_coordinates
    y_coor : numpy array (n,m) , y_coordinates
    perturbation : float, amplitude of the perturbation perturbation
                   with respect to the grid size

    Returns :
    ----------
    x_coor : numpy array (n,m) , x_coordinates shifted
    y_coor : numpy array (n,m) , y_coordinates shifted

     """
    x_width = x_coor.max() - x_coor.min()
    y_width = y_coor.max() - y_coor.min()
    x_center = x_coor.min() + 0.5*x_width
    y_center = y_coor.min() + 0.5*y_width

    adim_rad = np.sqrt(((x_coor-x_center)/(0.5*x_width))**2
                       + ((y_coor-y_center)/(0.5*y_width))**2)

    rad_dir_x = (x_coor-x_center) / np.maximum(adim_rad, 1.e-16)
    rad_dir_y = (y_coor-y_center) / np.maximum(adim_rad, 1.e-16)
    dilate = np.maximum((1.-adim_rad), 0)
    dilate = 3*dilate*dilate*(1-dilate)

    shift_x = perturbation*x_width*dilate*rad_dir_x
    shift_y = perturbation*y_width*dilate*rad_dir_y

    return x_coor+shift_x, y_coor+shift_y, dilate


def donut_function(x_coor, y_coor, center, radius):
    """
    create a donut test function, with analytically known derivatives

    Parameters :
    -----------
    x_coor : numpy array (n,m) , x_coordinates
    y_coor : numpy array (n,m) , y_coordinates
    center : tuple of floats, center
    radius ; float, radius of donut

    Returns :
    ---------
    donut : numpy array (n,m) , donut test function

    """
    r_coor = np.hypot(x_coor-center[0], y_coor-center[1])
    r_calib = (np.clip(r_coor/radius, 0.5, 1.0)*2-1)
    donut = np.cos(r_calib*np.pi)

    mslope = np.pi/(0.5*radius)
    diff_donut = np.sin(r_calib*np.pi)*mslope
    diff_donut = np.where(r_calib > 0, diff_donut, 0)
    diff_donut = np.where(r_calib < 1, diff_donut, 0)

    diff2_donut = -np.cos(r_calib*np.pi)*mslope*mslope
    diff2_donut = np.where(r_calib > 0, diff2_donut, 0)
    diff2_donut = np.where(r_calib < 1, diff2_donut, 0)

    print('Max grad, grad2 ', mslope, mslope**2)

    return donut, diff_donut, diff2_donut


def double_sine_function(x_coor, y_coor):
    """
    create a  double_sine function, with analytically known derivatives

    Parameters :
    -----------
    x_coor : numpy array (n,m), x_coordinates
    y_coor : numpy array (n,m), y_coordinates

    Returns :
    ---------
    slop : numpy array (n,m) , donut test function

    """
    return np.sin(x_coor)*np.sin(y_coor)


def slope_function(coor, min_val, max_val):
    """
    create a slope x test function, with analytically known derivatives

    Parameters :
    -----------
    coor : numpy array (n,m) , coordinates
    min_val : minimum value
    max_val ; maximum value

    Returns :
    ---------
    slop : numpy array (n,m) , slope test function

    """

    min_c = coor.min()
    max_c = coor.max()

    out = np.ones_like(coor)*min_val
    out += (coor-min_c)/(max_c-min_c) * (max_val-min_val)

    return out


def compute_constants(params):
    """ compute_constants parameters

    Parameters :
    ------------
    params : dict of setup parameters


    Returns :
    ------------
    const : dict of constant parameters
    """

    const = {}
    const["h_ratio"] = params["h_cold"]/params["h_hot"]
    const["biot"] = params["h_hot"] * params["width"]/params["lambda"]
    const["t_ref"] = (params["t_cold"]
                      + ((params["t_hot"] - params["t_cold"])
                         * (1. / (1. + const["h_ratio"]))))
    const["dx"] = params["typ_size"] / params["res"]

    const["lam_ov_rhocp"] = params["lambda"]/(params["rho"]*params["cp"])

    const["dt"] = params["fourier"] * const["dx"]**2 / const["lam_ov_rhocp"]
    const["total_time"] = params["typ_size"]**2 / const["lam_ov_rhocp"]
    const["exp_iterations"] = const["total_time"] / const["dt"]

    for key in const:
        print(key
              + ":"
              + str(const[key]))

    return const


def explicit_solve(temp0, metric, params, const, t_ref):
    """ Explicit time marching solver """

    def residual_max(res):
        """ Compute the non dimensional residual maxx """
        return (np.abs(res).max()
                / (params["t_hot"]-params["t_cold"])
                * const["total_time"]/const["dt"])

    def gap(temp):
        """ return the maximum absolute error """
        return np.abs(t_ref-temp).max()

    loop = 0
    residual = temp0
    temp = temp0
    counter = 0
    while gap(temp) > params["tol"] and loop < params["max_loop"]:
        loop += 1
        counter += 1
        temp[0, :] = params["t_cold"]
        temp[-1, :] = params["t_hot"]
        residual = (const["dt"]
                    * const["lam_ov_rhocp"]
                    * metric.compute_laplacian(temp))
        temp += residual

        if counter > 1000:
            counter = 0
            print("iterations :" + str(loop))
            print("relative residual : " + str(residual_max(residual)))

    print("final time : " + str(loop*const["dt"]))

    return temp


def optimize_solve(temp0, metric, params, const):
    """ give solution by root finding """
    shape2d = (params["res"], params["res"])

    def res_func(temp):
        """ test function for fsolve"""
        rhs2d = (const["dt"]
                 * const["lam_ov_rhocp"]
                 * metric.compute_laplacian(temp.reshape(shape2d)))

        rhs2d[:, 0] = params["t_cold"] - temp.reshape(shape2d)[:, 0]
        rhs2d[:, -1] = params["t_hot"] - temp.reshape(shape2d)[:, -1]

        return rhs2d.ravel()
    # root
    #opt = sciopt.root(res_func, temp0.ravel())
    # print opt.success
    #out = opt.x.reshape(shape2d)

    out = sciopt.fmin_bfgs(res_func, temp0.ravel())
    return out


def showmat(matrx):
    """ show matrix """
    fig = plt.figure()
    axes = fig.add_subplot(111)
    cax = axes.matshow(matrx)
    fig.colorbar(cax)
    plt.show()

def apply_bc_csr(
        matrix_csr_operator,
        size_i,
        size_j,
        min_val,
        max_val):
    """ give the altered version of matrix and RHS to apply CLS """
    i = 0
    bnd_south = np.array([(j + size_j*i) for j in range(size_j)])
    i = size_i-1
    bnd_north = np.array([(j + size_j*i) for j in range(size_j)])
    # j = 0
    # bnd_west = [(j + size_j*i) for i in range(size_i)]
    # j = size_j-1
    # bnd_east = [(j + size_j*i) for i in range(size_i)]

    matrix_lhs = scp.csr_matrix.copy(matrix_csr_operator)
    rhs = np.zeros(size_i * size_j)
    def enforce_bc_dirichlet(positions, value):
        """ single function to enforce the bc effect """
        for row in positions:
            mat_bc.data[mat_bc.indptr[row]:mat_bc.indptr[row+1]] = 0.
        mat_bc[positions, positions] = 1.
        # for pos in positions:
        #    mat_bc[pos, :] = 0.
        #    mat_bc[pos, pos] = 1.
        # initial version for non-csr matrix:
        #mat_bc[positions, :] = 0.
        #mat_bc[positions, pos] = 1.
        rhs[positions] = value

    enforce_bc_dirichlet(bnd_north, max_val)
    #enforce_bc(bnd_west, max_val)
    enforce_bc_dirichlet(bnd_south, min_val)
    #enforce_bc(bnd_east, min_val)
    return mat_bc, rhs


def main_2dheattreansf(params):
    """ Set up main 2D theat transfert resolution

    Parameters :
    ------------
    params : dict of setup parameters

    """
    const = compute_constants(params)
    x_coor, y_coor = gen_cart_grid(gridrange=(params["typ_size"],
                                              params["typ_size"]),
                                   gridpoints=(params["res"],
                                               params["res"]))
    if params["dilate_grid"]:
        x_coor, y_coor, _ = dilate_center(x_coor, y_coor)

    metric = Metrics(x_coor, y_coor)
    #temp0 = np.ones_like(x_coor)

    temp_final = slope_function(y_coor, params["t_cold"], params["t_hot"])
    #temp0 = double_sine_function(x_coor, y_coor)
    #lap2 = np.dot(metric.matlap, temp0.ravel()).reshape(temp0.shape)

    temp0_1d = np.ones(metric.shp1d) * params["t_cold"]
    temp0_2d = temp0_1d.reshape(metric.shp2d)

    if params["method"] == "iterative":
        mat_bc_csr, rhs = apply_bc_csr(
            metric.lapl,
            metric.size_i,
            metric.size_j,
            params["t_cold"],
            params["t_hot"])

        temp1d, info = scp.linalg.bicgstab(
            mat_bc_csr,
            rhs,
            x0=temp0_1d,
            tol=1e-1
        )
        print(">> Result bicg ", info)
        temp = temp1d.reshape(metric.shp2d)

    if params["method"] == "direct":
        temp = explicit_solve(
            temp0_2d,
            metric,
            params,
            const,
            temp_final)

    def gap(temp):
        """ return the maximum absolute error """
        return np.abs(temp_final-temp).max()
    print("Max error:", gap(temp))

    outh5 = NpArray2Xmf("out.h5")
    outh5.create_grid(x_coor,
                      y_coor,
                      np.zeros(metric.shp2d))
    outh5.add_field(temp, "temp")
    outh5.add_field(temp_final-temp, "temp_error")
    outh5.dump()


if __name__ == "__main__":

    PARAMS = {"res": 1000,
              "max_loop": 1000000,
              "dilate_grid": True,
              "method": "iterative",
              #"method": "direct",
              "tol": 1.0,
              "fourier": 0.8,
              "typ_size": 0.1,
              "width": 0.001,
              "rho": 7900.,
              "cp": 435.,
              "lambda": 11.4,
              "t_hot": 1500.,
              "t_cold": 600.,
              "h_hot": 1500.,
              "h_cold": 3000.}
    main_2dheattreansf(PARAMS)
