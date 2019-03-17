from sklearn_helper.tests.util.model_input_builder import ModelInputBuilder


class TestUtil:

    @classmethod
    def generate_model_input(cls, *models):
        model_input_builder = ModelInputBuilder()

        for model in models:
            model_input_builder.add_model(model)

        return model_input_builder.build()
