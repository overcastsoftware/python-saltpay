# -*- coding: utf-8 -*-

import os

from .context import saltpay_python

import unittest
import pytest
from random import randint

CurrencyClass = saltpay_python.currencies.ISO4217

@pytest.mark.currencies
def test_can_init_currency():
    
    assert CurrencyClass("ISK").value == "ISK"

@pytest.mark.currencies
def test_invalid_currency_raises_exception():
    
    with pytest.raises(ValueError) as exc_info:
        CurrencyClass("BLA")

