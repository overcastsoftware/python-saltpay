# -*- coding: utf-8 -*-

import os

from .context import saltpay_python

import unittest
import pytest
from random import randint


import random


@pytest.fixture
def creditcard():
    """
    test card  should be in ENV variable SALTPAY_TEST_CARD and contain information about the 
    card formatted as such:

        SALTPAY_TEST_CARD=number:<card number>,month:<month>,year:<year>,cvv:<CVV code>

    """
    testcard = os.getenv('SALTPAY_TEST_CARD', None)
    card = dict(map(lambda k: k.split(':'), testcard.split(",")))
    return card


@pytest.fixture
def credentials():
    apikey = os.getenv('SALTPAY_APIKEY', None)
    
    return {
        'apikey': apikey,
    }

@pytest.fixture
def saltpay(credentials):
    return saltpay_python.SaltpayClient(**credentials)

@pytest.fixture
def saltpay_v2(credentials):
    options = {'apiversion': '2.0'}
    options.update(**credentials)
    return saltpay_python.SaltpayClient(**options)

@pytest.fixture
def wrong_credentials():
    return {
        'apikey': "DummyApiKey"
    }

@pytest.fixture
def wrong_saltpay(wrong_credentials):
    return saltpay_python.SaltpayClient(**wrong_credentials)


@pytest.fixture
def verification_data():
    return {
        "cardholderAuthenticationVerificationData": "jq6EHIP0PfZEYwAAnuCpB4MAAAA=",
        "transactionXid": "nrQGVcVW0CIzw6wsqwIlxLAUTCE=",
    }


@pytest.fixture
def verification_data_v2():
    return {
        "cavv": "jq6EHIP0PfZEYwAAnuCpB4MAAAA=",
        "xid": "nrQGVcVW0CIzw6wsqwIlxLAUTCE=",
    }


@pytest.fixture
def verification_data_payment():
    return {
        "cardholderAuthenticationVerificationData": "jq6EHIP0PfZEYwAAnuCpB4MAAAA=",
        "transactionXid": "nrQGVcVW0CIzw6wsqwIlxLAUTCE=",
        "mdStatus": "1",
    }


@pytest.fixture
def verification_data_payment_v2():
    return {
        "cavv": "jq6EHIP0PfZEYwAAnuCpB4MAAAA=",
        "xid": "nrQGVcVW0CIzw6wsqwIlxLAUTCE=",
        "mdStatus": "1",
    }

@pytest.fixture
def verification_data_payment_transid_v2():
    return {
        "cavv": "jq6EHIP0PfZEYwAAnuCpB4MAAAA=",
        "xid": "nrQGVcVW0CIzw6wsqwIlxLAUTCE=",
        "mdStatus": "1",
        "dsTransId": None
    }



@pytest.mark.saltpay
def test_can_init_client(credentials):
    saltpay = saltpay_python.SaltpayClient(**credentials)


# @pytest.mark.saltpay
# def test_card_verification(saltpay, creditcard):

#     response = saltpay.CardVerification(creditcard['number'], creditcard['year'], creditcard['month'], 0, 'ISK', 'http://acme.com/success', 'http://acme.com/failed', merchantData='reference-1000')

#     assert 'cavv' in response
#     assert 'xid' in response

# @pytest.mark.saltpay
# def test_card_verification_json(saltpay, creditcard):

#     response = saltpay.CardVerification(creditcard['number'], creditcard['year'], creditcard['month'], 0, 'ISK', 'http://acme.com/success', 'http://acme.com/failed', merchantData='reference-1000', threeDeeSecureResponseType=saltpay.ThreeDeeSecureResponseType.JSON)

#     assert 'postUrl' in response.keys()
#     assert 'verificationFields' in response.keys()


@pytest.mark.saltpay
def test_create_virtual_card(saltpay, creditcard, verification_data):

    response = saltpay.TokenMultiRequest(creditcard['number'], creditcard['month'], creditcard['year'], 0, '352', creditcard['cvc'])
    assert response['Enabled']
    assert 'VirtualNumber' in response.keys()
    assert 'VerifyCardResult' in response.keys()
    assert response['VerifyCardResult']['ActionCode'] == '000'
    assert response['VirtualNumber'] == creditcard['virtual']


@pytest.mark.saltpay
def test_create_virtual_card_without_credentials_raises_exception(wrong_saltpay, creditcard, verification_data):

    with pytest.raises(saltpay_python.SaltpayException) as exc_info:
        response = wrong_saltpay.TokenMultiRequest(creditcard['number'], creditcard['month'], creditcard['year'], 0, '352', creditcard['cvc'])

# @pytest.mark.saltpay
# def test_create_virtual_card_without_verification_data_raises_exception(saltpay, creditcard, verification_data):

#     with pytest.raises(saltpay_python.SaltpayException) as exc_info:
#         response = saltpay.CreateVirtualCard(creditcard['number'], creditcard['year'], creditcard['month'], creditcard['cvc'], cardVerificationData=None)


# @pytest.mark.saltpay
# def test_card_payment(saltpay, creditcard, verification_data_payment):
#     response = saltpay.CardPayment(creditcard['number'], creditcard['year'], creditcard['month'], creditcard['cvc'], 100, "ISK", saltpay.CardOperation.Sale, saltpay.TransactionType.ECommerce, cardVerificationData=verification_data_payment)
#     assert response["isSuccess"] == True


@pytest.mark.saltpay
def test_virtual_card_payment(saltpay, creditcard, verification_data):
    t_id = random.randint(1,100000)
    order_id = f'{t_id:012}'

    response = saltpay.Payment(creditcard['token'], 100, "352", order_id)

    assert response['TransactionStatus'] == 'Accepted'
    assert response['ActionCode'] == '000'
    assert response['PaymentMethod']['Token'] == creditcard['token']

@pytest.mark.saltpay
def test_virtual_card_payment_and_refund(saltpay, creditcard, verification_data):
    t_id = random.randint(1,100000)
    order_id = f'{t_id:012}'
    response = saltpay.Payment(creditcard['token'], 100, "352", order_id)

    assert response['TransactionStatus'] == 'Accepted'
    assert response['ActionCode'] == '000'
    assert response['PaymentMethod']['Token'] == creditcard['token']

    response2 = saltpay.Refund(response['TransactionId'])
    assert response2['ActionCode'] == '000'
    assert 'RefundTransactionId' in response2.keys()

# @pytest.mark.saltpay
# def test_create_virtual_card_v2(saltpay_v2, creditcard, verification_data_v2):

#     response = saltpay_v2.CreateVirtualCard(creditcard['number'], creditcard['year'], creditcard['month'], creditcard['cvc'], cardVerificationData=verification_data_v2)

#     assert response['isSuccess'] == True
#     assert 'virtualCard' in response.keys()

# @pytest.mark.saltpay
# def test_card_payment_v2(saltpay_v2, creditcard, verification_data_payment_v2):
#     response = saltpay_v2.CardPayment(creditcard['number'], creditcard['year'], creditcard['month'], creditcard['cvc'], 100, "ISK", saltpay_v2.CardOperation.Sale, saltpay_v2.TransactionType.ECommerce, cardVerificationData=verification_data_payment_v2)
#     assert response["isSuccess"] == True

# @pytest.mark.saltpay
# def test_virtual_card_payment_v2(saltpay_v2, creditcard, verification_data_v2):
#     response = saltpay_v2.VirtualCardPayment(creditcard['virtual'], 100, "ISK", saltpay_v2.VirtualCardOperation.Sale)
#     assert response["isSuccess"] == True

# @pytest.mark.saltpay
# def test_card_payment_transid_v2(saltpay_v2, creditcard, verification_data_payment_transid_v2):
#     response = saltpay_v2.CardPayment(creditcard['number'], creditcard['year'], creditcard['month'], creditcard['cvc'], 100, "ISK", saltpay_v2.CardOperation.Sale, saltpay_v2.TransactionType.ECommerce, cardVerificationData=verification_data_payment_transid_v2)
#     print(response)
#     assert response["isSuccess"] == True
