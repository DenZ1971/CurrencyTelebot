import json
import requests
from config import keys, KEY


class ConvercionExeption(Exception):
    pass

class ValueConverter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        if quote == base:
            raise ConvercionExeption(f'Не возможно перевести одинаковые валюты {base}')
        try:
            quote_ticker = keys[quote.lower()]
        except KeyError:
            raise ConvercionExeption(f'Не удалось обработать валюту {quote}')

        try:
            base_ticker = keys[base.lower()]
        except KeyError:
            raise ConvercionExeption(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvercionExeption(f'Не удалось обработать количество {amount}')

        r = requests.get(f'https://currate.ru/api/?get=rates&pairs={quote_ticker}{base_ticker}&key={KEY}')
        total_base = json.loads(r.content)['data'][f'{quote_ticker}{base_ticker}']

        return total_base