from parse_data.bitzlato import bitzlato
from parse_data.garantex import gatrantex
from parse_data.binance_p2p import binance
from parse_data.binance_ import spot
from bestchange_sell import bestchange_s
from bestchange_buy import bestchange_b
from get_.get_mak_mak import get_mak_mak
from get_.get_tak_ch_mak import get_tak_ch_mak
from get_.get_mak_ch_mak import get_mak_ch_mak
from datetime import datetime
from table import sql, db
import os


def start():
    money = 100000
    sql.execute('DELETE FROM spot;', );
    print('delete spot')
    sql.execute('DELETE FROM p2p;', );
    print('delete p2p')
    sql.execute('DELETE FROM makers_change_makers;', );
    print('delete makers_change_makers')
    sql.execute('DELETE FROM takers_change_makers;', );
    print('delete takers_change_makers')
    sql.execute('DELETE FROM makers_makers;', );
    print('delete makers_makers')
    start_time = datetime.now()
    bestchange_s()
    bestchange_b()
    print(datetime.now() - start_time)
    start_time = datetime.now()
    spot()
    print(datetime.now() - start_time)
    start_time = datetime.now()
    binance()
    print(datetime.now() - start_time)
    start_time = datetime.now()
    bitzlato()
    print(datetime.now() - start_time)
    start_time = datetime.now()
    gatrantex()
    print(datetime.now() - start_time)
    db.commit()
    start_time = datetime.now()
    get_mak_mak(money)
    print(datetime.now() - start_time)
    start_time = datetime.now()
    get_tak_ch_mak(money)
    print(datetime.now() - start_time)
    start_time = datetime.now()
    get_mak_ch_mak(money)
    print(datetime.now() - start_time)

    db.commit()
    db.close()


if __name__ == '__main__':
    start()