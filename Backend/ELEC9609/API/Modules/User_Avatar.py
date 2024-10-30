from django.forms import model_to_dict

from ELEC9609.API.Modules.Base import *


def __user_avatar_operate(data, update_or_delete):
    auth = get_authorisation(data)
    if not auth['error_code'] == 200:
        return auth
    if not auth['data']['type'] == get_model_data_key(User):
        return get_result(FALSE, None, f'Your account type {auth['data']['type']} has no permission to do that.')

    operator = User.objects.filter(email=auth['data']['email']).first()
    if not operator:
        return get_result(FALSE, None, f'Operator user {auth['data']['email']} is not exist')

    operating_user_avatar = User_Avatar.objects.filter(uid=data['user_avatar']['uid']).first()
    if not operating_user_avatar:
        return get_result(FALSE, None, f'Operating user_avatar {data['user_avatar']['uid']} is not exist')

    if not operator.admin and operating_user_avatar.uid != operator:
        return get_result(FALSE, None,
                          f'Operating user_avatar {data['user_avatar']['uid']} is not belong to user {auth['data']['email']} and user is not admin')

    if update_or_delete:
        # Data for updating
        updating_data = remove_redundant_data(data['user_avatar_new'],
                                              [f.name for f in User_Avatar._meta.get_fields()])
        if 'uid' in updating_data:
            updating_data.pop('uid')
            TLogger.twarn(f'Removed auto field uid in updating data')
        # if 'avatar' in updating_data and updating_data['avatar']:
        #     updating_data.update({'avatar': base64.b64decode(updating_data['avatar'])})
        operating_user_avatar.__dict__.update(**updating_data)
        operating_user_avatar.save()
        TLogger.tlog(f'user_avatar_update: {data['user_avatar']} to {data['user_avatar_new']}')
        return get_result(SUCCESS, None, 'User_Avatar updated')
    else:
        operating_user_avatar.delete()
        TLogger.tlog(f'user_avatar_delete: {data['user_avatar']}')
        return get_result(SUCCESS, None, 'User_Avatar deleted')


def user_avatar_update(data):
    """
    Authorised account types: User,
    if not admin, user can only update avatar belong to user
    :param data: {
            "token": "<token>",
            "user_avatar": {
                "uid": 0,
            },
            "user_avatar_new": {
                "avatar": "base64 str"
            }
        }
    :return: {
            "error_code": 200,
            "data": null,
            "error_msg": "str?"
        }
    """
    assert 'user_avatar' in data and type(data['user_avatar']) == dict and 'uid' in data[
        'user_avatar'] and 'user_avatar_new' in data and type(data['user_avatar_new']) == dict
    return __user_avatar_operate(data, True)


def user_avatar_delete(data):
    """
    Authorised account types: User,
    if not admin, user can only delete avatar belong to user
    :param data: {
            "token": "<token>",
            "user_avatar": {
                "uid": 0
            }
        }
    :return: {
            "error_code": 200,
            "data": null,
            "error_msg": "str?"
        }
    """
    assert 'user_avatar' in data and type(data['user_avatar']) == dict and 'uid' in data['user_avatar']
    return __user_avatar_operate(data, False)


def user_avatar_create(data):
    """
    Authorised account types: User,
    create an avatar belong to user
    :param data: {
            "token": "<token>",
            "user_avatar": {
                "avatar": "base64 str"
            }
        }
    :return: {
            "error_code": 200,
            "data": null,
            "error_msg": "str?"
        }
    """

    assert 'user_avatar' in data and type(data['user_avatar']) == dict
    user_avatar_data = data['user_avatar']

    auth = get_authorisation(data)
    if not auth['error_code'] == 200:
        return auth
    if not auth['data']['type'] == get_model_data_key(User):
        return get_result(FALSE, None, f'Your account type {auth['data']['type']} has no permission to do that.')

    operator = User.objects.filter(email=auth['data']['email']).first()
    if not operator:
        return get_result(FALSE, None, f'Operator user {auth['data']['email']} is not exist')

    if User_Avatar.objects.filter(uid=operator).first():
        return get_result(FALSE, None, f'Operator {auth['data']['email']} user_avatar {operator.uid} already exists')

    user_avatar_data.update({'uid': operator})
    # if 'avatar' in user_avatar_data and user_avatar_data['avatar']:
    #     user_avatar_data.update({'avatar': base64.b64decode(user_avatar_data['avatar'])})
    User_Avatar.objects.create(**user_avatar_data)
    # TLogger.tlog(f'user_avatar_create: {user_avatar_data}')
    return get_result(SUCCESS, None, 'User_Avatar created')


def user_avatar_select(data):
    """
    Authorised account types: Any,
    :param data: 	{
            // Can not exist, but some data will not return if unauthorised
            "token": "<token>",
            // filter
            "user_avatar": {
                "uid": 0,
                "avatar": "base64 str"
            }
        }
    :return: 	{
            "error_code": 200,
            "data": {
                "user_avatar_list": [
                    {
                        "uid": 0,
                        "avatar": "base64 str"
                    }
                ]
            },
            "error_msg": "str?"
        }
    """

    assert 'user_avatar' in data and type(data['user_avatar']) == dict

    user_avatar = data['user_avatar']

    if 'uid' in user_avatar:
        user = User.objects.filter(uid=user_avatar['uid']).first()
        if not user:
            return get_result(SUCCESS, {'user_avatar_list': []}, f'User {data['user_avatar']['uid']} is not exist')
        user_avatar.update({'uid': user})

    # if 'avatar' in user_avatar and user_avatar['avatar']:
    #     user_avatar.update({'avatar': base64.b64decode(user_avatar['avatar'])})
    #
    # user_avatar_list = []
    # for m in User_Avatar.objects.filter(
    #         **remove_redundant_data(user_avatar, [f.name for f in User_Avatar._meta.get_fields()])):
    #     if m.avatar:
    #         user_avatar_list.append({'uid': m.uid.uid, 'avatar': base64.b64encode(m.avatar).decode('utf-8')})
    #     else:
    #         user_avatar_list.append({'uid': m.uid.uid, 'avatar': m.avatar})

    # return get_result(SUCCESS, {'user_avatar_list': user_avatar_list})
    return get_result(SUCCESS, {'user_avatar_list': [model_to_dict(m) for m in User_Avatar.objects.filter(
        **remove_redundant_data(user_avatar, [f.name for f in User_Avatar._meta.get_fields()]))]})
