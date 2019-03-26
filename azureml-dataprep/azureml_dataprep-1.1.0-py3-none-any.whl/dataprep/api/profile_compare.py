#  ---------------------------------------------------------
#  Copyright (c) Microsoft Corporation. All rights reserved.
#  ---------------------------------------------------------
"""compare helper class."""
from azureml.dataprep import FieldType
from azureml.dataprep.api.engineapi.typedefinitions import HistogramCompareMethod


class _ProfileCompare:
    """Library code to help with compare operations."""

    @staticmethod
    def compare_profiles(
        lhs_profile,
        rhs_profile,
        include_columns,
        exclude_columns,
        histogram_compare_method
        ):
        """
            If include and exclude columns are None, comparison is on full profile by finding matched columns.
            If both Include and exclude columns are provided then comparison will consider include first then apply exclude list.
            If only exclude column list is provided then columns remaining after exclusion will be compared.
        """
        matched_column_profiles = list()
        unmatched_column_profiles = list()
        selected_column_list = _ProfileCompare._select_columns_for_compare(lhs_profile, rhs_profile, include_columns, exclude_columns)

        _ProfileCompare._find_lhs_matched_columns(lhs_profile,
                                                    rhs_profile,
                                                    matched_column_profiles,
                                                    unmatched_column_profiles,
                                                    selected_column_list)

        _ProfileCompare._find_rhs_unmatched_columns(lhs_profile,
                                                    rhs_profile,
                                                    unmatched_column_profiles,
                                                    selected_column_list)

        list_column_difference = _ProfileCompare._compare_column_profile(matched_column_profiles, histogram_compare_method)
        from azureml.dataprep.api.engineapi.typedefinitions import DataProfileDifference
        ds_profile_diff = DataProfileDifference()
        ds_profile_diff.column_profile_difference =list_column_difference
        ds_profile_diff.unmatched_column_profiles = unmatched_column_profiles

        return ds_profile_diff

    @staticmethod
    def _select_columns_for_compare(lhs_profile, rhs_profile, include_columns, exclude_columns):
        """
        """
        column_list = list()
        for column in lhs_profile.columns.values():
            column_list.append(column.name)

        for r_column in rhs_profile.columns.values():
            if(r_column.name not in column_list):
                r_column.append(column.name)

        if(include_columns is None and exclude_columns is None):
            return column_list
        elif(include_columns is not None and exclude_columns is not None):
            filtered_list = list([x for x in include_columns if x not in exclude_columns])
            if(filtered_list is None or len(filtered_list) == 0):
                raise Exception("Both Include and Exclude column lists match")
            else:
                return list([x for x in filtered_list if x in column_list])
        elif(include_columns is not None and exclude_columns is None):
            return list([x for x in include_columns if x in column_list])
        else:
            return list([x for x in exclude_columns if x not in column_list])
        pass

    @staticmethod
    def _find_lhs_matched_columns(
        lhs_profile,
        rhs_profile,
        matched_column_profiles,
        unmatched_column_profiles,
        selected_column_list):
        """
        """
        for lhs_column_profile in lhs_profile.columns.values():
            foundMatch = False
            if(lhs_column_profile.name in selected_column_list):
                for rhs_column_profile in rhs_profile.columns.values():
                    if (lhs_column_profile.name == rhs_column_profile.name and lhs_column_profile.type == rhs_column_profile.type):
                        matched_column_profiles.append((lhs_column_profile, rhs_column_profile))
                        foundMatch = True
                        break
                if not foundMatch:
                    unmatched_column_profiles.append((lhs_column_profile.name, -1))
        pass

    @staticmethod
    def _find_rhs_unmatched_columns(
        lhs_profile,
        rhs_profile,
        unmatched_column_profiles,
        selected_column_list):
        for rhs_column_profile in rhs_profile.columns.values():
            if(rhs_column_profile.name in selected_column_list):
                for lhs_column_profile in lhs_profile.columns.values():
                    if (lhs_column_profile.name != rhs_column_profile.name and lhs_column_profile.type != rhs_column_profile.type):
                        unmatched_column_profiles.append((rhs_column_profile.name, 1))
                        break

    @staticmethod
    def _compare_column_profile(columns: list, histogram_distance_method: HistogramCompareMethod):
        from azureml.dataprep.api.engineapi.typedefinitions import ColumnProfileDifference
        from azureml.dataprep.api.engineapi.typedefinitions import MomentsDifference

        list_column_difference = list()
        for lhs_column_profile, rhs_column_profile in columns:
            col_diff = ColumnProfileDifference()
            col_diff.name=lhs_column_profile.name
            col_diff.column_type=lhs_column_profile.type
            col_diff.difference_in_histograms = _ProfileCompare._compare_histogram_bins(
                lhs_column_profile=lhs_column_profile,
                rhs_column_profile=rhs_column_profile,
                histogram_distance_method=histogram_distance_method
                )
            col_diff.difference_in_count_in_percent = _ProfileCompare._compare_count_in_percent(lhs_column_profile.count, rhs_column_profile.count)
            col_diff.difference_in_value_counts_in_percent = _ProfileCompare._compare_value_counts(lhs_column_profile.value_counts, rhs_column_profile.value_counts)
            # TODO Below min / max / std / mean / mode / skewness diff should consider categorical values

            if(lhs_column_profile.type in({FieldType.INTEGER, FieldType.DECIMAL})):
                col_diff.difference_in_min = rhs_column_profile.min - lhs_column_profile.min
                col_diff.difference_in_max = rhs_column_profile.max - lhs_column_profile.max
                diff_in_moments = MomentsDifference()
                diff_in_moments.difference_in_mean = rhs_column_profile.moments.mean - lhs_column_profile.moments.mean
                col_diff.difference_in_moments = diff_in_moments
                col_diff.difference_in_median = rhs_column_profile.median - lhs_column_profile.median
            elif(lhs_column_profile.type == FieldType.DATE):
                col_diff.difference_in_min = (rhs_column_profile.min - lhs_column_profile.min).total_seconds()
                col_diff.difference_in_max = (rhs_column_profile.max - lhs_column_profile.max).total_seconds()
                diff_in_moments = MomentsDifference()
                diff_in_moments.difference_in_mean = (rhs_column_profile.mean - lhs_column_profile.mean).total_seconds()
                diff_in_moments.difference_in_median = (rhs_column_profile.median - lhs_column_profile.median).total_seconds()
                col_diff.difference_in_moments = diff_in_moments
            else:
                # TODO implement string comparisions.
                print("TODO implement string comparisions.")

            list_column_difference.append(col_diff)
        return list_column_difference

    @staticmethod
    def _compare_value_counts(lhs_value_counts, rhs_value_counts):
        from azureml.dataprep.api.engineapi.typedefinitions import ValueCountDifference
        return_dict = list()

        if(lhs_value_counts is None and rhs_value_counts is None):
            return None
        elif(lhs_value_counts is None):
            return rhs_value_counts # TODO copy over the rhs Value counts
        elif(rhs_value_counts is None):
            return lhs_value_counts # TODO set the value counts to be -ve value
        else:
            lhs_count = len(lhs_value_counts)
            rhs_count = len(rhs_value_counts)

        if(lhs_count == 0 and rhs_count == 0):
            return None
        elif(lhs_count == 0):
            return rhs_value_counts # TODO copy over the rhs Value counts
        elif(rhs_count == 0):
            return lhs_value_counts # TODO set the value counts to be -ve value
        else:
            pass

        if(lhs_count>rhs_count):
            for r_value_count in rhs_value_counts:
                for l_value_count in lhs_value_counts:
                    if(r_value_count.value == l_value_count.value):
                        valueCountDiff = ValueCountDifference()
                        valueCountDiff.value = l_value_count.value
                        valueCountDiff.difference_in_percent = _ProfileCompare._compare_count_in_percent(
                            l_value_count.count, r_value_count.count)
                        return_dict.append(valueCountDiff)
                        break
                if(r_value_count.value not in return_dict):
                    valueCountDiff = ValueCountDifference()
                    valueCountDiff.value = r_value_count.value
                    valueCountDiff.difference_in_percent = r_value_count.count
                    return_dict.append(valueCountDiff)

            for l_value_count in lhs_value_counts:
                if(l_value_count.value not in return_dict):
                    valueCountDiff = ValueCountDifference()
                    valueCountDiff.value = l_value_count.value
                    valueCountDiff.difference_in_percent = - l_value_count.count
                    return_dict.append(valueCountDiff)
        else:
            for l_value_count in lhs_value_counts:
                for r_value_count in rhs_value_counts:
                    if(r_value_count.value == l_value_count.value):
                        valueCountDiff = ValueCountDifference()
                        valueCountDiff.value = l_value_count.value
                        valueCountDiff.difference_in_percent = _ProfileCompare._compare_count_in_percent(
                            l_value_count.count, r_value_count.count)
                        return_dict.append(valueCountDiff)
                        break
                if(l_value_count.value not in return_dict):
                    valueCountDiff = ValueCountDifference()
                    valueCountDiff.value = l_value_count.value
                    valueCountDiff.difference_in_percent = - l_value_count.count
                    return_dict.append(valueCountDiff)

            for r_value_count in rhs_value_counts:
                if(r_value_count.value not in return_dict):
                    valueCountDiff = ValueCountDifference()
                    valueCountDiff.value = r_value_count.value
                    valueCountDiff.difference_in_percent = - r_value_count.count
                    return_dict.append(valueCountDiff)
        return return_dict

    @staticmethod
    def _compare_count_in_percent(lhs_count, rhs_count):
        """
            Always rhs_count - lhs_count and then find the percent deviation
        """
        if lhs_count == 0:
            return rhs_count
        if rhs_count == 0:
            return -lhs_count
        if lhs_count == rhs_count:
            return 0

        one_percent = lhs_count/100
        diff = rhs_count - lhs_count
        return diff/one_percent

    @staticmethod
    def _compare_histogram_bins(lhs_column_profile, rhs_column_profile, histogram_distance_method):
        if(lhs_column_profile.histogram == None or rhs_column_profile.histogram == None):
            return None

        lhs_cdf_arry = []
        lhs_weights_arry = []
        rhs_cdf_arry = []
        rhs_weights_arry = []
        for bin in lhs_column_profile.histogram:
            lhs_cdf_arry.append((bin.lower_bound+bin.upper_bound)/2)
            lhs_weights_arry.append(bin.count)

        for bin in rhs_column_profile.histogram:
            rhs_cdf_arry.append((bin.lower_bound+bin.upper_bound)/2)
            rhs_weights_arry.append(bin.count)

        if(histogram_distance_method == HistogramCompareMethod.WASSERSTEIN):
            from scipy.stats import wasserstein_distance
            return wasserstein_distance(lhs_cdf_arry, rhs_cdf_arry, lhs_weights_arry, rhs_weights_arry)
        elif(histogram_distance_method == HistogramCompareMethod.ENERGY):
            from scipy.stats import energy_distance
            return energy_distance(lhs_cdf_arry, rhs_cdf_arry, lhs_weights_arry, rhs_weights_arry)
        else:
            raise NotImplementedError()