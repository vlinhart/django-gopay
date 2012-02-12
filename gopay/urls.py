# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('gopay.views',
    url(r'^notification$', 'gopay_notification', name='gopay_notification'),
)
