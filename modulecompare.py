# -*- coding: utf-8 -*-
"""
Created on Wed Mar  1 18:46:06 2017

@author: sean-l
"""

import xml.etree.ElementTree as ET
import pandas as pd
import os

def printxml(child):
    
    for ModuleType in child.getchildren():
        print(ModuleType.attrib['Name'])
        for i in range(0,len(ModuleType)):
            base = '  '+ ModuleType[i].attrib['Name']
            try:
                pair = ': '+ ModuleType[i][0].text
            except:
                pair = ':'
            print(base+pair)
            for Field in ModuleType[i][0]:
                key = '    '+list(Field.attrib.values())[0]
                try:
                    value = ': '+Field[0].text
                except:
                    value = ':'
                print(key+value)
                for Field2 in Field[0]:
                    horse = '    '+list(Field2.attrib.values())[0]
                    carriage = ': '+Field2[0].text
                    print(horse+carriage)

def createIND(child,modulename):
    
    parameter = []  
    for ModuleType in child.getchildren():
        if ModuleType.attrib['Name'] == modulename:
            parameter.append(ModuleType.attrib['Name'])
            for i in range(0,len(ModuleType)):
                base = '    '+ ModuleType[i].attrib['Name']
                parameter.append(base)
                for Field in ModuleType[i][0]:
                    key = '    -- '+list(Field.attrib.values())[0]
                    parameter.append(key)
                    for Field2 in Field[0]:
                        horse = '      '+list(Field2.attrib.values())[0]
                        parameter.append(horse)
    return(parameter)

files = os.listdir()
files.remove('modulecompare.py')

alldata = []

for each in files:
    modulename = 'XenonLamp'
    tree = ET.parse(each)
    toolID = ('CA'+each[0:2]+'0'+each[2])
    root = tree.getroot()
    child = root[0]
    indices = createIND(child,modulename)
    tablevalues = []
    for ModuleType in child.getchildren():
        if ModuleType.attrib['Name'] == modulename:
            tablevalues.append('')
            for i in range(0,len(ModuleType)):
                try:
                    pair = (ModuleType[i][0].text)
                except:
                    pair = ''
                tablevalues.append(pair)
                for Field in ModuleType[i][0]:
                    try:
                        value = (Field[0].text)
                    except:
                        value = ''
                    tablevalues.append(value)
                    for Field2 in Field[0]:
                        carriage = (Field2[0].text)
                        tablevalues.append(carriage)
            series = tablevalues
            data = pd.Series(series)
            data = data.rename(toolID)
            data.index = indices
            alldata.append(data)
length = []
alldata.sort(key=len)
for each in alldata:
    length.append(len(each))
length = pd.Series(length)
    
lower = 0
upper = 27
results = alldata[lower]
check = []
for i in range(lower,upper):
    for j in range(0,len(alldata[i])):
        if alldata[i].index[j] == results.index[j]:
            check.append('yes')
        else:
            check.append('no')
try:
    check.index('no')
except:
    print ('Index Match Passed')

         
results = pd.DataFrame()
for i in range(lower,upper):
    results[alldata[i].name]=alldata[i]

rows = results.values.tolist()
results['Flag'] = ''
for i in range(0,len(rows)):
    flag = len(set(rows[i]))
    if flag > 1:
        results['Flag'][i] = 'flag'
            
results.to_excel(modulename+'.xls')
