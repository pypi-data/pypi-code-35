from django.urls.conf import path

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

urlpatterns = [path("tmg/", TmgHomeView.as_view(), name="tmg_home_url")]

urlpatterns += SubjectListboardView.urls(
    namespace=app_name, label="subject_listboard", identifier_pattern=subject_identifier
)
urlpatterns += ScreeningListboardView.urls(
    namespace=app_name,
    label="screening_listboard",
    identifier_label="screening_identifier",
    identifier_pattern=screening_identifier,
)
urlpatterns += SubjectDashboardView.urls(
    namespace=app_name, label="subject_dashboard", identifier_pattern=subject_identifier
)
urlpatterns += TmgAeListboardView.urls(
    namespace=app_name, label="tmg_ae_listboard", identifier_pattern=subject_identifier
)
urlpatterns += TmgDeathListboardView.urls(
    namespace=app_name,
    label="tmg_death_listboard",
    identifier_pattern=subject_identifier,
)
urlpatterns += TmgSummaryListboardView.urls(
    namespace=app_name,
    label="tmg_summary_listboard",
    identifier_pattern=subject_identifier,
)
urlpatterns += SubjectReviewListboardView.urls(
    namespace=app_name,
    label="subject_review_listboard",
    identifier_pattern=subject_identifier,
)
