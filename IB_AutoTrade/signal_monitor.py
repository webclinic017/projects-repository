import pyodbc
import pypyodbc as odbc
import pandas as pd
import datetime
import pickle
import os
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

records = ['CBA','ANZ','NCM']


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


Longs = []
Shorts = []
Time = []


call_statement = f"""SELECT * FROM PriceData ORDER BY PriceData.SYMBOL, PriceData.DATE_TIME ASC"""

try:
    df = pd.read_sql(call_statement, conn)
except Exception as e:
    cursor.rollback()
    print(e.value)
    print('selection failed')
if conn.connected == 1:
    print('connection closed')
    conn.close()

records = list(df['symbol'].unique())

for r in range(0,len(records)):

    df1 = df[df['symbol']==records[r]]
    for n in range(1,2):
        Longs.append((df1['close_price'].iloc[-n] / df1['bb_upper'].iloc[-n] - 1)*100)
        Shorts.append((df1['close_price'].iloc[-n] / df1['bb_lower'].iloc[-n] - 1)*100)
        Time.append(df1['date_time'].iloc[-n])
monitor = pd.DataFrame.from_dict({'Date_Time':Time,'Ticker':records,'Long_Signal':Longs,'Short_Signal':Shorts})

monitor['LTrade'] = monitor['Long_Signal'] > 0
monitor['STrade'] = monitor['Short_Signal'] < 0

Longs = monitor[(monitor['LTrade'] == True)].sort_values(by='Long_Signal',ascending=False).reset_index(drop=True).drop(columns=['STrade','Short_Signal'])
Shorts = monitor[(monitor['STrade'] == True)].sort_values(by='Short_Signal',ascending=True).reset_index(drop=True).drop(columns=['LTrade','Long_Signal'])

print(monitor)
print('\n')
print(Longs)
print('\n')
print(Shorts)


Longs.to_csv('Longs.csv')
Shorts.to_csv('Shorts.csv')
    