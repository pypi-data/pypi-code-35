class JsonUtils:
    @staticmethod
    def get_attribute(data, attributes, default_value):
        if (data is None):
            return default_value

        if (len(attributes) == 1):
            return data.get(attributes[0]) or default_value
        else:
            new_data = data.get(attributes[0]) or None
            if (new_data is None):
                return default_value
            else:
                del attributes[0]
                return JsonUtils.get_attribute(new_data, attributes, default_value)
