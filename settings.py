# -*- coding: utf-8 -*-

ESHOP_GOID = 1163419611
SECRET = "rtytJemTrcpE9VmRR5VRbrty"
GOPAY_URL = 'http://testgw.gopay.cz/vytvorit-platbu'
GOPAY_REDIRECT_URL = 'https://testgw.gopay.cz/zaplatit-plna-integrace'

try:
    from settings_local import *
except ImportError:
    pass
