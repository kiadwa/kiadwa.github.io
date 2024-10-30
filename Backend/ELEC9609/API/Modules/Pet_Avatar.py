from django.forms import model_to_dict

from ELEC9609.API.Modules.Base import *


def __pet_avatar_operate(data, update_or_delete):
    auth = get_authorisation(data)
    if not auth['error_code'] == 200:
        return auth

    a_type_name = auth['data']['type']
    a_type = get_model_type_by_data_key(a_type_name)

    if not a_type_name == get_model_data_key(User):
        return get_result(FALSE, None, f'Your account type {a_type_name} has no permission to do that.')

    operator = a_type.objects.filter(email=auth['data']['email']).first()

    if not operator:
        return get_result(FALSE, None, f'Operator user {auth['data']['email']} is not exist')

    admin = False
    if a_type_name == get_model_data_key(User):
        admin = operator.admin

    operating_pet_avatar = Pet_Avatar.objects.filter(pid=data['pet_avatar']['pid']).first()
    if not operating_pet_avatar:
        return get_result(FALSE, None, f'Operating pet_avatar {data['pet_avatar']['pid']} is not exist')

    if not admin and operating_pet_avatar.pid.uid != operator:
        return get_result(FALSE, None,
                          f'Operating pet_avatar {data['pet_avatar']['pid']} is not belong to user {auth['data']['email']} and user is not admin')

    if update_or_delete:
        # Data for updating
        updating_data = remove_redundant_data(data['pet_avatar_new'],
                                              [f.name for f in Pet_Avatar._meta.get_fields()])
        if 'pid' in updating_data:
            updating_data.pop('pid')
            TLogger.twarn(f'Removed auto field pid in updating data')
        # if 'avatar' in updating_data and updating_data['avatar']:
        #     updating_data.update({'avatar': base64.b64decode(updating_data['avatar'])})
        operating_pet_avatar.__dict__.update(**updating_data)
        operating_pet_avatar.save()
        TLogger.tlog(f'pet_avatar_update: {data['pet_avatar']} to {data['pet_avatar_new']}')
        return get_result(SUCCESS, None, 'Pet_Avatar updated')
    else:
        operating_pet_avatar.delete()
        TLogger.tlog(f'pet_avatar_delete: {data['pet_avatar']}')
        return get_result(SUCCESS, None, 'Pet_Avatar deleted')


def pet_avatar_update(data):
    """
    Authorised account types: User,
    if not admin, pet can only update avatar belong to pet
    :param data: {
            "token": "<token>",
            "pet_avatar": {
                "pid": 0,
            },
            "pet_avatar_new": {
                "avatar": "base64 str"
            }
        }
    :return: {
            "error_code": 200,
            "data": null,
            "error_msg": "str?"
        }
    """
    assert 'pet_avatar' in data and type(data['pet_avatar']) == dict and 'pid' in data[
        'pet_avatar'] and 'pet_avatar_new' in data and type(data['pet_avatar_new']) == dict
    return __pet_avatar_operate(data, True)


def pet_avatar_delete(data):
    """
    Authorised account types: User,
    if not admin, pet can only delete avatar belong to pet
    :param data: {
            "token": "<token>",
            "pet_avatar": {
                "pid": 0
            }
        }
    :return: {
            "error_code": 200,
            "data": null,
            "error_msg": "str?"
        }
    """
    assert 'pet_avatar' in data and type(data['pet_avatar']) == dict and 'pid' in data['pet_avatar']
    return __pet_avatar_operate(data, False)


def pet_avatar_create(data):
    """
    Authorised account types: User,
    create an avatar belong to pet
    :param data: {
            "token": "<token>",
            "pet_avatar": {
                // pet pid required
                "pid": 0,
                "avatar": "base64 str"
            }
        }
    :return: {
            "error_code": 200,
            "data": null,
            "error_msg": "str?"
        }
    """

    assert 'pet_avatar' in data and type(data['pet_avatar']) == dict
    trainer_avatar_data = data['pet_avatar']
    assert 'pid' in trainer_avatar_data

    auth = get_authorisation(data)
    if not auth['error_code'] == 200:
        return auth
    if not auth['data']['type'] == get_model_data_key(User):
        return get_result(FALSE, None, f'Your account type {auth['data']['type']} has no permission to do that.')

    operator = User.objects.filter(email=auth['data']['email']).first()
    if not operator:
        return get_result(FALSE, None, f'Operator user {auth['data']['email']} is not exist')

    pet = Pet.objects.filter(pid=trainer_avatar_data['pid']).first()
    if not pet:
        return get_result(FALSE, None,
                          f'Operator {auth['data']['email']} pet {trainer_avatar_data['pid']} is not exist')

    if pet.uid != operator:
        return get_result(FALSE, None,
                          f'Operator {auth['data']['email']} pet {trainer_avatar_data['pid']} is not owned')

    if Pet_Avatar.objects.filter(pid=pet).first():
        return get_result(FALSE, None,
                          f'Operator {auth['data']['email']} pet_avatar {trainer_avatar_data['pid']} already exists')

    trainer_avatar_data.update({'pid': pet})
    # if 'avatar' in trainer_avatar_data and trainer_avatar_data['avatar']:
    #     trainer_avatar_data.update({'avatar': base64.b64decode(trainer_avatar_data['avatar'])})
    Pet_Avatar.objects.create(**trainer_avatar_data)
    return get_result(SUCCESS, None, 'Pet_Avatar created')


def pet_avatar_select(data):
    """
    Authorised account types: Any,
    :param data: 	{
            // Can not exist, but some data will not return if unauthorised
            "token": "<token>",
            // filter
            "pet_avatar": {
                "pid": 0,
                "avatar": "base64 str"
            }
        }
    :return: 	{
            "error_code": 200,
            "data": {
                "pet_avatar_list": [
                    {
                        "pid": 0,
                        "avatar": "base64 str"
                    }
                ]
            },
            "error_msg": "str?"
        }
    """

    assert 'pet_avatar' in data and type(data['pet_avatar']) == dict

    pet_avatar = data['pet_avatar']

    if 'pid' in pet_avatar:
        pet = Pet.objects.filter(pid=pet_avatar['pid']).first()
        if not pet:
            return get_result(SUCCESS, {'pet_avatar_list': []}, f'Pet {data['pet_avatar']['pid']} is not exist')
        pet_avatar.update({'pid': pet})

    # if 'avatar' in pet_avatar and pet_avatar['avatar']:
    #     pet_avatar.update({'avatar': base64.b64decode(pet_avatar['avatar'])})

    # pet_avatar_list = []
    # for m in Pet_Avatar.objects.filter(
    #         **remove_redundant_data(pet_avatar, [f.name for f in Pet_Avatar._meta.get_fields()])):
    #     if m.avatar:
    #         pet_avatar_list.append({'pid': m.pid.pid, 'avatar': base64.b64encode(m.avatar).decode('utf-8')})
    #     else:
    #         pet_avatar_list.append({'pid': m.pid.pid, 'avatar': m.avatar})
    #
    # return get_result(SUCCESS, {'pet_avatar_list': pet_avatar_list})

    return get_result(SUCCESS, {'pet_avatar_list': [model_to_dict(m) for m in Pet_Avatar.objects.filter(
        **remove_redundant_data(pet_avatar, [f.name for f in Pet_Avatar._meta.get_fields()]))]})
