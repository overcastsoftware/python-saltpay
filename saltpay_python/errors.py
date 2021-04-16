
class SaltpayException(Exception):

    def __init__(self, message):
        print(message)
        self.message = message
