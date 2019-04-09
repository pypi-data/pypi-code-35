from aldryn_forms.cms_plugins import Field
from aldryn_forms.contrib.email_notifications.cms_plugins import \
    EmailNotificationForm
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext_lazy as _

from djangocms_honeypot_captcha.fields import HoneypotField
from djangocms_honeypot_captcha.widgets import HoneypotInput


class HoneypotCaptchaPlugin(Field):
    name = _("Honeypot Captcha")
    parent_classes = [
        "FormPlugin",
        "EmailNotificationForm",
        "SilentHoneypotEmailNotificationForm",
    ]
    allow_children = False  # do not allow use other children

    form_field = HoneypotField
    form_field_widget = HoneypotInput

    form_field_enabled_options = []
    fieldset_general_fields = []
    fieldset_advanced_fields = []


plugin_pool.register_plugin(HoneypotCaptchaPlugin)


class SilentHoneypotEmailNotificationForm(EmailNotificationForm):
    name = _('Form (Advanced with Silent Honeypot Captcha)')
    
    _honeypot_captcha_field_name = 'honeypotcaptchaplugin_1'

    def process_form(self, instance, request):
        form = super(EmailNotificationForm, self).process_form(instance, request)

        is_no_errors = form._errors is None
        if is_no_errors:
            return form

        is_honeypot_filled = self._honeypot_captcha_field_name in form._errors
        if is_honeypot_filled:
            form = self._silently_remove_error_without_form_processing(form)
        
        return form
    
    def _silently_remove_error_without_form_processing(self, form):
        del form._errors[self._honeypot_captcha_field_name]
        return form


plugin_pool.register_plugin(SilentHoneypotEmailNotificationForm)
