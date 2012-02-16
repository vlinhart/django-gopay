# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

def require_settings(name):
    try:
        return getattr(settings, name)
    except AttributeError:
        raise ImproperlyConfigured("GOPAY: You must set the '%s' in settings file." % name)

require_settings('GOPAY_ESHOP_GOID')
require_settings('GOPAY_SECRET')
require_settings('GOPAY_SUCCESS_URL')
require_settings('GOPAY_FAILED_URL')
require_settings('GOPAY_TESTING_MODE')

# callback function default one is provided, does nothing however, 'gopay.utils.notification_callback'
require_settings('GOPAY_NOTIFICATION_CALLBACK')
