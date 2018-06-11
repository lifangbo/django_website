
import os

MAJOR_STATUS = 'primaryStatus'
MINOR_STATUS = 'secondaryStatus'

NRK_OK = {MAJOR_STATUS:'OK'}

NRK_SERVER_ERR = {MAJOR_STATUS:'server_error'}, 500

NRK_SERVER_BUSY = {MAJOR_STATUS:'server_busy'}, 500

NRK_INVALID_OPERA_INVALID_METHOD = {MAJOR_STATUS:'invalid_operation', MINOR_STATUS:'invalid_method' }, 403
NRK_INVALID_OPERA_LOW_PRIVILEGE = {MAJOR_STATUS:'invalid_operation', MINOR_STATUS:'low_privilege' }, 403

NRK_INVALID_PARAM_UNKNOWN_ERR = { MAJOR_STATUS:'Invalid_parameter' ,MINOR_STATUS:'unknow_err'}, 400
NRK_INVALID_PARAM_ID_ERR = {MAJOR_STATUS:'Invalid_parameter', MINOR_STATUS:'invalid_id'}, 400
NRK_INVALID_PARAM_USR_PWD_ERR_MSG = {MAJOR_STATUS:'Invalid_parameter', MINOR_STATUS:'user_passwd_err'}
NRK_INVALID_PARAM_USR_PWD_ERR = {MAJOR_STATUS:'Invalid_parameter', MINOR_STATUS:'user_passwd_err'}, 400
NRK_INVALID_PARAM_PWD_TOO_SHORT = {MAJOR_STATUS:'Invalid_parameter', MINOR_STATUS:'password_too_short'}, 400
NRK_INVALID_PARAM_PWD_TOO_SIMILAR = {MAJOR_STATUS:'Invalid_parameter', MINOR_STATUS:'password_too_similar'}, 400
NRK_INVALID_PARAM_PWD_TOO_COMMON = {MAJOR_STATUS:'Invalid_parameter', MINOR_STATUS:'password_too_common'}, 400
NRK_INVALID_PARAM_PWD_ENTIR_NUM = {MAJOR_STATUS:'Invalid_parameter', MINOR_STATUS:'password_entirely_numeric'}, 400
NRK_INVALID_PARAM_WRONG_TIME_FORMAT = {MAJOR_STATUS:'Invalid_parameter', MINOR_STATUS:'Wrong_time_format'}, 400
NRK_INVALID_PARAM_USER_ALREADY_EXIST = {MAJOR_STATUS:'Invalid_parameter', MINOR_STATUS:'user_already_exist'}, 400



