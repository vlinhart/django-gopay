# -*- coding: utf-8 -*-
from django.conf import settings

PAYMENT_DONE = "PAYMENT_DONE"
CANCELED = "CANCELED"
TIMEOUTED = "TIMEOUTED"
WAITING = "WAITING"
FAILED = "FAILED"
CALL_COMPLETED = "CALL_COMPLETED"
UNKNOWN = "UNKNOWN"

PAYMENT_COMMAND = {
    'successURL': 'http://tolary.cz',
    'failedURL': 'http://tolary.cz',
    'productName': 'test',
    'eshopGoId': settings.ESHOP_GOID,
    'variableSymbol': '235',
    'totalPrice': 100,
    }

PREFIX_CMD_PAYMENT = 'paymentCommand.'
PREFIX_CMD_PAYMENT_RESULT = 'paymentSessionInfo.'
PREFIX_CMD_REDIRECT_URL = 'sessionInfo.'

GOPAY_NEW_PAYMENT_URL_TEST = 'https://testgw.gopay.cz/vytvorit-platbu'
GOPAY_REDIRECT_URL_TEST = 'https://testgw.gopay.cz/zaplatit-plna-integrace'
GOPAY_PAYMENT_STATUS_URL_TEST = 'https://testgw.gopay.cz/stav-platby-gw2'

GOPAY_NEW_PAYMENT_URL = 'https://gate.gopay.cz/vytvorit-platbu'
GOPAY_REDIRECT_URL = 'https://gate.gopay.cz/zaplatit-plna-integrace'
GOPAY_PAYMENT_STATUS_URL = 'https://gate.gopay.cz/stav-platby-gw2'
