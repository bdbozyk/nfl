import urllib
import re
import pandas
import os

os.chdir('/Users/KarliBozyk/nfl/')
os.getcwd()

gameId = '400554301'

year = 2014
gameIds = pandas.read_csv(os.getcwd()+'/gameSummary_'+str(year)+'.csv')['GAME_ID'].drop_duplicates().get_values()



    
def StatSummary(gameId):
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
    teamFrame.columns = ['gameId','team','teamAbbrev','homeFg']
    
    teamFrame2 = teamFrame[:]
    teamFrame2['source'] = url
    teamFrame2.to_csv(os.getcwd()+'/boxScoreMeta_'+gameId+'.csv',index=False)
    
    print '1. Team Boxscore Metadata complete...'
    
    ###-------------------------------------------------------------------------###
    ###   START OF AWAY PASSING   ----------------------------------------------###
    ###-------------------------------------------------------------------------###    
    header = ['player','c','att','yds','avg','td','int','sacks','sacksYds']    
    string = strings[1]
    junk = re.findall(r'>.*?<',string)
    junk2 = []
    for thing in junk:
        temp = thing.translate(None,'><')
        if temp != '':
            junk2.append(temp.upper())
    colNum = 7
    if 'QBR' in junk2:
        colNum += 1
        header.append('qbr')
    if 'RTG' in junk2:
        colNum += 1
        header.append('rtg')    
    del(junk2[:colNum],junk2[-colNum:])
    junk3 = []
    counter = 1
    for thing in junk2:
        if (counter - 2)%colNum == 0:
            temp = thing.split('/')
            junk3.append(temp[0])
            junk3.append(temp[1])
        elif (counter - 7)%colNum == 0:
            temp = thing.split('-')
            junk3.append(temp[0])
            junk3.append(temp[1])
        else:
            junk3.append(thing)
        counter += 1
    rows = []
    for i in xrange(int(len(junk3)/(colNum+2))):
        rows.append(junk3[i*(colNum+2):(i+1)*(colNum+2)])
    frame = pandas.DataFrame(rows)
    frame.columns = header
    junk4 = re.findall(r'id/.*?<',string)
    rows = []
    for thing in junk4:
        temp = thing.split('"')
        rows.append([re.sub('[^0-9]','',temp[0]),temp[1].translate(None,'><').upper()])
    playerFrame = pandas.DataFrame(rows)
    playerFrame.columns = ['playerId','player']
    playerFrame['homeFg'] = 0
    awayFrame = pandas.merge(left = playerFrame, right = frame, on = 'player')
    
    ###-------------------------------------------------------------------------###
    ###   START OF HOME PASSING   ----------------------------------------------###
    ###-------------------------------------------------------------------------###
    header = ['player','c','att','yds','avg','td','int','sacks','sacksYds']    
    string = strings[2]
    junk = re.findall(r'>.*?<',string)
    junk2 = []
    for thing in junk:
        temp = thing.translate(None,'><')
        if temp != '':
            junk2.append(temp.upper())
    colNum = 7
    if 'QBR' in junk2:
        colNum += 1
        header.append('qbr')
    if 'RTG' in junk2:
        colNum += 1
        header.append('rtg')    
    del(junk2[:colNum],junk2[-colNum:])
    junk3 = []
    counter = 1
    for thing in junk2:
        if (counter - 2)%colNum == 0:
            temp = thing.split('/')
            junk3.append(temp[0])
            junk3.append(temp[1])
        elif (counter - 7)%colNum == 0:
            temp = thing.split('-')
            junk3.append(temp[0])
            junk3.append(temp[1])
        else:
            junk3.append(thing)
        counter += 1
    rows = []
    for i in xrange(int(len(junk3)/(colNum+2))):
        rows.append(junk3[i*(colNum+2):(i+1)*(colNum+2)])
    frame = pandas.DataFrame(rows)
    frame.columns = header
    junk4 = re.findall(r'id/.*?<',string)
    rows = []
    for thing in junk4:
        temp = thing.split('"')
        rows.append([re.sub('[^0-9]','',temp[0]),temp[1].translate(None,'><').upper()])
    playerFrame = pandas.DataFrame(rows)
    playerFrame.columns = ['playerId','player']
    playerFrame['homeFg'] = 1
    homeFrame = pandas.merge(left = playerFrame, right = frame, on = 'player')
    
    ###-------------------------------------------------------------------------###
    ###   COMBINE HOME AND AWAY PASSING   --------------------------------------###
    ###-------------------------------------------------------------------------###
    passing = pandas.concat([awayFrame,homeFrame])
    passing = pandas.merge(left = teamFrame,right = passing, on = 'homeFg')
    passing.to_csv(os.getcwd()+'/passing_'+gameId+'.csv',index=False)
    
    print '2. Passing is complete...'
    
    ###-------------------------------------------------------------------------###
    ###   START OF AWAY RUSHING   ----------------------------------------------###
    ###-------------------------------------------------------------------------###
    string = strings[3]
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
    frame = pandas.DataFrame(rows)
    frame.columns = ['PLAYER','CAR','YDS','AVG_YDS_CAR','TD','LONG']    
    junk3 = re.findall(r'id/.*?<',string)
    rows = []
    for thing in junk3:
        temp = thing.split('"')
        rows.append([re.sub('[^0-9]','',temp[0]),temp[1].translate(None,'><').upper()])
    playerFrame = pandas.DataFrame(rows)
    playerFrame.columns = ['PLAYER_ID','PLAYER']
    playerFrame['HOME_FG'] = 0
    frame = pandas.merge(left = playerFrame, right = frame, on = 'PLAYER')
    awayFrame = frame[['PLAYER_ID','PLAYER','HOME_FG','CAR','YDS','AVG_YDS_CAR','TD','LONG']]
    
    ###-------------------------------------------------------------------------###
    ###   START OF HOME RUSHING   ----------------------------------------------###
    ###-------------------------------------------------------------------------###
    string = strings[4]
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
    frame = pandas.DataFrame(rows)
    frame.columns = ['PLAYER','CAR','YDS','AVG_YDS_CAR','TD','LONG']    
    junk3 = re.findall(r'id/.*?<',string)
    rows = []
    for thing in junk3:
        temp = thing.split('"')
        rows.append([re.sub('[^0-9]','',temp[0]),temp[1].translate(None,'><').upper()])
    playerFrame = pandas.DataFrame(rows)
    playerFrame.columns = ['PLAYER_ID','PLAYER']
    playerFrame['HOME_FG'] = 1
    frame = pandas.merge(left = playerFrame, right = frame, on = 'PLAYER')
    homeFrame = frame[['PLAYER_ID','PLAYER','HOME_FG','CAR','YDS','AVG_YDS_CAR','TD','LONG']]
    
    ###-------------------------------------------------------------------------###
    ###   COMBINE HOME AND AWAY RUSHING   --------------------------------------###
    ###-------------------------------------------------------------------------###
    rushing = pandas.concat([awayFrame,homeFrame])
    rushing = pandas.merge(left = teamFrame,right = rushing, on = 'HOME_FG')
    rushing.to_csv(os.getcwd()+'/rushing/rushing_'+gameId+'.csv',index=False)
    
    print '3. Rushing is complete...'
        
    ###-------------------------------------------------------------------------###
    ###   START OF AWAY RECEIVING   --------------------------------------------###
    ###-------------------------------------------------------------------------###
    string = strings[5]
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
    frame = pandas.DataFrame(rows)
    frame.columns = ['PLAYER','REC','YDS','AVG_YDS_REC','TD','LONG','TGTS']
    junk3 = re.findall(r'id/.*?<',string)
    rows = []
    for thing in junk3:
        temp = thing.split('"')
        rows.append([re.sub('[^0-9]','',temp[0]),temp[1].translate(None,'><').upper()])
    playerFrame = pandas.DataFrame(rows)
    playerFrame.columns = ['PLAYER_ID','PLAYER']
    playerFrame['HOME_FG'] = 0
    frame = pandas.merge(left = playerFrame, right = frame, on = 'PLAYER')
    awayFrame = frame[['PLAYER_ID','PLAYER','HOME_FG','REC','YDS','AVG_YDS_REC','TD','LONG','TGTS']]
       
    ###-------------------------------------------------------------------------###
    ###   START OF HOME RECEIVING   --------------------------------------------###
    ###-------------------------------------------------------------------------###
    string = strings[6]
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
    frame = pandas.DataFrame(rows)
    frame.columns = ['PLAYER','REC','YDS','AVG_YDS_REC','TD','LONG','TGTS']
    junk3 = re.findall(r'id/.*?<',string)
    rows = []
    for thing in junk3:
        temp = thing.split('"')
        rows.append([re.sub('[^0-9]','',temp[0]),temp[1].translate(None,'><').upper()])
    playerFrame = pandas.DataFrame(rows)
    playerFrame.columns = ['PLAYER_ID','PLAYER']
    playerFrame['HOME_FG'] = 1
    frame = pandas.merge(left = playerFrame, right = frame, on = 'PLAYER')
    homeFrame = frame[['PLAYER_ID','PLAYER','HOME_FG','REC','YDS','AVG_YDS_REC','TD','LONG','TGTS']]
         
    ###-------------------------------------------------------------------------###
    ###   COMBINE HOME AND AWAY RECEIVING  -------------------------------------###
    ###-------------------------------------------------------------------------###
    receiving = pandas.concat([awayFrame,homeFrame])
    receiving = pandas.merge(left = teamFrame, right = receiving, on = 'HOME_FG')
    receiving.to_csv(os.getcwd()+'/receiving/receiving_'+gameId+'.csv',index=False)
    
    print '4. Receiving is complete...'
    
    ###-------------------------------------------------------------------------###
    ###   START OF AWAY FUMBLES   ----------------------------------------------###
    ###-------------------------------------------------------------------------###
    string = strings[7]
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
    frame.columns = ['PLAYER','FUM','LOST','REC']
    junk3 = re.findall(r'id/.*?<',string)
    rows = []
    for thing in junk3:
        temp = thing.split('"')
        rows.append([re.sub('[^0-9]','',temp[0]),temp[1].translate(None,'><').upper()])
    if len(rows) == 0:
        rows = [[-1,'NONE']]
    playerFrame = pandas.DataFrame(rows)
    playerFrame.columns = ['PLAYER_ID','PLAYER']
    playerFrame['HOME_FG'] = 0
    frame = pandas.merge(left = playerFrame, right = frame, on = 'PLAYER')
    awayFrame = frame[['PLAYER_ID','PLAYER','HOME_FG','FUM','LOST','REC']]
    
    ###-------------------------------------------------------------------------###
    ###   START OF HOME FUMBLES   ----------------------------------------------###
    ###-------------------------------------------------------------------------###
    string = strings[8]
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
    frame.columns = ['PLAYER','FUM','LOST','REC']
    junk3 = re.findall(r'id/.*?<',string)
    rows = []
    for thing in junk3:
        temp = thing.split('"')
        rows.append([re.sub('[^0-9]','',temp[0]),temp[1].translate(None,'><').upper()])
    if len(rows) == 0:
        rows = [[-1,'NONE']]
    playerFrame = pandas.DataFrame(rows)
    playerFrame.columns = ['PLAYER_ID','PLAYER']
    playerFrame['HOME_FG'] = 1
    frame = pandas.merge(left = playerFrame, right = frame, on = 'PLAYER')
    homeFrame = frame[['PLAYER_ID','PLAYER','HOME_FG','FUM','LOST','REC']]
       
    ###-------------------------------------------------------------------------###
    ###   COMBINE HOME AND AWAY FUMBLES  ---------------------------------------###
    ###-------------------------------------------------------------------------###
    fumbles = pandas.concat([awayFrame,homeFrame])
    fumbles = pandas.merge(left = teamFrame, right = fumbles, on = 'HOME_FG')
    fumbles.to_csv(os.getcwd()+'/fumbles/fumbles_'+gameId+'.csv',index=False)
    
    print '5. Fumbles is complete...'
    
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
    playerFrame['HOME_FG'] = 0
    frame = pandas.merge(left = playerFrame, right = frame, on = 'PLAYER')
    awayDefense = frame[['PLAYER_ID','PLAYER','HOME_FG','TOT','SOLO','SACKS','TFL','PD','QB_HITS','TD']]
    
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
    playerFrame['HOME_FG'] = 1
    frame = pandas.merge(left = playerFrame, right = frame, on = 'PLAYER')
    homeDefense = frame[['PLAYER_ID','PLAYER','HOME_FG','TOT','SOLO','SACKS','TFL','PD','QB_HITS','TD']]
    
    ###-------------------------------------------------------------------------###
    ###   COMBINE HOME AND AWAY DEFENSE  ---------------------------------------###
    ###-------------------------------------------------------------------------###
    defense = pandas.concat([awayDefense,homeDefense])
    defense = pandas.merge(left = teamFrame, right = defense, on = 'HOME_FG')
    defense.to_csv(os.getcwd()+'/defense/defense_'+gameId+'.csv',index=False)
    
    print '6. Defense is complete...'
    
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
    playerFrame['HOME_FG'] = 0
    frame = pandas.merge(left = playerFrame, right = frame, on = 'PLAYER')
    awayFrame = frame[['PLAYER_ID','PLAYER','HOME_FG','INT','YDS','TD']]
    
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
    playerFrame['HOME_FG'] = 1
    frame = pandas.merge(left = playerFrame, right = frame, on = 'PLAYER')
    homeFrame = frame[['PLAYER_ID','PLAYER','HOME_FG','INT','YDS','TD']]
    
    
    ###-------------------------------------------------------------------------###
    ###   COMBINE HOME AND AWAY INTERCEPTIONS   --------------------------------###
    ###-------------------------------------------------------------------------###
    interceptions = pandas.concat([awayFrame,homeFrame])
    interceptions = pandas.merge(left = teamFrame, right = interceptions, on = 'HOME_FG')
    interceptions.to_csv(os.getcwd()+'/interceptions/interceptions_'+gameId+'.csv',index=False)
    
    print '7. Interceptions is complete...'
    
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
    playerFrame['HOME_FG'] = 0
    frame = pandas.merge(left = playerFrame, right = frame, on = 'PLAYER')
    awayFrame = frame[['PLAYER_ID','PLAYER','HOME_FG','NO','YDS','AVG','LONG','TD']]
    
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
    playerFrame['HOME_FG'] = 1
    frame = pandas.merge(left = playerFrame, right = frame, on = 'PLAYER')
    homeFrame = frame[['PLAYER_ID','PLAYER','HOME_FG','NO','YDS','AVG','LONG','TD']]
    
    ###-------------------------------------------------------------------------###
    ###   COMBINE HOME AND AWAY KICK RETURNS   ---------------------------------###
    ###-------------------------------------------------------------------------###
    kickReturns = pandas.concat([awayFrame,homeFrame])
    kickReturns = pandas.merge(left = teamFrame, right = kickReturns, on = 'HOME_FG')
    kickReturns.to_csv(os.getcwd()+'/kickReturns/kickReturns_'+gameId+'.csv',index=False)
    
    print '8. Kick Returns is complete...'
    
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
    playerFrame['HOME_FG'] = 0
    frame = pandas.merge(left = playerFrame, right = frame, on = 'PLAYER')
    awayFrame = frame[['PLAYER_ID','PLAYER','HOME_FG','NO','YDS','AVG','LONG','TD']]
    
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
    playerFrame['HOME_FG'] = 1
    frame = pandas.merge(left = playerFrame, right = frame, on = 'PLAYER')
    homeFrame = frame[['PLAYER_ID','PLAYER','HOME_FG','NO','YDS','AVG','LONG','TD']]
    
    ###-------------------------------------------------------------------------###
    ###   COMBINE HOME AND AWAY PUNT RETURNS   ---------------------------------###
    ###-------------------------------------------------------------------------###
    puntReturns = pandas.concat([awayFrame,homeFrame])
    puntReturns = pandas.merge(left = teamFrame, right = puntReturns, on = 'HOME_FG')
    puntReturns.to_csv(os.getcwd()+'/puntReturns/puntReturns_'+gameId+'.csv',index=False)
    
    print '9.  Punt Returns is complete...'
    
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
    playerFrame['HOME_FG'] = 0
    frame = pandas.merge(left = playerFrame, right = frame, on = 'PLAYER')
    awayFrame = frame[['PLAYER_ID','PLAYER','HOME_FG','FG_MADE','FG_ATT','PCT','LONG','XP_MADE','XP_ATT','PTS']]
    
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
    playerFrame['HOME_FG'] = 1
    frame = pandas.merge(left = playerFrame, right = frame, on = 'PLAYER')
    homeFrame = frame[['PLAYER_ID','PLAYER','HOME_FG','FG_MADE','FG_ATT','PCT','LONG','XP_MADE','XP_ATT','PTS']]
    
    ###-------------------------------------------------------------------------###
    ###   COMBINE HOME AND AWAY PUNT RETURNS   ---------------------------------###
    ###-------------------------------------------------------------------------###
    kicking = pandas.concat([awayFrame,homeFrame])
    kicking = pandas.merge(left = teamFrame, right = kicking, on = 'HOME_FG')
    kicking.to_csv(os.getcwd()+'/kicking/kicking_'+gameId+'.csv',index=False)
    
    print '10. Kicking is complete...'
    
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
    playerFrame['HOME_FG'] = 0
    frame = pandas.merge(left = playerFrame, right = frame, on = 'PLAYER')
    awayFrame = frame[['PLAYER_ID','PLAYER','HOME_FG','NO','YDS','AVG','TB','IN20','LONG']]
    
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
    playerFrame['HOME_FG'] = 1
    frame = pandas.merge(left = playerFrame, right = frame, on = 'PLAYER')
    homeFrame = frame[['PLAYER_ID','PLAYER','HOME_FG','NO','YDS','AVG','TB','IN20','LONG']]
    
    ###-------------------------------------------------------------------------###
    ###   COMBINE HOME AND AWAY PUNTING   --------------------------------------###
    ###-------------------------------------------------------------------------###
    punting = pandas.concat([awayFrame,homeFrame])
    punting = pandas.merge(left = teamFrame, right = punting, on = 'HOME_FG')
    punting.to_csv(os.getcwd()+'/punting/punting_'+gameId+'.csv',index=False)
    
    
    print '11. Punting is complete...'
    print str(gameId)+' is complete.'
    
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
    
    return
    
for gameId in gameIds[1:10]:
    gameId = str(gameId)
    StatSummary(gameId)
    
        