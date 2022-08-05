import pymysql

db = pymysql.connect(
    host = 'localhost',
    port = 3306,
    user = 'u1746962_default',
    password = 'e1q6SV5ueY94BRc7',
    database = 'u1746962_default',
    cursorclass = pymysql.cursors.DictCursor)
print('successfully connected')
print('#' * 20)
    
sql = db.cursor()


