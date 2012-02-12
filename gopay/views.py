# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse, HttpResponseForbidden
from gopay.gopay_http import Payment
from gopay import callback_notification_function


def gopay_notification(request):
    """
    This function must return 200 status if the notification was successfuly processed.
    """
    p = Payment()
    callback_notification_function(request.GET)
    try:
        p.payment_status_notification_validation(request.GET)
    except Exception, e:
        return HttpResponseForbidden(e.message)

    return HttpResponse("OK")
