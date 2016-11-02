
from jsonview.decorators import json_view
from utils import statusCode
from .models import user_ext
from .forms import AAAPasswordChangeForm, AAAUserCreationForm, AAAUserChangeForm
from django.contrib.auth import login as update_session_auth_hash
import json


# Create your views here.
# /NRK/AAA/user
@json_view
def user(request):
    user_list = user_ext.objects.values('id', 'username').order_by('id')
    return list(user_list)

# /NRK/AAA/user/1
@json_view
def user_id(request, user_id):
    if request.method == "GET":
        try:
            user_info = user_ext.objects.filter(pk=user_id).values()
        except user_ext.DoesNotExist:
            return statusCode.NRK_INVALID_PARAM_ID_ERR
        except:
            return statusCode.NRK_INVALID_PARAM_UNKNOWN_ERR
        else:
            return user_info[0]
    #change the specified user's information
    elif request.method == "PUT":
        if request.content_type == 'application/json':
            http_body = json.loads(request.body)
        else:
            return statusCode.NRK_INVALID_PARAM_UNKNOWN_ERR

        form = AAAUserChangeForm(data = http_body)
        if form.is_valid():
            form.save()
            return statusCode.NRK_OK
        else:
            return statusCode.NRK_INVALID_PARAM_UNKNOWN_ERR
    else:
        return statusCode.NRK_INVALID_OPERA_INVALID_METHOD

# /NRK/AAA/user/1/password
@json_view
def password(request, user_id):
    if request.method != "POST":
        return statusCode.NRK_INVALID_OPERA_INVALID_METHOD

    form = AAAPasswordChangeForm(user=request.user, data=request.POST)
    if form.is_valid():
        form.save()
        # Updating the password logs out all other sessions for the user
        # except the current one.
        update_session_auth_hash(request, form.user)

        return statusCode.NRK_OK

    else:
        if form.has_error('old_password') is not None:
            return statusCode.NRK_INVALID_PARAM_USR_PWD_ERR
        elif form.has_error('new_password'):
            return statusCode.NRK_INVALID_PARAM_PWD_TOO_SIMPLE
        else:
            return statusCode.NRK_INVALID_PARAM_UNKNOWN_ERR

# /NRK/AAA/user/login
@json_view
def login(request):
    if request.method != "POST":
        return statusCode.NRK_INVALID_OPERA_INVALID_METHOD

    from django.contrib.admin.forms import AdminAuthenticationForm
    from django.contrib.auth import login as auth_login

    form = AdminAuthenticationForm(request, data=request.POST)
    if form.is_valid():
        auth_login(request, form.get_user())
        return statusCode.NRK_OK
    else:
        return statusCode.NRK_INVALID_PARAM_USR_PWD_ERR

# /NRK/AAA/user/logout
@json_view
def logout(request):
    if request.method != "POST":
        return statusCode.NRK_INVALID_OPERA_INVALID_METHOD

    from django.contrib.auth import logout as auth_logout

    auth_logout(request)

    return statusCode.NRK_OK

# /NRK/AAA/user/add
@json_view
def user_add(request):
    if request.method != "POST":
        return statusCode.NRK_INVALID_OPERA_INVALID_METHOD

    form = AAAUserCreationForm(data=request.POST)
    if form.is_valid():
        form.save()
        return statusCode.NRK_OK
    else:
        if form.has_error('username') is not None:
            return statusCode.NRK_INVALID_PARAM_USER_ALREADY_EXIST
        elif form.has_error('password') is not None:
            return statusCode.NRK_INVALID_PARAM_PWD_TOO_SIMPLE
        elif form.has_error('phone_number') is not None:
            return statusCode.NRK_INVALID_PARAM_UNKNOWN_ERR
        else:
            return statusCode.NRK_INVALID_PARAM_UNKNOWN_ERR