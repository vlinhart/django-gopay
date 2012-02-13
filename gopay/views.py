# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from gopay.gopay_http import Payment
from gopay import callback_notification_function


def gopay_notification(request, type='notification'):
    """
    This function must return 200 status if the notification was successfuly processed.
    """
    payment_data = request.GET
    p = Payment()
    try:
        p.payment_status_notification_validation(payment_data)
    except Exception, e:
        return HttpResponseForbidden(e.message)

    paid_ok = p.verify_payment_status(
        payment_data['paymentSessionId']) #TODO this is maybe not necessary for notification only call
    return callback_notification_function(request, paid_ok, type, payment_data['paymentSessionId'],
        payment_data['variableSymbol'])

@login_required
def gopay_success(request):
    return gopay_notification(request, type='success')


@login_required
def gopay_failure(request):
    return gopay_notification(request, type='failure')

