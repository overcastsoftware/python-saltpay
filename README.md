[![Build Status](https://travis-ci.org/overcastsoftware/python-saltpay.svg?branch=master)](https://travis-ci.org/overcastsoftware/python-saltpay)

Borgun/SaltPay python library
========================

Python implementation of the Borgun/SaltPay payments solution RPG. See [https://docs.borgun.is/paymentgateways/bapi/](https://docs.borgun.is/paymentgateways/bapi/).


Test coverage
=============
<img width="615" alt="Screenshot 2021-04-16 at 16 45 31" src="https://user-images.githubusercontent.com/143557/115057121-2f131580-9ed3-11eb-99e9-8cd3eaf01e23.png">


Testing
=======

You need to create a pytest.ini file in the project root with the following contents, you need to fill in the credentials supplied by Saltpay:

```
[pytest]
env =
    SALTPAY_APIKEY=<APIKEY>
    SALTPAY_TEST_CARD=number:<test_number>,month:<test_month>,year:<test_year>,cvv:<test_cvv>,virtual:<virtual_test_number>
```

Running tests
-------------

You can run the whole suite:

```
    make test
````

Or pick your module to test:

```
    make test_currencies
    make test_saltpay
```


