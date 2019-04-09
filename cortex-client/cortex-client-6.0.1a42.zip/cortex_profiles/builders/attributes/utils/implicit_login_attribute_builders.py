"""
Users dont really configure how these attributes are derived ... they just are ...
"""

from typing import List

import pandas as pd

from cortex_profiles.builders.attributes.utils import attribute_builder_utils, implicit_attribute_builder_utils
from cortex_profiles.implicit.schema import implicit_attributes, implicit_templates
from cortex_profiles.schemas.dataframes import LOGIN_COUNTS_COL, LOGIN_DURATIONS_COL, DAILY_LOGIN_DURATIONS_COL, \
    DAILY_LOGIN_COUNTS_COL
from cortex_profiles.schemas.schemas import CONTEXTS
from cortex_profiles.types.attribute_values import CounterAttributeValue, TotalAttributeValue, AverageAttributeValue
from cortex_profiles.types.attributes import ObservedProfileAttribute


def derive_counter_attributes_for_specific_logins(sessions_df:pd.DataFrame, df_timeframe:str="eternally") -> List[ObservedProfileAttribute]:

    login_counts_df = implicit_attribute_builder_utils.derive_count_of_user_logins(sessions_df)

    if login_counts_df.empty:
        return []

    attribute_value_constructor = attribute_builder_utils.simple_counter_attribute_value_constructor(
        LOGIN_COUNTS_COL.TOTAL,
        CounterAttributeValue
    )

    return attribute_builder_utils.derive_attributes_from_groups_in_df(
        login_counts_df,
        [
            LOGIN_COUNTS_COL.PROFILEID,
            LOGIN_COUNTS_COL.APPID,
        ],
        implicit_attributes.NameTemplates.COUNT_OF_APP_SPECIFIC_LOGINS,
        ObservedProfileAttribute,
        attribute_value_constructor,
        additional_identifiers={implicit_templates.TIMEFRAME: df_timeframe}
    )


def derive_counter_attributes_for_login_durations(sessions_df:pd.DataFrame, df_timeframe:str="eternally") -> List[ObservedProfileAttribute]:

    login_durations_df = implicit_attribute_builder_utils.derive_time_users_spent_logged_in(sessions_df)

    if login_durations_df.empty:
        return []

    attribute_value_constructor = attribute_builder_utils.simple_counter_attribute_value_constructor(
         LOGIN_DURATIONS_COL.DURATION,
        TotalAttributeValue
    )

    return attribute_builder_utils.derive_attributes_from_groups_in_df(
        login_durations_df,
        [
            LOGIN_DURATIONS_COL.PROFILEID,
            LOGIN_DURATIONS_COL.APPID,
        ],
        implicit_attributes.NameTemplates.TOTAL_DURATION_OF_APP_SPECIFIC_LOGINS,
        ObservedProfileAttribute,
        attribute_value_constructor,
        additional_identifiers={implicit_templates.TIMEFRAME: df_timeframe}
    )


def derive_dimensional_attributes_for_daily_login_counts(sessions_df: pd.DataFrame, df_timeframe: str = "eternally") -> List[ObservedProfileAttribute]:

    daily_login_counts_df = implicit_attribute_builder_utils.derive_daily_login_counts(sessions_df)

    if daily_login_counts_df.empty:
        return []

    attribute_value_constructor = attribute_builder_utils.simple_dimensional_attribute_value_constructor(
        CONTEXTS.DAY,
        CounterAttributeValue,
        DAILY_LOGIN_COUNTS_COL.DAY,
        DAILY_LOGIN_COUNTS_COL.TOTAL
    )

    return attribute_builder_utils.derive_attributes_from_groups_in_df(
        daily_login_counts_df,
        [
            DAILY_LOGIN_COUNTS_COL.PROFILEID,
            DAILY_LOGIN_COUNTS_COL.APPID
        ],
        implicit_attributes.NameTemplates.COUNT_OF_DAILY_APP_SPECIFIC_LOGINS,
        ObservedProfileAttribute,
        attribute_value_constructor,
        additional_identifiers={implicit_templates.TIMEFRAME: df_timeframe}
    )


def derive_dimensional_attributes_for_daily_login_durations(sessions_df:pd.DataFrame, df_timeframe:str="eternally") -> List[ObservedProfileAttribute]:

    login_counts_df = implicit_attribute_builder_utils.derive_daily_login_duration(sessions_df)

    if login_counts_df.empty:
        return []

    attribute_value_constructor = attribute_builder_utils.simple_dimensional_attribute_value_constructor(
        CONTEXTS.DAY,
        TotalAttributeValue,
        DAILY_LOGIN_DURATIONS_COL.DAY,
        DAILY_LOGIN_DURATIONS_COL.DURATION
    )

    return attribute_builder_utils.derive_attributes_from_groups_in_df(
        login_counts_df,
        [
            DAILY_LOGIN_DURATIONS_COL.PROFILEID,
            DAILY_LOGIN_DURATIONS_COL.APPID
        ],
        implicit_attributes.NameTemplates.TOTAL_DURATION_OF_DAILY_APP_SPECIFIC_LOGINS,
        ObservedProfileAttribute,
        attribute_value_constructor,
        additional_identifiers={implicit_templates.TIMEFRAME: df_timeframe}
    )


def derive_average_attributes_for_daily_login_counts(sessions_df:pd.DataFrame, df_timeframe:str="eternally") -> List[ObservedProfileAttribute]:

    average_of_login_counts_df = implicit_attribute_builder_utils.derive_average_of_daily_login_counts(sessions_df)

    if average_of_login_counts_df.empty:
        return []

    attribute_value_constructor = attribute_builder_utils.simple_attribute_value_selector_constructor(
        DAILY_LOGIN_COUNTS_COL.TOTAL,
        AverageAttributeValue,
    )

    return attribute_builder_utils.derive_attributes_from_groups_in_df(
        average_of_login_counts_df,
        [
            DAILY_LOGIN_COUNTS_COL.PROFILEID,
            DAILY_LOGIN_COUNTS_COL.APPID
        ],
        implicit_attributes.NameTemplates.AVERAGE_COUNT_OF_DAILY_APP_SPECIFIC_LOGINS,
        ObservedProfileAttribute,
        attribute_value_constructor,
        additional_identifiers={implicit_templates.TIMEFRAME: df_timeframe}
    )


def derive_average_attributes_for_daily_login_duration(sessions_df:pd.DataFrame, df_timeframe:str="eternally") -> List[ObservedProfileAttribute]:
    average_of_login_duration_df = implicit_attribute_builder_utils.derive_average_of_daily_login_durations(sessions_df)

    if average_of_login_duration_df.empty:
        return []

    attribute_value_constructor = attribute_builder_utils.simple_attribute_value_selector_constructor(
        DAILY_LOGIN_DURATIONS_COL.DURATION,
        AverageAttributeValue,
    )

    return attribute_builder_utils.derive_attributes_from_groups_in_df(
        average_of_login_duration_df,
        [
            DAILY_LOGIN_DURATIONS_COL.PROFILEID,
            DAILY_LOGIN_DURATIONS_COL.APPID
        ],
        implicit_attributes.NameTemplates.AVERAGE_DURATION_OF_DAILY_APP_SPECIFIC_LOGINS,
        ObservedProfileAttribute,
        attribute_value_constructor,
        additional_identifiers={implicit_templates.TIMEFRAME: df_timeframe}
    )
