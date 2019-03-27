#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
SSBJ test case - http://ntrs.nasa.gov/archive/nasa/casi.ntrs.nasa.gov/19980234657.pdf
Original Python implementation for OpenMDAO integration developed by
Sylvain Dubreuil and Remi Lafage of ONERA, the French Aerospace Lab.
Original files taken from: https://github.com/OneraHub/SSBJ-OpenMDAO
The files were adjusted for optimal use in KADMOS by Imco van Gent of TU Delft.
"""
from __future__ import absolute_import, division, print_function

import sys

import numpy as np
from lxml import etree

from openlego.partials.partials import Partials
from ssbjkadmos.config import root_tag, x_tc, x_AR, x_Lambda, x_Sref, x_lambda, x_section, x_WO, x_WE, x_WFO, \
    x_L, x_Nz, x_WT, x_WF, x_sigma1, x_sigma2, x_sigma3, x_sigma4, x_sigma5, x_Theta
from ssbjkadmos.tools.SsbjDiscipline import SsbjDiscipline
from ssbjkadmos.utils.general import get_float_value
from ssbjkadmos.utils.math import polynomial_function, get_d_dict
from ssbjkadmos.utils.execution import run_tool
from kadmos.utilities.xml_utils_openlego import xml_safe_create_element


class Structures(SsbjDiscipline):  # AbstractDiscipline

    @property
    def description(self):
        return u'Structural analysis discipline of the SSBJ test case.'

    @property
    def supplies_partials(self):
        return True

    def generate_input_xml(self):
        root = etree.Element(root_tag)
        doc = etree.ElementTree(root)

        xml_safe_create_element(doc, x_tc, self.get_scaler(x_tc))
        xml_safe_create_element(doc, x_AR, self.get_scaler(x_AR))
        xml_safe_create_element(doc, x_Lambda, self.get_scaler(x_Lambda))
        xml_safe_create_element(doc, x_Sref, self.get_scaler(x_Sref))
        xml_safe_create_element(doc, x_lambda, self.get_scaler(x_lambda))
        xml_safe_create_element(doc, x_section, self.get_scaler(x_section))
        xml_safe_create_element(doc, x_WE, self.get_scaler(x_WE))
        xml_safe_create_element(doc, x_L, self.get_scaler(x_L))
        xml_safe_create_element(doc, x_Nz, 6.)
        xml_safe_create_element(doc, x_WO, 25000.)
        xml_safe_create_element(doc, x_WFO, 2000.)

        return etree.tostring(doc, encoding='utf-8', pretty_print=True, xml_declaration=True)

    def generate_output_xml(self):
        root = etree.Element(root_tag)
        doc = etree.ElementTree(root)

        xml_safe_create_element(doc, x_WT, self.get_scaler(x_WT))
        xml_safe_create_element(doc, x_WF, self.get_scaler(x_WF))
        xml_safe_create_element(doc, x_sigma1, self.get_scaler(x_sigma1))
        xml_safe_create_element(doc, x_sigma2, self.get_scaler(x_sigma2))
        xml_safe_create_element(doc, x_sigma3, self.get_scaler(x_sigma3))
        xml_safe_create_element(doc, x_sigma4, self.get_scaler(x_sigma4))
        xml_safe_create_element(doc, x_sigma5, self.get_scaler(x_sigma5))
        xml_safe_create_element(doc, x_Theta, self.get_scaler(x_Theta))

        return etree.tostring(doc, encoding='utf-8', pretty_print=True, xml_declaration=True)

    def generate_partials_xml(self):
        partials = Partials()
        partials.declare_partials(x_WT,
                                  [x_tc, x_AR, x_Lambda, x_Sref, x_lambda, x_section, x_WE, x_L])
        partials.declare_partials(x_WF,
                                  [x_tc, x_AR, x_Lambda, x_Sref, x_lambda, x_section, x_WE, x_L])
        partials.declare_partials(x_sigma1,
                                  [x_tc, x_AR, x_Lambda, x_Sref, x_lambda, x_section, x_WE, x_L])
        partials.declare_partials(x_sigma2,
                                  [x_sigma3, x_AR, x_Lambda, x_Sref, x_lambda, x_section, x_WE, x_L])
        partials.declare_partials(x_sigma4,
                                  [x_tc, x_AR, x_Lambda, x_Sref, x_lambda, x_section, x_WE, x_L])
        partials.declare_partials(x_sigma5,
                                  [x_tc, x_AR, x_Lambda, x_Sref, x_lambda, x_section, x_WE, x_L])
        partials.declare_partials(x_Theta,
                                  [x_tc, x_AR, x_Lambda, x_Sref, x_lambda, x_section, x_WE, x_L])
        return partials.get_string()

    def execute(self, in_file, out_file):
        doc = etree.parse(in_file)
        z0 = self.unscale_float_value(x_tc, doc)
        z3 = self.unscale_float_value(x_AR, doc)
        z4 = self.unscale_float_value(x_Lambda, doc)
        z5 = self.unscale_float_value(x_Sref, doc)
        x0 = self.unscale_float_value(x_lambda, doc)
        x1 = self.unscale_float_value(x_section, doc)
        L = self.unscale_float_value(x_L, doc)
        WE = self.unscale_float_value(x_WE, doc)
        NZ = get_float_value(x_Nz, doc)
        WO = get_float_value(x_WO, doc)
        WFO = get_float_value(x_WFO, doc)

        Theta, WF, WT, sigma = structure(np.array([x0, x1]), np.array([z0, 0., 0., z3, z4, z5]),
                                         L, WE, NZ, WFO, WO)

        root = etree.Element(root_tag)
        doc = etree.ElementTree(root)
        xml_safe_create_element(doc, x_WF, self.scale_value(WF, x_WF))
        xml_safe_create_element(doc, x_WT, self.scale_value(WT, x_WT))

        xml_safe_create_element(doc, x_sigma1, self.scale_value(sigma[0], x_sigma1))
        xml_safe_create_element(doc, x_sigma2, self.scale_value(sigma[1], x_sigma2))
        xml_safe_create_element(doc, x_sigma3, self.scale_value(sigma[2], x_sigma3))
        xml_safe_create_element(doc, x_sigma4, self.scale_value(sigma[3], x_sigma4))
        xml_safe_create_element(doc, x_sigma5, self.scale_value(sigma[4], x_sigma5))

        xml_safe_create_element(doc, x_Theta, self.scale_value(Theta, x_Theta))

        doc.write(out_file, encoding='utf-8', pretty_print=True, xml_declaration=True)

    def linearize(self, in_file, partials_file):
        doc = etree.parse(in_file)
        z0 = self.unscale_float_value(x_tc, doc)
        z3 = self.unscale_float_value(x_AR, doc)
        z4 = self.unscale_float_value(x_Lambda, doc)
        z5 = self.unscale_float_value(x_Sref, doc)
        x0 = self.unscale_float_value(x_lambda, doc)
        x1 = self.unscale_float_value(x_section, doc)
        L = self.unscale_float_value(x_L, doc)
        NZ = get_float_value(x_Nz, doc)

        J_WT, J_WF, J_sigma, J_Theta = structure_partials(dict(z=np.array([z0, 0., 0., z3, z4, z5]),
                                                               x_str=np.array([x0, x1]),
                                                               L=L, NZ=NZ),
                                                          scalers=self.scalers)

        partials = Partials()
        partials.declare_partials(x_WT,
                                  [x_tc, x_AR, x_Lambda, x_Sref, x_lambda, x_section, x_WE, x_L],
                                  [J_WT['z'][0,0], J_WT['z'][0,3], J_WT['z'][0,4], J_WT['z'][0,5],
                                   J_WT['x_str'][0, 0], J_WT['x_str'][0, 1],
                                   J_WT['WE'], J_WT['L']])
        partials.declare_partials(x_WF,
                                  [x_tc, x_AR, x_Lambda, x_Sref, x_lambda, x_section, x_WE, x_L],
                                  [J_WF['z'][0, 0], J_WF['z'][0, 3], J_WF['z'][0, 4], J_WF['z'][0, 5],
                                   J_WF['x_str'][0, 0], J_WF['x_str'][0, 1],
                                   J_WF['WE'], J_WF['L']])
        partials.declare_partials(x_sigma1,
                                  [x_tc, x_AR, x_Lambda, x_Sref, x_lambda, x_section, x_WE, x_L],
                                  [J_sigma['z'][0, 0], J_sigma['z'][0, 3], J_sigma['z'][0, 4], J_sigma['z'][0, 5],
                                   J_sigma['x_str'][0, 0], J_sigma['x_str'][0, 1],
                                   J_sigma['WE'][0], J_sigma['L'][0]])
        partials.declare_partials(x_sigma2,
                                  [x_tc, x_AR, x_Lambda, x_Sref, x_lambda, x_section, x_WE, x_L],
                                  [J_sigma['z'][1, 0], J_sigma['z'][1, 3], J_sigma['z'][1, 4], J_sigma['z'][1, 5],
                                   J_sigma['x_str'][1, 0], J_sigma['x_str'][1, 1],
                                   J_sigma['WE'][1],J_sigma['L'][1]])
        partials.declare_partials(x_sigma3,
                                  [x_tc, x_AR, x_Lambda, x_Sref, x_lambda, x_section, x_WE, x_L],
                                  [J_sigma['z'][2, 0], J_sigma['z'][2, 3], J_sigma['z'][2, 4], J_sigma['z'][2, 5],
                                   J_sigma['x_str'][2, 0], J_sigma['x_str'][2, 1],
                                   J_sigma['WE'][2], J_sigma['L'][2]])
        partials.declare_partials(x_sigma4,
                                  [x_tc, x_AR, x_Lambda, x_Sref, x_lambda, x_section, x_WE, x_L],
                                  [J_sigma['z'][3, 0], J_sigma['z'][3, 3], J_sigma['z'][3, 4], J_sigma['z'][3, 5],
                                   J_sigma['x_str'][3, 0], J_sigma['x_str'][3, 1],
                                   J_sigma['WE'][3], J_sigma['L'][3]])
        partials.declare_partials(x_sigma5,
                                  [x_tc, x_AR, x_Lambda, x_Sref, x_lambda, x_section, x_WE, x_L],
                                  [J_sigma['z'][4, 0], J_sigma['z'][4, 3], J_sigma['z'][4, 4], J_sigma['z'][4, 5],
                                   J_sigma['x_str'][4, 0], J_sigma['x_str'][4, 1],
                                   J_sigma['WE'][4], J_sigma['L'][4]])
        partials.declare_partials(x_Theta,
                                  [x_tc, x_AR, x_Lambda, x_Sref, x_lambda, x_section, x_WE, x_L],
                                  [J_Theta['z'][0, 0], J_Theta['z'][0, 3], J_Theta['z'][0, 4], J_Theta['z'][0, 5],
                                   J_Theta['x_str'][0, 0], J_Theta['x_str'][0, 1],
                                   J_Theta['WE'], J_Theta['L']])
        partials.write(partials_file)


def structure(x_str, Z, L, WE, NZ, WFO, WO):
    # Structure calculation as taken from the ONERA repository
    # Removed "pf" input and added "NZ", "WFO" and "WO" input
    t = Z[0]*Z[5]/(np.sqrt(abs(Z[5]*Z[3])))
    b = np.sqrt(abs(Z[5]*Z[3]))/2.0
    R = (1.0+2.0*x_str[0])/(3.0*(1.0+x_str[0]))
    Theta = polynomial_function([abs(x_str[1]), b, R, L],
                         [2, 4, 4, 3], [0.25]*4, "twist")

    Fo1 = polynomial_function([x_str[1]], [1], [.008], "Fo1")

    WT_hat = L
    WW = Fo1 * (0.0051 * abs(WT_hat*NZ)**0.557 * \
                abs(Z[5])**0.649 * abs(Z[3])**0.5 * abs(Z[0])**(-0.4) \
                * abs(1.0+x_str[0])**0.1 * (0.1875*abs(Z[5]))**0.1 \
                / abs(np.cos(Z[4]*np.pi/180.)))
    WFW = 5.0/18.0 * abs(Z[5]) * 2.0/3.0 * t * 42.5
    WF = WFW + WFO
    WT = WO + WW + WF + WE
    sigma = 5*[0.]
    sigma[0] = polynomial_function([Z[0], L, x_str[1], b, R], [4, 1, 4, 1, 1], [0.1]*5, "sigma[1]")
    sigma[1] = polynomial_function([Z[0], L, x_str[1], b, R], [4, 1, 4, 1, 1], [0.15]*5, "sigma[2]")
    sigma[2] = polynomial_function([Z[0], L, x_str[1], b, R], [4, 1, 4, 1, 1], [0.2]*5, "sigma[3]")
    sigma[3] = polynomial_function([Z[0], L, x_str[1], b, R], [4, 1, 4, 1, 1], [0.25]*5, "sigma[4]")
    sigma[4] = polynomial_function([Z[0], L, x_str[1], b, R], [4, 1, 4, 1, 1], [0.30]*5, "sigma[5]")
    return Theta, WF, WT, sigma


def structure_partials(inputs, scalers):
    # Aerodynamics partial calculation from ONERA repository
    # Removed self, J, scalers
    # Replaced pf for polynomial_function
    # Get d dictionary as static value
    Z = inputs['z']
    Xstr = inputs['x_str']
    L = inputs['L']
    NZ = inputs['NZ']
    pf_d = get_d_dict()

    # dWT ################################################################
    J_WT = dict()
    Fo1 = polynomial_function([Xstr[1]], [1], [.008], "Fo1")

    dWtdlambda = 0.1 * Fo1 / np.cos(Z[4] * np.pi / 180.) * 0.0051 \
                 * (abs(L) * NZ) ** 0.557 * abs(Z[5]) ** 0.649 \
                 * abs(Z[3]) ** 0.5 * abs(Z[0]) ** (-0.4) \
                 * (1.0 + Xstr[0]) ** -0.9 * (0.1875 * abs(Z[5])) ** 0.1
    A = (0.0051 * abs(L * NZ) ** 0.557 * abs(Z[5]) ** 0.649 \
         * abs(Z[3]) ** 0.5 * abs(Z[0]) ** (-0.4) * abs(1.0 + Xstr[0]) ** 0.1 \
         * (0.1875 * abs(Z[5])) ** 0.1 / abs(np.cos(Z[4] * np.pi / 180.)))

    S_shifted, Ai, Aij = polynomial_function([Xstr[1]], [1], [.008],
                                 "Fo1", deriv=True)
    if Xstr[1] / pf_d['Fo1'][0] >= 0.75 and Xstr[1] / pf_d['Fo1'][0] <= 1.25:
        dSxdx = 1.0 / pf_d['Fo1'][0]
    else:
        dSxdx = 0.0

    dWtdx = A * (Ai[0] * dSxdx \
                 + Aij[0, 0] * dSxdx * S_shifted[0])

    val = np.append(dWtdlambda/scalers['WT']*scalers['lambda'],
                    dWtdx/scalers['WT']*scalers['section'])
    J_WT['x_str'] = np.array([val])
    dWTdtc = -0.4 * Fo1 / np.cos(Z[4] * np.pi / 180.) * 0.0051 \
             * abs(L * NZ) ** 0.557 * abs(Z[5]) ** 0.649 \
             * abs(Z[3]) ** 0.5 * abs(Z[0]) ** (-1.4) * abs(1.0 + Xstr[0]) ** 0.1 \
             * (0.1875 * abs(Z[5])) ** 0.1 + 212.5 / 27. * Z[5] ** (3.0 / 2.0) / np.sqrt(Z[3])
    dWTdh = 0.0
    dWTdM = 0.0
    dWTdAR = 0.5 * Fo1 / np.cos(Z[4] * np.pi / 180.) * 0.0051 \
             * abs(L * NZ) ** 0.557 * abs(Z[5]) ** 0.649 \
             * abs(Z[3]) ** -0.5 * abs(Z[0]) ** (-0.4) * abs(1.0 + Xstr[0]) ** 0.1 \
             * (0.1875 * abs(Z[5])) ** 0.1 + 212.5 / 27. * Z[5] ** (3.0 / 2.0) \
             * Z[0] * -0.5 * Z[3] ** (-3.0 / 2.0)
    dWTdLambda = Fo1 * np.pi / 180. * np.sin(Z[4] * np.pi / 180.) / np.cos(Z[4] * np.pi / 180.) ** 2 \
                 * 0.0051 * abs(L * NZ) ** 0.557 * abs(Z[5]) ** 0.649 \
                 * abs(Z[3]) ** 0.5 * abs(Z[0]) ** (-0.4) * abs(1.0 + Xstr[0]) ** 0.1 \
                 * (0.1875 * abs(Z[5])) ** 0.1
    dWTdSref = 0.749 * Fo1 / np.cos(Z[4] * np.pi / 180.) * 0.1875 ** (0.1) * 0.0051 \
               * abs(L * NZ) ** 0.557 * abs(Z[5]) ** -0.251 \
               * abs(Z[3]) ** 0.5 * abs(Z[0]) ** (-0.4) * abs(1.0 + Xstr[0]) ** 0.1 \
               + 637.5 / 54. * Z[5] ** (0.5) * Z[0] / np.sqrt(Z[3])
    val = np.append(dWTdtc/scalers['WT']*scalers['tc'],
                    [dWTdh/scalers['WT']*scalers['h'],
                     dWTdM/scalers['WT']*scalers['M'],
                     dWTdAR/scalers['WT']*scalers['AR'],
                     dWTdLambda/scalers['WT']*scalers['Lambda'],
                     dWTdSref/scalers['WT']*scalers['Sref']])
    J_WT['z'] = np.array([val])
    dWTdL = 0.557 * Fo1 / np.cos(Z[4] * np.pi / 180.) * 0.0051 * abs(L) ** -0.443 \
            * NZ ** 0.557 * abs(Z[5]) ** 0.649 * abs(Z[3]) ** 0.5 \
            * abs(Z[0]) ** (-0.4) * abs(1.0 + Xstr[0]) ** 0.1 * (0.1875 * abs(Z[5])) ** 0.1
    J_WT['L'] = np.array([[dWTdL]])
    dWTdWE = 1.0
    J_WT['WE'] = np.array([[dWTdWE/scalers['WT']*scalers['WE']]])

    # dWF ################################################################
    J_WF = dict()
    dWFdlambda = 0.0
    dWFdx = 0.0
    val = np.append(dWFdlambda/scalers['WF']*scalers['lambda'],
                    dWFdx/scalers['WF']*scalers['section'])
    J_WF['x_str'] = np.array([val])
    dWFdtc = 212.5 / 27. * Z[5] ** (3.0 / 2.0) / np.sqrt(Z[3])
    dWFdh = 0.0
    dWFdM = 0.0
    dWFdAR = 212.5 / 27. * Z[5] ** (3.0 / 2.0) * Z[0] * -0.5 * Z[3] ** (-3.0 / 2.0)
    dWFdLambda = 0.0
    dWFdSref = 637.5 / 54. * Z[5] ** (0.5) * Z[0] / np.sqrt(Z[3])
    val = np.append(dWFdtc/scalers['WF']*scalers['tc'],
                    [dWFdh/scalers['WF']*scalers['h'],
                     dWFdM/scalers['WF']*scalers['M'],
                     dWFdAR/scalers['WF']*scalers['AR'],
                     dWFdLambda/scalers['WF']*scalers['Lambda'],
                     dWFdSref/scalers['WF']*scalers['Sref']])
    J_WF['z'] = np.array([val])
    dWFdL = 0.0
    J_WF['L'] = np.array([[dWFdL/scalers['WF']*scalers['L']]])
    dWFdWE = 0.0
    J_WF['WE'] = np.array([[dWFdWE/scalers['WF']*scalers['WE']]])

    ### dTheta ###########################################################
    J_Theta = dict()
    b = np.sqrt(abs(Z[5] * Z[3])) / 2.0
    R = (1.0 + 2.0 * Xstr[0]) / (3.0 * (1.0 + Xstr[0]))
    S_shifted, Ai, Aij = polynomial_function([abs(Xstr[1]), b, R, L],
                                 [2, 4, 4, 3],
                                 [0.25] * 4, "twist", deriv=True)
    if R / pf_d['twist'][2] >= 0.75 and R / pf_d['twist'][2] <= 1.25:
        dSRdlambda = 1.0 / pf_d['twist'][2] * 1.0 / (3.0 * (1.0 + Xstr[0]) ** 2)
    else:
        dSRdlambda = 0.0

    dSRdlambda2 = 2.0 * S_shifted[2] * dSRdlambda
    dThetadlambda = Ai[2] * dSRdlambda + 0.5 * Aij[2, 2] * dSRdlambda2 \
                    + Aij[0, 2] * S_shifted[0] * dSRdlambda \
                    + Aij[1, 2] * S_shifted[1] * dSRdlambda \
                    + Aij[3, 2] * S_shifted[3] * dSRdlambda
    if abs(Xstr[1]) / pf_d['twist'][0] >= 0.75 and abs(Xstr[1]) / pf_d['twist'][0] <= 1.25:
        dSxdx = 1.0 / pf_d['twist'][0]
    else:
        dSxdx = 0.0
    dSxdx2 = 2.0 * S_shifted[0] * dSxdx
    dThetadx = Ai[0] * dSxdx + 0.5 * Aij[0, 0] * dSxdx2 \
               + Aij[1, 0] * S_shifted[1] * dSxdx \
               + Aij[2, 0] * S_shifted[2] * dSxdx \
               + Aij[3, 0] * S_shifted[3] * dSxdx
    J_Theta['x_str'] = np.array([np.append(dThetadlambda[0]/scalers['Theta']*scalers['lambda'],
                                              dThetadx[0]/scalers['Theta']*scalers['section'])])
    dThetadtc = 0.0
    dThetadh = 0.0
    dThetadM = 0.0
    if b / pf_d['twist'][1] >= 0.75 and b / pf_d['twist'][1] <= 1.25:
        dSbdAR = 1.0 / pf_d['twist'][1] * (np.sqrt(Z[5]) / 4.0 * Z[3] ** -0.5)
    else:
        dSbdAR = 0.0
    dSbdAR2 = 2.0 * S_shifted[1] * dSbdAR
    dThetadAR = float(Ai[1] * dSbdAR + 0.5 * Aij[1, 1] * dSbdAR2 \
                + Aij[0, 1] * S_shifted[0] * dSbdAR \
                + Aij[2, 1] * S_shifted[2] * dSbdAR \
                + Aij[3, 1] * S_shifted[3] * dSbdAR)
    dThetadLambda = 0.0
    if b / pf_d['twist'][1] >= 0.75 and b / pf_d['twist'][1] <= 1.25:
        dSbdSref = 1.0 / pf_d['twist'][1] * (np.sqrt(Z[3]) / 4.0 * Z[5] ** -0.5)
    else:
        dSbdSref = 0.0
    dSbdSref2 = 2.0 * S_shifted[1] * dSbdSref
    dThetadSref = float(Ai[1] * dSbdSref + 0.5 * Aij[1, 1] * dSbdSref2 \
                  + Aij[0, 1] * S_shifted[0] * dSbdSref \
                  + Aij[2, 1] * S_shifted[2] * dSbdSref \
                  + Aij[3, 1] * S_shifted[3] * dSbdSref)

    J_Theta['z'] = np.array([np.append(dThetadtc/scalers['Theta']*scalers['tc'],
                                          [dThetadh/scalers['Theta']*scalers['h'],
                                           dThetadM/scalers['Theta']*scalers['M'],
                                           dThetadAR/scalers['Theta']*scalers['AR'],
                                           dThetadLambda/scalers['Theta']*scalers['Lambda'],
                                           dThetadSref/scalers['Theta']*scalers['Sref']])])
    if L / pf_d['twist'][3] >= 0.75 and L / pf_d['twist'][3] <= 1.25:
        dSLdL = 1.0 / pf_d['twist'][3]
    else:
        dSLdL = 0.0
    dSLdL2 = 2.0 * S_shifted[3] * dSLdL
    dThetadL = Ai[3] * dSLdL + 0.5 * Aij[3, 3] * dSLdL2 \
               + Aij[0, 3] * S_shifted[0] * dSLdL \
               + Aij[1, 3] * S_shifted[1] * dSLdL \
               + Aij[2, 3] * S_shifted[2] * dSLdL
    J_Theta['L'] = (np.array([[dThetadL/scalers['Theta']*scalers['L']]])).reshape((1, 1))
    dThetadWE = 0.0
    J_Theta['WE'] = np.array([[dThetadWE/scalers['Theta']*scalers['WE']]])

    # dsigma #############################################################
    J_sigma = dict()
    b = np.sqrt(abs(Z[5] * Z[3])) / 2.0
    R = (1.0 + 2.0 * Xstr[0]) / (3.0 * (1.0 + Xstr[0]))
    s_new = [Z[0], L, Xstr[1], b, R]
    S_shifted, Ai, Aij = polynomial_function(s_new,
                                 [4, 1, 4, 1, 1], [0.1] * 5,
                                 "sigma[1]", deriv=True)
    if R / pf_d['sigma[1]'][4] >= 0.75 and R / pf_d['sigma[1]'][4] <= 1.25:
        dSRdlambda = 1.0 / pf_d['sigma[1]'][4] * 1.0 / (3.0 * (1.0 + Xstr[0]) ** 2)
    else:
        dSRdlambda = 0.0
    dSRdlambda2 = 2.0 * S_shifted[4] * dSRdlambda
    dsigma1dlambda = Ai[4] * dSRdlambda + 0.5 * Aij[4, 4] * dSRdlambda2 \
                     + Aij[0, 4] * S_shifted[0] * dSRdlambda \
                     + Aij[1, 4] * S_shifted[1] * dSRdlambda \
                     + Aij[2, 4] * S_shifted[2] * dSRdlambda \
                     + Aij[3, 4] * S_shifted[3] * dSRdlambda
    if Xstr[1] / pf_d['sigma[1]'][2] >= 0.75 and Xstr[1] / pf_d['sigma[1]'][2] <= 1.25:
        dSxdx = 1.0 / pf_d['sigma[1]'][2]
    else:
        dSxdx = 0.0
    dSxdx2 = 2.0 * S_shifted[2] * dSxdx
    dsigma1dx = Ai[2] * dSxdx + 0.5 * Aij[2, 2] * dSxdx2 \
                + Aij[0, 2] * S_shifted[0] * dSxdx \
                + Aij[1, 2] * S_shifted[1] * dSxdx \
                + Aij[3, 2] * S_shifted[3] * dSxdx \
                + Aij[4, 2] * S_shifted[4] * dSxdx

    S_shifted, Ai, Aij = polynomial_function(s_new,
                                 [4, 1, 4, 1, 1], [0.15] * 5,
                                 "sigma[2]", deriv=True)
    if R / pf_d['sigma[2]'][4] >= 0.75 and R / pf_d['sigma[2]'][4] <= 1.25:
        dSRdlambda = 1.0 / pf_d['sigma[2]'][4] * 1.0 / (3.0 * (1.0 + Xstr[0]) ** 2)
    else:
        dSRdlambda = 0.0
    dSRdlambda2 = 2.0 * S_shifted[4] * dSRdlambda
    dsigma2dlambda = Ai[4] * dSRdlambda \
                     + 0.5 * Aij[4, 4] * dSRdlambda2 \
                     + Aij[0, 4] * S_shifted[0] * dSRdlambda \
                     + Aij[1, 4] * S_shifted[1] * dSRdlambda \
                     + Aij[2, 4] * S_shifted[2] * dSRdlambda \
                     + Aij[3, 4] * S_shifted[3] * dSRdlambda
    if Xstr[1] / pf_d['sigma[2]'][2] >= 0.75 and Xstr[1] / pf_d['sigma[2]'][2] <= 1.25:
        dSxdx = 1.0 / pf_d['sigma[2]'][2]
    else:
        dSxdx = 0.0
    dSxdx2 = 2.0 * S_shifted[2] * dSxdx
    dsigma2dx = Ai[2] * dSxdx + 0.5 * Aij[2, 2] * dSxdx2 \
                + Aij[0, 2] * S_shifted[0] * dSxdx \
                + Aij[1, 2] * S_shifted[1] * dSxdx \
                + Aij[3, 2] * S_shifted[3] * dSxdx \
                + Aij[4, 2] * S_shifted[4] * dSxdx

    S_shifted, Ai, Aij = polynomial_function(s_new,
                                 [4, 1, 4, 1, 1], [0.2] * 5,
                                 "sigma[3]", deriv=True)
    if R / pf_d['sigma[3]'][4] >= 0.75 and R / pf_d['sigma[3]'][4] <= 1.25:
        dSRdlambda = 1.0 / pf_d['sigma[3]'][4] * 1.0 / (3.0 * (1.0 + Xstr[0]) ** 2)
    else:
        dSRdlambda = 0.0
    dSRdlambda2 = 2.0 * S_shifted[4] * dSRdlambda
    dsigma3dlambda = Ai[4] * dSRdlambda + 0.5 * Aij[4, 4] * dSRdlambda2 \
                     + Aij[0, 4] * S_shifted[0] * dSRdlambda \
                     + Aij[1, 4] * S_shifted[1] * dSRdlambda \
                     + Aij[2, 4] * S_shifted[2] * dSRdlambda \
                     + Aij[3, 4] * S_shifted[3] * dSRdlambda
    if Xstr[1] / pf_d['sigma[3]'][2] >= 0.75 and Xstr[1] / pf_d['sigma[3]'][2] <= 1.25:
        dSxdx = 1.0 / pf_d['sigma[3]'][2]
    else:
        dSxdx = 0.0
    dSxdx2 = 2.0 * S_shifted[2] * dSxdx
    dsigma3dx = Ai[2] * dSxdx + 0.5 * Aij[2, 2] * dSxdx2 \
                + Aij[0, 2] * S_shifted[0] * dSxdx \
                + Aij[1, 2] * S_shifted[1] * dSxdx \
                + Aij[3, 2] * S_shifted[3] * dSxdx \
                + Aij[4, 2] * S_shifted[4] * dSxdx

    S_shifted, Ai, Aij = polynomial_function(s_new,
                                 [4, 1, 4, 1, 1], [0.25] * 5,
                                 "sigma[4]", deriv=True)
    if R / pf_d['sigma[4]'][4] >= 0.75 and R / pf_d['sigma[4]'][4] <= 1.25:
        dSRdlambda = 1.0 / pf_d['sigma[4]'][4] * 1.0 / (3.0 * (1.0 + Xstr[0]) ** 2)
    else:
        dSRdlambda = 0.0
    dSRdlambda2 = 2.0 * S_shifted[4] * dSRdlambda
    dsigma4dlambda = Ai[4] * dSRdlambda \
                     + 0.5 * Aij[4, 4] * dSRdlambda2 \
                     + Aij[0, 4] * S_shifted[0] * dSRdlambda \
                     + Aij[1, 4] * S_shifted[1] * dSRdlambda \
                     + Aij[2, 4] * S_shifted[2] * dSRdlambda \
                     + Aij[3, 4] * S_shifted[3] * dSRdlambda
    if Xstr[1] / pf_d['sigma[4]'][2] >= 0.75 and Xstr[1] / pf_d['sigma[4]'][2] <= 1.25:
        dSxdx = 1.0 / pf_d['sigma[4]'][2]
    else:
        dSxdx = 0.0
    dSxdx2 = 2.0 * S_shifted[2] * dSxdx
    dsigma4dx = Ai[2] * dSxdx + 0.5 * Aij[2, 2] * dSxdx2 \
                + Aij[0, 2] * S_shifted[0] * dSxdx \
                + Aij[1, 2] * S_shifted[1] * dSxdx \
                + Aij[3, 2] * S_shifted[3] * dSxdx \
                + Aij[4, 2] * S_shifted[4] * dSxdx
    S_shifted, Ai, Aij = polynomial_function(s_new,
                                 [4, 1, 4, 1, 1], [0.3] * 5,
                                 "sigma[5]", deriv=True)
    if R / pf_d['sigma[5]'][4] >= 0.75 and R / pf_d['sigma[5]'][4] <= 1.25:
        dSRdlambda = 1.0 / pf_d['sigma[5]'][4] * 1.0 / (3.0 * (1.0 + Xstr[0]) ** 2)
    else:
        dSRdlambda = 0.0
    dSRdlambda2 = 2.0 * S_shifted[4] * dSRdlambda
    dsigma5dlambda = Ai[4] * dSRdlambda + 0.5 * Aij[4, 4] * dSRdlambda2 \
                     + Aij[0, 4] * S_shifted[0] * dSRdlambda \
                     + Aij[1, 4] * S_shifted[1] * dSRdlambda \
                     + Aij[2, 4] * S_shifted[2] * dSRdlambda \
                     + Aij[3, 4] * S_shifted[3] * dSRdlambda
    if Xstr[1] / pf_d['sigma[5]'][2] >= 0.75 and Xstr[1] / pf_d['sigma[5]'][2] <= 1.25:
        dSxdx = 1.0 / pf_d['sigma[5]'][2]
    else:
        dSxdx = 0.0
    dSxdx2 = 2.0 * S_shifted[2] * dSxdx
    dsigma5dx = Ai[2] * dSxdx + 0.5 * Aij[2, 2] * dSxdx2 \
                + Aij[0, 2] * S_shifted[0] * dSxdx \
                + Aij[1, 2] * S_shifted[1] * dSxdx \
                + Aij[3, 2] * S_shifted[3] * dSxdx \
                + Aij[4, 2] * S_shifted[4] * dSxdx

    J_sigma['x_str'] = np.array(
        [[dsigma1dlambda[0]/scalers['sigma1']*scalers['lambda'],
          dsigma1dx[0]/scalers['sigma1']*scalers['section']],
         [dsigma2dlambda[0]/scalers['sigma2']*scalers['lambda'],
          dsigma2dx[0]/scalers['sigma2']*scalers['section']],
         [dsigma3dlambda[0]/scalers['sigma3']*scalers['lambda'],
          dsigma3dx[0]/scalers['sigma3']*scalers['section']],
         [dsigma4dlambda[0]/scalers['sigma4']*scalers['lambda'],
          dsigma4dx[0]/scalers['sigma4']*scalers['section']],
         [dsigma5dlambda[0]/scalers['sigma5']*scalers['lambda'],
          dsigma5dx[0]/scalers['sigma5']*scalers['section']]])

    S_shifted, Ai, Aij = polynomial_function(s_new,
                                 [4, 1, 4, 1, 1], [0.1] * 5,
                                 "sigma[1]", deriv=True)
    if Z[0] / pf_d['sigma[1]'][0] >= 0.75 and Z[0] / pf_d['sigma[1]'][0] <= 1.25:
        dStcdtc = 1.0 / pf_d['sigma[1]'][0]
    else:
        dStcdtc = 0.0
    dStcdtc2 = 2.0 * S_shifted[0] * dStcdtc
    dsigma1dtc = Ai[0] * dStcdtc + 0.5 * Aij[0, 0] * dStcdtc2 \
                 + Aij[1, 0] * S_shifted[1] * dStcdtc \
                 + Aij[2, 0] * S_shifted[2] * dStcdtc \
                 + Aij[3, 0] * S_shifted[3] * dStcdtc \
                 + Aij[4, 0] * S_shifted[4] * dStcdtc
    dsigma1dh = 0.0
    dsigma1dM = 0.0
    if b / pf_d['sigma[1]'][3] >= 0.75 and b / pf_d['sigma[1]'][3] <= 1.25:
        dSbdAR = 1.0 / pf_d['sigma[1]'][3] * (np.sqrt(Z[5]) / 4.0 * Z[3] ** -0.5)
        dSbdSref = 1.0 / pf_d['sigma[1]'][3] * (np.sqrt(Z[3]) / 4.0 * Z[5] ** -0.5)
    else:
        dSbdAR = 0.0
        dSbdSref = 0.0
    dSbdAR2 = 2.0 * S_shifted[3] * dSbdAR
    dsigma1dAR = Ai[3] * dSbdAR + 0.5 * Aij[3, 3] * dSbdAR2 \
                 + Aij[0, 3] * S_shifted[0] * dSbdAR \
                 + Aij[1, 3] * S_shifted[1] * dSbdAR \
                 + Aij[2, 3] * S_shifted[2] * dSbdAR \
                 + Aij[4, 3] * S_shifted[4] * dSbdAR
    dsigma1dLambda = 0.0
    dSbdSref2 = 2.0 * S_shifted[3] * dSbdSref
    dsigma1dSref = Ai[3] * dSbdSref + 0.5 * Aij[3, 3] * dSbdSref2 \
                   + Aij[0, 3] * S_shifted[0] * dSbdSref \
                   + Aij[1, 3] * S_shifted[1] * dSbdSref \
                   + Aij[2, 3] * S_shifted[2] * dSbdSref \
                   + Aij[4, 3] * S_shifted[4] * dSbdSref
    S_shifted, Ai, Aij = polynomial_function(s_new,
                                 [4, 1, 4, 1, 1], [0.15] * 5,
                                 "sigma[2]", deriv=True)

    if Z[0] / pf_d['sigma[2]'][0] >= 0.75 and Z[0] / pf_d['sigma[2]'][0] <= 1.25:
        dStcdtc = 1.0 / pf_d['sigma[2]'][0]
    else:
        dStcdtc = 0.0
    dStcdtc2 = 2.0 * S_shifted[0] * dStcdtc
    dsigma2dtc = Ai[0] * dStcdtc + 0.5 * Aij[0, 0] * dStcdtc2 \
                 + Aij[1, 0] * S_shifted[1] * dStcdtc \
                 + Aij[2, 0] * S_shifted[2] * dStcdtc \
                 + Aij[3, 0] * S_shifted[3] * dStcdtc \
                 + Aij[4, 0] * S_shifted[4] * dStcdtc
    dsigma2dh = 0.0
    dsigma2dM = 0.0
    if b / pf_d['sigma[2]'][3] >= 0.75 and b / pf_d['sigma[2]'][3] <= 1.25:
        dSbdAR = 1.0 / pf_d['sigma[2]'][3] * (np.sqrt(Z[5]) / 4.0 * Z[3] ** -0.5)
        dSbdSref = 1.0 / pf_d['sigma[2]'][3] * (np.sqrt(Z[3]) / 4.0 * Z[5] ** -0.5)
    else:
        dSbdAR = 0.0
        dSbdSref = 0.0
    dSbdAR2 = 2.0 * S_shifted[3] * dSbdAR
    dsigma2dAR = Ai[3] * dSbdAR + 0.5 * Aij[3, 3] * dSbdAR2 \
                 + Aij[0, 3] * S_shifted[0] * dSbdAR \
                 + Aij[1, 3] * S_shifted[1] * dSbdAR \
                 + Aij[2, 3] * S_shifted[2] * dSbdAR \
                 + Aij[4, 3] * S_shifted[4] * dSbdAR
    dsigma2dLambda = 0.0
    dSbdSref2 = 2.0 * S_shifted[3] * dSbdSref
    dsigma2dSref = Ai[3] * dSbdSref + 0.5 * Aij[3, 3] * dSbdSref2 \
                   + Aij[0, 3] * S_shifted[0] * dSbdSref \
                   + Aij[1, 3] * S_shifted[1] * dSbdSref \
                   + Aij[2, 3] * S_shifted[2] * dSbdSref \
                   + Aij[4, 3] * S_shifted[4] * dSbdSref

    S_shifted, Ai, Aij = polynomial_function(s_new,
                                 [4, 1, 4, 1, 1], [0.20] * 5,
                                 "sigma[3]", deriv=True)
    if Z[0] / pf_d['sigma[3]'][0] >= 0.75 and Z[0] / pf_d['sigma[3]'][0] <= 1.25:
        dStcdtc = 1.0 / pf_d['sigma[3]'][0]
    else:
        dStcdtc = 0.0
    dStcdtc2 = 2.0 * S_shifted[0] * dStcdtc
    dsigma3dtc = Ai[0] * dStcdtc + 0.5 * Aij[0, 0] * dStcdtc2 \
                 + Aij[1, 0] * S_shifted[1] * dStcdtc \
                 + Aij[2, 0] * S_shifted[2] * dStcdtc \
                 + Aij[3, 0] * S_shifted[3] * dStcdtc \
                 + Aij[4, 0] * S_shifted[4] * dStcdtc
    dsigma3dh = 0.0
    dsigma3dM = 0.0
    if b / pf_d['sigma[3]'][3] >= 0.75 and b / pf_d['sigma[3]'][3] <= 1.25:
        dSbdAR = 1.0 / pf_d['sigma[3]'][3] * (np.sqrt(Z[5]) / 4.0 * Z[3] ** -0.5)
        dSbdSref = 1.0 / pf_d['sigma[3]'][3] * (np.sqrt(Z[3]) / 4.0 * Z[5] ** -0.5)
    else:
        dSbdAR = 0.0
        dSbdSref = 0.0
    dSbdAR2 = 2.0 * S_shifted[3] * dSbdAR
    dsigma3dAR = Ai[3] * dSbdAR + 0.5 * Aij[3, 3] * dSbdAR2 \
                 + Aij[0, 3] * S_shifted[0] * dSbdAR \
                 + Aij[1, 3] * S_shifted[1] * dSbdAR \
                 + Aij[2, 3] * S_shifted[2] * dSbdAR \
                 + Aij[4, 3] * S_shifted[4] * dSbdAR
    dsigma3dLambda = 0.0
    dSbdSref2 = 2.0 * S_shifted[3] * dSbdSref
    dsigma3dSref = Ai[3] * dSbdSref + 0.5 * Aij[3, 3] * dSbdSref2 \
                   + Aij[0, 3] * S_shifted[0] * dSbdSref \
                   + Aij[1, 3] * S_shifted[1] * dSbdSref \
                   + Aij[2, 3] * S_shifted[2] * dSbdSref \
                   + Aij[4, 3] * S_shifted[4] * dSbdSref

    S_shifted, Ai, Aij = polynomial_function(s_new,
                                 [4, 1, 4, 1, 1], [0.25] * 5,
                                 "sigma[4]", deriv=True)
    if Z[0] / pf_d['sigma[4]'][0] >= 0.75 and Z[0] / pf_d['sigma[4]'][0] <= 1.25:
        dStcdtc = 1.0 / pf_d['sigma[4]'][0]
    else:
        dStcdtc = 0.0
    dStcdtc2 = 2.0 * S_shifted[0] * dStcdtc
    dsigma4dtc = Ai[0] * dStcdtc + 0.5 * Aij[0, 0] * dStcdtc2 \
                 + Aij[1, 0] * S_shifted[1] * dStcdtc \
                 + Aij[2, 0] * S_shifted[2] * dStcdtc \
                 + Aij[3, 0] * S_shifted[3] * dStcdtc \
                 + Aij[4, 0] * S_shifted[4] * dStcdtc
    dsigma4dh = 0.0
    dsigma4dM = 0.0
    if b / pf_d['sigma[4]'][3] >= 0.75 and b / pf_d['sigma[4]'][3] <= 1.25:
        dSbdAR = 1.0 / pf_d['sigma[4]'][3] * (np.sqrt(Z[5]) / 4.0 * Z[3] ** -0.5)
        dSbdSref = 1.0 / pf_d['sigma[4]'][3] * (np.sqrt(Z[3]) / 4.0 * Z[5] ** -0.5)
    else:
        dSbdAR = 0.0
        dSbdSref = 0.0
    dSbdAR2 = 2.0 * S_shifted[3] * dSbdAR
    dsigma4dAR = Ai[3] * dSbdAR + 0.5 * Aij[3, 3] * dSbdAR2 \
                 + Aij[0, 3] * S_shifted[0] * dSbdAR \
                 + Aij[1, 3] * S_shifted[1] * dSbdAR \
                 + Aij[2, 3] * S_shifted[2] * dSbdAR \
                 + Aij[4, 3] * S_shifted[4] * dSbdAR
    dsigma4dLambda = 0.0
    dSbdSref2 = 2.0 * S_shifted[3] * dSbdSref
    dsigma4dSref = Ai[3] * dSbdSref + 0.5 * Aij[3, 3] * dSbdSref2 \
                   + Aij[0, 3] * S_shifted[0] * dSbdSref \
                   + Aij[1, 3] * S_shifted[1] * dSbdSref \
                   + Aij[2, 3] * S_shifted[2] * dSbdSref \
                   + Aij[4, 3] * S_shifted[4] * dSbdSref

    S_shifted, Ai, Aij = polynomial_function(s_new,
                                 [4, 1, 4, 1, 1], [0.3] * 5,
                                 "sigma[5]", deriv=True)
    if Z[0] / pf_d['sigma[5]'][0] >= 0.75 and Z[0] / pf_d['sigma[5]'][0] <= 1.25:
        dStcdtc = 1.0 / pf_d['sigma[5]'][0]
    else:
        dStcdtc = 0.0
    dStcdtc2 = 2.0 * S_shifted[0] * dStcdtc
    dsigma5dtc = Ai[0] * dStcdtc + 0.5 * Aij[0, 0] * dStcdtc2 \
                 + Aij[1, 0] * S_shifted[1] * dStcdtc \
                 + Aij[2, 0] * S_shifted[2] * dStcdtc \
                 + Aij[3, 0] * S_shifted[3] * dStcdtc \
                 + Aij[4, 0] * S_shifted[4] * dStcdtc
    dsigma5dh = 0.0
    dsigma5dM = 0.0
    if b / pf_d['sigma[5]'][3] >= 0.75 and b / pf_d['sigma[5]'][3] <= 1.25:
        dSbdAR = 1.0 / pf_d['sigma[5]'][3] * (np.sqrt(Z[5]) / 4.0 * Z[3] ** -0.5)
        dSbdSref = 1.0 / pf_d['sigma[5]'][3] * (np.sqrt(Z[3]) / 4.0 * Z[5] ** -0.5)
    else:
        dSbdAR = 0.0
        dSbdSref = 0.0
    dSbdAR2 = 2.0 * S_shifted[3] * dSbdAR
    dsigma5dAR = Ai[3] * dSbdAR + 0.5 * Aij[3, 3] * dSbdAR2 \
                 + Aij[0, 3] * S_shifted[0] * dSbdAR \
                 + Aij[1, 3] * S_shifted[1] * dSbdAR \
                 + Aij[2, 3] * S_shifted[2] * dSbdAR \
                 + Aij[4, 3] * S_shifted[4] * dSbdAR
    dsigma5dLambda = 0.0
    dSbdSref2 = 2.0 * S_shifted[3] * dSbdSref
    dsigma5dSref = Ai[3] * dSbdSref + 0.5 * Aij[3, 3] * dSbdSref2 \
                   + Aij[0, 3] * S_shifted[0] * dSbdSref \
                   + Aij[1, 3] * S_shifted[1] * dSbdSref \
                   + Aij[2, 3] * S_shifted[2] * dSbdSref \
                   + Aij[4, 3] * S_shifted[4] * dSbdSref

    J_sigma['z'] = np.array(
        [[dsigma1dtc[0]/scalers['sigma1']*scalers['tc'],
          dsigma1dh/scalers['sigma1']*scalers['h'],
          dsigma1dM/scalers['sigma1']*scalers['M'],
          dsigma1dAR[0]/scalers['sigma1']*scalers['AR'],
          dsigma1dLambda/scalers['sigma1']*scalers['Lambda'],
          dsigma1dSref[0]/scalers['sigma1']*scalers['Sref']],
         [dsigma2dtc[0]/scalers['sigma2']*scalers['tc'],
          dsigma2dh/scalers['sigma2']*scalers['h'],
          dsigma2dM/scalers['sigma2']*scalers['M'],
          dsigma2dAR[0]/scalers['sigma2']*scalers['AR'],
          dsigma2dLambda/scalers['sigma2']*scalers['Lambda'],
          dsigma2dSref[0]/scalers['sigma2']*scalers['Sref']],
         [dsigma3dtc[0]/scalers['sigma3']*scalers['tc'],
          dsigma3dh/scalers['sigma3']*scalers['h'],
          dsigma3dM/scalers['sigma3']*scalers['M'],
          dsigma3dAR[0]/scalers['sigma3']*scalers['AR'],
          dsigma3dLambda/scalers['sigma3']*scalers['Lambda'],
          dsigma3dSref[0]/scalers['sigma3']*scalers['Sref']],
         [dsigma4dtc[0]/scalers['sigma4']*scalers['tc'],
          dsigma4dh/scalers['sigma4']*scalers['h'],
          dsigma4dM/scalers['sigma4']*scalers['M'],
          dsigma4dAR[0]/scalers['sigma4']*scalers['AR'],
          dsigma4dLambda/scalers['sigma4']*scalers['Lambda'],
          dsigma4dSref[0]/scalers['sigma4']*scalers['Sref']],
         [dsigma5dtc[0]/scalers['sigma5']*scalers['tc'],
          dsigma5dh/scalers['sigma5']*scalers['h'],
          dsigma5dM/scalers['sigma5']*scalers['M'],
          dsigma5dAR[0]/scalers['sigma5']*scalers['AR'],
          dsigma5dLambda/scalers['sigma5']*scalers['Lambda'],
          dsigma5dSref[0]/scalers['sigma5']*scalers['Sref']]])

    # dS #################################################################
    S_shifted, Ai, Aij = polynomial_function([Z[0], L, Xstr[1], b, R],
                                 [4, 1, 4, 1, 1], [0.1] * 5,
                                 "sigma[1]", deriv=True)
    if L / pf_d['sigma[1]'][1] >= 0.75 and L / pf_d['sigma[1]'][1] <= 1.25:
        dSLdL = 1.0 / pf_d['sigma[1]'][1]
    else:
        dSLdL = 0.0
    dSLdL2 = 2.0 * S_shifted[1] * dSLdL
    dsigma1dL = Ai[1] * dSLdL + 0.5 * Aij[1, 1] * dSLdL2 \
                + Aij[0, 1] * S_shifted[0] * dSLdL \
                + Aij[2, 1] * S_shifted[2] * dSLdL \
                + Aij[3, 1] * S_shifted[3] * dSLdL \
                + Aij[4, 1] * S_shifted[4] * dSLdL

    S_shifted, Ai, Aij = polynomial_function(s_new,
                                 [4, 1, 4, 1, 1], [0.15] * 5,
                                 "sigma[2]", deriv=True)
    if L / pf_d['sigma[2]'][1] >= 0.75 and L / pf_d['sigma[2]'][1] <= 1.25:
        dSLdL = 1.0 / pf_d['sigma[2]'][1]
    else:
        dSLdL = 0.0
    dSLdL2 = 2.0 * S_shifted[1] * dSLdL
    dsigma2dL = Ai[1] * dSLdL + 0.5 * Aij[1, 1] * dSLdL2 \
                + Aij[0, 1] * S_shifted[0] * dSLdL \
                + Aij[2, 1] * S_shifted[2] * dSLdL \
                + Aij[3, 1] * S_shifted[3] * dSLdL \
                + Aij[4, 1] * S_shifted[4] * dSLdL

    S_shifted, Ai, Aij = polynomial_function(s_new,
                                 [4, 1, 4, 1, 1], [0.2] * 5,
                                 "sigma[3]", deriv=True)
    if L / pf_d['sigma[3]'][1] >= 0.75 and L / pf_d['sigma[3]'][1] <= 1.25:
        dSLdL = 1.0 / pf_d['sigma[3]'][1]
    else:
        dSLdL = 0.0
    dSLdL2 = 2.0 * S_shifted[1] * dSLdL
    dsigma3dL = Ai[1] * dSLdL + 0.5 * Aij[1, 1] * dSLdL2 \
                + Aij[0, 1] * S_shifted[0] * dSLdL \
                + Aij[2, 1] * S_shifted[2] * dSLdL \
                + Aij[3, 1] * S_shifted[3] * dSLdL \
                + Aij[4, 1] * S_shifted[4] * dSLdL

    S_shifted, Ai, Aij = polynomial_function(s_new,
                                 [4, 1, 4, 1, 1], [0.25] * 5,
                                 "sigma[4]", deriv=True)
    if L / pf_d['sigma[4]'][1] >= 0.75 and L / pf_d['sigma[4]'][1] <= 1.25:
        dSLdL = 1.0 / pf_d['sigma[4]'][1]
    else:
        dSLdL = 0.0
    dSLdL2 = 2.0 * S_shifted[1] * dSLdL
    dsigma4dL = Ai[1] * dSLdL + 0.5 * Aij[1, 1] * dSLdL2 \
                + Aij[0, 1] * S_shifted[0] * dSLdL \
                + Aij[2, 1] * S_shifted[2] * dSLdL \
                + Aij[3, 1] * S_shifted[3] * dSLdL \
                + Aij[4, 1] * S_shifted[4] * dSLdL

    S_shifted, Ai, Aij = polynomial_function(s_new,
                                 [4, 1, 4, 1, 1], [0.3] * 5,
                                 "sigma[5]", deriv=True)
    if L / pf_d['sigma[5]'][1] >= 0.75 and L / pf_d['sigma[5]'][1] <= 1.25:
        dSLdL = 1.0 / pf_d['sigma[5]'][1]
    else:
        dSLdL = 0.0
    dSLdL2 = 2.0 * S_shifted[1] * dSLdL
    dsigma5dL = Ai[1] * dSLdL + 0.5 * Aij[1, 1] * dSLdL2 \
                + Aij[0, 1] * S_shifted[0] * dSLdL \
                + Aij[2, 1] * S_shifted[2] * dSLdL \
                + Aij[3, 1] * S_shifted[3] * dSLdL \
                + Aij[4, 1] * S_shifted[4] * dSLdL

    J_sigma['L'] = np.array(
        [[dsigma1dL/scalers['sigma1']*scalers['L']],
         [dsigma2dL/scalers['sigma2']*scalers['L']],
         [dsigma3dL/scalers['sigma3']*scalers['L']],
         [dsigma4dL/scalers['sigma4']*scalers['L']],
         [dsigma5dL/scalers['sigma5']*scalers['L']]]).reshape((5, 1))

    J_sigma['WE'] = np.zeros((5, 1))

    return J_WT, J_WF, J_sigma, J_Theta


if __name__ == "__main__":

    analysis = Structures()
    # run_tool(analysis, sys.argv)
    inputs = dict(z=np.array([5.00000000e-02,
                              4.5e+04,
                              1.6,
                              5.5,
                              55.,
                              1.0e+03]),
                  x_str=np.array([0.25, 1.0]),
                  x_aer=np.array([1.]),
                  x_pro=0.5,
                  fin=4.093062,
                  D=5572.5217226,
                  DT=0.162151493275,
                  L=49909.58578,
                  R=528.91363,
                  WE=6354.07017266,
                  WF=7306.20261,
                  WT=49909.58578,
                  WBE=4360.,
                  WFO=2000.,
                  WO=25000.,
                  Theta=1.0,
                  ESF=1.0,
                  sigma1=0.93390994,
                  sigma2=0.95593996,
                  sigma3=0.96695497,
                  sigma4=0.97356398,
                  sigma5=0.97796998,
                  SFC=1.12328,
                  Temp=1.0,
                  NZ=6.0,
                  CDMIN=0.01375,
                  dpdx=1.)
    structure_partials(inputs)
