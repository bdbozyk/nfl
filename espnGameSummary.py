import urllib
import re
import pandas
import os

os.chdir('/Users/George/espnNFL/')

os.getcwd()

url = 'http://espn.go.com/nfl/playbyplay?gameId=400554214&period=0'
html = urllib.urlopen(url).readlines()

for line in html:
    if 'game-time-location' in line:
        gameTimeLocation = line
    if '<tr><td class="team"' in line:
        scoreSummary = line
    if 'Top Performers' in line:
        topPerformers = line
    if '<!-- treat=0 -->' in line:
        playByPlay = line
        
        
        
        
gameId = '400554232'
url = 'http://scores.espn.go.com/nfl/boxscore?gameId='+gameId
html = urllib.urlopen(url).read()
work = re.search('<!-- SETTINGS: boxscore.*?<!-- begin sp links -->',html,re.DOTALL).group()

#------------------------------------------------------------------------------
## SCORING SUMMARY START
#------------------------------------------------------------------------------
q1 = re.search(r'FIRST QUARTER.*?SECOND QUARTER',work,re.DOTALL).group()
q2 = re.search(r'SECOND QUARTER.*?THIRD QUARTER',work,re.DOTALL).group()
q3 = re.search(r'THIRD QUARTER.*?FOURTH QUARTER',work,re.DOTALL).group()
quarters = [['1',q1],['2',q2],['3',q3]]
q4 = re.search(r'FOURTH QUARTER.*?Team Stat Comparison',work,re.DOTALL).group()
if 'OVERTIME' in q4:
    q4 = re.search(r'FOURTH QUARTER.*?OVERTIME',q4,re.DOTALL).group()
    ot = re.search(r'OVERTIME.*?Team Stat Comparison',work,re.DOTALL).group()
    quarters.append(['4',q4])
    quarters.append(['5',ot])
else:
    quarters.append(['4',q4])
rows = []
for label,quarter in quarters:
    # Determine the type of scoring
    scoreTypesWork = re.findall('"width: 15px;">.*?</td>',quarter)
    scoreTypes = []
    for scoreType in scoreTypesWork:
        scoreTypes.append(re.search('>.*?<',scoreType).group().translate(None,'><').upper())
    # Determine the teams playing
    teamsWork = re.findall('"width:30px;">.*?</th>',quarter)
    teams = []
    for team in teamsWork:
        teams.append(re.search('>.*?<',team).group().translate(None,'><').upper())
    # Determine the score descriptions
    scoreDescsWork = re.findall('"text-align:left;">.*?<div',quarter)
    scoreDescs = []
    for scoreDesc in scoreDescsWork:
        scoreDescs.append(re.search('>.*?<',scoreDesc).group().translate(None,'><').upper())
    # Determine the score times
    scoreTimesWork = re.findall('"center">.*?</td>',quarter)
    scoreTimes = []
    for scoreTime in scoreTimesWork:
        scoreTimes.append(re.search('>.*?<',scoreTime).group().translate(None,'><'))
    # Determine drive Summaries
    driveSummariesWork = re.findall('"font-style:italic;">.*?</div>',quarter)
    driveSummaries = []
    for driveSummary in driveSummariesWork:
        driveSummaries.append(re.sub(',',' -',re.search('>.*?<',driveSummary).group().translate(None,'><')[12:].upper()))
    # Determine the home and away scores
    scoresWork = re.findall(r'"font-size: 12px;">.*?</td>',quarter)
    awayScores = []
    homeScores = []
    i=0
    for score in scoresWork:
        if i%2 == 0:
            awayScores.append(re.search('>.*?<',score).group().translate(None,'><'))
        else:
            homeScores.append(re.search('>.*?<',score).group().translate(None,'><'))
        i+=1
    # Determine which team scored
    scoreTeamsWork = re.findall('alt=".*?"/>',quarter)
    scoreTeams = []
    for scoreTeam in scoreTeamsWork:
        scoreTeams.append(re.search('".*?"',scoreTeam).group().translate(None,'"').upper())      
    # Now we have the following fields
    #  1.scoreTypes
    #  2.teams
    #  3.scoreDescs
    #  4.scoreTimes
    #  5.driveSummaries
    #  6.awayScores
    #  7.homeScores
    #  8.scoreTeams
    for i in xrange(len(scoreTypes)):
        rows.append([gameId,label,scoreTypes[i],scoreTimes[i],scoreTeams[i],scoreDescs[i],driveSummaries[i],teams[0],teams[1],awayScores[i],homeScores[i]])
        
scoringSummary = pandas.DataFrame(rows)
scoringSummary.columns = ['GAME_ID','QUARTER','SCORE_TYPE','SCORE_TIME','SCORE_TEAM','SCORE_DESC','DRIVE_SUMMARY','AWAY_TEAM','HOME_TEAM','AWAY_SCORE','HOME_SCORE']     
scoringSummary.to_csv(os.getcwd()+'/scoringSummary/scoringSummary_'+gameId+'.csv',index=False)
#------------------------------------------------------------------------------
## SCORING SUMMARY END
#------------------------------------------------------------------------------



#------------------------------------------------------------------------------
## TEAM STAT COMPARISON START
#------------------------------------------------------------------------------
teamStatComparison = re.search(r'Team Stat Comparison.*?Helvetica,Arial,sans-serif',work).group()



teamsWork = re.findall(r'"float:right;">.*?</div>',teamStatComparison)
teams = []
for team in teamsWork:
    teams.append(re.search('>.*?<',team).group().translate(None,'><').upper())  
    
statsWork = re.findall('</td><td>.*?</td></tr>',teamStatComparison)

stats = []
for stat in statsWork:
    stats.append(re.sub('</td><td>','|',stat[9:-10]).split('|'))
    
firstDowns = stats[0]
passingFirstDowns = stats[1]
rushingFirstDowns = stats[2]
penaltyFirstDowns = stats[3]
thirdDowns = []
for thing in stats[4]:
    thirdDowns.append(thing.split('-'))
fourthDowns = []
for thing in stats[5]:
    fourthDowns.append(thing.split('-'))
totalPlays = stats[6]
totalYards = stats[7]
yardsPerPlay = stats[8]
totalDrives = stats[9]
passingYards = stats[10]
passing = []
for thing in stats[11]:
    passing.append(thing.split('-'))
yardsPerPass = stats[12]
interceptions = stats[13]
sacksYardsLost = []
for thing in stats[14]:
    sacksYardsLost.append(thing.split('-'))
rushingYards = stats[15]
rushingAttempts = stats[16]
yardsPerRush = stats[17]
redZone = []
for thing in stats[18]:
    redZone.append(thing.split('-'))
penalties = []
for thing in stats[19]:
    penalties.append(thing.split('-'))
turnovers = stats[20]
fumblesLost = stats[21]
defensiveSpecialTeamsTDs = stats[23]
timeOfPossession = stats[24]

rows = []
for i in xrange(2):
    rows.append([gameId,teams[i],firstDowns[i],passingFirstDowns[i],rushingFirstDowns[i],penaltyFirstDowns[i],thirdDowns[i][0],thirdDowns[i][1],fourthDowns[i][0],fourthDowns[i][1],totalPlays[i],totalYards[i],yardsPerPlay[i],totalDrives[i],passingYards[i],passing[i][0],passing[i][1],yardsPerPass[i],interceptions[i],sacksYardsLost[i][0],sacksYardsLost[i][1],rushingYards[i],rushingAttempts[i],yardsPerRush[i],redZone[i][0],redZone[i][1],penalties[i][0],penalties[i][1],turnovers[i],fumblesLost[i],defensiveSpecialTeamsTDs[i],timeOfPossession[i]])


teamStatComparison = pandas.DataFrame(rows).reset_index()
teamStatComparison.columns = ['HOME_FG','GAME_ID','TEAM','FIRST_DOWNS','PASSING_FIRST_DOWNS','RUSHING_FIRST_DOWNS','PENALTY_FIRST_DOWNS','THIRD_DOWNS_ATTEMPTED','THIRD_DOWNS_CONVERTED','FOURTH_DOWNS_ATTEMPTED','FOURTH_DOWNS_CONVERTED','TOTAL_PLAYS','TOTAL_YARDS','YARDS_PER_PLAY','TOTAL_DRIVES','PASSING_YARDS','PASSES_ATTEMPTED','PASSES_COMPLETED','YARDS_PER_PASS','INTERCEPTIONS_THROWN','SACKS','SACKS_YARDS_LOST','RUSHING_YARDS','RUSHES_ATTEMPTED','YARDS_PER_RUSH','RED_ZONE_SCORES','RED_ZONE_ATTEMPTED','PENALTIES','PENALTY_YARDS','TURNOVERS','FUMBLES_LOST','DEF_ST_TDS','TIME_OF_POSSESSION']
teamStatComparison.to_csv(os.getcwd()+'/teamStatComparison/teamStatComparison_'+gameId+'.csv',index=False)










