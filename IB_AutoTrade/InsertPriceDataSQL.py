import pyodbc
import pypyodbc as odbc
import pandas as pd
import datetime
import pickle
import os


df = pd.read_csv('C:/Users/Toby/Desktop/tradedata.csv').tail(10)
df.drop(columns=['Unnamed: 0'],inplace=True)
print(df)

records = []
for n in df.iterrows():
    records.append(list(n[1]))

DRIVER = 'SQL Server'
SERVER_NAME = 'DESKTOP-F2PO6H3\SQLEXPRESS'
DATABASE_NAME = 'IBData'
TABLE_NAME = 'PriceData'

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
    IF NOT EXISTS (SELECT * FROM PriceData WHERE 
        SECTYPE = ? AND
        CURRENCY = ? AND
        SYMBOL = ? AND
        EXCHANGE = ? AND
        PRIME_EXCHANGE = ? AND
        FREQUENCY = ? AND
        DATE = ? AND
        TIME = ? AND
        OPEN_PRICE = ? AND
        HIGH_PRICE = ? AND
        LOW_PRICE = ? AND
        CLOSE_PRICE = ? AND
        DATE_TIME = ? AND
        RET = ? AND
        MA_3D = ? AND
        BB_UPPER = ? AND 
        BB_LOWER = ? AND
        LONG = ? AND
        SHORT = ?)
    BEGIN
        INSERT INTO PriceData
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    END 
"""
try:
    for record in records:
        # print(record)
        cursor.execute(insert_statement , record*2)       
except Exception as e:
    cursor.rollback()
    print(e.value)
    print('\nTransaction Rolled Back')
else:
    print('\nPrice Data Inserted Successfully')
    cursor.commit()
    cursor.close()
finally:
    if conn.connected == 1:
        print('\nConnection Closed')
        conn.close()

os.remove('C:/Users/Toby/Desktop/tradedata.csv')