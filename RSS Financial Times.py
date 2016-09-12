import feedparser
import string
import pandas as pd

comment = {}
sector = {}
world = {}
comcur = {}
comment['FTAlphaville'] = 'http://ftalphaville.ft.com//feed/'
world['Home Page']= 'http://www.ft.com/rss/home/us'
sector['Aerospace Defense']= 'http://www.ft.com/rss/companies/aerospace-defence'
sector['Automobiles']= 'http://www.ft.com/rss/companies/automobiles'
sector['Chemicals'] = 'http://www.ft.com/rss/companies/chemicals'
sector['Energy'] = 'http://www.ft.com/rss/companies/energy'
sector['Industrials'] = 'http://www.ft.com/rss/companies/industrials'
sector['Oil and Gas'] = 'http://www.ft.com/rss/companies/oil-gas'
sector['Mining'] = 'http://www.ft.com/rss/companies/mining'
sector['Pharamceuticals'] = 'http://www.ft.com/rss/companies/pharmaceuticals'
sector['Technology'] = 'http://www.ft.com/rss/companies/technology'
world['China'] = 'http://www.ft.com/rss/world/asia-pacific/china'
world['American Politics'] = 'http://www.ft.com/rss/world/americas/politics'
world['Europe'] = 'http://www.ft.com/rss/world/europe'
world['Middle East'] = 'http://www.ft.com/rss/world/mideast/politics'
comment['Lex Column'] = 'http://www.ft.com/rss/lex'
comcur['Commodities'] = 'http://www.ft.com/rss/markets/commodities'
comcur['Currencies'] = 'http://www.ft.com/rss/markets/currencies'

open('RSSfeed.txt','w').close()
text = open('RSSfeed.txt','w')

print ("Please select a topic of interest")
print ('Enter 1 for Sector News')
print ('Enter 2 for World News')
print ('Enter 3 for Commodities or Currencies')
print ('Enter 4 for Commentary and Analysis')
print ('Enter 5 for all')
choice = int(input(':'))

def RSSReader(sector):

    RSSFeeds = pd.Series(sector)
    for i in range(0,len(sector)):
        print ('Select %d for %s:' %(i+1,RSSFeeds.index[i]))
    print ('Select 0 for keyword search:')
    key = int(input(':'))
    if key != 0:
        d = feedparser.parse(RSSFeeds[key-1])
        for i in range(0,len(d.entries)):
            text.write('\n|---'+ d.entries[i].title+'----|\n')
            text.write('\n\t'+ d.entries[i].summary + '\n')
            #text.write('\n'+ d.entries[i].links[0]['href'] + '\n')
    else:
        keyword = input('Please enter keyword:')
        for eachfeed in RSSFeeds:
            d = feedparser.parse(eachfeed)
            for i in range(0,len(d.entries)):
                rss = d.entries[i].title.lower()
                summary = d.entries[i].summary.lower()
                if rss.find(keyword.lower()) != -1 or summary.find(keyword.lower()) != -1:   
                    text.write('\n|----'+ d.entries[i].title+'----|\n')
                    text.write('\n\t\t'+ d.entries[i].summary + '\n')
                    #text.write('\n'+ d.entries[i].links[0]['href'] + '\n')

if choice == 1:
    RSSReader(sector)
elif choice == 2:
    RSSReader(world)
elif choice == 3:
    RSSReader(comcur)
elif choice == 4:
    RSSReader(comment)
elif choice ==5:
    ndic = dict(list(world.items()) + list(comment.items()) +list(comcur.items()) + list(sector.items()))
    RSSReader(ndic)
else:
    print ('Invalid Selection, please run program again')
    

            
            

#keyword = input('Please enter keyword of interest:')
#

#
#for eachfeed in feed:
#    d = feedparser.parse(eachfeed)    
#    for i in range(0,len(d.entries)):
#        rss = d.entries[i].title.lower()
#        if rss.find(keyword.lower()) != -1:    
#            text.write('\n----'+ d.entries[i].title+'----\n')
#            text.write('\n'+ d.entries[i].summary + '\n')
#
text.close()
