from marshmallow import Schema, fields


class PetSchema(Schema):
    description = dict(id="Pet id", name="Pet name", password="Password")
    id = fields.Int(dump_only=True, description=description["id"])
    name = fields.Str(
        required=True,
        deprecated=False,
        allowEmptyValue=False,
        description=description["name"],
    )
    password = fields.Str(load_only=True, description=description["password"])


class SampleSchema(Schema):
    runs = fields.Nested("RunSchema", many=True)

    count = fields.Int()


class RunSchema(Schema):
    sample = fields.Nested(SampleSchema)


class AnalysisSchema(Schema):
    sample = fields.Nested(SampleSchema)


class AnalysisWithListSchema(Schema):
    samples = fields.List(fields.Nested(SampleSchema))


class PatternedObjectSchema(Schema):
    count = fields.Int(dump_only=True, **{"x-count": 1})
    count2 = fields.Int(dump_only=True, x_count2=2)


class SelfReferencingSchema(Schema):
    id = fields.Int()
    single = fields.Nested("self")
    many = fields.Nested("self", many=True)


class OrderedSchema(Schema):
    field1 = fields.Int()
    field2 = fields.Int()
    field3 = fields.Int()
    field4 = fields.Int()
    field5 = fields.Int()

    class Meta:
        ordered = True


class DefaultValuesSchema(Schema):
    number_auto_default = fields.Int(missing=12)
    number_manual_default = fields.Int(missing=12, doc_default=42)
    string_callable_default = fields.Str(missing=lambda: "Callable")
    string_manual_default = fields.Str(missing=lambda: "Callable", doc_default="Manual")
    numbers = fields.List(fields.Int, missing=list)
