from django import forms
from django.utils.safestring import mark_safe


class HoneypotInput(forms.TextInput):
    """
    Default honeypot field widget.
    Display text input in hidden div.
    Inspired from https://github.com/mixkorshun/django-antispam/blob/master/antispam/honeypot/widgets.py
    """

    def render(self, *args, **kwargs):
        """
        Returns this widget rendered as HTML.
        """
        return mark_safe(
            '<div style="display: none;">%s</div>' % str(
                super(HoneypotInput, self).render(*args, **kwargs))
        )
