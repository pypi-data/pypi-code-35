class ModelInputBuilder:
    def __init__(self):
        self.model_count = 0
        self.models = {}

    def add_model(self, model, params={}):
        self.models["model_{}".format(self.model_count)] = {
            "model": model,
            "params": params
        }
        self.model_count += 1
        return self

    def build(self):
        models = self.models
        self.models = {}
        return models

