import pandas as pd

trainingDataFolder = 'backtestingData'
initialWalletLiquidity = 100000

RED = '\033[31m'
GREEN = '\033[32m'
DEFAULT = '\033[0m'


class stockPurchaseDetails:
    def __init__(self) -> None:
        self.symbol = None
        self.volume = None
        self.stockPriceAtPurchase = None
        self.costOfPurchase = None
        self.purchaseDate = None

    def printPurchaseOrder(self) -> None:
        print()
        print(f'Stock Purchase Order:')
        print(f'\tSymbol → \t{self.symbol}')
        print(f'\tStock Price → \t${self.stockPriceAtPurchase.round(3)}')
        print(f'\tVolume →\t{self.volume}')
        print(f'\tTotal Cost → \t${self.costOfPurchase}')
        print(f'\tDate Bought → \t{self.purchaseDate}')
        print()


class Portfolio:
    def __init__(self) -> None:
        self.walletLiquidity = initialWalletLiquidity
        self.ownedStocks = []

    def buyStock(self,symbol,purchaseValue):
        
        stockDf = pd.read_csv(f'{trainingDataFolder}/{symbol.upper()}.csv')
        rowOfPurchase = stockDf.head(1)

        purchaseOrder = self.createPurchaseStockOrder(rowOfPurchase,purchaseValue)

        if purchaseOrder.costOfPurchase>self.walletLiquidity:
            print('Not Enough Wallet Liquidity')
            return 

        self.ownedStocks.append(purchaseOrder)
        self.walletLiquidity-=purchaseOrder.costOfPurchase


    def createPurchaseStockOrder(self,rowOfPurchase,value) -> stockPurchaseDetails:
        stockPurchaseOrder = stockPurchaseDetails()
        if len(rowOfPurchase) == 0:
            print('RowofPurchase: ',rowOfPurchase)
            quit()

        stockPurchaseOrder.stockPriceAtPurchase = rowOfPurchase['Close/Last'].values[0]
        stockPurchaseOrder.costOfPurchase = value
        stockPurchaseOrder.volume = value/stockPurchaseOrder.stockPriceAtPurchase
        stockPurchaseOrder.symbol = rowOfPurchase['symbol'].values[0]
        stockPurchaseOrder.purchaseDate = rowOfPurchase['Date'].values[0]

        return stockPurchaseOrder

    def checkWalletValue(self)->float:
        return self.walletLiquidity
    
    def printWalletValue(self) -> None:
        value = self.checkWalletValue()
        print(f'Current wallet Value → {value}') 

    def getCurrentValueOfStock(self,purchaseOrder):
        symbol = purchaseOrder.symbol
        curStockPrice = self.getCurrentSingleStockPrice(symbol)
        return curStockPrice*purchaseOrder.volume
    
    def getCurrentSingleStockPrice(self,symbol):
        stockdf = pd.read_csv(f'{trainingDataFolder}/{symbol.upper()}.csv')
        curStockPrice = stockdf.head(1)['Close/Last'].values[0]

        return curStockPrice

    def getPortfolioValue(self):
        value = 0
        for po in self.ownedStocks:
            currentStockVal = self.getCurrentValueOfStock(po)
            value+=currentStockVal
        
        return value
            

    def printPortfolio(self):
        if len(self.ownedStocks) == 0:
            print('Portfolio Currently Empty')
        for po in self.ownedStocks:
            po.printPurchaseOrder()

    def sellPurchaseOrder(self,po):
        currentStockValue = self.getCurrentSingleStockPrice(po.symbol)
        sellValue = po.volume*currentStockValue
        self.walletLiquidity+=sellValue

    def sellStock(self,symbol):
        if len(self.ownedStocks) == 0:
            print('No stocks to Sell')
            return 
        
        i = 0
        if symbol=='EVERYTHING':
            print('selling all stocks')
            for po in self.ownedStocks:
                self.sellPurchaseOrder(po)

            self.ownedStocks = []

        while i<len(self.ownedStocks):
            po = self.ownedStocks[i]
            if po.symbol == symbol.upper():
                self.sellPurchaseOrder(po)
                self.ownedStocks.pop(i)

            else:
                i+=1 

    def getTotalEarnings(self):
        return (self.walletLiquidity+self.getPortfolioValue())-initialWalletLiquidity
    
    def printTotalEarnings(self):
        earnings = self.getTotalEarnings()
        print(f'Total Earnings → ',end='')
        if earnings>0:
            print(f'{GREEN} {earnings}↑{DEFAULT}')

        else:
             print(f'{RED} ({abs(earnings)})↓{DEFAULT}')
