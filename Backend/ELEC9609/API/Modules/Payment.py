from django.forms import model_to_dict

from ELEC9609.API.Modules.Base import *


def __payment_operate(data, update_or_delete):
    auth = get_authorisation(data)
    if not auth['error_code'] == 200:
        return auth

    a_type_name = auth['data']['type']
    a_type = get_model_type_by_data_key(a_type_name)

    if not a_type_name == get_model_data_key(User):
        return get_result(FALSE, None, f'Your account type {a_type_name} has no permission to do that.')

    operator = a_type.objects.filter(email=auth['data']['email']).first()

    if not operator:
        return get_result(FALSE, None, f'Operator {a_type_name} {auth['data']['email']} is not exist')

    admin = False
    if a_type_name == get_model_data_key(User):
        admin = operator.admin

    operating_payment = Payment.objects.filter(paymentid=data['payment']['paymentid']).first()
    if not operating_payment:
        return get_result(FALSE, None, f'Operating payment {data['payment']['paymentid']} is not exist')

    if not admin and a_type == User and operating_payment.order_id.uid != operator:
        return get_result(FALSE, None,
                          f'Operating payment {data['payment']['paymentid']} is not belong to {a_type_name} {auth['data']['email']} and user is not admin')

    if update_or_delete:
        if not admin:
            if not 'payment_info' in data['payment_new']:
                return get_result(FALSE, None,
                                  f'For Payment, user can only change the payment_info, but not included in data')
            operating_payment.__dict__.update(payment_info=data['payment_new']['payment_info'])
            operating_payment.save()
            TLogger.tlog(
                f'payment_update: only support change payment_info {data['payment']} to {data['payment_new']}')
        else:
            updating_data = remove_redundant_data(data['payment_new'],
                                                  [f.name for f in Payment._meta.get_fields()])
            service_order = None
            if 'order_id' in updating_data:
                service_order = Service_Order.objects.filter(order_id=updating_data['order_id']).first()
                if not service_order:
                    return get_result(FALSE, None, f'Service_Order {updating_data["order_id"]} is not exist')
            if 'paymentid' in updating_data:
                updating_data.pop('paymentid')
                TLogger.twarn(f'Removed auto field pid in updating data')
            operating_payment.__dict__.update(**updating_data)
            if 'order_id' in updating_data:
                operating_payment.pid = service_order
            operating_payment.save()
            TLogger.tlog(f'payment_update: {data['payment']} to {data['payment_new']}')
        return get_result(SUCCESS, None, 'Payment updated')
    else:
        if not admin:
            return get_result(FALSE, None,
                              f'Operator {operator} is not admin, delete payment can only support admin operation.')
        operating_payment.delete()
        TLogger.tlog(f'payment_delete: {data['payment']}')
        return get_result(SUCCESS, None, 'Payment deleted')


def payment_update(data):
    """
    Authorised account types: User, Trainer,
    if not admin, user can only update order belong to user
    :param data: {
            "token": "<token>",
            "payment": {
                "paymentid": 0,
            },
            "payment_new": {
                "paymentid": 0,
                "order_id": 0,
                "payment_info": "str"
            }
        }
    :return: {
            "error_code": 200,
            "data": null,
            "error_msg": "str?"
        }
    """
    assert 'payment' in data and type(data['payment']) == dict and 'paymentid' in data[
        'payment'] and 'payment_new' in data and type(data['payment_new']) == dict
    return __payment_operate(data, True)


def payment_delete(data):
    """
    Authorised account types: User,
    only admin can delete service order
    :param data: {
            "token": "<token>",
            "payment": {
                "paymentid": 0
            }
        }
    :return: {
            "error_code": 200,
            "data": null,
            "error_msg": "str?"
        }
    """
    assert 'payment' in data and type(data['payment']) == dict and 'paymentid' in data['payment']
    return __payment_operate(data, False)


def payment_create(data):
    """
    Authorised account types: User,
    create an avatar belong to
    :param data: {
            "token": "<token>",
            "payment": {
                "paymentid": 0,
                "order_id": 0,
                "payment_info": "str"
            }
        }
    :return: {
            "error_code": 200,
            "data": null,
            "error_msg": "str?"
        }
    """

    assert 'payment' in data and type(data['payment']) == dict
    payment_data = data['payment']
    assert 'order_id' in payment_data and 'payment_info' in payment_data

    auth = get_authorisation(data)
    if not auth['error_code'] == 200:
        return auth
    if not auth['data']['type'] == get_model_data_key(User):
        return get_result(FALSE, None, f'Your account type {auth['data']['type']} has no permission to do that.')

    operator = User.objects.filter(email=auth['data']['email']).first()
    if not operator:
        return get_result(FALSE, None, f'Operator user {auth['data']['email']} is not exist')

    service_order = Service_Order.objects.filter(order_id=payment_data['order_id']).first()
    if not service_order:
        return get_result(FALSE, None,
                          f'Operator {auth['data']['email']} service_order {payment_data['order_id']} is not exist')

    if service_order.uid != operator:
        return get_result(FALSE, None,
                          f'Operator {auth['data']['email']} service_order {payment_data['order_id']} is not owned')

    payment_data.update({'order_id': service_order})

    if 'paymentid' in payment_data:
        payment_data.pop('paymentid')
        TLogger.tlog(f'Removed auto field order_id')

    Payment.objects.create(**payment_data)
    return get_result(SUCCESS, None, 'Payment created')


def payment_select(data):
    """
    Authorised account types: Any,
    :param data: 	{
            // Can not exist, but some data will not return if unauthorised
            "token": "<token>",
            // filter
            "payment": {
                "paymentid": 0,
                "order_id": 0,
                "payment_info": "str"
            }
        }
    :return: 	{
            "error_code": 200,
            "data": {
                "payment_list": [
                    {
                        "paymentid": 0,
                        "order_id": 0,
                        "payment_info": "str"
                    }
                ]
            },
            "error_msg": "str?"
        }
    """

    assert 'payment' in data and type(data['payment']) == dict

    payment = data['payment']

    return get_result(SUCCESS, {'payment_list': [model_to_dict(m) for m in Payment.objects.filter(
        **remove_redundant_data(payment, [f.name for f in Payment._meta.get_fields()]))]})
