# -*- coding: utf-8 -*-
from Crypto.Cipher import DES3
from hashlib import sha1
from binascii import unhexlify
import xml.etree.ElementTree as ET
import urllib
import settings


def concat_payment_command(eshopGoId, productName, totalPrice, variableSymbol, failedURL, successURL,
                           secret=settings.SECRET):
    bits = [eshopGoId, productName, totalPrice, variableSymbol, failedURL, successURL, secret]
    return '|'.join([bit if isinstance(bit, basestring) else str(bit) for bit in bits])


def concat_for_validation(eshopGoId, productName, totalPrice, variableSymbol, result, sessionState,
                          secret=settings.SECRET, **kwargs):
    bits = [eshopGoId, productName, totalPrice, variableSymbol, result, sessionState, secret]
    return '|'.join([bit if isinstance(bit, basestring) else str(bit) for bit in bits])


def concat_for_redirect(eshopGoId, paymentSessionId, secret=settings.SECRET, **kwargs):
    bits = [eshopGoId, paymentSessionId, secret]
    return '|'.join([bit if isinstance(bit, basestring) else str(bit) for bit in bits])


def prefix_payment_command_keys(command, prefix='paymentCommand.'):
    prefixed = {}
    for k, v in command.items():
        prefixed[prefix + k] = v
    return prefixed


def hash(string):
    h = sha1()
    h.update(string)
    return h.hexdigest()


def encrypt(command, key=settings.SECRET):
    hashed_command = hash(command)
    des = DES3.new(key, DES3.MODE_ECB)
    result = des.encrypt(hashed_command)
    return result.encode('hex')


def encrypt_pydes(command, key=settings.SECRET):
    from pyDes import triple_des

    hashed_command = hash(command)
    des = triple_des(key)
    result = des.encrypt(hashed_command)
    return result.encode('hex')


def decrypt_pydes(encrypted_data, key=settings.SECRET):
    from pyDes import triple_des

    des = triple_des(key)
    return des.decrypt(unhexlify(encrypted_data)).rstrip('\x00')


def decrypt(encrypted_data, key=settings.SECRET):
    des = DES3.new(key, DES3.MODE_ECB)
    return des.decrypt(unhexlify(encrypted_data)).rstrip('\x00')


def parse_xml_to_dict(xml):
    tree = ET.XML(xml)
    response_dict = {}
    for e in tree:
        response_dict[e.tag] = e.text
    return response_dict


def validate_xml_response(xml):
    response = parse_xml_to_dict(xml)
    print response
    response_cmd = concat_for_validation(**response)
    hashed_cmd = hash(response_cmd)
    decrypted = decrypt(response['encryptedSignature'])
    #    print encrypted
    #    print response['encryptedSignature']
    return decrypted == hashed_cmd


def create_redirect_url(paymentSessionId):
    redirect_cmd = dict(eshopGoId=settings.ESHOP_GOID, paymentSessionId=paymentSessionId)
    command = concat_for_redirect(**redirect_cmd)
    redirect_cmd['encryptedSignature'] = encrypt(command)
    redirect_cmd = prefix_payment_command_keys(redirect_cmd,prefix='sessionInfo.')
    return settings.GOPAY_REDIRECT_URL + '?' + urllib.urlencode(redirect_cmd)
