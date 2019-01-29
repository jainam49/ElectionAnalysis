import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from numpy.random import randn
from pandas import Series
from pandas import DataFrame
from io import StringIO
from scipy import stats
from datetime import datetime
from pandas_datareader import DataReader
import requests
#PLOTTING 
import matplotlib as mpl
import seaborn.apionly as sns


sns.set_style('whitegrid')
#get data from the web
url = "http://elections.huffingtonpost.com/pollster/2012-general-election-romney-vs-obama.csv"
source=requests.get(url).text
poll_data=StringIO(source)
poll_df=pd.read_csv(poll_data)


print(poll_df.head())
poll_df.info()
sns.catplot(x='Affiliation',kind='count',data=poll_df)
sns.catplot(x='Affiliation',kind='count',hue='Population',data=poll_df)
#strong showing of likely and registered voters,thus poll data should  be a good reflection on the populations polled
avg=pd.DataFrame(poll_df.mean())
print(avg.head())
#We dont require number of observations
avg.drop('Number of Observations',axis=0,inplace=True)

print(avg.head())
std=pd.DataFrame(poll_df.std())
std.drop('Number of Observations',axis=0,inplace=True)
print(std.head())
avg.head(3).plot(yerr=std,kind='bar',legend=False)
poll_avg=pd.concat([std,avg],axis=1,sort=True)

poll_avg.columns=['Average','STD']
print(poll_avg.head())

poll_df.plot(x='End Date', y=['Obama','Romney','Undecided'],linestyle='',marker='o')
#change in diff of votes acc. to various polls
poll_df['Difference']=(poll_df['Obama']-poll_df['Romney'])/100
print(poll_df['Difference'].head())
poll_df=poll_df.groupby(['Start Date'],as_index=False).mean()
print(poll_df.head())
poll_df.plot('Start Date','Difference',figsize=(12,4),marker='o',linestyle='-',color='purple')

row_in=0
xlimit=[]
for date in poll_df['Start Date']:
    if date[0:7]=='2012-10':
        xlimit.append(row_in)
        row_in +=1
    else:
        row_in +=1

print (min(xlimit))
print (max(xlimit))

poll_df.plot('Start Date','Difference',figsize=(12,4),marker='o',linestyle='-',color='purple',xlim=(325,352))
#now plot vertical lines of debate dates
#3 oct
plt.axvline(x=325+2,linewidth=4,color='r')
#11 oct
plt.axvline(x=325+10,linewidth=4,color='r')
#22 oct
plt.axvline(x=325+21,linewidth=4,color='r')
#SEE THE SENTIMENTS AFTER EACH DEBATE