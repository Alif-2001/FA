from stockData import *


'''
db = data.most_actives()

symbols = []
for i in db:
    symbols.append(db[i]['Symbols'])

print(i)
'''

z = 0

symbols = ["MGM"]

for symbol in symbols:

    print(z, symbol)
    print('\n')

    stock = Stock(symbol,notWork)
    print(stock.open)
    stock.filter()
    print('\n')
    stock.FA()
    print('\n')
    stock.valuation()
    print('\n')

    print('-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0\n')

    z+=1

#print(notWork)

#stock = Stock(symbol)
#stock.valuation()
#stock.FA()


'''
stock.get_balance_sheet()
stock.get_financials()
print(stock.cashAndCashEq)
print(percentageChange(stock.cashAndCashEq))
'''