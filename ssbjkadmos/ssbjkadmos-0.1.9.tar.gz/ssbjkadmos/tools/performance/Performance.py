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
from ssbjkadmos.config import root_tag, x_WT, x_h, x_M, x_fin, x_SFC, x_WF, x_R
from ssbjkadmos.tools.SsbjDiscipline import SsbjDiscipline
from ssbjkadmos.utils.execution import run_tool
from kadmos.utilities.xml_utils_openlego import xml_safe_create_element


class Performance(SsbjDiscipline):  # AbstractDiscipline

    @property
    def description(self):
        return u'Performance analysis discipline of the SSBJ test case.'

    @property
    def supplies_partials(self):
        return True

    def generate_input_xml(self):
        root = etree.Element(root_tag)
        doc = etree.ElementTree(root)

        xml_safe_create_element(doc, x_h, 45000.0)
        xml_safe_create_element(doc, x_M, 1.6)
        xml_safe_create_element(doc, x_fin, 4.093062)
        xml_safe_create_element(doc, x_SFC, 1.12328)
        xml_safe_create_element(doc, x_WT, 49909.58578)
        xml_safe_create_element(doc, x_WF, 7306.20261)

        return etree.tostring(doc, encoding='utf-8', pretty_print=True, xml_declaration=True)

    def generate_output_xml(self):
        root = etree.Element(root_tag)
        doc = etree.ElementTree(root)

        xml_safe_create_element(doc, x_R, 528.91363)

        return etree.tostring(doc, encoding='utf-8', pretty_print=True, xml_declaration=True)

    def generate_partials_xml(self):
        partials = Partials()
        partials.declare_partials(x_R, [x_h, x_M, x_fin, x_SFC, x_WT, x_WF])
        return partials.get_string()

    #@staticmethod
    def execute(self, in_file, out_file):
        doc = etree.parse(in_file)
        z1 = self.unscale_float_value(x_h, doc)
        z2 = self.unscale_float_value(x_M, doc)
        fin = self.unscale_float_value(x_fin, doc)
        SFC = self.unscale_float_value(x_SFC, doc)
        WT = self.unscale_float_value(x_WT, doc)
        WF = self.unscale_float_value(x_WF, doc)

        # Execute ONERA performance function
        R = performance(np.array([0.0, z1, z2, 0.0, 0.0, 0.0]), fin, SFC, WT, WF)

        root = etree.Element(root_tag)
        doc = etree.ElementTree(root)
        xml_safe_create_element(doc, x_R, self.scale_value(R, x_R))
        doc.write(out_file, encoding='utf-8', pretty_print=True, xml_declaration=True)

    #@staticmethod
    def linearize(self, in_file, partials_file):
        doc = etree.parse(in_file)
        z1 = self.unscale_float_value(x_h, doc)
        z2 = self.unscale_float_value(x_M, doc)
        fin = self.unscale_float_value(x_fin, doc)
        SFC = self.unscale_float_value(x_SFC, doc)
        WT = self.unscale_float_value(x_WT, doc)
        WF = self.unscale_float_value(x_WF, doc)

        # Execute ONERA partials function
        J_R = performance_partials(inputs=dict(z=np.array([0.0, z1, z2, 0.0, 0.0, 0.0]),
                                               fin=fin, SFC=SFC, WT=WT, WF=WF), scalers=self.scalers)

        # Declare and write partials
        partials = Partials()
        partials.declare_partials(x_R,
                                  [x_h, x_M, x_fin, x_SFC, x_WT, x_WF],
                                  [J_R['z'][0, 1], J_R['z'][0, 2], J_R['fin'], J_R['SFC'], J_R['WT'], J_R['WF']])
        partials.write(partials_file)


def performance(Z, fin, SFC, WT, WF):
    # Performance calculation as taken from the ONERA repository
    if Z[1] <= 36089.:
        theta = 1.0 - 6.875E-6 * Z[1]
    else:
        theta = 0.7519
    R = 661.0 * np.sqrt(theta) * Z[2] * fin / SFC * np.log(abs(WT / (WT - WF)))
    return R


def performance_partials(inputs, scalers):
    # Performance partials calculation as taken from the ONERA repository
    # Adjustments: removed "self" and "scalers" and replaced "J" for "J_R"
    Z = inputs['z']
    fin = inputs['fin']
    SFC = inputs['SFC']
    WT = inputs['WT']
    WF = inputs['WF']

    if Z[1] <= 36089:
        theta = 1.0 - 6.875E-6 * Z[1]
        dRdh = -0.5 * 661.0 * theta ** -0.5 * 6.875e-6 * Z[2] * fin \
               / SFC * np.log(abs(WT / (WT - WF)))
    else:
        theta = 0.7519
        dRdh = 0.0

    dRdM = 661.0 * np.sqrt(theta) * fin / SFC * np.log(abs(WT / (WT - WF)))

    J_R = dict()
    J_R['z'] = np.zeros((1, 6))
    J_R['z'][0, 1] = np.array([dRdh/scalers['R']*scalers['h']])
    J_R['z'][0, 2] = np.array([dRdM/scalers['R']*scalers['M']])
    dRdfin = 661.0 * np.sqrt(theta) * Z[2] / SFC * np.log(abs(WT / (WT - WF)))
    J_R['fin'] = np.array([dRdfin/scalers['R']*scalers['fin']])
    dRdSFC = -661.0 * np.sqrt(theta) * Z[2] * fin / SFC ** 2 * np.log(abs(WT / (WT - WF)))
    J_R['SFC'] = np.array([dRdSFC/scalers['R']*scalers['SFC']])
    dRdWT = 661.0 * np.sqrt(theta) * Z[2] * fin / SFC * -WF / (WT * (WT - WF))
    J_R['WT'] = np.array([dRdWT/scalers['R']*scalers['WT']])
    dRdWF = 661.0 * np.sqrt(theta) * Z[2] * fin / SFC * 1.0 / (WT - WF)
    J_R['WF'] = np.array([dRdWF/scalers['R']*scalers['WF']])
    return J_R


if __name__ == "__main__":
    analysis = Performance()
    #run_tool(analysis, sys.argv)
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
                  Theta=1.02643602,
                  ESF=0.5027771,
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
    performance_partials(inputs)
