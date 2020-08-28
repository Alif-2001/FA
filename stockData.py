import bs as data
from termcolor import colored

SUCCESS = 'green'
FAIL = 'red'
OK = 'yellow'

def convertInt(string, name):
    if string == '-' or string == 'N/A':
        #FIX THIS
        printc("THIS DATA MISSING ", 0, 'blue')
        print(name)
        return False
    elif '.' in string:
        string = float(string)
        string *= 1000
        return int(string)
    else:
        string = string.replace(',','')
        return int(string)*1000

def convertFloat(string, name):
    if string == '-' or string == 'N/A':
        #FIX THIS
        printc("THIS DATA MISSING ", 0, 'blue')
        print(name)
        return False
    else:
        string = string.replace(',','')
        return float(string)

def percentageChange(inputList):
    count = 0
    change = []

    for i in inputList:
        if count < (len(inputList)-1):
            if inputList[count+1] != 0:
                change.append(((i-inputList[count+1])/inputList[count+1])*100)
            else:
                change.append(i*100)
        count += 1
        
    count = 0
    total = 0
    for i in change:
        total += i
        count += 1

    return (total/count)

def adder(listInput, listTodivide):
    listToAdd = []

    if len(listTodivide) == len(listInput):
        c = 0
        for i in listInput:
            if listTodivide[c] != 0:
                listToAdd.append(i/listTodivide[c])
            else:
                listToAdd.append(0)
            c+=1
    elif len(listTodivide)>len(listInput):
        c = 1
        for i in listInput:
            if listTodivide[c] != 0:
                listToAdd.append(i/listTodivide[c])
            else:
                listToAdd.append(0)
            c += 1
    elif len(listInput)>len(listTodivide):
        c = 1
        for i in listTodivide:
            if i != 0:
                listToAdd.append(listInput[c]/i)
            else:
                listToAdd.append(0)
            c += 1
    else:
        c = 0
        for i in listInput:
            if listTodivide[c] != 0:
                listToAdd.append(i/listTodivide[c])
            else:
                listToAdd.append(0)
            c+=1
        
    
    return listToAdd

def printc(string, data, color):
    print(colored(string+str(data),color))

def check_Growth(change, string, allData, growth):
    if change > 0:
        if growth == True:
            printc(string, change, SUCCESS)
            print(allData)
        else:
            printc(string, change, FAIL)
            print(allData)
    
    if change < 0:
        if growth == True:
            printc(string, change, FAIL)
            print(allData)
        else:
            printc(string, change, SUCCESS)
            print(allData)

notWork = []


class Stock:

    def __init__(self, symbol, notWork):
        self.symbol = symbol
        
        #initialize summary
        self.growth = data.growth_estimates(self.symbol,notWork)
        self.financials =  data.finance(self.symbol, notWork)
        self.summary = data.summary(self.symbol, notWork)
        self.balanceSheet = data.balance_sheet(self.symbol, notWork)
        self.cash = data.cash_flow(self.symbol, notWork)
        self.stat = data.statistics(self.symbol, notWork)
        
        self.open = self.summary[0]["Open"]
        self.previousClose = self.summary[0]["Previous Close"]

        #initialize financials

    def get_financials(self):
        self.totalRev = []
        self.cost = []
        self.GP = []
        self.operatingExp = []
        self.operatingInc = []
        self.interestExp = []
        self.otherIncExp = []
        self.pretaxInc = []
        self.taxExp = []
        self.netInc = []
        self.basicEPS = []
        self.dilutedEPS = []
        self.TrailingPE = []

        financials = self.financials 
        summary = self.summary

        for i in financials:
            if financials[i]["Total Revenue"]:
                item = financials[i]["Total Revenue"]
                if convertInt(item, 'Total Rev') != False:
                    self.totalRev.append(convertInt(item, 'Total Rev'))

            if financials[i]["Cost"]:
                item = financials[i]["Cost"]
                if convertInt(item, 'Cost') != False:
                    self.cost.append(convertInt(item, 'Cost'))

            if financials[i]["Gross Profit"]:
                item = financials[i]["Gross Profit"]
                if convertInt(item, 'Gross Profit') != False:
                    self.GP.append(convertInt(item, 'Gross Profit'))
            
            if financials[i]["Operating Expense"]:
                item = financials[i]["Operating Expense"]
                if convertInt(item, 'Operating Expense') != False:
                    self.operatingExp.append(convertInt(item, 'Operating Expense'))
            
            if financials[i]["Operating Income or Loss"]:
                item = financials[i]["Operating Income or Loss"]
                if convertInt(item, 'Operating Income') != False:
                    self.operatingInc.append(convertInt(item, 'Operating Income'))
            
            if financials[i]["Interest Expense"]:
                item = financials[i]["Interest Expense"]
                if convertInt(item, 'Interest Expense') != False:
                    self.interestExp.append(convertInt(item, 'Interest Expense'))
            
            if financials[i]["Other Income Expense"]:
                item = financials[i]["Other Income Expense"]
                if convertInt(item, 'Other Income expense') != False:
                    self.otherIncExp.append(convertInt(item, 'Other Income expense'))
            
            if financials[i]["Pretax Income"]:
                item = financials[i]["Pretax Income"]
                if convertInt(item, 'Pretax Income') != False:
                    self.pretaxInc.append(convertInt(item,'Pretax Income'))
            
            if financials[i]["Tax Expense"]:
                item = financials[i]["Tax Expense"]
                if convertInt(item, 'Tax Expense') != False:
                    self.taxExp.append(convertInt(item,'Tax Expense'))

            if financials[i]["Net Income"]:
                item = financials[i]["Net Income"]
                if convertInt(item, 'Net Income') != False:
                    self.netInc.append(convertInt(item, 'Net Income'))

            if financials[i]["Basic EPS"]:

                #add if i == 0

                if i>0:
                    item = financials[i]["Basic EPS"]
                    if convertFloat(item, 'Basic EPS') != False:
                        self.basicEPS.append(convertFloat(item, 'Basic EPS')*1000)

            if financials[i]["Diluted EPS"]:

                #add if i == 0
                if i == 0:
                    item = summary[0]["EPS"]
                    if convertFloat(item, 'EPS') != False:
                        self.dilutedEPS.append(convertFloat(item,'EPS'))

                if i>0:
                    item = financials[i]["Diluted EPS"]
                    if item == '0':
                        item = '0.0005'
                    elif item == '-0':
                        item = '-0.0005'
                    if convertFloat(item, 'Diluted EPS') != False:
                        self.dilutedEPS.append(convertFloat(item,'Diluted EPS')*1000)
        
        # Shares Outstanding

        if self.netInc != [] or self.dilutedEPS != []:
            self.sharesOutstanding = adder(self.netInc, self.dilutedEPS)
            self.PEratio = convertFloat(self.open,'Open')/self.dilutedEPS[0]

            stat = self.stat

            for i in stat:
                if stat[i]['PE Ratio'] != 'N/A' and stat[i]['PE Ratio'] != '-':
                    item = stat[i]['PE Ratio']
                    for i in item:
                        if i == 'k':
                            item = item.replace('k','')
                            item = float(item)
                            item *= 1000
                            item = str(item)        
                    self.TrailingPE.append(convertFloat(item,'PE ratio'))
                else:
                    self.TrailingPE.append(self.PEratio)
        else:
            self.sharesOutstanding = []
            self.PEratio = []

        
        if self.totalRev == [] or self.cost == [] or self.GP == [] or self.operatingExp == [] or self.operatingInc == [] or self.interestExp == [] or self.otherIncExp == [] or self.pretaxInc == [] or self.taxExp == [] or self.netInc == [] or self.basicEPS == [] or self.dilutedEPS == [] or self.TrailingPE == [] or self.sharesOutstanding == []:
            print('some data missing in Income statement')
            return False




        #initialize balance sheet

    def get_balance_sheet(self):
        self.totalCurAssets = []
        self.totalNonCurAssets = []
        self.totalAssets = []
        self.totalCurLiab = []
        self.totalNonCurLiab = []
        self.totalLiab = []
        self.totalSE = []
        self.totalLiabAndSE = []
        self.cashAndCashEq = []
        self.longTermDebt = []

        balanceSheet = self.balanceSheet

        for i in balanceSheet:
            if balanceSheet[i]["Total Current Assets"]:
                item = balanceSheet[i]["Total Current Assets"]
                if convertInt(item, 'Total Cur Assets') != False:
                    self.totalCurAssets.append(convertInt(item, 'Total Cur Assets'))

            if balanceSheet[i]["Total Non Current Assets"]:
                item = balanceSheet[i]["Total Non Current Assets"]
                if convertInt(item, 'Total Non Current Assets') != False:
                    self.totalNonCurAssets.append(convertInt(item, 'Total Non Current Assets'))
            
            if balanceSheet[i]["Total Assets"]:
                item = balanceSheet[i]["Total Assets"]
                if convertInt(item, 'Total Assets') != False:
                    self.totalAssets.append(convertInt(item, 'Total Assets'))
            
            if balanceSheet[i]["Total Current Liabilities"]:
                item = balanceSheet[i]["Total Current Liabilities"]
                if convertInt(item, 'Total Current Liab') != False:
                    self.totalCurLiab.append(convertInt(item, 'Total Current Liab'))
            
            if balanceSheet[i]["Total Non Current Liabilities"]:
                item = balanceSheet[i]["Total Non Current Liabilities"]
                if convertInt(item, 'Total Non Current Liab') != False:
                    self.totalNonCurLiab.append(convertInt(item, 'Total Non Current Liab'))
            
            if balanceSheet[i]["Total Liabilities"]:
                item = balanceSheet[i]["Total Liabilities"]
                if convertInt(item, 'Total Liab') != False:
                    self.totalLiab.append(convertInt(item,'Total Liab'))
            
            if balanceSheet[i]["Total SE"]:
                item = balanceSheet[i]["Total SE"]
                if convertInt(item, 'Total SE') != False:
                    self.totalSE.append(convertInt(item,'Total SE'))
            
            if balanceSheet[i]["Total Liabilities and SE"]:
                item = balanceSheet[i]["Total Liabilities and SE"]
                if convertInt(item, 'Total Liab & SE') != False:
                    self.totalLiabAndSE.append(convertInt(item,'Total Liab & SE'))
            
            if balanceSheet[i]["Cash And Cash Equivalents"]:
                item = balanceSheet[i]["Cash And Cash Equivalents"]
                if convertInt(item, 'Cash and Cash Eq.') != False:
                    self.cashAndCashEq.append(convertInt(item,'Cash and Cash Eq.'))
            
            if balanceSheet[i]["Long-Term Debt"]:
                item = balanceSheet[i]["Long-Term Debt"]
                if convertInt(item, 'Long-Term Debt') != False:
                    self.longTermDebt.append(convertInt(item,'Long-Term Debt'))
        
        # stat = data.statistics(self.symbol)

        # for i in stat:
            #if stat[i]['Shares Outstanding']:
                #item = stat[i]['Shares Outstanding']
                #item = item.replace('M','')
                #item = (float(item))*1000000

        # self.bookValuePerShare

        if self.totalCurAssets == [] or self.totalNonCurAssets == [] or self.totalAssets == [] or self.totalCurLiab == [] or self.totalNonCurLiab == [] or self.totalLiab == [] or self.totalSE == [] or self.totalLiabAndSE == [] or self.cashAndCashEq == [] or self.longTermDebt == [] :
            print('some data missing in Balance sheet')
            return False


        #initialize cash flow
    def get_cash_flow(self):
        self.freeCashFlow = []
        self.operatingCashFlow = []
        self.capitalExpenditure = []

        cash = self.cash

        for i in cash:
            if cash[i]["Free Cash Flow"]:
                item = cash[i]["Free Cash Flow"]
                if convertInt(item, 'FCF') != False:
                    self.freeCashFlow.append(convertInt(item,'FCF'))
            
            if cash[i]["Operating Cash Flow"]:
                item = cash[i]["Operating Cash Flow"]
                if convertInt(item, 'Operating Exp') != False:
                    self.operatingCashFlow.append(convertInt(item,'Operating Exp'))
            
            if cash[i]["Capital Expenditure"]:
                item = cash[i]["Capital Expenditure"]
                if convertInt(item, 'Capital Expenditure') != False:
                    self.capitalExpenditure.append(convertInt(item,'Capital Expenditure'))
            
        
        if self.freeCashFlow == [] or self.operatingCashFlow == [] or self.capitalExpenditure == []:
            print('some data missing in cash flow')
            return False
            

        #initialize growth estimates
    def get_growth(self):
        growth = self.growth

        self.nextQtrGrowth = growth[0]["Next Qtr."]
        self.nextYearGrowth = growth[0]["Next Year"]


        self.next5YearGrowth = growth[0]["Next 5 Years"]
        self.next5YearGrowth = self.next5YearGrowth.replace('%','')
        self.next5YearGrowth = convertFloat(self.next5YearGrowth,'Next five growth')/100


    def calculate_filter(self):

        go = 0

        if self.get_financials() != False:
            go += 1
        
        if self.get_balance_sheet() != False:
            go += 1


        if go == 2:

            self.ROE = adder(self.netInc, self.totalSE)
            
            #for banks
            if self.totalCurAssets != None or self.totalCurLiab != None:
                self.currentRatio = adder(self.totalCurAssets, self.totalCurLiab)
            else:
                print('Current Ratio missing')
                self.currentRatio.append(0)

            self.debtToEquity = adder(self.totalLiab, self.totalSE)
        else:
            return False

    def calculate_FA(self):

        go = 0

        if self.calculate_filter() != False:
            go += 1
        
        if self.get_cash_flow() != False:
            go += 1

        if go == 2:

            #calculate book value per share
            self.bookValuePerShare = adder(self.totalSE, self.sharesOutstanding)
            
            #calculate Net margin
            self.netMargin = adder(self.netInc, self.totalRev)
            

            #forEPS growth
            self.EPSGrowth = percentageChange(self.dilutedEPS)
            self.FCFGrowth = percentageChange(self.freeCashFlow)
            self.CACEqGrowth = percentageChange(self.cashAndCashEq)
            self.BVPSGrowth = percentageChange(self.bookValuePerShare)
            self.NMGrowth = percentageChange(self.netMargin)
            self.ROEGrowth = percentageChange(self.ROE)
            self.DTEqGrowth = percentageChange(self.debtToEquity)
        
        else:
            return False


    def filter(self):
        if self.calculate_filter() != False:

            ROE = False
            CR = False
            DTEq = False

            if self.ROE[0]>=0.15:
                ROE = True
                printc('ROE: ',self.ROE[0], SUCCESS)
            else:
                printc('ROE: ',self.ROE[0], FAIL)

            if self.currentRatio[0]>=0.02:
                CR = True
                printc('Current Ratio: ',self.currentRatio[0], SUCCESS)
            else:
                printc('Current Ratio: ',self.currentRatio[0], FAIL)

            if self.debtToEquity[0]<=0.5:
                DTEq = True
                printc('Debt to equity: ',self.debtToEquity[0], SUCCESS) 
            elif self.debtToEquity[0]>0.5 and self.debtToEquity[0]<=1.5:
                DTEq = True
                printc('Debt to equity: ',self.debtToEquity[0], OK)   
            else:
                printc('Debt to equity: ',self.debtToEquity[0], FAIL)
                print('CHECK INDUSTRY : FINANCE? CONSTRUCTION? MANUFACTURING?')

             
    def FA(self):
        if self.calculate_FA() != False:
            EPSGrowth = False
            PEGrowth = False
            FCFGrowth = False
            CACGrowth = False
            BVPSGrowth = False
            NMGrowth = False
            ROEGrowth = False
            DTEqGrowth = False

            check_Growth(self.EPSGrowth, "EPS GROWTH %: ", self.dilutedEPS, True)
            check_Growth(self.FCFGrowth, "FCF GROWTH %: ", self.freeCashFlow, True)
            check_Growth(self.CACEqGrowth, "Cash and Cash Eq GROWTH %: ", self.cashAndCashEq, True)
            check_Growth(self.BVPSGrowth, "Book Value Per Share GROWTH %: ", self.bookValuePerShare, True)
            check_Growth(self.NMGrowth, "Net Margin GROWTH %: ", self.netMargin, True)
            check_Growth(self.ROEGrowth, "ROE GROWTH %: ", self.ROE, True)
            check_Growth(self.DTEqGrowth, "Debt to equity GROWTH %: ", self.debtToEquity, False)
        

    def valuation(self):
        if self.calculate_FA() != False:

            self.get_growth()
            

            #FCF
            fcf = self.freeCashFlow[0]
            gr = self.next5YearGrowth
            MS = 0.25
            GDR = 0.05
            LGRC = 0.03
            discountRate = 0.1

            mult = gr*(1-MS)
            FCFYearOne = fcf*(1+mult)
            
            mult = 1 + (mult*(1-GDR))
            FCFYearFive = FCFYearOne* (mult**4)

            terminalValue = (FCFYearFive*(1+LGRC))/(discountRate-LGRC)
            NPV = terminalValue/((1+discountRate)**5)

            companyValue = NPV + (self.cashAndCashEq[0]) - (self.longTermDebt[0])
            intrisicValueStock = companyValue/self.sharesOutstanding[0]

            print('Company value: '+str(companyValue))
            print('Intrisic Value: '+str(intrisicValueStock))





