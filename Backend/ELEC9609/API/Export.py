from json.decoder import JSONDecodeError

from django.db import DataError
from django.http import FileResponse
from django.template.context_processors import csrf

from ELEC9609.API.Modules.Accounts import *
from ELEC9609.API.Modules.Payment import *
from ELEC9609.API.Modules.Pet import *
from ELEC9609.API.Modules.Pet_Avatar import *
from ELEC9609.API.Modules.Provider import *
from ELEC9609.API.Modules.Service_Order import *
from ELEC9609.API.Modules.Trainer import *
from ELEC9609.API.Modules.Trainer_Avatar import *
from ELEC9609.API.Modules.UploadFile import *
from ELEC9609.API.Modules.User import *
from ELEC9609.API.Modules.User_Avatar import *
from ELEC9609.Tools.Logger import TLogger


def get_csrf_token(request):
    """
    Get csrf token before use POST methods
    :param request: a GET request
    :return: the CSRF token stored in the COOKIES of input request
    """
    return csrf(request)['csrf_token']


def function(request):
    """
    Export functions
    :param request: body should be a JSON object or JSON string like {"function": "<function_name>", "data": "<required_data_for_called_function>"}
    :return: JsonResponse() like {'error_code': 'HTTP response code', 'data': 'data', 'error_msg': 'error_msg'}
    """
    try:
        if request.method != 'POST':
            return get_result(METHOD_NOT_ALLOWED, None, f'Method Not Allowed: {request.method}')
        func, data = get_function_data(request)
        TLogger.tlog(f'Received parameter: ''function'': 'f'{func}'', ''data'f': {data}')
        get_result(CLIENT_INVALID_PARAMETER, None, 'default')
        match func:
            case 'user_login':
                result = user_login(data)
            case 'provider_login':
                result = provider_login(data)
            case 'trainer_login':
                result = trainer_login(data)
            case 'user_register':
                result = user_register(data)
            case 'provider_register':
                result = provider_register(data)
            case 'trainer_register':
                result = trainer_register(data)
            case 'user_check_exists':
                result = user_check_exists(data)
            case 'provider_check_exists':
                result = provider_check_exists(data)
            case 'trainer_check_exists':
                result = trainer_check_exists(data)
            case 'user_update':
                result = user_update(data)
            case 'user_delete':
                result = user_delete(data)
            case 'user_select':
                result = user_select(data)
            case 'pet_update':
                result = pet_update(data)
            case 'pet_delete':
                result = pet_delete(data)
            case 'pet_create':
                result = pet_create(data)
            case 'pet_select':
                result = pet_select(data)
            case 'user_avatar_update':
                result = user_avatar_update(data)
            case 'user_avatar_delete':
                result = user_avatar_delete(data)
            case 'user_avatar_create':
                result = user_avatar_create(data)
            case 'user_avatar_select':
                result = user_avatar_select(data)
            case 'trainer_avatar_update':
                result = trainer_avatar_update(data)
            case 'trainer_avatar_delete':
                result = trainer_avatar_delete(data)
            case 'trainer_avatar_create':
                result = trainer_avatar_create(data)
            case 'trainer_avatar_select':
                result = trainer_avatar_select(data)
            case 'pet_avatar_update':
                result = pet_avatar_update(data)
            case 'pet_avatar_delete':
                result = pet_avatar_delete(data)
            case 'pet_avatar_create':
                result = pet_avatar_create(data)
            case 'pet_avatar_select':
                result = pet_avatar_select(data)
            case 'service_order_update':
                result = service_order_update(data)
            case 'service_order_delete':
                result = service_order_delete(data)
            case 'service_order_create':
                result = service_order_create(data)
            case 'service_order_select':
                result = service_order_select(data)
            case 'payment_update':
                result = payment_update(data)
            case 'payment_delete':
                result = payment_delete(data)
            case 'payment_create':
                result = payment_create(data)
            case 'payment_select':
                result = payment_select(data)
            case 'trainer_update':
                result = trainer_update(data)
            case 'trainer_delete':
                result = trainer_delete(data)
            case 'trainer_select':
                result = trainer_select(data)
            case 'provider_update':
                result = provider_update(data)
            case 'provider_delete':
                result = provider_delete(data)
            case 'provider_select':
                result = provider_select(data)
            case _:
                raise AssertionError(f'Invalid function name {func}')
        TLogger.tlog(f'Return result: {result}')
        return result
    except JSONDecodeError as e:
        TLogger.twarn(f'Invalid parameter: {e}.')
        return get_result(CLIENT_INVALID_PARAMETER, None, 'Invalid parameter')
    except AssertionError as e:
        TLogger.twarn(f'Invalid parameter: {e}.')
        return get_result(CLIENT_INVALID_PARAMETER, None, 'Invalid parameter')
    except DataError as e:
        TLogger.twarn(f'Invalid data format: {e}.')
        return get_result(CLIENT_INVALID_PARAMETER, None, 'Invalid data format')
    except Exception as e:
        TLogger.terror(e)
        return get_result(INTERNAL_SERVER_ERROR, None, 'Internal Server Error')


def upload_file(request):
    """

    :param request: FILES, header: {
            "token": "<token>",
            "X-CSRF-Token": "<csrf_token>"
        }
    :return: JsonResponse() like {'error_code': 200, 'data': 'data', 'error_msg': 'error_msg'}
    """
    try:
        if request.method != 'POST':
            return get_result(METHOD_NOT_ALLOWED, None, f'Method Not Allowed: {request.method}')
        return func_upload_file(request)
    except AssertionError as e:
        TLogger.twarn(f'Invalid parameter: {e}.')
        return get_result(CLIENT_INVALID_PARAMETER, None, 'Invalid parameter')
    except Exception as e:
        TLogger.terror(e)
        return get_result(INTERNAL_SERVER_ERROR, None, 'Internal Server Error')


def get_media_file(request, file_path):
    """

    :param file_path: the url of the file
    :param request: header: {
            "token": "<token>",
            "X-CSRF-Token": "<csrf_token>"
        }
    :return:
    """
    try:
        if request.method != 'GET':
            return get_json_response_result(METHOD_NOT_ALLOWED, None, f'Method Not Allowed: {request.method}')
        auth = get_authorisation({'token': request.headers['token']} if 'token' in request.headers else {})
        if auth['error_code'] != SUCCESS:
            return get_json_response(auth)
        filename = os.path.join(settings.MEDIA_ROOT, file_path)
        if not os.path.isfile(filename):
            return get_json_response_result(NOT_FOUND, None, 'File Not Found')
        return FileResponse(open(filename, 'rb'), as_attachment=True)
    except AssertionError as e:
        TLogger.twarn(f'Invalid parameter: {e}.')
        return get_json_response_result(CLIENT_INVALID_PARAMETER, None, 'Invalid parameter')
    except Exception as e:
        TLogger.terror(e)
        return get_json_response_result(INTERNAL_SERVER_ERROR, None, 'Internal Server Error')
