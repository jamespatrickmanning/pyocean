# -*- coding: utf-8 -*-
"""
Created on Fri Sep 20 12:43:19 2013
Generates a table of statistics include obs-mod mean and standard deviations

@author: yacheng and jmanning
"""

import pandas as pd
import numpy as np
from math import sqrt
import scipy
import os.path

# original site=['AB01','AG01','BA01','BA02','BC01','BD01','BF01','BI02','BI01','BM01','BM02','BN01','BS02','CJ01','CP01','DC01','DJ01','DK01','DMF1','ET01','GS01','JA01','JC01','JS06','JT04','KO01','MF02','MM01','MW01','NL01','PF01','PM02','PM03','PW01','RA01','RM02','RM04','SJ01','TA14','TA15','TS01']
#site=['AB01','AG01','BA01','BC01','BA02','BD01','BF01','BI02','BI01','BM01','BM02','BN01','BS02','CJ01','DC01','DJ01','DK01','DMF1','ET01','GS01','JA01','JC01','JS06','JT04','KO01','MF02','MM01','MW01','NL01','PF01','PM02','PM03','PW01','RA01','RM02','RM04','SJ01','TA14','TA15','TS01']
#site=['MW01','MM01','MF02','DJ01','DK01','CJ01','BS02','AB01','BM01','JS06','BN01','JA01','RM04','ET01','BF01','RA01','DC01','PW01','CP01']
#site=['AG01surf','AG01bott','BA01surf','BA01bott','BA02surf','BA02bott','BA03surf','BA03bott']
#site=['DMF1','BI01','RS01','TA15','NL01','JT04','DJ02','SK01']
site=['JP02','JP14','JP19','JP22','MM01','OC01','OC03']# roms sites

# READ  OBSERVED - MODELED MONTHLY CLIMATOLOGY
#df1=pd.read_csv("all_text_outputfile_new/"+site[0]+'botttemp_mc_mod_mc_obs.csv',index_col=0)
df1=pd.read_csv("/net/data5/jmanning/modvsobs/roms/"+site[0]+'botttemp_mc_mod_mc_obs.csv',index_col=0)
#ts1=pd.read_csv(site[0]+'bottsalinity_mc_obs.csv',index_col=0,names=['yy','mm','dd','count','mean','median','min','max','std'])

# CALCULATE THE MEAN, MIN, & MAX OF THE 12 MONTHLY MEAN VALUES
dfmean1=df1.mean().dropna()
#df2=df1['mean'].fillna(0) # fills missing values with zero but I'm not sure this should be done 
dfmean1['max']=np.nanmax(df1['mean'])
dfmean1['min']=np.nanmin(df1['mean'])
#dfmean1=dfmean1.drop('rms')
dfmean1=dfmean1.drop('median')
dfmean1=dfmean1.drop('std')

# CALCULATE STD AND RMS OF THESE MEAN DIFFERENCES AND MAKE DATAFRAME
#dfmean1['std']=ts1['std'].mean()
std1=df1['mean'].std() # standard deviation of the monthly mean
rms1=sqrt((np.sum(np.square(df1['mean'])))/(np.count_nonzero(df1['mean'])))
row1 = pd.DataFrame([dict(rms=rms1,std=std1), ])
row1=row1.T
pdmean1=pd.DataFrame(dfmean1)
pdmean1=pdmean1.append(row1)
#pdmean1=pdmean1.drop('median')
pdmean1.columns=[site[0]]

# DO THE SAME AS ABOVE FOR MULTIPLE SITES
for k in range(len(site)):
    if (k!=0) and (os.path.isfile("/net/data5/jmanning/modvsobs/roms/"+site[k]+'botttemp_mc_mod_mc_obs.csv')):
        df=pd.read_csv("/net/data5/jmanning/modvsobs/roms/"+site[k]+'botttemp_mc_mod_mc_obs.csv',index_col=0)
#        ts=pd.read_csv(site[k]+'bottsalinity_mc_obs.csv',index_col=0,names=['yy','mm','dd','count','mean','median','min','max','std'])
        dfmean=df.mean().dropna()
        #df3=df['mean'].fillna(0)
        dfmean['max']=np.nanmax(df['mean'])
        dfmean['min']=np.nanmin(df['mean'])
 #       dfmean=dfmean.drop('rms')
        dfmean=dfmean.drop('std')
        dfmean=dfmean.drop('median')
#        dfmean['std']=ts['std'].mean()
        std=df['mean'].std()
        rms=sqrt((np.sum(np.square(df['mean'])))/(np.count_nonzero(df['mean'])))
        row= pd.DataFrame([dict(rms=rms,std=std), ])
        row=row.T
        pdmean=pd.DataFrame(dfmean)
        pdmean=pdmean.append(row)
        #pdmean=pdmean.drop('median')
        pdmean.columns=[site[k]]
        pdmean1=pdmean1.join(pdmean)
pdmean1=pdmean1.T
pdmean1.to_csv('/data5/jmanning/modvsobs/roms/totalcalculate.csv',index=True,float_format='%8.3f')
htmlmean=pdmean1.to_html(header=True,index=True,float_format=lambda x: '%10.2f' % x)
save(htmlmean,'/net/nwebserver/epd/ocean/MainPage/modvsobs/roms/emoltvsroms_diff.html')
print pdmean1
#save(htmlmean,'emoltvsnecofs_diff.html')
