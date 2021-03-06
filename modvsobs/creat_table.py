# -*- coding: utf-8 -*-
"""
Created on Thu Feb 21 13:24:56 2013

@author: yacheng and jmanning
This reads in all the individual modvsobs.py output csv files for each site and makes a summary table in both "totalcalulate.csv" and "emoltvsnecofs_diff.html"
It generates the input for "warmcold.py" map.
Note: In Oct 2014, I added the "mode" hardcode which is either '_pre2008' or empty. 
"""

import pandas as pd
from pandas.core.common import save

#site=['MW01','DK01','MM01','MF02','DMF1','BI01','JC01','DJ01','CJ01','BS02','AB01','BM01','JS06','BN01','JA01','RM04','ET01','BF01','RA01','DC01','PW01','CP01']
site=['DC01','DJ01']
mode='_pre2008' # otherwise make empty string
outputdir='/net/data5/jmanning/modvsobs/'

# read in the output of "modvsobs.py"
df1=pd.read_csv(outputdir+site[0]+'botttemp_mc_mod_mc_obs'+mode+'.csv',index_col=0)
#ts1=pd.read_csv(outputdir+site[0]+'botttemp_mc_obs'+mode+'.csv',index_col=0,names=['yy','mm','dd','count','mean','median','min','max','std','rms'])
ts1=pd.read_csv(outputdir+site[0]+'botttemp_mc_obs'+mode+'.csv',index_col=0,names=['yy','mm','dd','count','mean','median','min','max','std'])
dfmean1=df1.mean()
df2=df1['mean'].fillna(0)
dfmean1['max']=max(df2)
dfmean1['min']=min(df2)
dfmean1['std']=ts1['std'].mean()
pdmean1=pd.DataFrame(dfmean1)
pdmean1=pdmean1.drop('median')
pdmean1.columns=[site[0]]

for k in range(len(site)):
    if k!=0:
        df=pd.read_csv(outputdir+site[k]+'botttemp_mc_mod_mc_obs'+mode+'.csv',index_col=0)
        ts=pd.read_csv(outputdir+site[k]+'botttemp_mc_obs'+mode+'.csv',index_col=0,names=['yy','mm','dd','count','mean','median','min','max','std'])
        dfmean=df.mean()
        df3=df['mean'].fillna(0)
        dfmean['max']=max(df3)
        dfmean['min']=min(df3)
        dfmean['std']=ts['std'].mean()
        pdmean=pd.DataFrame(dfmean)
        pdmean=pdmean.drop('median')
        pdmean.columns=[site[k]]
        pdmean1=pdmean1.join(pdmean)
pdmean1=pdmean1.T
pdmean1.to_csv('totalcaculate'+mode+'.csv',index=True)
htmlmean=pdmean1.to_html(header=True,index=True,float_format=lambda x: '%10.2f' % x)
save(htmlmean,'/net/nwebserver/epd/ocean/MainPage/lob/emoltvsnecofs_diff'+mode+'.html')
