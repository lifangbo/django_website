from __future__ import unicode_literals

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from AAA.models import user_ext

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


ENVIRO_TYPE_CODES = (
    (1, 'QUIET'),
    (2, 'RESTRERANT'),
    (3, 'INDOOR'),
    (4, 'OUTDOOR'),
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


class EnvironmentCodec(models.Model):
    id = models.IntegerField(choices= ENVIRO_TYPE_CODES, primary_key=True)
    enviro_type = models.CharField(editable=False, max_length= 10)


# uploaded by user, Initial Layer
class Logging(models.Model):
    user = models.ForeignKey(user_ext, related_name="Logging")
    date = models.DateField()
    time = models.TimeField()
    volume = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])
    map = models.ForeignKey(MapCodec)
    battery = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])
    input_sel = models.ForeignKey(InputSelCodec)
    mode = models.ForeignKey(ModeCodec)
    environment = models.ForeignKey(EnvironmentCodec)


# Cached log information to accelerate retrieve
# Second Layer, the unit of #total_time is minute
class LoggingPowerOnTime(models.Model):
    user = models.ForeignKey(user_ext, related_name="LoggingPowerOnTime")
    date = models.DateField(unique=True)
    total_time = models.PositiveIntegerField()       # in minutes


class LoggingMapTime(models.Model):
    date_time = models.ForeignKey(LoggingPowerOnTime, related_name="LoggingMapTime")
    map = models.ForeignKey(MapCodec)
    total_time = models.PositiveIntegerField()


class LoggingInputSelTime(models.Model):
    date_time = models.ForeignKey(LoggingPowerOnTime, related_name="LoggingInputSelTime")
    input_sel = models.ForeignKey(InputSelCodec)
    total_time = models.PositiveIntegerField()


class LoggingModeTime(models.Model):
    date_time = models.ForeignKey(LoggingPowerOnTime, related_name="LoggingModeTime")
    mode = models.ForeignKey(ModeCodec)
    total_time = models.PositiveIntegerField()


class LoggingEnvironmentTime(models.Model):
    date_time = models.ForeignKey(LoggingPowerOnTime, related_name="LoggingEnvironmentTime")
    environment = models.ForeignKey(EnvironmentCodec)
    total_time = models.PositiveIntegerField()


# Third Layer
class LoggingPowerOnDetails(models.Model):
    date_time = models.ForeignKey(LoggingPowerOnTime, related_name="LoggingPowerOnDetails")
    start_time = models.TimeField()
    end_time = models.TimeField()


class LoggingMapDetails(models.Model):
    on_time = models.ForeignKey(LoggingMapTime, related_name="LoggingMapDetails")
    start_time = models.TimeField()
    end_time = models.TimeField()


class LoggingInputSelDetails(models.Model):
    on_time = models.ForeignKey(LoggingInputSelTime, related_name="LoggingInputSelDetails")
    start_time = models.TimeField()
    end_time = models.TimeField()


class LoggingModeDetails(models.Model):
    on_time = models.ForeignKey(LoggingModeTime, related_name="LoggingModeDetails")
    start_time = models.TimeField()
    end_time = models.TimeField()


class LoggingEnvironmentDetails(models.Model):
    on_time = models.ForeignKey(LoggingEnvironmentTime, related_name="LoggingEnvironmentDetails")
    start_time = models.TimeField()
    end_time = models.TimeField()


# AS (MapCodec, InputSelCodec, ModeCodec,...) these tables are constant tables, so you must be sure construct them at first
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

    if EnvironmentCodec.objects.count() == 0:
        for id, name in ENVIRO_TYPE_CODES:
            EnvironmentCodec.objects.create(id = id, enviro_type = name)


def build_test_tables(user_id):
    LoggingPowerOnTime.objects.all().delete()
    LoggingMapTime.objects.all().delete()
    LoggingInputSelTime.objects.all().delete()
    LoggingModeTime.objects.all().delete()
    LoggingEnvironmentTime.objects.all().delete()

    LoggingPowerOnDetails.objects.all().delete()
    LoggingMapDetails.objects.all().delete()
    LoggingInputSelDetails.objects.all().delete()
    LoggingModeDetails.objects.all().delete()
    LoggingEnvironmentDetails.objects.all().delete()

# 08-01
    # second layer --statics
    poweron_time_entry = LoggingPowerOnTime.objects.create(user_id=user_id, date="2018-08-01", total_time=14 * 60)

    LoggingPowerOnDetails.objects.create(date_time=poweron_time_entry, start_time="08:00:00", end_time="12:00:00")
    LoggingPowerOnDetails.objects.create(date_time=poweron_time_entry, start_time="12:00:00", end_time="22:00:00")

    on_time_entry = LoggingMapTime.objects.create(date_time=poweron_time_entry, map=MapCodec.objects.get(pk=1), total_time=8 * 60)
    LoggingMapDetails.objects.create(on_time=on_time_entry, start_time="08:00:00", end_time="10:00:00")
    LoggingMapDetails.objects.create(on_time=on_time_entry, start_time="12:00:00", end_time="18:00:00")
    on_time_entry = LoggingMapTime.objects.create(date_time=poweron_time_entry, map=MapCodec.objects.get(pk=2), total_time=2 * 60)
    LoggingMapDetails.objects.create(on_time=on_time_entry, start_time="10:00:00", end_time="11:00:00")
    LoggingMapDetails.objects.create(on_time=on_time_entry, start_time="18:00:00", end_time="19:00:00")
    on_time_entry = LoggingMapTime.objects.create(date_time=poweron_time_entry, map=MapCodec.objects.get(pk=3), total_time=4 * 60)
    LoggingMapDetails.objects.create(on_time=on_time_entry, start_time="11:00:00", end_time="12:00:00")
    LoggingMapDetails.objects.create(on_time=on_time_entry, start_time="19:00:00", end_time="22:00:00")
    LoggingMapTime.objects.create(date_time=poweron_time_entry, map=MapCodec.objects.get(pk=4), total_time=0 * 60)

    on_time_entry = LoggingInputSelTime.objects.create(date_time=poweron_time_entry, input_sel=InputSelCodec.objects.get(pk=1), total_time=6 * 60)
    LoggingInputSelDetails.objects.create(on_time=on_time_entry, start_time="08:00:00", end_time="12:00:00")
    LoggingInputSelDetails.objects.create(on_time=on_time_entry, start_time="12:00:00", end_time="14:00:00")
    on_time_entry = LoggingInputSelTime.objects.create(date_time=poweron_time_entry, input_sel=InputSelCodec.objects.get(pk=2),total_time=8 * 60)
    LoggingInputSelDetails.objects.create(on_time=on_time_entry, start_time="14:00:00", end_time="22:00:00")

    on_time_entry = LoggingModeTime.objects.create(date_time=poweron_time_entry, mode=ModeCodec.objects.get(pk=1), total_time=10*60)
    LoggingModeDetails.objects.create(on_time=on_time_entry, start_time="12:00:00", end_time="22:00:00")
    on_time_entry = LoggingModeTime.objects.create(date_time=poweron_time_entry, mode=ModeCodec.objects.get(pk=2), total_time=4 * 60)
    LoggingModeDetails.objects.create(on_time=on_time_entry, start_time="08:00:00", end_time="12:00:00")

    on_time_entry = LoggingEnvironmentTime.objects.create(date_time=poweron_time_entry, environment=EnvironmentCodec.objects.get(pk=1), total_time=4 * 60)
    LoggingEnvironmentDetails.objects.create(on_time=on_time_entry, start_time="08:00:00", end_time="12:00:00")
    on_time_entry = LoggingEnvironmentTime.objects.create(date_time=poweron_time_entry, environment=EnvironmentCodec.objects.get(pk=2),total_time=4 * 60)
    LoggingEnvironmentDetails.objects.create(on_time=on_time_entry, start_time="12:00:00", end_time="16:00:00")
    on_time_entry = LoggingEnvironmentTime.objects.create(date_time=poweron_time_entry, environment=EnvironmentCodec.objects.get(pk=3),total_time=4 * 60)
    LoggingEnvironmentDetails.objects.create(on_time=on_time_entry, start_time="16:00:00", end_time="20:00:00")
    on_time_entry = LoggingEnvironmentTime.objects.create(date_time=poweron_time_entry, environment=EnvironmentCodec.objects.get(pk=4), total_time=2 * 60)
    LoggingEnvironmentDetails.objects.create(on_time=on_time_entry, start_time="20:00:00", end_time="22:00:00")

# 08-02
    poweron_time_entry = LoggingPowerOnTime.objects.create(user_id=user_id, date="2018-08-06", total_time=12 * 60)
    LoggingMapTime.objects.create(date_time=poweron_time_entry, map=MapCodec.objects.get(pk=1), total_time=4 * 60)
    LoggingMapTime.objects.create(date_time=poweron_time_entry, map=MapCodec.objects.get(pk=2), total_time=2 * 60)
    LoggingMapTime.objects.create(date_time=poweron_time_entry, map=MapCodec.objects.get(pk=3), total_time=4 * 60)
    LoggingMapTime.objects.create(date_time=poweron_time_entry, map=MapCodec.objects.get(pk=4), total_time=2 * 60)
    LoggingInputSelTime.objects.create(date_time=poweron_time_entry, input_sel=InputSelCodec.objects.get(pk=1),
                                       total_time=3 * 60)
    LoggingInputSelTime.objects.create(date_time=poweron_time_entry, input_sel=InputSelCodec.objects.get(pk=2),
                                       total_time=9 * 60)
    LoggingModeTime.objects.create(date_time=poweron_time_entry, mode=ModeCodec.objects.get(pk=1), total_time=10 * 60)
    LoggingModeTime.objects.create(date_time=poweron_time_entry, mode=ModeCodec.objects.get(pk=2), total_time=2 * 60)
    LoggingEnvironmentTime.objects.create(date_time=poweron_time_entry, environment=EnvironmentCodec.objects.get(pk=1),
                                          total_time=4 * 60)
    LoggingEnvironmentTime.objects.create(date_time=poweron_time_entry, environment=EnvironmentCodec.objects.get(pk=2),
                                          total_time=2 * 60)
    LoggingEnvironmentTime.objects.create(date_time=poweron_time_entry, environment=EnvironmentCodec.objects.get(pk=3),
                                          total_time=2 * 60)
    LoggingEnvironmentTime.objects.create(date_time=poweron_time_entry, environment=EnvironmentCodec.objects.get(pk=4),
                                          total_time=4 * 60)
# 08-05
    poweron_time_entry = LoggingPowerOnTime.objects.create(user_id=user_id, date="2018-09-01", total_time=10 * 60)
    LoggingMapTime.objects.create(date_time=poweron_time_entry, map=MapCodec.objects.get(pk=1), total_time=4 * 60)
    LoggingMapTime.objects.create(date_time=poweron_time_entry, map=MapCodec.objects.get(pk=2), total_time=2 * 60)
    LoggingMapTime.objects.create(date_time=poweron_time_entry, map=MapCodec.objects.get(pk=3), total_time=4 * 60)
    LoggingMapTime.objects.create(date_time=poweron_time_entry, map=MapCodec.objects.get(pk=4), total_time=0 * 60)
    LoggingInputSelTime.objects.create(date_time=poweron_time_entry, input_sel=InputSelCodec.objects.get(pk=1),
                                       total_time=4 * 60)
    LoggingInputSelTime.objects.create(date_time=poweron_time_entry, input_sel=InputSelCodec.objects.get(pk=2),
                                       total_time=6 * 60)
    LoggingModeTime.objects.create(date_time=poweron_time_entry, mode=ModeCodec.objects.get(pk=1), total_time=8 * 60)
    LoggingModeTime.objects.create(date_time=poweron_time_entry, mode=ModeCodec.objects.get(pk=2), total_time=2 * 60)
    LoggingEnvironmentTime.objects.create(date_time=poweron_time_entry, environment=EnvironmentCodec.objects.get(pk=1),
                                          total_time=2 * 60)
    LoggingEnvironmentTime.objects.create(date_time=poweron_time_entry, environment=EnvironmentCodec.objects.get(pk=2),
                                          total_time=3 * 60)
    LoggingEnvironmentTime.objects.create(date_time=poweron_time_entry, environment=EnvironmentCodec.objects.get(pk=3),
                                          total_time=2 * 60)
    LoggingEnvironmentTime.objects.create(date_time=poweron_time_entry, environment=EnvironmentCodec.objects.get(pk=4),
                                          total_time=3 * 60)