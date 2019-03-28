from marshmallow import Schema, fields, post_load
from marshmallow.validate import OneOf
from . import models, custom_fields


class AmrUmSchema(Schema):
    __model__ = None

    @post_load()
    def make_object(self, data):
        return self.__model__(**data)


class DlmsWrapperSchema(AmrUmSchema):
    __model__ = models.DlmsWrapper

    source_wport = fields.Integer()
    destination_wport = fields.Integer()
    version = fields.Integer()


class DlmsPushMessageSchema(AmrUmSchema):
    __model__ = models.DlmsPushMessage

    payload = custom_fields.Base64ByteString()
    transport = fields.String(validate=[OneOf(choices=['udp', 'tcp'])])
    source_address = fields.String()
    source_port = fields.Integer()
    application_context = fields.String()
    dlms_wrapper = fields.Nested(DlmsWrapperSchema)


class NewMeterReadingSchema(AmrUmSchema):
    __model__ = models.NewMeterReading

    meter = fields.String()
    series = fields.String()
    timestamp = fields.DateTime(format='iso')
    value = fields.Decimal(as_string=True)

