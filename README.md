# About django-gopay

This code is not a full implementation of the [gopay api](https://www.gopay.cz/jak-funguje-gopay/integrace) according to
[integration manual](https://www.gopay.cz/download/GoPay-integracni-manual_v_1_9.pdf). 
It's simple implementation of the GoPayHTTP api which consists of only two api calls

* paymentCommand - which creates new payment command
* paymentStatus - which allows you to find out the result of the paymentCommand

It also provides payment status notification callback encryption validation.

There are no SOAP calls implemented, these cover more specific commands which will be implemented later, maybe.

##Installation
    pip install git+git://github.com/vlinhart/django-gopay.git#egg=gopay
    add 'gopay' to the INSTALLED_APPS.
    add url(r'^gopay/', include('gopay.urls', namespace="gopay")) to urls.py

##Configuration
It's necessary to set several constants in settings.py:

    GOPAY_ESHOP_GOID = your gopay id
    GOPAY_SECRET = 'your gopay secret'
    GOPAY_SUCCESS_URL = 'url to which user will be redirected after successful payment on GOPAY'
    GOPAY_FAILED_URL = 'url to which user will be redirected after failed payment on GOPAY'
    GOPAY_NOTIFICATION_CALLBACK = 'gopay.utils.notification_callback' more about this later
    GOPAY_TESTING_MODE = True # set to False if you want the production URLS for gopay

    optional is:
    GOPAY_VERIFY_SSL = False #if you want the ssl cert of gopay to be checked ala browser, set it to True

###More about GOPAY_NOTIFICATION_CALLBACK
You need to create this method to process the successfull payment/failure/notification from GOPAY. It's called
in these three situations after the caller was verified. You should process the payment in this function.
Its' signature is

    def gopay_notification_callback(request, paid_ok, payment_details, type, paymentSessionId, variableSymbol)

* request - django request object
* paid_ok - whether the payment was really finished and money were transfered
* payment_details - dict containing payment details as returned from GOPAY, see GOPAY integration manual 13.7
* type - which url this was called from ('notification'/ 'success' / 'failure')
* paymentSessionId - gopay session id
* variableSymbol - variable symbol
