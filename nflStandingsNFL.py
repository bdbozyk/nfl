#!/usr/bin/env python

import pandas
import os
import re
import urllib

os.chdir('/home/bdbozyk/nflData/')

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
    
regDf.to_csv('nflStandingsRegNFL.csv')
preDf.to_csv('nflStandingsPreNFL.csv')    

#regDf[['W','L','T','NET PTS']] = regDf[['W','L','T','NET PTS']].astype(int)
#preDf[['W','L','T','NET PTS']] = preDf[['W','L','T','NET PTS']].astype(int)


#regDf['AVG REG NEG PTS GAME'] = regDf['NET PTS']/(regDf['W']+regDf['L']+regDf['T'])
#preDf['AVG PRE NEG PTS GAME'] = preDf['NET PTS']/(preDf['W']+preDf['L']+preDf['T'])
    
    
#import numpy as np
#prePts = preDf[['YEAR','TEAM','AVG PRE NEG PTS GAME']]
#regPts = regDf[['YEAR','TEAM','AVG REG NEG PTS GAME','SEASON OUTCOME']]
#regPts['PLAYOFFS'] = np.where(regPts['SEASON OUTCOME']=='NONE',tuple((31/270.,119/270.,180/270.)),tuple(((255/270.,127/270.,14/270.))))

#tabColors = []
#colors = regPts[['PLAYOFFS']].get_values()
#for color in colors:
#    if color == 0:
#        tabColors.append( (31/270.,119/270.,180/270.))
#    else:
#        tabColors.append((255/270.,127/270.,14/270.))

#pts = pandas.merge(left = prePts, right = regPts, on = ['YEAR','TEAM'])
#pts.columns = ['YEAR','TEAM','AVG NET PRE PTS GAME','AVG NET REG PTS GAME','SEASON OUTCOME','PLAYOFFS']

#import matplotlib.pyplot as plt
#plt.style.use('ggplot')
 
#x = pts[['AVG NET PRE PTS GAME']]
#y = pts[['AVG NET REG PTS GAME']]
#color = pts[['PLAYOFFS']].get_values()


#plt.scatter(x, y, s = 50,c=[(31,119,180),(255,127,14)])

#tableau10 = [
#[31,119,180],
#[255,127,14],
#[44,160,44],
#[214,39,40],
#[148,103,189],
#[140,86,75],
#[227,119,194],
#[127,127,127],
#[188,189,34],
#[23,190,207]

#]
