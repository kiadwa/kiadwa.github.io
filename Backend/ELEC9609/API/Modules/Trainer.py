from django.forms import model_to_dict

from ELEC9609.API.Modules.Base import *


def __trainer_operate(data, update_or_delete):
    auth = get_authorisation(data)
    if not auth['error_code'] == 200:
        return auth

    a_type_name = auth['data']['type']
    a_type = get_model_type_by_data_key(a_type_name)

    if not a_type_name == get_model_data_key(User) and not a_type_name == get_model_data_key(Trainer):
        return get_result(FALSE, None, f'Your account type {a_type_name} has no permission to do that.')

    operator = a_type.objects.filter(email=auth['data']['email']).first()

    if not operator:
        return get_result(FALSE, None, f'Operator {a_type_name} {auth['data']['email']} is not exist')

    admin = False
    if a_type_name == get_model_data_key(User):
        admin = operator.admin

    operating_trainer = Trainer.objects.filter(email=data['trainer']['email']).first()

    if not admin and (a_type != Trainer or a_type == Trainer and operating_trainer.tid != operator.tid):
        return get_result(FALSE, None,
                          f'Operating trainer {data['trainer']['email']} is not {a_type_name} {auth['data']['email']} and user is not admin')

    # admin or own data
    if update_or_delete:
        updating_data = remove_redundant_data(data['trainer_new'], [f.name for f in Trainer._meta.get_fields()])
        if 'email' in updating_data and updating_data['email'] != operator.email and Trainer.objects.filter(
                email=updating_data['email']).first():
            return get_result(FALSE, None,
                              f'Operator {a_type_name} {operator.email} attempt to change email {data['trainer']['email']}, but target email {updating_data['email']} already exists')
        if 'tid' in updating_data:
            updating_data.pop('tid')
            TLogger.twarn(f'Removed auto field tid in updating_data')
        if 'password' in updating_data:
            updating_data.update({'password': password_encrypt(updating_data['password'])})
        if 'dob' in updating_data:
            updating_data.update({'dob': datetime.fromtimestamp(updating_data['dob'])})
        if 'lockout' in updating_data:
            updating_data.update({'lockout': datetime.fromtimestamp(updating_data['lockout'], UTC)})

        if not admin:
            if 'provid' in updating_data:
                updating_data.pop('provid')
                TLogger.twarn(f'Trainer {auth['data']['email']} attempt to change provid, but not admin')
            original_email, original_password = operating_trainer.email, operating_trainer.password
            operating_trainer.__dict__.update(**updating_data)
            operating_trainer.save()
            if 'email' in updating_data and not original_email == updating_data[
                'email'] or 'password' in updating_data and not original_password == updating_data['password']:
                remove_logged_in_account_by_email(data['trainer']['email'], Trainer)
                TLogger.tlog(f'email or password changed, log out trainer {original_email}')
            TLogger.tlog(
                f'trainer_update: {data['trainer']} to {data['trainer_new']}')
        else:
            if 'provid' in updating_data:
                provider = Provider.objects.filter(provid=updating_data['provid']).first()
                if not provider:
                    return get_result(FALSE, None, f'Provider {updating_data['provid']} is not exist')
                updating_data.update({'provid': provider})

            original_email, original_password = operating_trainer.email, operating_trainer.password
            operating_trainer.__dict__.update(**updating_data)
            if 'provid' in updating_data:
                operating_trainer.provid = updating_data['provid']
            operating_trainer.save()
            if 'email' in updating_data and not original_email == updating_data[
                'email'] or 'password' in updating_data and not original_password == updating_data['password']:
                remove_logged_in_account_by_email(data['trainer']['email'], Trainer)
                TLogger.tlog(f'email or password changed, log out trainer {original_email}')
            TLogger.tlog(
                f'trainer_update: {data['trainer']} to {data['trainer_new']}')
        return get_result(SUCCESS, None, 'Trainer updated')
    else:
        operating_trainer.delete()
        remove_logged_in_account_by_email(data['trainer']['email'], Trainer)
        TLogger.tlog(f'trainer_delete: {data['trainer']}')
        return get_result(SUCCESS, None, 'Trainer deleted')


def trainer_update(data):
    """
    Authorised account types: User, Trainer,
    if not admin, user can only update his own data,
    if email or password changed, login again required,
    if not admin, user cannot update lockout or admin columns
    :param data: 	{
            "token": "<token>",
            "trainer": {
                // trainer who want to update
                "email": "str",
            },
            "trainer_new": {
                // what you want to update
                "provid": 0,
                "l_name": "str",
                "f_name": "str",
                "email": "str",
                "dob": 1728805599.043506,
                "password": "str",
                "lockout": 1728805599.043506
            }
        }
    :return:	{
            "error_code": 200,
            "data": null,
            "error_msg": "str?"
        }
    """

    assert 'trainer' in data and type(data['trainer']) == dict and 'email' in data[
        'trainer'] and 'trainer_new' in data and type(
        data['trainer_new']) == dict

    return __trainer_operate(data, True)


def trainer_delete(data):
    """
    Authorised account types: User, Trainer,
    if not admin, user can only delete his own data,
    deleted account will log out
    :param data: 	{
            "token": "<token>",
            "trainer": {
                "email": "str",
            }
        }
    :return:	{
            "error_code": 200,
            "data": null,
            "error_msg": "str?"
        }
    """
    assert 'trainer' in data and type(data['trainer']) == dict and 'email' in data['trainer']

    return __trainer_operate(data, False)


def trainer_select(data):
    """
    Authorised account types: Any,
    if not admin, some data will not return
    :param data: 	{
            // Can not exist, but some data will not return if unauthorised
            "token": "<token>",
            // filter
            "trainer": {
                "provid: 0,
                "l_name": "al",
                "f_name": "af",
                "email": "3@e.com",
                "dob": 1728805599.043506,
                "password": "str",
                "lockout": 1728805599.043506
            }
        }
    :return: 	{
            "error_code": 200,
            "data": {
                "trainer_list": [
                    {
                        "tid": 0,
                        "provid: 0,
                        "l_name": "al",
                        "f_name": "af",
                        "email": "3@e.com",
                        "dob": 1728805599.043506,
                        "password": "str",
                        "lockout": 1728805599.043506
                    }
                ]
            },
            "error_msg": "str?"
        }
    """

    def remove_private_data(trainer):
        for t in trainer:
            t.pop('password')
        return trainer

    auth = get_authorisation(data)
    if not auth['error_code'] == 200:
        if not 'trainer' in data:
            return get_result(SUCCESS, {
                'trainer_list': list_str_to_timestamp(
                    remove_private_data([model_to_dict(m) for m in Trainer.objects.filter()]))},
                              f'Unauthorised user execute select')
        trainer = data['trainer']
        if 'dob' in trainer:
            trainer.update(dob=datetime.fromtimestamp(trainer['dob']))
        if 'lockout' in trainer:
            trainer.update(lockout=datetime.fromtimestamp(trainer['lockout'], UTC))
        if 'password' in trainer:
            trainer.pop('password')
            TLogger.tlog(f'Unauthorised user attempt to filter trainer by password, remove filter')
        return get_result(SUCCESS,
                          {'trainer_list': list_str_to_timestamp(remove_private_data(
                              [model_to_dict(m) for m in Trainer.objects.filter(
                                  **remove_redundant_data(trainer,
                                                          [f.name for f in Trainer._meta.get_fields()]))]))})

    operator_type = get_model_type_by_data_key(auth['data']['type'])

    # Current logged-in user, as operator
    operator_email = auth['data']['email']
    operator = operator_type.objects.filter(email=operator_email).first()

    if not operator:
        return get_result(FALSE, None, f'Operator {operator_type} {operator_email} is not exist')

    admin = False
    if operator_type == User:
        admin = operator.admin

    if not 'trainer' in data:
        if admin:
            return get_result(SUCCESS,
                              {'trainer_list': list_str_to_timestamp(
                                  [model_to_dict(m) for m in Trainer.objects.filter()])})
        else:
            return get_result(SUCCESS, {
                'trainer_list': remove_private_data(
                    list_str_to_timestamp([model_to_dict(m) for m in Trainer.objects.filter()]))},
                              f'Operator {auth['data']['type']} {operator_email} is not admin')

    trainer = data['trainer']
    if 'dob' in trainer:
        trainer.update(dob=datetime.fromtimestamp(trainer['dob']))
    if 'lockout' in trainer:
        trainer.update(lockout=datetime.fromtimestamp(trainer['lockout'], UTC))
    # Not admin, try filter password
    if not admin and 'password' in trainer:
        trainer.pop('password')
        TLogger.tlog(
            f'{auth['data']['type']} {operator_email} attempt to filter trainer by password but not admin, remove filter')

    if admin:
        return get_result(SUCCESS,
                          {'trainer_list': list_str_to_timestamp([model_to_dict(m) for m in Trainer.objects.filter(
                              **remove_redundant_data(trainer, [f.name for f in Trainer._meta.get_fields()]))])})
    else:
        return get_result(SUCCESS,
                          {'trainer_list': list_str_to_timestamp(remove_private_data(
                              [model_to_dict(m) for m in Trainer.objects.filter(
                                  **remove_redundant_data(trainer,
                                                          [f.name for f in Trainer._meta.get_fields()]))]))})
