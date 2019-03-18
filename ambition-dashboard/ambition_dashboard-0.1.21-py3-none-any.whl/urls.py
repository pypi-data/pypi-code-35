from django.conf import settings
from django.urls.conf import path, include
from edc_appointment.admin_site import edc_appointment_admin
from edc_dashboard import UrlConfig

from .patterns import subject_identifier, screening_identifier
from .views import (
    SubjectListboardView,
    SubjectDashboardView,
    ScreeningListboardView,
    TmgAeListboardView,
    TmgDeathListboardView,
    TmgHomeView,
    TmgSummaryListboardView,
    SubjectReviewListboardView,
)

app_name = "ambition_dashboard"

subject_listboard_url_config = UrlConfig(
    url_name="subject_listboard_url",
    view_class=SubjectListboardView,
    label="subject_listboard",
    identifier_label="subject_identifier",
    identifier_pattern=subject_identifier,
)
screening_listboard_url_config = UrlConfig(
    url_name="screening_listboard_url",
    view_class=ScreeningListboardView,
    label="screening_listboard",
    identifier_label="screening_identifier",
    identifier_pattern=screening_identifier,
)
subject_dashboard_url_config = UrlConfig(
    url_name="subject_dashboard_url",
    view_class=SubjectDashboardView,
    label="subject_dashboard",
    identifier_label="subject_identifier",
    identifier_pattern=subject_identifier,
)
tmg_ae_listboard_url_config = UrlConfig(
    url_name="tmg_ae_listboard_url",
    view_class=TmgAeListboardView,
    label="tmg_ae_listboard",
    identifier_label="subject_identifier",
    identifier_pattern=subject_identifier,
)
tmg_death_listboard_url_config = UrlConfig(
    url_name="tmg_death_listboard_url",
    view_class=TmgDeathListboardView,
    label="tmg_death_listboard",
    identifier_label="subject_identifier",
    identifier_pattern=subject_identifier,
)
tmg_summary_listboard_url_config = UrlConfig(
    url_name="tmg_summary_listboard_url",
    view_class=TmgSummaryListboardView,
    label="tmg_summary_listboard",
    identifier_label="subject_identifier",
    identifier_pattern=subject_identifier,
)
subject_review_listboard_url_config = UrlConfig(
    url_name="subject_review_listboard_url",
    view_class=SubjectReviewListboardView,
    label="subject_review_listboard",
    identifier_label="subject_identifier",
    identifier_pattern=subject_identifier,
)


urlpatterns = [path(r"tmg/", TmgHomeView.as_view(), name="tmg_home_url")]
urlpatterns += subject_listboard_url_config.listboard_urls
urlpatterns += screening_listboard_url_config.listboard_urls
urlpatterns += subject_dashboard_url_config.dashboard_urls
urlpatterns += tmg_ae_listboard_url_config.listboard_urls
urlpatterns += tmg_death_listboard_url_config.listboard_urls
urlpatterns += tmg_summary_listboard_url_config.listboard_urls
urlpatterns += subject_review_listboard_url_config.listboard_urls


if settings.APP_NAME == "ambition_dashboard":

    from ambition_ae.admin_site import ambition_ae_admin
    from ambition_prn.admin_site import ambition_prn_admin
    from ambition_screening.admin_site import ambition_screening_admin
    from ambition_subject.admin_site import ambition_subject_admin
    from django.contrib import admin
    from django.views.generic.base import RedirectView
    from edc_action_item.admin_site import edc_action_item_admin
    from edc_consent.admin_site import edc_consent_admin
    from edc_dashboard.views import AdministrationView
    from edc_locator.admin_site import edc_locator_admin
    from edc_reference.admin_site import edc_reference_admin

    from .tests.admin import ambition_test_admin

    urlpatterns += [
        path("accounts/", include("edc_auth.urls")),
        path("admin/", include("edc_auth.urls")),
        path("admin/", edc_appointment_admin.urls),
        path("admin/", edc_consent_admin.urls),
        path("admin/", ambition_test_admin.urls),
        path("admin/", ambition_ae_admin.urls),
        path("admin/", ambition_prn_admin.urls),
        path("admin/", edc_reference_admin.urls),
        path("admin/", edc_locator_admin.urls),
        path("admin/", ambition_subject_admin.urls),
        path("admin/", ambition_screening_admin.urls),
        path("admin/", edc_action_item_admin.urls),
        path("admin/", admin.site.urls),
        path(
            "administration/", AdministrationView.as_view(), name="administration_url"
        ),
        path("ambition_ae/", include("ambition_ae.urls")),
        path("ambition_prn/", include("ambition_prn.urls")),
        path("ambition_screening/", include("ambition_screening.urls")),
        path("ambition_subject/", include("ambition_subject.urls")),
        path("edc_action_item/", include("edc_action_item.urls")),
        path("edc_appointment/", include("edc_appointment.urls")),
        path("edc_locator/", include("edc_locator.urls")),
        path("edc_visit_schedule/", include("edc_visit_schedule.urls")),
        path("edc_consent/", include("edc_consent.urls")),
        path("edc_device/", include("edc_device.urls")),
        path("edc_reference/", include("edc_reference.urls")),
        path("edc_protocol/", include("edc_protocol.urls")),
        path("edc_auth/", include("edc_auth.urls")),
        path("edc_base/", include("edc_base.urls")),
        path("edc_lab/", include("edc_lab.urls")),
        path("edc_lab_dashboard/", include("edc_lab_dashboard.urls")),
        path("edc_subject_dashboard/", include("edc_subject_dashboard.urls")),
        path("edc_pharmacy_dashboard/", include("edc_pharmacy_dashboard.urls")),
        path("", RedirectView.as_view(url="admin/"), name="home_url"),
    ]
