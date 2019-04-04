#!/usr/bin/env python
# -*- coding: UTF-8 -*-

""" internal_extensions.py: file with extended methods and objects based on internals.py """

import os
import sys
from pathlib import Path
import pandas as pd

file_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(file_dir)

from VEnCode import internals
from VEnCode.utils import exceptions
from VEnCode import common_variables as cv


class GetVencode:
    """
    thresholds for non target cell type inactivity, target cell type activity and regulatory element sparseness can
    be supplied as a keyword argument: thresholds = (non_target_celltypes_inactivity, target_celltype_activity,
    reg_element_sparseness).
    """

    def __init__(self, cell_type, data_type, algorithm, n_regulatory_elements, number_vencodes=1, parsed=False,
                 sample_type=None, thresholds=()):
        self.cell_type = cell_type
        self.data_type = data_type
        self.algorithm = algorithm
        self.k = n_regulatory_elements
        self.vencodes = self._get_vencode(number_vencodes, sample_type, parsed, thresholds)

    def _get_sample_type(self, sample_type):
        if sample_type:
            return sample_type

        if self.cell_type in cv.primary_cell_list:
            sample_type = "primary cells"
        elif any([self.cell_type in cancer for cancer in (cv.cancer_celltype_list, cv.cancer_donors_list)]):
            sample_type = "cell lines"
        else:
            parent_path = os.path.join(str(Path(__file__).parents[2]), "Files")
            sample_type_file = pd.read_csv(os.path.join(parent_path, cv.sample_type_file), sep=",",
                                           index_col=0,
                                           engine="python")
            if sample_type_file["Name"].str.contains(self.cell_type).any():
                sample_category = sample_type_file.loc[
                    sample_type_file['Name'].str.contains(self.cell_type), ['Sample category']]
                if len(sample_category["Sample category"].unique()) == 1:
                    sample_type = sample_category["Sample category"][0]
                else:
                    raise exceptions.SampleTypeNotSupported(sample_type, self.cell_type)
            else:
                raise exceptions.SampleTypeNotSupported(sample_type, self.cell_type)
        return sample_type

    def _thresholds(self):
        non_target_celltypes_inactivity = 0
        if self.data_type == "enhancers":
            target_celltype_activity = 0.1
        elif self.data_type == "promoters":
            target_celltype_activity = 0.5
        else:
            raise AttributeError("data_type - {} - currently not supported".format(self.data_type))
        if self.algorithm == "heuristic":
            reg_element_sparseness = 0
        elif self.algorithm == "sampling":
            reg_element_sparseness = 90
        else:
            raise AttributeError("Algorithm - {} - currently not supported".format(self.algorithm))
        return non_target_celltypes_inactivity, target_celltype_activity, reg_element_sparseness

    def _get_thresholds(self, thresholds):
        if thresholds:
            non_target_celltypes_inactivity, target_celltype_activity, reg_element_sparseness = thresholds
        else:
            non_target_celltypes_inactivity, target_celltype_activity, reg_element_sparseness = self._thresholds()
        return non_target_celltypes_inactivity, target_celltype_activity, reg_element_sparseness

    def _get_re_file_name(self):
        if self.data_type == "enhancers":
            file_name = cv.enhancer_file_name
        elif self.data_type == "promoters":
            file_name = cv.promoter_file_name
        else:
            raise AttributeError("data_type - {} - currently not supported".format(self.data_type))
        return file_name

    def _prepare_data_parsed(self, sample_type, thresholds):
        non_tgt_ctp_inact, tgt_ctp_act, reg_el_spsness = self._get_thresholds(thresholds)
        data = internals.DataTpm(file="parsed", sample_types=sample_type, data_type=self.data_type)
        data.make_data_celltype_specific(self.cell_type)
        data.filter_by_target_celltype_activity(threshold=tgt_ctp_act)
        data.filter_by_reg_element_sparseness(threshold=reg_el_spsness)
        data.define_non_target_celltypes_inactivity(threshold=non_tgt_ctp_inact)
        if self.algorithm != "sampling":
            data.sort_sparseness()
        return data

    def _prepare_data_raw(self, sample_type, thresholds):
        non_tgt_ctp_inact, tgt_ctp_act, reg_el_spsness = self._get_thresholds(thresholds)
        file_name = self._get_re_file_name()
        data = internals.DataTpm(file=file_name, sample_types="primary cells", data_type=self.data_type)
        data.merge_donors_primary(exclude_target=False)
        data_second = internals.DataTpm(file=file_name, sample_types=sample_type,
                                        data_type=self.data_type)

        data.add_celltype(self.cell_type, file=data_second)

        data.make_data_celltype_specific(self.cell_type)
        data.filter_by_target_celltype_activity(threshold=tgt_ctp_act)
        data.filter_by_reg_element_sparseness(threshold=reg_el_spsness)
        data.define_non_target_celltypes_inactivity(threshold=non_tgt_ctp_inact)
        return data

    def _get_data(self, sample_type, parsed, thresholds):
        sample_type = self._get_sample_type(sample_type)
        if parsed:
            data = self._prepare_data_parsed(sample_type, thresholds)
        else:
            data = self._prepare_data_raw(sample_type, thresholds)
        return data

    def _get_vencode(self, amount, sample_type, parsed, thresholds):
        data = self._get_data(sample_type, parsed, thresholds)
        if self.algorithm == "sampling":
            vencodes = internals.Vencodes(data, algorithm="sampling", number_of_re=self.k, n_samples=10000)
        elif self.algorithm == "heuristic":
            vencodes = internals.Vencodes(data, algorithm="heuristic", number_of_re=self.k, stop=3)
        else:
            raise AttributeError("Algorithm '{}' not recognized".format(self.algorithm))
        vencodes.next(amount=amount)
        if vencodes.vencodes:
            return vencodes
        else:
            raise exceptions.NoVencodeError("No VEnCodes found for {}!".format(self.cell_type))
