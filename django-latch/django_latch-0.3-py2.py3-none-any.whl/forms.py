from django import forms
from django.utils.translation import gettext_lazy as _


class LatchPairForm(forms.Form):
    latch_pin = forms.CharField(label=_("Latch Pin"))


class LatchUnpairForm(forms.Form):
    latch_confirm = forms.BooleanField(label=_("Confirm"))
