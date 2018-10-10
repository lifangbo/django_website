# -*- coding: utf-8 -*-
import sys
from aliyunsdkdysmsapi.request.v20170525 import SendSmsRequest
from aliyunsdkdysmsapi.request.v20170525 import QuerySendDetailsRequest
from aliyunsdkcore.client import AcsClient
import uuid
from aliyunsdkcore.profile import region_provider
from aliyunsdkcore.http import method_type as MT
from aliyunsdkcore.http import format_type as FT
import const
import json


"""
短信业务调用接口示例，版本号：v20170525

Created on 2017-06-12

"""
try:
    reload(sys)
    sys.setdefaultencoding('utf8')
except NameError:
    pass
except Exception as err:
    raise err

# 注意：不要更改
REGION = "cn-hangzhou"
PRODUCT_NAME = "Dysmsapi"
DOMAIN = "dysmsapi.aliyuncs.com"

acs_client = AcsClient(const.ACCESS_KEY_ID, const.ACCESS_KEY_SECRET, REGION)
region_provider.add_endpoint(PRODUCT_NAME, REGION, DOMAIN)

def send_sms(business_id, phone_numbers, sign_name, template_code, template_param=None):
    smsRequest = SendSmsRequest.SendSmsRequest()
    # 申请的短信模板编码,必填
    smsRequest.set_TemplateCode(template_code)

    # 短信模板变量参数
    if template_param is not None:
        smsRequest.set_TemplateParam(template_param)

    # 设置业务请求流水号，必填。
    smsRequest.set_OutId(business_id)

    # 短信签名
    smsRequest.set_SignName(sign_name)
	
    # 数据提交方式
	# smsRequest.set_method(MT.POST)
	
	# 数据提交格式
    # smsRequest.set_accept_format(FT.JSON)
	
    # 短信发送的号码列表，必填。
    smsRequest.set_PhoneNumbers(phone_numbers)

    # 调用短信发送接口，返回json
    smsResponse = acs_client.do_action_with_exception(smsRequest)

    # TODO 业务处理

    return smsResponse


# Sign name list
SIGN_NAME_NUROTRON_CHN = "诺尔康"
SIGN_NAME_NUROTRON_EN = "NUROTRON"

# Template code list
TEMPLATE_CODE_PASSCODE = "SMS_147590173"
TEMPLATE_CODE_LOGIN_NOTICE = "SMS_147590172"


# Send one passcode to specified the phone number
def sms_send_passcode(phone_number, passcode):
    __business_id = uuid.uuid1()
    params = {}

    if isinstance(passcode, unicode):
        passcode = passcode.encode()

    params['code'] = ''.join(passcode)

    if phone_number.startswith('+86'):
        phone_number_cleaned = phone_number.replace('+86', '')
    else:
        phone_number_cleaned = phone_number.replace('+', '00')    # Internal code format: 00+国际区号+号码，如“0085200000000”

    response = send_sms(__business_id, phone_number_cleaned, SIGN_NAME_NUROTRON_CHN, TEMPLATE_CODE_PASSCODE, params)

    ret = json.loads(response)

    ret_status = True
    if ret.get('Code') != 'OK':
        ret_status = False

    return ret_status, ret.get('Code')
    #return ret_status, response


if __name__ == '__main__':
    __business_id = uuid.uuid1()
    #print(__business_id)
    params = "{\"code\":\"12345\"}"
	#params = u'{"name":"wqb","code":"12345678","address":"bz","phone":"13000000000"}'
    #print(send_sms(__business_id, "18516288394", "诺尔康", "SMS_147590173", params))
    print(sms_send_passcode('+8618516288394', '3516'))

