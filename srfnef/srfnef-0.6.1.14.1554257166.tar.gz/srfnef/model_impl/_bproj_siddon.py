# encoding: utf-8
'''
@author: Minghao Guo
@contact: mh.guo0111@gmail.com
@software: srf_ct
@file: BackProjectors.py
@date: 1/7/2019
@desc:
'''

import math

import numpy as np
from numba import jit, cuda

running_env = jit(nopython = True, parallel = True)


@running_env
def _kernel_bproj_3d_siddon(i, fst, snd, vproj, unit_size, center, image):
    dx, dy, dz = unit_size
    dz /= dx
    x1, y1, z1 = (fst[i, 0] - center[0]) / dx, (fst[i, 1] - center[1]) / dx, (
            fst[i, 2] - center[2]) / dx
    x2, y2, z2 = (snd[i, 0] - center[0]) / dx, (snd[i, 1] - center[1]) / dx, (
            snd[i, 2] - center[2]) / dx
    dx = 1.
    xd, yd, zd = x2 - x1, y2 - y1, z2 - z1
    if (xd ** 2 + yd ** 2) ** 0.5 < 10:
        return
    nx, ny, nz = image.shape[0], image.shape[1], image.shape[2]
    nx2, ny2, nz2 = nx / 2, ny / 2, nz / 2
    L = (xd ** 2 + yd ** 2 + zd ** 2) ** 0.5
    if abs(xd) > abs(yd):
        ky = yd / xd
        kz = zd / xd
        for ix in range(nx):
            xx1 = ix - nx2
            xx2 = xx1 + 1
            if ky >= 0:
                yy1 = y1 + ky * (xx1 - x1) + ny2
                yy2 = y1 + ky * (xx2 - x1) + ny2
            else:
                yy1 = y1 + ky * (xx2 - x1) + ny2
                yy2 = y1 + ky * (xx1 - x1) + ny2
            cy1 = math.floor(yy1)
            cy2 = math.floor(yy2)

            if kz >= 0:
                zz1 = (z1 + kz * (xx1 - x1)) / dz + nz2
                zz2 = (z1 + kz * (xx2 - x1)) / dz + nz2
            else:
                zz1 = (z1 + kz * (xx2 - x1)) / dz + nz2
                zz2 = (z1 + kz * (xx1 - x1)) / dz + nz2
            cz1 = math.floor(zz1)
            cz2 = math.floor(zz2)
            if cy1 == cy2:
                if 0 <= cy1 < ny:
                    if cz1 == cz2:
                        if 0 <= cz1 < nz:
                            iy = cy1
                            iz = cz1
                            image[ix, iy, iz] += vproj[i] * (
                                    1 + ky ** 2 + kz ** 2) ** 0.5 * dx / L / L
                    else:
                        if -1 <= cz1 < nz:
                            rz = (cz2 - zz1) / (zz2 - zz1)
                            if cz1 >= 0:
                                iy = cy1
                                iz = cz1
                                image[ix, iy, iz] += vproj[i] * rz * (
                                        1 + ky ** 2 + kz ** 2) ** 0.5 * dx / L / L
                            if cz2 < nz:
                                iy = cy1
                                iz = cz2
                                image[ix, iy, iz] += vproj[i] * (1 - rz) * (
                                        1 + ky ** 2 + kz ** 2) ** 0.5 * dx / L / L
            else:
                if -1 <= cy1 < ny:
                    if cz1 == cz2:
                        if 0 <= cz1 < nz:
                            ry = (cy2 - yy1) / (yy2 - yy1)
                            if cy1 >= 0:
                                iy = cy1
                                iz = cz1
                                image[ix, iy, iz] += vproj[i] * ry * (
                                        1 + ky ** 2 + kz ** 2) ** 0.5 * dx / L / L
                            if cy2 < ny:
                                iy = cy2
                                iz = cz1
                                image[ix, iy, iz] += vproj[i] * (1 - ry) * (
                                        1 + ky ** 2 + kz ** 2) ** 0.5 * dx / L / L
                    else:
                        if -1 <= cz1 < nz:
                            ry = (cy2 - yy1) / (yy2 - yy1)
                            rz = (cz2 - zz1) / (zz2 - zz1)
                            if ry > rz:
                                if cy1 >= 0 and cz1 >= 0:
                                    iy = cy1
                                    iz = cz1
                                    image[ix, iy, iz] += vproj[i] * rz * (
                                            1 + ky ** 2 + kz ** 2) ** 0.5 * dx / L / L
                                if cy1 >= 0 and cz2 < nz:
                                    iy = cy1
                                    iz = cz2
                                    image[ix, iy, iz] += vproj[i] * (ry - rz) * (
                                            1 + ky ** 2 + kz ** 2) ** 0.5 * dx / L / L
                                if cy2 < ny and cz2 < nz:
                                    iy = cy2
                                    iz = cz2
                                    image[ix, iy, iz] += vproj[i] * (1 - ry) * (
                                            1 + ky ** 2 + kz ** 2) ** 0.5 * dx / L / L
                            else:
                                if cy1 >= 0 and cz1 >= 0:
                                    iy = cy1
                                    iz = cz1
                                    image[ix, iy, iz] += vproj[i] * ry * (
                                            1 + ky ** 2 + kz ** 2) ** 0.5 * dx / L / L
                                if cy2 < ny and cz1 >= 0:
                                    iy = cy2
                                    iz = cz1
                                    image[ix, iy, iz] += vproj[i] * (rz - ry) * (
                                            1 + ky ** 2 + kz ** 2) ** 0.5 * dx / L / L
                                if cy2 < ny and cz2 < nz:
                                    iy = cy2
                                    iz = cz2
                                    image[ix, iy, iz] += vproj[i] * (1 - rz) * (
                                            1 + ky ** 2 + kz ** 2) ** 0.5 * dx / L / L
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
            cx1 = math.floor(xx1)
            cx2 = math.floor(xx2)

            if kz >= 0:
                zz1 = (z1 + kz * (yy1 - y1)) / dz + nz2
                zz2 = (z1 + kz * (yy2 - y1)) / dz + nz2
            else:
                zz1 = (z1 + kz * (yy2 - y1)) / dz + nz2
                zz2 = (z1 + kz * (yy1 - y1)) / dz + nz2
            cz1 = math.floor(zz1)
            cz2 = math.floor(zz2)
            if cx1 == cx2:
                if 0 <= cx1 < nx:
                    if cz1 == cz2:
                        if 0 <= cz1 < nz:
                            ix = cx1
                            iz = cz1
                            image[ix, iy, iz] += vproj[i] * (
                                    1 + kx ** 2 + kz ** 2) ** 0.5 * dx / L / L
                    else:
                        if -1 <= cz1 < nz:
                            rz = (cz2 - zz1) / (zz2 - zz1)
                            if cz1 >= 0:
                                ix = cx1
                                iz = cz1
                                image[ix, iy, iz] += vproj[i] * rz * (
                                        1 + kx ** 2 + kz ** 2) ** 0.5 * dx / L / L
                            if cz2 < nz:
                                ix = cx1
                                iz = cz2
                                image[ix, iy, iz] += vproj[i] * (1 - rz) * (
                                        1 + kx ** 2 + kz ** 2) ** 0.5 * dx / L / L
            else:
                if -1 <= cx1 < nx:
                    if cz1 == cz2:
                        if 0 <= cz1 < nz:
                            rx = (cx2 - xx1) / (xx2 - xx1)
                            if cx1 >= 0:
                                ix = cx1
                                iz = cz1
                                image[ix, iy, iz] += vproj[i] * rx * (
                                        1 + kx ** 2 + kz ** 2) ** 0.5 * dx / L / L
                            if cx2 < nx:
                                ix = cx2
                                iz = cz1
                                image[ix, iy, iz] += vproj[i] * (1 - rx) * (
                                        1 + kx ** 2 + kz ** 2) ** 0.5 * dx / L / L
                    else:
                        if -1 <= cz1 < nz:
                            rx = (cx2 - xx1) / (xx2 - xx1)
                            rz = (cz2 - zz1) / (zz2 - zz1)
                            if rx > rz:
                                if cx1 >= 0 and cz1 >= 0:
                                    ix = cx1
                                    iz = cz1
                                    image[ix, iy, iz] += vproj[i] * rz * (
                                            1 + kx ** 2 + kz ** 2) ** 0.5 * dx / L / L
                                if cx1 >= 0 and cz2 < nz:
                                    ix = cx1
                                    iz = cz2
                                    image[ix, iy, iz] += vproj[i] * (rx - rz) * (
                                            1 + kx ** 2 + kz ** 2) ** 0.5 * dx / L / L
                                if cx2 < nx and cz2 < nz:
                                    ix = cx2
                                    iz = cz2
                                    image[ix, iy, iz] += vproj[i] * (1 - rx) * (
                                            1 + kx ** 2 + kz ** 2) ** 0.5 * dx / L / L
                            else:
                                if cx1 >= 0 and cz1 >= 0:
                                    ix = cx1
                                    iz = cz1
                                    image[ix, iy, iz] += vproj[i] * rx * (
                                            1 + kx ** 2 + kz ** 2) ** 0.5 * dx / L / L
                                if cx2 < nx and cz1 >= 0:
                                    ix = cx2
                                    iz = cz1
                                    image[ix, iy, iz] += vproj[i] * (rz - rx) * (
                                            1 + kx ** 2 + kz ** 2) ** 0.5 * dx / L / L
                                if cx2 < nx and cz2 < nz:
                                    ix = cx2
                                    iz = cz2
                                    image[ix, iy, iz] += vproj[i] * (1 - rz) * (
                                            1 + kx ** 2 + kz ** 2) ** 0.5 * dx / L / L


def bproj_siddon(vproj, lors, unit_size, center, shape):
    image = np.zeros(shape, dtype = np.float32)
    for i in range(lors.shape[0]):
        _kernel_bproj_3d_siddon(i, lors[:, :3], lors[:, 3:6], vproj, unit_size, center,
                                image)
    return image


@cuda.jit(device = True)
def _kernel_bproj_3d_siddon_cuda(i, fst, snd, vproj, unit_size, center, image):
    dx, dy, dz = unit_size
    dy /= dx
    dz /= dx
    x1, y1, z1 = (fst[i, 0] - center[0]) / dx, (fst[i, 1] - center[1]) / dx, (
            fst[i, 2] - center[2]) / dx
    x2, y2, z2 = (snd[i, 0] - center[0]) / dx, (snd[i, 1] - center[1]) / dx, (
            snd[i, 2] - center[2]) / dx
    xd, yd, zd = x2 - x1, y2 - y1, z2 - z1
    if (xd ** 2 + yd ** 2) ** 0.5 < 10:
        return
    nx, ny, nz = image.shape[0], image.shape[1], image.shape[2]
    nx2, ny2, nz2 = nx / 2, ny / 2, nz / 2
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
            cy1 = math.floor(yy1)
            cy2 = math.floor(yy2)

            if kz >= 0:
                zz1 = (z1 + kz * (xx1 - x1)) / dz + nz2
                zz2 = (z1 + kz * (xx2 - x1)) / dz + nz2
            else:
                zz1 = (z1 + kz * (xx2 - x1)) / dz + nz2
                zz2 = (z1 + kz * (xx1 - x1)) / dz + nz2
            cz1 = math.floor(zz1)
            cz2 = math.floor(zz2)
            if cy1 == cy2:
                if 0 <= cy1 < ny:
                    if cz1 == cz2:
                        if 0 <= cz1 < nz:
                            iy = cy1
                            iz = cz1
                            cuda.atomic.add(image, (ix, iy, iz),
                                            vproj[i] * (1 + ky ** 2 + kz ** 2) ** 0.5 * dx)
                            # image[ix, iy, iz] += vproj[i] * (1 + ky ** 2 + kz ** 2) ** 0.5
                    else:
                        if -1 <= cz1 < nz:
                            rz = (cz2 - zz1) / (zz2 - zz1)
                            if cz1 >= 0:
                                iy = cy1
                                iz = cz1
                                cuda.atomic.add(image, (ix, iy, iz),
                                                vproj[i] * rz * (
                                                        1 + ky ** 2 + kz ** 2) ** 0.5 * dx)
                                # image[ix, iy, iz] += vproj[i] * rz * (1 + ky ** 2 + kz ** 2) ** 0.5
                            if cz2 < nz:
                                iy = cy1
                                iz = cz2
                                cuda.atomic.add(image, (ix, iy, iz), vproj[i] * (1 - rz) * (
                                        1 + ky ** 2 + kz ** 2) ** 0.5 * dx)
                                # image[ix, iy, iz] += vproj[i] * (1 - rz) * (
                                #         1 + ky ** 2 + kz ** 2) ** 0.5
            else:
                if -1 <= cy1 < ny:
                    if cz1 == cz2:
                        if 0 <= cz1 < nz:
                            ry = (cy2 - yy1) / (yy2 - yy1)
                            if cy1 >= 0:
                                iy = cy1
                                iz = cz1
                                cuda.atomic.add(image, (ix, iy, iz),
                                                vproj[i] * ry * (
                                                        1 + ky ** 2 + kz ** 2) ** 0.5 * dx)
                                # image[ix, iy, iz] += vproj[i] * ry * (1 + ky ** 2 + kz ** 2) ** 0.5
                            if cy2 < ny:
                                iy = cy2
                                iz = cz1
                                cuda.atomic.add(image, (ix, iy, iz), vproj[i] * (1 - ry) * (
                                        1 + ky ** 2 + kz ** 2) ** 0.5 * dx)
                                # image[ix, iy, iz] += vproj[i] * (1 - ry) * (
                                #         1 + ky ** 2 + kz ** 2) ** 0.5
                    else:
                        if -1 <= cz1 < nz:
                            ry = (cy2 - yy1) / (yy2 - yy1)
                            rz = (cz2 - zz1) / (zz2 - zz1)
                            if ry > rz:
                                if cy1 >= 0 and cz1 >= 0:
                                    iy = cy1
                                    iz = cz1
                                    cuda.atomic.add(image, (ix, iy, iz), vproj[i] * rz * (
                                            1 + ky ** 2 + kz ** 2) ** 0.5 * dx)
                                    # image[ix, iy, iz] += vproj[i] * rz * (
                                    #         1 + ky ** 2 + kz ** 2) ** 0.5
                                if cy1 >= 0 and cz2 < nz:
                                    iy = cy1
                                    iz = cz2
                                    cuda.atomic.add(image, (ix, iy, iz), vproj[i] * (ry - rz) * (
                                            1 + ky ** 2 + kz ** 2) ** 0.5 * dx)
                                    # image[ix, iy, iz] += vproj[i] * (ry - rz) * (
                                    #         1 + ky ** 2 + kz ** 2) ** 0.5
                                if cy2 < ny and cz2 < nz:
                                    iy = cy2
                                    iz = cz2
                                    cuda.atomic.add(image, (ix, iy, iz), vproj[i] * (1 - ry) * (
                                            1 + ky ** 2 + kz ** 2) ** 0.5 * dx)
                                    # image[ix, iy, iz] += vproj[i] * (1 - ry) * (
                                    #         1 + ky ** 2 + kz ** 2) ** 0.5
                            else:
                                if cy1 >= 0 and cz1 >= 0:
                                    iy = cy1
                                    iz = cz1
                                    cuda.atomic.add(image, (ix, iy, iz), vproj[i] * ry * (
                                            1 + ky ** 2 + kz ** 2) ** 0.5 * dx)
                                    # image[ix, iy, iz] += vproj[i] * ry * (
                                    #         1 + ky ** 2 + kz ** 2) ** 0.5
                                if cy2 < ny and cz1 >= 0:
                                    iy = cy2
                                    iz = cz1
                                    cuda.atomic.add(image, (ix, iy, iz), vproj[i] * (rz - ry) * (
                                            1 + ky ** 2 + kz ** 2) ** 0.5 * dx)
                                    # image[ix, iy, iz] += vproj[i] * (rz - ry) * (
                                    #         1 + ky ** 2 + kz ** 2) ** 0.5
                                if cy2 < ny and cz2 < nz:
                                    iy = cy2
                                    iz = cz2
                                    cuda.atomic.add(image, (ix, iy, iz), vproj[i] * (1 - rz) * (
                                            1 + ky ** 2 + kz ** 2) ** 0.5 * dx)
                                    # image[ix, iy, iz] += vproj[i] * (1 - rz) * (
                                    #         1 + ky ** 2 + kz ** 2) ** 0.5
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
            cx1 = math.floor(xx1)
            cx2 = math.floor(xx2)

            if kz >= 0:
                zz1 = (z1 + kz * (yy1 - y1)) / dz + nz2
                zz2 = (z1 + kz * (yy2 - y1)) / dz + nz2
            else:
                zz1 = (z1 + kz * (yy2 - y1)) / dz + nz2
                zz2 = (z1 + kz * (yy1 - y1)) / dz + nz2
            cz1 = math.floor(zz1)
            cz2 = math.floor(zz2)
            if cx1 == cx2:
                if 0 <= cx1 < nx:
                    if cz1 == cz2:
                        if 0 <= cz1 < nz:
                            ix = cx1
                            iz = cz1
                            cuda.atomic.add(image, (ix, iy, iz), vproj[i] * (1 + kx ** 2 + kz **
                                                                             2) ** 0.5 * dx)
                            # image[ix, iy, iz] += vproj[i] * (1 + kx ** 2 + kz ** 2) ** 0.5
                    else:
                        if -1 <= cz1 < nz:
                            rz = (cz2 - zz1) / (zz2 - zz1)
                            if cz1 >= 0:
                                ix = cx1
                                iz = cz1
                                cuda.atomic.add(image, (ix, iy, iz), vproj[i] * rz * (1 + kx ** 2
                                                                                      + kz ** 2) ** 0.5 * dx)
                                # image[ix, iy, iz] += vproj[i] * rz * (1 + kx ** 2 + kz ** 2) ** 0.5
                            if cz2 < nz:
                                ix = cx1
                                iz = cz2
                            cuda.atomic.add(image, (ix, iy, iz), vproj[i] * (1 - rz) * (
                                    1 + kx ** 2 + kz ** 2) ** 0.5 * dx)
                            #         image[ix, iy, iz] += vproj[i] * (1 - rz) * (
                            # 1 + kx ** 2 + kz ** 2) ** 0.5
            else:
                if -1 <= cx1 < nx:
                    if cz1 == cz2:
                        if 0 <= cz1 < nz:
                            rx = (cx2 - xx1) / (xx2 - xx1)
                            if cx1 >= 0:
                                ix = cx1
                                iz = cz1
                                cuda.atomic.add(image, (ix, iy, iz), vproj[i] * rx * (
                                        1 + kx ** 2 + kz ** 2) ** 0.5 * dx)
                            #     image[ix, iy, iz] += vproj[i] * rx * (
                            # 1 + kx ** 2 + kz ** 2) ** 0.5
                            if cx2 < nx:
                                ix = cx2
                                iz = cz1
                                cuda.atomic.add(image, (ix, iy, iz), vproj[i] * (1 - rx) * (
                                        1 + kx ** 2 + kz ** 2) ** 0.5 * dx)
                            #         image[ix, iy, iz] += vproj[i] * (1 - rx) * (
                            # 1 + kx ** 2 + kz ** 2) ** 0.5
                    else:
                        if -1 <= cz1 < nz:
                            rx = (cx2 - xx1) / (xx2 - xx1)
                            rz = (cz2 - zz1) / (zz2 - zz1)
                            if rx > rz:
                                if cx1 >= 0 and cz1 >= 0:
                                    ix = cx1
                                    iz = cz1
                                    cuda.atomic.add(image, (ix, iy, iz), vproj[i] * rz * (
                                            1 + kx ** 2 + kz ** 2) ** 0.5 * dx)
                                    #         image[ix, iy, iz] += vproj[i] * rz * (
                                    # 1 + kx ** 2 + kz ** 2) ** 0.5
                                if cx1 >= 0 and cz2 < nz:
                                    ix = cx1
                                    iz = cz2
                                    cuda.atomic.add(image, (ix, iy, iz), vproj[i] * (rx - rz) * (
                                            1 + kx ** 2 + kz ** 2) ** 0.5 * dx)
                                    #         image[ix, iy, iz] += vproj[i] * (rx - rz) * (
                                    # 1 + kx ** 2 + kz ** 2) ** 0.5
                                if cx2 < nx and cz2 < nz:
                                    ix = cx2
                                    iz = cz2
                                    cuda.atomic.add(image, (ix, iy, iz), vproj[i] * (1 - rx) * (
                                            1 + kx ** 2 + kz ** 2) ** 0.5 * dx)
                                    #         image[ix, iy, iz] += vproj[i] * (1 - rx) * (
                                    # 1 + kx ** 2 + kz ** 2) ** 0.5
                            else:
                                if cx1 >= 0 and cz1 >= 0:
                                    ix = cx1
                                    iz = cz1
                                    cuda.atomic.add(image, (ix, iy, iz), vproj[i] * rx * (
                                            1 + kx ** 2 + kz ** 2) ** 0.5 * dx)
                                    #         image[ix, iy, iz] += vproj[i] * rx * (
                                    # 1 + kx ** 2 + kz ** 2) ** 0.5
                                if cx2 < nx and cz1 >= 0:
                                    ix = cx2
                                    iz = cz1
                                    cuda.atomic.add(image, (ix, iy, iz), vproj[i] * (rz - rx) * (
                                            1 + kx ** 2 + kz ** 2) ** 0.5 * dx)
                                    #         image[ix, iy, iz] += vproj[i] * (rz - rx) * (
                                    # 1 + kx ** 2 + kz ** 2) ** 0.5
                                if cx2 < nx and cz2 < nz:
                                    ix = cx2
                                    iz = cz2
                                    cuda.atomic.add(image, (ix, iy, iz), vproj[i] * (1 - rz) * (
                                            1 + kx ** 2 + kz ** 2) ** 0.5 * dx)
                                    #         image[ix, iy, iz] += vproj[i] * (1 - rz) * (
                                    # 1 + kx ** 2 + kz ** 2) ** 0.5


@cuda.jit
def bproj_siddon_cuda(vproj, lors, unit_size, center, image):
    i = cuda.grid(1)
    if i >= lors.shape[0]:
        return
    _kernel_bproj_3d_siddon_cuda(i, lors[:, :3], lors[:, 3:6], vproj, unit_size, center,
                                 image)
