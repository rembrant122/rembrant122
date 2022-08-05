
import os
os.environ["OMP_NUM_THREADS"] = "1"
import pandas as pd
import numpy
import urllib.request
import zipfile
from sqlalchemy import create_engine
from table import db


def bestchange_b():
    # zip = 'info.zip'
    # url = 'http://api.bestchange.ru/info.zip'
    # urllib.request.urlretrieve(url, zip)
    # with zipfile.ZipFile(zip, 'r') as zip_file:
    #     zip_file.extract('bm_rates.dat', '.')

    columns = ['ID отдаваемой валюты', 'ID получаемой валюты', 'ID обменного пункта', 'Курс обмена (отдать)',
               'Курс обмена (получить)', 'Резерв получаемой валюты', 'Отзывы', 'Не используется',
               'Минимальная сумма обмена', 'Максимальная сумма обмена', 'ID города (для направлений с наличными)']

    data = pd.read_csv('bm_rates.dat', encoding='Windows-1251', header=None, sep=";", names=columns)
    df = pd.DataFrame(data)

    df = df[
        (df['ID отдаваемой валюты'] == 93) | (df['ID отдаваемой валюты'] == 16) | (df['ID отдаваемой валюты'] == 206) |
        (df['ID отдаваемой валюты'] == 139) | (df['ID отдаваемой валюты'] == 99) | (df['ID отдаваемой валюты'] == 163) |
        (df['ID отдаваемой валюты'] == 32) | (df['ID отдаваемой валюты'] == 115) | (df['ID отдаваемой валюты'] == 140) |
        (df['ID отдаваемой валюты'] == 228) | (df['ID отдаваемой валюты'] == 203) | (df['ID отдаваемой валюты'] == 172)]

    df.loc[(df['ID отдаваемой валюты'] == 93), 'ID отдаваемой валюты'] = 'BTC'
    df.loc[(df['ID отдаваемой валюты'] == 16), 'ID отдаваемой валюты'] = 'BNB'
    df.loc[(df['ID отдаваемой валюты'] == 206), 'ID отдаваемой валюты'] = 'BUS'
    df.loc[(df['ID отдаваемой валюты'] == 139), 'ID отдаваемой валюты'] = 'ETH'
    df.loc[(df['ID отдаваемой валюты'] == 99), 'ID отдаваемой валюты'] = 'LTC'
    df.loc[(df['ID отдаваемой валюты'] == 163), 'ID отдаваемой валюты'] = 'USDT'
    df.loc[(df['ID отдаваемой валюты'] == 32), 'ID отдаваемой валюты'] = 'SHIB'
    df.loc[(df['ID отдаваемой валюты'] == 115), 'ID отдаваемой валюты'] = 'DOGE'
    df.loc[(df['ID отдаваемой валюты'] == 140), 'ID отдаваемой валюты'] = 'DUSH'
    df.loc[(df['ID отдаваемой валюты'] == 228), 'ID отдаваемой валюты'] = 'USDC'
    df.loc[(df['ID отдаваемой валюты'] == 203), 'ID отдаваемой валюты'] = 'DAI'
    df.loc[(df['ID отдаваемой валюты'] == 172), 'ID отдаваемой валюты'] = 'BCH'
    df = df[
        (df['ID получаемой валюты'] == 52) | (df['ID получаемой валюты'] == 42) | (df['ID получаемой валюты'] == 63) | (
                df['ID получаемой валюты'] == 105)]

    df.loc[(df['ID получаемой валюты'] == 52), 'ID получаемой валюты'] = 'Alfa-bank'
    df.loc[(df['ID получаемой валюты'] == 42), 'ID получаемой валюты'] = 'Sberbank'
    df.loc[(df['ID получаемой валюты'] == 63), 'ID получаемой валюты'] = 'QIWI'
    df.loc[(df['ID получаемой валюты'] == 105), 'ID получаемой валюты'] = 'Tinkoff'

    df["type"] = 'Покупка'
    df["exchange"] = 'bestchange'
    df.rename(columns={"ID отдаваемой валюты": "pairs"}, inplace=True)
    df.rename(columns={"Курс обмена (получить)": "price"}, inplace=True)
    df.rename(columns={"Минимальная сумма обмена": "min"}, inplace=True)
    df.rename(columns={"Максимальная сумма обмена": "max"}, inplace=True)
    df.rename(columns={"ID получаемой валюты": "paytype"}, inplace=True)
    
    engine = create_engine("mysql://u1746962_default:e1q6SV5ueY94BRc7@localhost/u1746962_default?charset=utf8", encoding = 'utf-8')

    df = df[['type', 'exchange', 'pairs', 'price', 'min', 'max', 'paytype']]
    df.to_sql(name='p2p', con=engine, if_exists='append', index=False)