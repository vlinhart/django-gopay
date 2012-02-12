# -*- coding: utf-8 -*-

ESHOP_GOID = 1163419611
SECRET = "rtytJemTrcpE9VmRR5VRbrty"

GOPAY_NEW_PAYMENT_URL_TEST = 'https://testgw.gopay.cz/vytvorit-platbu'
GOPAY_REDIRECT_URL_TEST = 'https://testgw.gopay.cz/zaplatit-plna-integrace'
GOPAY_PAYMENT_STATUS_URL_TEST = 'https://testgw.gopay.cz/stav-platby-gw2'

GOPAY_NEW_PAYMENT_URL = 'https://gate.gopay.cz/vytvorit-platbu'
GOPAY_REDIRECT_URL = 'https://gate.gopay.cz/zaplatit-plna-integrace'
GOPAY_PAYMENT_STATUS_URL = 'https://gate.gopay.cz/stav-platby-gw2'

VERIFY_SSL=False

try:
    from settings_local import *
except ImportError:
    pass
