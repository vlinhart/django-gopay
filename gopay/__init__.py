# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

try: # pragma: no cover
    from importlib import import_module # pragma: no cover
except ImportError: # pragma: no cover
    from django.utils.importlib import import_module # pragma: no cover

def require_settings(name):
    try:
        return getattr(settings, name)
    except AttributeError:
        raise ImproperlyConfigured("GOPAY: You must set the '%s' in settings file." % name)

require_settings('GOPAY_ESHOP_GOID')
require_settings('GOPAY_SECRET')
require_settings('GOPAY_SUCCESS_URL')
require_settings('GOPAY_FAILED_URL')


# take the function from settings, default one is provided, does nothing :-)
callback_notification_function = getattr(settings, 'GOPAY_NOTIFICATION_CALLBACK', 'gopay.utils.notification_callback')

i = callback_notification_function.rfind('.')
module, attr = callback_notification_function[:i], callback_notification_function[i + 1:]
try:
    callback_notification_function = getattr(import_module(module), attr)
except (ImportError, AttributeError), e:
    raise ImproperlyConfigured('GOPAY: Error loading callback_notification_function from module %s: "%s"' % (module, e))

