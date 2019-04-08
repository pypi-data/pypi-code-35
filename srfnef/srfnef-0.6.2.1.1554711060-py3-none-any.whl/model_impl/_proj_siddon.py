# encoding: utf-8
'''
@author: Minghao Guo
@contact: mh.guo0111@gmail.com
@software: srf_ct
@file: _proj_siddon.py
@date: 1/21/2019
@desc:
'''

import numpy as np
from numba import jit, cuda

running_env = jit(nopython = True, parallel = True)


@running_env
def _kernel_proj_3d_siddon(i, image, fst, snd, unit_size, center, vproj):
    dx, dy, dz = unit_size
    nx, ny, nz = image.shape[0], image.shape[1], image.shape[2]
    nx2, ny2, nz2 = nx / 2, ny / 2, nz / 2

    x1, y1, z1 = fst[i, 0] - center[0], fst[i, 1] - center[1], fst[i, 2] - center[2]
    x2, y2, z2 = snd[i, 0] - center[0], snd[i, 1] - center[1], snd[i, 2] - center[2]
    xd, yd, zd = x2 - x1, y2 - y1, z2 - z1
    if (xd ** 2 + yd ** 2) ** 0.5 < 10:
        return
    L = (xd ** 2 + yd ** 2 + zd ** 2) ** 0.5

    x1, y1, z1 = (fst[i, 0] - center[0]) / dx, \
                 (fst[i, 1] - center[1]) / dx, \
                 (fst[i, 2] - center[2]) / dx
    x2, y2, z2 = (snd[i, 0] - center[0]) / dx, \
                 (snd[i, 1] - center[1]) / dx, \
                 (snd[i, 2] - center[2]) / dx
    dy, dz = dy / dx, dz / dx

    if abs(xd) > abs(yd):
        ky = yd / xd
        kz = zd / xd
        for ix in range(nx):
            xx1 = ix - nx2
            xx2 = xx1 + 1
            if ky >= 0:
                yy1 = (y1 + ky * (xx1 - x1)) / dy + ny2
                yy2 = (y1 + ky * (xx2 - x1)) / dy + ny2
            else:
                yy1 = (y1 + ky * (xx2 - x1)) / dy + ny2
                yy2 = (y1 + ky * (xx1 - x1)) / dy + ny2
            cy1 = int(yy1)
            cy2 = int(yy2)

            if kz >= 0:
                zz1 = (z1 + kz * (xx1 - x1)) / dz + nz2
                zz2 = (z1 + kz * (xx2 - x1)) / dz + nz2
            else:
                zz1 = (z1 + kz * (xx2 - x1)) / dz + nz2
                zz2 = (z1 + kz * (xx1 - x1)) / dz + nz2
            cz1 = int(zz1)
            cz2 = int(zz2)
            if cy1 == cy2:
                if 0 <= cy1 < ny:
                    if cz1 == cz2:
                        if 0 <= cz1 < nz:
                            iy = cy1
                            iz = cz1
                            weight = (1 + ky ** 2 + kz ** 2) ** 0.5
                            vproj[i] += image[ix, iy, iz] * weight

                    else:
                        if -1 <= cz1 < nz:
                            rz = (cz2 - zz1) / (zz2 - zz1)
                            if cz1 >= 0:
                                iy = cy1
                                iz = cz1
                                weight = rz * (1 + ky ** 2 + kz ** 2) ** 0.5
                                vproj[i] += image[ix, iy, iz] * weight

                            if cz2 < nz:
                                iy = cy1
                                iz = cz2
                                weight = (1 - rz) * (1 + ky ** 2 + kz ** 2) ** 0.5
                                vproj[i] += image[ix, iy, iz] * weight

            else:
                if -1 <= cy1 < ny:
                    if cz1 == cz2:
                        if 0 <= cz1 < nz:
                            ry = (cy2 - yy1) / (yy2 - yy1)
                            if cy1 >= 0:
                                iy = cy1
                                iz = cz1
                                weight = ry * (1 + ky ** 2 + kz ** 2) ** 0.5
                                vproj[i] += image[ix, iy, iz] * weight

                            if cy2 < ny:
                                iy = cy2
                                iz = cz1
                                weight = (1 - ry) * (1 + ky ** 2 + kz ** 2) ** 0.5
                                vproj[i] += image[ix, iy, iz] * weight

                    else:
                        if -1 <= cz1 < nz:
                            ry = (cy2 - yy1) / (yy2 - yy1)
                            rz = (cz2 - zz1) / (zz2 - zz1)
                            if ry > rz:
                                if cy1 >= 0 and cz1 >= 0:
                                    iy = cy1
                                    iz = cz1
                                    weight = rz * (1 + ky ** 2 + kz ** 2) ** 0.5
                                    vproj[i] += image[ix, iy, iz] * weight

                                if cy1 >= 0 and cz2 < nz:
                                    iy = cy1
                                    iz = cz2
                                    weight = (ry - rz) * (1 + ky ** 2 + kz ** 2) ** 0.5
                                    vproj[i] += image[ix, iy, iz] * weight

                                if cy2 < ny and cz2 < nz:
                                    iy = cy2
                                    iz = cz2
                                    weight = (1 - ry) * (1 + ky ** 2 + kz ** 2) ** 0.5
                                    vproj[i] += image[ix, iy, iz] * weight

                            else:
                                if cy1 >= 0 and cz1 >= 0:
                                    iy = cy1
                                    iz = cz1
                                    weight = ry * (1 + ky ** 2 + kz ** 2) ** 0.5
                                    vproj[i] += image[ix, iy, iz] * weight

                                if cy2 < ny and cz1 >= 0:
                                    iy = cy2
                                    iz = cz1
                                    weight = (rz - ry) * (1 + ky ** 2 + kz ** 2) ** 0.5
                                    vproj[i] += image[ix, iy, iz] * weight

                                if cy2 < ny and cz2 < nz:
                                    iy = cy2
                                    iz = cz2
                                    weight = (1 - rz) * (1 + ky ** 2 + kz ** 2) ** 0.5
                                    vproj[i] += image[ix, iy, iz] * weight

    else:
        kx = xd / yd
        kz = zd / yd
        for iy in range(ny):
            yy1 = iy - ny2
            yy2 = yy1 + 1
            if kx >= 0:
                xx1 = (x1 + kx * (yy1 - y1)) / 1.0 + nx2
                xx2 = (x1 + kx * (yy2 - y1)) / 1.0 + nx2
            else:
                xx1 = (x1 + kx * (yy2 - y1)) / 1.0 + nx2
                xx2 = (x1 + kx * (yy1 - y1)) / 1.0 + nx2
            cx1 = int(xx1)
            cx2 = int(xx2)

            if kz >= 0:
                zz1 = (z1 + kz * (yy1 - y1)) / dz + nz2
                zz2 = (z1 + kz * (yy2 - y1)) / dz + nz2
            else:
                zz1 = (z1 + kz * (yy2 - y1)) / dz + nz2
                zz2 = (z1 + kz * (yy1 - y1)) / dz + nz2
            cz1 = int(zz1)
            cz2 = int(zz2)
            if cx1 == cx2:
                if 0 <= cx1 < nx:
                    if cz1 == cz2:
                        if 0 <= cz1 < nz:
                            ix = cx1
                            iz = cz1
                            weight = (1 + kx ** 2 + kz ** 2) ** 0.5
                            vproj[i] += image[ix, iy, iz] * weight

                    else:
                        if -1 <= cz1 < nz:
                            rz = (cz2 - zz1) / (zz2 - zz1)
                            if cz1 >= 0:
                                ix = cx1
                                iz = cz1
                                weight = rz * (1 + kx ** 2 + kz ** 2) ** 0.5
                                vproj[i] += image[ix, iy, iz] * weight

                            if cz2 < nz:
                                ix = cx1
                                iz = cz2
                                weight = (1 - rz) * (1 + kx ** 2 + kz ** 2) ** 0.5
                                vproj[i] += image[ix, iy, iz] * weight

            else:
                if -1 <= cx1 < nx:
                    if cz1 == cz2:
                        if 0 <= cz1 < nz:
                            rx = (cx2 - xx1) / (xx2 - xx1)
                            if cx1 >= 0:
                                ix = cx1
                                iz = cz1
                                weight = rx * (1 + kx ** 2 + kz ** 2) ** 0.5
                                vproj[i] += image[ix, iy, iz] * weight

                            if cx2 < nx:
                                ix = cx2
                                iz = cz1
                                weight = (1 - rx) * (1 + kx ** 2 + kz ** 2) ** 0.5
                                vproj[i] += image[ix, iy, iz] * weight

                    else:
                        if -1 <= cz1 < nz:
                            rx = (cx2 - xx1) / (xx2 - xx1)
                            rz = (cz2 - zz1) / (zz2 - zz1)
                            if rx > rz:
                                if cx1 >= 0 and cz1 >= 0:
                                    ix = cx1
                                    iz = cz1
                                    weight = rz * (1 + kx ** 2 + kz ** 2) ** 0.5
                                    vproj[i] += image[ix, iy, iz] * weight

                                if cx1 >= 0 and cz2 < nz:
                                    ix = cx1
                                    iz = cz2
                                    weight = (rx - rz) * (1 + kx ** 2 + kz ** 2) ** 0.5
                                    vproj[i] += image[ix, iy, iz] * weight

                                if cx2 < nx and cz2 < nz:
                                    ix = cx2
                                    iz = cz2
                                    weight = (1 - rx) * (1 + kx ** 2 + kz ** 2) ** 0.5
                                    vproj[i] += image[ix, iy, iz] * weight

                            else:
                                if cx1 >= 0 and cz1 >= 0:
                                    ix = cx1
                                    iz = cz1
                                    weight = rx * (1 + kx ** 2 + kz ** 2) ** 0.5
                                    vproj[i] += image[ix, iy, iz] * weight

                                if cx2 < nx and cz1 >= 0:
                                    ix = cx2
                                    iz = cz1
                                    weight = (rz - rx) * (1 + kx ** 2 + kz ** 2) ** 0.5
                                    vproj[i] += image[ix, iy, iz] * weight

                                if cx2 < nx and cz2 < nz:
                                    ix = cx2
                                    iz = cz2
                                    weight = (1 - rz) * (1 + kx ** 2 + kz ** 2) ** 0.5
                                    vproj[i] += image[ix, iy, iz] * weight

    vproj[i] *= dx
    if L > 0:
        vproj[i] /= L * L


@running_env
def proj_siddon(image, lors, unit_size, center):
    vproj = np.zeros((lors.shape[0],), dtype = np.float32)

    for i in range(lors.shape[0]):
        _kernel_proj_3d_siddon(i, image, lors[:, :3], lors[:, 3:6], unit_size, center, vproj)
    return vproj


@cuda.jit(device = True)
def _kernel_proj_3d_siddon_cuda(i, image, fst, snd, unit_size, center, vproj):
    dx, dy, dz = unit_size
    dy /= dx
    dz /= dx
    x1, y1, z1 = (fst[0] - center[0]) / dx, (fst[1] - center[1]) / dx, \
                 (fst[2] - center[2]) / dx
    x2, y2, z2 = (snd[0] - center[0]) / dx, (snd[1] - center[1]) / dx, \
                 (snd[2] - center[2]) / dx
    xd, yd, zd = x2 - x1, y2 - y1, z2 - z1
    if (xd ** 2 + yd ** 2) ** 0.5 < 10:
        return
    nx, ny, nz = image.shape[0], image.shape[1], image.shape[2]
    nx2, ny2, nz2 = nx / 2, ny / 2, nz / 2
    L = (xd ** 2 + yd ** 2 + zd ** 2) ** 0.5 * dx
    if abs(xd) > abs(yd):
        ky = yd / xd
        kz = zd / xd
        for ix in range(nx):
            xx1 = ix - nx2
            xx2 = xx1 + 1.0
            if ky >= 0:
                yy1 = (y1 + ky * (xx1 - x1)) / dy + ny2
                yy2 = (y1 + ky * (xx2 - x1)) / dy + ny2
            else:
                yy1 = (y1 + ky * (xx2 - x1)) / dy + ny2
                yy2 = (y1 + ky * (xx1 - x1)) / dy + ny2

            cy1 = int(yy1) if yy1 >= 0.0 else int(yy1) - 1
            cy2 = int(yy2) if yy2 >= 0.0 else int(yy2) - 1

            if kz >= 0:
                zz1 = (z1 + kz * (xx1 - x1)) / dz + nz2
                zz2 = (z1 + kz * (xx2 - x1)) / dz + nz2
            else:
                zz1 = (z1 + kz * (xx2 - x1)) / dz + nz2
                zz2 = (z1 + kz * (xx1 - x1)) / dz + nz2
            cz1 = int(zz1) if zz1 >= 0.0 else int(zz1) - 1
            cz2 = int(zz2) if zz2 >= 0.0 else int(zz2) - 1

            if cy1 == cy2:
                if 0 <= cy1 < ny:
                    if cz1 == cz2:
                        if 0 <= cz1 < nz:
                            iy = cy1
                            iz = cz1
                            weight = (1 + ky ** 2 + kz ** 2) ** 0.5
                            vproj[i] += image[ix, iy, iz] * weight
                    else:
                        if -1 <= cz1 < nz:
                            rz = (cz2 - zz1) / (zz2 - zz1)
                            if cz1 >= 0:
                                iy = cy1
                                iz = cz1
                                weight = rz * (1 + ky ** 2 + kz ** 2) ** 0.5
                                vproj[i] += image[ix, iy, iz] * weight

                            if cz2 < nz:
                                iy = cy1
                                iz = cz2
                                weight = (1 - rz) * (
                                        1 + ky ** 2 + kz ** 2) ** 0.5
                                vproj[i] += image[ix, iy, iz] * weight
            else:
                if -1 <= cy1 < ny:
                    if cz1 == cz2:
                        if 0 <= cz1 < nz:
                            ry = (cy2 - yy1) / (yy2 - yy1)
                            if cy1 >= 0:
                                iy = cy1
                                iz = cz1
                                weight = ry * (1 + ky ** 2 + kz ** 2) ** 0.5
                                vproj[i] += image[ix, iy, iz] * weight

                            if cy2 < ny:
                                iy = cy2
                                iz = cz1
                                weight = (1 - ry) * (1 + ky ** 2 + kz ** 2) ** 0.5
                                vproj[i] += image[ix, iy, iz] * weight

                    else:

                        if -1 <= cz1 < nz:
                            ry = (cy2 - yy1) / (yy2 - yy1)
                            rz = (cz2 - zz1) / (zz2 - zz1)
                            if ry > rz:
                                if cy1 >= 0 and cz1 >= 0:
                                    iy = cy1
                                    iz = cz1
                                    weight = rz * (
                                            1 + ky ** 2 + kz ** 2) ** 0.5
                                    vproj[i] += image[ix, iy, iz] * weight

                                if cy1 >= 0 and cz2 < nz:
                                    iy = cy1
                                    iz = cz2
                                    weight = (ry - rz) * (1 + ky ** 2 + kz ** 2) ** 0.5
                                    vproj[i] += image[ix, iy, iz] * weight

                                if cy2 < ny and cz2 < nz:
                                    iy = cy2
                                    iz = cz2
                                    weight = (1 - ry) * (1 + ky ** 2 + kz ** 2) ** 0.5
                                    vproj[i] += image[ix, iy, iz] * weight

                            else:
                                if cy1 >= 0 and cz1 >= 0:
                                    iy = cy1
                                    iz = cz1
                                    weight = ry * (1 + ky ** 2 + kz ** 2) ** 0.5
                                    vproj[i] += image[ix, iy, iz] * weight

                                if cy2 < ny and cz1 >= 0:
                                    iy = cy2
                                    iz = cz1
                                    weight = (rz - ry) * (1 + ky ** 2 + kz ** 2) ** 0.5
                                    vproj[i] += image[ix, iy, iz] * weight

                                if cy2 < ny and cz2 < nz:
                                    iy = cy2
                                    iz = cz2
                                    weight = (1 - rz) * (1 + ky ** 2 + kz ** 2) ** 0.5
                                    vproj[i] += image[ix, iy, iz] * weight

    else:

        kx = xd / yd
        kz = zd / yd
        for iy in range(ny):
            yy1 = iy - ny2
            yy2 = yy1 + 1
            if kx >= 0:
                xx1 = x1 + kx * (yy1 - y1) + nx2
                xx2 = x1 + kx * (yy2 - y1) + nx2
            else:
                xx1 = x1 + kx * (yy2 - y1) + nx2
                xx2 = x1 + kx * (yy1 - y1) + nx2
            cx1 = int(xx1) if xx1 >= 0.0 else int(xx1) - 1
            cx2 = int(xx2) if xx2 >= 0.0 else int(xx2) - 1

            if kz >= 0:
                zz1 = (z1 + kz * (yy1 - y1)) / dz + nz2
                zz2 = (z1 + kz * (yy2 - y1)) / dz + nz2
            else:
                zz1 = (z1 + kz * (yy2 - y1)) / dz + nz2
                zz2 = (z1 + kz * (yy1 - y1)) / dz + nz2
            cz1 = int(zz1) if zz1 >= 0.0 else int(zz1) - 1
            cz2 = int(zz2) if zz2 >= 0.0 else int(zz2) - 1
            if cx1 == cx2:
                if 0 <= cx1 < nx:
                    if cz1 == cz2:
                        if 0 <= cz1 < nz:
                            ix = cx1
                            iz = cz1
                            weight = (1 + kx ** 2 + kz ** 2) ** 0.5
                            vproj[i] += image[ix, iy, iz] * weight

                    else:
                        if -1 <= cz1 < nz:
                            rz = (cz2 - zz1) / (zz2 - zz1)
                            if cz1 >= 0:
                                ix = cx1
                                iz = cz1
                                weight = rz * (1 + kx ** 2 + kz ** 2) ** 0.5
                                vproj[i] += image[ix, iy, iz] * weight

                            if cz2 < nz:
                                ix = cx1
                                iz = cz2
                                weight = (1 - rz) * (1 + kx ** 2 + kz ** 2) ** 0.5
                                vproj[i] += image[ix, iy, iz] * weight

            else:
                if -1 <= cx1 < nx:
                    if cz1 == cz2:
                        if 0 <= cz1 < nz:
                            rx = (cx2 - xx1) / (xx2 - xx1)
                            if cx1 >= 0:
                                ix = cx1
                                iz = cz1
                                weight = rx * (1 + kx ** 2 + kz ** 2) ** 0.5
                                vproj[i] += image[ix, iy, iz] * weight

                            if cx2 < nx:
                                ix = cx2
                                iz = cz1
                                weight = (1 - rx) * (1 + kx ** 2 + kz ** 2) ** 0.5
                                vproj[i] += image[ix, iy, iz] * weight

                    else:
                        if -1 <= cz1 < nz:
                            rx = (cx2 - xx1) / (xx2 - xx1)
                            rz = (cz2 - zz1) / (zz2 - zz1)
                            if rx > rz:
                                if cx1 >= 0 and cz1 >= 0:
                                    ix = cx1
                                    iz = cz1
                                    weight = rz * (1 + kx ** 2 + kz ** 2) ** 0.5
                                    vproj[i] += image[ix, iy, iz] * weight

                                if cx1 >= 0 and cz2 < nz:
                                    ix = cx1
                                    iz = cz2
                                    weight = (rx - rz) * (1 + kx ** 2 + kz ** 2) ** 0.5
                                    vproj[i] += image[ix, iy, iz] * weight

                                if cx2 < nx and cz2 < nz:
                                    ix = cx2
                                    iz = cz2
                                    weight = (1 - rx) * (1 + kx ** 2 + kz ** 2) ** 0.5
                                    vproj[i] += image[ix, iy, iz] * weight

                            else:
                                if cx1 >= 0 and cz1 >= 0:
                                    ix = cx1
                                    iz = cz1
                                    weight = rx * (1 + kx ** 2 + kz ** 2) ** 0.5
                                    vproj[i] += image[ix, iy, iz] * weight

                                if cx2 < nx and cz1 >= 0:
                                    ix = cx2
                                    iz = cz1
                                    weight = (rz - rx) * (1 + kx ** 2 + kz ** 2) ** 0.5
                                    vproj[i] += image[ix, iy, iz] * weight

                                if cx2 < nx and cz2 < nz:
                                    ix = cx2
                                    iz = cz2
                                    weight = (1 - rz) * (1 + kx ** 2 + kz ** 2) ** 0.5
                                    vproj[i] += image[ix, iy, iz] * weight

    vproj[i] *= dx
    if L > 0:
        vproj[i] /= L * L


@cuda.jit
def proj_siddon_cuda(image, lors, unit_size, center, vproj):
    # i, j = cuda.grid(2)
    # id = i + j * cuda.gridDim.x * cuda.blockDim.x
    # if id >= lors.shape[0]:
    #     return
    # _kernel_proj_3d_siddon_cuda(id, image, lors[id, :3], lors[id, 3:6], unit_size, center,
    #                             vproj)
    i = cuda.grid(1)
    if i >= lors.shape[0]:
        return
    _kernel_proj_3d_siddon_cuda(i, image, lors[i, :3], lors[i, 3:6], unit_size, center,
                                vproj)
