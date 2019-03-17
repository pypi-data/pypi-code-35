"""Model implements CMS-HCC software V2318.83.P1"""

from pyriskadjust.icd_mapping.mapping_2019_v23 import ICD_MAPPING
from pyriskadjust.hccs.hccs_v23 import HCC_HIERARCHY
from pyriskadjust.hccs.hccs_v23 import HCC_LABELS
from pyriskadjust.coefficients.coefficients_v2019_v23 import COEFFICIENTS
from pyriskadjust.models.common import (
    MODEL_DESCRIPTIONS,
    MODEL_ABBREVIATIONS,
    get_age_sex_string,
    _diagnoses_to_hccs,
    _explain_score,
)
import logging

INTERACTION_VARIABLE_DESCRIPTIONS = {
    "hcc47_gcancer": "Immunity Disorders & Cancer",
    "hcc85_gdiabetesmellit": "Congestive Heart Failure & Diabetes",
    "hcc85_gcopdcf": "Congestive Heart Failure & Cystic Fibrosis/COPD",
    # "hcc85_grenal": "Congestive Heart Failure & Renal Failure",
    "hcc85_grenal_v23": "Congestive Heart Failure & Renal Failure",
    "grespdepandarre_gcopdcf": "Cardio-Respiratory Failure & Cystic Fibrosis/COPD",
    "hcc85_hcc96": "Congestive Heart failure & Specified Heart Arrhythmias",
    # "gsubstanceabuse_gpsychiatric": "Drug/Alcohol Misuse & Psychiatric Disorder",
    "disable_substabuse_psych_v23": "Disabled, Substance Misuse & Psychiatric Disorder",
    "originallydisabled_female": "Female who originally qualified due to disability",
    "originallydisabled_male": "Male who originally qualified due to disability",
    "chf_gcopdcf": "Congestive Heart Failure & Cystic Fibrosis/COPD",
    # "gcopdcf_card_resp_fail": "Cardio-Respiratory Failure & Cystic Fibrosis/COPD",
    # "asp_spec_bact_pneum_pres_ulc": "Pressure Ulcer & Aspiration and Specified Bacterial Pneumonias",
    "sepsis_asp_spec_bact_pneum": "Sepsis & Aspiration and Specified Bacterial Pneumonias",
    "schizophrenia_gcopdcf": "Schizophrenia & Cystic Fibrosis/COPD",
    "schizophrenia_chf": "Schizophrenia & Congestive Heart Failure",
    "schizophrenia_seizures": "Schizophrenia & Seizures",
    "disabled_hcc85": "Disabled & Congestive Heart Failure",
    "disabled_pressure_ulcer": "Disabled & Pressure Ulcer",
    "disabled_hcc161": "Disabled & Chronic Ulcer of Skin, Except Pressure",
    "disabled_hcc39": "Disabled & Bone/Joint/Muscle Infections/Necrosis",
    "disabled_hcc77": "Disabled & Multiple Sclerosis",
    "disabled_hcc6": "Disbaled & Opportunistic Infections",
    "ltimcaid": "Institutional Model & Patient on Medicaid at least part of the payment year",
    "origds": "Patient is over 65 & Original reason for entitlement is disability",
    "asp_spec_b_pneum_pres_ulc": "",
    "art_openings_press_ulcer": "",
    "gcopdcf_asp_spec_b_pneum": "",
}


def explain_score(score_components):
    return _explain_score(
        MODEL_ABBREVIATIONS,
        INTERACTION_VARIABLE_DESCRIPTIONS,
        HCC_LABELS,
        score_components,
    )


def diagnoses_to_hccs(diagnoses, age, sex):
    return _diagnoses_to_hccs(ICD_MAPPING, HCC_HIERARCHY, diagnoses, age, sex)
