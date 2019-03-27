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

from kadmos.utilities.xml_utils_openlego import xml_safe_create_element
from openlego.partials.partials import Partials

from ssbjkadmos.config import root_tag, x_tc, x_h, x_M, x_AR, x_Lambda, x_Sref, x_WT, x_ESF, x_Theta, x_Cf, \
    x_L, x_D, x_fin, x_dpdx, x_CDmin
from ssbjkadmos.tools.SsbjDiscipline import SsbjDiscipline
from ssbjkadmos.utils.execution import run_tool
from ssbjkadmos.utils.general import get_float_value
from ssbjkadmos.utils.math import polynomial_function, get_d_dict


class Aerodynamics(SsbjDiscipline):  # AbstractDiscipline

    @property
    def description(self):
        return u'Aerodynamic analysis discipline of the SSBJ test case.'

    @property
    def supplies_partials(self):
        return True

    def generate_input_xml(self):
        root = etree.Element(root_tag)
        doc = etree.ElementTree(root)

        xml_safe_create_element(doc, x_tc, self.get_scaler(x_tc))
        xml_safe_create_element(doc, x_h, self.get_scaler(x_h))
        xml_safe_create_element(doc, x_M, self.get_scaler(x_M))
        xml_safe_create_element(doc, x_AR, self.get_scaler(x_AR))
        xml_safe_create_element(doc, x_Lambda, self.get_scaler(x_Lambda))
        xml_safe_create_element(doc, x_Sref, self.get_scaler(x_Sref))
        xml_safe_create_element(doc, x_WT, self.get_scaler(x_WT))
        xml_safe_create_element(doc, x_ESF, self.get_scaler(x_ESF))
        xml_safe_create_element(doc, x_Theta, self.get_scaler(x_Theta))
        xml_safe_create_element(doc, x_Cf, self.get_scaler(x_Cf))
        xml_safe_create_element(doc, x_CDmin, 0.01375)

        return etree.tostring(doc, encoding='utf-8', pretty_print=True, xml_declaration=True)

    def generate_output_xml(self):
        root = etree.Element(root_tag)
        doc = etree.ElementTree(root)

        xml_safe_create_element(doc, x_L, self.get_scaler(x_L))
        xml_safe_create_element(doc, x_D, self.get_scaler(x_D))
        xml_safe_create_element(doc, x_fin, self.get_scaler(x_fin))
        xml_safe_create_element(doc, x_dpdx, self.get_scaler(x_dpdx))

        return etree.tostring(doc, encoding='utf-8', pretty_print=True, xml_declaration=True)

    def generate_partials_xml(self):
        partials = Partials()
        partials.declare_partials(x_L, [x_tc, x_h, x_M, x_AR, x_Lambda, x_Sref, x_WT, x_ESF, x_Theta, x_Cf])
        partials.declare_partials(x_D, [x_tc, x_h, x_M, x_AR, x_Lambda, x_Sref, x_WT, x_ESF, x_Theta, x_Cf])
        partials.declare_partials(x_fin, [x_tc, x_h, x_M, x_AR, x_Lambda, x_Sref, x_WT, x_ESF, x_Theta, x_Cf])
        partials.declare_partials(x_dpdx, [x_tc, x_h, x_M, x_AR, x_Lambda, x_Sref, x_WT, x_ESF, x_Theta, x_Cf])
        return partials.get_string()

    def execute(self, in_file, out_file):
        doc = etree.parse(in_file)
        z0 = self.unscale_float_value(x_tc, doc)
        z1 = self.unscale_float_value(x_h, doc)
        z2 = self.unscale_float_value(x_M, doc)
        z3 = self.unscale_float_value(x_AR, doc)
        z4 = self.unscale_float_value(x_Lambda, doc)
        z5 = self.unscale_float_value(x_Sref, doc)
        WT = self.unscale_float_value(x_WT, doc)
        ESF = self.unscale_float_value(x_ESF, doc)
        Theta = self.unscale_float_value(x_Theta, doc)
        x_aer = self.unscale_float_value(x_Cf, doc)
        CDMIN = get_float_value(x_CDmin, doc)

        L, D, fin, dpdx = aerodynamics(x_aer, np.array([z0, z1, z2, z3, z4, z5]), WT, ESF, Theta, CDMIN)

        root = etree.Element(root_tag)
        doc = etree.ElementTree(root)
        xml_safe_create_element(doc, x_L, self.scale_value(L, x_L))
        xml_safe_create_element(doc, x_D, self.scale_value(D, x_D))
        xml_safe_create_element(doc, x_fin, self.scale_value(fin, x_fin))
        xml_safe_create_element(doc, x_dpdx, self.scale_value(dpdx, x_dpdx))
        doc.write(out_file, encoding='utf-8', pretty_print=True, xml_declaration=True)

    def linearize(self, in_file, partials_file):
        doc = etree.parse(in_file)
        z0 = self.unscale_float_value(x_tc, doc)
        z1 = self.unscale_float_value(x_h, doc)
        z2 = self.unscale_float_value(x_M, doc)
        z3 = self.unscale_float_value(x_AR, doc)
        z4 = self.unscale_float_value(x_Lambda, doc)
        z5 = self.unscale_float_value(x_Sref, doc)
        WT = self.unscale_float_value(x_WT, doc)
        ESF = self.unscale_float_value(x_ESF, doc)
        Theta = self.unscale_float_value(x_Theta, doc)
        x_aer = self.unscale_float_value(x_Cf, doc)
        CDMIN = get_float_value(x_CDmin, doc)

        # Execute ONERA partials function
        J_L, J_D, J_fin, J_dpdx = aerodynamics_partials(inputs=dict(z=np.array([z0, z1, z2, z3, z4, z5]),
                                                                    x_aer=x_aer,
                                                                    WT=WT, ESF=ESF, Theta=Theta,
                                                                    CDMIN=CDMIN),
                                                        scalers=self.scalers)

        # Declare and write partials
        partials = Partials()
        partials.declare_partials(x_L,
                                  [x_tc, x_h, x_M, x_AR, x_Lambda, x_Sref, x_WT, x_ESF, x_Theta, x_Cf],
                                  [J_L['z'][0,0],J_L['z'][0,1],J_L['z'][0,2],J_L['z'][0,3],J_L['z'][0,4],J_L['z'][0,5],
                                   J_L['WT'][0],J_L['ESF'][0],J_L['Theta'][0], J_L['x_aer'][0]])
        partials.declare_partials(x_D,
                                  [x_tc, x_h, x_M, x_AR, x_Lambda, x_Sref, x_WT, x_ESF, x_Theta, x_Cf],
                                  [J_D['z'][0, 0], J_D['z'][0, 1], J_D['z'][0, 2], J_D['z'][0, 3], J_D['z'][0, 4],
                                   J_D['z'][0, 5],
                                   J_D['WT'][0], J_D['ESF'][0], J_D['Theta'][0], J_D['x_aer'][0]])
        partials.declare_partials(x_fin,
                                  [x_tc, x_h, x_M, x_AR, x_Lambda, x_Sref, x_WT, x_ESF, x_Theta, x_Cf],
                                  [J_fin['z'][0, 0], J_fin['z'][0, 1], J_fin['z'][0, 2], J_fin['z'][0, 3], J_fin['z'][0, 4],
                                   J_fin['z'][0, 5],
                                   J_fin['WT'][0], J_fin['ESF'][0], J_fin['Theta'][0], J_fin['x_aer'][0]])
        partials.declare_partials(x_dpdx,
                                  [x_tc, x_h, x_M, x_AR, x_Lambda, x_Sref, x_WT, x_ESF, x_Theta, x_Cf],
                                  [J_dpdx['z'][0, 0], J_dpdx['z'][0, 1], J_dpdx['z'][0, 2], J_dpdx['z'][0, 3], J_dpdx['z'][0, 4],
                                   J_dpdx['z'][0, 5],
                                   J_dpdx['WT'][0], J_dpdx['ESF'][0], J_dpdx['Theta'][0], J_dpdx['x_aer'][0]])
        partials.write(partials_file)


def aerodynamics(x_aer, Z, WT, ESF, Theta, CDMIN):
    # Aerodynamics calculation as taken from the ONERA repository
    # Removed "pf" input and added "CDMIN" input
    if Z[1] <= 36089.0:
        V = 1116.39 * Z[2] * np.sqrt(abs(1.0 - 6.875E-6*Z[1]))
        rho = 2.377E-3 * (1. - 6.875E-6*Z[1])**4.2561
    else:
        V = 968.1 * abs(Z[2])
        rho = 2.377E-3 * 0.2971 * np.exp((36089.0 - Z[1]) / 20806.7)
    CL = WT / (0.5*rho*(V**2)*Z[5])
    Fo2 = polynomial_function([ESF, abs(x_aer)], [1, 1], [.25]*2, "Fo2")

    CDmin = CDMIN*Fo2 + 3.05*abs(Z[0])**(5.0/3.0) \
            * abs(np.cos(Z[4]*np.pi/180.0))**1.5
    if Z[2] >= 1.:
        k = abs(Z[3]) * (abs(Z[2])**2-1.0) * np.cos(Z[4]*np.pi/180.) \
        / (4.* abs(Z[3])* np.sqrt(abs(Z[4]**2 - 1.) - 2.))
    else:
        k = (0.8 * np.pi * abs(Z[3]))**-1

    Fo3 = polynomial_function([Theta], [5], [.25], "Fo3")
    CD = (CDmin + k * CL**2) * Fo3
    D = CD * 0.5 * rho * V**2 * Z[5]
    fin = WT/D
    L = WT
    dpdx = polynomial_function([Z[0]], [1], [.25], "dpdx")

    return L, D, fin, dpdx


def aerodynamics_partials(inputs, scalers):
    # Aerodynamics partial calculation from ONERA repository
    # Removed self, J, scalers
    # Replaced pf for polynomial_function
    # Get d dictionary as static value
    Z = inputs['z']
    WT = inputs['WT']
    ESF = inputs['ESF']
    Theta = inputs['Theta']
    CDMIN = inputs['CDMIN']
    pf_d = get_d_dict()

    # auxiliary computations
    if Z[1] <= 36089.0:
        V = 1116.39 * Z[2] * np.sqrt(abs(1.0 - 6.875E-6 * Z[1]))
        rho = 2.377E-3 * (1. - 6.875E-6 * Z[1]) ** 4.2561
    else:
        V = 968.1 * abs(Z[2])
        rho = 2.377E-3 * 0.2971 * np.exp((36089.0 - Z[1]) / 20806.7)
    CL = WT / (0.5 * rho * (V ** 2) * Z[5])
    s_new = [ESF, abs(inputs['x_aer'])]
    Fo2 = polynomial_function(s_new, [1, 1], [.25] * 2, "Fo2")

    CDmin = CDMIN * Fo2 + 3.05 * abs(Z[0]) ** (5.0 / 3.0) \
            * abs(np.cos(Z[4] * np.pi / 180.0)) ** 1.5
    if Z[2] >= 1.:
        k = abs(Z[3]) * (abs(Z[2]) ** 2 - 1.0) * np.cos(Z[4] * np.pi / 180.) \
            / (4. * abs(Z[3]) * np.sqrt(abs(Z[4] ** 2 - 1.) - 2.))
    else:
        k = (0.8 * np.pi * abs(Z[3])) ** -1

    Fo3 = polynomial_function([Theta], [5], [.25], "Fo3")
    CD = (CDmin + k * CL ** 2) * Fo3
    D = CD * 0.5 * rho * V ** 2 * Z[5]

    # dL #################################################################
    J_L = dict()
    J_L['x_aer'] = np.array([[0.0]])
    J_L['z'] = np.zeros((1, 6))
    J_L['WT'] = np.array([[1.0]])
    J_L['Theta'] = np.array([[0.0]])
    J_L['ESF'] = np.array([[0.0]])

    # dD #################################################################
    J_D = dict()
    S_shifted, Ai, Aij = polynomial_function(s_new,
                                 [1, 1], [.25] * 2, "Fo2", deriv=True)
    if abs(inputs['x_aer']) / pf_d['Fo2'][1] >= 0.75 and \
            abs(inputs['x_aer']) / pf_d['Fo2'][1] <= 1.25:
        dSCfdCf = 1.0 / pf_d['Fo2'][1]
    else:
        dSCfdCf = 0.0
    dSCfdCf2 = 2.0 * S_shifted[1] * dSCfdCf
    dFo1dCf = Ai[1] * dSCfdCf + 0.5 * Aij[1, 1] * dSCfdCf2 + Aij[0, 1] * S_shifted[1] * dSCfdCf
    dDdCf = 0.5 * rho * V ** 2 * Z[5] * Fo3 * CDMIN * dFo1dCf
    J_D['x_aer'] = np.array([[dDdCf/scalers['D']*scalers['Cf']]]).reshape((1, 1))
    dDdtc = 0.5 * rho * V ** 2 * Z[5] * 5.0 / 3.0 * 3.05 * Fo3 * Z[0] ** (2. / 3.) * np.cos(Z[4] * np.pi / 180.) ** (
                3. / 2.)
    if Z[1] <= 36089.0:
        drhodh = 2.377E-3 * 4.2561 * 6.875E-6 * (1. - 6.875E-6 * Z[1]) ** 3.2561
        dVdh = 6.875E-6 * 1116.39 * Z[2] / 2 * (1.0 - 6.875E-6 * Z[1]) ** -0.5
    else:
        drhodh = 2.377E-3 * 0.2971 * (-1.0) / 20806.7 * np.exp((36089.0 - Z[1]) / 20806.7)
        dVdh = 0.0
    dVdh2 = 2.0 * dVdh * V
    dCDdh = -k * Fo3 * CL * WT / (0.5 * Z[5]) * (V ** -2 * rho ** -2 * drhodh + rho ** -1 * V ** -3 * dVdh)
    dDdh = 0.5 * Z[5] * (drhodh * CDmin * V ** 2 + rho * dCDdh * V ** 2 + rho * CDmin * dVdh2)
    if Z[1] <= 36089.0:
        dVdM = 1116.39 * (1.0 - 6.875E-6 * Z[1]) ** -0.5
    else:
        dVdM = 968.1
    if Z[2] >= 1:
        dkdM = abs(Z[3]) * (2.0 * abs(Z[2])) * np.cos(Z[4] * np.pi / 180.) \
               / (4. * abs(Z[3]) * np.sqrt(abs(Z[4] ** 2 - 1.) - 2.))
    else:
        dkdM = 0.0
    dVdM2 = 2.0 * V * dVdM
    dCLdM = -2.0 * WT / (0.5 * Z[5]) * rho ** -1 * V ** -3 * dVdM
    dCDdM = Fo3 * (2.0 * k * CL * dCLdM + CL ** 2 * dkdM)
    dDdM = 0.5 * rho * Z[5] * (CD * dVdM2 + V ** 2 * dCDdM)
    if Z[2] >= 1:
        dkdAR = 0.0
    else:
        dkdAR = -1.0 / (0.8 * np.pi * abs(Z[3]) ** 2)
    dCDdAR = Fo3 * CL ** 2 * dkdAR
    dDdAR = 0.5 * rho * Z[5] * V ** 2 * dCDdAR
    dCDmindLambda = -3.05 * 3.0 / 2.0 * Z[0] ** (5.0 / 3.0) \
                    * np.cos(Z[4] * np.pi / 180.) ** 0.5 * np.pi / 180. * np.sin(Z[4] * np.pi / 180.)
    if Z[2] >= 1:
        u = (Z[2] ** 2 - 1.) * np.cos(Z[4] * np.pi / 180.)
        up = -np.pi / 180.0 * (Z[2] ** 2 - 1.) * np.sin(Z[4] * np.pi / 180.)
        v = 4.0 * np.sqrt(Z[4] ** 2 - 1.0) - 2.0
        vp = 4.0 * Z[4] * (Z[4] ** 2 - 1.0) ** -0.5
        dkdLambda = (up * v - u * vp) / v ** 2
    else:
        dkdLambda = 0.0
    dCDdLambda = Fo3 * (dCDmindLambda + CL ** 2 * dkdLambda)
    dDdLambda = 0.5 * rho * Z[5] * V ** 2 * dCDdLambda
    dCLdSref2 = 2.0 * CL * -WT / (0.5 * rho * V ** 2 * Z[5] ** 2)
    dCDdSref = Fo3 * k * dCLdSref2
    dDdSref = 0.5 * rho * V ** 2 * (CD + Z[5] * dCDdSref)
    J_D['z'] = np.array([np.append(dDdtc/scalers['D']*scalers['tc'], [dDdh/scalers['D']*scalers['h'],
                                           dDdM/scalers['D']*scalers['M'],
                                           dDdAR/scalers['D']*scalers['AR'],
                                           dDdLambda/scalers['D']*scalers['Lambda'],
                                           dDdSref/scalers['D']*scalers['Sref']])])
    dDdWT = Fo3 * k * 2.0 * WT / (0.5 * rho * V ** 2 * Z[5])
    J_D['WT'] = np.array([[dDdWT/scalers['D']*scalers['WT']]])
    S_shifted, Ai, Aij = polynomial_function([Theta], [5], [.25], "Fo3", deriv=True)
    if Theta / pf_d['Fo3'][0] >= 0.75 and Theta / pf_d['Fo3'][0] <= 1.25:
        dSThetadTheta = 1.0 / pf_d['Fo3'][0]
    else:
        dSThetadTheta = 0.0
    dSThetadTheta2 = 2.0 * S_shifted[0] * dSThetadTheta
    dFo3dTheta = Ai[0] * dSThetadTheta + 0.5 * Aij[0, 0] * dSThetadTheta2
    dCDdTheta = dFo3dTheta * (CDmin + k * CL ** 2)
    dDdTheta = 0.5 * rho * V ** 2 * Z[5] * dCDdTheta
    J_D['Theta'] = np.array(
        [[dDdTheta/scalers['D']*scalers['Theta']]]).reshape((1, 1))
    S_shifted, Ai, Aij = polynomial_function(s_new,
                                 [1, 1], [.25] * 2, "Fo2", deriv=True)
    if ESF / pf_d['Fo2'][0] >= 0.75 and ESF / pf_d['Fo2'][0] <= 1.25:
        dSESFdESF = 1.0 / pf_d['Fo2'][0]
    else:
        dSESFdESF = 0.0
    dSESFdESF2 = 2.0 * S_shifted[0] * dSESFdESF
    dFo2dESF = Ai[0] * dSESFdESF + 0.5 * Aij[0, 0] * dSESFdESF2 \
               + Aij[1, 0] * S_shifted[1] * dSESFdESF
    dCDdESF = Fo3 * CDMIN * dFo2dESF
    dDdESF = 0.5 * rho * V ** 2 * Z[5] * dCDdESF
    J_D['ESF'] = np.array(
        [[dDdESF/scalers['D']*scalers['ESF']]]).reshape((1, 1))

    # dpdx ################################################################
    J_dpdx = dict()
    J_dpdx['x_aer'] = np.array([[0.0]])
    J_dpdx['z'] = np.zeros((1, 6))
    S_shifted, Ai, Aij = polynomial_function([Z[0]], [1], [.25], "dpdx", deriv=True)
    if Z[0] / pf_d['dpdx'][0] >= 0.75 and Z[0] / pf_d['dpdx'][0] <= 1.25:
        dStcdtc = 1.0 / pf_d['dpdx'][0]
    else:
        dStcdtc = 0.0
    dStcdtc2 = 2.0 * S_shifted[0] * dStcdtc
    ddpdxdtc = Ai[0] * dStcdtc + 0.5 * Aij[0, 0] * dStcdtc2
    J_dpdx['z'][0, 0] = ddpdxdtc/scalers['dpdx']*scalers['tc']
    J_dpdx['WT'] = np.array([[0.0]])
    J_dpdx['Theta'] = np.array([[0.0]])
    J_dpdx['ESF'] = np.array([[0.0]])

    # dfin ###############################################################
    J_fin = dict()
    J_fin['x_aer'] = np.array([[-dDdCf * WT / D ** 2/scalers['WT']*scalers['D']]]).reshape((1, 1))
    J_fin['z'] = np.array([-J_D['z'][0] * WT/ D ** 2/scalers['WT']*scalers['D']**2])
    J_fin['WT'] = np.array([[(D - dDdWT * WT) / D ** 2/scalers['WT']*scalers['D']*scalers['WT']]]).reshape((1, 1))
    J_fin['Theta'] = np.array([[(-dDdTheta * WT) / D ** 2/scalers['WT']*scalers['D']*scalers['Theta']]]).reshape((1, 1))
    J_fin['ESF'] = np.array([[(-dDdESF * WT) / D ** 2/scalers['WT']*scalers['D']*scalers['ESF']]]).reshape((1, 1))
    return J_L, J_D, J_fin, J_dpdx


if __name__ == "__main__":

    analysis = Aerodynamics()
    # run_tool(analysis, sys.argv)
    inputs = dict(z=np.array([5.00000000e-02,
                              4.5e+04,
                              1.6,
                              5.5,
                              55.,
                              1.0e+03]),
                  x_str=np.array([0.25, 1.]),
                  x_aer=np.array([1.]),
                  x_pro=0.5,
                  fin=4.093062,
                  D=5572.5217226,
                  DT=0.162151493275,
                  L=50606.68120583,
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
    aerodynamics_partials(inputs)