import marshmallow
import base64


class Base64ByteString(marshmallow.fields.Field):
    """
    This fields serialize bytes to a base64 encoded UTF-8 string
    """

    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None

        return base64.b64encode(value).decode()

    def _deserialize(self, value, attr, data, **kwargs):
        return base64.b64decode(value)
