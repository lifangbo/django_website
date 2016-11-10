from jsonview.decorators import json_view
from utils import statusCode
from .models import FirmwarePool, FirmwarePoolInit,FRIMWARE_TYPE_ARR
from transfer import TransferHttpResponse
from django.conf import settings
import json

# Create your views here.
# NRK/DFU/version/
@json_view
def get_version(request):
    if request.method != "GET":
        return statusCode.NRK_INVALID_OPERA_INVALID_METHOD

    FirmwarePoolInit()
    firmware_type = request.GET.get('type', False)

    if firmware_type not in  FRIMWARE_TYPE_ARR:
        return statusCode.NRK_INVALID_PARAM_UNKNOWN_ERR

    try:
        firmWare = FirmwarePool.objects.filter(type=firmware_type).values('type', 'version', 'size', 'build_date')
    except:
        return statusCode.NRK_SERVER_ERR

    return firmWare[0]

#if you return a status code wrapped by json_view directly , a error will be showed, so wrapped is.
@json_view
def _ret_wrapped(status):
    return status


# NRK/DFU/upgrade/
def upgrade(request):
    if request.method != "GET" and request.method != "POST":
        return _ret_wrapped(statusCode.NRK_INVALID_OPERA_INVALID_METHOD)

    firmware_type = request.GET.get('type', False)

    if firmware_type not in FRIMWARE_TYPE_ARR:
        return _ret_wrapped(statusCode.NRK_INVALID_PARAM_UNKNOWN_ERR)

    try:
        firmWare = FirmwarePool.objects.get(type=firmware_type)
    except:
        return _ret_wrapped(statusCode.NRK_SERVER_ERR)

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

    #else POST means upload request
    if firmware_type == 'enduro':
        return _ret_wrapped({"URI":request.path, "body":request.body})
    elif firmware_type == 'bte_3g':
        return _ret_wrapped(request.POST)
    else:
        return _ret_wrapped(request.FILES)

