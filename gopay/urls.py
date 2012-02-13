# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('gopay.views',
    url(r'^success$', 'gopay_success', name='gopay_success'),
    url(r'^failure$', 'gopay_failure', name='gopay_failure'),
    url(r'^notification$', 'gopay_notification', name='gopay_notification'),
)
