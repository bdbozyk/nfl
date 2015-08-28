### VARIABLES NEEDED ----------------------------------------------------------
#   dataDirectory - LOCATION FOR OUTPUT DATASET(S)
#------------------------------------------------------------------------------

### PROGRAM SUMMARY -----------------------------------------------------------
#   THIS PROGRAM SCANS THE <dataDirectory> AND COMBINES ALL DATASETS 
#------------------------------------------------------------------------------

### VARIABLE SPECIFICATION ----------------------------------------------------
dataDirectory = ''
#------------------------------------------------------------------------------

import os
import pandas
os.chdir(dataDirectory)


files = os.listdir(os.getcwd())
files.sort()
if 'gameSummary_curr.csv' in files:
    os.remove(dataDirectory+'gameSummary_curr.csv')
    print 'Removed gameSummary_curr.csv for replacement'
files = os.listdir(os.getcwd())
files.sort()    
    
base = pandas.read_csv(files[0])
del(files[0])
for df in files:
    base = pandas.concat([base,pandas.read_csv(df)])
    
base.to_csv('gameSummary_curr.csv',index=False)
