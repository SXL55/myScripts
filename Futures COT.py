import pandas as pd
import time
import matplotlib.pyplot as plt
import quandl
import pandas_datareader.data as web
import sys
import matplotlib
matplotlib.rcParams.update({'font.size': 10})

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


start = str(int(time.strftime("%Y"))-years)+'-'+str(int(time.strftime("%m"))-months)+'-'+str(int(time.strftime("%d"))-days)
end = time.strftime("%Y")+'-'+time.strftime("%m")+'-'+time.strftime("%d")

datasets = {}
datasets['S&P 500 VIX Futures'] = ['CFTC/VX_F_ALL','CBOE/VIX.4','VIX Index']
datasets['S&P 500 Futures'] = ['CFTC/SPC_F_ALL','YAHOO/INDEX_GSPC.4','S&P 500 Index']
datasets['Gold Futures'] = ['CFTC/GC_F_ALL','LBMA/GOLD.2','Gold Spot Price ($)']
datasets['Crude Futures'] = ['CFTC/WS_F_ALL','YAHOO/XL.6','XLE Energy ETF ($)']
datasets['Silver Futures'] = ['CFTC/SI_F_ALL','LBMA/SILVER','Silver Spot Price ($)']

econData = pd.Series(datasets)

print ("Please select a series from the list")
n = 1
for i in range(0,len(econData.index)):
    print ('Enter %d for %s' %(n,econData.index[n-1]))
    n = n+1
selection = int(input(':'))

df = quandl.get([econData[selection-1][0],econData[selection-1][1]], trim_start = start, trim_end = end, authtoken="X4PkMnh9pzNV_h_ixxn4")
if df.index[0] > df.index[1]:
    df1 = df.loc[::-1]
else:
    df1 = df

df1 = df1.dropna()
x = 1
for i in range(0,len(df1.columns)-1):
    print ('Enter %d for %s' %(x,df1.columns[x-1].split('-')[1]))
    x = x+1
choice1 = int(input('First Selection:'))
choice2 = int(input('Second Selection (enter 0 for no selection):'))
plot1 = df1[df1.columns[choice1-1]]

if choice2 == 0:
    plot2 = 0
else:
    plot2 = df1[df1.columns[choice2-1]]

plot3 = df1[df1.columns[-1]]
    
plot1.rename(df1.columns[choice1-1].split('-')[1]).plot(kind = 'line', style = 'b',figsize = (10,6),grid = True,legend=True)
plt.ylabel('Futures Contracts')

if choice2 == 0:
    plot2 = 0
else:
    plot2.rename(df1.columns[choice2-1].split('-')[1]).plot(kind = 'line', style = 'm',figsize = (10,6),grid = True,legend=True)

plot3.rename(df1.columns[-1].split('-')[1]).plot(kind = 'line', style = 'g',figsize = (10,6),grid = True,secondary_y = True,legend=True)
plt.ylabel(econData[selection-1][2])
plt.title(econData.index[selection-1])
#plt.savefig(econData.index[selection-1])
plt.show()

