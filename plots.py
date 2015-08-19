import matplotlib.pyplot as plt
import pandas
import numpy
tableau10Blind = [(0,107,164),(255,128,14),(171,171,171),(89,89,89),(95,158,209),(200,82,0),(137,137,137),(163,200,236),(255,188,121),(207,207,207)]
for i in range(len(tableau10Blind)):
  r,g,b = tableau10Blind[i]
  tableau10Blind[i] = (r/255.,g/255.,b/255.)

preLoc = '/home/bdbozyk/nflData/nflStandingsPreNFL.csv'
regLoc = '/home/bdbozyk/nflData/nflStandingsRegNFL.csv'


pre = pandas.read_csv(preLoc)
reg = pandas.read_csv(regLoc)

basePre = pre[['YEAR','SEASON OUTCOME','TEAM','PCT','NET PTS','TD','W','L','T']]
baseReg = reg[['YEAR','SEASON OUTCOME','TEAM','PCT','NET PTS','TD','W','L','T']]

base = pandas.merge(left=basePre,right=baseReg,on=['YEAR','TEAM'])

base['AVG NET PTS GAME PRE'] = base['NET PTS_x']/(base['W_x']+base['L_x']+base['T_x'])
base['AVG NET PTS GAME REG'] = base['NET PTS_y']/(base['W_y']+base['L_y']+base['T_y'])


x = base[['AVG NET PTS GAME PRE']].get_values()
y = base[['AVG NET PTS GAME REG']].get_values()


SB = [[2014,'NE'],[2013,'SEA'],[2012,'BAL'],[2011,'NYG'],[2010,'GB'],[2009,'NO'],[2008,'PIT'],[2007,'NYG'],[2006,'IND']]
SBwinners = pandas.DataFrame(SB)
SBwinners['SB_F'] = 1
SBwinners.columns = ['YEAR','TEAM','SB_F']

base = pandas.merge(left=base,right=SBwinners,on=['YEAR','TEAM'],how='left').fillna(0)
colors = numpy.where(base['SEASON OUTCOME_y']=='NONE',0,1)
SB = base['SB_F'].get_values()
color = []
size = []

noPlayoffs_x = []
noPlayoffs_y = []
playoffs_x = []
playoffs_y = []
superBowl_x = []
superBowl_y = []

for i in range(len(colors)):
    if colors[i]==0 and SB[i]==0:
        color.append(tableau10Blind[0])
        size.append(40)
        noPlayoffs_x.append(x[i])
        noPlayoffs_y.append(y[i])
    elif colors[i]==1 and SB[i]==0:
        color.append(tableau10Blind[2])
        size.append(40)
        playoffs_x.append(x[i])
        playoffs_y.append(y[i])
    else:
        color.append(tableau10Blind[1])
        size.append(65)
        superBowl_x.append(x[i])
        superBowl_y.append(y[i])


plt.scatter(x,y,s=size,c=color,edgecolors='grey')

plt.style.use('fivethirtyeight')
plt.scatter(noPlayoffs_x,noPlayoffs_y,s=75,c=tableau10Blind[0])
plt.scatter(playoffs_x,playoffs_y,s=75,c=tableau10Blind[2])
plt.scatter(superBowl_x,superBowl_y,s=75,c=tableau10Blind[1])

plt.show()












