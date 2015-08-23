import urllib
import re
import pandas
import os



def weekByWeek(directory,year):
    ''' The function weekByWeek will take a specified year and pull the weekly
        boxScore summaries and write them to the specified directory'''
        
    os.chdir(directory)
    
    weeks = []
    for i in range(5):
        # 2011 did not have a HOF preseason game
        if year == 2011:
              if i != 0:
                  weeks.append(['PRE',str(i)])
        else:
            weeks.append(['PRE',str(i)])
    for i in range(1,23):
        if i <= 17:
            weeks.append(['REG',str(i)])
        else:
            # NFL moved the ProBowl to the week before the Superbowl after 2008
            if year > 2008:
                if i == 21:
                    weeks.append(['PRO',str(i)])
                else:
                    weeks.append(['POST',str(i)])
            else:
                if i == 22:
                    weeks.append(['PRO',str(i)])
                else:
                    weeks.append(['POST',str(i)])
          
    seasonSummaries = []
    for seasonType, week in weeks:
    
        
        url = 'http://www.nfl.com/scores/'+str(year)+'/'+seasonType+str(week)
        print url
        
        html = urllib.urlopen(url).read()
        
        
        games = re.findall(r'<!-- BEGIN INCLUDE scoresbox/post -->.*?<!-- END INCLUDE scores/nav -->',html,re.DOTALL)
        
        
        dfs = []
        for game in games:
            game = game.translate(None,'\t\n\r')
            # Get NFL.com game ids 
            gameId = re.sub("[^0-9]","",re.search(r'id="scorebox-.*?"',game).group())
            # Get the date the gamed aired
            dateAired = re.search(r'"Date Aired".*?<',game).group()
            # Get the day of the week the games was played
            dow = re.search(r'>.*,',dateAired).group().translate(None,'>,').upper()
            # Get the date the game was played
            date = re.search(r',.*?<',dateAired).group().translate(None,',<')[1:]
            # Get the network the game aired on
            network = re.search(r'>.*<',re.search(r'"Aired on Network".*?<',game).group()).group().translate(None,'<>').upper()
            # Get the two teams that played
            meh = re.findall(r'team=.*?"',game)
            teams = []
            for thing in meh:
                thing = re.search(r'=.*"',thing).group().translate(None,'="')
                if thing not in teams:
                    teams.append(thing)
            # ProBowl has a different html for team
            if len(teams) < 2:
                pros = re.findall(r'"team-name"><a href="#">.*?<',game)
                teams.append(pros[0][24:27])
                teams.append(pros[1][24:27])
            # Get the Total Scores for the teams
            tot = re.findall(r'p class="total-score".*?<',game)
            totals = []
            for thing in tot:
                thing = re.sub("[^0-9]","",thing)
                totals.append(thing)
            # Get the points for each team/quarter played
            qtr1 = re.findall(r'first-qt">.*?<',game)
            for i in xrange(len(qtr1)):
                qtr1[i] = re.sub("[^0-9]","",qtr1[i])
            qtr2 = re.findall(r'second-qt">.*?<',game)
            for i in xrange(len(qtr2)):
                qtr2[i] = re.sub("[^0-9]","",qtr2[i])
            qtr3 = re.findall(r'third-qt".*?<',game)
            for i in xrange(len(qtr3)):
                qtr3[i] = re.sub("[^0-9]","",qtr3[i])
            qtr4 = re.findall(r'fourth-qt".*?<',game)
            for i in xrange(len(qtr4)):
                qtr4[i] = re.sub("[^0-9]","",qtr4[i])
            ot   = re.findall(r'ot-qt".*?<',game)
            for i in xrange(len(ot)):
                if re.sub("[^0-9]","",ot[i]) != '':
                    ot[i] = re.sub("[^0-9]","",ot[i])
                else:
                    ot[i] = 0
            # Count the number of big plays
            bigPlays = re.sub("[^0-9]","",re.search(r'big-plays-count.*?<',game).group())
            
            away = [year,week,seasonType,gameId,dow,date,network,teams[0],int(totals[0]),qtr1[0],qtr2[0],qtr3[0],qtr4[0],ot[0],bigPlays,'AWAY']
            home = [year,week,seasonType,gameId,dow,date,network,teams[1],int(totals[1]),qtr1[1],qtr2[1],qtr3[1],qtr4[1],ot[1],bigPlays,'HOME']
            
            df = pandas.DataFrame([away,home])
        
            df.columns = ['SEASON_YEAR','WEEK','SEASON_TYPE','NFL_GAME_ID','DAY_OF_WEEK','DATE','NETWORK','TEAM','TOTAL_PTS','Q1_PTS','Q2_PTS','Q3_PTS','Q4_PTS','OT_PTS','BIG_PLAYS','HOME_AWAY']
            df = df.sort('TOTAL_PTS').reset_index()
            del(df['index'])    
            dfs.append(df)    
            
        weekSummary = pandas.concat(dfs).reset_index()
        weekSummary.columns = ['WIN_F','SEASON_YEAR','WEEK','SEASON_TYPE','NFL_GAME_ID','DAY_OF_WEEK','DATE','NETWORK','TEAM','TOTAL_PTS','Q1_PTS','Q2_PTS','Q3_PTS','Q4_PTS','OT_PTS','BIG_PLAYS','HOME_AWAY']
        weekSummary['SOURCE'] = url        
        seasonSummaries.append(weekSummary)
        print seasonType+' '+week+' is complete.'
    
    seasonSummary = pandas.concat(seasonSummaries)  
    seasonSummary.to_csv('weekByWeekGameSummariesNFL'+str(year)+'.csv',index=False)
    return seasonSummary

df2001 = weekByWeek('/Users/George/nflData/',2001)
df2002 = weekByWeek('/Users/George/nflData/',2002)
df2003 = weekByWeek('/Users/George/nflData/',2003)
df2004 = weekByWeek('/Users/George/nflData/',2004)
df2005 = weekByWeek('/Users/George/nflData/',2005)
df2006 = weekByWeek('/Users/George/nflData/',2006)
df2007 = weekByWeek('/Users/George/nflData/',2007)
df2008 = weekByWeek('/Users/George/nflData/',2008)
df2009 = weekByWeek('/Users/George/nflData/',2009)
df2010 = weekByWeek('/Users/George/nflData/',2010)
df2011 = weekByWeek('/Users/George/nflData/',2011)
df2012 = weekByWeek('/Users/George/nflData/',2012)
df2013 = weekByWeek('/Users/George/nflData/',2013)
df2014 = weekByWeek('/Users/George/nflData/',2014)

