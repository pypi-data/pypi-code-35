from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class HoneypotField(forms.CharField):
    """
    Honeypot form field.
    Inspired from https://github.com/mixkorshun/django-antispam/blob/master/antispam/honeypot/forms.py
    """
    default_error_messages = {
        'honeypot': _('Invalid value for honey pot field.'),
    }

    def __init__(self, **kwargs):
        assert 'required' not in kwargs
        kwargs['required'] = False
        kwargs.setdefault('label', '')
        super(HoneypotField, self).__init__(**kwargs)

    def clean(self, *args, **kwargs):
        """
        Validates form field value entered by user.
        :param value: user-input
        :raise: ValidationError with code="spam-protection" if honeypot check failed.
        """
        data = super(HoneypotField, self).clean(*args, **kwargs)

        if data:
            raise ValidationError(self.error_messages['honeypot'], code='spam-protection')
