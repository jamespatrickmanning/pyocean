# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 12:31:24 2013

@author: jmanning
"""

import pandas as pd

site=['AB01','AG01','BA01','BA02','BC01','BD01','BF01','BI02','BI01','BM01','BM02','BN01','BS02','CJ01','CP01','DC01','DJ01','DK01','DMF1','ET01','GS01','JA01','JC01','JS06','JT04','KO01','MF02','MM01','MW01','NL01','PF01','PM02','PM03','PW01','RA01','RM02','RM04','SJ01','TA14','TA15','TS01']
df=pd.read_csv('site.csv',sep=',',index_col=0)
processsite=[]


f = open('ProcessedSite.csv', 'w')

for i in range(len(df)):
    if df.index[i] in site:
        f.write(df.index[i]+','+str(df[' emolt_site.LAT_DDMM'][i])+','+str(df[' emolt_site.LON_DDMM'][i])+'\n')

f.close()