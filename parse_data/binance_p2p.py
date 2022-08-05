import requests
from table import sql, db


def binance():
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Length": "123",
        "content-type": "application/json",
        "Host": "p2p.binance.com",
        "Origin": "https://p2p.binance.com",
        "Pragma": "no-cache",
        "TE": "Trailers",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0"
    }

    types = "BUY", "SELL"
    for tp in types:
        asset = 'USDT', 'BTC', 'BNB', 'BUSD', 'ETH', 'DAI', 'SHIB'

        for ass in asset:
            data = {
                "asset": f"{ass}",
                "fiat": "RUB",
                "merchantCheck": False,
                "page": 1,
                "publisherType": None,
                "rows": 20,
                "tradeType": f"{tp}",
                "transAmount": "1000"
            }

            r = requests.post('https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search', headers=headers,
                              json=data).json()

            for item in r['data']:
                trade_type = item['adv']['tradeType']
                asset = item['adv']['asset']
                fiatUnit = item['adv']['fiatUnit']
                price = item['adv']['price']
                aviable = item['adv']['surplusAmount']
                min = item['adv']['minSingleTransAmount']
                max = item['adv']['maxSingleTransAmount']

                for i in item['adv']['tradeMethods']:
                    payType = i['tradeMethodName']

                    if any([(i['tradeMethodName'] == "QIWI"), (i['tradeMethodName'] == "Raiffeisenbank"),
                            (i['tradeMethodName'] == "Alfa-bank"), (i['tradeMethodName'] == "Tinkoff"),
                            (i['tradeMethodName'] == "Sberbank")]):
                        if trade_type == "SELL":
                            # print(f'Про=дажа | Binance p2p | {asset}{fiatUnit} | {price} | {min} - {max}')
                            sql.execute(
                                f"INSERT INTO p2p VALUES ('Продажа' , 'Binance_ ', '{asset}' , '{price}', '{min}', '{max}', '{payType}')")
                        else:
                            # print(f'Покупка | Binance p2p | {asset}{fiatUnit} | {price} | {min} - {max}')
                            sql.execute(
                                f"INSERT INTO p2p VALUES ('Покупка' , 'Binance_ ', '{asset}' , '{price}', '{min}', '{max}', '{payType}')")
