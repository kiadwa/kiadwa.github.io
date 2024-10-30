import os
from json.decoder import JSONDecodeError

from django.db import DataError
from django.http.response import HttpResponse, FileResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from ELEC9609.API import Export
from ELEC9609.API.Export import get_csrf_token
from ELEC9609.API.REST import *
from ELEC9609.Tools.Logger import TLogger



def hello_world(request):
    print("Hello World")
    context = {
        'test': 'Hello World!'
    }
    return render(request, 'hello_world.html', context)


def hello_world_test(request, test_id):
    print('Current directory: ' + os.getcwd())
    print("test id: " + str(test_id))
    context = {
        'test': 'TEST'
    }
    if test_id == 1:
        with open('static/picture.jpg', 'rb') as f:
            context.update({'picture_base64': base64.b64encode(f.read()).decode('utf-8')})
    # return render(request, 'hello_world.html', context)
    return JsonResponse(context)

def verify_ssl(request, filename):
    try:
        file = open(os.path.join('.well-known/pki-validation/', filename), 'rb')
        return FileResponse(file, as_attachment=True)
    except Exception as e:
        TLogger.terror(e)
        return get_json_response_result(INTERNAL_SERVER_ERROR)



@csrf_exempt
def api(request):
    context = Export.function(request)
    return JsonResponse(context)


def api_cookies_get_csrf_token(request):
    try:
        response = HttpResponse()
        response.set_cookie('csrf_token', get_csrf_token(request))
        return response
    except Exception as e:
        TLogger.terror(e)
        return render(request, 'null.html', {})


def api_get_csrf_token(request):
    try:
        # Generate the CSRF token
        csrf_token = request.COOKIES.get('csrftoken') or get_csrf_token(request)
        str_token = str(csrf_token)
        print(csrf_token)
        # Create the JsonResponse and set the token as data
        response = JsonResponse({'csrftoken': str_token})
        # Set the CSRF token as a cookie
        response.set_cookie(
            'csrftoken',
            csrf_token,
            samesite='Strict',
            secure=True
        )
        # Optionally, set the token as a custom header
        response['X-CSRFToken'] = str_token
        return response
    except Exception as e:
        TLogger.terror(e)
        return JsonResponse({'error': 'Failed to generate CSRF token'}, status=500)

@csrf_exempt
def api_upload_file(request):
    result = Export.upload_file(request)
    return JsonResponse(result, status=result['error_code'])


def rest(func):
    try:
        return func()
    except JSONDecodeError as e:
        print('this')
        TLogger.twarn(f'Invalid parameter: {e}.')
        return get_json_response_result(CLIENT_INVALID_PARAMETER, None, 'Invalid parameter')
    #except AssertionError as e:
     #   print('this')
     #   TLogger.twarn(f'Invalid parameter: {e}.')
     #   return get_json_response_result(CLIENT_INVALID_PARAMETER, None, 'Invalid parameter')
    except DataError as e:
        TLogger.twarn(f'Invalid data format: {e}.')
        return get_json_response_result(CLIENT_INVALID_PARAMETER, None, 'Invalid data format')
    except Exception as e:
        TLogger.terror(e)
        return get_json_response_result(INTERNAL_SERVER_ERROR, None, 'Internal Server Error')

@csrf_exempt
def rest_user(request):
    #print(request.body)
    def func():
        result = request_user(request)
        return JsonResponse(result, status=result['error_code'])
    return rest(func)

@csrf_exempt
def rest_user_avatar(request):
    def func():
        result = request_user_avatar(request)
        return JsonResponse(result, status=result['error_code'])

    return rest(func)

@csrf_exempt
def rest_pet(request):
    def func():
        result = request_pet(request)
        return JsonResponse(result, status=result['error_code'])

    return rest(func)

@csrf_exempt
#this
def rest_pethelp_ai(request):
    def func():
        print(request)
        result = request_pethelp(request)
        return JsonResponse(result, status=result['error_code'])
    
    return rest(func)

@csrf_exempt
def rest_pet_avatar(request):
    def func():
        result = request_pet_avatar(request)
        return JsonResponse(result, status=result['error_code'])
    
    return rest(func)

@csrf_exempt
def rest_provider(request):
    def func():
        result = request_provider(request)
        return JsonResponse(result, status=result['error_code'])

    return rest(func)

@csrf_exempt
def rest_trainer(request):
    def func():
        result = request_trainer(request)
        return JsonResponse(result, status=result['error_code'])

    return rest(func)

@csrf_exempt
def rest_trainer_avatar(request):
    def func():
        result = request_trainer_avatar(request)
        return JsonResponse(result, status=result['error_code'])

    return rest(func)

@csrf_exempt
def rest_service_order(request):
    def func():
        result = request_service_order(request)
        return JsonResponse(result, status=result['error_code'])

    return rest(func)

@csrf_exempt
def rest_payment(request):
    def func():
        result = request_payment(request)
        return JsonResponse(result, status=result['error_code'])

    return rest(func)

@csrf_exempt
def get_media_file(request, file_path):
    return Export.get_media_file(request, file_path)


def index(request):
    return render(request, 'index.html')
