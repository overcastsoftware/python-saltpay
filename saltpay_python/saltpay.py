 # -*- coding: utf-8 -*-

from datetime import date, datetime, timedelta
import base64
from .errors import SaltpayException
import uuid
from enum import Enum
import requests
from .currencies import ISO4217Numeric

class SaltpayClient(object):

    def format_url(self, path):
        return "{}{}".format(self.ENDPOINT, path)

    def check_error(self, response):
        if response.status_code == 400:
            errors = response.json()
            raise SaltpayException(errors["Message"])
        if response.status_code == 401:
            raise SaltpayException("401 credentials error")



    def __init__(self, apikey, testing=True, apiversion='1.0'):
        self.APIKEY = apikey
        self.TESTING = testing
        self.APIVERSION = apiversion

        self.ENDPOINT = 'https://test.borgun.is/rpg/'
        if not testing:
            self.ENDPOINT = 'https://ecommerce.borgun.is/rpg/'


    def make_request(self, action, method, **args):
        if method == 'POST':
            response = requests.post(self.format_url(action), auth=(self.APIKEY, ''), **args)

        self.check_error(response)
        return response.json()


    def TokenMultiRequest(self, PAN, ExpMonth, ExpYear, CheckAmount, Currency, CVC):

        assert str(Currency) in ISO4217Numeric

        payload = {
            "PAN": PAN,
            "ExpMonth": ExpMonth,
            "ExpYear": ExpYear,
            "VerifyCard": {
                "CheckAmount": CheckAmount,
                "Currency": Currency,
                "CVC": CVC,
            }
        }        

        return self.make_request("/api/token/multi", "POST", json=payload)

    def Payment(self, Token, Amount, Currency, CVC, OrderId):

        assert str(Currency) in ISO4217Numeric

        TransactionDate = date.today().isoformat()

        payload = {
            "TransactionType": "Sale",
            "Amount": Amount,
            "Currency": Currency,
            "TransactionDate": TransactionDate,
            "OrderId": "WHATTHEHELL1",
            "PaymentMethod": {
                "PaymentType": "TokenMulti",
                "Token": Token,
                "CVC": CVC,
            }
        }        

        return self.make_request("/api/payment", "POST", json=payload)

