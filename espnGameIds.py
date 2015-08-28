import urllib
import pandas
import re
import os

os.chdir('/)


dfs = []
year = 2014
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
        gameIds.append(re.sub("[^0-9]","",gameId))
    # get all the total scores
    totalScoresWork = re.findall(r'"score":".*?"',work)
    totalScores = []
    for totalScore in totalScoresWork:
        totalScores.append(re.sub("[^0-9]","",totalScore))
    # get all the team names
    teamsWork = re.findall(r'shortDisplayName":".*?"',work)
    teams = []
    for team in teamsWork:
        teams.append(team[19:-1])
    # get all the scores by quarter
    scoresWork = re.findall(r'"linescores":\[.*?\]',work)
    scores = []
    for score in scoresWork:
        qtrsWork = re.findall(r'"value":.*?}',score)
        qtrs = []
        for qtr in qtrsWork:
            qtrs.append(re.sub(r'[^0-9]',"",qtr))
        if len(qtrs) == 4:
            qtrs.append('0')
        scores.append(qtrs)
    rows = []
    for i in range(len(gameIds)):
        rows.append([year,seasontype,week,gameIds[i],teams[i],totalScores[i],scores[i][0],scores[i][1],scores[i][2],scores[i][3],scores[i][4]])
    if len(rows) == 0:
        print 'Did nothing for this week.'
    else:
        df = pandas.DataFrame(rows)
        df.columns = ['SEASON_YEAR','SEASON_TYPE','WEEK','ESPN_GAME_ID','TEAM','TOTAL_PTS','Q1_PTS','Q2_PTS','Q3_PTS','Q4_PTS','OT_PTS']
        dfs.append(df)
        print str(year)+' '+seasontype+' '+str(week)+' is done.'
  
    
    
    
    
