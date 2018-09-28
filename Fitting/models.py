from __future__ import unicode_literals

from django.db import models
from AAA.models import user_ext


# Create your models here.
class FittingRecord(models.Model):
    user = models.ForeignKey(user_ext, related_name="FittingRecord")
    size = models.IntegerField(blank=True)
    path = models.FilePathField(editable=False, blank=False)
    fitting_date = models.DateField(blank=False)
    uploaded_date = models.DateTimeField(blank=True)
    download_count = models.IntegerField(blank=True, default=0)
    notes = models.CharField(max_length=128, blank=True)
