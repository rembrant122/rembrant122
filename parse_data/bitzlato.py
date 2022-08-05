from jose import jwt
from jose.constants import ALGORITHMS
import datetime
import random
import time
import requests
from table import sql, db


def bitzlato():
    r = 'ETH', "BTC", "BCH", 'LTC', "DASH", "DOGE", "USDT", "USDC", "DAI", "MCR", "MDT"
    c = 'selling', 'purchase'
    for tp in c:
        for item in r:
            kid = '1'
            key = {"kty": "EC", "alg": "ES256", "crv": "P-256", "x": "GgbDdmPqJC-GzXS4l8a3rvCzyG1vYwKQLxUx40sqK5E",
                   "y": "JyHDPCxczxEZlgu2PPQ2Vru-94-1qOkUuxx7CxQqF9k",
                   "d": "uXpwV7jidGlcdcGJUsNVCI8qaA9MU7K4-nmq4m0LBk8"}
            dt = datetime.datetime.now()
            ts = time.mktime(dt.timetuple())
            claims = {
                "email": 'fert1k@icloud.com',
                "aud": "usr",
                "iat": int(ts),
                "jti": hex(random.getrandbits(64))
            }
            token = jwt.encode(claims, key, algorithm=ALGORITHMS.ES256)

            type = tp
            crypto = item
            currency = 'RUB'
            a = requests.get('https://bitzlato.com/api/p2p/exchange/dsa/', headers={
                "Authorization": "Bearer " + token},
                             params={
                                 'type': f'{type}',
                                 'cryptocurrency': {crypto},
                                 'currency': {currency},
                                 "limit": '99999',
                                 "pay_method": '',
                             }).json()

            for item in a['data']:
                if any([(item['paymethod']['name'] == "QIWI"), (item['paymethod']['name'] == "Raiffeisenbank"),
                        (item['paymethod']['name'] == "Alfa-bank"), (item['paymethod']['name'] == "Tinkoff"),
                        (item['paymethod']['name'] == "Sberbank")]):

                    if tp == 'selling':
                        cryptocurrency = item['cryptocurrency']
                        currency = item['currency']
                        rate = item['rate']
                        min = item['limitCurrency']['min']
                        max = item['limitCurrency']['max']
                        paymethod = item['paymethod']['name']
                        # print(f'Продажа | Bitzlato | {paymethod} | {cryptocurrency}{currency} | {rate} | {min} - {max}')
                        sql.execute(f"INSERT INTO p2p VALUES ('Покупка' , 'Bitzlato' , '{cryptocurrency}' , '{rate}', '{min}', '{max}', '{paymethod}')")
                    else:
                        cryptocurrency = item['cryptocurrency']
                        currency = item['currency']
                        rate = item['rate']
                        min = item['limitCurrency']['min']
                        max = item['limitCurrency']['max']
                        paymethod = item['paymethod']['name']
                        # print(f'Покупка | Bitzlato | {paymethod} | {cryptocurrency}{currency} | {rate} | {min} - {max}')

                        sql.execute(f"INSERT INTO p2p VALUES ('Продажа' , 'Bitzlato' , '{cryptocurrency}' , '{rate}', '{min}', '{max}', '{paymethod}')")