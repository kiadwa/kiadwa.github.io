from ELEC9609.API.Modules.Accounts import *
from ELEC9609.API.Modules.Payment import *
from ELEC9609.API.Modules.Pet import *
from ELEC9609.API.Modules.Pet_Avatar import *
from ELEC9609.API.Modules.Provider import *
from ELEC9609.API.Modules.Service_Order import *
from ELEC9609.API.Modules.Trainer import *
from ELEC9609.API.Modules.Trainer_Avatar import *
from ELEC9609.API.Modules.User import *
from ELEC9609.API.Modules.User_Avatar import *
from ELEC9609.API.Modules.AI_API import *

def request_user(request):

    assert 'token' in request.headers
    if request.method == 'GET':
        data_user = {}
        uid = request.GET.get('uid')
        if uid:
            assert uid.isdigit()
            data_user.update({'uid': int(uid)})
        dob = request.GET.get('dob')
        if dob:
            assert dob.replace('.', '', 1).isdigit() and float(dob) >= 0
            data_user.update({'dob': float(dob)})
        admin = request.GET.get('admin')
        if admin:
            assert admin.lower() in ['true', 'false']
            data_user.update({'admin': bool(admin)})
        verification = request.GET.get('verification')
        if verification:
            assert verification.lower() in ['true', 'false']
            data_user.update({'verification': bool(verification)})
        data_user.update({
            'l_name': request.GET.get('l_name'),
            'f_name': request.GET.get('f_name'),
            'email': request.GET.get('email'),
            'password': request.GET.get('password'),
            'description': request.GET.get('description')
        })
        return user_select({'token': request.headers['token'], 'user': data_user})
    elif request.method == 'POST':
        return user_register(get_request_data(request))
    elif request.method == 'PUT':
        return user_update(get_request_data(request))
    elif request.method == 'DELETE':
        return user_delete(get_request_data(request))
    return get_result(METHOD_NOT_ALLOWED, None, 'Method Not Allowed')


def request_user_avatar(request):
    assert 'token' in request.headers
    if request.method == 'GET':
        data_user_avatar = {}
        uid = request.GET.get('uid')
        if uid:
            assert uid.isdigit()
            data_user_avatar.update({'uid': int(uid)})
        data_user_avatar.update({
            'avatar': request.GET.get('avatar')
        })
        return user_avatar_select({'token': request.headers['token'], 'user_avatar': data_user_avatar})
    elif request.method == 'POST':
        return user_avatar_create(get_request_data(request))
    elif request.method == 'PUT':
        return user_avatar_update(get_request_data(request))
    elif request.method == 'DELETE':
        return user_avatar_delete(get_request_data(request))
    return get_result(METHOD_NOT_ALLOWED, None, 'Method Not Allowed')


def request_pet(request):
    assert 'token' in request.headers
    if request.method == 'GET':
        data_pet = {}
        pid = request.GET.get('pid')
        if pid:
            assert pid.isdigit()
            data_pet.update({'pid': int(pid)})
        uid = request.GET.get('uid')
        if uid:
            assert uid.isdigit()
            data_pet.update({'uid': int(uid)})
        age = request.GET.get('age')
        if age:
            assert age.isdigit()
            data_pet.update({'age': int(age)})
        dob = request.GET.get('dob')
        if dob:
            assert dob.replace('.', '', 1).isdigit() and float(dob) >= 0
            data_pet.update({'dob': float(dob)})
        data_pet.update({
            'p_name': request.GET.get('p_name'),
            'species': request.GET.get('species'),
            'breed': request.GET.get('breed'),
            'diagnosis': request.GET.get('diagnosis'),
        })
        return pet_select({'token': request.headers['token'], 'pet': data_pet})
    elif request.method == 'POST':
        return pet_create(get_request_data(request))
    elif request.method == 'PUT':
        return pet_update(get_request_data(request))
    elif request.method == 'DELETE':
        return pet_delete(get_request_data(request))
    return get_result(METHOD_NOT_ALLOWED, None, 'Method Not Allowed')


def request_pet_avatar(request):
    assert 'token' in request.headers
    if request.method == 'GET':
        data_pet_avatar = {}
        pid = request.GET.get('pid')
        if pid:
            assert pid.isdigit()
            data_pet_avatar.update({'pid': int(pid)})
        data_pet_avatar.update({
            'avatar': request.GET.get('avatar')
        })
        return pet_avatar_select({'token': request.headers['token'], 'pet_avatar': data_pet_avatar})
    elif request.method == 'POST':
        return pet_avatar_create(get_request_data(request))
    elif request.method == 'PUT':
        return pet_avatar_update(get_request_data(request))
    elif request.method == 'DELETE':
        return pet_avatar_delete(get_request_data(request))
    return get_result(METHOD_NOT_ALLOWED, None, 'Method Not Allowed')


def request_provider(request):
    assert 'token' in request.headers
    if request.method == 'GET':
        data_provider = {}
        provid = request.GET.get('provid')
        if provid:
            assert provid.isdigit()
            data_provider.update({'provid': int(provid)})
        verification = request.GET.get('verification')
        if verification:
            assert verification.lower() in ['true', 'false']
            data_provider.update({'verification': bool(verification)})
        data_provider.update({
            'provider_name': request.GET.get('provider_name'),
            'email': request.GET.get('email'),
            'password': request.GET.get('password'),
            'phone_number': request.GET.get('phone_number')
        })
        return provider_select({'token': request.headers['token'], 'provider': data_provider})
    elif request.method == 'POST':
        return provider_register(get_request_data(request))
    elif request.method == 'PUT':
        return provider_update(get_request_data(request))
    elif request.method == 'DELETE':
        return provider_delete(get_request_data(request))
    return get_result(METHOD_NOT_ALLOWED, None, 'Method Not Allowed')


def request_trainer(request):
    assert 'token' in request.headers
    if request.method == 'GET':
        data_trainer = {}
        tid = request.GET.get('tid')
        if tid:
            assert tid.isdigit()
            data_trainer.update({'tid': int(tid)})
        provid = request.GET.get('provid')
        if provid:
            assert provid.isdigit()
            data_trainer.update({'provid': int(provid)})
        dob = request.GET.get('dob')
        if dob:
            assert dob.replace('.', '', 1).isdigit() and float(dob) >= 0
            data_trainer.update({'dob': float(dob)})
        verification = request.GET.get('verification')
        if verification:
            assert verification.lower() in ['true', 'false']
            data_trainer.update({'verification': bool(verification)})
        data_trainer.update({
            'l_name': request.GET.get('l_name'),
            'f_name': request.GET.get('f_name'),
            'email': request.GET.get('email'),
            'password': request.GET.get('password')
        })
        return trainer_select({'token': request.headers['token'], 'trainer': data_trainer})
    elif request.method == 'POST':
        return trainer_register(get_request_data(request))
    elif request.method == 'PUT':
        return trainer_update(get_request_data(request))
    elif request.method == 'DELETE':
        return trainer_delete(get_request_data(request))
    return get_result(METHOD_NOT_ALLOWED, None, 'Method Not Allowed')


def request_trainer_avatar(request):
    assert 'token' in request.headers
    if request.method == 'GET':
        data_trainer_avatar = {}
        tid = request.GET.get('tid')
        if tid:
            assert tid.isdigit()
            data_trainer_avatar.update({'tid': int(tid)})
        data_trainer_avatar.update({
            'avatar': request.GET.get('avatar')
        })
        return trainer_avatar_select({'token': request.headers['token'], 'trainer_avatar': data_trainer_avatar})
    elif request.method == 'POST':
        return trainer_avatar_create(get_request_data(request))
    elif request.method == 'PUT':
        return trainer_avatar_update(get_request_data(request))
    elif request.method == 'DELETE':
        return trainer_avatar_delete(get_request_data(request))
    return get_result(METHOD_NOT_ALLOWED, None, 'Method Not Allowed')


def request_service_order(request):
    assert 'token' in request.headers
    if request.method == 'GET':
        data_service_order = {}
        order_id = request.GET.get('order_id')
        if order_id:
            assert order_id.isdigit()
            data_service_order.update({'order_id': int(order_id)})
        pid = request.GET.get('pid')
        if pid:
            assert pid.isdigit()
            data_service_order.update({'pid': int(pid)})
        uid = request.GET.get('uid')
        if uid:
            assert uid.isdigit()
            data_service_order.update({'uid': int(uid)})
        tid = request.GET.get('tid')
        if tid:
            assert tid.isdigit()
            data_service_order.update({'tid': int(tid)})
        order_date = request.GET.get('order_date')
        if order_date:
            assert order_date.replace('.', '', 1).isdigit() and float(order_date) >= 0
            data_service_order.update({'order_date': float(order_date)})
        cost = request.GET.get('cost')
        if cost:
            assert cost.isdigit()
            data_service_order.update({'cost': int(cost)})
        data_service_order.update({
            'service_type': request.GET.get('service_type'),
            'status': request.GET.get('status')
        })
        return service_order_select({'token': request.headers['token'], 'service_order': data_service_order})
    elif request.method == 'POST':
        return service_order_create(get_request_data(request))
    elif request.method == 'PUT':
        return service_order_update(get_request_data(request))
    elif request.method == 'DELETE':
        return service_order_delete(get_request_data(request))
    return get_result(METHOD_NOT_ALLOWED, None, 'Method Not Allowed')


def request_payment(request):
    assert 'token' in request.headers
    if request.method == 'GET':
        data_payment = {}
        paymentid = request.GET.get('paymentid')
        if paymentid:
            assert paymentid.isdigit()
            data_payment.update({'paymentid': int(paymentid)})
        order_id = request.GET.get('order_id')
        if order_id:
            assert order_id.isdigit()
            data_payment.update({'order_id': int(order_id)})
        data_payment.update({
            'payment_info': request.GET.get('payment_info')
        })
        return payment_select({'token': request.headers['token'], 'payment': data_payment})
    elif request.method == 'POST':
        return payment_create(get_request_data(request))
    elif request.method == 'PUT':
        return payment_update(get_request_data(request))
    elif request.method == 'DELETE':
        return payment_delete(get_request_data(request))
    return get_result(METHOD_NOT_ALLOWED, None, 'Method Not Allowed')

def request_pethelp(request):
    assert 'token' in request.headers
    if request.method == 'POST':
        return pet_help(get_request_data(request))
    return get_result(METHOD_NOT_ALLOWED, None, 'Method Not Allowed')
