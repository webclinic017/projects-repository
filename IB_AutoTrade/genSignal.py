import scipy.stats as statistics
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import warnings
from matplotlib.pyplot import figure
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.common import BarData
import datetime
import sys, pprint
import pickle
import os
import gc
import time 

sns.set()
warnings.filterwarnings("ignore")
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


print('\nGathering Data\n')

# Gather Minute Data
data = {'Date':[],'Open':[],'High':[],'Low':[],'Close':[]}
d1 = []


global symbol
global secType
global exchange
global currency
global frequency
global accountName
global port
global clientId

with open("trade_monitor.txt", "rb") as fp:
	Trade_Monitor = pickle.load(fp)

symbol = Trade_Monitor[0]
secType = Trade_Monitor[1]
exchange = Trade_Monitor[2]
prime_exchange = Trade_Monitor[3]
currency = Trade_Monitor[4]
frequency = Trade_Monitor[5]
backtestlength = Trade_Monitor[6]
accountName = Trade_Monitor[7]
port = Trade_Monitor[8]
clientId = Trade_Monitor[9]
plot = Trade_Monitor[10]

print(Trade_Monitor)

os.remove("trade_monitor.txt")

class MyWrapper(EWrapper):

    def nextValidId(self, orderId:int):
        #4 first message received is this one
        print("setting nextValidOrderId: %d", orderId)
        self.nextValidOrderId = orderId
        #5 start requests here
        self.start(secType, symbol, currency, exchange, prime_exchange)

    def historicalData(self, reqId:int, bar: BarData):
        #7 data is received for every bar
        d1.append(bar)
        data['Date'].append(str(d1).split(',')[0].split(': ')[2])
        data['Open'].append(str(d1).split(',')[1].split(': ')[1])
        data['High'].append(str(d1).split(',')[2].split(': ')[1])
        data['Low'].append(str(d1).split(',')[3].split(': ')[1])
        data['Close'].append(str(d1).split(',')[4].split(': ')[1])
        d1.clear()
        #print("HistoricalData. ReqId:", reqId, "BarData.", bar)

    def historicalDataEnd(self, reqId: int, start: str, end: str):
    	try:
	        #8 data is finished
	        print("HistoricalDataEnd. ReqId:", reqId, "from", start, "to", end)
	        #9 this is the logical end of your program
	        app.disconnect()
	        print("finished")
    	except Exception:
	    	pass

    def error(self, reqId, errorCode, errorString):
    	try:
        # these messages can come anytime.
        	print("Error. Id: " , reqId, " Code: " , errorCode , " Msg: " , errorString)
    	except Exception:
	    	pass

    def start(self, secType, symbol, currency, exchange, primexchange):
    	try:
	        queryTime = (datetime.datetime.today()).strftime("%Y%m%d %H:%M:%S")
	        fx = Contract()
	        fx.secType = secType 
	        fx.symbol = symbol
	        fx.currency = currency
	        fx.exchange = exchange
	        fx.primexchange = primexchange
	        #6 request data, using fx since I don't have Japanese data
	        app.reqHistoricalData(4102, fx, queryTime, backtestlength, "1 "+str(frequency), "MIDPOINT", 1, 1, False, [])
    	except Exception:
	    	pass


# if 'app' not in sys.modules:
# 	app = EClient(MyWrapper()) #1 create wrapper subclass and pass it to EClient
# 	app.connect("127.0.0.1", port, clientId=clientId) #2 connect to TWS/IBG
# 	app.run() #3 start message thread
# else:
# 	importlib.reload(genSignal)


app = EClient(MyWrapper()) #1 create wrapper subclass and pass it to EClient
app.connect("127.0.0.1", port, clientId=clientId) #2 connect to TWS/IBG
app.run() #3 start message thread

var = currency+'.'+symbol

# Collect last mintute of data
df = pd.DataFrame.from_dict(data)
print(df.tail(5))

year = df['Date'].str[0:4]
month = df['Date'].str[4:6]
day = df['Date'].str[6:8]
df['Time'] = df['Date'].str[10:15]

df['Date'] = day+'-'+month+'-'+year
df['DateTime'] = df['Date']+' - '+df['Time']
df['SecType'] = secType
df['Currency'] = currency
df['Symbol'] = symbol
df['Exchange'] = exchange
df['PrimeExchange'] = prime_exchange
df['Frequency'] = frequency

cols = ['SecType','Currency','Symbol','Exchange','PrimeExchange','Frequency','Date','Time','Open','High','Low','Close']
df = df.loc[:, cols]

# Set Variables
n = '3ma'
u = '3ba'
l = '3bbb'

if df['Frequency'][0] == 'hour':
    nn = 72
elif df['Frequency'][0] == 'min':
    nn = 4320    
elif df['Frequency'][0] == 'day':
    nn = 3

df['DateTime'] = df['Date'].astype(str) + ' - '+ df['Time'].astype(str) 
df['closeret'] = df['Close'].astype(float) / df['Close'].astype(float).shift(1) -1
df['closeret'] = df['closeret'].shift(1)

# Bollinger Bands & MA Calculation
df[n] = df['Close'].rolling(window=nn).mean()
df[u] = (df[n].rolling(window=nn).std())+df[n]
df[l] = df[n]-(df[n].rolling(window=nn).std())

# Go long and short if price above upper BB and 
df['Close'] = df['Close'].astype(float)
df['Long'] = df['Close'] > df[u]
df['Short'] = df['Close'] < df[l]



df.loc[df.Short == True, 'closeret'] = -df['closeret']

mean = (df.loc[(df['Long']==True) | (df['Short'] == True),['closeret']].mean().values[0])*100
se = (df.loc[(df['Long']==True) | (df['Short'] == True),['closeret']].sem().values[0])*100
tstat = mean / se
std = (df.loc[(df['Long']==True) | (df['Short'] == True),['closeret']].std().values[0])*100

# Show Plot
if plot == 1:
	sns.set()
	xvar = df['DateTime']

	# Plot Timeseries of Price, Trades & Signals
	figure(figsize=(15, 12), dpi=100)
	ax = plt.axes()
	ax.xaxis.set_major_locator(ticker.MultipleLocator(round(len(xvar)*1/7)))
	ax.fill_between(xvar, df['Close'], df[u], where=(df['Long']),
	                facecolor='orange', interpolate=True, label='Long')
	ax.fill_between(xvar, df['Close'], df[l], where=(df['Short']),
	                facecolor='purple', interpolate=True, label ='Short')
	plt.plot(xvar, df['Close'], color='black', label='Price')
	plt.plot(xvar, df[n], color='red', label=n, linewidth=0.8)
	plt.plot(xvar, df[u], color='blue', label='bb_upper', linewidth=0.8)
	plt.plot(xvar, df[l], color='green', label='bb_lower', linewidth=0.8)
	plt.title('Trade Monitor: '+symbol+' '+currency+' ('+secType+')\nHourly Data - '+str(n.upper())+' '+backtestlength+'\n'+'Longs: '+str(round(df[df['Long']==True]['closeret'].sum(),4))+'\n'+'Shorts: '+str(round(df[df['Short']==True]['closeret'].sum(),4))+'\nLMS Mean (daily ret): '+str(round(mean*6,4))+'%'+'   LMS Std (daily ret): '+str(round(std*6,4))+'%'+'   LMS Tstat: '+str(round(tstat,4)))
	plt.legend()
	plt.show()
else:
	pass


#Artificially Trigger Signal - For Testing
# df['Long'].iloc[-2] = False
# df['Long'].iloc[-1] = True

df.to_csv('C:/Users/Toby/Desktop/tradedata.csv')

print('\n')
print(df.tail(10))
print('\n')

# Signal Trigger
for n, o, t in zip(['Long','Short'], ['BUY','SELL'], ['SELL','BUY']):
	if (df[n].iloc[-1] != df[n].iloc[-2]) & (df[n].iloc[-1] == True):
		print(df.tail(2))
		print('\n'+n +' Opportunity Detected!')
		trade = [datetime.datetime.now(), o]
		with open("trade_order.txt", "wb") as to:
			pickle.dump(trade, to)

	elif (df[n].iloc[-1] != df[n].iloc[-2]) & (df[n].iloc[-1] == False):
		print(df.tail(2))
		print('\nClosing '+n+' Position')
		trade = [datetime.datetime.now(), t]
		with open("trade_order.txt", "wb") as to:
			pickle.dump(trade, to)
	else:
		pass

time.sleep(1)