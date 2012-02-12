# About django-gopay

This code is not a full implementation of the [gopay api](https://www.gopay.cz/jak-funguje-gopay/integrace). It's simple
implementation of the GoPayHTTP api which consists of only two api calls

* paymentCommand - which creates new payment command
* paymentStatus - which allows you to find out the result of the paymentCommand

It also provides payment status notification callback encryption validation.

There are no SOAP calls implemented, these cover more specific commands which will be implemented later, maybe.

#Installation
    pip install git@github.com:vlinhart/django-gopay.git#gopay

* add 'gopay' to the INSTALLED_APPS.
* add url(r'^gopay/', include('gopay.urls', namespace="gopay")) to urls.py
* set GOPAY_NOTIFICATION_CALLBACK in settings to your function which will handle gopay notification callback, 
like this GOPAY_NOTIFICATION_CALLBACK = 'gopay.utils.notification_callback'

