# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 10:19:49 2017

@author: sean-l
"""
import pandas as pd
import matplotlib.pyplot as plt
import datetime


def checkrecipelength(recipelist,data):
    for each in recipelist:
        recipedata = data[data.RecipePath == each]
        print (len(recipedata))
        print (each)
        print ('\n')
        
def stagecheck(diespot):
    
    y1,y2,rof = [],[],[]
    for i in range (0,len(diespot)):
        y1.append(int(diespot['MpointX'][i]))
        y2.append(int(diespot['MpointY'][i]))
        rof.append(float(diespot['ROF'][i])*10000)
    
    x = list(range(0,len(y1)))
    plt.figure(figsize = (10,6))
    plt.scatter(y1,rof,c = 'g')
    plt.ylabel('ROF')
    plt.xlabel('X Stage Location')
    plt.title('X Stage v.s. ROF')
    plt.grid()
    plt.show()
    plt.figure(figsize = (10,6))
    plt.scatter(y2,rof,c = 'r')
    plt.ylabel('ROF')
    plt.xlabel('Y Stage Location')
    plt.title('Y Stage v.s. ROF')
    plt.grid()
    plt.show()
    plt.figure(figsize = (10,6))
    plt.plot(x,y1,'g')
    plt.ylabel('X Stage')
    plt.title('X Stage Variation')
    plt.grid()
    plt.show()
    plt.figure(figsize = (10,6))
    plt.plot(x,y2,'r')
    plt.ylabel('Y Stage')
    plt.title('Y Stage Variation')
    plt.grid()
    plt.show()

def processvariation(delta):
    x = delta['DateTime'].tolist()
    y = delta['L1S0'].tolist()
    z = delta['ROF'].tolist()
    
    colorbar = 'ROF'
    plt.figure(figsize = (15,9))
    plt.grid()
    plt.axis('auto')
    plt.title(colorbar)
    plt.ylabel('Thickness')
    plt.xlabel('Time')
    plt.scatter(x[:110],y[:110],c = z[:110])
    
    for i in range(len(delta[:110])):
        plt.annotate(z[i],(x[i],y[i]),(x[i],y[i]+25)) 
    plt.show()
    
    plt.figure(figsize = (15,9))
    plt.grid()
    plt.axis('auto')
    plt.title(colorbar)
    plt.xlabel('Time')
    plt.ylabel('Thickness')
    plt.scatter(x[130:],y[130:],c = z[130:])
#    for i in range(len(delta[130:])):
#        plt.annotate(z[i],(x[i],y[i]),(x[i],y[i]+25))

def wafervariation(recipedata):
    for j in range(1,14):
        #select die spot
        dienumber = j
        diespot = recipedata[recipedata.Die_Spot == str(dienumber)]
        index = list(range(0,len(diespot)))
        diespot.index = index
        #select die spot
        
        l1s,l2s,rof = [],[],[]
        for i in range (0,len(diespot)):
            l1s.append(float(diespot['L1S0'][i]))
            l2s.append(float(diespot['L2S0'][i]))
            rof.append(float(diespot['ROF'][i])*10000)
        results = {}
        results['L1SO'] = l1s
        results['L2SO'] = l2s
        results['ROF'] = rof
        results = pd.DataFrame(results)
        results.index = diespot['WaferID'].tolist()
        results['L1SO'].plot(kind='line',style = 'b',figsize=(10,6),grid = True,legend=True,secondary_y=False)
        plt.ylabel('Thickness L1SO')
        plt.xlabel('Wafer ID')
        results['ROF'].plot(kind='line',style = 'y--',figsize=(10,6),grid = True,legend=True,secondary_y=True)
        plt.title('L1SO and ROF Die Number : '+str(dienumber))
        plt.ylabel('ROF')       
        plt.show()
        plt.clf()
        
        results['L2SO'].plot(kind='line',style = 'k',figsize=(10,6),grid = True,legend=True,secondary_y=False)
        plt.ylabel('Thickness L2SO')
        plt.xlabel('Wafer ID')
        results['ROF'].plot(kind='line',style = 'r--',figsize=(10,6),grid = True,legend=True,secondary_y=True)
        plt.title('L12O and ROF Die Number : '+str(dienumber))
        plt.ylabel('ROF')       
        plt.show()
        plt.clf()
        
def thicknessmapping(recipedata):
    wafers = list(set(recipedata['WaferID']))
    alldata = pd.DataFrame()
    for each in wafers:
        alldata[each] = ''
        y = []
        waferdata = recipedata[recipedata.WaferID == each]
        index = list(range(0,len(waferdata)))
        waferdata.index = index
        for i in range(0,len(waferdata)):
            slotnumber = waferdata[waferdata.Die_Spot == str(i+1)]
            y.append(float(slotnumber['L1S0'][i]))
        alldata[each] = y
    for each in alldata.columns:
        alldata[each].plot(kind='line',figsize=(15,9),grid = True,legend=True)
    plt.ylabel('L1S0 Thickness')
    plt.xlabel('Die Spot')
    plt.title('Thickness Variation v.s. Die Spot')

def waferthicknessmap(recipedata):
    wafers = list(set(recipedata['WaferID']))

    for each in wafers:    
        x,y = [],[]
        waferdata = recipedata[recipedata.WaferID == each]
        index = list(range(0,len(waferdata)))
        waferdata.index = index
        x = waferdata['MpointX'].tolist()
        y = waferdata['MpointY'].tolist()
        z = waferdata['L1S0'].tolist()
        plt.figure(figsize = (15,9))
        plt.xlabel('X Stage Position')
        plt.ylabel('Y Stage Position')
        plt.grid()
        plt.title(each+' Thickness Color Map')
        plt.scatter(x,y,c=z,s=100)
        for i in range(len(waferdata)):
            plt.annotate(round(z[i],2),(x[i],y[i]),(x[i]+1300,y[i]+500))    
        plt.show()
    
def waferrofmap(recipedata):
    wafers = list(set(recipedata['WaferID']))

    for each in wafers:    
        x,y = [],[]
        waferdata = recipedata[recipedata.WaferID == each]
        index = list(range(0,len(waferdata)))
        waferdata.index = index
        x = waferdata['MpointX'].tolist()
        y = waferdata['MpointY'].tolist()
        z = waferdata['ROF'].tolist()
        plt.figure(figsize = (15,9))
        plt.xlabel('X Stage Position')
        plt.ylabel('Y Stage Position')
        plt.grid()
        plt.title(each+' ROF Color Map')
        plt.scatter(x,y,c=z,s=100)
        for i in range(len(waferdata)):
            plt.annotate(z[i],(x[i],y[i]),(x[i]+1300,y[i]+500))    
        plt.show()

def waferdiemap(recipedata):
    wafers = list(set(recipedata['WaferID']))

    for each in wafers:    
        x,y = [],[]
        waferdata = recipedata[recipedata.WaferID == each]
        index = list(range(0,len(waferdata)))
        waferdata.index = index
        x = waferdata['MpointX'].tolist()
        y = waferdata['MpointY'].tolist()
        z = waferdata['Die_Spot'].tolist()
        plt.figure(figsize = (15,9))
        plt.xlabel('X Stage Position')
        plt.ylabel('Y Stage Position')
        plt.grid()
        plt.title(each+' Die Map')
        plt.scatter(x,y,s=100)
        for i in range(len(waferdata)):
            plt.annotate(z[i],(x[i],y[i]),(x[i]+1300,y[i]+500))    
        plt.show()
    
##############################################################################
############################ RECIPE EXTRACTION ###############################
##############################################################################
    
data = pd.read_csv('rawdata.csv')
data = data[data.Slot != 'Slot']

recipelist = data['RecipePath']
recipelist = set(recipelist)
prerecipe, postrecipe = [],[]

for each in recipelist:
    if each[-3::] == 'PRE':
        prerecipe.append(each)
    elif each[-3::] == 'OST':
        postrecipe.append(each)
        
##############################################################################

##############################################################################
##############################################################################
# input recipe path 
premeasure = 'RBR\PHNX\M78G\PHNXM78GILD1_PRE'
postmeasure = 'RBR\PHNX\M78G\PHNXM78GILD1_POST'
# input recipe path
##############################################################################
##############################################################################

post = data[data.RecipePath == postmeasure]
pre = data[data.RecipePath == premeasure]
x = list(range(0,len(post)))
post.index = x
pre.index = x
delta = pd.DataFrame()
l1s0,l2s0,xstage,ystage,slot,date = [],[],[],[],[],[]

for i in range(0,len(post)):
    l1s0.append(float(pre['L1S0'][i])-float(post['L1S0'][i]))
    l2s0.append(float(pre['L2S0'][i])-float(post['L2S0'][i]))
    xstage.append(int(post['MpointX'][i]))
    ystage.append(int(post['MpointY'][i]))
    slot.append(int(post['Slot'][i]))
    day = post['DateTime'][i].split(' ')[0].split('/')
    time = post['DateTime'][i].split(' ')[1].split(':')
    date.append(datetime.datetime(int(day[2]),int(day[0]),int(day[1]),int(time[0]),int(time[1])))
    
delta = pd.DataFrame()
delta['L1S0'] = l1s0
delta['L2S0'] = l2s0
delta['ROF'] = post['ROF']
delta['Die_Spot'] = post['Die_Spot']
delta['MpointX'] = xstage
delta['MpointY'] = ystage
delta['WaferID'] = pre['WaferID']
delta['Slot'] = slot
delta['DateTime'] = date
     
######################################################################
################ SELECT DATA TO BE ANALYZED ##########################
######################################################################
#recipedata can be delta / post / pre
recipedata = delta
#recipedata can be delta / post / pre
######################################################################
######################################################################

dienumber = 10
diespot = recipedata[recipedata.Die_Spot == str(dienumber)]
index = list(range(0,len(diespot)))
diespot.index = index
       
#stagecheck(diespot)

#wafervariation(recipedata)
#thicknessmapping(recipedata)
waferthicknessmap(recipedata)
#waferrofmap(recipedata)
#processvariation(delta)
#waferdiemap(recipedata)

    


