from jsonview.decorators import json_view
from utils import statusCode
from .models import FirmwarePool, FirmwarePoolInit,FRIMWARE_TYPE_ARR
from transfer import TransferHttpResponse
from django.conf import settings
from django.http import HttpResponse
from datetime import datetime
from os import mknod
from os.path import exists
from utils.auth import auth_login_required, auth_administrator_required, ret_code_json_wrapped
import shutil


# Create your views here.
# NRK/DFU/version/
@json_view
@auth_login_required
def get_version(request):
    if request.method != "GET":
        return statusCode.NRK_INVALID_OPERA_INVALID_METHOD

    firmware_type = request.GET.get('type', False)

    if firmware_type not in  FRIMWARE_TYPE_ARR:
        return statusCode.NRK_INVALID_PARAM_UNKNOWN_ERR

    try:
        firmWare = FirmwarePool.objects.filter(type=firmware_type).values('type', 'version', 'size', 'build_date')
    except:
        return statusCode.NRK_SERVER_ERR

    return firmWare[0]


# NRK/DFU/upgrade/
@auth_administrator_required
def upgrade(request):
    if request.method != "GET" and request.method != "POST":
        return ret_code_json_wrapped(statusCode.NRK_INVALID_OPERA_INVALID_METHOD)

    firmware_type = request.GET.get('type', False)

    if firmware_type not in FRIMWARE_TYPE_ARR:
        return ret_code_json_wrapped(statusCode.NRK_INVALID_PARAM_UNKNOWN_ERR)

    try:
        firmWare = FirmwarePool.objects.get(type=firmware_type)
    except:
        return ret_code_json_wrapped(statusCode.NRK_SERVER_ERR)

    if firmWare.path == '':
        if firmware_type == 'enduro':
            path = '/DFU/enduro.bin'
        elif firmware_type == 'bte_3g':
            path = '/DFU/bte_3g.bin'
        else:
            path = '/DFU/bluetooth_3g.bin'
    else:
        path = firmWare.path

    root, location = settings.TRANSFER_MAPPINGS.items()[0]

    path = root + path
    #path = './static/visa.jpg'

    #download request
    if request.method == "GET":
        return TransferHttpResponse(path)

    # else POST means upload request
    new_version = request.GET.get('version', False)
    # upload a firmware operation must specified a version.
    if new_version == False:
        return ret_code_json_wrapped(statusCode.NRK_INVALID_PARAM_UNKNOWN_ERR)

    major_new, bracket, minor_new = new_version.partition('.')
    major_old, bracket, minor_old = firmWare.version.partition('.')

    # FIX ME!!! Here assumption that #minor_version will be nerver greater than 99
    if (major_new*100+minor_new) < (major_old*100+minor_old):
        return ret_code_json_wrapped(statusCode.NRK_INVALID_PARAM_UNKNOWN_ERR)

    for name in request.FILES.keys():
        data = request.FILES.getlist(name)

        #Only one file will be allowed to be uploaded to server each time.
        if len(data) != 1:
            return ret_code_json_wrapped(statusCode.NRK_INVALID_PARAM_UNKNOWN_ERR)


        file = data[0]
        file.close()   #close at first, or a {32 errorno} will be raised

        firmWare.size = file.size
        firmWare.version = new_version
        firmWare.uploaded_date = datetime.now()
        firmWare.build_date = datetime.now()

        #path = './static/visa2.jpg'   #for test purpose only
        if not exists(path):
            try:
                mknod(path, 0o777)
            except:
                return ret_code_json_wrapped(statusCode.NRK_SERVER_ERR)

        try :
            shutil.copyfile(file.path, path)
        except :
            return ret_code_json_wrapped(statusCode.NRK_SERVER_ERR)

        try :
            firmWare.save()
        except :
            return ret_code_json_wrapped(statusCode.NRK_SERVER_BUSY)

        return ret_code_json_wrapped(statusCode.NRK_OK)

