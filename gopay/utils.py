# -*- coding: utf-8 -*-
from copy import copy
from Crypto.Cipher import DES3
from hashlib import sha1
from binascii import unhexlify
import xml.etree.ElementTree as ET
import urllib
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
import const


class ValidationException(Exception):
    pass


class Concat(object):
    PAYMENT = ['eshopGoId', 'productName', 'totalPrice', 'variableSymbol', 'failedURL', 'successURL', 'secret']
    PAYMENT_RESULT = ['eshopGoId', 'productName', 'totalPrice', 'variableSymbol', 'result', 'sessionState', 'secret']
    REDIRECT = ['eshopGoId', 'paymentSessionId', 'secret']
    PAYMENT_STATUS = ['eshopGoId', 'paymentSessionId', 'secret']
    PAYMENT_STATUS_RESULT = ['eshopGoId', 'productName', 'totalPrice', 'variableSymbol', 'result', 'sessionState',
                             'paymentChannel', 'secret']
    PAYMENT_NOTIFICATION = ['eshopGoId', 'paymentSessionId', 'variableSymbol', 'secret']

    def __init__(self, secret=settings.GOPAY_SECRET):
        self.secret = secret

    def __call__(self, command, data):
        """instance can be called with the same result as calling command method"""
        return self.command(command, data)

    def command(self, keys, data):
        cp_data = copy(data)
        cp_data['secret'] = self.secret
        return self.concat_bits([cp_data[key] for key in keys])

    def concat_bits(self, bits):
        return '|'.join([bit if isinstance(bit, basestring) else str(bit) for bit in bits])


class Crypt(object):
    """ takes care of hashing, encryption and decrypting of commands"""

    def __init__(self, secret=settings.GOPAY_SECRET):
        self.secret = secret

    def hash(self, string):
        h = sha1()
        h.update(string)
        return h.hexdigest()


    def encrypt(self, command):
        hashed_command = self.hash(command)
        des = DES3.new(self.secret, DES3.MODE_ECB)
        result = des.encrypt(hashed_command)
        return result.encode('hex')


    def encrypt_pydes(self, command):
        from pyDes import triple_des

        hashed_command = self.hash(command)
        des = triple_des(self.secret)
        result = des.encrypt(hashed_command)
        return result.encode('hex')


    def decrypt(self, encrypted_data):
        des = DES3.new(self.secret, DES3.MODE_ECB)
        return des.decrypt(unhexlify(encrypted_data)).rstrip('\x00')

    def decrypt_pydes(self, encrypted_data):
        from pyDes import triple_des

        des = triple_des(self.secret)
        return des.decrypt(unhexlify(encrypted_data)).rstrip('\x00')


class CommandsValidator(object):
    concat = Concat()

    def __init__(self, xml_response, data=None):
        self.xml = xml_response
        self.response = data if data else parse_xml_to_dict(xml_response)
        self.crypt = Crypt()


    def _basic_result_validation(self):
    #        print self.response
        if self.response['result'] != const.CALL_COMPLETED:
            raise ValidationException(
                u'wrong result: %s - %s' % (self.response['result'], self.response['resultDescription']))

    def _signature_validation(self, response_cmd):
        hashed_cmd = self.crypt.hash(response_cmd)
        decrypted = self.crypt.decrypt(self.response['encryptedSignature'])
        if not decrypted == hashed_cmd:
            raise ValidationException(u'wrong signature')

    def payment(self):
        self._basic_result_validation()
        response_cmd = self.concat(Concat.PAYMENT_RESULT, self.response)
        self._signature_validation(response_cmd)

    def payment_status(self):
        self._basic_result_validation()
        if 'paymentChannel' not in self.response:
            self.response['paymentChannel'] = '' #strange but necessary
        response_cmd = self.concat(Concat.PAYMENT_STATUS_RESULT, self.response)
        self._signature_validation(response_cmd)

    def payment_notification(self):
        response_cmd = self.concat(Concat.PAYMENT_NOTIFICATION, self.response)
        self._signature_validation(response_cmd)


def prefix_command_keys(command, prefix):
    prefixed = {}
    for k, v in command.items():
        prefixed[prefix + k] = v
    return prefixed


def parse_xml_to_dict(xml):
    tree = ET.XML(xml)
    response_dict = {}
    for e in tree:
        response_dict[e.tag] = e.text
    return response_dict


def create_redirect_url(paymentSessionId):
    cmd = dict(eshopGoId=settings.GOPAY_ESHOP_GOID, paymentSessionId=paymentSessionId)
    concat_cmd = Concat().command(Concat.REDIRECT, cmd)
    cmd['encryptedSignature'] = Crypt().encrypt(concat_cmd)
    cmd = prefix_command_keys(cmd, prefix=const.PREFIX_CMD_REDIRECT_URL)
    return const.GOPAY_REDIRECT_URL_TEST + '?' + urllib.urlencode(cmd)


def notification_callback(request, paid_ok, type, paymentSessionId, variableSymbol):
    """ do some order processing here based on arguments """

    if paid_ok:
        pass #process the payment
    else:
        pass #process the failure
    return render(request, "gopay/%s.html" % type, locals())
