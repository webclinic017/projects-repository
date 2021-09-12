import pyodbc
import pypyodbc as odbc
import pandas as pd
import datetime
import pickle
import os

with open("trade_data.txt", "rb") as fp:
	Trade_Params = pickle.load(fp)

action = Trade_Params[0]
orderType = Trade_Params[1]
totalQuantity = Trade_Params [2]
lmtPrice = Trade_Params[3]
symbol = Trade_Params[4]
secType = Trade_Params[5]
exchange = Trade_Params[6]
prime_exchange = Trade_Params[7]
currency = Trade_Params[8]
os.remove("trade_data.txt")


dict = {'DATETIME':str(datetime.datetime.now()),
		'ACTION':action,
		'TYPE':orderType,
		'QUANTITY':totalQuantity,
		'LMT_PRICE':lmtPrice,
		'SYMBOL':symbol,
		'SECTYPE':secType,
		'EXCHANGE':exchange,
		'PRIME_EXCHANGE':prime_exchange,
		'CURRENCY':currency}

df = pd.DataFrame.from_dict(dict, orient = 'index').transpose()


records = []
for n in df.iterrows():
    records.append(list(n[1]))

DRIVER = 'SQL Server'
SERVER_NAME = 'DESKTOP-F2PO6H3\SQLEXPRESS'
DATABASE_NAME = 'IBData'
TABLE_NAME = 'OrderData'

conn_string = f"""
    Driver={{{DRIVER}}};
    Server={SERVER_NAME};
    Database={DATABASE_NAME};
    Trust_Connection=yes;
"""

try:
    conn = odbc.connect(conn_string)
except Exception as e:
    print(e)
    print('task is terminated')
    sys.exit()
else:
    cursor = conn.cursor()

insert_statement = f"""
    IF NOT EXISTS (SELECT * FROM OrderData WHERE 
        DATETIME = ? AND
        ACTION = ? AND
        TYPE = ? AND
        QUANTITY = ? AND
        LMT_PRICE = ? AND
        SYMBOL = ? AND
        SECTYPE = ? AND
        EXCHANGE = ? AND
        PRIME_EXCHANGE = ? AND
        CURRENCY = ?)
    BEGIN
        INSERT INTO OrderData
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    END 
"""
try:
    for record in records:
        # print(record)
        cursor.execute(insert_statement, record*2)        
except Exception as e:
    cursor.rollback()
    print(e.value)
    print('\nTransaction Rolled Back')
else:
    print('\nTrade Order Inserted Successfully')
    cursor.commit()
    cursor.close()
finally:
    if conn.connected == 1:
        print('\nConnection Closed')
        conn.close()