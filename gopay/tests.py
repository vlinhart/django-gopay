# -*- coding: utf-8 -*-
import unittest
import settings
import utils

PAYMENT_COMMAND = {
    'successURL': 'http://tolary.cz',
    'failedURL': 'http://tolary.cz',
    'productName': 'test',
    'eshopGoId': '1',
    'variableSymbol': '235',
    'totalPrice': 100,
    }

SECRET = '111111111111111111111111'

PAYMENT_RESULT_RESPONSE = """<?xml version="1.0" encoding="UTF-8"?>
<ePaymentResult>
  <paymentSessionId>3000841324</paymentSessionId>
  <url>http://tolary.cz</url>
  <sessionState>WAITING</sessionState>
  <result>CALL_COMPLETED</result>
  <resultDescription>WAITING</resultDescription>
  <productName>test</productName>
  <eshopGoId>8363419680</eshopGoId>
  <variableSymbol>235</variableSymbol>
  <totalPrice>100</totalPrice>
  <encryptedSignature>58ed2745b1a1905e0be962c45cdb04be5d726def8e839d047e0436e29f7162afb266b3b2268c25e8435d6a611a35f177</encryptedSignature>
</ePaymentResult>
"""

PAYMENT_STATUS_RESPONSE = """<?xml version="1.0" encoding="UTF-8"?>
<ePaymentStatus>
  <paymentSessionId>3000842143</paymentSessionId>
  <url>http://tolary.cz</url>
  <sessionState>TIMEOUTED</sessionState>
  <result>CALL_COMPLETED</result>
  <resultDescription>TIMEOUTED</resultDescription>
  <productName>test</productName>
  <eshopGoId>8363419680</eshopGoId>
  <variableSymbol>235</variableSymbol>
  <totalPrice>100</totalPrice>
  <encryptedSignature>a5d48c13bbb27ce6a914bfddf17ee57b8485744d6e2d4bb96ca9afeeeccd1b09db9c065837a361b3435d6a611a35f177</encryptedSignature>
</ePaymentStatus>
"""

class TestGoPay(unittest.TestCase):
    crypt = utils.Crypt()
    concat = utils.Concat()

    def test_concat_commands(self):
        expected_result = '1|test|100|235|http://tolary.cz|http://tolary.cz|111111111111111111111111'
        result = utils.Concat(secret=SECRET).command(utils.Concat.PAYMENT, PAYMENT_COMMAND)
        self.assertEqual(expected_result, result)

        #try another way to call Concat
        result = utils.Concat(secret=SECRET)(utils.Concat.PAYMENT, PAYMENT_COMMAND)
        self.assertEqual(expected_result, result)

        expected_result = '8363419680|test|100|235|CALL_COMPLETED|WAITING|111111111111111111111111'
        result = utils.Concat(secret=SECRET).command(utils.Concat.PAYMENT_RESULT,
            utils.parse_xml_to_dict(PAYMENT_RESULT_RESPONSE))
        self.assertEqual(expected_result, result)


    def test_encryption_methods_equal(self):
        command = self.concat(utils.Concat.PAYMENT, PAYMENT_COMMAND)
        signature_pycrypt = self.crypt.encrypt(command)
        signature_pydes = self.crypt.encrypt_pydes(command)
        self.assertEqual(signature_pycrypt, signature_pydes)

    def test_decryption_methods_equal(self):
        response = utils.parse_xml_to_dict(PAYMENT_RESULT_RESPONSE)
        pycrypt = self.crypt.decrypt(response['encryptedSignature'])
        pydes = self.crypt.decrypt_pydes(response['encryptedSignature'])
        self.assertEqual(pycrypt, pydes)

    def test_decrypt(self):
        response = utils.parse_xml_to_dict(PAYMENT_RESULT_RESPONSE)
        response_cmd = self.concat(utils.Concat.PAYMENT_RESULT, response)
        hashed_cmd = self.crypt.hash(response_cmd)
        decrypted = self.crypt.decrypt(response['encryptedSignature'])
        self.assertEqual(hashed_cmd, decrypted)


    def test_parse_response_xml(self):
        response_dict = utils.parse_xml_to_dict(PAYMENT_RESULT_RESPONSE)
        self.assertEqual(response_dict['productName'], PAYMENT_COMMAND['productName'])

    def test_validate_payment_response(self):
        self.assertEqual(utils.CommandsValidator(PAYMENT_RESULT_RESPONSE).payment(), None)

    def test_validate_payment_status_response(self):
        self.assertEqual(utils.CommandsValidator(PAYMENT_STATUS_RESPONSE).payment_status(), None)

    def test_create_redirect_cmd(self):
        self.assertEqual(
            settings.GOPAY_REDIRECT_URL_TEST + '?sessionInfo.eshopGoId=8363419680&sessionInfo.encryptedSignature=7d9405a3f474e843a5f61c271f632a2899470f5623a18189941f0b86396699eebe6f77d937e960e3&sessionInfo.paymentSessionId=3000841324'
            ,
            utils.create_redirect_url('3000841324'))
