# -*- coding: utf-8 -*-
"""
Created on Fri Sep 20 12:43:19 2013

@author: yacheng and jmanning
"""

import pandas as pd
import numpy as np
from math import sqrt
#site=['E01']
site=['AB01','AG01','BA01','BA02','BC01','BD01','BF01','BI02','BI01','BM01','BM02','BN01','BS02','CJ01','CP01','DC01','DJ01','DK01','DMF1','ET01','GS01','JA01','JC01','JS06','JT04','KO01','MF02','MM01','MW01','NL01','PF01','PM02','PM03','PW01','RA01','RM02','RM04','SJ01','TA14','TA15','TS01']
#site=['AG01surf','AG01bott','BA01surf','BA01bott','BA02surf','BA02bott','BA03surf','BA03bott']
#site=['RS01','TA15','NL01','JT04','DJ02','SK01']
df1=pd.read_csv("all_text_outputfile_new/"+site[0]+'botttemp_mc_mod_mc_obs.csv',index_col=0)
#ts1=pd.read_csv(site[0]+'bottsalinity_mc_obs.csv',index_col=0,names=['yy','mm','dd','count','mean','median','min','max','std'])
dfmean1=df1.mean()
df2=df1['mean'].fillna(0)
dfmean1['max']=max(df2)
dfmean1['min']=min(df2)
dfmean1=dfmean1.drop('rms')
dfmean1=dfmean1.drop('std')
#dfmean1['std']=ts1['std'].mean()
std1=df1['mean'].std()
rms1=sqrt((np.sum(np.square(df2)))/(np.count_nonzero(df2)))
row1 = pd.DataFrame([dict(rms=rms1,std=std1), ])
row1=row1.T
pdmean1=pd.DataFrame(dfmean1)
pdmean1=pdmean1.append(row1)
pdmean1=pdmean1.drop('median')
pdmean1.columns=[site[0]]

for k in range(len(site)):
    if k!=0:
        df=pd.read_csv("all_text_outputfile_new/"+site[k]+'botttemp_mc_mod_mc_obs.csv',index_col=0)
#        ts=pd.read_csv(site[k]+'bottsalinity_mc_obs.csv',index_col=0,names=['yy','mm','dd','count','mean','median','min','max','std'])
        dfmean=df.mean()
        df3=df['mean'].fillna(0)
        dfmean['max']=max(df3)
        dfmean['min']=min(df3)
        dfmean=dfmean.drop('rms')
        dfmean=dfmean.drop('std')
#        dfmean['std']=ts['std'].mean()
        std=df['mean'].std()
        rms=sqrt((np.sum(np.square(df3)))/(np.count_nonzero(df3)))
        row= pd.DataFrame([dict(rms=rms,std=std), ])
        row=row.T
        pdmean=pd.DataFrame(dfmean)
        pdmean=pdmean.append(row)
        pdmean=pdmean.drop('median')
        pdmean.columns=[site[k]]
        pdmean1=pdmean1.join(pdmean)
pdmean1=pdmean1.T
pdmean1.to_csv('totalcaculate.csv',index=True)
htmlmean=pdmean1.to_html(header=True,index=True,float_format=lambda x: '%10.2f' % x)
#save(htmlmean,'/net/nwebserver/epd/ocean/MainPage/lob/emoltvsnecofs_diff.html')
print pdmean1
#save(htmlmean,'emoltvsnecofs_diff.html')