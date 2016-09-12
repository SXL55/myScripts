import time
from urllib.request import urlopen
import pandas as pd
import numpy as np

stock = input('Enter ticker of interest')
sourceCode = str(urlopen('https://www.estimize.com/'+stock.upper()).read())
section1 = sourceCode.split('var parsedData = DataModel.parse(')[1]
section2 = section1.split('],"all_releases":[{')[0]
length = section1.split('"wallstreet_eps_mean":')

street_eps = []
street_revenue = []
eps = []
revenue = []
quarter = []

for i in range(2,len(length)):
    
    street_eps.append(float(section1.split('"wallstreet_eps_mean":')[i].split(',"wallstreet_eps_range"')[0]))
    street_revenue.append(int(section1.split('wallstreet_revenue_mean":')[i].split(',"wallstreet_revenue_range":')[0]))
    eps.append(section1.split(',"eps":')[i+1].split(',"revenue":')[0])
    revenue.append(section1.split(',"revenue":')[i+2].split(',"eps_flagging_range":')[0])
    quarter.append(section1.split(',"name":"')[i].split('","ticker":')[0])

matrix = {}
matrix['EPS Guess'] = street_eps
matrix['Revenue Guess'] = street_revenue 
matrix['Quarter'] = quarter
matrix['Actual Revenue'] = revenue
matrix['Actual EPS'] = eps


df = pd.DataFrame(matrix)
df = df.set_index('Quarter')
df = df[['EPS Guess','Actual EPS','Revenue Guess','Actual Revenue']]

print (df)

a = input('Press any key to exit')