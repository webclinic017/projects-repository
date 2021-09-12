import pickle
import os
import pandas as pd
import time
import importlib
import sys

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


global Position_Summary
global Portfolio

def gatherSymbols():
	Path = (str(os.path)+str('/'))
	with open("port_monitor.txt", "rb") as fp:
		securities = pickle.load(fp)
	symbols = securities[0]
	return symbols

def gatherSecTypes():
	Path = (str(os.path)+str('/'))
	with open("port_monitor.txt", "rb") as fp:
		securities = pickle.load(fp)
	secTypes = securities[1]
	return secTypes

def gatherExchanges():
	Path = (str(os.path)+str('/'))
	with open("port_monitor.txt", "rb") as fp:
		securities = pickle.load(fp)
	Exchanges = securities[2]
	return Exchanges

def gatherCurrencies():
	Path = (str(os.path)+str('/'))
	with open("port_monitor.txt", "rb") as fp:
		securities = pickle.load(fp)
	Currencies = securities[3]
	return Currencies





def Signal(symbol, secType, exchange, primeExchange, currency, frequency, backtestlength, accountName, port, clientId, plot):
	global genSignal
	Path = (str(os.path)+str('/'))
	Trade_Monitor = [symbol, secType, exchange, primeExchange, currency, frequency, backtestlength, accountName, port, clientId, plot]
	with open("trade_monitor.txt", "wb") as tm:
		pickle.dump(Trade_Monitor, tm)

	if 'genSignal' not in sys.modules:
		import genSignal
	else:
		importlib.reload(genSignal)





def tradeOrder(Signal, orderType, totalQuantity, lmtPrice, symbol, secType, exchange, primeExchange, currency):
	global Execute_Trade
	# 2. Store Parameters in Variable
	Path = (str(os.path)+str('/'))
	Trade_Params = [Signal, orderType, totalQuantity, lmtPrice, symbol, secType, exchange, primeExchange, currency]
	Account_Params = [accountName, port, clientId]
	# 3. Assign Variable to Text file to be read by Execute_Trade
	with open("trade_data.txt", "wb") as td:
		pickle.dump(Trade_Params, td)
	with open("account_data.txt", "wb") as ad:
		pickle.dump(Account_Params, ad)
	# 4. Print Parameters in Terminal

	if 'Execute_Trade' not in sys.modules:
		import Execute_Trade
	else:
		importlib.reload(Execute_Trade)






def readPositions(accountName, port, clientId):
	global Read_Positions
	# 5. Run Execute_Trade Script & Return Positions from IBAPI
	Account_Params = [accountName, port, clientId]
	with open("account_data.txt", "wb") as ad:
		pickle.dump(Account_Params, ad)

	if 'Read_Positions' not in sys.modules:
		import Read_Positions
	else:
		importlib.reload(Read_Positions)







def insertDataSQL(Signal, orderType, totalQuantity, lmtPrice, symbol, secType, exchange, primeExchange, currency):
	global insertData
	Path = (str(os.path)+str('/'))
	Trade_Params = [Signal, orderType, totalQuantity, lmtPrice, symbol, secType, exchange, primeExchange, currency]
	with open("trade_data.txt", "wb") as tp:
		pickle.dump(Trade_Params, tp)

	if 'insertData' not in sys.modules:
		import insertData
	else:
		importlib.reload(insertData)


def insertPriceDataSQL():
	import InsertPriceDataSQL









symbol  = gatherSymbols()
secType  = gatherSecTypes()
exchange  = gatherExchanges()
currency = gatherCurrencies()
os.remove("port_monitor.txt")

# Input Parameters
orderType = 'MKT'
totalQuantity = 35000
lmtPrice = 0
primeExchange = 'SMART'
pos_exposure = 0.02

# Plot == 1 else 0
plot = 0

print('\n Monitoring: '+symbol+' '+currency+' '+secType+'\n')

# OR frequency = 'day'
frequency = 'hour'
# OR frequency = 'min'
backtestlength = '1 Y'

# 1b. Set Account Parameters - PLEASE SET YOUR IB ACCOUNT PARAMETERS HERE
accountName = ""
port = 
clientId = 

Signal(symbol, secType, exchange, primeExchange, currency, frequency, backtestlength, accountName, port, clientId, plot)
readPositions(accountName, port, clientId)

Portfolio = pd.read_csv('Portfolio.csv')
Position_Summary = pd.read_csv('Position_Summary.csv')
Open_Status = pd.read_csv('openstat.csv')
Open_Order = pd.read_csv('openorder.csv')
accvalue = pd.read_csv('accvalue.csv')
tradedata = pd.read_csv('tradedata.csv')

# Calculated Quantity
portval = accvalue[accvalue['key']=='AvailableFunds']['value'].values[0]
pos_cost = float(portval)*pos_exposure
lastprice = tradedata['Close'].iloc[-1]
totalQuantity = abs(round(pos_cost/lastprice))



try:

	try:
		with open("trade_order.txt", "rb") as to:
			trade_order = pickle.load(to)
		Time = trade_order[0]
		Signal = trade_order[1]
		os.remove("trade_order.txt")

		print('\nQuantity: '+str(totalQuantity)+' - '+Signal+'\n')

		try:
			tQ2 = list(Portfolio[Portfolio['Symbol']==symbol]['Position'])[0]
			print(tQ2)
		except:
			tQ2 = 0
			print('Portfolio is empty')



		
		# SHORTS #
		if (tQ2 > 0) & (Signal == 'SELL'):
			try:
				print('Closing Long Position')
				tradeOrder(Signal, orderType, abs(tQ2), lmtPrice, symbol, secType, exchange, primeExchange, currency)
				insertDataSQL(Signal, orderType, abs(tQ2), lmtPrice, symbol, secType, exchange, primeExchange, currency)
			except:
				print('\nTrade Failed to Excute!')
				insertDataSQL(Signal, orderType, abs(tQ2), lmtPrice, symbol, secType, exchange, primeExchange, currency)

		elif (tQ2 < 0) & (Signal == 'SELL'):
			print('Skipping. Portfolio Already Holds Short Position')	






		# LONGS #
		elif (tQ2 < 0) & (Signal == 'BUY'):
			try:
				print('Closing Short Position')
				tradeOrder(Signal, orderType, abs(tQ2), lmtPrice, symbol, secType, exchange, primeExchange, currency)
				insertDataSQL(Signal, orderType, abs(tQ2), lmtPrice, symbol, secType, exchange, primeExchange, currency)
			except:
				print('\nTrade Failed to Excute!')
				insertDataSQL(Signal, orderType, abs(tQ2), lmtPrice, symbol, secType, exchange, primeExchange, currency)						

		elif (tQ2 > 0) & (Signal == 'BUY'):
			print('Skipping. Portfolio Already Holds Long Position')	






		else:
			print('Opening Trade Position')
			tradeOrder(Signal, orderType, totalQuantity, lmtPrice, symbol, secType, exchange, primeExchange, currency)
			insertDataSQL(Signal, orderType, totalQuantity, lmtPrice, symbol, secType, exchange, primeExchange, currency)								

	except:
		print('\nNo Trade Opportunity Detected!\n')

except KeyboardInterrupt:
	print('Interrupted')
	sys.exit(0)

totalQuantity = 0
insertPriceDataSQL()
