# -*- coding: utf-8 -*-
import requests
import utils
import settings

PAYMENT_COMMAND = {
    'successURL': 'http://tolary.cz',
    'failedURL': 'http://tolary.cz',
    'productName': 'test',
    'eshopGoId': settings.ESHOP_GOID,
    'variableSymbol': '235',
    'totalPrice': 100,
    }


def create_payment(payment_data):
    payment_cmd = utils.prefix_payment_command_keys(payment_data)
    payment_string = utils.concat_payment_command(**payment_data)
    encryptedSignature = utils.encrypt(payment_string)
    payment_cmd['paymentCommand.encryptedSignature'] = encryptedSignature
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    r = requests.post(settings.GOPAY_URL, data=payment_cmd, verify=False, headers=headers) #TODO verify ssl?
    if r.status_code == 200 and utils.validate_xml_response(r.content):
        response = utils.parse_xml_to_dict(r.content)
        print response
        return response['paymentSessionId']
    else:
        #TODO throw some menacing exception
        pass


if __name__ == '__main__':
#    test_string = "paymentCommand.encryptedSignature=%s&paymentCommand.eshopGoId=%s&paymentCommand.productName=%s&paymentCommand.totalPrice=%s&paymentCommand.variableSymbol=%s&paymentCommand.failedURL=%s&paymentCommand.successURL=%s"
#    test_string = test_string % (
#    encryptedSignature, settings.ESHOP_GOID, 'test', 100, '235', 'http://tolary.cz', 'http://tolary.cz')

#    create_payment(test_string)
    paymentSessionId = create_payment(PAYMENT_COMMAND)
    print 'paymentSessionId', paymentSessionId
    print utils.create_redirect_url(paymentSessionId)



