from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import *
import os
import threading
import time
import pickle

global symbol
global secType
global exchange
global currency

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

print('\naction: '+str(action))
print('orderType: '+str(orderType))
print('totalQuantity: '+str(totalQuantity))
if orderType == 'LMT':
	print('lmtPrice: '+str(lmtPrice))
print('symbol: '+str(symbol))
print('secType: '+str(secType))
print('exchange: '+str(exchange))
print('primeExchange: '+str(prime_exchange))
print('currency: '+str(currency)+'\n')


class IBapi(EWrapper, EClient):
	def __init__(self):
		EClient.__init__(self, self)

	def nextValidId(self, orderId: int):
		super().nextValidId(orderId)
		self.nextorderId = orderId
		print('The next valid order id is: ', self.nextorderId)

	def orderStatus(self, orderId, status, filled, remaining, avgFullPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice):
		print('orderStatus - orderid:', orderId, 'status:', status, 'filled', filled, 'remaining', remaining, 'lastFillPrice', lastFillPrice)
	
	def openOrder(self, orderId, contract, order, orderState):
		print('openOrder id:', orderId, contract.symbol, contract.secType, '@', contract.exchange, ':', order.action, order.orderType, order.totalQuantity, orderState.status)

	def execDetails(self, reqId, contract, execution):
		print('Order Executed: ', reqId, contract.symbol, contract.secType, contract.currency, execution.execId, execution.orderId, execution.shares, execution.lastLiquidity)


def run_loop():
	app.run()

#Function to create FX Order contract
def FX_order(symbol, secType, exchange, currency):
	contract = Contract()
	contract.symbol = symbol
	contract.secType = secType
	contract.exchange = exchange
	contract.currency = currency
	return contract

app = IBapi()
app.connect('127.0.0.1', 7497, 100)

app.nextorderId = None

#Start the socket in a thread
api_thread = threading.Thread(target=run_loop, daemon=True)
api_thread.start()

#Check if the API is connected via orderid
while True:
	if isinstance(app.nextorderId, int):
		print('connected')
		break
	else:
		print('waiting for connection')
		time.sleep(1)

#Create order object
order = Order()
order.action = action
order.totalQuantity = totalQuantity
order.orderType = orderType

if order.orderType == 'LMT':
		order.lmtPrice = lmtPrice


#Place order
app.placeOrder(app.nextorderId, FX_order(symbol,secType,exchange,currency), order)
print('\n')

# app.orderStatus(app.status)

time.sleep(45)

#Cancel order 
# print('cancelling order')
app.cancelOrder(app.nextorderId)

# Finish
# time.sleep(3)
app.disconnect()

