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
cell_technology_enum = PlantPredictEnum()
cell_technology_enum.NTYPE_MONO_CSI = 1
cell_technology_enum.PTYPE_MONO_CSI_PERC = 2
cell_technology_enum.PTYPE_MONO_CSI_BSF = 3
cell_technology_enum.POLY_CSI_PERC = 4
cell_technology_enum.POLY_CSI_BSF = 5
cell_technology_enum.CDTE = 6
cell_technology_enum.CIGS = 7

# Cleaning Frequency
cleaning_frequency_enum = PlantPredictEnum()
cleaning_frequency_enum.NONE = 0
cleaning_frequency_enum.DAILY = 1
cleaning_frequency_enum.MONTHLY = 2
cleaning_frequency_enum.QUARTERLY = 3
cleaning_frequency_enum.YEARLY = 4

# Construction Type


# Entity Type
entity_type_enum = PlantPredictEnum()

# Module Orientation
module_orientation_enum = PlantPredictEnum()

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
