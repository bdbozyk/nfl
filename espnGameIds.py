### VARIABLES NEEDED ----------------------------------------------------------
#   dataDirectory - LOCATION FOR OUTPUT DATASET(S)
#            year - YEAR FOR THE GAMEIDS
#------------------------------------------------------------------------------

### PROGRAM SUMMARY -----------------------------------------------------------
#   THIS PROGRAM TAKES THE <year>, GOES TO ESPN.COM, AND GRABS ALL THE GAMEIDS
#   FOR THAT year. IT WRITES THEM IN A TABLE WITH THE FOLLOWING:
#      {SOURCE_URL,YEAR,SEASONTYPE,WEEK,GAMEID}.
#   IT FINISHES BY WRITING THIS DATASET TO <dataDirectory> USING THE FOLLOWING
#   NAMING SCHEME:
#      <dataDirectory>/gameSummary/gameSummary_<year>.csv
#------------------------------------------------------------------------------

### VARIABLE SPECIFICATION ----------------------------------------------------
dataDirectory = ''
year = 2015
#------------------------------------------------------------------------------

import urllib
import pandas
import re
import os


os.chdir(dataDirectory)
dfs = []
keys = []
for i in xrange(1,6):
    keys.append([1,i,year])
for i in xrange(1,18):
    keys.append([2,i,year])
for i in xrange(1,6):
    keys.append([3,i,year])

for seasontype,week,year in keys:      
    url = 'http://espn.go.com/nfl/scoreboard?year='+str(year)+'&seasontype='+str(seasontype)+'&week='+str(week)
    html = urllib.urlopen(url).read()
    
    work = re.search(r'</script><script>window.espn.scoreboardData.*?{window.espn.loadType = "ready"};</script>',html).group()
    if seasontype ==  1:
        seasontype = 'PRE'
    elif seasontype == 2:
        seasontype = 'REG'
    else:
        seasontype = 'POST'   
    # get all the gameIds for the week
    gameIdsWork = re.findall(r'/boxscore\?gameId=.*?"',work)
    gameIds = []
    for gameId in gameIdsWork:
        gameIds.append(re.sub("[^0-9]","",gameId))
   
    rows = []
    for gameId in gameIds:
         rows.append([url.upper(),year,seasontype,week,gameId])
   
    if len(rows) == 0:
         print 'Did nothing for this week.'
    else:
         df = pandas.DataFrame(rows)
         df.columns = ['SOURCE','SEASON_YEAR','SEASON_TYPE','WEEK','GAME_ID']
         dfs.append(df)
         print str(year)+' '+seasontype+' '+str(week)+' is done.'
  
pandas.concat(dfs).to_csv(os.getcwd()+'/gameSummary/gameSummary_'+str(year)+'.csv',index=False)
    
    
    
    
