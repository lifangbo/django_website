from django.shortcuts import render
from jsonview.decorators import json_view
from utils import statusCode
from .models import *
from datetime import datetime, date, timedelta, time
import json
from utils.auth import auth_login_required, auth_administrator_required, json_convert
from .forms import *
from django.forms.models import model_to_dict

# Retrieve event type Macro definition
RetrievePoweron = 1
RetrieveMap = 2
RetrieveInputSel = 3
RetrieveMode = 4
RetrieveEnvironment = 5

# Create your views here.
# NRK/ContentMgr/logging/
@json_view
@auth_login_required
def logging(request):
    if request.method != "POST":
        return statusCode.NRK_INVALID_OPERA_INVALID_METHOD

    log_list = []
    log_entries = json_convert(request)

    if log_entries is None:
        return statusCode.NRK_INVALID_PARAM_NULL_ENTRY

    if isinstance(log_entries, dict):
        log_list.append(log_entries)
    else:
        log_list = log_entries

    for log in log_list:
        log_form = ContentMgrLoggingForm(data=log)
        if not log_form.is_valid():
            return statusCode.NRK_INVALID_PARAM_NULL_ENTRY

    # All log entry are valid, so save them into database
    for log in log_list:
        log_form = ContentMgrLoggingForm(data=log)
        new_log = log_form.save(commit=False)
        new_log.user_id = request.user.id
        new_log.save()

    return statusCode.NRK_OK


# NRK/ContentMgr/retrieve/
@json_view
@auth_login_required
def retrieve(request):
    if request.method != "GET":
        return statusCode.NRK_INVALID_OPERA_INVALID_METHOD

    build_test_tables(request.user.id)
    return statusCode.NRK_OK


def retrieve_power_on(request, start_datetime, end_datetime, details):
    response_list = []
    try:
        power_on_list = LoggingPowerOnTime.objects.filter(
            date__range=(start_datetime.date(), end_datetime.date()),
            user__user_ptr=request.user.id)
    except:
        return statusCode.NRK_INVALID_PARAM_UNKNOWN_ERR

    response_dict = {}
    for power_on_time in power_on_list:
        response_dict.clear()
        response_dict['date'] = power_on_time.date
        response_dict['total_time'] = power_on_time.total_time

        if details:
            try:
                content_details = power_on_time.LoggingPowerOnDetails.all().values('start_time', 'end_time')
            except:
                response_dict['time_segments'] = []
            else:
                content_details = list(content_details)
                response_dict['time_segments'] = content_details

        response_list.append(response_dict.copy())

    return response_list


# NRK/ContentMgr/retrieve/map/ utility
def retrieve_map_call(request, start_datetime, end_datetime, details):
    response_list = []
    try:
        power_on_list = LoggingPowerOnTime.objects.filter(
            date__range=(start_datetime.date(), end_datetime.date()),
            user__user_ptr=request.user.id)
    except:
        return statusCode.NRK_INVALID_PARAM_UNKNOWN_ERR

    response_dict = {}
    for power_on_time in power_on_list:
        response_dict.clear()
        response_dict['date'] = power_on_time.date

        try:
            content_time = power_on_time.LoggingMapTime.all()
        except:
            return statusCode.NRK_INVALID_PARAM_UNKNOWN_ERR

        content_list = []
        response_ctx = {}
        for content_entry in content_time:
            response_ctx.clear()
            response_ctx['map'] = content_entry.map.id
            response_ctx['total_time'] = content_entry.total_time
            if details:
                try:
                    content_details = content_entry.LoggingMapDetails.all().values('start_time', 'end_time')
                except:
                    response_ctx['time_segments'] = []
                else:
                    content_details = list(content_details)
                    response_ctx['time_segments'] = content_details

            content_list.append(response_ctx.copy())

        response_dict['content'] = content_list

        response_list.append(response_dict.copy())

    return response_list


# NRK/ContentMgr/retrieve/input_sel/ utility
def retrieve_inputsel_call(request, start_datetime, end_datetime, details):
    response_list = []
    try:
        power_on_list = LoggingPowerOnTime.objects.filter(
            date__range=(start_datetime.date(), end_datetime.date()),
            user__user_ptr=request.user.id)
    except:
        return statusCode.NRK_INVALID_PARAM_UNKNOWN_ERR

    response_dict = {}
    for power_on_time in power_on_list:
        response_dict.clear()
        response_dict['date'] = power_on_time.date

        try:
            content_time = power_on_time.LoggingInputSelTime.all()
        except:
            return statusCode.NRK_INVALID_PARAM_UNKNOWN_ERR

        content_list = []
        response_ctx = {}
        for content_entry in content_time:
            response_ctx.clear()
            response_ctx['input_sel'] = content_entry.input_sel.id
            response_ctx['total_time'] = content_entry.total_time
            if details:
                try:
                    content_details = content_entry.LoggingInputSelDetails.all().values('start_time', 'end_time')
                except:
                    response_ctx['time_segments'] = []
                else:
                    content_details = list(content_details)
                    response_ctx['time_segments'] = content_details

            content_list.append(response_ctx.copy())

        response_dict['content'] = content_list

        response_list.append(response_dict.copy())

    return response_list


# NRK/ContentMgr/retrieve/mode/ utility
def retrieve_mode_call(request, start_datetime, end_datetime, details):
    response_list = []
    try:
        power_on_list = LoggingPowerOnTime.objects.filter(
            date__range=(start_datetime.date(), end_datetime.date()),
            user__user_ptr=request.user.id)
    except:
        return statusCode.NRK_INVALID_PARAM_UNKNOWN_ERR

    response_dict = {}
    for power_on_time in power_on_list:
        response_dict.clear()
        response_dict['date'] = power_on_time.date

        try:
            content_time = power_on_time.LoggingModeTime.all()
        except:
            return statusCode.NRK_INVALID_PARAM_UNKNOWN_ERR

        content_list = []
        response_ctx = {}
        for content_entry in content_time:
            response_ctx.clear()
            response_ctx['mode'] = content_entry.mode.id
            response_ctx['total_time'] = content_entry.total_time
            if details:
                try:
                    content_details = content_entry.LoggingModeDetails.all().values('start_time', 'end_time')
                except:
                    response_ctx['time_segments'] = []
                else:
                    content_details = list(content_details)
                    response_ctx['time_segments'] = content_details

            content_list.append(response_ctx.copy())

        response_dict['content'] = content_list

        response_list.append(response_dict.copy())

    return response_list


# NRK/ContentMgr/retrieve/environment/ utility
def retrieve_environment_call(request, start_datetime, end_datetime, details):
    response_list = []
    try:
        power_on_list = LoggingPowerOnTime.objects.filter(
            date__range=(start_datetime.date(), end_datetime.date()),
            user__user_ptr=request.user.id)
    except:
        return statusCode.NRK_INVALID_PARAM_UNKNOWN_ERR

    response_dict = {}
    for power_on_time in power_on_list:
        response_dict.clear()
        response_dict['date'] = power_on_time.date

        try:
            content_time = power_on_time.LoggingEnvironmentTime.all()
        except:
            return statusCode.NRK_INVALID_PARAM_UNKNOWN_ERR

        content_list = []
        response_ctx = {}
        for content_entry in content_time:
            response_ctx.clear()
            response_ctx['environment'] = content_entry.environment.id
            response_ctx['total_time'] = content_entry.total_time
            if details:
                try:
                    content_details = content_entry.LoggingEnvironmentDetails.all().values('start_time', 'end_time')
                except:
                    response_ctx['time_segments'] = []
                else:
                    content_details = list(content_details)
                    response_ctx['time_segments'] = content_details

            content_list.append(response_ctx.copy())

        response_dict['content'] = content_list

        response_list.append(response_dict.copy())

    return response_list


def retrieve_call(request, retrieve_evt, start_datetime, end_datetime, details):
    print('Retrieve for %d, start_time:%s, end_time:%s, details=%s' % (retrieve_evt, start_datetime, end_datetime, details))

    if retrieve_evt == RetrievePoweron:
        return retrieve_power_on(request, start_datetime, end_datetime, details)
    elif retrieve_evt == RetrieveMap:
        return retrieve_map_call(request, start_datetime, end_datetime, details)
    elif retrieve_evt == RetrieveInputSel:
        return retrieve_inputsel_call(request, start_datetime, end_datetime, details)
    elif retrieve_evt == RetrieveMode:
        return retrieve_mode_call(request, start_datetime, end_datetime, details)
    elif retrieve_evt == RetrieveEnvironment:
        return retrieve_environment_call(request, start_datetime, end_datetime, details)
    else:
        return statusCode.NRK_INVALID_PARAM_UNKNOWN_ERR


def retrieve_entry(request, retrieve_evt=RetrievePoweron):
    retrieve_type = request.GET.get('type', False)
    if not retrieve_type:
        retrieve_type = 'day'

    if request.content_type == 'application/json':
        request.POST = json.loads(request.body)
    else:
        return statusCode.NRK_INVALID_PARAM_UNKNOWN_ERR

    # Json load may return a list when input httpbody is array.
    if not isinstance(request.POST, dict):
        return statusCode.NRK_INVALID_PARAM_UNKNOWN_ERR

    start_time =  request.POST.get('start_time', False)
    end_time = request.POST.get('end_time', False)
    if not start_time or not end_time:
        return statusCode.NRK_INVALID_PARAM_WRONG_TIME_FORMAT

    start_datetime = datetime.strptime(start_time, '%Y-%m-%d %H:%M')
    end_datetime = datetime.strptime(end_time, '%Y-%m-%d %H:%M')

    if start_datetime > end_datetime:
        return statusCode.NRK_INVALID_PARAM_WRONG_TIME_FORMAT

    details = False
    if retrieve_type == 'day':
        start_day  = start_datetime.date()
        end_day = end_datetime.date()

        if start_day != end_day:
            end_datetime = datetime.combine(start_day, time(23, 59))

        details = True
    elif retrieve_type == 'week':
        iso_start_time = start_datetime.isocalendar() #0-ISO year, 1- ISO week, 2- ISO weekday
        iso_end_time = end_datetime.isocalendar()

        # start_time does not in the same with end_time
        if iso_start_time[1] != iso_end_time[1]:
            start_datetime = start_datetime - timedelta(days= iso_start_time[2]-1)
            start_datetime = start_datetime.replace(hour=0, minute=0)
            end_datetime = start_datetime + timedelta(days = 7, seconds=-1)
    elif retrieve_type == 'month':
        start_month = start_datetime.month
        if start_datetime.month != end_datetime.month:
            start_datetime = start_datetime.replace(day=1, hour=0, minute=0)
            end_datetime = start_datetime.replace(month=start_month+1, day=1, hour=0, minute=0) - timedelta(seconds=1)
    elif retrieve_type == 'year':
        start_year = start_datetime.year
        if start_datetime.year != end_datetime.year:
            start_datetime = start_datetime.replace(month=1, day = 1, hour=0, minute=0)
            end_datetime = start_datetime.replace(year = start_year+1,month=1, day=1, hour=0, minute=0) - timedelta(seconds=1)
    else:
        return statusCode.NRK_INVALID_PARAM_UNKNOWN_ERR

    return retrieve_call(request, retrieve_evt, start_datetime, end_datetime, details)


# NRK/ContentMgr/retrieve/poweron/
@json_view
@auth_login_required
def retrieve_poweron(request):
    if request.method != "GET":
        return statusCode.NRK_INVALID_OPERA_INVALID_METHOD

    return retrieve_entry(request, RetrievePoweron)


# NRK/ContentMgr/retrieve/map/
@json_view
@auth_login_required
def retrieve_map(request):
    if request.method != "GET":
        return statusCode.NRK_INVALID_OPERA_INVALID_METHOD

    return retrieve_entry(request, RetrieveMap)


# NRK/ContentMgr/retrieve/input_sel/
@json_view
@auth_login_required
def retrieve_input_sel(request):
    if request.method != "GET":
        return statusCode.NRK_INVALID_OPERA_INVALID_METHOD

    return retrieve_entry(request, RetrieveInputSel)


# NRK/ContentMgr/retrieve/mode/
@json_view
@auth_login_required
def retrieve_mode(request):
    if request.method != "GET":
        return statusCode.NRK_INVALID_OPERA_INVALID_METHOD

    return retrieve_entry(request, RetrieveMode)


# NRK/ContentMgr/retrieve/environment/
@json_view
@auth_login_required
def retrieve_environment(request):
    if request.method != "GET":
        return statusCode.NRK_INVALID_OPERA_INVALID_METHOD

    return retrieve_entry(request, RetrieveEnvironment)