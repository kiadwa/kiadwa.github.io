import hashlib
import json
from datetime import datetime

import jwt
from django.http import JsonResponse

from ELEC9609.Tools.Logger import TLogger
from ELEC9609.models import *

"""
[{
    "token": "<token>",
    "email": "<email>",
    // should be one of models
    "type": User
}]
"""

LOGGED_IN_ACCOUNTS = []

SUCCESS = 200
FALSE = 204
UNAUTHORIZED = 401
CLIENT_INVALID_PARAMETER = 400
NOT_FOUND = 404
METHOD_NOT_ALLOWED = 405
INTERNAL_SERVER_ERROR = 500
JWT_KEY = '6446f12aeb4741dca83c31ba8ea5b3dc'


def get_result(error_code=SUCCESS, data=None, error_msg=None):
    return {'error_code': error_code, 'data': data, 'error_msg': error_msg}


def get_json_response(result):
    return JsonResponse(result, status=result['error_code'])


def get_json_response_result(error_code=SUCCESS, data=None, error_msg=None):
    return JsonResponse(get_result(error_code=error_code, data=data, error_msg=error_msg), status=error_code)


def get_function_data(request):
    data = json.loads(request.body)
    assert type(data) == dict and 'function' in data and type(data['function']) == str and 'data' in data and type(
        data['data']) == dict
    if 'token' in request.headers:
        assert type(request.headers['token']) == str
        data['data'].update({'token': request.headers['token']})
    return data['function'], data['data']


def get_request_data(request):
    print(request)
    data = json.loads(request.body)
    assert type(data) == dict and 'data' in data and type(
        data['data']) == dict
    if 'token' in request.headers:
        assert type(request.headers['token']) == str
        data['data'].update({'token': request.headers['token']})
    return data['data']


def get_data_by_model_type(data, m_type):
    m_type_name = get_model_data_key(m_type)
    assert m_type_name in data and type(data[m_type_name]) == dict
    return data[m_type_name]


def remove_redundant_data(dic, list_target):
    redundant_data = []
    for k, v in dic.items():
        if not k in list_target or v is None:
            redundant_data.append(k)
    for k in redundant_data:
        dic.pop(k)
    return dic


def get_logged_in_account(token):
    for logged_in_user in LOGGED_IN_ACCOUNTS:
        if logged_in_user['token'] == token:
            return logged_in_user
    return None


def get_logged_in_account_by_email(email, a_type):
    for logged_in_account in LOGGED_IN_ACCOUNTS:
        if logged_in_account['email'] == email and logged_in_account['type'] == get_model_data_key(a_type):
            return logged_in_account
    return None


def remove_logged_in_account_by_email(email, a_type):
    for i in range(len(LOGGED_IN_ACCOUNTS)):
        if LOGGED_IN_ACCOUNTS[i]['email'] == email and LOGGED_IN_ACCOUNTS[i]['type'] == get_model_data_key(a_type):
            TLogger.tlog(f'LOGGED_IN_USERS: {LOGGED_IN_ACCOUNTS.pop(i)} has been removed')
            break


def get_logged_in_account_info(email, a_type):
    try:
        return jwt.decode(get_logged_in_account_by_email(email, a_type)['token'], JWT_KEY, algorithms=['HS256'])
    except Exception as e:
        TLogger.terror(f'Invalid JWT: {e}')
        return None


def get_model_data_key(m_type):
    if m_type == User:
        return 'user'
    elif m_type == Trainer:
        return 'trainer'
    elif m_type == Provider:
        return 'provider'
    elif m_type == Payment:
        return 'payment'
    elif m_type == Pet:
        return 'pet'
    elif m_type == Pet_Avatar:
        return 'pet_avatar'
    elif m_type == Service_Order:
        return 'service_order'
    elif m_type == Trainer_Avatar:
        return 'trainer_avatar'
    elif m_type == User_Avatar:
        return 'user_avatar'
    else:
        return None


def get_model_type_by_data_key(data_key):
    match data_key:
        case 'user':
            return User
        case 'trainer':
            return Trainer
        case 'provider':
            return Provider
        case 'payment':
            return Payment
        case 'pet':
            return Pet
        case 'pet_avatar':
            return Pet_Avatar
        case 'service_order':
            return Service_Order
        case 'trainer_avatar':
            return Trainer_Avatar
        case 'user_avatar':
            return User_Avatar
        case _:
            return None


def get_authorisation(data):
    if not 'token' in data:
        return get_result(UNAUTHORIZED, None, 'Unauthorized no token')
    logged_in_account = get_logged_in_account(data['token'])
    if not logged_in_account:
        return get_result(UNAUTHORIZED, None, 'Unauthorized not log in')
    a_type = get_model_type_by_data_key(logged_in_account['type'])
    logged_in_account_info = get_logged_in_account_info(logged_in_account['email'], a_type)
    if type(logged_in_account_info) == dict and 'exp' in logged_in_account_info and 'email' in logged_in_account_info and type(
            logged_in_account_info['exp']) == float:
        if logged_in_account_info['exp'] > datetime.timestamp(datetime.now()):
            return get_result(SUCCESS, logged_in_account)
    # token expired
    return get_result(UNAUTHORIZED, None, 'Unauthorized token expired')


def list_str_to_timestamp(model_list):
    for model in model_list:
        if 'dob' in model and model['dob']:
            model.update({'dob': datetime.timestamp(datetime.strptime(str(model['dob']), '%Y-%m-%d'))})
        if 'order_date' in model and model['order_date']:
            model.update({'order_date': datetime.timestamp(model['order_date'])})
        if 'lockout' in model and model['lockout']:
            model.update({'lockout': datetime.timestamp(model['lockout'])})
    return model_list


def password_encrypt(pwd):
    md5 = hashlib.md5()
    md5.update(pwd.encode())
    result = md5.hexdigest()
    return result
