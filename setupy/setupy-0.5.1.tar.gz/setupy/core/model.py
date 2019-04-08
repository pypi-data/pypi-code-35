class Setup():

    def __init__(self, dependency_loader):
        self._dependency_loader = dependency_loader

        self._imports = set()
        self._features = set()
        self._settings = []

    def add_import(self, _import):
        self._imports.add(_import)
        return _import

    def add_feature(self, feature_name):
        if any(f.name == feature_name for f in self._features):
            return

        feature = self._dependency_loader.load_feature(feature_name)
        self._features.add(feature)

        self._load_dependant_features(feature)
        self._load_dependant_imports(feature)

    def add_setting(self, setting_name):
        if any(s.name == setting_name for s in self._settings):
            return

        setting = self._dependency_loader.load_setting(setting_name)
        self._load_dependant_imports(setting)
        self._load_dependant_features(setting)

        self._settings.append(setting)

    def add_setting_object(self, setting_object):
        if any(s.name == setting_object.name for s in self._settings):
            return

        self._load_dependant_imports(setting_object)
        self._load_dependant_features(setting_object)

        self._settings.append(setting_object)

    def _load_dependant_features(self, object_with_deps):
        for f_name in object_with_deps.dependencies("features"):
            self.add_feature(f_name)

    def _load_dependant_imports(self, object_with_deps):
        for i in object_with_deps.dependencies("imports"):
            self.add_import(i)

    @property
    def imports(self):
        return self._imports

    @property
    def features(self):
        return self._features

    @property
    def settings(self):
        return self._settings
