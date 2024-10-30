import base64

from django.forms import model_to_dict

from ELEC9609.API.Modules.Base import *


def __trainer_avatar_operate(data, update_or_delete):
    auth = get_authorisation(data)
    if not auth['error_code'] == 200:
        return auth

    a_type_name = auth['data']['type']
    a_type = get_model_type_by_data_key(a_type_name)

    if not a_type_name == get_model_data_key(Trainer) and not a_type_name == get_model_data_key(User):
        return get_result(FALSE, None, f'Your account type {a_type_name} has no permission to do that.')

    operator = a_type.objects.filter(email=auth['data']['email']).first()

    if not operator:
        return get_result(FALSE, None, f'Operator trainer {auth['data']['email']} is not exist')

    admin = False
    if a_type_name == get_model_data_key(User):
        if not operator.admin:
            return get_result(FALSE, None, f'Your account type {a_type_name} has no admin permission to do that.')
        admin = True

    operating_trainer_avatar = Trainer_Avatar.objects.filter(tid=data['trainer_avatar']['tid']).first()
    if not operating_trainer_avatar:
        return get_result(FALSE, None, f'Operating trainer_avatar {data['trainer_avatar']['tid']} is not exist')

    if not admin and operating_trainer_avatar.tid != operator:
        return get_result(FALSE, None,
                          f'Operating trainer_avatar {data['trainer_avatar']['tid']} is not belong to trainer {auth['data']['email']} and trainer is not admin')

    if update_or_delete:
        # Data for updating
        updating_data = remove_redundant_data(data['trainer_avatar_new'],
                                              [f.name for f in Trainer_Avatar._meta.get_fields()])
        if 'tid' in updating_data:
            updating_data.pop('tid')
            TLogger.twarn(f'Removed auto field tid in updating data')
        # if 'avatar' in updating_data and updating_data['avatar']:
        #     updating_data.update({'avatar': base64.b64decode(updating_data['avatar'])})
        operating_trainer_avatar.__dict__.update(**updating_data)
        operating_trainer_avatar.save()
        TLogger.tlog(f'trainer_avatar_update: {data['trainer_avatar']} to {data['trainer_avatar_new']}')
        return get_result(SUCCESS, None, 'Trainer_Avatar updated')
    else:
        operating_trainer_avatar.delete()
        TLogger.tlog(f'trainer_avatar_delete: {data['trainer_avatar']}')
        return get_result(SUCCESS, None, 'Trainer_Avatar deleted')


def trainer_avatar_update(data):
    """
    Authorised account types: Trainer,
    if not admin, trainer can only update avatar belong to trainer
    :param data: {
            "token": "<token>",
            "trainer_avatar": {
                "tid": 0,
            },
            "trainer_avatar_new": {
                "avatar": "base64 str"
            }
        }
    :return: {
            "error_code": 200,
            "data": null,
            "error_msg": "str?"
        }
    """
    assert 'trainer_avatar' in data and type(data['trainer_avatar']) == dict and 'tid' in data[
        'trainer_avatar'] and 'trainer_avatar_new' in data and type(data['trainer_avatar_new']) == dict
    return __trainer_avatar_operate(data, True)


def trainer_avatar_delete(data):
    """
    Authorised account types: Trainer,
    if not admin, trainer can only delete avatar belong to trainer
    :param data: {
            "token": "<token>",
            "trainer_avatar": {
                "tid": 0
            }
        }
    :return: {
            "error_code": 200,
            "data": null,
            "error_msg": "str?"
        }
    """
    assert 'trainer_avatar' in data and type(data['trainer_avatar']) == dict and 'tid' in data['trainer_avatar']
    return __trainer_avatar_operate(data, False)


def trainer_avatar_create(data):
    """
    Authorised account types: Trainer,
    create an avatar belong to trainer
    :param data: {
            "token": "<token>",
            "trainer_avatar": {
                "avatar": "base64 str"
            }
        }
    :return: {
            "error_code": 200,
            "data": null,
            "error_msg": "str?"
        }
    """

    assert 'trainer_avatar' in data and type(data['trainer_avatar']) == dict
    trainer_avatar_data = data['trainer_avatar']

    auth = get_authorisation(data)
    if not auth['error_code'] == 200:
        return auth
    if not auth['data']['type'] == get_model_data_key(Trainer):
        return get_result(FALSE, None, f'Your account type {auth['data']['type']} has no permission to do that.')

    operator = Trainer.objects.filter(email=auth['data']['email']).first()
    if not operator:
        return get_result(FALSE, None, f'Operator trainer {auth['data']['email']} is not exist')

    if Trainer_Avatar.objects.filter(tid=operator).first():
        return get_result(FALSE, None, f'Operator {auth['data']['email']} trainer_avatar {operator.tid} already exists')

    trainer_avatar_data.update({'tid': operator})
    # if 'avatar' in trainer_avatar_data and trainer_avatar_data['avatar']:
    #     trainer_avatar_data.update({'avatar': base64.b64decode(trainer_avatar_data['avatar'])})
    Trainer_Avatar.objects.create(**trainer_avatar_data)
    # TLogger.tlog(f'trainer_avatar_create: {trainer_avatar_data}')
    return get_result(SUCCESS, None, 'Trainer_Avatar created')


def trainer_avatar_select(data):
    """
    Authorised account types: Any,
    :param data: 	{
            // Can not exist, but some data will not return if unauthorised
            "token": "<token>",
            // filter
            "trainer_avatar": {
                "tid": 0,
                "avatar": "base64 str"
            }
        }
    :return: 	{
            "error_code": 200,
            "data": {
                "trainer_avatar_list": [
                    {
                        "tid": 0,
                        "avatar": "base64 str"
                    }
                ]
            },
            "error_msg": "str?"
        }
    """

    assert 'trainer_avatar' in data and type(data['trainer_avatar']) == dict

    trainer_avatar = data['trainer_avatar']

    if 'tid' in trainer_avatar:
        trainer = Trainer.objects.filter(tid=trainer_avatar['tid']).first()
        if not trainer:
            return get_result(SUCCESS, {'trainer_avatar_list': []}, f'Trainer {data['trainer_avatar']['tid']} is not exist')
        trainer_avatar.update({'tid': trainer})

    # if 'avatar' in trainer_avatar and trainer_avatar['avatar']:
    #     trainer_avatar.update({'avatar': base64.b64decode(trainer_avatar['avatar'])})
    #
    # trainer_avatar_list = []
    # for m in Trainer_Avatar.objects.filter(
    #         **remove_redundant_data(trainer_avatar, [f.name for f in Trainer_Avatar._meta.get_fields()])):
    #     if m.avatar:
    #         trainer_avatar_list.append({'tid': m.tid.tid, 'avatar': base64.b64encode(m.avatar).decode('utf-8')})
    #     else:
    #         trainer_avatar_list.append({'tid': m.tid.tid, 'avatar': m.avatar})
    #
    # return get_result(SUCCESS, {'trainer_avatar_list': trainer_avatar_list})
    return get_result(SUCCESS, {'trainer_avatar_list': [model_to_dict(m) for m in Trainer_Avatar.objects.filter(
        **remove_redundant_data(trainer_avatar, [f.name for f in Trainer_Avatar._meta.get_fields()]))]})
