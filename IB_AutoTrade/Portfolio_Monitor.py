import pickle
import time
import importlib
import sys
import gc

# Define security tickers list
secs = ['NCM']

# Begin iteration 
for n in range(0,len(secs)):
	
	# Print ticker name and index 
	print(str(n)+': '+str(secs[n]))

	# If text file exists, delete
	try:
		os.remove("port_monitor.txt")
	except:
		pass

	# Create List with security attributes to append to 'port_monitor.txt'
	trade = []
	trade.append(secs[n])
	trade.append('STK')
	trade.append('SMART')
	trade.append('AUD')

	# Populate text file with trade list
	with open("port_monitor.txt", "wb") as pm:
		pickle.dump(trade, pm)
	
	# This logic works.
	if 'AutoTrade' not in sys.modules:
		import AutoTrade
	else:
		importlib.reload(AutoTrade)
	gc.collect()

