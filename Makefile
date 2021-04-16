init:
	pip install -r requirements.txt

test:
	pytest -s -v --cov=saltpay_python --cov-report=html tests

# test_saltpay:
# 	pytest -s -v -m saltpay tests

# test_currencies:
# 	pytest -s -v -m currencies tests

# test_saltpay:
# 	pytest -s -v -m saltpay tests
