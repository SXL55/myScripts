# script takes time series price data from google, and fits it to a polynomial fitting of a user's choice.
# summing the square of the differences between model and data, it then sorts it and creates a list of tickers below a certain threshold
# this list is then fed into a secondary function to determine the most recent price in relation to 2 separate moving averages, and then creating a CSV.

import pandas as pd
import pandas_datareader.data as web
import datetime
from numpy.polynomial import polynomial as P
import numpy as np
import math
import time
import sys

def polyfitting(tickers,power,start,end):
    symbol,fit = [],[]
    for each in tickers:

        stock = web.DataReader(each, "google", start, end)
          
        x = list(range(0,len(stock)))
        y = np.array(stock['Close'])
        y = y.tolist()       
        
        coeff = P.polyfit(x,y,power)
        coeff = coeff.tolist()
        equation = np.poly1d(coeff[::-1])
        derivative = np.polyder(equation)
        derivative2 = np.polyder(derivative)
        SSres = 0
        
        if derivative(len(y)) > 0 and derivative2(len(y)) > 0:
            for i in range(1,len(x)):
                model = 0
                for j in range(0,len(coeff)):
                    model = model + coeff[j]*(x[i]**j)
                res = (y[i]-model)**2
                SSres = SSres + res
            
            NormSSres = math.sqrt(SSres)/len(y)
            if NormSSres < .5:
                symbol.append(each)
                fit.append(NormSSres)
                
            time.sleep(1)
            
    return (symbol)
#    matrix = {}
#    matrix['Ticker'] = symbol
#    matrix['Norm'] = fit 
#    df = pd.DataFrame(matrix)
#    df = df.sort_values('Norm')
#    print (df)
    
def movingAverage(tickers,MAhigh,MAlow,start,end):
    SMA, LMA, name, price, spike = ([] for i in range(0,5))
    for each in tickers:        
        stock = web.DataReader(each, "google", start, end)
        close = stock['Close'].tolist()
        MAsup = sum(close[-MAhigh:])/MAhigh
        MAsub = sum(close[-MAlow:])/MAlow
        yearrange = sorted(close[-252:])
        yearlow,yearhigh = yearrange[0],yearrange[-1]
        recent = close[-1]
        changefromyearlow = (recent-yearlow)/yearlow*100 
        
        if MAsub > MAsup:
            SMA.append(MAsub)
            LMA.append(MAsup)
            name.append(each)
            price.append(recent)
            spike.append(str(changefromyearlow)+'%')
    matrix = {}
    matrix['50 DMA'] = SMA
    matrix['200 DMA'] = LMA
    matrix['Symbol'] = name
    matrix['Price'] = price
    matrix['Spike'] = spike
    
    df = pd.DataFrame(matrix)
    index = list(range(1,len(SMA)+1))
    df = df.set_index([index])
    df.to_csv('MomentumScreen.csv')
    
#--------------------------------------------------------------------------------------------------------
    
tickers = ['DOW','GE','GOOG','AAPL','VRX','MSFT','XOM','SLB','TSLA','BP','GM','F','AMAT','LRCX','TSM']

choice = int(input('Are you interested in years or days worth of data?\n 1 - years \n 2 - days\n :'))
if choice == 1:
    years = int(input('how many years worth of data are you interested in?'))
    days = 0
    months = 0
elif choice == 2:
    days = int(input('how many days worth of data are you interested in?'))
    if days >= 30:
        months = int(days/30)
        days = days%30
        years = 0
    elif days <30 and days > int(time.strftime("%d")):
        months = 1
        days = days - 30
        years = 0
    else:
        months = 0
        years = 0
else:
    print('invalid input - please run program again and follow instructions')
    sys.exit()


start = datetime.datetime(int(time.strftime("%Y"))-years,int(time.strftime("%m"))-months,int(time.strftime("%d"))-days)
end = datetime.datetime(int(time.strftime("%Y")),int(time.strftime("%m")),int(time.strftime("%d")))

power = int(input('Input maximum polynomial power:'))

high = int(input('Input long moving average period in number of days:'))
low = int(input('Input short moving average period in number of days:'))

symbols = polyfitting(tickers,power,start,end)
movingAverage(symbols,high,low,start,end)














