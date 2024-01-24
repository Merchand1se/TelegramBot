import requests
import json
from config import currency

class ConvertionException(Exception):
    pass

class CryptoConverter:
    @staticmethod
    def get_price (quote: str, base: str, amount: str):
        if quote == base:
            raise ConvertionException(f'Нельзя конвертировать {currency[quote]} в {currency[base]}')

        try:
            quote_ticker = currency[quote]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {quote}')

        try:
            base_ticker = currency[base]
        except KeyError:
            raise ConvertionException(f'Не удалось обработаь валютю {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Не удалось обработать количество {amount}')
        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        mlp = json.loads(r.content)[currency[base]]
        total_base = mlp * amount
        return total_base

