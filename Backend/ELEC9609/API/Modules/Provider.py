from django.forms import model_to_dict

from ELEC9609.API.Modules.Base import *


def __provider_operate(data, update_or_delete):
    auth = get_authorisation(data)
    if not auth['error_code'] == 200:
        return auth

    a_type_name = auth['data']['type']
    a_type = get_model_type_by_data_key(a_type_name)

    if not a_type_name == get_model_data_key(User) and not a_type_name == get_model_data_key(Provider):
        return get_result(FALSE, None, f'Your account type {a_type_name} has no permission to do that.')

    operator = a_type.objects.filter(email=auth['data']['email']).first()

    if not operator:
        return get_result(FALSE, None, f'Operator {a_type_name} {auth['data']['email']} is not exist')

    admin = False
    if a_type_name == get_model_data_key(User):
        admin = operator.admin

    operating_provider = Provider.objects.filter(email=data['provider']['email']).first()

    if not admin and (a_type != Provider or a_type == Provider and operating_provider.provid != operator.provid):
        return get_result(FALSE, None,
                          f'Operating provider {data['provider']['email']} is not {a_type_name} {auth['data']['email']} and user is not admin')

    # admin or own data
    if update_or_delete:
        updating_data = remove_redundant_data(data['provider_new'], [f.name for f in Provider._meta.get_fields()])
        if 'email' in updating_data and updating_data['email'] != operator.email and Provider.objects.filter(
                email=updating_data['email']).first():
            return get_result(FALSE, None,
                              f'Operator {a_type_name} {operator.email} attempt to change email {data['provider']['email']}, but target email {updating_data['email']} already exists')
        if 'provid' in updating_data:
            updating_data.pop('provid')
            TLogger.twarn(f'Removed auto field tid in updating_data')
        if 'password' in updating_data:
            updating_data.update({'password': password_encrypt(updating_data['password'])})
        if 'lockout' in updating_data:
            updating_data.update({'lockout': datetime.fromtimestamp(updating_data['lockout'], UTC)})
        original_email, original_password = operating_provider.email, operating_provider.password
        operating_provider.__dict__.update(**updating_data)
        operating_provider.save()
        if 'email' in updating_data and not original_email == updating_data[
            'email'] or 'password' in updating_data and not original_password == updating_data['password']:
            remove_logged_in_account_by_email(data['provider']['email'], Provider)
            TLogger.tlog(f'email or password changed, log out provider {original_email}')
        TLogger.tlog(
            f'provider_update: {data['provider']} to {data['provider_new']}')
        return get_result(SUCCESS, None, 'Provider updated')
    else:
        operating_provider.delete()
        remove_logged_in_account_by_email(data['provider']['email'], Provider)
        TLogger.tlog(f'provider_delete: {data['provider']}')
        return get_result(SUCCESS, None, 'Provider deleted')


def provider_update(data):
    """
    Authorised account types: User, Provider,
    if not admin, user can only update his own data,
    if email or password changed, login again required,
    if not admin, user cannot update lockout or admin columns
    :param data: 	{
            "token": "<token>",
            "provider": {
                // provider who want to update
                "email": "str",
            },
            "provider_new": {
                // what you want to update
                "provider_name": "str",
                "email": "str",
                "password": "str",
                "phone_number": "str",
                "lockout": 1728805599.043506
            }
        }
    :return:	{
            "error_code": 200,
            "data": null,
            "error_msg": "str?"
        }
    """

    assert 'provider' in data and type(data['provider']) == dict and 'email' in data[
        'provider'] and 'provider_new' in data and type(
        data['provider_new']) == dict

    return __provider_operate(data, True)


def provider_delete(data):
    """
    Authorised account types: User, Provider,
    if not admin, user can only delete his own data,
    deleted account will log out
    :param data: 	{
            "token": "<token>",
            "provider": {
                "email": "str",
            }
        }
    :return:	{
            "error_code": 200,
            "data": null,
            "error_msg": "str?"
        }
    """
    assert 'provider' in data and type(data['provider']) == dict and 'email' in data['provider']

    return __provider_operate(data, False)


def provider_select(data):
    """
    Authorised account types: Any,
    if not admin, some data will not return
    :param data: 	{
            // Can not exist, but some data will not return if unauthorised
            "token": "<token>",
            // filter
            "provider": {
                "provid: 0,
                "provider_name": "str",
                "email": "str",
                "password": "str",
                "phone_number": "str",
                "lockout": 1728805599.043506
            }
        }
    :return: 	{
            "error_code": 200,
            "data": {
                "provider_list": [
                    {
                        "provid: 0,
                        "provider_name": "str",
                        "email": "str",
                        "password": "str",
                        "phone_number": "str",
                        "lockout": 1728805599.043506
                    }
                ]
            },
            "error_msg": "str?"
        }
    """

    def remove_private_data(provider):
        for t in provider:
            t.pop('password')
        return provider

    auth = get_authorisation(data)
    if not auth['error_code'] == 200:
        if not 'provider' in data:
            return get_result(SUCCESS, {
                'provider_list': list_str_to_timestamp(
                    remove_private_data([model_to_dict(m) for m in Provider.objects.filter()]))},
                              f'Unauthorised user execute select')
        provider = data['provider']
        if 'password' in provider:
            provider.pop('password')
            TLogger.tlog(f'Unauthorised user attempt to filter provider by password, remove filter')
        return get_result(SUCCESS,
                          {'provider_list': list_str_to_timestamp(remove_private_data(
                              [model_to_dict(m) for m in Provider.objects.filter(
                                  **remove_redundant_data(provider,
                                                          [f.name for f in Provider._meta.get_fields()]))]))})

    operator_type = get_model_type_by_data_key(auth['data']['type'])

    # Current logged-in user, as operator
    operator_email = auth['data']['email']
    operator = operator_type.objects.filter(email=operator_email).first()

    if not operator:
        return get_result(FALSE, None, f'Operator {operator_type} {operator_email} is not exist')

    admin = False
    if operator_type == User:
        admin = operator.admin

    if not 'provider' in data:
        if admin:
            return get_result(SUCCESS,
                              {'provider_list': list_str_to_timestamp(
                                  [model_to_dict(m) for m in Provider.objects.filter()])})
        else:
            return get_result(SUCCESS, {
                'provider_list': remove_private_data(
                    list_str_to_timestamp([model_to_dict(m) for m in Provider.objects.filter()]))},
                              f'Operator {auth['data']['type']} {operator_email} is not admin')

    provider = data['provider']
    # Not admin, try filter password
    if not admin and 'password' in provider:
        provider.pop('password')
        TLogger.tlog(
            f'{auth['data']['type']} {operator_email} attempt to filter provider by password but not admin, remove filter')

    if admin:
        return get_result(SUCCESS,
                          {'provider_list': list_str_to_timestamp([model_to_dict(m) for m in Provider.objects.filter(
                              **remove_redundant_data(provider, [f.name for f in Provider._meta.get_fields()]))])})
    else:
        return get_result(SUCCESS,
                          {'provider_list': list_str_to_timestamp(remove_private_data(
                              [model_to_dict(m) for m in Provider.objects.filter(
                                  **remove_redundant_data(provider,
                                                          [f.name for f in Provider._meta.get_fields()]))]))})
