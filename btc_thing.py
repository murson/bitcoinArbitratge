import urllib
import json
import ast
from pprint import pprint

lunoBidPrice = 0
lunoAskPrice = 0
lunoBidUSD = 0
lunoAskUSD = 0
zarusd = 0
coinbaseBidPrice = 0
coinbaseAskPrice = 0
lunoFees = 0
coinbaseFees = 0

def getLunoData():

    global lunoBidPrice
    global lunoAskPrice
    
    #Getting the Luno data
    luno = urllib.urlopen("https://api.mybitx.com/api/1/ticker?pair=XBTZAR")
    luno_dict = json.loads(luno.read())
    lunoBidPrice = float(luno_dict['bid'])
    lunoAskPrice = float(luno_dict['ask'])

def getForexData():
    global zarusd
    
    #Getting the exchange rate data    
    zarusd_string = urllib.urlopen("https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=USD&to_currency=ZAR&apikey=9EMJICPXUQ6Q8D9H")
    zarusd_data = json.loads(zarusd_string.read())
    zarusd_dict = zarusd_data['Realtime Currency Exchange Rate']#resolves the dictionary within dictionary problem
    zarusd = float(zarusd_dict['5. Exchange Rate'])

def getCoinbaseData():#clunky but it works
    global coinbaseAskPrice
    global coinbaseBidPrice  

    coinbase_string = urllib.urlopen("https://api.coinbase.com/v2/prices/BTC-USD/buy")
    coinbase_data = json.loads(coinbase_string.read())['data']
    coinbaseAskPrice = float(coinbase_data['amount'])
    coinbase_string = urllib.urlopen("https://api.coinbase.com/v2/prices/BTC-USD/sell")
    coinbase_data = json.loads(coinbase_string.read())['data']
    coinbaseBidPrice = float(coinbase_data['amount'])

    
def convertLuno():
    #1. Calculate Luno prices in USD
    global lunoBidUSD
    global lunoAskUSD

    lunoBidUSD = round(lunoBidPrice/zarusd,2)
    lunoAskUSD = round(lunoAskPrice/zarusd,2)

def calcArb():

    global lunoFees
    global coinbaseFees
    
    #1. Determine whether or not there is an arbitrage opportunity
    
    if lunoAskUSD < lunoBidUSD:
        print("Luno she is broken")

    if coinbaseAskPrice < coinbaseBidPrice:
        print("Coinbase she is broken")

    if coinbaseAskPrice < lunoBidUSD:
        print("Buy from Coinbase, sell on Luno")
        dallazBuy = float(raw_input("\nHow muts dalla$$$ u 1 2 sp3nd? "))
        
        BTCpurch = dallazBuy/coinbaseAskPrice
        BTCproceeds = BTCpurch*lunoBidUSD/coinbaseAskPrice

        dallazSell = dallazBuy*lunoBidUSD/coinbaseAskPrice
        
        feeCalc(dallazSell,dallazBuy)

        profitUSD = dallazSell-dallazBuy-lunoFees-coinbaseFees

        print("\nResults of trading strategy:\n=============================")
        print("Investment amount (USD)\t\t\t"+str(-dallazBuy))
        print("Proceeds amount (USD)\t\t\t"+str(round(dallazSell,2)))
        print("Fees: Luno (USD)\t\t\t"+str(round(-lunoFees,2)))
        print("Fees: Coinbase (USD)\t\t\t"+str(round(-coinbaseFees,0)))
        print("Profit on trading strategy (USD)\t"+str(round(profitUSD,2)))
        print("Return on investment (%)\t\t"+str(round(profitUSD/dallazBuy*100,2)))

        if profitUSD<0:
            print("Don't do it, son!")
            again = raw_input("Type, 'yas' to try again")
                          
            if again=="yas":
                printTheThings()
                calcArb()          
            else:
                print()

        else:
            print("Hell yeaz")
            again = raw_input("Type, 'yas' to try again ")
                          
            if again=="yas":
                printTheThings()
                calcArb()          
            else:
                print()
        

    if lunoAskUSD < coinbaseBidPrice:
        
        print("Buy from Luno, sell on Coinbase")

    
def feeCalc(qL,qCB):
    #fee schedule
    global lunoFees
    global coinbaseFees
    
    coinbaseRate = 0.01
    coinbaseMin = 1
    lunoRate = 0.01

    if qCB < 100:
        lunoFees = qL*lunoRate
        coinbaseFees = 1

    else:
        lunoFees = qL*lunoRate
        coinbaseFees = qCB*coinbaseRate  
    
def printTheThings():

    lunoZARSpread = (lunoAskPrice-lunoBidPrice)/lunoBidPrice
    lunoUSDSpread = (lunoAskUSD-lunoBidUSD)/lunoBidUSD
    coinbaseSpread = (coinbaseAskPrice-coinbaseBidPrice)/coinbaseBidPrice
    
    print("\t\t\tBid Price\tAsk Price\tSpread")
    print("\t\t\t=========\t=========\t======")
    print("Luno (ZAR)\t\t"+str(lunoBidPrice)+"\t"+str(lunoAskPrice)+"\t"+str(round(lunoZARSpread,2)))
    print("Luno (USD)\t\t"+str(lunoBidUSD)+"\t\t"+str(lunoAskUSD)+"\t\t"+str(round(lunoUSDSpread,2)))
    print("Coinbase (USD)\t\t"+str(coinbaseBidPrice)+"\t\t"+str(coinbaseAskPrice)+"\t\t"+str(round(coinbaseSpread,2)))


getLunoData()
getForexData()
getCoinbaseData()
convertLuno()
printTheThings()
calcArb()







