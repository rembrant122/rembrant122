from binance.spot import Spot as Client
from table import sql, db

def spot():


    pairs = 'ETHBTC', 'LTCBTC', 'BNBBTC', 'BTCUSDT', 'ETHUSDT', 'TRXBTC', 'XRPBTC', 'BNBUSDT', 'LTCUSDT', 'LTCBNB', 'XRPUSDT', 'XRPBNB', 'TRXBNB', 'TRXUSDT', 'BNBBUSD', 'BTCBUSD', 'XRPBUSD', 'ETHBUSD', 'LTCBUSD', 'TRXBUSD'
    for item in pairs:
        pairs = item

        API_Key = '4ErWHOXdAlJF291hrGDzj09WRLotTl1p2SAJ4IkCHsPz4VsZXJ0wfaezVLmL8vWg'
        Secret_Key = '2ODQ8lh8S294CKKi4xPr3jslkktIlSI4NDThWT3xEv93Lh0Bi4JLQgi9Zlsiu3v2'

        client = Client(API_Key, Secret_Key, base_url='https://api1.binance.com', show_limit_usage=5000)

        response = client.depth(pairs )
      
        for a in response['bids']:
            # print(f'Покупка | Binance SPOT | {pairs} | {a}')
            sql.execute(f"INSERT INTO spot VALUES ('Продажа' , 'Binance SPOT' , '{pairs}' , '{a[0]}', '{a[1]}')")

        for a in response['asks']:
            # print(f'Продажа | Binance SPOT | {pairs} | {a}')
            sql.execute(f"INSERT INTO spot VALUES ('Покупка' , 'Binance SPOT' , '{pairs}' , '{a[0]}', '{a[1]}')")
