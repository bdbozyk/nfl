import os
import urllib
import re

os.getcwd()




def summary(year,week):
    year = str(year)
    week = str(week)
    url = 'http://www.nfl.com/schedules/'+year+'/'+week
    text = urllib.urlopen(url).read()
    games = re.search(r'<!-- gameTablesList: 1 -->.*?<!-- satelliteList in table:  -->',text,re.DOTALL).group()
    awayTeams = re.findall(r'team-name away .*?</span>',games)
    homeTeams = re.findall(r'team-name home .*?</span>',games)
    awayScores = re.findall(r'team-score away .*?</span>',games)
    homeScores = re.findall(r'team-score home .*?</span>',games)
    links = re.findall(r'url: "http://www.nfl.com/gamecenter/.*?"',games)
    if len(homeScores) == 0:
        for dummy in xrange(len(links)):
            homeScores.append('>-1<')
    if len(awayScores) == 0:
        for dummy in xrange(len(links)):
            awayScores.append('>-<')
    rows = []
    for i in xrange(len(links)):
        link = links[i][6:-1]
        work = link.split('/')
        date = work[4][4:6]+'-'+work[4][6:-2]+'-'+work[4][:4]
        gameNum = work[4][-2:]
        year = work[5]
        week = work[6]
        homeTeam = re.search(r'>.*?<',homeTeams[i]).group().translate(None,'><').upper()
        awayTeam = re.search(r'>.*?<',awayTeams[i]).group().translate(None,'><').upper()
   http://www.kcchiefs.com/     homeScore = re.search(r'>.*?<',homeScores[i]).group().translate(None,'><').upper()
        awayScore = re.search(r'>.*?<',awayScores[i]).group().translate(None,'><').upper()    
        if awayScore == '?' or homeScore == '?':
            awayOut = '?'
            homeOut = '?'
        elif int(awayScore)>int(homeScore):
            awayOut = 'W'
            homeOut = 'L'
        elif int(awayScore)<int(homeScore):
            awayOut = 'L'
            homeOut = 'W'
        elif int(awayScore)==int(homeScore):
            awayOut = 'T'
            homeOut = 'T'
        else:
            awayOut = '?'
            homeOut = '?'
        awayRow = [year,week,date,gameNum,'AWAY',awayTeam,awayOut,awayScore,link]
        homeRow = [year,week,date,gameNum,'HOME',homeTeam,homeOut,homeScore,link]
        rows.append(awayRow)
        rows.append(homeRow)
    return rows


#1970 Reg   
