import warnings

from edc_dashboard.view_mixins import EdcViewMixin as EdcBaseViewMixin  # noqa

warnings.warn(
    "Import path edc_base.view_mixins.EdcBaseViewMixin is deprecated. "
    "Import as edc_base.view_mixins.EdcViewMixin",
    DeprecationWarning,
)
