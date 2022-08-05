from table import sql, db


def get_mak_mak(money):
    crypto = 'BTC', 'BNB', 'BUSD', 'ETH', 'LTC', "USDT"

    sql.execute("SELECT * FROM p2p WHERE type = 'Покупка'")
    res = sql.fetchall()
    for i in crypto:
        b = []
        for item in res:
            if item['pairs'] == i and float(item['max']) >= money * 4:
                b.append(float(item['price']))

        for item in res:
            if float(item['price']) == max(b):
                sum = money / float(item['price'])

                break
        sql.execute("SELECT * FROM p2p WHERE type = 'Продажа'")
        res_sell = sql.fetchall()

        b_sell = []
        for item_sell in res_sell:
            if item_sell['pairs'] == i and float(item_sell['max']) >= money * 4:
                b_sell.append(float(item_sell['price']))

        for item_sell in res_sell:

            if float(item_sell['price']) == min(b_sell):
                sum1 = sum * float(item_sell['price'])
                procent = ((sum1 - money) / money) * 100
                procent = float('{:.2f}'.format(procent))
                                   
                # print(
                #     f' {money}руб {item[1]}|{item[6]} -> {i}: {sum} -> {i}:{sum} -> {sum1}руб')
                sql.execute(
                    f"INSERT INTO makers_makers VALUES ('{money}' , '{item['exchange']}|{item['paytype']}', '{i}' , '{sum}', '{sum1}', '{item_sell['exchange']}|{item_sell['paytype']}','{procent}%')")
                db.commit()
                break
