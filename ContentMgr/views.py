from django.shortcuts import render
from jsonview.decorators import json_view
from utils import statusCode
from .models import *
from datetime import datetime, date, timedelta, time
import json


# Retrieve event type Macro definition
RetrievePoweron = 1
RetrieveMap = 2
RetrieveInputSel = 3
RetrieveMode = 4


# Create your views here.
# NRK/ContentMgr/logging/
@json_view
def logging(request):
    if request.method != "POST":
        return statusCode.NRK_INVALID_OPERA_INVALID_METHOD

    return statusCode.NRK_OK


# NRK/ContentMgr/retrieve/
@json_view
def retrieve(request):
    if request.method != "GET":
        return statusCode.NRK_INVALID_OPERA_INVALID_METHOD

    return statusCode.NRK_OK


def retrieve_call_day(request, retrieve_evt, start_datetime, end_datetime):
    if retrieve_evt == RetrievePoweron:
        db_tbl = LoggingPowerOnDetails
    elif retrieve_evt == RetrieveMap:
        db_tbl = LoggingMapDetails
    elif retrieve_evt == RetrieveInputSel:
        db_tbl = LoggingInputSelDetails
    elif retrieve_evt == RetrieveMode:
        db_tbl = LoggingModeDetails
    else:
        return statusCode.NRK_INVALID_PARAM_UNKNOWN_ERR

    print('Retrieve for %d as\'day\' type, start_time:%s, end_time:%s'  % (retrieve_evt, start_datetime, end_datetime))

    return statusCode.NRK_OK


def __retrieve_type_to_db_tbl(retrieve_evt):
    if retrieve_evt == RetrievePoweron:
        db_tbl = LoggingPowerOnTime
    elif retrieve_evt == RetrieveMap:
        db_tbl = LoggingMapTime
    elif retrieve_evt == RetrieveInputSel:
        db_tbl = LoggingInputSelTime
    elif retrieve_evt == RetrieveMode:
        db_tbl = LoggingModeTime
    else:
        return None

    return db_tbl



def retrieve_call_week(request, retrieve_evt, start_datetime, end_datetime):
    db_tbl = __retrieve_type_to_db_tbl(retrieve_evt)      #obtain specified db_table

    if db_tbl is None:
        return statusCode.NRK_INVALID_PARAM_UNKNOWN_ERR

    print('Retrieve for %d \'week\' as type, start_time:%s, end_time:%s' % (retrieve_evt, start_datetime, end_datetime))

    return statusCode.NRK_OK


def retrieve_call_month(request, retrieve_evt, start_datetime, end_datetime):
    db_tbl = __retrieve_type_to_db_tbl(retrieve_evt)  # obtain specified db_table

    if db_tbl is None:
        return statusCode.NRK_INVALID_PARAM_UNKNOWN_ERR

    print('Retrieve for %d \'month\' as type, start_time:%s, end_time:%s' % (retrieve_evt, start_datetime, end_datetime))

    return statusCode.NRK_OK


def retrieve_call_year(request, retrieve_evt, start_datetime, end_datetime):
    db_tbl = __retrieve_type_to_db_tbl(retrieve_evt)  # obtain specified db_table

    if db_tbl is None:
        return statusCode.NRK_INVALID_PARAM_UNKNOWN_ERR

    print('Retrieve for %d \'year\' as type, start_time:%s, end_time:%s' % (retrieve_evt, start_datetime, end_datetime))

    return statusCode.NRK_OK


def retrieve_entry(request, retrieve_evt=RetrievePoweron):
    retrieve_type = request.GET.get('type', False)
    if not retrieve_type:
        retrieve_type = 'day'

    if request.content_type == 'application/json':
        request.POST = json.loads(request.body)
    else:
        return statusCode.NRK_INVALID_PARAM_UNKNOWN_ERR

    start_time =  request.POST.get('start_time', False)
    end_time = request.POST.get('end_time', False)
    if not start_time or not end_time:
        return statusCode.NRK_INVALID_PARAM_WRONG_TIME_FORMAT

    start_datetime = datetime.strptime(start_time, '%Y-%m-%d %H:%M')
    end_datetime = datetime.strptime(end_time, '%Y-%m-%d %H:%M')

    if start_datetime > end_datetime:
        return statusCode.NRK_INVALID_PARAM_WRONG_TIME_FORMAT

    if retrieve_type == 'day':
        start_day  = start_datetime.date()
        end_day = end_datetime.date()

        if start_day != end_day:
            end_datetime = datetime.combine(start_day, time(23, 59))

        return retrieve_call_day(request, retrieve_evt, start_datetime, end_datetime)
    elif retrieve_type == 'week':
        iso_start_time = start_datetime.isocalendar() #0-ISO year, 1- ISO week, 2- ISO weekday
        iso_end_time = end_datetime.isocalendar()

        # start_time does not in the same with end_time
        if iso_start_time[1] != iso_end_time[1]:
            start_datetime = start_datetime - timedelta(days= iso_start_time[2]-1)
            start_datetime = start_datetime.replace(hour=0, minute=0)
            end_datetime = start_datetime + timedelta(days = 7, seconds=-1)

        return retrieve_call_week(request, retrieve_evt, start_datetime, end_datetime)
    if retrieve_type == 'month':
        start_month = start_datetime.month
        if start_datetime.month != end_datetime.month:
            start_datetime = start_datetime.replace(day=1, hour=0, minute=0)
            end_datetime = start_datetime.replace(month=start_month+1, day=1, hour=0, minute=0) - timedelta(seconds=1)

        return retrieve_call_month(request, retrieve_evt, start_datetime, end_datetime)
    elif retrieve_type == 'year':
        start_year = start_datetime.year
        if start_datetime.year != end_datetime.year:
            start_datetime = start_datetime.replace(month=1, day = 1, hour=0, minute=0)
            end_datetime = start_datetime.replace(year = start_year+1,month=1, day=1, hour=0, minute=0) - timedelta(seconds=1)

        return retrieve_call_year(request, retrieve_evt, start_datetime, end_datetime)
    else:
        return statusCode.NRK_INVALID_PARAM_UNKNOWN_ERR

# NRK/ContentMgr/retrieve/poweron/
@json_view
def retrieve_poweron(request):
    if request.method != "POST":
        return statusCode.NRK_INVALID_OPERA_INVALID_METHOD

    return retrieve_entry(request, RetrievePoweron)


# NRK/ContentMgr/retrieve/map/
@json_view
def retrieve_map(request):
    if request.method != "POST":
        return statusCode.NRK_INVALID_OPERA_INVALID_METHOD

    return retrieve_entry(request, RetrieveMap)


# NRK/ContentMgr/retrieve/input_sel/
@json_view
def retrieve_input_sel(request):
    if request.method != "POST":
        return statusCode.NRK_INVALID_OPERA_INVALID_METHOD

    return retrieve_entry(request, RetrieveInputSel)


# NRK/ContentMgr/retrieve/mode/
@json_view
def retrieve_mode(request):
    if request.method != "POST":
        return statusCode.NRK_INVALID_OPERA_INVALID_METHOD

    return retrieve_entry(request, RetrieveMode)