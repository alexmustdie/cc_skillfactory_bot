import requests

from config import URL, APP_ID

class APIException(BaseException):

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message

class API:

    def __init__(self):
        self.values = None

    @staticmethod
    def request(url, **kwargs):
        while True:
            try:
                return requests.get(f'{url}?app_id={APP_ID}', timeout=10, **kwargs).json()
            except:
                raise APIException('Long wait for response, please try again')

    @staticmethod
    def get_price(base, quote, amount):
        response = API.request(f'{URL}/latest.json')
        rates = response['rates']
        return round(rates[quote] / rates[base] * amount, 2)

    def get_values(self):
        if not self.values:
            self.values = API.request(f'{URL}/currencies.json').keys()
        return self.values
