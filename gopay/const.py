# -*- coding: utf-8 -*-
from django.conf import settings

PAYMENT_DONE = "PAYMENT_DONE"
CANCELED = "CANCELED"
TIMEOUTED = "TIMEOUTED"
WAITING = "WAITING"
FAILED = "FAILED"
CALL_COMPLETED = "CALL_COMPLETED"
UNKNOWN = "UNKNOWN"

PAYMENT_METHODS = set((
    'eu_mb_a',
    'eu_mb_b',
    'eu_mb_w',
    'SUPERCASH',
    'cz_sms',
    'cz_kb',
    'cz_rb',
    'cz_mb',
    'cz_ge',
    'cz_fb',
    'cz_vb',
    'cz_bank',
    'cz_gp_w',
    'cz_gp_c',
))


PREFIX_CMD_PAYMENT = 'paymentCommand.'
PREFIX_CMD_PAYMENT_RESULT = 'paymentSessionInfo.'
PREFIX_CMD_REDIRECT_URL = 'sessionInfo.'

GOPAY_NEW_PAYMENT_URL_TEST = 'https://testgw.gopay.cz/vytvorit-platbu'
GOPAY_REDIRECT_URL_TEST = 'https://testgw.gopay.cz/zaplatit-plna-integrace'
GOPAY_PAYMENT_STATUS_URL_TEST = 'https://testgw.gopay.cz/stav-platby-gw2'

GOPAY_NEW_PAYMENT_URL_PRODUCTION = 'https://gate.gopay.cz/vytvorit-platbu'
GOPAY_REDIRECT_URL_PRODUCTION = 'https://gate.gopay.cz/zaplatit-plna-integrace'
GOPAY_PAYMENT_STATUS_URL_PRODUCTION = 'https://gate.gopay.cz/stav-platby-gw2'

GOPAY_NEW_PAYMENT_URL = GOPAY_NEW_PAYMENT_URL_PRODUCTION
GOPAY_REDIRECT_URL = GOPAY_REDIRECT_URL_PRODUCTION
GOPAY_PAYMENT_STATUS_URL = GOPAY_PAYMENT_STATUS_URL_PRODUCTION

if settings.GOPAY_TESTING_MODE:
    GOPAY_NEW_PAYMENT_URL = GOPAY_NEW_PAYMENT_URL_TEST
    GOPAY_REDIRECT_URL = GOPAY_REDIRECT_URL_TEST
    GOPAY_PAYMENT_STATUS_URL = GOPAY_PAYMENT_STATUS_URL_TEST
