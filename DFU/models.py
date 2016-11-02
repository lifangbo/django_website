from __future__ import unicode_literals
from datetime import date, datetime, time

from django.db import models

# Create your models here.
FRIMWARE_TYPE = (
    (1, 'enduro'),
    (2, 'bte_3g'),
    (3, 'bluetooth_3g'),
)


class FirmwarePool(models.Model):
    type = models.CharField(editable=False, primary_key=True, choices=FRIMWARE_TYPE, max_length=15)
    version = models.CharField(editable=False, max_length=15)  #V99.99
    size = models.IntegerField(editable=False, blank=True)
    path = models.FilePathField(editable=False, blank=True)
    build_date = models.DateTimeField(blank = True)
    uploaded_date = models.DateTimeField(blank=True)
    download_count = models.IntegerField(blank=True, default=0)


    def __str__(self):
        return self.type, self.version, self.size, self.build_date


def FirmwarePoolInit():
    if FirmwarePool.objects.count() == 0:
        for id , type in FRIMWARE_TYPE:
            FirmwarePool.objects.create(type = type, version='1.0', size = 1, build_date=datetime.now(),uploaded_date=datetime.now())
    return


