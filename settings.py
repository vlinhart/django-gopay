# -*- coding: utf-8 -*-

ESHOP_GOID = 1163419611
SECRET = "rtytJemTrcpE9VmRR5VRbrty"
GOPAY_NEW_PAYMENT_URL = 'http://testgw.gopay.cz/vytvorit-platbu'
GOPAY_REDIRECT_URL = 'https://testgw.gopay.cz/zaplatit-plna-integrace'
GOPAY_PAYMENT_STATUS_URL = 'https://testgw.gopay.cz/stav-platby-gw2'

try:
    from settings_local import *
except ImportError:
    pass
