from __future__ import unicode_literals

from django.db import models

# Create your models here.
MAP_CODES = (
    (1, 'MAP1'),
    (2, 'MAP2'),
    (3, 'MAP3'),
    (4, 'MAP4'),
)

MODE_CODES = (
    (1, 'RICH'),
    (2, 'NORMAL'),
)

INPUT_SEL_CODES = (
    (1, 'MIC'),
    (2, 'T-COIL'),
    (3, 'AUX_IN'),
    (4, 'MIC_T-COIL'),
    (5, 'MIC_AUX_IN'),
)

EVENT_TYPE_CODES = (
    (1, 'POWER_ON'),
    (2, 'POWER_OFF'),
    (3, 'MAP_SWITCH'),
    (4, 'INPUT_SEL_SWITCH'),
    (5, 'MODE_SWITCH'),
)


class MapCodec(models.Model):
    id = models.IntegerField(choices= MAP_CODES, primary_key=True)
    map = models.CharField(editable=False, max_length= 10)


class InputSelCodec(models.Model):
    id = models.IntegerField(choices= INPUT_SEL_CODES, primary_key=True)
    input_sel = models.CharField(editable=False, max_length= 10)


class ModeCodec(models.Model):
    id = models.IntegerField(choices= MODE_CODES, primary_key=True)
    mode = models.CharField(editable=False, max_length= 10)


class EventTypeCodec(models.Model):
    id = models.IntegerField(choices= EVENT_TYPE_CODES, primary_key=True)
    event_type = models.CharField(editable=False, max_length= 10)


class ReservedCodec(models.Model):
    #id = models.IntegerField(choices= EVENT_TYPE_CODES, primary_key=True)
    xxx_type = models.CharField(editable=False, max_length= 10)


# uploaded by user, Initial Layer
class Logging(models.Model):
    date = models.DateField(editable=False)
    time = models.TimeField(editable=False)
    event_type = models.ForeignKey(EventTypeCodec, blank = True)
    map = models.ForeignKey(MapCodec, blank = True)
    input_sel = models.ForeignKey(InputSelCodec, blank = True)
    mode = models.ForeignKey(ModeCodec, blank = True)
    RESERVERD1 = models.ForeignKey(ReservedCodec, blank = True)


# Cached log information to accelerate retrieve
# Second Layer, the unit of #total_time is minute
class LoggingPowerOnTime(models.Model):
    date = models.DateField()
    total_time = models.IntegerField()


class LoggingMapTime(models.Model):
    date = models.DateField()
    map = models.ForeignKey(MapCodec)
    total_time = models.TimeField()


class LoggingInputSelTime(models.Model):
    date = models.DateField()
    input_sel = models.ForeignKey(InputSelCodec)
    total_time = models.TimeField()


class LoggingModeTime(models.Model):
    date = models.DateField()
    mode = models.ForeignKey(ModeCodec)
    total_time = models.TimeField()


# Third Layer
class LoggingPowerOnDetails(models.Model):
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()


class LoggingMapDetails(models.Model):
    power_on = models.ForeignKey(LoggingPowerOnDetails)
    map = models.ForeignKey(MapCodec)
    start_time = models.TimeField()
    end_time = models.TimeField()


class LoggingInputSelDetails(models.Model):
    power_on = models.ForeignKey(LoggingPowerOnDetails)
    input_sel = models.ForeignKey(InputSelCodec)
    start_time = models.TimeField()
    end_time = models.TimeField()


class LoggingModeDetails(models.Model):
    power_on = models.ForeignKey(LoggingPowerOnDetails)
    mode = models.ForeignKey(ModeCodec)
    start_time = models.TimeField()
    end_time = models.TimeField()


# AS (MapCodec, InputSelCodec, ModeCodec) these tables are constant tables, so you must be sure construct them at first
def codec_tbls_construct():
    if MapCodec.objects.count() == 0:
        for id, name in MAP_CODES:
            MapCodec.objects.create(id = id, map = name)

    if InputSelCodec.objects.count() == 0:
        for id, name in INPUT_SEL_CODES:
            InputSelCodec.objects.create(id = id, input_sel = name)

    if ModeCodec.objects.count() == 0:
        for id, name in MODE_CODES:
            ModeCodec.objects.create(id = id, mode = name)

    if EventTypeCodec.objects.count() == 0:
        for id, name in EVENT_TYPE_CODES:
            EventTypeCodec.objects.create(id = id, event_type = name)