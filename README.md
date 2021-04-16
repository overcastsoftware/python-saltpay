[![Build Status](https://travis-ci.org/overcastsoftware/python-saltpay.svg?branch=master)](https://travis-ci.org/overcastsoftware/python-saltpay)

Borgun/SaltPay python library
========================

Python implementation of the Borgun/SaltPay payments solution RPG. See [https://docs.borgun.is/paymentgateways/bapi/](https://docs.borgun.is/paymentgateways/bapi/).


Test coverage
=============
<img width="694" alt="Coverage report" src="https://user-images.githubusercontent.com/143557/114572408-fa9b2180-9c66-11eb-9140-0f64da2ebd2f.png">


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


