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
teamFrame = pandas.DataFrame([[gameId,teams[0],teams[1],0],[gameId,teams[2],teams[3],1]])
teamFrame.columns = ['GAME_ID','TEAM','TEAM_ABBREV','HOME_FG']

###-------------------------------------------------------------------------###
###   START OF AWAY PASSING   ----------------------------------------------###
###-------------------------------------------------------------------------###
frameColumns = ['PLAYER','COMPS','ATTS','YDS','AVG','TD','INT','SACKS','SACKS_YDS_LOST','QBR','RTG']

string = strings[1]
junk = re.findall(r'>.*?<',string)
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
frame = pandas.DataFrame(rows)
frame.columns = frameColumns
junk4 = re.findall(r'id/.*?<',string)
rows = []
for thing in junk4:
    temp = thing.split('"')
    rows.append([re.sub('[^0-9]','',temp[0]),temp[1].translate(None,'><').upper()])
playerFrame = pandas.DataFrame(rows)
playerFrame.columns = ['PLAYER_ID','PLAYER']
playerFrame['HOME_FG'] = 0
awayFrame = pandas.merge(left = playerFrame, right = frame, on = 'PLAYER')

###-------------------------------------------------------------------------###
###   START OF HOME PASSING   ----------------------------------------------###
###-------------------------------------------------------------------------###
string = strings[2]
junk = re.findall(r'>.*?<',string)
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
frame = pandas.DataFrame(rows)
frame.columns = frameColumns
junk4 = re.findall(r'id/.*?<',string)
rows = []
for thing in junk4:
    temp = thing.split('"')
    rows.append([re.sub('[^0-9]','',temp[0]),temp[1].translate(None,'><').upper()])
playerFrame = pandas.DataFrame(rows)
playerFrame.columns = ['PLAYER_ID','PLAYER']
playerFrame['HOME_FG'] = 1
homeFrame = pandas.merge(left = playerFrame, right = frame, on = 'PLAYER')

###-------------------------------------------------------------------------###
###   COMBINE HOME AND AWAY PASSING   --------------------------------------###
###-------------------------------------------------------------------------###
passing = pandas.concat([awayFrame,homeFrame])
passing = pandas.merge(left = teamFrame,right = passing, on = 'HOME_FG')
passing.to_csv(os.getcwd()+'/passing/passing_'+gameId+'.csv',index=False)

######################## Good above this!!


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
###   START OF AWAY RECEIVING   --------------------------------------------###
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
awayReceivingFrame = pandas.DataFrame(rows)
awayReceivingFrame.columns = ['PLAYER','REC','YDS','AVG_YDS_REC','TD','REC_LONG','TGTS']
junk3 = re.findall(r'id/.*?<',string5)
rows = []
for thing in junk3:
    temp = thing.split('"')
    rows.append([re.sub('[^0-9]','',temp[0]),temp[1].translate(None,'><').upper()])
playerFrame = pandas.DataFrame(rows)
playerFrame.columns = ['PLAYER_ID','PLAYER']
playerFrame['GAME_ID'] = gameId
playerFrame['HOME_FG'] = 0
awayReceiving = pandas.merge(left = playerFrame, right = awayReceivingFrame, on = 'PLAYER')
awayReceiving = awayReceiving[['GAME_ID','PLAYER_ID','PLAYER','HOME_FG','REC','YDS','AVG_YDS_REC','TD','REC_LONG','TGTS']]
   
###-------------------------------------------------------------------------###
###   START OF HOME RECEIVING   --------------------------------------------###
###-------------------------------------------------------------------------###
string6 = strings[6]
junk = re.findall(r'>.*?<',string6)
junk2 = []
for thing in junk:
    temp = thing.translate(None,'><')
    if temp != '':
        junk2.append(temp.upper())
del(junk2[:7],junk2[-7:])
rows = []
for i in xrange(int(len(junk2)/7.)):
    rows.append(junk2[i*7:(i+1)*7])
homeReceivingFrame = pandas.DataFrame(rows)
homeReceivingFrame.columns = ['PLAYER','REC','YDS','AVG_YDS_REC','TD','REC_LONG','TGTS']
junk3 = re.findall(r'id/.*?<',string6)
rows = []
for thing in junk3:
    temp = thing.split('"')
    rows.append([re.sub('[^0-9]','',temp[0]),temp[1].translate(None,'><').upper()])
playerFrame = pandas.DataFrame(rows)
playerFrame.columns = ['PLAYER_ID','PLAYER']
playerFrame['GAME_ID'] = gameId
playerFrame['HOME_FG'] = 1
homeReceiving = pandas.merge(left = playerFrame, right = homeReceivingFrame, on = 'PLAYER')
homeReceiving = homeReceiving[['GAME_ID','PLAYER_ID','PLAYER','HOME_FG','REC','YDS','AVG_YDS_REC','TD','REC_LONG','TGTS']]
    
###-------------------------------------------------------------------------###
###   COMBINE HOME AND AWAY RECEIVING  -------------------------------------###
###-------------------------------------------------------------------------###
receiving = pandas.concat([awayReceiving,homeReceiving])
receiving.to_csv(os.getcwd()+'/receiving/receiving_'+gameId+'.csv',index=False)

###-------------------------------------------------------------------------###
###   START OF AWAY FUMBLES   ----------------------------------------------###
###-------------------------------------------------------------------------###
string7 = strings[7]
junk = re.findall(r'>.*?<',string7)
junk2 = []
for thing in junk:
    temp = thing.translate(None,'><')
    if temp != '':
        junk2.append(temp.upper())
del(junk2[:4],junk2[-4:])
rows = []
for i in xrange(int(len(junk2)/4.)):
    rows.append(junk2[i*4:(i+1)*4])
if len(rows) == 0:
    rows = [['NONE',0,0,0]]
awayFumbleFrame = pandas.DataFrame(rows)
awayFumbleFrame.columns = ['PLAYER','FUM','LOST','REC']
junk3 = re.findall(r'id/.*?<',string7)
rows = []
for thing in junk3:
    temp = thing.split('"')
    rows.append([re.sub('[^0-9]','',temp[0]),temp[1].translate(None,'><').upper()])
if len(rows) == 0:
    rows = [[-1,'NONE']]
playerFrame = pandas.DataFrame(rows)
playerFrame.columns = ['PLAYER_ID','PLAYER']
playerFrame['GAME_ID'] = gameId
playerFrame['HOME_FG'] = 0
awayFumble = pandas.merge(left = playerFrame, right = awayFumbleFrame, on = 'PLAYER')
awayFumble = awayFumble[['GAME_ID','PLAYER_ID','PLAYER','HOME_FG','FUM','LOST','REC']]

###-------------------------------------------------------------------------###
###   START OF HOME FUMBLES   ----------------------------------------------###
###-------------------------------------------------------------------------###
string8 = strings[8]
junk = re.findall(r'>.*?<',string8)
junk2 = []
for thing in junk:
    temp = thing.translate(None,'><')
    if temp != '':
        junk2.append(temp.upper())
del(junk2[:4],junk2[-4:])
rows = []
for i in xrange(int(len(junk2)/4.)):
    rows.append(junk2[i*4:(i+1)*4])
if len(rows) == 0:
    rows = [['NONE',0,0,0]]
homeFumbleFrame = pandas.DataFrame(rows)
homeFumbleFrame.columns = ['PLAYER','FUM','LOST','REC']
junk3 = re.findall(r'id/.*?<',string8)
rows = []
for thing in junk3:
    temp = thing.split('"')
    rows.append([re.sub('[^0-9]','',temp[0]),temp[1].translate(None,'><').upper()])
if len(rows) == 0:
    rows = [[-1,'NONE']]
playerFrame = pandas.DataFrame(rows)
playerFrame.columns = ['PLAYER_ID','PLAYER']
playerFrame['GAME_ID'] = gameId
playerFrame['HOME_FG'] = 1
homeFumble = pandas.merge(left = playerFrame, right = homeFumbleFrame, on = 'PLAYER')
homeFumble = homeFumble[['GAME_ID','PLAYER_ID','PLAYER','HOME_FG','FUM','LOST','REC']]
    
###-------------------------------------------------------------------------###
###   COMBINE HOME AND AWAY FUMBLES  ---------------------------------------###
###-------------------------------------------------------------------------###
fumbles = pandas.concat([awayFumble,homeFumble])
fumbles.to_csv(os.getcwd()+'/fumbles/fumbles_'+gameId+'.csv',index=False)

###-------------------------------------------------------------------------###
###   START OF AWAY DEFENSE   ----------------------------------------------###
###-------------------------------------------------------------------------###
string = strings[9]
junk = re.findall(r'>.*?<',string)
junk2 = []
for thing in junk:
    temp = thing.translate(None,'><')
    if temp != '':
        junk2.append(temp.upper())
del(junk2[:8],junk2[-8:])
rows = []
for i in xrange(int(len(junk2)/8.)):
    rows.append(junk2[i*8:(i+1)*8])
frame = pandas.DataFrame(rows)
frame.columns = ['PLAYER','TOT','SOLO','SACKS','TFL','PD','QB_HITS','TD']
junk3 = re.findall(r'id/.*?<',string)
rows = []
for thing in junk3:
    temp = thing.split('"')
    rows.append([re.sub('[^0-9]','',temp[0]),temp[1].translate(None,'><').upper()])
playerFrame = pandas.DataFrame(rows)
playerFrame.columns = ['PLAYER_ID','PLAYER']
playerFrame['GAME_ID'] = gameId
playerFrame['HOME_FG'] = 0
frame = pandas.merge(left = playerFrame, right = frame, on = 'PLAYER')
awayDefense = frame[['GAME_ID','PLAYER_ID','PLAYER','HOME_FG','TOT','SOLO','SACKS','TFL','PD','QB_HITS','TD']]

###-------------------------------------------------------------------------###
###   START OF HOME DEFENSE   ----------------------------------------------###
###-------------------------------------------------------------------------###
string = strings[10]
junk = re.findall(r'>.*?<',string)
junk2 = []
for thing in junk:
    temp = thing.translate(None,'><')
    if temp != '':
        junk2.append(temp.upper())
del(junk2[:8],junk2[-8:])
rows = []
for i in xrange(int(len(junk2)/8.)):
    rows.append(junk2[i*8:(i+1)*8])
frame = pandas.DataFrame(rows)
frame.columns = ['PLAYER','TOT','SOLO','SACKS','TFL','PD','QB_HITS','TD']
junk3 = re.findall(r'id/.*?<',string)
rows = []
for thing in junk3:
    temp = thing.split('"')
    rows.append([re.sub('[^0-9]','',temp[0]),temp[1].translate(None,'><').upper()])
playerFrame = pandas.DataFrame(rows)
playerFrame.columns = ['PLAYER_ID','PLAYER']
playerFrame['GAME_ID'] = gameId
playerFrame['HOME_FG'] = 1
frame = pandas.merge(left = playerFrame, right = frame, on = 'PLAYER')
homeDefense = frame[['GAME_ID','PLAYER_ID','PLAYER','HOME_FG','TOT','SOLO','SACKS','TFL','PD','QB_HITS','TD']]

###-------------------------------------------------------------------------###
###   COMBINE HOME AND AWAY DEFENSE  ---------------------------------------###
###-------------------------------------------------------------------------###
defense = pandas.concat([awayDefense,homeDefense])
defense.to_csv(os.getcwd()+'/defense/defense_'+gameId+'.csv',index=False)

###-------------------------------------------------------------------------###
###   START OF AWAY INTERCEPTIONS   ----------------------------------------###
###-------------------------------------------------------------------------###
string = strings[11]
junk = re.findall(r'>.*?<',string)
junk2 = []
for thing in junk:
    temp = thing.translate(None,'><')
    if temp != '':
        junk2.append(temp.upper())
del(junk2[:4],junk2[-4:])
rows = []
for i in xrange(int(len(junk2)/4.)):
    rows.append(junk2[i*4:(i+1)*4])
if len(rows) == 0:
    rows = [['NONE',0,0,0]]
frame = pandas.DataFrame(rows)
frame.columns = ['PLAYER','INT','YDS','TD']
junk3 = re.findall(r'id/.*?<',string)
rows = []
for thing in junk3:
    temp = thing.split('"')
    rows.append([re.sub('[^0-9]','',temp[0]),temp[1].translate(None,'><').upper()])
if len(rows) == 0:
    rows = [[-1,'NONE']]
playerFrame = pandas.DataFrame(rows)
playerFrame.columns = ['PLAYER_ID','PLAYER']
playerFrame['GAME_ID'] = gameId
playerFrame['HOME_FG'] = 0
frame = pandas.merge(left = playerFrame, right = frame, on = 'PLAYER')
awayInterceptionFrame = frame[['GAME_ID','PLAYER_ID','PLAYER','HOME_FG','INT','YDS','TD']]

###-------------------------------------------------------------------------###
###   START OF HOME INTERCEPTIONS   ----------------------------------------###
###-------------------------------------------------------------------------###
string = strings[12]
junk = re.findall(r'>.*?<',string)
junk2 = []
for thing in junk:
    temp = thing.translate(None,'><')
    if temp != '':
        junk2.append(temp.upper())
del(junk2[:4],junk2[-4:])
rows = []
for i in xrange(int(len(junk2)/4.)):
    rows.append(junk2[i*4:(i+1)*4])
if len(rows) == 0:
    rows = [['NONE',0,0,0]]
frame = pandas.DataFrame(rows)
frame.columns = ['PLAYER','INT','YDS','TD']
junk3 = re.findall(r'id/.*?<',string)
rows = []
for thing in junk3:
    temp = thing.split('"')
    rows.append([re.sub('[^0-9]','',temp[0]),temp[1].translate(None,'><').upper()])
if len(rows) == 0:
    rows = [[-1,'NONE']]
playerFrame = pandas.DataFrame(rows)
playerFrame.columns = ['PLAYER_ID','PLAYER']
playerFrame['GAME_ID'] = gameId
playerFrame['HOME_FG'] = 1
frame = pandas.merge(left = playerFrame, right = frame, on = 'PLAYER')
homeInterceptionFrame = frame[['GAME_ID','PLAYER_ID','PLAYER','HOME_FG','INT','YDS','TD']]


###-------------------------------------------------------------------------###
###   COMBINE HOME AND AWAY INTERCEPTIONS   --------------------------------###
###-------------------------------------------------------------------------###
interceptions = pandas.concat([awayInterceptionFrame,homeInterceptionFrame])
interceptions.to_csv(os.getcwd()+'/interceptions/interceptions_'+gameId+'.csv',index=False)

###-------------------------------------------------------------------------###
###   START OF AWAY KICK RETURNS   -----------------------------------------###
###-------------------------------------------------------------------------###
string = strings[13]
junk = re.findall(r'>.*?<',string)
junk2 = []
for thing in junk:
    temp = thing.translate(None,'><')
    if temp != '':
        junk2.append(temp.upper())
del(junk2[:6],junk2[-6:])
rows = []
for i in xrange(int(len(junk2)/6.)):
    rows.append(junk2[i*6:(i+1)*6])
if len(rows) == 0:
    rows = [['NONE',0,0,0,0,0]]
frame = pandas.DataFrame(rows)
frame.columns = ['PLAYER','NO','YDS','AVG','LONG','TD']
junk3 = re.findall(r'id/.*?<',string)
rows = []
for thing in junk3:
    temp = thing.split('"')
    rows.append([re.sub('[^0-9]','',temp[0]),temp[1].translate(None,'><').upper()])
if len(rows) == 0:
    rows = [[-1,'NONE']]
playerFrame = pandas.DataFrame(rows)
playerFrame.columns = ['PLAYER_ID','PLAYER']
playerFrame['GAME_ID'] = gameId
playerFrame['HOME_FG'] = 0
frame = pandas.merge(left = playerFrame, right = frame, on = 'PLAYER')
awayFrame = frame[['GAME_ID','PLAYER_ID','PLAYER','HOME_FG','NO','YDS','AVG','LONG','TD']]

###-------------------------------------------------------------------------###
###   START OF HOME KICK RETURNS   -----------------------------------------###
###-------------------------------------------------------------------------###
string = strings[14]
junk = re.findall(r'>.*?<',string)
junk2 = []
for thing in junk:
    temp = thing.translate(None,'><')
    if temp != '':
        junk2.append(temp.upper())
del(junk2[:6],junk2[-6:])
rows = []
for i in xrange(int(len(junk2)/6.)):
    rows.append(junk2[i*6:(i+1)*6])
if len(rows) == 0:
    rows = [['NONE',0,0,0,0,0]]
frame = pandas.DataFrame(rows)
frame.columns = ['PLAYER','NO','YDS','AVG','LONG','TD']
junk3 = re.findall(r'id/.*?<',string)
rows = []
for thing in junk3:
    temp = thing.split('"')
    rows.append([re.sub('[^0-9]','',temp[0]),temp[1].translate(None,'><').upper()])
if len(rows) == 0:
    rows = [[-1,'NONE']]
playerFrame = pandas.DataFrame(rows)
playerFrame.columns = ['PLAYER_ID','PLAYER']
playerFrame['GAME_ID'] = gameId
playerFrame['HOME_FG'] = 1
frame = pandas.merge(left = playerFrame, right = frame, on = 'PLAYER')
homeFrame = frame[['GAME_ID','PLAYER_ID','PLAYER','HOME_FG','NO','YDS','AVG','LONG','TD']]

###-------------------------------------------------------------------------###
###   COMBINE HOME AND AWAY KICK RETURNS   ---------------------------------###
###-------------------------------------------------------------------------###
kickReturns = pandas.concat([awayFrame,homeFrame])
kickReturns.to_csv(os.getcwd()+'/kickReturns/kickReturns_'+gameId+'.csv',index=False)

###-------------------------------------------------------------------------###
###   START OF AWAY PUNT RETURNS   -----------------------------------------###
###-------------------------------------------------------------------------###
string = strings[15]
junk = re.findall(r'>.*?<',string)
junk2 = []
for thing in junk:
    temp = thing.translate(None,'><')
    if temp != '':
        junk2.append(temp.upper())
del(junk2[:6],junk2[-6:])
rows = []
for i in xrange(int(len(junk2)/6.)):
    rows.append(junk2[i*6:(i+1)*6])
if len(rows) == 0:
    rows = [['NONE',0,0,0,0,0]]
frame = pandas.DataFrame(rows)
frame.columns = ['PLAYER','NO','YDS','AVG','LONG','TD']
junk3 = re.findall(r'id/.*?<',string)
rows = []
for thing in junk3:
    temp = thing.split('"')
    rows.append([re.sub('[^0-9]','',temp[0]),temp[1].translate(None,'><').upper()])
if len(rows) == 0:
    rows = [[-1,'NONE']]
playerFrame = pandas.DataFrame(rows)
playerFrame.columns = ['PLAYER_ID','PLAYER']
playerFrame['GAME_ID'] = gameId
playerFrame['HOME_FG'] = 0
frame = pandas.merge(left = playerFrame, right = frame, on = 'PLAYER')
awayFrame = frame[['GAME_ID','PLAYER_ID','PLAYER','HOME_FG','NO','YDS','AVG','LONG','TD']]

###-------------------------------------------------------------------------###
###   START OF HOME PUNT RETURNS   -----------------------------------------###
###-------------------------------------------------------------------------###
string = strings[16]
junk = re.findall(r'>.*?<',string)
junk2 = []
for thing in junk:
    temp = thing.translate(None,'><')
    if temp != '':
        junk2.append(temp.upper())
del(junk2[:6],junk2[-6:])
rows = []
for i in xrange(int(len(junk2)/6.)):
    rows.append(junk2[i*6:(i+1)*6])
if len(rows) == 0:
    rows = [['NONE',0,0,0,0,0]]
frame = pandas.DataFrame(rows)
frame.columns = ['PLAYER','NO','YDS','AVG','LONG','TD']
junk3 = re.findall(r'id/.*?<',string)
rows = []
for thing in junk3:
    temp = thing.split('"')
    rows.append([re.sub('[^0-9]','',temp[0]),temp[1].translate(None,'><').upper()])
if len(rows) == 0:
    rows = [[-1,'NONE']]
playerFrame = pandas.DataFrame(rows)
playerFrame.columns = ['PLAYER_ID','PLAYER']
playerFrame['GAME_ID'] = gameId
playerFrame['HOME_FG'] = 1
frame = pandas.merge(left = playerFrame, right = frame, on = 'PLAYER')
homeFrame = frame[['GAME_ID','PLAYER_ID','PLAYER','HOME_FG','NO','YDS','AVG','LONG','TD']]

###-------------------------------------------------------------------------###
###   COMBINE HOME AND AWAY PUNT RETURNS   ---------------------------------###
###-------------------------------------------------------------------------###
puntReturns = pandas.concat([awayFrame,homeFrame])
puntReturns.to_csv(os.getcwd()+'/puntReturns/puntReturns_'+gameId+'.csv',index=False)

###-------------------------------------------------------------------------###
###   START OF AWAY KICKING   ----------------------------------------------###
###-------------------------------------------------------------------------###
string = strings[17]
junk = re.findall(r'>.*?<',string)
junk2 = []
for thing in junk:
    temp = thing.translate(None,'><')
    if temp != '':
        junk2.append(temp.upper())
del(junk2[:6],junk2[-6:])
rows = []
for i in xrange(int(len(junk2)/6.)):
    rows.append(junk2[i*6:(i+1)*6])
    
if len(rows) == 0:
    rows = [['NONE',0,0,0,0,0,0,0]]
else:
    junk3 = []
    counter = 1
    for thing in junk2:
        if (counter - 2)%6 == 0:
            temp = thing.split('/')
            junk3.append(temp[0])
            junk3.append(temp[1])
        elif (counter - 5)%6 == 0:
            temp = thing.split('/')
            junk3.append(temp[0])
            junk3.append(temp[1])
        else:
            junk3.append(thing)
        counter += 1    
rows = []
for i in xrange(int(len(junk3)/8.)):
    rows.append(junk3[i*8:(i+1)*8])        
frame = pandas.DataFrame(rows)
frame.columns = ['PLAYER','FG_MADE','FG_ATT','PCT','LONG','XP_MADE','XP_ATT','PTS']
junk3 = re.findall(r'id/.*?<',string)
rows = []
for thing in junk3:
    temp = thing.split('"')
    rows.append([re.sub('[^0-9]','',temp[0]),temp[1].translate(None,'><').upper()])
if len(rows) == 0:
    rows = [[-1,'NONE']]
playerFrame = pandas.DataFrame(rows)
playerFrame.columns = ['PLAYER_ID','PLAYER']
playerFrame['GAME_ID'] = gameId
playerFrame['HOME_FG'] = 0
frame = pandas.merge(left = playerFrame, right = frame, on = 'PLAYER')
awayFrame = frame[['GAME_ID','PLAYER_ID','PLAYER','HOME_FG','FG_MADE','FG_ATT','PCT','LONG','XP_MADE','XP_ATT','PTS']]

###-------------------------------------------------------------------------###
###   START OF HOME KICKING   ----------------------------------------------###
###-------------------------------------------------------------------------###
string = strings[18]
junk = re.findall(r'>.*?<',string)
junk2 = []
for thing in junk:
    temp = thing.translate(None,'><')
    if temp != '':
        junk2.append(temp.upper())
del(junk2[:6],junk2[-6:])
rows = []
for i in xrange(int(len(junk2)/6.)):
    rows.append(junk2[i*6:(i+1)*6])
    
if len(rows) == 0:
    rows = [['NONE',0,0,0,0,0,0,0]]
else:
    junk3 = []
    counter = 1
    for thing in junk2:
        if (counter - 2)%6 == 0:
            temp = thing.split('/')
            junk3.append(temp[0])
            junk3.append(temp[1])
        elif (counter - 5)%6 == 0:
            temp = thing.split('/')
            junk3.append(temp[0])
            junk3.append(temp[1])
        else:
            junk3.append(thing)
        counter += 1    
rows = []
for i in xrange(int(len(junk3)/8.)):
    rows.append(junk3[i*8:(i+1)*8])        
frame = pandas.DataFrame(rows)
frame.columns = ['PLAYER','FG_MADE','FG_ATT','PCT','LONG','XP_MADE','XP_ATT','PTS']
junk3 = re.findall(r'id/.*?<',string)
rows = []
for thing in junk3:
    temp = thing.split('"')
    rows.append([re.sub('[^0-9]','',temp[0]),temp[1].translate(None,'><').upper()])
if len(rows) == 0:
    rows = [[-1,'NONE']]
playerFrame = pandas.DataFrame(rows)
playerFrame.columns = ['PLAYER_ID','PLAYER']
playerFrame['GAME_ID'] = gameId
playerFrame['HOME_FG'] = 1
frame = pandas.merge(left = playerFrame, right = frame, on = 'PLAYER')
homeFrame = frame[['GAME_ID','PLAYER_ID','PLAYER','HOME_FG','FG_MADE','FG_ATT','PCT','LONG','XP_MADE','XP_ATT','PTS']]

###-------------------------------------------------------------------------###
###   COMBINE HOME AND AWAY PUNT RETURNS   ---------------------------------###
###-------------------------------------------------------------------------###
kicking = pandas.concat([awayFrame,homeFrame])
kicking.to_csv(os.getcwd()+'/kicking/kicking_'+gameId+'.csv',index=False)

###-------------------------------------------------------------------------###
###   START OF AWAY PUNTING   ----------------------------------------------###
###-------------------------------------------------------------------------###
string = strings[19]
junk = re.findall(r'>.*?<',string)
junk2 = []
for thing in junk:
    temp = thing.translate(None,'><')
    if temp != '':
        junk2.append(temp.upper())
del(junk2[:7],junk2[-7:])
rows = []
for i in xrange(int(len(junk2)/7.)):
    rows.append(junk2[i*7:(i+1)*7])
if len(rows) == 0:
    rows = [['NONE',0,0,0,0,0,0]]
      
frame = pandas.DataFrame(rows)
frame.columns = ['PLAYER','NO','YDS','AVG','TB','IN20','LONG']
junk3 = re.findall(r'id/.*?<',string)
rows = []
for thing in junk3:
    temp = thing.split('"')
    rows.append([re.sub('[^0-9]','',temp[0]),temp[1].translate(None,'><').upper()])
if len(rows) == 0:
    rows = [[-1,'NONE']]
playerFrame = pandas.DataFrame(rows)
playerFrame.columns = ['PLAYER_ID','PLAYER']
playerFrame['GAME_ID'] = gameId
playerFrame['HOME_FG'] = 0
frame = pandas.merge(left = playerFrame, right = frame, on = 'PLAYER')
awayFrame = frame[['GAME_ID','PLAYER_ID','PLAYER','HOME_FG','NO','YDS','AVG','TB','IN20','LONG']]

###-------------------------------------------------------------------------###
###   START OF HOME PUNTING   ----------------------------------------------###
###-------------------------------------------------------------------------###
string = strings[20]
junk = re.findall(r'>.*?<',string)
junk2 = []
for thing in junk:
    temp = thing.translate(None,'><')
    if temp != '':
        junk2.append(temp.upper())
del(junk2[:7],junk2[-7:])
rows = []
for i in xrange(int(len(junk2)/7.)):
    rows.append(junk2[i*7:(i+1)*7])
if len(rows) == 0:
    rows = [['NONE',0,0,0,0,0,0]]
      
frame = pandas.DataFrame(rows)
frame.columns = ['PLAYER','NO','YDS','AVG','TB','IN20','LONG']
junk3 = re.findall(r'id/.*?<',string)
rows = []
for thing in junk3:
    temp = thing.split('"')
    rows.append([re.sub('[^0-9]','',temp[0]),temp[1].translate(None,'><').upper()])
if len(rows) == 0:
    rows = [[-1,'NONE']]
playerFrame = pandas.DataFrame(rows)
playerFrame.columns = ['PLAYER_ID','PLAYER']
playerFrame['GAME_ID'] = gameId
playerFrame['HOME_FG'] = 1
frame = pandas.merge(left = playerFrame, right = frame, on = 'PLAYER')
homeFrame = frame[['GAME_ID','PLAYER_ID','PLAYER','HOME_FG','NO','YDS','AVG','TB','IN20','LONG']]

###-------------------------------------------------------------------------###
###   COMBINE HOME AND AWAY PUNTING   --------------------------------------###
###-------------------------------------------------------------------------###
punting = pandas.concat([awayFrame,homeFrame])
punting.to_csv(os.getcwd()+'/punting/punting_'+gameId+'.csv',index=False)


###
###   1.  teams
###   2.  passing
###   3.  rushing
###   4.  receiving
###   5.  fumbles
###   6.  defense
###   7.  interceptions
###   8.  kickReturns
###   9.  puntReturns
###   10. kicking
###   11. punting


    