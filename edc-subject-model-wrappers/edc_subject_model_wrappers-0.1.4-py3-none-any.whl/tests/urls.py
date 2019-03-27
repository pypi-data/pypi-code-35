from django.urls import path
from django.contrib import admin

from .admin import edc_subject_model_wrapper_admin

app_name = "edc_subject_model_wrappers"

urlpatterns = [
    path("admin/", edc_subject_model_wrapper_admin.urls),
    path("admin/", admin.site.urls),
]
