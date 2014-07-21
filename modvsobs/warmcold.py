# -*- coding: utf-8 -*-
"""
Created on Fri Mar 22 15:38:51 2013

@author: yacheng and jmanning
"""

import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np
import sys
sys.path.append('../modules')
from basemap import basemap_usgs
######################################################  
# read in the output of "creat_table.py" 
#dfcaculate=pd.read_csv('totalcaculate_10Dec2013.csv',sep=',',skiprows=1,index_col=0,names=['site','mean','min','max','rms','std'])
#dfcaculate=pd.read_csv('/net/data5/jmanning/modvsobs/totalcaculate_orig.csv',sep=',',skiprows=1,index_col=0,names=['site','mean','min','max','std'])
dfcaculate=pd.read_csv('/net/data5/jmanning/modvsobs/totalcalculate_with_roms.csv',sep=',',skiprows=1,index_col=0,names=['mean','min','max','rms','std'])
dfsite=pd.read_csv('/net/data5/jmanning/modvsobs/site.csv',sep=',',index_col=0)
f = open('warmcold.csv', 'w')
for i in range(len(dfcaculate)):
    for j in range(len(dfsite)):
         if str(dfcaculate.index[i]) == str(dfsite.index[j]):
             f.write(dfcaculate.index[i]+','+str(dfsite[' emolt_site.LAT_DDMM'][j])+','+str(dfsite[' emolt_site.LON_DDMM'][j])+','+str(dfcaculate['mean'][i])+'\n')

f.close()
df=pd.read_csv('warmcold.csv',sep=',',skiprows=1,index_col=0,names=['site','lat','lon','mean'])
for i in range(len(df)):
    (a,b)=divmod(float(df['lat'][i]),100)   
    aa=int(a)
    bb=float(b)
    df['lat'][i]=aa+bb/60
    (c,d)=divmod(float(df['lon'][i]),100)
    cc=int(c)
    dd=float(d)
    df['lon'][i]=cc+(dd/60)
latsize=[39.0,45.0] #40
lonsize=[-73.,-67.0] #-72
plt.figure(figsize=(7,6))

m = Basemap(projection='cyl',llcrnrlat=min(latsize)-0.01,urcrnrlat=max(latsize)+0.01,\
            llcrnrlon=min(lonsize)-0.01,urcrnrlon=max(lonsize)+0.01,resolution='h')#,fix_aspect=False)
m.drawparallels(np.arange(int(min(latsize)),int(max(latsize))+1,1),labels=[1,0,0,0])
m.drawmeridians(np.arange(int(min(lonsize)),int(max(lonsize))+1,1),labels=[0,0,0,1])
m.drawcoastlines()
m.fillcontinents(color='grey')
m.drawmapboundary()

# Now draw the isobaths (-200m)
#basemap_usgs(lat,lon,bathy,draw_parallels,parallels_interval,cont_range,ss):
basemap_usgs(latsize,lonsize,True,False,2,[-200],10)
#x, y = m2(-df['lon'],df['lat'])
x=-df['lon']
y=df['lat']

for i in range(len(df)):
    if df['mean'][i]>=np.float64(0):
        #print x[i],y[i] 
        #m.scatter(x[i],y[i],50*df['mean'][i],marker='o',color='red')
        plt.scatter(x[i],y[i],50*df['mean'][i],marker='o',color='red')
        if 50*df['mean'][i]>=np.float64(70) and df.index[i]<>'TA15':
            plt.annotate(df.index[i],xy=(x[i],y[i]),xytext=(x[i]+0.51,y[i]+0.35),arrowprops=dict(frac=0.3,facecolor='red', shrink=0.2))
        if df.index[i]=='TA15':
             plt.annotate(df.index[i],xy=(x[i],y[i]),xytext=(x[i]-0.31,y[i]+0.45),arrowprops=dict(frac=0.3,shrink=0.25,facecolor='red'))
    else:
        #print x[i],y[i]
        plt.scatter(x[i],y[i],50*(-df['mean'][i]),marker='o',color='blue')
        #print 50*df['mean'][i]
        if 50*(-df['mean'][i])>=np.float64(70):
            plt.annotate(df.index[i],xy=(x[i],y[i]),xytext=(x[i]+0.51,y[i]+0.35),arrowprops=dict(frac=0.3,facecolor='blue', shrink=0.2))
    if i>=38: #ROMS cases
        if df.index[i]=='MM01': # offset result for ROMS case
            plt.scatter(x[i]-0.1,y[i],50*(-df['mean'][i]),marker='o',color='blue')
        #plt.text(x[i]-0.021,y[i]-0.025,'R',fontsize=6,color='w',fontweight='bold')
        plt.text(x[i],y[i],'R',fontsize=6,color='w',fontweight='bold',verticalalignment='center',horizontalalignment='center')
plt.title('obs - mod mean bot temps (where largest blue = -1.5 degC)')
plt.show()
plt.savefig('/net/nwebserver/epd/ocean/MainPage/modvsobs/figs/fig1b_warmcold.png')
plt.savefig('/net/nwebserver/epd/ocean/MainPage/modvsobs/figs/fig1b_warmcold.eps')
