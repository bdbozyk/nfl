import os
import urllib
import re
import pandas

os.chdir('/home/brett/nflData/')

def summary(year,week):
    year = str(year)
    week = str(week)
    url = 'http://www.nfl.com/schedules/'+year+'/'+week
    text = urllib.urlopen(url).read()
    awayTeams = re.findall(r'team-name away .*?</span>',text)
    homeTeams = re.findall(r'team-name home .*?</span>',text)
    awayScores = re.findall(r'team-score away .*?</span>',text)
    homeScores = re.findall(r'team-score home .*?</span>',text)
    links = re.findall(r'url: "http://www.nfl.com/gamecenter/.*?"',text)
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
        homeScore = re.search(r'>.*?<',homeScores[i]).group().translate(None,'><').upper()
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

years = []
# 1970-1977
#   -Reg: 14
#   -Post: 1
for year in xrange(1970,1978):
    for week in xrange(1,15):
        years.append([str(year),'REG'+str(week)])
    years.append([str(year),'POST'])
# 1978-1981
#   -Reg: 16
#   -Post: 1
for year in xrange(1978,1982):
    for week in xrange(1,17):
        years.append([str(year),'REG'+str(week)])
    years.append([str(year),'POST'])
# 1982
#   -Reg: 9
#   -Post: 1
#   -Notes: A 57 day player strike shortened the regular season.
for week in xrange(1,10):
    years.append(['1982','REG'+str(week)])
years.append(['1982','POST'])
# 1983-1986
#   -Reg: 16
#   -Post: 1
for year in xrange(1983,1987):
    for week in xrange(1,17):
        years.append([str(year),'REG'+str(week)])
    years.append([str(year),'POST'])
# 1987
#   -Reg: 15
#   -Post: 1
#   -Notes: A 24 day player strike shortened the regular season.
for week in xrange(1,16):
    years.append(['1987','REG'+str(week)])
years.append(['1987','POST'])
# 1988-1989
#   -Reg: 16
#   -Post: 1
for year in xrange(1988,1990):
    for week in xrange(1,17):
        years.append([str(year),'REG'+str(week)])
    years.append([str(year),'POST'])
# 1990-1992
#   -Reg: 17
#   -Post: 1
for year in xrange(1990,1993):
    for week in xrange(1,18):
        years.append([str(year),'REG'+str(week)])
    years.append([str(year),'POST'])
# 1993
#   -Reg: 18
#   -Post: 1
#   -Notes: Successful test of 16 games season over 17 weeks in 1990-1992 led to an
#    additional test in 1993 of 18 weeks. Teams didn't like it.
for week in xrange(1,19):
    years.append(['1993','REG'+str(week)])
years.append(['1993','POST'])
# 1994-1998
#   -Reg: 17
#   -Post: 1
for year in xrange(1994,1999):
    for week in xrange(1,18):
        years.append([str(year),'REG'+str(week)])
    years.append([str(year),'POST'])
# 1999-2010
#   -Pre: 5 (starting at 0)
#   -Reg: 17
#   -Post: 1
for year in xrange(1999,2011):
    for pre in xrange(5):
        years.append([str(year),'PRE'+str(pre)])
    for week in xrange(1,18):
        years.append([str(year),'REG'+str(week)])
    years.append([str(year),'POST'])
# 2011
#   -Pre: 4 (starting at 1)
#   -Reg: 17
#   -Post: 1
#   -Notes: No Hall of Fame Week Game for whatever reason
for pre in xrange(1,5):
    years.append(['2011','PRE'+str(pre)])
for week in xrange(1,18):
    years.append(['2011','REG'+str(week)])
years.append(['2011','POST'])
# 2012-2015
#   -Pre: 5 (starting at 0)
#   -Reg: 17
#   -Post: 1
for year in xrange(2012,2016):
    for pre in xrange(5):
        years.append([str(year),'PRE'+str(pre)])
    for week in xrange(1,18):
        years.append([str(year),'REG'+str(week)])
    years.append([str(year),'POST'])
    
masterSummary = []
for thing in years:
    masterSummary = masterSummary+summary(thing[0],thing[1])
    print thing[0],thing[1]

masterFrame = pandas.DataFrame(masterSummary)
masterFrame.columns = ['YEAR','WEEK','DATE','GAME_NUM','HOME_AWAY','TEAM','OUTCOME','PTS','BOXSCORE_LINK']

masterFrame.to_csv('nflGameSummary.csv',index=False)