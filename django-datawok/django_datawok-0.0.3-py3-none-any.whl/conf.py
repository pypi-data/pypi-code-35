"""
Use this file to configure pluggable app settings and resolve defaults
with any overrides set in project settings.
"""

from django.conf import settings as project_settings


class Settings:
    pass


Settings.AUTH_DECORATOR = getattr(
    project_settings,
    "DATAWOK_AUTH_DECORATOR",
    "django.contrib.auth.decorators.login_required",
)

Settings.SECRET_KEY = getattr(
    project_settings, "DATAWOK_SECRET_KEY", "a-bad-secret-key"
)

Settings.AWS_ACCESS_KEY_ID = getattr(
    project_settings, "DATAWOK_AWS_ACCESS_KEY_ID", None
)

Settings.AWS_SECRET_ACCESS_KEY = getattr(
    project_settings, "DATAWOK_AWS_SECRET_ACCESS_KEY", None
)

Settings.AWS_REGION = getattr(project_settings, "DATAWOK_AWS_REGION", None)

Settings.AWS_S3_BUCKET = getattr(
    project_settings, "DATAWOK_AWS_S3_BUCKET", None
)

Settings.CLOUDFRONT_ALTERNATE_DOMAIN = getattr(
    project_settings, "DATAWOK_CLOUDFRONT_ALTERNATE_DOMAIN", None
)

Settings.AWS_PUBLIC_ROOT = getattr(
    project_settings,
    "AWS_PUBLIC_ROOT",
    Settings.CLOUDFRONT_ALTERNATE_DOMAIN
    if Settings.CLOUDFRONT_ALTERNATE_DOMAIN
    else "http://s3.amazonaws.com/{}".format(Settings.AWS_S3_BUCKET),
)

Settings.S3_UPLOAD_ROOT = getattr(
    project_settings, "DATAWOK_S3_UPLOAD_ROOT", "uploads/datawok"
)

Settings.MODELS = getattr(project_settings, "DATAWOK_MODELS", [])

Settings.QUERY_TIMEOUT = getattr(
    project_settings, "DATAWOK_QUERY_TIMEOUT", 2000
)

Settings.QUERY_LIMIT = getattr(project_settings, "DATAWOK_QUERY_TIMEOUT", 1000)

Settings.DATABASE = getattr(project_settings, "DATAWOK_DATABASE", "default")

Settings.CSV_FILE_ENCODING = getattr(
    project_settings, "DATAWOK_CSV_FILE_ENCODING", "utf-8-sig"
)

Settings.APP_ROOT = getattr(project_settings, "DATAWOK_APP_ROOT", "")

settings = Settings
