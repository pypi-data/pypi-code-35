from django.forms import ModelForm
from django import forms
from django.utils.translation import gettext_lazy as _

from latch.models import LatchSetup


class LatchPairForm(forms.Form):
    latch_pin = forms.CharField(label=_("Latch Pin"))


class LatchSetupForm(ModelForm):
    exclude = []
    class Meta:
        model = LatchSetup
        fields = '__all__'


class LatchUnpairForm(forms.Form):
    latch_confirm = forms.BooleanField(label=_("Confirm"))
