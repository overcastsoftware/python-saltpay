 # -*- coding: utf-8 -*-

import base64
import uuid
from datetime import date, datetime, timedelta
from enum import Enum

import requests

from .currencies import ISO4217Numeric
from .errors import SaltpayException


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
        if method == 'GET':
            response = requests.get(self.format_url(action), auth=(self.APIKEY, ''), **args)
        if method == 'PUT':
            response = requests.put(self.format_url(action), auth=(self.APIKEY, ''), **args)

        self.check_error(response)
        print(response.content)
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

    def Payment(self, Token, Amount, Currency, OrderId, MpiToken=None):

        assert str(Currency) in ISO4217Numeric

        TransactionDate = date.today().isoformat()

        payload = {
            "TransactionType": "Sale",
            "Amount": Amount,
            "Currency": Currency,
            "TransactionDate": TransactionDate,
            "OrderId": OrderId,
        }

        if Token.startswith("99") and len(Token) == 16:
            payload["PaymentMethod"] = {
                "PaymentType": "Card",
                "PAN": Token,
            }
        else:
            payload["PaymentMethod"] = {
                "PaymentType": "TokenMulti",
                "Token": Token,
            }

        if MpiToken:
            payload["ThreeDSecure"] = {
                "DataType": "Token",
                "MpiToken": MpiToken,
            }

        return self.make_request("/api/payment", "POST", json=payload)

    def Refund(self, TransactionId):
        return self.make_request(f"/api/payment/{TransactionId}/refund", "PUT")


    def Enrollment(self, PAN, ExpMonth, ExpYear, Amount, Exponent, Currency, CVC2, OkUrl, FailUrl, TermUrl, MD=''):
        payload = {
            "CardDetails": {
                "PaymentType": "Card",
                "PAN": PAN,
                "ExpYear": ExpYear,
                "ExpMonth": ExpMonth,
                "CVC2": CVC2,
            },
            "PurchAmount": Amount,
            "Exponent": Exponent,
            "Currency": Currency,
            "MD": base64.b64encode(MD.encode()).decode('utf-8'),
            "OkUrl": OkUrl,
            "FailUrl": FailUrl,
            "TermUrl": TermUrl,
        }

        response = self.make_request("/api/mpi/v2/enrollment", "POST", json=payload)

        if response["ResultStatus"] == 0 and response["MdStatus"] == "9":
            url = ""
            fields = {}
            for item in response["RedirectToACSData"]:
                if item["Name"] == "actionURL":
                    url = item["Value"]
                else:
                    fields[item["Name"]] = item["Value"]

            return {
                'token': response['MPIToken'],
                'postUrl': url,
                'verificationFields': fields,
                'html': response['RedirectToACSForm']
            }
        elif response["ResultStatus"] == 0 and response["MdStatus"] in ["1", "2", "3", "4"]:
            return {
                'token': response['MPIToken'],
                'postUrl': '',
                'verificationFields': '',
                'html': '',
            }
        if 'MdErrorMessage' in response.keys():
            raise SaltpayException(message=f"Unsuccessful request. {response['MdErrorMessage']}")
        else:
            raise SaltpayException(message=f"Unsuccessful request.")


    def Validation(self, PARes=None, CRes=None):

        payload =  {}
        if PARes or (PARes and CRes):
            payload = {
                "PARes": PARes,
            }
        if not PARes and CRes:
            payload = {
                "CRes": CRes
            }

        response = self.make_request("/api/mpi/v2/validation", "POST", json=payload)

        if response['MdStatus'] == '1' or response['MdStatus'] == '9':
            return True

        raise SaltpayException(message=f"Unsuccessful request. {response['MdErrorMessage']}")
