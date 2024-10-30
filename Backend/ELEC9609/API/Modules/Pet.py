from django.forms import model_to_dict

from ELEC9609.API.Modules.Base import *


def __pet_operate(data, update_or_delete):
    auth = get_authorisation(data)
    if not auth['error_code'] == 200:
        return auth
    if not auth['data']['type'] == get_model_data_key(User):
        return get_result(FALSE, None, f'Your account type {auth['data']['type']} has no permission to do that.')

    operator = User.objects.filter(email=auth['data']['email']).first()
    if not operator:
        return get_result(FALSE, None, f'Operator user {auth['data']['email']} is not exist')

    operating_pet = Pet.objects.filter(pid=data['pet']['pid']).first()
    if not operating_pet:
        return get_result(FALSE, None, f'Operating pet {data['pet']['pid']} is not exist')

    if not operator.admin and operating_pet.uid != operator:
        return get_result(FALSE, None,
                          f'Operating pet {data['pet']['pid']} is not belong to user {auth['data']['email']} and user is not admin')

    if update_or_delete:
        # Data for updating
        updating_data = remove_redundant_data(data['pet_new'], [f.name for f in Pet._meta.get_fields()])
        if 'pid' in updating_data:
            updating_data.pop('pid')
            TLogger.twarn(f'Removed auto field pid in updating data')
        # Change pet owner
        if 'uid' in updating_data:
            if not operator.admin:
                updating_data.pop('uid')
                TLogger.twarn(f'Operator user {auth['data']['email']} attempt to change uid of pet, but not admin')
            else:
                if updating_data['uid'] == operating_pet.uid.uid:
                    updating_data.pop('uid')
                    TLogger.twarn(
                        f'Admin user {auth['data']['email']} attempt to change uid of pet using same value as before')
                else:
                    target_user = User.objects.filter(uid=updating_data['uid']).first()
                    if not target_user:
                        return get_result(FALSE, None,
                                          f'Admin user {auth['data']['email']} attempt to change uid of pet, but user with uid {updating_data['uid']} is not exist')
                    updating_data.update({'uid': target_user})
                    TLogger.tlog(
                        f'Admin user {auth['data']['email']} changed uid of pet from {operating_pet.uid} to {updating_data['uid']}')
        if 'dob' in updating_data:
            updating_data.update({'dob': datetime.fromtimestamp(updating_data['dob'])})

        operating_pet.__dict__.update(**updating_data)
        if 'uid' in updating_data:
            operating_pet.uid = updating_data['uid']
        operating_pet.save()
        TLogger.tlog(f'pet_update: {data['pet']} to {data['pet_new']}')
        return get_result(SUCCESS, None, 'Pet updated')
    else:
        operating_pet.delete()
        TLogger.tlog(f'pet_delete: {data['pet']}')
        return get_result(SUCCESS, None, 'Pet deleted')


def pet_update(data):
    """
    Authorised account types: User,
    if not admin, user can only update pet that belong to user
    :param data: {
            "token": "<token>",
            "pet": {
                "pid": 0
            },
            "pet_new": {
                "p_name": "str",
                "species": "str",
                "breed": "str",
                "age": 0,
                "uid": 0,
                "diagnosis": "str",
                "dob": 1728805599.043506
            }
        }
    :return: {
            "error_code": 200,
            "data": null,
            "error_msg": "str?"
        }
    """
    assert 'pet' in data and type(data['pet']) == dict and 'pid' in data['pet'] and 'pet_new' in data and type(
        data['pet_new']) == dict
    return __pet_operate(data, True)


def pet_delete(data):
    """
    Authorised account types: User,
    if not admin, user can only delete pet that belong to user
    :param data: {
        "token": "<token>",
        "pet": {
            "pid": 0
        }
    :return: {
            "error_code": 200,
            "data": null,
            "error_msg": "str?"
        }
    """
    assert 'pet' in data and type(data['pet']) == dict and 'pid' in data['pet']
    return __pet_operate(data, False)


def pet_create(data):
    """
    Authorised account types: User,
    create a pet belong to operator
    :param data: {
            "token": "<token>",
            "pet": {
                "p_name": "str",
                "species": "str",
                "breed": "str",
                "age": 0,
                "diagnosis": "str?",
                "dob": 1728805599.043506
            }
    :return: {
            "error_code": 200,
            "data": null,
            "error_msg": "str?"
        }
    """

    assert 'pet' in data and type(data['pet']) == dict
    pet_data = data['pet']
    assert 'p_name' in pet_data and 'species' in pet_data and 'breed' in pet_data and type(
        pet_data['p_name']) == str and type(pet_data['species']) == str and type(pet_data['breed']) == str

    auth = get_authorisation(data)
    if not auth['error_code'] == 200:
        return auth
    if not auth['data']['type'] == get_model_data_key(User):
        return get_result(FALSE, None, f'Your account type {auth['data']['type']} has no permission to do that.')

    operator = User.objects.filter(email=auth['data']['email']).first()
    if not operator:
        return get_result(FALSE, None, f'Operator user {auth['data']['email']} is not exist')

    if 'pid' in pet_data:
        pet_data.pop('pid')
        TLogger.tlog(f'Removed auto field pid')

    if 'dob' in pet_data:
        pet_data.update({'dob': datetime.fromtimestamp(pet_data['dob'])})

    pet_data.update({'uid': operator})
    Pet.objects.create(**pet_data)
    TLogger.tlog(f'pet_create: {pet_data}')
    return get_result(SUCCESS, None, 'Pet created')


def pet_select(data):
    """
    Authorised account types: Any,
    :param data: 	{
            // Can not exist, but some data will not return if unauthorised
            "token": "<token>",
            // filter
            "pet": {
                "pid": 0
                "uid": 0,
                "p_name": "str",
                "species": "str",
                "breed": "str",
                "age": 0,
                "diagnosis": "str",
                "dob": 1728805599.043506
            }
        }
    :return: 	{
            "error_code": 200,
            "data": {
                "pet_list": [
                    {
                        "pid": 0,
                        "uid": 0,
                        "p_name": "str",
                        "species": "str",
                        "breed": "str",
                        "age": 0,
                        // if not admin or owner, remove this
                        "diagnosis": "str",
                        "dob": 1728805599.043506
                    }
                ]
            },
            "error_msg": "str?"
        }
    """

    assert 'pet' in data and type(data['pet']) == dict

    pet = data['pet']

    if 'uid' in pet:
        pet_owner = User.objects.filter(uid=pet['uid']).first()
        if not pet_owner:
            return get_result(SUCCESS, {'pet_list': []}, f'Pet owner user {data['pet']['uid']} is not exist')
        pet.update({'uid': pet_owner})

    if 'dob' in pet:
        pet.update({'dob': datetime.fromtimestamp(pet['dob'])})

    return get_result(SUCCESS, {'pet_list': list_str_to_timestamp([model_to_dict(m) for m in Pet.objects.filter(
        **remove_redundant_data(pet, [f.name for f in Pet._meta.get_fields()]))])})
