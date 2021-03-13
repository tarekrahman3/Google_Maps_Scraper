import glob
import pandas as pd
df = pd.concat(map(pd.read_csv, glob.glob('*.csv')))
#df = map(pd.read_csv, glob.glob('*.csv'))
n = df.replace({'business_url':r'.+ \| '}, {'business_url':''}, regex=True)
n.to_csv('a.csv', index = False)
