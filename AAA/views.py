
from jsonview.decorators import json_view
from utils import statusCode
from utils.auth import auth_login_required, auth_administrator_required, json_convert
from .models import user_ext
from .forms import AAAPasswordChangeForm, AAAUserCreationForm, AAAUserChangeForm
from django.contrib.auth import login as update_session_auth_hash
import json
from django.views.decorators.cache import never_cache


# Create your views here.
# /NRK/AAA/user
@json_view
def user(request):
    # Only Administrator can get user list.
    if not request.user.is_superuser:
        return statusCode.NRK_INVALID_OPERA_LOW_PRIVILEGE
    user_list = user_ext.objects.values('id', 'username').order_by('id')
    return list(user_list)


# Obtain user own information
# /NRK/AAA/user/userInfo
@json_view
@auth_login_required
def user_info(request):
    if request.method != "GET":
        return statusCode.NRK_INVALID_OPERA_INVALID_METHOD

    return get_user_info(request.user.id)


# /NRK/AAA/user/1
@json_view
@auth_login_required
def user_id(request, user_id):
    # Administrator can get/change any user's infomation, but normal users can only get/change its own information.
    if (not request.user.is_superuser) and (request.user.id != int(user_id)):
        return statusCode.NRK_INVALID_OPERA_LOW_PRIVILEGE

    if request.method == "GET":
        return get_user_info(user_id)

    # change the specified user's information
    elif request.method == "PUT":
        try:
            user_info = user_ext.objects.get(pk=user_id)
        except user_ext.DoesNotExist:
            return statusCode.NRK_INVALID_PARAM_ID_ERR
        except:
            return statusCode.NRK_INVALID_PARAM_UNKNOWN_ERR

        form = AAAUserChangeForm(data = json_convert(request), instance=user_info)
        if form.is_valid():
            form.save()
            return statusCode.NRK_OK
        else:
            return statusCode.NRK_INVALID_PARAM_UNKNOWN_ERR
    else:
        return statusCode.NRK_INVALID_OPERA_INVALID_METHOD


# /NRK/AAA/user/1/password
@json_view
@auth_login_required
def password(request, user_id):
    if request.method != "PUT":
        return statusCode.NRK_INVALID_OPERA_INVALID_METHOD

    if request.user.id != int(user_id):
        return statusCode.NRK_INVALID_OPERA_LOW_PRIVILEGE

    form = AAAPasswordChangeForm(user=request.user, data=json_convert(request))
    if form.is_valid():
        form.save()
        # Updating the password logs out all other sessions for the user
        # except the current one.
        update_session_auth_hash(request, form.user)

        return statusCode.NRK_OK

    else:
        if form.has_error('old_password'):
            return statusCode.NRK_INVALID_PARAM_USR_PWD_ERR
        elif form.has_error('new_password'):
            return parse_pwd_validate_err(form, 'new_password')
        else:
            return statusCode.NRK_INVALID_PARAM_UNKNOWN_ERR


# /NRK/AAA/user/login
@never_cache
@json_view
def login(request):
    if request.method != "POST":
        return statusCode.NRK_INVALID_OPERA_INVALID_METHOD

    from django.contrib.admin.forms import AdminAuthenticationForm
    from django.contrib.auth import login as auth_login

    form = AdminAuthenticationForm(request, data=json_convert(request))
    if form.is_valid():
        auth_login(request, form.get_user())
        return statusCode.NRK_OK
    else:
        return statusCode.NRK_INVALID_PARAM_USR_PWD_ERR


# /NRK/AAA/user/logout
@never_cache
@json_view
@auth_login_required
def logout(request):
    if request.method != "GET":
        return statusCode.NRK_INVALID_OPERA_INVALID_METHOD

    from django.contrib.auth import logout as auth_logout

    auth_logout(request)

    return statusCode.NRK_OK


# /NRK/AAA/user/add
@json_view
# @auth_administrator_required
def user_add(request):
    if request.method != "POST":
        return statusCode.NRK_INVALID_OPERA_INVALID_METHOD

    form = AAAUserCreationForm(data=json_convert(request))
    if form.is_valid():
        new_user = form.save(commit = False)
        new_user.is_staff = True
        new_user.is_active = True
        new_user.save()
        return statusCode.NRK_OK
    else:
        if form.has_error('username'):
            return statusCode.NRK_INVALID_PARAM_USER_ALREADY_EXIST
        elif form.has_error('password'):
            return parse_pwd_validate_err(form, 'password')
        elif form.has_error('phone_number'):
            return statusCode.NRK_INVALID_PARAM_UNKNOWN_ERR
        else:
            return statusCode.NRK_INVALID_PARAM_UNKNOWN_ERR


'''precommit:if form.has_error('password') is not None:
#parse password validate errors.'''
def parse_pwd_validate_err(form, field):
    if form.has_error(field, 'password_too_short'):
        return statusCode.NRK_INVALID_PARAM_PWD_TOO_SHORT
    elif form.has_error(field, 'password_too_similar'):
        return statusCode.NRK_INVALID_PARAM_PWD_TOO_SIMILAR
    elif form.has_error(field, 'password_too_common'):
        return statusCode.NRK_INVALID_PARAM_PWD_TOO_COMMON
    elif form.has_error(field, 'password_entirely_numeric'):
        return statusCode.NRK_INVALID_PARAM_PWD_ENTIR_NUM
    else:
        return statusCode.NRK_INVALID_PARAM_USR_PWD_ERR


# Obtain user information according to specific user id.
def get_user_info(user_id):
    try:
        field_names = [f.attname for f in user_ext.objects.model._meta.concrete_fields]
        field_names.remove('password')            # password information should be hidden
        field_names.remove('user_ptr_id')
        user_own = user_ext.objects.filter(pk=user_id).values(*field_names)
    except user_ext.DoesNotExist:
        return statusCode.NRK_INVALID_PARAM_ID_ERR
    except:
        return statusCode.NRK_INVALID_PARAM_UNKNOWN_ERR
    else:
        if user_own is None:
            return statusCode.NRK_INVALID_PARAM_NULL_ENTRY
        else:
            return user_own[0]          # Assert should be have and only have one entry.