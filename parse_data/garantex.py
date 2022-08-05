import requests
from table import sql, db


def gatrantex():
    marker = "usdtrub", "btcrub", "dairub", "ethrub", "usdcrub",
    for item_m in marker:
        params = {
            "market": item_m
        }

        p2p_res = requests.get('https://garantex.io/api/v2/depth', params=params).json()

        for item in p2p_res['asks']:
            price = item['price']
            amount = item['amount']
            item_m = item_m.replace('rub','').upper()
            # print(f'Продажа | Garantex | {item_m} | {price} | {amount}')
            sql.execute(f"INSERT INTO p2p VALUES ('Продажа' , 'Garantex' , '{item_m}' , '{price}', '1', '{amount}', '-')")
    for item_m in marker:
        params = {
            "market": item_m
        }

        p2p_res = requests.get('https://garantex.io/api/v2/depth', params=params).json()

        for item in p2p_res['bids']:
            price = item['price']
            amount = item['amount']
            item_m = item_m.replace('rub', '').upper()
            # print(f'Покупка | Garantex | {item_m} | {price} | {amount}')
            sql.execute(f"INSERT INTO p2p VALUES ('Покупка' , 'Garantex' , '{item_m}' , '{price}', '1', '{amount}', '-')")
