from jsonview.decorators import json_view
from utils import statusCode
from .models import FirmwarePool, FirmwarePoolInit


# Create your views here.
# NRK/DFU/version/
@json_view
def get_version(request):
    FirmwarePoolInit()
    firmware_type = request.GET.get('type', False)
    if firmware_type is False:
        return statusCode.NRK_INVALID_PARAM_UNKNOWN_ERR

    try:
        firmWare = FirmwarePool.objects.filter(type=firmware_type).values('type', 'version', 'size', 'build_date')

    except:
        return statusCode.NRK_SERVER_ERR

    return firmWare[0]


# NRK/DFU/upgrade/
def upgrade(request):
    if request.method != "POST":
        return json_view(statusCode.NRK_INVALID_OPERA_INVALID_METHOD)

    return json_view(statusCode.NRK_OK)
