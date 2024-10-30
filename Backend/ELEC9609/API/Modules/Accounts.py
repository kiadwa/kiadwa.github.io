from datetime import timedelta

from ELEC9609.API.Modules.Base import *

"""
{
    ('a_type_name', 'email'): {
        'last_attempt': datetime.now(), 
        'attempts': 0
    }
}
"""
LOGIN_RECORDS = {}


def __account_login(data, a_type):
    a_type_name = get_model_data_key(a_type)
    data = get_data_by_model_type(data, a_type)

    assert 'email' in data and 'password' in data and type(data['email']) == str and type(data['password']) == str
    if (a_type_name, data['email']) in LOGIN_RECORDS:
        if datetime.now() - LOGIN_RECORDS[(a_type_name, data['email'])]['last_attempt'] < timedelta(seconds=10):
            return get_result(FALSE, None, 'Login rate limit, please login after 10 seconds')
    account = a_type.objects.filter(email=data['email']).first()
    if not account:
        return get_result(FALSE, None, f'{a_type_name} account {data['email']} does not exist')

    remove_logged_in_account_by_email(account.email, a_type)
    if datetime.now(UTC) - account.lockout < timedelta(minutes=30):
        return get_result(FALSE, None,
                          f'{a_type_name} account {data['email']} has been lockout until {account.lockout + timedelta(minutes=30)}')
    if not account.password == password_encrypt(data['password']):
        LOGIN_RECORDS.update({
            (a_type_name, data['email']): {
                'last_attempt': datetime.now(),
                'attempts': LOGIN_RECORDS[(a_type_name, data['email'])]['attempts'] + 1 if (a_type_name, data[
                    'email']) in LOGIN_RECORDS else 1
            }
        })
        if LOGIN_RECORDS[(a_type_name, data['email'])]['attempts'] >= 3:
            account.lockout = datetime.now(UTC)
            account.save()
            return get_result(FALSE, None, 'Wrong password and the account has been locked for 30 minutes')
        return get_result(FALSE, None, 'Wrong password')
    logged_in_account = get_logged_in_account_by_email(account.email, a_type)
    if logged_in_account:
        logged_in_account_info = get_logged_in_account_info(account.email, a_type)
        if type(logged_in_account_info) == dict and 'exp' in logged_in_account_info and 'email' in logged_in_account_info and type(
                logged_in_account_info['exp']) == float:
            if logged_in_account_info['exp'] > datetime.timestamp(datetime.now()) and logged_in_account_info[
                'email'] == account.email:
                TLogger.tlog(f'user_login: {logged_in_account_info['email']}')
                return get_result(SUCCESS, {'token': logged_in_account['token']},
                                  f'{a_type_name} account {data['email']} already logged in')
    token = jwt.encode(
        {'email': account.email, 'exp': datetime.timestamp(datetime.now() + timedelta(days=7)),
         'type': get_model_data_key(a_type)},
        JWT_KEY,
        algorithm='HS256')
        #algorithm='HS256'
    logging_in_account = {'email': account.email, 'token': token, 'type': get_model_data_key(a_type)}
    LOGGED_IN_ACCOUNTS.append(logging_in_account)
    if (a_type_name, data['email']) in LOGIN_RECORDS:
        LOGIN_RECORDS[(a_type_name, data['email'])].update({
            'last_attempt': datetime.now(),
            'attempts': 0
        })
        account.lockout = datetime.fromtimestamp(0.0, UTC)
        account.save()
    TLogger.tlog(f'user_login: {logging_in_account}')
    return get_result(SUCCESS, {'token': token}, f'{a_type_name} account {data['email']} logged in')


def __account_register(data, a_type, assertations, extra=None):
    a_type_name = get_model_data_key(a_type)
    data = get_data_by_model_type(data, a_type)
    assertations(data)
    if extra:
        exr = extra(data)
        if not exr['error_code'] == SUCCESS:
            return exr
    if a_type.objects.filter(email=data['email']).first():
        return get_result(FALSE, None, f'{a_type_name} account {data['email']} already exists')
    if 'dob' in data:
        data.update({'dob': datetime.fromtimestamp(data['dob'])})
    if 'admin' in data:
        data.update({'admin': False})
    pwd = data['password']
    if not 8 <= len(pwd) <= 16:
        return get_result(FALSE, None, 'The length of the password should between 8 and 16 characters')
    if not any(c in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ' for c in pwd):
        return get_result(FALSE, None, 'The password should contain at least one alphabet')
    if not any(c in '0123456789' for c in pwd):
        return get_result(FALSE, None, 'The password should contain at least one number')
    data.update({'password': password_encrypt(pwd)})
    account = a_type.objects.create(**data)
    TLogger.tlog(f'user_register: {account}')
    return get_result(SUCCESS, None, f'{a_type_name} account {data['email']} registered')


def __model_check_exists(data, m_type, key):
    data = get_data_by_model_type(data, m_type)
    assert key in data
    return get_result(SUCCESS, bool(m_type.objects.filter(**{key: data[key]}).first()))


def user_login(data):
    """

    :param data: 	{
        "user": {
            "email": "str",
            "password": "str"
        }
    }
    :return: 	{
        "error_code": 200,
        "data": {
            "token": "str"
        },
        "error_msg": "str?"
    }
    """
    return __account_login(data, User)


def provider_login(data):
    """

    :param data: 	{
        "provider": {
            "email": "str",
            "password": "str"
        }
    }
    :return: 	{
        "error_code": 200,
        "data": {
            "token": "str"
        },
        "error_msg": "str?"
    }
    """
    return __account_login(data, Provider)


def trainer_login(data):
    """

    :param data: 	{
        "trainer": {
            "email": "str",
            "password": "str"
        }
    }
    :return: 	{
        "error_code": 200,
        "data": {
            "token": "str"
        },
        "error_msg": "str?"
    }
    """
    return __account_login(data, Trainer)


def user_register(data):
    """

    :param data: 	{
        "user": {
            "l_name": "str",
            "f_name": "str",
            "email": "str",
            "dob": 1728805599.043506,
            "password": "str",
            "admin": false,
            "verification": false,
            "description": "str?"
        }
    }
    :return: 	{
        "error_code": 200,
        "data": null,
        "error_msg": "str?"
    }
    """

    def assertations(data):
        assert 'l_name' in data and 'f_name' in data and 'email' in data and 'dob' in data and 'password' in data and type(
            data['l_name']) == str and type(data['f_name']) == str and type(data['email']) == str and type(
            data['dob']) == float and type(data['password']) == str

    return __account_register(data, User, assertations)


def provider_register(data):
    """

    :param data: 	{
        "provider": {
            "provider_name": "str",
            "email": "str",
            "phone_number": "str",
            "password": "str",
            "verification": false
        }
    }
    :return: 	{
        "error_code": 200,
        "data": null,
        "error_msg": "str?"
    }
    """

    def assertations(data):
        assert 'provider_name' in data and 'email' in data and 'phone_number' in data and 'password' in data and type(
            data['provider_name']) == str and type(data['email']) == str and type(data['phone_number']) == str and type(
            data['password']) == str

    return __account_register(data, Provider, assertations)


def trainer_register(data):
    """

    :param data: 	{
        "trainer": {
            // int
            "provid": 0,
            "l_name": "str",
            "f_name": "str",
            "email": "str",
            "dob": 1728805599.043506,
            "password": "str",
            "verification": false
        }
    }
    :return: 	{
        "error_code": 200,
        "data": null,
        "error_msg": "str?"
    }
    """

    def assertations(data):
        assert 'provid' in data and 'l_name' in data and 'f_name' in data and 'dob' in data and 'email' in data and 'password' in data and type(
            data['provid']) == int and type(data['l_name']) == str and type(data['f_name']) == str and type(
            data['dob']) == float and type(data['email']) == str and type(data['password']) == str

    def extra(data):
        provider = Provider.objects.filter(provid=data['provid']).first()
        if not provider:
            return get_result(FALSE, None,
                              f'Trainer must register under a specific provider, but get invalid provid {data['provid']}')
        data.update({'provid': provider})
        return get_result(SUCCESS)

    return __account_register(data, Trainer, assertations, extra)


def user_check_exists(data):
    """

    :param data: 	{
        "user": {
            "email": "str"
        }
    }
    :return: 	{
        "error_code": 200,
        "data": true,
        "error_msg": "str?"
    }
    """
    return __model_check_exists(data, User, 'email')


def provider_check_exists(data):
    """

    :param data: 	{
        "provider": {
            "email": "str"
        }
    }
    :return: 	{
        "error_code": 200,
        "data": true,
        "error_msg": "str?"
    }
    """
    return __model_check_exists(data, Provider, 'email')


def trainer_check_exists(data):
    """

    :param data: 	{
        "trainer": {
            "email": "str"
        }
    }
    :return: 	{
        "error_code": 200,
        "data": true,
        "error_msg": "str?"
    }
    """
    return __model_check_exists(data, Trainer, 'email')
