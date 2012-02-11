# -*- coding: utf-8 -*-
import requests
import const
import utils
import settings

class Payment(object):
    def __init__(self, secret=settings.SECRET):
        self.crypt = utils.Crypt(secret=secret)
        self.concat = utils.Concat(secret=secret)

    def create_payment(self, payment_data):
        payment_string = self.concat.command(utils.Concat.PAYMENT, payment_data)
        payment_data['encryptedSignature'] = self.crypt.encrypt(payment_string)
        payment_data = utils.prefix_command_keys(payment_data, 'paymentCommand.')
        r = requests.post(settings.GOPAY_NEW_PAYMENT_URL, data=payment_data, verify=False) #TODO verify ssl?

        if r.status_code != 200:
            raise utils.ValidationException(u'wrong status code: %s' % r.status_code)
        utils.ValidateResponse(r.content).payment()

        response = utils.parse_xml_to_dict(r.content)
        print response
        return response['paymentSessionId']


    def verify_payment_status(self, paymentSessionId):
        cmd = dict(eshopGoId=settings.ESHOP_GOID, paymentSessionId=paymentSessionId)
        concat_cmd = self.concat.command(utils.Concat.PAYMENT_STATUS, cmd)
        cmd['encryptedSignature'] = self.crypt.encrypt(concat_cmd)
        cmd = utils.prefix_command_keys(cmd, prefix='paymentSessionInfo.')
        r = requests.post(settings.GOPAY_PAYMENT_STATUS_URL, data=cmd, verify=False) #TODO verify ssl?

        if r.status_code != 200:
            raise utils.ValidationException(u'wrong status code: %s' % r.status_code)
        utils.ValidateResponse(r.content).payment_status()
        response = utils.parse_xml_to_dict(r.content)
        print response

        #TODO check the result and do somethin


if __name__ == '__main__':
    p = Payment()

#    paymentSessionId = p.create_payment(const.PAYMENT_COMMAND)
#    print 'paymentSessionId', paymentSessionId
#    print utils.create_redirect_url(paymentSessionId)
    p.verify_payment_status('3000842143')

