import urllib
import os
import re

os.chdir('/Users/KarliBozyk/nfl/')
os.getcwd()

gameId = '400554301'

year = 2014
gameIds = pandas.read_csv(os.getcwd()+'/gameSummary_'+str(year)+'.csv').drop_duplicates().get_values()

for game in gameIds:
    year = str(game[1])
    seasonType = game[2]
    week = str(game[3]).zfill(2)
    gameId = str(game[4])
    
    url = 'http://scores.espn.go.com/nfl/boxscore?gameId='+gameId
    html = urllib.urlopen(url).read()
    work = re.search(r'gamepackage-box-score".*?</div></div></div></article>',html,re.DOTALL).group()
    
    os.chdir('/Users/KarliBozyk/nfl/boxScoreRaw/')
    
    text_file = open('boxScoreRaw_'+year+'_'+seasonType+'_'+week+'_'+gameId+'.txt', 'w')
    text_file.write(work)
    text_file.close()


