
from jsonview.decorators import json_view
from utils import statusCode
from utils.auth import auth_login_required, auth_administrator_required, json_convert
from .models import *
from .forms import AAAPasswordChangeForm, AAAUserCreationForm, AAAUserChangeForm, validate_mobile_phonenumber, \
    AAASetPasswordForm
from django.contrib.auth import login as update_session_auth_hash
from django.utils import timezone
from django.views.decorators.cache import never_cache
import random
import string
from dysms.demo_sms_send import sms_send_passcode


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


# /NRK/AAA/user/resetPassword
@json_view
def reset_password(request):
    if request.method != "PUT":
        return statusCode.NRK_INVALID_OPERA_INVALID_METHOD

    request.POST = json_convert(request)

    if 'passcode'not in request.POST or 'phone_number'not in request.POST:
        return statusCode.NRK_INVALID_PARAM_PARAMETERS_ABSENT

    passcode = request.POST['passcode']
    phone_number = request.POST['phone_number']

    ret_code = check_passcode(phone_number, passcode)
    if ret_code != statusCode.NRK_OK:
        return ret_code

    try:
        user_entry = user_ext.objects.get(phone_number=phone_number)
    except:
        return statusCode.NRK_SERVER_ERR

    form = AAASetPasswordForm(user=user_entry, data=request.POST)
    if form.is_valid():
        form.save()
        return statusCode.NRK_OK
    else:
        if form.has_error('new_password'):
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

    request.POST = json_convert(request)

    username_exist = ('username' in request.POST)
    phone_number_exist = ('phone_number' in request.POST)

    if not username_exist and not phone_number_exist:
        return statusCode.NRK_INVALID_PARAM_PARAMETERS_ABSENT

    if not username_exist:
        phone_number = request.POST['phone_number']
        try:
            user_entry = user_ext.objects.get(phone_number=phone_number)
            request.POST['username'] = user_entry.username
        except:
            return statusCode.NRK_SERVER_ERR

    form = AdminAuthenticationForm(request, data=request.POST)
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

    request.POST = json_convert(request)

    # First, Check passcode is exist and valid
    if 'passcode' not in request.POST:
        return statusCode.NRK_INVALID_PARAM_PARAMETERS_ABSENT

    if 'phone_number' not in request.POST:
        return statusCode.NRK_INVALID_PARAM_PARAMETERS_ABSENT

    passcode = request.POST['passcode']
    phone_number = request.POST['phone_number']

    ret_code = check_passcode(phone_number, passcode)
    if ret_code != statusCode.NRK_OK:
        return ret_code

    # if 'username' is not specified, make one randomly. should be keep unique in database.
    if 'username' not in request.POST:
        request.POST['username'] = 'nrkid_' + ''.join(random.choice(string.letters + string.digits) for _ in range(14))

    form = AAAUserCreationForm(data=request.POST)
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


# /NRK/AAA/verify
@json_view
def short_message_verify(request):
    if request.method != "POST":
        return statusCode.NRK_INVALID_OPERA_INVALID_METHOD

    request.POST = json_convert(request)

    try:
        phone_number = request.POST['phone_number']
        verify = request.POST['verify']
    except:
        return statusCode.NRK_INVALID_PARAM_PARAMETERS_ABSENT

    if not validate_mobile_phonenumber(phone_number):
        return statusCode.NRK_INVALID_PARAM_PARAMETERS_INVALID

    if verify not in VERIFY_TYPE:
        return statusCode.NRK_INVALID_PARAM_PARAMETERS_INVALID

    try:
        user_entry = user_ext.objects.get(phone_number=phone_number)
        user_exist = user_entry.is_active
    except user_ext.DoesNotExist:
        user_exist = False
    except :
        return statusCode.NRK_SERVER_ERR

    if verify == 'password' and (not user_exist):
        return statusCode.NRK_INVALID_PARAM_USER_NOT_EXIST

    if verify == 'register' and user_exist:
        return statusCode.NRK_INVALID_PARAM_USER_ALREADY_EXIST

    try:
        verify_entry = SmsVerify.objects.get(phone_number=phone_number)
        verify_user_exist = True
    except SmsVerify.DoesNotExist:
        verify_entry = SmsVerify(phone_number=phone_number, verify=verify)
        verify_user_exist = False
    except:
        return statusCode.NRK_SERVER_ERR

    passcode_update = True
    if verify_user_exist:
        # protect from violence attack
        if verify_entry.locked_expires > timezone.make_aware(datetime.datetime.today(), timezone.get_default_timezone()):
            return statusCode.NRK_SERVER_BUSY

        # Because of congestion possibility of SMS, send the same passcode in #valid_expires times.
        if verify_entry.valid_expires > timezone.make_aware(datetime.datetime.today(), timezone.get_default_timezone()):
            passcode_update = False

    if  passcode_update:
        # create passcode and send response
        pl = random.sample([1, 2, 3, 4, 5, 6, 7, 8, 9, 0], 4)
        passcode = ''.join(str(p) for p in pl)

        verify_entry.passcode = passcode
        verify_entry.valid_expires = timezone.make_aware(datetime.datetime.today() + datetime.timedelta(minutes=5),
                                                         timezone.get_default_timezone())

    # update lock expire time after each verify request.
    verify_entry.locked_expires = timezone.make_aware(datetime.datetime.today() + datetime.timedelta(minutes=1),
                                                      timezone.get_default_timezone())

    verify_entry.verify = verify

    # Send the generated passcode to client through SMS server.
    ret, code = sms_send_passcode(phone_number, verify_entry.passcode)
    if not ret:
        return statusCode.err_response_with_messages(statusCode.NRK_SERVER_ERR, code)

    try:
        verify_entry.save()
    except:
        statusCode.NRK_SERVER_ERR

    return statusCode.NRK_OK


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


# Check passcode is correct
def check_passcode(phone_number, passcode):
    try:
        verify_entry = SmsVerify.objects.get(phone_number=phone_number)
    except:
        return statusCode.NRK_SERVER_ERR

    if passcode != verify_entry.passcode:
        return statusCode.NRK_INVALID_PARAM_PASSCODE_INVALID

    if verify_entry.valid_expires < timezone.make_aware(datetime.datetime.today(), timezone.get_default_timezone()):
        return statusCode.NRK_INVALID_PARAM_PASSCODE_EXPIRED

    return statusCode.NRK_OK



