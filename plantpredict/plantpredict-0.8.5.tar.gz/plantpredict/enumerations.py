class PlantPredictEnum(dict):
    def __getattr__(self, key):
        if key not in self:
            raise AttributeError(key)
        return self[key]

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        del self[key]


# Air Mass Model
air_mass_model_type_enum = PlantPredictEnum()
air_mass_model_type_enum.BIRD_HULSTROM = 0
air_mass_model_type_enum.KASTEN_SANDIA = 1

# Backtracking Type
backtracking_type_enum = PlantPredictEnum()
backtracking_type_enum.TRUE_TRACKING = 0   # no backtracking
backtracking_type_enum.BACKTRACKING = 1    # shade avoidance

# Cell Technology
cell_technology_type_enum = PlantPredictEnum()
cell_technology_type_enum.NTYPE_MONO_CSI = 1
cell_technology_type_enum.PTYPE_MONO_CSI_PERC = 2
cell_technology_type_enum.PTYPE_MONO_CSI_BSF = 3
cell_technology_type_enum.POLY_CSI_PERC = 4
cell_technology_type_enum.POLY_CSI_BSF = 5
cell_technology_type_enum.CDTE = 6
cell_technology_type_enum.CIGS = 7

# Cleaning Frequency
cleaning_frequency_enum = PlantPredictEnum()
cleaning_frequency_enum.NONE = 0
cleaning_frequency_enum.DAILY = 1
cleaning_frequency_enum.MONTHLY = 2
cleaning_frequency_enum.QUARTERLY = 3
cleaning_frequency_enum.YEARLY = 4

# Construction Type
construction_type_enum = PlantPredictEnum()
construction_type_enum.GLASS_GLASS = 1
construction_type_enum.GLASS_BACKSHEET = 2

# Data Source
data_source_enum = PlantPredictEnum()
data_source_enum.MANUFACTURER = 1
data_source_enum.PVSYST = 2
data_source_enum.UNIVERSITY_OF_GENEVA = 3
data_source_enum.PHOTON = 4
data_source_enum.SANDIA_DATABASE = 5
data_source_enum.CUSTOM = 6

# Entity Type
entity_type_enum = PlantPredictEnum()
entity_type_enum.PROJECT = 1
entity_type_enum.MODULE = 2
entity_type_enum.INVERTER = 3
entity_type_enum.WEATHER = 4
entity_type_enum.PREDICTION = 5

# Faciality
faciality_enum = PlantPredictEnum()
faciality_enum.MONOFACIAL = 0
faciality_enum.BIFACIAL = 1

# Module Degradation Model
module_degradation_model_enum = PlantPredictEnum()
module_degradation_model_enum.UNSPECIFIED = 0
module_degradation_model_enum.LINEAR = 1
module_degradation_model_enum.NONLINEAR = 2

# Module Orientation
module_orientation_enum = PlantPredictEnum()
module_orientation_enum.LANDSCAPE = 0
module_orientation_enum.PORTRAIT = 1

# Prediction Status
prediction_status_enum = PlantPredictEnum()
prediction_status_enum.DRAFT_PRIVATE = 1
prediction_status_enum.DRAFT_SHARED = 2
prediction_status_enum.ANALYSIS = 3
prediction_status_enum.BID = 4
prediction_status_enum.CONTRACT = 5
prediction_status_enum.DEVELOPMENT = 6
prediction_status_enum.AS_BUILT = 7
prediction_status_enum.WARRANTY = 8
prediction_status_enum.ARCHIVED = 9

# PV Model
pv_model_type_enum = PlantPredictEnum()
pv_model_type_enum.ONE_DIODE_RECOMBINATION = 0
pv_model_type_enum.ONE_DIODE = 1
pv_model_type_enum.ONE_DIODE_RECOMBINATION_NONLINEAR = 3

# Spectral Shift Model
spectral_shift_model_enum = PlantPredictEnum()
spectral_shift_model_enum.NO_SPECTRAL_SHIFT = 0
spectral_shift_model_enum.ONE_PARAM_PWAT_OR_SANDIA = 1
spectral_shift_model_enum.TWO_PARAM_PWAT_AND_AM = 2
spectral_shift_model_enum.MONTHLY_OVERRIDE = 3

# Tracking Type
tracking_type_enum = PlantPredictEnum()
tracking_type_enum.FIXED_TILT = 0
tracking_type_enum.HORIZONTAL_TRACKER = 1
tracking_type_enum.SEASONAL_TILT = 2
