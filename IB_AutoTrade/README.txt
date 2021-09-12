This project was completed to automate signal generation, monitoring and execution of trade positions using the Interactive Brokers TradersWorkStation (TWS) API. 

In it's current form, the projects calls on 6 scripts:

  Portfolio_Monitor.py - The highest level script designed to set the security parameters to be monitored. This script will call AutoTrade.py after parameter specification.

  AutoTrade.py - This script provides the core functionality for the program. This script will call price data collection and signal calculation, account data, trade sizing, and trade order execution scripts based on signal event. Ensure that unique account parameters are specified here.

  genSignal.py - This script provides the data collection functionality to extract security price data and overlay a moving average indictor. The outputs from this script provide trade signal to determine when to long or short the security.
  
  Read_Positions.py - This script calls trade account data including open orders, account value, portfolio positions. The outputs of this script are used in the event of closure of position. The amount of securites held must be read from the account and incorporated in trade execution script.
  
  Execute_Trade.py - This script executes trade orders, incorporating all previously specified account, trade sizing and security parameters.
  
  insertData.py - This script is event driven following execution of trade order. This script inserts trade order data to SQL table for future review.
  
  

