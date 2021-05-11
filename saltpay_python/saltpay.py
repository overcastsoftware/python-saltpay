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

    def Payment(self, Token, Amount, Currency, OrderId, MpiToken=None):

        assert str(Currency) in ISO4217Numeric

        TransactionDate = date.today().isoformat()

        payload = {
            "TransactionType": "Sale",
            "Amount": Amount,
            "Currency": Currency,
            "TransactionDate": TransactionDate,
            "OrderId": OrderId,
            "PaymentMethod": {
                "PaymentType": "TokenMulti",
                "Token": Token,
            }
        }
        if MpiToken:
            payload["ThreeDSecure"] = {
                "DataType": "Token",
                "MpiToken": MpiToken,
            }

        return self.make_request("/api/payment", "POST", json=payload)


    def Enrollment(self, PAN, ExpMonth, ExpYear, Amount, Exponent, Currency, CVC2, OkUrl, FailUrl, TermUrl, MD=''):
        payload = {
            "CardDetails": {
                "PaymentType": "Card",
                "PAN": PAN,
                "ExpYear": ExpYear,
                "ExpMonth": ExpMonth,
                "CVC2": CVC2,
            },
            "Amount": Amount,
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
        raise SaltpayException(message=f"Unsuccessful request. {response['MdErrorMessage']}")


    def Validation(self, PARes=None, CRes=None):

        if PARes or (PARes and CERes):

            payload = {
                "PARes": PARes,
            }
        if not PARes and CRes:
            payload = {
                "CRes": CRes
            }

        response = self.make_request("/api/mpi/v2/validation", "POST", json=payload)

        if response['MdStatus'] == '1':
            return True
        
        raise SaltpayException(message=f"Unsuccessful request. {response['MdErrorMessage']}")
