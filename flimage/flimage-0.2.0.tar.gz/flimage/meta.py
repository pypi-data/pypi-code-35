from qpimage.meta import MetaDict, DATA_KEYS, OTHER_DEF


OTHER_DEF_FL = OTHER_DEF.copy()
OTHER_DEF_FL["flimage version"] = "flimage software version used"
OTHER_KEYS_FL = sorted(OTHER_DEF_FL.keys())


#: valid :class:`flimage.core.FLImage` meta data keys
META_KEYS_FL = DATA_KEYS + OTHER_KEYS_FL


class FLMetaDict(MetaDict):
    valid_keys = META_KEYS_FL
