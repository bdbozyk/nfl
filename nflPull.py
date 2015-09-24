import os
import urllib
import re
import time
import random
import pandas


os.chdir('/home/brett/nflData/gamecenter/')

masterFrame = pandas.read_csv('/home/brett/nflData/nflGameSummary.csv')


def getter(year,week):
    year = int(year)
    week = str(week)
    
    filteredYear = masterFrame[masterFrame['YEAR']==year]
    filteredWeek = filteredYear[filteredYear['WEEK']==week]
    links = list(filteredWeek['BOXSCORE_LINK'].drop_duplicates().get_values())
    
    for link in links:       
        url = link
        stuff = url.split('/')
        nameBase = stuff[4]+'-'+stuff[6].lower()+'-'+stuff[7]
        textFileName = nameBase.lower()+'.txt'
        gameFileName = nameBase.lower()+'.pdf'   
        text = urllib.urlopen(url).read()
        key = re.findall(r'\d+',re.findall(r'<!-- gamekey :.*?-->',text)[0])[0]
        homeTeam = re.findall(r"'.*?'",re.findall(r'content=.*?/',re.findall(r"<meta id='homeTeam'.*?/>",text)[0])[0])[0].translate(None,"'")
        newLink = 'http://www.nfl.com/liveupdate/gamecenter/'+key+'/'+homeTeam+'_Gamebook.pdf'
        urllib.urlretrieve(newLink,)
        urllib.urlretrieve(newLink,gameFileName)
        f = open(textFileName,"w") 
        f.write(text)
        f.close()
        rand = random.randint(5,25)
        print nameBase+' has been saved.'
        print 'Waiting '+str(rand)+' seconds...'
        print ''
        time.sleep(rand)
    print 'Completed '+str(year)+'-'+week
        
        
getter('2015','REG2')
getter('2015','REG1')
getter('2015','PRE4')
getter('2015','PRE3')