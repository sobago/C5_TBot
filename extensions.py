import requests
import json
from config import keys


class APIException(Exception):
    pass


class APIRequest:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        if base == quote:
            raise APIException(f'Нельзя конвертировать валюту "{base}" саму в себя...')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту "{base}"')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту "{quote}"')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Количество "{amount}" должно быть числом')

        if amount <= 0:
            raise APIException(f'Количество должно быть больше нуля!')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base_ticker}&tsyms={quote_ticker}')
        result = round(float(json.loads(r.content)[keys[quote]]) * amount, 2)

        return result
