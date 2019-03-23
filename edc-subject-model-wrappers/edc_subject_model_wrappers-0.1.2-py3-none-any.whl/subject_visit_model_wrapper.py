from django.apps import apps as django_apps
from edc_model_wrapper import ModelWrapper
from edc_metadata.constants import REQUIRED, KEYED


class SubjectVisitModelWrapper(ModelWrapper):

    model = None
    next_url_attrs = ["subject_identifier", "appointment", "reason"]
    next_url_name = "subject_dashboard_url"

    @property
    def appointment(self):
        return str(self.object.appointment.id)

    @property
    def appointment_model_cls(self):
        return self.object.appointment.__class__

    @property
    def subject_identifier(self):
        return self.object.subject_identifier

    @property
    def crf_metadata(self):
        CrfMetadata = django_apps.get_model('edc_metadata.crfmetadata')
        return CrfMetadata.objects.filter(
            subject_identifier=self.object.subject_identifier,
            visit_code=self.object.visit_code,
            visit_code_sequence=self.object.visit_code_sequence,
            entry_status__in=[KEYED, REQUIRED],
        )

    @property
    def requisition_metadata(self):
        RequisitionMetadata = django_apps.get_model(
            'edc_metadata.requisitionmetadata')
        return RequisitionMetadata.objects.filter(
            subject_identifier=self.object.subject_identifier,
            visit_code=self.object.visit_code,
            visit_code_sequence=self.object.visit_code_sequence,
            entry_status__in=[KEYED, REQUIRED],
        )
