import urllib
import re
import pandas
import os

os.chdir('/home/brett/espnNFL/')
os.getcwd()

gameId = '400554213'
url = 'http://scores.espn.go.com/nfl/boxscore?gameId='+gameId
html = urllib.urlopen(url).read()
work = re.search(r'gamepackage-box-score".*?</div></div></div></article>',html,re.DOTALL).group()
strings = work.split('combiner')

###-------------------------------------------------------------------------###
###   START OF THE TEAM SUMMARY   ------------------------------------------###
###-------------------------------------------------------------------------###
string0 = strings[0]
junk = re.findall(r'>.*?<',string0)
teams = []
for team in junk:
    temp = team.translate(None,'><')
    if temp not in ['','Overview']:
        teams.append(temp.upper())

###-------------------------------------------------------------------------###
###   START OF AWAY PASSING   ----------------------------------------------###
###-------------------------------------------------------------------------###
string1 = strings[1]
junk = re.findall(r'>.*?<',string1)
junk2 = []
for thing in junk:
    temp = thing.translate(None,'><')
    if temp != '':
        junk2.append(temp.upper())
del(junk2[:9],junk2[-9:])
junk3 = []
counter = 1
for thing in junk2:
    if (counter - 2)%9 == 0:
        temp = thing.split('/')
        junk3.append(temp[0])
        junk3.append(temp[1])
    elif (counter - 7)%9 == 0:
        temp = thing.split('-')
        junk3.append(temp[0])
        junk3.append(temp[1])
    else:
        junk3.append(thing)
    counter += 1
rows = []
for i in xrange(int(len(junk3)/11.)):
    rows.append(junk3[i*11:(i+1)*11])
awayPassingFrame = pandas.DataFrame(rows)
awayPassingFrame.columns = ['PLAYER','PASS_COMPLETIONS','PASS_ATTEMPTS','YDS','AVG_YDS_PASS','TD','INT','SACKS','SACKS_YDS_LOST','QBR','RTG']
junk4 = re.findall(r'id/.*?<',string1)
rows = []
for thing in junk4:
    temp = thing.split('"')
    rows.append([re.sub('[^0-9]','',temp[0]),temp[1].translate(None,'><').upper()])
playerFrame = pandas.DataFrame(rows)
playerFrame.columns = ['PLAYER_ID','PLAYER']
playerFrame['GAME_ID'] = gameId
playerFrame['HOME_FG'] = 0
awayPassing = pandas.merge(left = playerFrame, right = awayPassingFrame, on = 'PLAYER')
awayPassing = awayPassing[['GAME_ID','PLAYER_ID','PLAYER','HOME_FG','PASS_COMPLETIONS','PASS_ATTEMPTS','YDS','AVG_YDS_PASS','TD','INT','SACKS','SACKS_YDS_LOST','QBR','RTG']]

###-------------------------------------------------------------------------###
###   START OF HOME PASSING   ----------------------------------------------###
###-------------------------------------------------------------------------###
string2 = strings[2]
junk = re.findall(r'>.*?<',string2)
junk2 = []
for thing in junk:
    temp = thing.translate(None,'><')
    if temp != '':
        junk2.append(temp.upper())
del(junk2[:9],junk2[-9:])
junk3 = []
counter = 1
for thing in junk2:
    if (counter - 2)%9 == 0:
        temp = thing.split('/')
        junk3.append(temp[0])
        junk3.append(temp[1])
    elif (counter - 7)%9 == 0:
        temp = thing.split('-')
        junk3.append(temp[0])
        junk3.append(temp[1])
    else:
        junk3.append(thing)
    counter += 1
rows = []
for i in xrange(int(len(junk3)/11.)):
    rows.append(junk3[i*11:(i+1)*11])
homePassingFrame = pandas.DataFrame(rows)
homePassingFrame.columns = ['PLAYER','PASS_COMPLETIONS','PASS_ATTEMPTS','YDS','AVG_YDS_PASS','TD','INT','SACKS','SACKS_YDS_LOST','QBR','RTG']
junk4 = re.findall(r'id/.*?<',string2)
rows = []
for thing in junk4:
    temp = thing.split('"')
    rows.append([re.sub('[^0-9]','',temp[0]),temp[1].translate(None,'><').upper()])
playerFrame = pandas.DataFrame(rows)
playerFrame.columns = ['PLAYER_ID','PLAYER']
playerFrame['GAME_ID'] = gameId
playerFrame['HOME_FG'] = 1
homePassing = pandas.merge(left = playerFrame, right = homePassingFrame, on = 'PLAYER')
homePassing = homePassing[['GAME_ID','PLAYER_ID','PLAYER','HOME_FG','PASS_COMPLETIONS','PASS_ATTEMPTS','YDS','AVG_YDS_PASS','TD','INT','SACKS','SACKS_YDS_LOST','QBR','RTG']]

###-------------------------------------------------------------------------###
###   COMBINE HOME AND AWAY PASSING   --------------------------------------###
###-------------------------------------------------------------------------###
passing = pandas.concat([awayPassing,homePassing])
passing.to_csv(os.getcwd()+'/passing/passing_'+gameId+'.csv',index=False)

###-------------------------------------------------------------------------###
###   START OF AWAY RUSHING   ----------------------------------------------###
###-------------------------------------------------------------------------###
string3 = strings[3]
junk = re.findall(r'>.*?<',string3)
junk2 = []
for thing in junk:
    temp = thing.translate(None,'><')
    if temp != '':
        junk2.append(temp.upper())    
del(junk2[:6],junk2[-6:])
rows = []
for i in xrange(int(len(junk2)/6.)):
    rows.append(junk2[i*6:(i+1)*6])
awayRushingFrame = pandas.DataFrame(rows)
awayRushingFrame.columns = ['PLAYER','CARRIES','YDS','YDS_PER_CARRY','TD','LONG']    
junk3 = re.findall(r'id/.*?<',string3)
rows = []
for thing in junk3:
    temp = thing.split('"')
    rows.append([re.sub('[^0-9]','',temp[0]),temp[1].translate(None,'><').upper()])
playerFrame = pandas.DataFrame(rows)
playerFrame.columns = ['PLAYER_ID','PLAYER']
playerFrame['GAME_ID'] = gameId
playerFrame['HOME_FG'] = 0
awayRushing = pandas.merge(left = playerFrame, right = awayRushingFrame, on = 'PLAYER')
awayRushing = awayRushing[['GAME_ID','PLAYER_ID','PLAYER','HOME_FG','CARRIES','YDS','YDS_PER_CARRY','TD','LONG']]

###-------------------------------------------------------------------------###
###   START OF HOME RUSHING   ----------------------------------------------###
###-------------------------------------------------------------------------###
string4 = strings[4]
junk = re.findall(r'>.*?<',string4)
junk2 = []
for thing in junk:
    temp = thing.translate(None,'><')
    if temp != '':
        junk2.append(temp.upper())    
del(junk2[:6],junk2[-6:])
rows = []
for i in xrange(int(len(junk2)/6.)):
    rows.append(junk2[i*6:(i+1)*6])
homeRushingFrame = pandas.DataFrame(rows)
homeRushingFrame.columns = ['PLAYER','CARRIES','YDS','YDS_PER_CARRY','TD','LONG']    
junk3 = re.findall(r'id/.*?<',string4)
rows = []
for thing in junk3:
    temp = thing.split('"')
    rows.append([re.sub('[^0-9]','',temp[0]),temp[1].translate(None,'><').upper()])
playerFrame = pandas.DataFrame(rows)
playerFrame.columns = ['PLAYER_ID','PLAYER']
playerFrame['GAME_ID'] = gameId
playerFrame['HOME_FG'] = 1
homeRushing = pandas.merge(left = playerFrame, right = homeRushingFrame, on = 'PLAYER')
homeRushing = homeRushing[['GAME_ID','PLAYER_ID','PLAYER','HOME_FG','CARRIES','YDS','YDS_PER_CARRY','TD','LONG']]
   
###-------------------------------------------------------------------------###
###   COMBINE HOME AND AWAY RUSHING   --------------------------------------###
###-------------------------------------------------------------------------###
rushing = pandas.concat([awayRushing,homeRushing])
rushing.to_csv(os.getcwd()+'/rushing/rushing_'+gameId+'.csv',index=False)
    
###-------------------------------------------------------------------------###
###   START OF AWAY PASING   -----------------------------------------------###
###-------------------------------------------------------------------------###
string5 = strings[5]
junk = re.findall(r'>.*?<',string5)
junk2 = []
for thing in junk:
    temp = thing.translate(None,'><')
    if temp != '':
        junk2.append(temp.upper())
del(junk2[:7],junk2[-7:])
rows = []
for i in xrange(int(len(junk2)/7.)):
    rows.append(junk2[i*7:(i+1)*7])
awayPassingFrame = pandas.DataFrame(rows)




homeRushingFrame.columns = ['PLAYER','CARRIES','YDS','YDS_PER_CARRY','TD','LONG']    
junk3 = re.findall(r'id/.*?<',string4)
rows = []
for thing in junk3:
    temp = thing.split('"')
    rows.append([re.sub('[^0-9]','',temp[0]),temp[1].translate(None,'><').upper()])
playerFrame = pandas.DataFrame(rows)
playerFrame.columns = ['PLAYER_ID','PLAYER']
playerFrame['GAME_ID'] = gameId
playerFrame['HOME_FG'] = 1
homeRushing = pandas.merge(left = playerFrame, right = homeRushingFrame, on = 'PLAYER')
homeRushing = homeRushing[['GAME_ID','PLAYER_ID','PLAYER','HOME_FG','CARRIES','YDS','YDS_PER_CARRY','TD','LONG']]
   
    
    
    