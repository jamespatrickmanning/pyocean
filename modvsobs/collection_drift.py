# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 09:26:25 2013

@author: jmanning
"""

import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

FList = np.genfromtxt('drift_data/FList.csv',dtype=None,names=['FNs'],delimiter=',')
FNS=list(FList['FNs'])
f = open('shorttimedrift.csv', 'w')
for k in range(len(FNS)):
    print FNS[k]
    df=pd.read_csv('drift_data/'+FNS[k],index_col=0,skiprows=9,sep=',',names=['ID','TimeRD','TIME_GMT','YRDAY0_GMT','LON_DD','LAT_DD','TEMP','DEPTH'])
    print 'start time is '+df['TIME_GMT'].values[0],'end time is '+df['TIME_GMT'].values[-1]
    dtstart = datetime.strptime(df['TIME_GMT'].values[0], "%Y-%m-%d")
    dtend=datetime.strptime(df['TIME_GMT'].values[-1], "%Y-%m-%d")
    daynum=dtend-dtstart
    if daynum.days<7 or dtstart<datetime.strptime('2003-01-01', "%Y-%m-%d"):
        print dtstart
        print FNS[k]+' did not float more than 7 days or start time is before 2003'
        f.write(FNS[k]+'\n')
        k=+1
    else:
        latmax=max(df['LAT_DD'].values)
        latmin=min(df['LAT_DD'].values)
        lonmax=max(df['LON_DD'].values)
        lonmin=min(df['LON_DD'].values)
        plt.figure(figsize=(7,6))
        m = Basemap(projection='cyl',llcrnrlat=latmin-5,urcrnrlat=latmax+5,\
                llcrnrlon=lonmin-5,urcrnrlon=lonmax+5,resolution='h')
        m.drawparallels(np.arange(int(latmin),int(latmax)+1,1),labels=[1,0,0,0])
        m.drawmeridians(np.arange(int(lonmin),int(lonmax)+1,2),labels=[0,0,0,2])
        m.drawcoastlines()
        m.fillcontinents(color='grey')
        m.drawmapboundary()
        x, y = m(df['LON_DD'].values,df['LAT_DD'].values)
        m.plot(x,y,linewidth=1.5,color='r')
        plt.title(FNS[k])
        plt.show()
        plt.savefig(FNS[k][0:-4]+'.png')
f.close()
    