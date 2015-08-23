#!/usr/bin/env python

import pandas
import os
import re
import urllib

os.chdir('/users/George/nflData/')

def standings(year,seasonType):
    if type(year) is not str:
        year = str(year)
    if seasonType not in ['REG','PRE']:
        print "seasonType must be either 'REG' or 'PRE"
    
    url = 'http://www.nfl.com/standings?category=league&season='+year+'-'+seasonType+'&split=Overall'
    html = urllib.urlopen(url).read()
    data = re.search(r'This table summarizes the NFL standings.*</table>',html,re.DOTALL).group()
    stats = re.findall(r'>.*?<',data)
    header = ['YEAR','SEASON TYPE','SEASON OUTCOME','TEAM']
    counter = 1
    for thing in stats[:20]:
        if counter == 15:
            header.append('DIV PCT')
        elif counter == 17:
            header.append('CONF PCT')
        else:
            header.append(thing.translate(None,'<>').upper())
        counter+=1
    del(stats[:20])
    data = data.translate(None,'\t\n')
    teams = re.findall(r'<td align="left.*?</td>',data)
    del(teams[0])
    dataset = []
    for i in xrange(32):
        row = [year,seasonType]
        playoff = re.search(r'>.*<a',teams[i]).group().translate(None,'><a')
        if playoff == 'z- ':
            playoff = 'CLINCHED DIVISION'
        elif playoff == '*- ':
            playoff = 'CLINCHED DIVISION AND HOME FIELD'
        elif playoff == 'y- ':
            playoff = 'CLINCHED WILDCARD'
        elif playoff == 'x- ':
            playoff = 'CLINCHED PLAYOFF'
        else:
            playoff = 'NONE'
        row.append(playoff)
        team = re.search(r'team=.*</a>',teams[i]).group()
        teamAbbrev = re.search(r'team=.*?"',team).group()[5:-1]
        teamName = re.search(r'>.*<',team).group().translate(None,'<>')
        row.append(teamAbbrev)
        row.append(teamName)
        for j in xrange(19):
            row.append(stats[i*19+j].translate(None,'<>'))
        dataset.append(row)
        
    df = pandas.DataFrame(dataset)
    df.columns = header
    
    return df


for year in xrange(2006,2015):
    if year == 2006:
        preDf = standings(year,'PRE')
    else:
        preDf = pandas.concat([preDf,standings(year,'PRE')])
    if year == 2006:
        regDf = standings(year,'REG')
    else:
        regDf = pandas.concat([regDf,standings(year,'REG')])
    print str(year)
    
regDf.to_csv('nflStandingsRegNFL.csv',index=False)
preDf.to_csv('nflStandingsPreNFL.csv',index=False)    
