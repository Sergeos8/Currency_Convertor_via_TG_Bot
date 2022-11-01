import requests
import json
from config import keys


class APIException(Exception):
    pass


class Converter:
    @staticmethod
    def get_price(base, quote, amount):
        try:
            base = keys[base.lower()]
        except KeyError:
            raise APIException(f"Указанная валюта {base} отсутствует в перечне!")
        try:
            quote = keys[quote.lower()]
        except KeyError:
            raise APIException(f"Указанная валюта {quote} отсутствует в перечне!")
        if base == quote:
            raise APIException(f'Указаны одинаковые валюты. Пересчет валюты {base} невозможен !')
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать указанное количество входных параметров.\n'
                               f'Просим обратится за помощью к инструкции по команде /helps!')
        r = requests.get(f"https://currate.ru/api/?get=rates&pairs={base}{quote}&key=b07450cc927b8e14634db33693d34fa7")
        print(r.content)
        resp = json.loads(r.content)
        new_price = float(resp['data'][base+quote]) * amount
        new_price = round(new_price, 2)
        message = f"Сумма {amount} {base} составляет: {new_price} {quote}"
        return message
