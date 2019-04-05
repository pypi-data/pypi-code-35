from django.db import models

MODEL = "model"
SERIALIZER = "serializer"
PUBLISH_SERIALIZER = "publish_serializer"
VIEWSET = "viewset"
DETAIL_VIEW = "detail"
PUBLISH_VIEW = "publish"
UPLOAD_CSV_FILE_VIEW = "upload_csv_file"

STRING_FIELDS = [
    models.CharField,
    models.EmailField,
    models.FilePathField,
    models.GenericIPAddressField,
    models.SlugField,
    models.TextField,
    models.URLField,
    models.UUIDField,
]

DATE_FIELDS = [models.DateField, models.DateTimeField, models.TimeField]

INTEGER_FIELDS = [
    models.AutoField,
    models.BigAutoField,
    models.BigIntegerField,
    models.IntegerField,
    models.PositiveIntegerField,
    models.PositiveSmallIntegerField,
    models.SmallIntegerField,
]

FLOAT_FIELDS = [models.DecimalField, models.FloatField]

BOOLEAN_FIELDS = [models.BooleanField, models.NullBooleanField]

FK_FIELDS = [models.ForeignKey, models.OneToOneField, models.ManyToManyField]

UNSUPPORTED_FIELDS = [
    models.BinaryField,
    models.DurationField,
    models.FileField,
    models.ImageField,
]
