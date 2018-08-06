
from django import forms
from .models import Logging
import unicodedata
from django.utils.translation import ugettext, ugettext_lazy as _


class ContentMgrLoggingForm(forms.ModelForm):
    """A form that add a log entry to database"""
    class Meta:
        model = Logging
        exclude = ('user',)




