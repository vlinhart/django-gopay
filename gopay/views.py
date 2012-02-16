# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponseForbidden
from gopay.gopay_http import Payment

try: # pragma: no cover
    from importlib import import_module # pragma: no cover
except ImportError: # pragma: no cover
    from django.utils.importlib import import_module # pragma: no cover

#TODO check on startup, can't be in init, due to some strange errors on uwsgi and translations in exceptions WTF
# get the function from settings
callback_notification_function = getattr(settings, 'GOPAY_NOTIFICATION_CALLBACK')
i = callback_notification_function.rfind('.')
module, attr = callback_notification_function[:i], callback_notification_function[i + 1:]
try:
    callback_notification_function = getattr(import_module(module), attr)
except (ImportError, AttributeError), e:
    raise ImproperlyConfigured('GOPAY: Error loading callback_notification_function from module %s: "%s"' % (module, e))


def common_view(request, type):
    payment_data = request.GET
    p = Payment()
    try:
        p.payment_status_notification_validation(payment_data)
        pass
    except Exception, e:
        return HttpResponseForbidden(str(e))

    paid_ok, payment_details = p.verify_payment_status(
        payment_data['paymentSessionId']) #TODO this is maybe not necessary for notification only call
    return callback_notification_function(request, paid_ok, payment_details, type, payment_data['paymentSessionId'],
        payment_data['variableSymbol'])


@login_required
def gopay_notification(request):
    """
    This function must return 200 status if the notification was successfuly processed.
    """
    return common_view(request, type='notification')


@login_required
def gopay_success(request):
    return common_view(request, type='success')


@login_required
def gopay_failure(request):
    return common_view(request, type='failure')

