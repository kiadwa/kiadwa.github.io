from django.forms import model_to_dict

from ELEC9609.API.Modules.Base import *


def __service_order_operate(data, update_or_delete):
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

    operating_service_order = Service_Order.objects.filter(order_id=data['service_order']['order_id']).first()
    if not operating_service_order:
        return get_result(FALSE, None, f'Operating service_order {data['service_order']['order_id']} is not exist')

    if not admin and (
            a_type == User and operating_service_order.uid != operator or a_type == Trainer and operating_service_order.tid == operator):
        return get_result(FALSE, None,
                          f'Operating service_order {data['service_order']['order_id']} is not belong to {a_type_name} {auth['data']['email']} and user is not admin')

    if update_or_delete:
        if not admin:
            if not 'status' in data['service_order_new']:
                return get_result(FALSE, None,
                                  f'For Service_Order, user can only change the status, but not included in data')
            operating_service_order.__dict__.update(status=data['service_order_new']['status'])
            operating_service_order.save()
            TLogger.tlog(
                f'service_order_update: only support change status {data['service_order']} to {data['service_order_new']}')
        else:
            updating_data = remove_redundant_data(data['service_order_new'],
                                                  [f.name for f in Service_Order._meta.get_fields()])
            pet = None
            if 'pid' in updating_data:
                pet = Pet.objects.filter(pid=updating_data['pid']).first()
                if not pet:
                    return get_result(FALSE, None, f'Pet {updating_data["pid"]} is not exist')
            user = None
            if 'uid' in updating_data:
                user = User.objects.filter(uid=updating_data['uid']).first()
                if not user:
                    return get_result(FALSE, None, f'User {updating_data["uid"]} is not exist')
            trainer = None
            if 'tid' in updating_data:
                trainer = Trainer.objects.filter(tid=updating_data['tid']).first()
                if not trainer:
                    return get_result(FALSE, None, f'Trainer {updating_data["tid"]} is not exist')
            if 'order_id' in updating_data:
                updating_data.pop('order_id')
                TLogger.twarn(f'Removed auto field pid in updating data')
            operating_service_order.__dict__.update(**updating_data)
            if 'pid' in updating_data:
                operating_service_order.pid = pet
            if 'uid' in updating_data:
                operating_service_order.uid = user
            if 'tid' in updating_data:
                operating_service_order.tid = trainer
            operating_service_order.save()
            TLogger.tlog(f'service_order_update: {data['service_order']} to {data['service_order_new']}')
        return get_result(SUCCESS, None, 'Service_Order updated')
    else:
        if not admin:
            return get_result(FALSE, None,
                              f'Operator {operator} is not admin, delete service_order can only support admin operation.')
        operating_service_order.delete()
        TLogger.tlog(f'service_order_delete: {data['service_order']}')
        return get_result(SUCCESS, None, 'Service_Order deleted')


def service_order_update(data):
    """
    Authorised account types: User, Trainer,
    if not admin, user can only update order belong to user
    :param data: {
            "token": "<token>",
            "service_order": {
                "order_id": 0,
            },
            "service_order_new": {
                "order_id": 0,
                "pid": 0,
                "uid": 0,
                "tid": 0,
                "order_date": 1728805599.043506,
                "service_type": "str",
                "cost": 0,
                "status": "str"
            }
        }
    :return: {
            "error_code": 200,
            "data": null,
            "error_msg": "str?"
        }
    """
    assert 'service_order' in data and type(data['service_order']) == dict and 'order_id' in data[
        'service_order'] and 'service_order_new' in data and type(data['service_order_new']) == dict
    return __service_order_operate(data, True)


def service_order_delete(data):
    """
    Authorised account types: User,
    only admin can delete service order
    :param data: {
            "token": "<token>",
            "service_order": {
                "order_id": 0
            }
        }
    :return: {
            "error_code": 200,
            "data": null,
            "error_msg": "str?"
        }
    """
    assert 'service_order' in data and type(data['service_order']) == dict and 'order_id' in data['service_order']
    return __service_order_operate(data, False)


def service_order_create(data):
    """
    Authorised account types: User,
    create an order 
    :param data: {
            "token": "<token>",
            "service_order": {
                "pid": 0,
                "tid": 0,
                "order_date": 1728805599.043506,
                "service_type": "str",
                "cost": 0,
                "status": "str"
            }
        }
    :return: {
            "error_code": 200,
            "data": null,
            "error_msg": "str?"
        }
    """

    assert 'service_order' in data and type(data['service_order']) == dict
    service_order_data = data['service_order']
    assert 'tid' in service_order_data and 'order_date' in service_order_data and 'service_type' in service_order_data and 'cost' in service_order_data and 'status' in service_order_data

    auth = get_authorisation(data)
    if not auth['error_code'] == 200:
        return auth
    if not auth['data']['type'] == get_model_data_key(User):
        return get_result(FALSE, None, f'Your account type {auth['data']['type']} has no permission to do that.')

    operator = User.objects.filter(email=auth['data']['email']).first()
    if not operator:
        return get_result(FALSE, None, f'Operator user {auth['data']['email']} is not exist')

    service_order_data.update({'uid': operator})

    pet = Pet.objects.filter(pid=service_order_data['pid']).first()
    if not pet:
        return get_result(FALSE, None,
                          f'Operator {auth['data']['email']} pet {service_order_data['pid']} is not exist')

    if pet.uid != operator:
        return get_result(FALSE, None,
                          f'Operator {auth['data']['email']} pet {service_order_data['pid']} is not owned')

    service_order_data.update({'pid': pet})

    trainer = Trainer.objects.filter(tid=service_order_data['tid']).first()
    if not trainer:
        return get_result(FALSE, None,
                          f'Operator {auth['data']['email']} trainer {service_order_data['tid']} is not exist')

    service_order_data.update({'tid': trainer})

    service_order_data.update({'order_date': datetime.fromtimestamp(service_order_data['order_date'])})

    if 'order_id' in service_order_data:
        service_order_data.pop('order_id')
        TLogger.tlog(f'Removed auto field order_id')

    newServiceOrder = Service_Order.objects.create(**service_order_data)
    #add order_id into return data to better navigate to payment
    order_id = newServiceOrder.order_id
    return get_result(SUCCESS, {'order_id': order_id}, 'Service_Order created')


def service_order_select(data):
    """
    Authorised account types: Any,
    :param data: 	{
            // Can not exist, but some data will not return if unauthorised
            "token": "<token>",
            // filter
            "service_order": {
                "order_id": 0,
                "pid": 0,
                "uid": 0,
                "tid": 0,
                "order_date": 1728805599.043506,
                "service_type": "str",
                "cost": 0,
                "status": "str"
            }
        }
    :return: 	{
            "error_code": 200,
            "data": {
                "service_order_list": [
                    {
                        "order_id": 0,
                        "pid": 0,
                        "uid": 0,
                        "tid": 0,
                        "order_date": 1728805599.043506,
                        "service_type": "str",
                        "cost": 0,
                        "status": "str"
                    }
                ]
            },
            "error_msg": "str?"
        }
    """

    assert 'service_order' in data and type(data['service_order']) == dict

    service_order = data['service_order']

    if 'order_date' in service_order:
        service_order.update({'order_date': datetime.fromtimestamp(service_order['order_date'])})

    return get_result(SUCCESS, {'service_order_list': list_str_to_timestamp([model_to_dict(m) for m in Service_Order.objects.filter(
        **remove_redundant_data(service_order, [f.name for f in Service_Order._meta.get_fields()]))])})
