import pandas as pd
import numpy as np
import time
from IBWrapper import IBWrapper, contract
from ib.ext.EClientSocket import EClientSocket
import pickle
import os
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

with open("account_data.txt", "rb") as fp:
	Account_Params = pickle.load(fp)

accountName = Account_Params[0]
port = Account_Params[1]
clientId = Account_Params[2]
os.remove("account_data.txt")

accountName = accountName
callback = IBWrapper()             # Instantiate IBWrapper. callback
tws = EClientSocket(callback)      # Instantiate EClientSocket and return data to callback
host = ""
port = port   # It is for default port no. in demo account
clientId = clientId
tws.eConnect(host, port, clientId) # connect to TWS
create = contract()                # Instantiate contract class
callback.initiate_variables()

# Account Summary
tws.reqAccountUpdates(1, accountName)
time.sleep(2)
accvalue = pd.DataFrame(callback.update_AccountValue, columns = ['key', 'value', 'currency', 'accountName']) #[:199]
Portfolio = pd.DataFrame(callback.update_Portfolio, columns=['Contract ID','Currency', 'Expiry','Include Expired','Local Symbol','Multiplier','Primary Exchange','Right',
                                'Security Type','Strike','Symbol','Trading Class','Position','Market Price','Market Value',
                                'Average Cost', 'Unrealised PnL', 'Realised PnL', 'Account Name'])
Portfolio = Portfolio[Portfolio['Position']!=0]
callback.update_AccountTime

# Position Summary
tws.reqPositions()
time.sleep(2)
Position_Summary = pd.DataFrame(callback.update_Position, 
               columns=['Account','Contract ID','Currency','Exchange','Expiry',
                        'Include Expired','Local Symbol','Multiplier','Right',
                        'Security Type','Strike','Symbol','Trading Class',
                        'Position','Average Cost'])
Position_Summary[Position_Summary["Account"] == accountName]
Position_Summary = Position_Summary[Position_Summary['Position']!=0]

# Open Orders
tws.reqAllOpenOrders()
time.sleep(2)
openstat = pd.DataFrame(callback.order_Status,columns=['orderId', 'status', 'filled', 'remaining',
                                                       'avgFillPrice','permId', 'parentId',
                                                       'lastFillPrice', 'clientId', 'whyHeld'])

# Open Orders
tws.reqAllOpenOrders()
time.sleep(2)
openorder = pd.DataFrame(callback.open_Order,columns=['orderId', 'contract', 'order', 'orderState'])

# Account Summary - ALL AVAILABLE ACCOUNT DATA
# print("\n\nAccountValue: \n" + str(accvalue))

Headings = ['Portfolio', 'Position Summary', 'Open Status', 'Open Order']
Frames = (Portfolio, Position_Summary, openstat, openorder)

for h, f in zip(Headings, Frames):
	if f.empty:
		pass
	else:
		print('\n'+h+': \n'+str(f)+'\n')
		
Position_Summary.to_csv('Position_Summary.csv')
Portfolio.to_csv('Portfolio.csv')
openstat.to_csv('openstat.csv')
openorder.to_csv('openorder.csv')
accvalue.to_csv('accvalue.csv')

