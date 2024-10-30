from django.forms import model_to_dict

from ELEC9609.API.Modules.Base import *
from ELEC9609.settings import TIME_ZONE


def __user_operate(data, update_or_delete):
    auth = get_authorisation(data)
    if not auth['error_code'] == 200:
        return auth
    if not auth['data']['type'] == get_model_data_key(User):
        return get_result(FALSE, None, f'Your account type {auth['data']['type']} has no permission to do that.')
    # Current logged-in user, as operator
    operator_user_email = auth['data']['email']
    # User being operated
    operating_user = User.objects.filter(email=data['user']['email']).first()
    if not operating_user:
        return get_result(FALSE, None, f'Operating user {data['user']['email']} is not exist')

    updating_data = None
    if update_or_delete:
        # Data for updating
        updating_data = remove_redundant_data(data['user_new'], [f.name for f in User._meta.get_fields()])
        if 'email' in updating_data and updating_data['email'] != operator_user_email and User.objects.filter(email=updating_data['email']).first():
            return get_result(FALSE, None, f'Operator user {operator_user_email} attempt to change email {data['user']['email']}, but target email {updating_data['email']} already exists')
        if 'uid' in updating_data:
            updating_data.pop('uid')
            TLogger.twarn(f'Removed auto field uid in updating data')
        if 'dob' in updating_data:
            updating_data.update({'dob': datetime.fromtimestamp(updating_data['dob'])})
        if 'lockout' in updating_data:
            updating_data.update({'lockout': datetime.fromtimestamp(updating_data['lockout'], UTC)})



    # User update by self
    if operator_user_email == data['user']['email']:
        if update_or_delete:
            # Prevent permission change by normal user
            if 'admin' in updating_data and not operating_user.admin:
                updating_data.pop('admin')
                TLogger.twarn(f'User {operator_user_email} attempt to update permission but not admin')
            TLogger.tlog(f'password: {updating_data['password']}')
            if 'password' in updating_data and updating_data['password']:
                updating_data.update({'password': password_encrypt(updating_data['password'])})
            original_email, original_password = operating_user.email, operating_user.password
            operating_user.__dict__.update(**updating_data)
            operating_user.save()
            TLogger.tlog(f'user_update: {data["user"]} to {data["user_new"]}')
            if 'email' in updating_data and not original_email == updating_data[
                'email'] or 'password' in updating_data and not original_password == updating_data['password']:
                remove_logged_in_account_by_email(data['user']['email'], User)
                TLogger.tlog(f'email or password changed, log out user {original_email}')
            return get_result(SUCCESS, None, 'User updated')
        else:
            operating_user.delete()
            remove_logged_in_account_by_email(data['user']['email'], User)
            TLogger.tlog(f'user {data['user']['email']} deleted')
            return get_result(SUCCESS, None, 'User deleted')
    # Admin operation
    operator_user = User.objects.filter(email=operator_user_email).first()
    if not operator_user:
        return get_result(FALSE, None, f'Operator user {operator_user_email} is not exist')
    if not operator_user.admin:
        return get_result(FALSE, None, f'Operator user {operator_user_email} is not admin')
    if update_or_delete:
        if 'password' in updating_data and updating_data['password']:
            updating_data.update({'password': password_encrypt(updating_data['password'])})
        original_email, original_password = operating_user.email, operating_user.password
        operating_user.__dict__.update(**updating_data)
        operating_user.save()
        TLogger.tlog(f'user_update: {data["user"]} to {data["user_new"]}, by admin: {operator_user_email}')
        if 'email' in updating_data and not original_email == updating_data[
            'email'] or 'password' in updating_data and not original_password == updating_data['password']:
            remove_logged_in_account_by_email(data['user']['email'], User)
            TLogger.tlog(f'email or password changed, log out user {operating_user.email}')
        return get_result(SUCCESS, None, f'User updated by admin {operator_user_email}')
    else:
        operating_user.delete()
        remove_logged_in_account_by_email(data['user']['email'], User)
        TLogger.tlog(f'user {data['user']['email']} deleted')
        return get_result(SUCCESS, None, f'User deleted by admin {operator_user_email}')


def user_update(data):
    """
    Authorised account types: User,
    if not admin, user can only update his own data,
    if email or password changed, login again required,
    if not admin, user cannot update admin columns
    :param data: 	{
            "token": "<token>",
            "user": {
                // user who want to update
                "email": "str",
            },
            "user_new": {
                // what you want to update
                "l_name": "str",
                "f_name": "str",
                "email": "str",
                "dob": 1728805599.043506,
                "password": "str",
                "admin": false,
                "description": "str?",
                "lockout": 1728805599.043506
            }
        }
    :return:	{
            "error_code": 200,
            "data": null,
            "error_msg": "str?"
        }
    """

    assert 'user' in data and type(data['user']) == dict and 'email' in data[
        'user'] and 'user_new' in data and type(
        data['user_new']) == dict

    return __user_operate(data, True)


def user_delete(data):
    """
    Authorised account types: User,
    if not admin, user can only delete his own data,
    deleted account will log out
    :param data: 	{
            "token": "<token>",
            "user": {
                "email": "str",
            }
        }
    :return:	{
            "error_code": 200,
            "data": null,
            "error_msg": "str?"
        }
    """
    assert 'user' in data and type(data['user']) == dict and 'email' in data['user']

    return __user_operate(data, False)


def user_select(data):
    """
    Authorised account types: Any,
    if not admin, some data will not return
    :param data: 	{
            // Can not exist, but some data will not return if unauthorised
            "token": "<token>",
            // filter
            "user": {
                "l_name": "al",
                "f_name": "af",
                "email": "3@e.com",
                "dob": 1728805599.043506,
                "password": "str",
                "admin": false,
                "description": "str?",
                "lockout": 1728805599.043506
            }
        }
    :return: 	{
            "error_code": 200,
            "data": {
                "user_list": [
                    {
                        "uid": 0,
                        "l_name": "al",
                        "f_name": "af",
                        "email": "3@e.com",
                        "dob": 1728805599.043506,
                        // if not admin, not include this
                        "password": "str",
                        "admin": false,
                        "lockout": 1728805599.043506
                        "description": "str?"
                    }
                ]
            },
            "error_msg": "str?"
        }
    """

    def remove_private_data(users):
        for u in users:
            u.pop('password')
            u.pop('admin')
        return users

    auth = get_authorisation(data)
    if not auth['error_code'] == 200:
        if not 'user' in data:
            return get_result(SUCCESS, {
                'user_list': list_str_to_timestamp(
                    remove_private_data([model_to_dict(m) for m in User.objects.filter()]))},
                              f'Unauthorised user execute select')
        user = data['user']
        if 'dob' in user:
            user.update(dob=datetime.fromtimestamp(user['dob']))
        if 'lockout' in user:
            user.update(lockout=datetime.fromtimestamp(user['lockout']))
        if 'password' in user:
            user.pop('password')
            TLogger.tlog(f'Unauthorised user attempt to filter user by password, remove filter')
        if 'admin' in user:
            user.pop('admin')
            TLogger.tlog(f'Unauthorised user attempt to filter user by admin, remove filter')
        return get_result(SUCCESS,
                          {'user_list': list_str_to_timestamp(remove_private_data(
                              [model_to_dict(m) for m in User.objects.filter(
                                  **remove_redundant_data(user,
                                                          [f.name for f in User._meta.get_fields()]))]))})

    operator_type = get_model_type_by_data_key(auth['data']['type'])

    # Current logged-in user, as operator
    operator_email = auth['data']['email']
    operator = operator_type.objects.filter(email=operator_email).first()

    if not operator:
        return get_result(FALSE, None, f'Operator user {operator_email} is not exist')

    if not 'user' in data:
        if operator_type == User and operator.admin:
            return get_result(SUCCESS,
                              {'user_list': list_str_to_timestamp([model_to_dict(m) for m in User.objects.filter()])})
        else:
            return get_result(SUCCESS, {
                'user_list': remove_private_data(
                    list_str_to_timestamp([model_to_dict(m) for m in User.objects.filter()]))},
                              f'Operator {auth['data']['type']} {operator_email} is not admin')

    user = data['user']
    if 'dob' in user:
        user.update(dob=datetime.fromtimestamp(user['dob']))
    if 'lockout' in user:
        user.update(lockout=datetime.fromtimestamp(user['lockout'], UTC))
    # Not admin, try filter password
    if (operator_type == User and not operator.admin or operator_type != User) and 'password' in user:
        user.pop('password')
        TLogger.tlog(
            f'{auth['data']['type']} {operator_email} attempt to filter user by password but not admin, remove filter')
    # Not admin, try filter admin
    if (operator_type == User and not operator.admin or operator_type != User) and 'admin' in user:
        user.pop('admin')
        TLogger.tlog(
            f'{auth['data']['type']} {operator_email} attempt to filter user by admin but not admin, remove filter')

    if operator_type == User and operator.admin:
        return get_result(SUCCESS, {'user_list': list_str_to_timestamp([model_to_dict(m) for m in User.objects.filter(
            **remove_redundant_data(user, [f.name for f in User._meta.get_fields()]))])})
    else:
        return get_result(SUCCESS,
                          {'user_list': list_str_to_timestamp(remove_private_data(
                              [model_to_dict(m) for m in User.objects.filter(
                                  **remove_redundant_data(user,
                                                          [f.name for f in User._meta.get_fields()]))]))})
