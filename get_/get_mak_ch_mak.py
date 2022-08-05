from table import sql, db



def get_mak_ch_mak(money):
    crypto = 'BTC', 'BNB', 'BUSD', 'ETH', 'LTC', "USDT"
    sql.execute("SELECT * FROM p2p WHERE type = 'Покупка'")
    res = sql.fetchall()
    pairs = 'ETHBTC', 'LTCBTC', 'BNBBTC', 'BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'LTCUSDT', 'LTCBNB', 'BNBBUSD', 'BTCBUSD', 'ETHBUSD', 'LTCBUSD'



    for i in crypto:
        b = []
        for item in res:
            if item['pairs'] == i and float(item['max']) >= money:
                b.append(float(item['price']))

        for item in res:
            if float(item['price']) == max(b):
                sum = money / float(item['price'])
                break
        sql.execute("SELECT * FROM spot")
        res_spot = sql.fetchall()
        for p in pairs:
            get = 0
            sum_ = sum
            for depth in res_spot:
                if depth['pairs'] == p:
                    if i in depth['pairs'][-4:] and depth['type'] == 'Покупка':

                        sum1 = float(depth['price']) * float(depth['number'])
                        if sum_ >= sum1:
                            sum_ = sum_ - sum1
                            get = get + float(depth['number'])
                        else:
                            get += sum_ / float(depth['price'])
                            get_crypto = p.replace(i, "")
                            # print(f'{i}: {sum} -> {get_crypto} -> {get}')

                            sql.execute("SELECT * FROM p2p WHERE type = 'Продажа'")
                            res_sell = sql.fetchall()

                            b_sell = []
                            get_crypt = p.replace(i, "")
                            for item_sell in res_sell:
                                if item_sell['pairs'] == get_crypt and float(item_sell['max']) >= money:
                                    b_sell.append(float(item_sell['price']))

                            for item_sell in res_sell:
                                if float(item_sell['price']) == min(b_sell):
                                    sum1 = get * float(item_sell['price'])
                                    procent = ((sum1 - money) / money) * 100
                                    procent = float('{:.2f}'.format(procent))
                                    # print(
                                    #     f'1- {money}руб {item[1]}|{item[6]} -> {i}: {sum} -> {get_crypto}:{get} -> {sum1}руб')
                                    sql.execute(
                                        f"INSERT INTO makers_change_makers VALUES ('{money}' , '{item['exchange']}|{item['paytype']}', '{i}' , '{sum}', '{get_crypto}', '{get}', '{sum1}', '{item_sell['exchange']}|{item_sell['paytype']}','{procent}%')")
                                    db.commit()
                            break

                    elif i in depth['pairs'][:4] and depth['type'] == 'Продажа':
                        if sum_ >= float(depth['number']):
                            sum1 = float(depth['price']) * float(depth['number'])
                            get = get + sum1
                            sum_ = sum_ - float(depth['number'])

                        else:
                            get += sum_ * float(depth['price'])

                            get_crypto = p.replace(i, "")


                            sql.execute("SELECT * FROM p2p WHERE type = 'Продажа'")
                            res_sell = sql.fetchall()

                            b_sell = []
                            get_crypt = p.replace(i, "")
                            for item_sell in res_sell:
                                if item_sell['pairs'] == get_crypt and float(item_sell['max']) >= money * 4:
                                    b_sell.append(float(item_sell['price']))

                            for item_sell in res_sell:

                                if float(item_sell['price']) == min(b_sell):
                                    sum1 = get * float(item_sell['price'])
                                    procent = ((sum1 - money) / money) * 100
                                    procent = float('{:.2f}'.format(procent))
                                   
                                    # print(
                                    #     f'2- {money}руб {item[1]}|{item[6]} -> {i}: {sum} -> {get_crypto}:{get} -> {sum1}руб')
                                    sql.execute(
                                        f"INSERT INTO makers_change_makers VALUES ('{money}' , '{item['exchange']}|{item['paytype']}', '{i}' , '{sum}', '{get_crypto}', '{get}', '{sum1}', '{item_sell['exchange']}|{item_sell['paytype']}','{procent}%')")
                                    db.commit()
                            break
