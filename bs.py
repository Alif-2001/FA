import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import csv
import pandas as pd
import time

from fake_useragent import UserAgent
from random import choice
from time import sleep
from urllib.parse import urlparse

import traceback

PROXY = True

def get_proxies():
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, features = 'html.parser')
    proxies = []
    for i in soup.find_all('table', attrs={'id':'proxylisttable'}):
        for row in i.find_all('tr'):
            ip = row.find('td')
            IP = str(ip)
            IP = IP.replace('<td>','')
            port = row.select("tr > td:nth-child(2)")
            PORT = str(port)
            PORT = PORT.replace('[<td>','')
            PORT = PORT.replace('</td>]','')
            IP = IP.replace('</td>','')
            IP = IP + ':'
            IP = IP + PORT
            if IP != None and IP != 'None:[]':
                proxies.append(IP)
    return proxies

def get_proxies_2():
    url = 'https://www.proxynova.com/proxy-server-list/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, features='html.parser')
    proxies = []
    for i in soup.find_all('table', attrs = {'class': 'table'}):
        for row in i.find_all('tr'):
            ip = row.find('td', attrs = {'align': 'left'})
            if ip != None:
                item = ip.find('script')
                IP = str(item)
                IP = IP.replace("<script>document.write('", "")
                IP = IP.replace("');</script>","")
                port = ip.find_next_sibling().text
                IP = IP + ':'
                port = str(port)
                port = port.replace(' ','')
                port = port.replace('\n','')
                IP = IP + port
                proxies.append(IP)
        
    return proxies

PROXIES = get_proxies()

def proxy_generator(PROXIES):
    # construct an HTTP session
    session = requests.Session()
    # choose one random proxy
    proxy = {"https":choice(PROXIES)}
    #session.proxies = {"https": proxy, "https": proxy}
    return proxy


def data_scraper(request_method, url, notWork, **kwargs):

    while True:
        try: 
            proxy = proxy_generator(PROXIES)
            if proxy not in notWork:
                print("Proxy currently being used: {}".format(proxy))
                response = requests.request(request_method, url, proxies=proxy, timeout=30, **kwargs)
                break
            # if the request is successful, no exception is raised
        except:
            print(proxy)
            notWork.append(proxy)
            print("Connection error, looking for another proxy")

            pass

    return response

#response = data_scraper('get', "https://zenscrape.com/ultimate-list-15-best-services-offering-rotating-proxies/", notWork)

def summary(symbol, notWork):
    
    URL = "https://finance.yahoo.com/quote/"+symbol+"?p="+symbol

    if PROXY:
        response = data_scraper('get',URL, notWork)
    else:
        response = requests.get(URL)

    soup = BeautifulSoup(response.text, features="html.parser")


    #FIX THIS

    Open = '1'
    previousClose = '1'
    PEratio = '1'
    EPS = '1'

    for table in soup.find_all('div', attrs = {'id': 'quote-summary'}):
        for row in table.find_all('tr', attrs = {'class': 'Bxz(bb)'}):
            if row.find('td', attrs = {'class': 'C($primaryColor)'}).find('span').text == "Previous Close":
                item = row.find('td', attrs = {'class': 'Ta(end)'}).find('span')
                previousClose = item.text
            
            if row.find('td', attrs = {'class': 'C($primaryColor)'}).find('span').text == "Open":
                item = row.find('td', attrs = {'class': 'Ta(end)'}).find('span')
                Open = item.text
            
            if row.find('td', attrs = {'class': 'C($primaryColor)'}).find('span').text == "PE Ratio (TTM)":
                item = row.find('td', attrs = {'class': 'Ta(end)'}).find('span')
                PEratio = item.text
            
            if row.find('td', attrs = {'class': 'C($primaryColor)'}).find('span').text == "EPS (TTM)":
                item = row.find('td', attrs = {'class': 'Ta(end)'}).find('span')
                EPS = item.text

    a = {"Open": Open, "Previous Close": previousClose, "PE Ratio": PEratio, "EPS": EPS}
    df = pd.DataFrame.from_dict(a, orient = 'index')

    return df

def finance(symbol, notWork):
    Date = []
    TotalRev = []
    Cost = []
    GP = []
    OperatingExp = []
    OperatingInc = []
    InterestExpense = []
    OtherIncomeExp = []
    PretaxIncome = []
    TaxExpense = []
    NetIncome = []
    BasicEPS = []
    DilutedEPS = []

    URL = "https://finance.yahoo.com/quote/"+symbol+"/financials?p="+symbol

    if PROXY:
        response = data_scraper('get',URL, notWork)
    else:
        response = requests.get(URL)

    soup = BeautifulSoup(response.text, features="html.parser")

    for listing in soup.find_all('div', attrs = {'class':'BdEnd'}):
        for breakdown in listing.find_all('div', attrs = {'class':'D(tbr)'}):
            if breakdown.find('div', attrs={'class':'D(ib)'}).find('span').text == 'Breakdown':
                dates = breakdown.find('div', attrs={'class':'D(ib)'})
                for date in dates.find_next_siblings('div', attrs={'class': 'Ta(c)'}):
                    Date.append(date.text)

            if breakdown.find('div', attrs={'class':'D(ib)'}).find('span').text == 'Total Revenue':
                items = breakdown.find('div', attrs={'class':'D(tbc)'})
                for item in items.find_next_siblings('div', attrs={'class': 'Ta(c)'}):
                    TotalRev.append(item.text)
            
            if breakdown.find('div', attrs={'class':'D(ib)'}).find('span').text == 'Cost of Revenue':
                items = breakdown.find('div', attrs={'class':'D(tbc)'})
                for item in items.find_next_siblings('div', attrs={'class': 'Ta(c)'}):
                    Cost.append(item.text)
                    

            if breakdown.find('div', attrs={'class':'D(ib)'}).find('span').text == 'Gross Profit':
                items = breakdown.find('div', attrs={'class':'D(tbc)'})
                for item in items.find_next_siblings('div', attrs={'class': 'Ta(c)'}):
                    GP.append(item.text)
                            

            if breakdown.find('div', attrs={'class':'D(ib)'}).find('span').text == 'Operating Expense':
                items = breakdown.find('div', attrs={'class':'D(tbc)'})
                for item in items.find_next_siblings('div', attrs={'class': 'Ta(c)'}):
                    OperatingExp.append(item.text)
                    
            
            if breakdown.find('div', attrs={'class':'D(ib)'}).find('span').text == 'Operating Income' or breakdown.find('div', attrs={'class':'D(ib)'}).find('span').text == 'Operating Income or Loss':
                items = breakdown.find('div', attrs={'class':'D(tbc)'})
                for item in items.find_next_siblings('div', attrs={'class': 'Ta(c)'}):
                    OperatingInc.append(item.text)

            if breakdown.find('div', attrs={'class':'D(ib)'}).find('span').text == 'Interest Expense':
                items = breakdown.find('div', attrs={'class':'D(tbc)'})
                for item in items.find_next_siblings('div', attrs={'class': 'Ta(c)'}):
                    InterestExpense.append(item.text)

            if breakdown.find('div', attrs={'class':'D(ib)'}).find('span').text == 'Other Income Expense' or breakdown.find('div', attrs={'class':'D(ib)'}).find('span').text == 'Total Other Income/Expense Net':
                items = breakdown.find('div', attrs={'class':'D(tbc)'})
                for item in items.find_next_siblings('div', attrs={'class': 'Ta(c)'}):
                    OtherIncomeExp.append(item.text)
                
            if breakdown.find('div', attrs={'class':'D(ib)'}).find('span').text == 'Pretax Income' or breakdown.find('div', attrs={'class':'D(ib)'}).find('span').text == 'Income Before Tax':
                items = breakdown.find('div', attrs={'class':'D(tbc)'})
                for item in items.find_next_siblings('div', attrs={'class': 'Ta(c)'}):
                    PretaxIncome.append(item.text)

            if breakdown.find('div', attrs={'class':'D(ib)'}).find('span').text == 'Income Tax Expense' or breakdown.find('div', attrs={'class':'D(ib)'}).find('span').text == 'Tax Provision':
                items = breakdown.find('div', attrs={'class':'D(tbc)'})
                for item in items.find_next_siblings('div', attrs={'class': 'Ta(c)'}):
                    TaxExpense.append(item.text)

            if breakdown.find('div', attrs={'class':'D(ib)'}).find('span').text == 'Net Income' or breakdown.find('div', attrs={'class':'D(ib)'}).find('span').text == 'Net Income Common Stockholders':
                items = breakdown.find('div', attrs={'class':'D(tbc)'})
                for item in items.find_next_siblings('div', attrs={'class': 'Ta(c)'}):
                    NetIncome.append(item.text)

            if breakdown.find('div', attrs={'class':'D(ib)'}).find('span').text == 'Basic EPS':
                items = breakdown.find('div', attrs={'class':'D(tbc)'})
                for item in items.find_next_siblings('div', attrs={'class': 'Ta(c)'}):
                    BasicEPS.append(item.text)
            
            if breakdown.find('div', attrs={'class':'D(ib)'}).find('span').text == 'Diluted EPS':
                items = breakdown.find('div', attrs={'class':'D(tbc)'})
                for item in items.find_next_siblings('div', attrs={'class': 'Ta(c)'}):
                    DilutedEPS.append(item.text)

    a = {"Date": Date, "Total Revenue": TotalRev, "Cost": Cost, "Gross Profit": GP, "Operating Expense": OperatingExp, "Operating Income or Loss": OperatingInc, "Interest Expense": InterestExpense, "Other Income Expense": OtherIncomeExp, "Pretax Income": PretaxIncome, "Tax Expense": TaxExpense, "Net Income": NetIncome, "Basic EPS": BasicEPS, "Diluted EPS": DilutedEPS}
    df = pd.DataFrame.from_dict(a, orient='index')

    return df



def balance_sheet(symbol, notWork):
    Date = []

    CashAndCashEq = []
    ShortTermInv = []
    TotalCash = []
    NetReceivables = []
    Inventory = []
    TotalCurrentAssets = []

    GrossPPE = []
    Depreciation = []
    NetPPE = []
    Goodwill = []
    IntangibleAssets = []
    OtherLongTermAssets = []
    TotalNonCurrentAssets = []

    TotalAssets = []


    AccountsPayable = []
    AccruedLiabilities = []
    DeferredRevenues = []
    TotalCurrentLiabilities = []

    LongTermDebt = []
    DeferredTaxesLiabilities = []
    OtherLongTermLiabities = []
    TotalNonCurrentLiabilities = []

    TotalLiabilities = []

    CommonStock = []
    RetainedEarnings = []
    AccumulatedOtherIncome = []
    TotalSE = []

    TotalLiabiltiesAndSE = []

    URL = "https://ca.finance.yahoo.com/quote/"+symbol+"/balance-sheet?p="+symbol

    if PROXY:
        response = data_scraper('get',URL, notWork)
    else:
        response = requests.get(URL)

    soup = BeautifulSoup(response.text, features="html.parser")

    for listing in soup.find_all('div', attrs = {'class': 'BdEnd'}):
        for breakdown in listing.find_all('div', attrs = {'class': 'D(tbr)'}):
            if breakdown.find('div', attrs = {'class': 'D(ib)'}).find('span').text == 'Breakdown':
                items = breakdown.find('div', attrs = {'class':'D(ib)'})
                for item in items.find_next_siblings('div', attrs = {'class': 'Ta(c)'}):
                    Date.append(item.text)

            if breakdown.find('div', attrs = {'class': 'D(ib)'}).find('span').text == 'Cash And Cash Equivalents':
                items = breakdown.find('div', attrs = {'class':'D(tbc)'})
                for item in items.find_next_siblings('div', attrs = {'class': 'Ta(c)'}):
                    CashAndCashEq.append(item.text)

            if breakdown.find('div', attrs = {'class': 'D(ib)'}).find('span').text == 'Other Short Term Investments':
                items = breakdown.find('div', attrs = {'class':'D(tbc)'})
                for item in items.find_next_siblings('div', attrs = {'class': 'Ta(c)'}):
                    ShortTermInv.append(item.text)

            if breakdown.find('div', attrs = {'class': 'D(ib)'}).find('span').text == 'Total Cash':
                items = breakdown.find('div', attrs = {'class':'D(tbc)'})
                for item in items.find_next_siblings('div', attrs = {'class': 'Ta(c)'}):
                    TotalCash.append(item.text)
                    
            if breakdown.find('div', attrs = {'class': 'D(ib)'}).find('span').text == 'Net Receivables':
                items = breakdown.find('div', attrs = {'class':'D(tbc)'})
                for item in items.find_next_siblings('div', attrs = {'class': 'Ta(c)'}):
                    NetReceivables.append(item.text)
                    
            if breakdown.find('div', attrs = {'class': 'D(ib)'}).find('span').text == 'Inventory':
                items = breakdown.find('div', attrs = {'class':'D(tbc)'})
                for item in items.find_next_siblings('div', attrs = {'class': 'Ta(c)'}):
                    Inventory.append(item.text)

            if breakdown.find('div', attrs = {'class': 'D(ib)'}).find('span').text == 'Total Current Assets':
                items = breakdown.find('div', attrs = {'class':'D(tbc)'})
                for item in items.find_next_siblings('div', attrs = {'class': 'Ta(c)'}):
                    TotalCurrentAssets.append(item.text)
                    
            if breakdown.find('div', attrs = {'class': 'D(ib)'}).find('span').text == 'Gross property, plant and equipment':
                items = breakdown.find('div', attrs = {'class':'D(tbc)'})
                for item in items.find_next_siblings('div', attrs = {'class': 'Ta(c)'}):
                    GrossPPE.append(item.text)
                    
            if breakdown.find('div', attrs = {'class': 'D(ib)'}).find('span').text == 'Accumulated Depreciation':
                items = breakdown.find('div', attrs = {'class':'D(tbc)'})
                for item in items.find_next_siblings('div', attrs = {'class': 'Ta(c)'}):
                    Depreciation.append(item.text)
                    
            
            if breakdown.find('div', attrs = {'class': 'D(ib)'}).find('span').text == 'Net property, plant and equipment':
                items = breakdown.find('div', attrs = {'class':'D(tbc)'})
                for item in items.find_next_siblings('div', attrs = {'class': 'Ta(c)'}):
                    NetPPE.append(item.text)
                
            if breakdown.find('div', attrs = {'class': 'D(ib)'}).find('span').text == 'Goodwill':
                items = breakdown.find('div', attrs = {'class':'D(tbc)'})
                for item in items.find_next_siblings('div', attrs = {'class': 'Ta(c)'}):
                    Goodwill.append(item.text)
                    
            if breakdown.find('div', attrs = {'class': 'D(ib)'}).find('span').text == 'Intangible Assets':
                items = breakdown.find('div', attrs = {'class':'D(tbc)'})
                for item in items.find_next_siblings('div', attrs = {'class': 'Ta(c)'}):
                    IntangibleAssets.append(item.text)
            
            if breakdown.find('div', attrs = {'class': 'D(ib)'}).find('span').text == 'Other long-term assets':
                items = breakdown.find('div', attrs = {'class':'D(tbc)'})
                for item in items.find_next_siblings('div', attrs = {'class': 'Ta(c)'}):
                    OtherLongTermAssets.append(item.text)

            if breakdown.find('div', attrs = {'class': 'D(ib)'}).find('span').text == 'Total non-current assets':
                items = breakdown.find('div', attrs = {'class':'D(tbc)'})
                for item in items.find_next_siblings('div', attrs = {'class': 'Ta(c)'}):
                    TotalNonCurrentAssets.append(item.text)
                    
            if breakdown.find('div', attrs = {'class': 'D(ib)'}).find('span').text == 'Total Assets':
                items = breakdown.find('div', attrs = {'class':'D(tbc)'})
                for item in items.find_next_siblings('div', attrs = {'class': 'Ta(c)'}):
                    TotalAssets.append(item.text)
                    
            if breakdown.find('div', attrs = {'class': 'D(ib)'}).find('span').text == 'Accounts Payable':
                items = breakdown.find('div', attrs = {'class':'D(tbc)'})
                for item in items.find_next_siblings('div', attrs = {'class': 'Ta(c)'}):
                    AccountsPayable.append(item.text)
                    
            if breakdown.find('div', attrs = {'class': 'D(ib)'}).find('span').text == 'Accrued liabilities':
                items = breakdown.find('div', attrs = {'class':'D(tbc)'})
                for item in items.find_next_siblings('div', attrs = {'class': 'Ta(c)'}):
                    AccruedLiabilities.append(item.text)
            
            if breakdown.find('div', attrs = {'class': 'D(ib)'}).find('span').text == 'Deferred revenues':
                items = breakdown.find('div', attrs = {'class':'D(tbc)'})
                for item in items.find_next_siblings('div', attrs = {'class': 'Ta(c)'}):
                    DeferredRevenues.append(item.text)
            
            if breakdown.find('div', attrs = {'class': 'D(ib)'}).find('span').text == 'Total Current Liabilities':
                items = breakdown.find('div', attrs = {'class':'D(tbc)'})
                for item in items.find_next_siblings('div', attrs = {'class': 'Ta(c)'}):
                    TotalCurrentLiabilities.append(item.text)
            
            if breakdown.find('div', attrs = {'class': 'D(ib)'}).find('span').text == 'Long Term Debt':
                items = breakdown.find('div', attrs = {'class':'D(tbc)'})
                for item in items.find_next_siblings('div', attrs = {'class': 'Ta(c)'}):
                    LongTermDebt.append(item.text)
            
            if breakdown.find('div', attrs = {'class': 'D(ib)'}).find('span').text == 'Deferred taxes liabilities':
                items = breakdown.find('div', attrs = {'class':'D(tbc)'})
                for item in items.find_next_siblings('div', attrs = {'class': 'Ta(c)'}):
                    DeferredTaxesLiabilities.append(item.text)
            
            if breakdown.find('div', attrs = {'class': 'D(ib)'}).find('span').text == 'Other long-term liabilities':
                items = breakdown.find('div', attrs = {'class':'D(tbc)'})
                for item in items.find_next_siblings('div', attrs = {'class': 'Ta(c)'}):
                    OtherLongTermLiabities.append(item.text)
                    
            if breakdown.find('div', attrs = {'class': 'D(ib)'}).find('span').text == 'Total non-current liabilities':
                items = breakdown.find('div', attrs = {'class':'D(tbc)'})
                for item in items.find_next_siblings('div', attrs = {'class': 'Ta(c)'}):
                    TotalNonCurrentLiabilities.append(item.text)
            
            if breakdown.find('div', attrs = {'class': 'D(ib)'}).find('span').text == 'Total Liabilities':
                items = breakdown.find('div', attrs = {'class':'D(tbc)'})
                for item in items.find_next_siblings('div', attrs = {'class': 'Ta(c)'}):
                    TotalLiabilities.append(item.text)
            
            if breakdown.find('div', attrs = {'class': 'D(ib)'}).find('span').text == 'Common Stock':
                items = breakdown.find('div', attrs = {'class':'D(tbc)'})
                for item in items.find_next_siblings('div', attrs = {'class': 'Ta(c)'}):
                    CommonStock.append(item.text)
            
            if breakdown.find('div', attrs = {'class': 'D(ib)'}).find('span').text == 'Retained Earnings':
                items = breakdown.find('div', attrs = {'class':'D(tbc)'})
                for item in items.find_next_siblings('div', attrs = {'class': 'Ta(c)'}):
                    RetainedEarnings.append(item.text)
            
            if breakdown.find('div', attrs = {'class': 'D(ib)'}).find('span').text == 'Accumulated other comprehensive income':
                items = breakdown.find('div', attrs = {'class':'D(tbc)'})
                for item in items.find_next_siblings('div', attrs = {'class': 'Ta(c)'}):
                    AccumulatedOtherIncome.append(item.text)

            if breakdown.find('div', attrs = {'class': 'D(ib)'}).find('span').text == "Total stockholders' equity":
                items = breakdown.find('div', attrs = {'class':'D(tbc)'})
                for item in items.find_next_siblings('div', attrs = {'class': 'Ta(c)'}):
                    TotalSE.append(item.text)
            
            if breakdown.find('div', attrs = {'class': 'D(ib)'}).find('span').text == "Total liabilities and stockholders' equity":
                items = breakdown.find('div', attrs = {'class':'D(tbc)'})
                for item in items.find_next_siblings('div', attrs = {'class': 'Ta(c)'}):
                    TotalLiabiltiesAndSE.append(item.text)

        
    a = {"Date": Date, "Total Current Assets": TotalCurrentAssets, "Total Non Current Assets": TotalNonCurrentAssets, "Total Assets": TotalAssets, "Total Current Liabilities": TotalCurrentLiabilities, "Total Non Current Liabilities": TotalNonCurrentLiabilities, "Total Liabilities": TotalLiabilities, "Total SE": TotalSE, "Total Liabilities and SE": TotalLiabiltiesAndSE, "Cash And Cash Equivalents": CashAndCashEq, "Long-Term Debt": LongTermDebt}
    df = pd.DataFrame.from_dict(a, orient = 'index')

    return df

def cash_flow(symbol, notWork):
    Date = []
    FreeCashFlow = []
    OperatingCashFlow = []
    CapitalExpenditure = []

    URL = "https://finance.yahoo.com/quote/"+symbol+"/cash-flow?p="+symbol

    if PROXY:
        response = data_scraper('get',URL, notWork)
    else:
        response = requests.get(URL)

    soup = BeautifulSoup(response.text, features="html.parser")

    for listing in soup.find_all('div', attrs = {'class': 'BdEnd'}):
        for breakdown in listing.find_all('div', attrs = {'class': 'D(tbr)'}):
            if breakdown.find('div', attrs={'class':'D(ib)'}).find('span').text == 'Breakdown':
                dates = breakdown.find('div', attrs={'class':'D(ib)'})
                for date in dates.find_next_siblings('div', attrs={'class': 'Ta(c)'}):
                    Date.append(date.text)
            
            if breakdown.find('div', attrs={'class':'D(ib)'}).find('span').text == 'Free Cash Flow':
                items = breakdown.find('div', attrs={'class':'D(tbc)'})
                for item in items.find_next_siblings('div', attrs={'class': 'Ta(c)'}):
                    FreeCashFlow.append(item.text)

            if breakdown.find('div', attrs={'class':'D(ib)'}).find('span').text == 'Operating Cash Flow':
                items = breakdown.find('div', attrs={'class':'D(tbc)'})
                for item in items.find_next_siblings('div', attrs={'class': 'Ta(c)'}):
                    OperatingCashFlow.append(item.text)
                    
            if breakdown.find('div', attrs={'class':'D(ib)'}).find('span').text == 'Capital Expenditure':
                items = breakdown.find('div', attrs={'class':'D(tbc)'})
                for item in items.find_next_siblings('div', attrs={'class': 'Ta(c)'}):
                    CapitalExpenditure.append(item.text)

    a = {"Date": Date, "Free Cash Flow": FreeCashFlow, "Operating Cash Flow": OperatingCashFlow, "Capital Expenditure": CapitalExpenditure}
    df = pd.DataFrame.from_dict(a, orient = 'index')

    return df                


def historical(symbol):
    Date = []
    Open = []
    High = []
    Low = []
    Close = []
    AdjClose = []
    Volume = []

    # symbol
    histURL = "https://finance.yahoo.com/quote/"+symbol+"/history?p="+symbol

    # Selenium scroll

    driver = webdriver.Safari()
    driver.get(histURL)
    driver.execute_script("window.scrollTo(0, 10000)")
    time.sleep(10)
    driver.execute_script("window.scrollTo(10000, 20000)")
    time.sleep(5)


    # Beautiful soup
    r = driver.page_source
    #data = r.text
    soup = BeautifulSoup(r, features="html.parser")

    driver.close()

    historical = soup.find('table', attrs={'data-test': 'historical-prices'}).find_next('tbody')

        
    for listing in historical.find_all('tr', attrs={'class': 'BdT'}):

        if (len(listing) == 7):

            dates = listing.find('td')
            Date.append(dates.find('span').text)
            
            opens = dates.find_next_sibling('td')
            Open.append(opens.find('span').text)
            
            high = opens.find_next_sibling('td')
            High.append(high.find('span').text)  
            
            low = high.find_next_sibling('td')
            Low.append(low.find('span').text)
            
            close = low.find_next_sibling('td')
            Close.append(close.find('span').text)
            
            adjClose = close.find_next_sibling('td')
            AdjClose.append(adjClose.find('span').text)
            
            volume = adjClose.find_next_sibling('td')
            Volume.append(volume.find('span').text)

        else:
            continue


    a = {"Date" : Date, "Open": Open, "High": High, "Low": Low, "Close": Close, "AdjClose": AdjClose, "Volume": Volume}
    df = pd.DataFrame.from_dict(a, orient='index')

    return df

def growth_estimates(symbol, notWork):
    NextQtr = []
    NextYear = []
    Next5Years = []

    URL = "https://finance.yahoo.com/quote/"+symbol+"/analysis?p="+symbol

    if PROXY:
        response = data_scraper('get',URL, notWork)
    else:
        response = requests.get(URL)

    soup = BeautifulSoup(response.text, features="html.parser")

    for listing in soup.find_all('table', attrs = {'class': 'BdB'}):
        for tables in listing.find_all('tr', attrs = {'class': 'Ta(start)'}):
            if tables.find('th', attrs = {'class': 'Fw(b)'}).text == 'Growth Estimates':
                for rows in listing.find_all('tr', attrs = {'class': 'BdT'}):
                    if rows.find('td', attrs = {'class': 'Ta(start)'}).find('span').text == "Next Qtr.":
                        row = rows.find('td', attrs = {'class': 'Ta(start)'})
                        NextQtr.append((row.find_next_sibling('td', attrs = {'class': 'Ta(end)'}).text))

                    if rows.find('td', attrs = {'class': 'Ta(start)'}).find('span').text == "Next Year":
                        row = rows.find('td', attrs = {'class': 'Ta(start)'})
                        NextYear.append((row.find_next_sibling('td', attrs = {'class': 'Ta(end)'}).text))
                    
                    if rows.find('td', attrs = {'class': 'Ta(start)'}).find('span').text == "Next 5 Years (per annum)":
                        row = rows.find('td', attrs = {'class': 'Ta(start)'})
                        Next5Years.append((row.find_next_sibling('td', attrs = {'class': 'Ta(end)'}).text))
            
    a = {"Next Qtr.": NextQtr, "Next Year": NextYear, "Next 5 Years": Next5Years}
    df = pd.DataFrame.from_dict(a, orient = 'index')

    return df      


def statistics(symbol, notWork):
    URL = "https://finance.yahoo.com/quote/"+symbol+"/key-statistics?p="+symbol

    if PROXY:
        response = data_scraper('get',URL, notWork)
    else:
        response = requests.get(URL)

    soup = BeautifulSoup(response.text, features = "html.parser")

    #can add to get more data

    for listing in soup.find_all('div', attrs = {'class': 'Fl(end)'}):
        for tables in listing.find_all('table', attrs={'class':'Bdcl(c)'}):
            for rows in tables.find_all('tr', attrs={'class': 'Bxz(bb)'}):
                if rows.find('td', attrs={'class':'Pos(st)'}).find('span').text == 'Shares Outstanding':
                    row = rows.find('td', attrs={'class':'Pos(st)'})
                    SharesOutstanding = row.find_next_sibling('td', attrs={'class': 'Ta(end)'}).text
    
    PERatio = []

    for table in soup.find_all('table', attrs = {'class': 'Bdcl(c)'}):
        for row2 in table.find_all('tr', attrs = {'class': 'Bxz(bb)'}):
            if row2.find('td', attrs = {'class': 'Pos(st)'}).find('span').text == 'Trailing P/E':
                item = row2.find('td', attrs = {'class': 'Pos(st)'})
                for col in item.find_next_siblings('td', attrs = {'class': 'Ta(c)'}):
                    PERatio.append(col.text)
                
    a = {"PE Ratio":PERatio}
    df = pd.DataFrame.from_dict(a, orient = 'index')

    return df


def most_actives():
    symbols = []
    names = []
    symbols = []
    prices = []
    changes = []
    percentChanges = []
    marketCaps = []
    volumes = []
    avgVolumes = []
    PE = []


    for i in range(0, 300, 100):
        CryptoCurrenciesUrl = "https://finance.yahoo.com/most-active?count=100&offset="+str(i)

        r = requests.get(CryptoCurrenciesUrl)
        data=r.text
        soup=BeautifulSoup(data, features="html.parser")

        for listing in soup.find_all('tr', attrs={'class':'simpTblRow'}):
            for symbol in listing.find_all('td', attrs={'aria-label': 'Symbol'}):
                symbols.append(symbol.find('a').text)
            for name in listing.find_all('td', attrs={'aria-label':'Name'}):
                names.append(name.text)
            for price in listing.find_all('td',{'aria-label':'Price (Intraday)'}):
                prices.append(price.find('span').text)
            for change in listing.find_all('td', attrs={'aria-label':'Change'}):
                changes.append(change.text)
            for percentChange in listing.find_all('td', attrs={'aria-label':'% Change'}):
                percentChanges.append(percentChange.text)
            for marketCap in listing.find_all('td', attrs={'aria-label':'Market Cap'}):
                marketCaps.append(marketCap.text)
            for volume in listing.find_all('td', attrs={'aria-label':'Volume'}):
                volumes.append(volume.text)
            for avgVolume in listing.find_all('td', attrs={'aria-label':'Avg Vol (3 month)'}):
                avgVolumes.append(avgVolume.text)
            for priceEarning in listing.find_all('td', attrs={'aria-label':'PE Ratio (TTM)'}):
                PE.append(priceEarning.text)
    
    a = {"Symbols":symbols, "Names": names, "Prices": prices, "Change": changes, "% Change": percentChanges, "Market Cap": marketCaps, "Average Volume": avgVolumes,"Volume": volumes, "PE ratio": PE }
    df = pd.DataFrame.from_dict(a, orient='index')

    return df

