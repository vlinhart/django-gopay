# -*- coding: utf-8 -*-
import unittest
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

RESPONSE = """<?xml version="1.0" encoding="UTF-8"?>
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

class TestGoPay(unittest.TestCase):
    def test_concat_commands(self):
        expected_result = '1|test|100|235|http://tolary.cz|http://tolary.cz|111111111111111111111111'
        result = utils.concat_payment_command(secret=SECRET, **PAYMENT_COMMAND)
        self.assertEqual(expected_result, result)

        expected_result = '8363419680|test|100|235|CALL_COMPLETED|WAITING|111111111111111111111111'
        result = utils.concat_for_validation(secret=SECRET, **utils.parse_xml_to_dict(RESPONSE))
        self.assertEqual(expected_result, result)


    def test_encryption_methods_equal(self):
        command = utils.concat_payment_command(**PAYMENT_COMMAND)
        signature_pycrypt = utils.encrypt(command)
        signature_pydes = utils.encrypt_pydes(command)
        self.assertEqual(signature_pycrypt, signature_pydes)

    def test_decryption_methods_equal(self):
        response = utils.parse_xml_to_dict(RESPONSE)
        pycrypt = utils.decrypt(response['encryptedSignature'])
        pydes = utils.decrypt_pydes(response['encryptedSignature'])
        self.assertEqual(pycrypt, pydes)

    def test_decrypt(self):
        response = utils.parse_xml_to_dict(RESPONSE)
        response_cmd = utils.concat_for_validation(**response)
        hashed_cmd = utils.hash(response_cmd)
        decrypted = utils.decrypt(response['encryptedSignature'])
        self.assertEqual(hashed_cmd, decrypted)


    def test_parse_response_xml(self):
        response_dict = utils.parse_xml_to_dict(RESPONSE)
        self.assertEqual(response_dict['productName'], PAYMENT_COMMAND['productName'])

    def test_validate_response(self):
        self.assertTrue(utils.validate_xml_response(RESPONSE))

    def test_create_redirect_cmd(self):
        self.assertEqual(
            'https://testgw.gopay.cz/prima-integrace?sessionInfo.eshopGoId=8363419680&sessionInfo.encryptedSignature=7d9405a3f474e843a5f61c271f632a2899470f5623a18189941f0b86396699eebe6f77d937e960e3&sessionInfo.paymentSessionId=3000841324'
            ,
            utils.create_redirect_url('3000841324'))
