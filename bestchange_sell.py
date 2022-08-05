import os
os.environ["OMP_NUM_THREADS"] = "1"
import pandas as pd
import numpy
import urllib.request
import zipfile
from sqlalchemy import create_engine
from table import db


def bestchange_s():
    zip = 'info.zip'
    url = 'http://api.bestchange.ru/info.zip'
    urllib.request.urlretrieve(url, zip)
    with zipfile.ZipFile(zip, 'r' ) as zip_file:
        zip_file.extract('bm_rates.dat', '.')
        
    columns = ['ID отдаваемой валюты', 'ID получаемой валюты', 'ID обменного пункта', 'Курс обмена (отдать)',
               'Курс обмена (получить)', 'Резерв получаемой валюты', 'Отзывы', 'Не используется',
                'Минимальная сумма обмена', 'Максимальная сумма обмена', 'ID города (для направлений с наличными)']
    
    data = pd.read_csv('bm_rates.dat', encoding='Windows-1251', header=None, sep=";", names=columns)
    df = pd.DataFrame(data)
    
    df = df[
        (df['ID отдаваемой валюты'] == 52) | (df['ID отдаваемой валюты'] == 42) | (df['ID отдаваемой валюты'] == 63) | (
                df['ID отдаваемой валюты'] == 105)]
    
    df.loc[(df['ID отдаваемой валюты'] == 52), 'ID отдаваемой валюты'] = 'Alfa-bank'
    df.loc[(df['ID отдаваемой валюты'] == 42), 'ID отдаваемой валюты'] = 'Sberbank'
    df.loc[(df['ID отдаваемой валюты'] == 63), 'ID отдаваемой валюты'] = 'QIWI'
    df.loc[(df['ID отдаваемой валюты'] == 105), 'ID отдаваемой валюты'] = 'Tinkoff'
    
    df = df[
            (df['ID получаемой валюты'] == 93) | (df['ID получаемой валюты'] == 16) | (df['ID получаемой валюты'] == 206) |
            (df['ID получаемой валюты'] == 139) | (df['ID получаемой валюты'] == 99) | (df['ID получаемой валюты'] == 163) |
            (df['ID получаемой валюты'] == 32) | (df['ID получаемой валюты'] == 115) | (df['ID получаемой валюты'] == 140)
            | (df['ID получаемой валюты'] == 228) | (df['ID получаемой валюты'] == 203) | (df['ID получаемой валюты'] == 172)]
    
    df.loc[(df['ID получаемой валюты'] == 93), 'ID получаемой валюты'] = 'BTC'
    df.loc[(df['ID получаемой валюты'] == 16), 'ID получаемой валюты'] = 'BNB'
    df.loc[(df['ID получаемой валюты'] == 206), 'ID получаемой валюты'] = 'BUS'
    df.loc[(df['ID получаемой валюты'] == 139), 'ID получаемой валюты'] = 'ETH'
    df.loc[(df['ID получаемой валюты'] == 99), 'ID получаемой валюты'] = 'LTC'
    df.loc[(df['ID получаемой валюты'] == 163), 'ID получаемой валюты'] = 'USDT'
    df.loc[(df['ID получаемой валюты'] == 32), 'ID получаемой валюты'] = 'SHIB'
    df.loc[(df['ID получаемой валюты'] == 115), 'ID получаемой валюты'] = 'DOGE'
    df.loc[(df['ID получаемой валюты'] == 140), 'ID получаемой валюты'] = 'DUSH'
    df.loc[(df['ID получаемой валюты'] == 228), 'ID получаемой валюты'] = 'USDC'
    df.loc[(df['ID получаемой валюты'] == 203), 'ID получаемой валюты'] = 'DAI'
    df.loc[(df['ID получаемой валюты'] == 172), 'ID получаемой валюты'] = 'BCH'
    df["type"] = 'Продажа'
    df["exchange"] = 'bestchange'
    df.rename(columns={"ID получаемой валюты": "pairs"}, inplace=True)
    df.rename(columns={"Курс обмена (отдать)": "price"}, inplace=True)
    df.rename(columns={"Минимальная сумма обмена": "min"}, inplace=True)
    df.rename(columns={"Максимальная сумма обмена": "max"}, inplace=True)
    df.rename(columns={"ID отдаваемой валюты": "paytype"}, inplace=True)
    engine = create_engine("mysql://u1746962_default:e1q6SV5ueY94BRc7@localhost/u1746962_default?charset=utf8", encoding = 'utf-8')
    
    df = df[['type', 'exchange', 'pairs', 'price', 'min', 'max', 'paytype']]
    df.to_sql(name='p2p', con=engine, if_exists='append', index=False)
