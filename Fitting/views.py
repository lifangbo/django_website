from jsonview.decorators import json_view
from utils import statusCode
from .models import *
from transfer import TransferHttpResponse
from django.conf import settings
from datetime import datetime, date
from os import mknod
from os.path import exists
from utils.auth import auth_login_required, ret_code_json_wrapped, json_convert
import shutil


# Create your views here.
# /NRK/Fitting/record/
@auth_login_required
def record(request):
    if request.method != "GET" and request.method != "POST":
        return ret_code_json_wrapped(statusCode.NRK_INVALID_OPERA_INVALID_METHOD)

    fitting_date_s = request.GET.get('date')
    if not fitting_date_s:
        fitting_datetime = datetime.now()
    else:
        fitting_datetime = datetime.strptime(fitting_date_s, '%Y-%m-%d')

    if not fitting_datetime:
        return ret_code_json_wrapped(statusCode.NRK_INVALID_PARAM_WRONG_TIME_FORMAT)

    fitting_record = {}
    try:
        fitting_record = FittingRecord.objects.get(
            fitting_date=fitting_datetime.date(),
            user__user_ptr=request.user.id)
    except FittingRecord.DoesNotExist:
        print('Warning:FittingRecord DoesNotExist')
    except FittingRecord.MultipleObjectsReturned:
        print('Warning:FittingRecord MultipleObjectsReturned')
    except:
        return ret_code_json_wrapped(statusCode.NRK_INVALID_PARAM_UNKNOWN_ERR)

    root, location = settings.TRANSFER_MAPPINGS.items()[0]

    if request.method == "GET":
        if not fitting_record:
            return ret_code_json_wrapped(statusCode.NRK_INVALID_PARAM_NULL_ENTRY)

        record_path = root + fitting_record.path
        return TransferHttpResponse(record_path)

    else:  # request.method == "POST":
        for name in request.FILES.keys():
            data = request.FILES.getlist(name)

            # Only one file will be allowed to be uploaded to server each time.
            if len(data) != 1:
                return ret_code_json_wrapped(statusCode.NRK_INVALID_PARAM_UNKNOWN_ERR)

            file = data[0]
            file.close()  # close at first, or a {32 errorno} will be raised

            if fitting_record:
                record_path = fitting_record.path
                fitting_record.delete()    # Keep only one record in one day
            else:
                record_path = '/media/' + request.user.username + '_' + date.strftime(fitting_datetime.date(), '%Y-%m-%d') + '.zip'

            new_record = FittingRecord(path=record_path)

            record_path = root + record_path
            # record_path = './static/visa.jpg'   #for test purpose only

            if not exists(record_path):
                try:
                    mknod(record_path, 0o777)
                except:
                    return ret_code_json_wrapped(statusCode.NRK_SERVER_ERR)


            new_record.user_id = request.user.id
            new_record.size = file.size
            new_record.fitting_date = fitting_datetime.date()
            new_record.uploaded_date = datetime.now()

            try:
                shutil.copyfile(file.path, record_path)
            except:
                return ret_code_json_wrapped(statusCode.NRK_SERVER_ERR)

            try:
                new_record.save()
            except:
                return ret_code_json_wrapped(statusCode.NRK_SERVER_BUSY)

            return ret_code_json_wrapped(statusCode.NRK_OK)


# /NRK/Fitting/record/retrieve/
@json_view
@auth_login_required
def retrieve(request):
    if request.method != "GET" and request.method != "POST":
        return statusCode.NRK_INVALID_OPERA_INVALID_METHOD

    retrieve_req = json_convert(request)
    if not retrieve_req :
        return statusCode.NRK_INVALID_PARAM_PARAMETERS_ABSENT

    start_date_s = retrieve_req.get('start_date')
    end_date_s = retrieve_req.get('end_date')

    if not start_date_s or not end_date_s:
        return statusCode.NRK_INVALID_PARAM_PARAMETERS_ABSENT

    start_datetime = datetime.strptime(start_date_s, '%Y-%m-%d')
    end_datetime = datetime.strptime(end_date_s, '%Y-%m-%d')

    if not start_datetime or not end_datetime:
        return statusCode.NRK_INVALID_PARAM_WRONG_TIME_FORMAT

    '''or ((end_date-start_date)> timedelta(year=5))'''
    if (start_datetime > end_datetime) :
        return statusCode.NRK_INVALID_PARAM_PARAMETERS_INVALID

    response_list = {}
    try:
        field_names = [f.attname for f in FittingRecord.objects.model._meta.concrete_fields]
        field_names.remove('path')  # path information should be hidden
        field_names.remove('user_id')
        field_names.remove('id')

        response_list = FittingRecord.objects.filter(
            fitting_date__range=(start_datetime.date(), end_datetime.date()),
            user__user_ptr=request.user.id).values(*field_names)
    except:
        return statusCode.NRK_INVALID_PARAM_UNKNOWN_ERR

    return list(response_list)
