# -*- coding: utf-8 -*-
"""
Created on Fri Feb 22 11:21:21 2013

@author: jmanning
"""
'''
we don't have below sites in the ProcessedSite.csv list 
which means we didn't process below site data.
ba03
dj02
RS01
SK01
'''

import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np
from pylab import rcParams
import sys
sys.path.append('../modules')
import basemap
from basemap import basemap_usgs,basemap_standard
######################################################   
assimsite=['NL01','TA14']
threesite=['AB01','JS06','BN01']
surfacesite=['AG01','BA01','BA02','BA03']
salinitysite=['NL01','JT04','DJ02','RS01','TA15','SK01']
roms=['JP02','JP14','JP19','JP22','MM01','OC01']
NERACOOS=['A01','B01','D02','E01','F01','I01','M01','N01']
case='_gommab' #'_MAB'
#df=pd.read_csv('ProcessedSite.csv',sep=',',skiprows=1,index_col=0,names=['site','lat','lon'])
#df=pd.read_csv('/net/home3/ocn/jmanning/sql/sqldump_sites'+case+'.dat',index_col=2,delim_whitespace=True)
df=pd.read_csv('/net/data5/jmanning/modvsobs/sqldump_sites'+case+'.dat',index_col=2,delim_whitespace=True)
df_RS01=pd.read_csv('/net/data5/jmanning/modvsobs/site.csv',index_col=0,names=['site','lat','lon']) #use for RS01
site,lon,lat=[],[],[]
for i in range(len(df)):
    site.append(df.index[i])
    (a,b)=divmod(float(df['LAT_DDMM'][i]),100)   
    aa=int(a)
    bb=float(b)
    lat.append(aa+bb/60)
    (c,d)=divmod(float(df['LON_DDMM'][i]),100)
    cc=int(c)
    dd=float(d)
    lon.append(-1*(cc+dd/60))
for i in range(len(df_RS01)):     #use for RS01
    if df_RS01.index[i]=='RS01':
        site.append(df_RS01.index[i])
        (a,b)=divmod(float(df_RS01['lat'][i]),100)   
        aa=int(a)
        bb=float(b)
        lat.append(aa+bb/60)
        (c,d)=divmod(float(df_RS01['lon'][i]),100)
        cc=int(c)
        dd=float(d)
        lon.append(-1*(cc+dd/60))
latsize=[39.,45.0]
lonsize=[-73.,-66.0]
bathy=True
draw_parallels=True
parallels_interval=[2]
cont_range=[-200,-100]
ss=10
basemap_usgs(latsize,lonsize,bathy,draw_parallels,parallels_interval,cont_range,ss)
basemap_standard(latsize,lonsize,[2])
#plt.figure(figsize=(15,10))
#x, y = m(-lon.values,lat.values)
x, y = lon,lat
plt.scatter(x,y,20,marker='o',color='r')
a=[]
for i in range(len(x)):
    if site[i] in threesite:
             #print site[i],lat[i],lon[i]
             plt.scatter(x[i],y[i],20,marker='o',color='blue')
             if site[i]=='BN01':
                 plt.annotate(site[i],xy=(x[i],y[i]),xytext=(x[i]+0.81,y[i]-0.35),arrowprops=dict(facecolor='blue', shrink=0.1,frac=0.3))#facecolor='black',));
             else:
                 plt.annotate(site[i],xy=(x[i],y[i]),xytext=(x[i]-0.31,y[i]-0.65),arrowprops=dict(facecolor='blue', shrink=0.1,frac=0.3))#facecolor='black',));
                 #plt.annotate(site[i],xy=(x[i],y[i]),xytext=(x[i]-0.31,y[i]-0.75),arrowprops=dict(arrowstyle="-|>",shrink=0.1))#connectionstyle="arc3,rad=-0.2",fc="w"));
    if site[i] in surfacesite:
             #print site[i],lat[i],lon[i]
             plt.scatter(x[i],y[i],20,marker='o',color='magenta')
             if site[i]=='BA01':
                 plt.annotate(site[i],xy=(x[i],y[i]),xytext=(x[i]-0.91,y[i]-0.55),arrowprops=dict(shrink=0.1,frac=0.3,facecolor='magenta'))#connectionstyle="arc3,rad=-0.2",fc="w"));
             elif site[i]=='AG01':
                 plt.annotate(site[i],xy=(x[i],y[i]),xytext=(x[i]-0.71,y[i]-0.45),arrowprops=dict(shrink=0.1,frac=0.3,facecolor='magenta'))#connectionstyle="arc3,rad=-0.2",fc="w"));

    if site[i] in salinitysite:
             #print ,site[i],lat[i],lon[i]
             plt.scatter(x[i],y[i],20,marker='o',color='green')
             if site[i]=='RS01':
                 plt.annotate(site[i],xy=(x[i],y[i]),xytext=(x[i]-1.01,y[i]+0.55),arrowprops=dict(shrink=0.1,frac=0.3,facecolor='green'))
             elif site[i]=='TA15':
                 plt.annotate(site[i],xy=(x[i],y[i]),xytext=(x[i]-0.11,y[i]+0.75),arrowprops=dict(shrink=0.1,frac=0.3,facecolor='green'))
    
    if site[i] in roms:
             plt.scatter(x[i],y[i],20,marker='o',color='cyan')
    if site[i] in assimsite:
             #print site[i],lat[i],lon[i]
             plt.scatter(x[i],y[i],20,marker='o',color='black')
             if site[i]=='NL01':
                 plt.annotate(site[i],xy=(x[i],y[i]),xytext=(x[i],y[i]-0.55),arrowprops=dict(arrowstyle="fancy",connectionstyle="arc3,rad=-0.2",facecolor='black'))
             elif site[i]=='TA14':
                 plt.annotate(site[i],xy=(x[i],y[i]),xytext=(x[i]+0.2,y[i]+0.75),arrowprops=dict(arrowstyle="fancy",connectionstyle="arc3,rad=-0.2",facecolor='black'))
    
if len(x)<=10:
     for i in range(len(x)):
         plt.text(x[i],y[i],site[i],fontsize=13,fontweight='normal',ha='right',va='baseline',color='b')

dfn=pd.read_csv('NERACOOS.csv',sep=',',index_col=0,names=['site','lat','lon'])
for jj in range(len(dfn)):
    plt.scatter(-1*dfn['lon'][jj],dfn['lat'][jj],20,marker='o',color='yellow')
    if dfn.index[jj]=="I01":
        plt.annotate(dfn.index[jj],xy=(-dfn['lon'][jj],dfn['lat'][jj]),xytext=(-dfn['lon'][jj]-0.15,dfn['lat'][jj]-0.75),arrowprops=dict(shrink=0.1,frac=0.3,facecolor='yellow'))
    if dfn.index[jj]=="E01":
        plt.annotate(dfn.index[jj],xy=(-dfn['lon'][jj],dfn['lat'][jj]),xytext=(-dfn['lon'][jj]+0.61,dfn['lat'][jj]-0.55),arrowprops=dict(shrink=0.1,frac=0.3,facecolor='yellow'))
rcParams['figure.figsize'] = 15, 12
plt.title('eMOLT sites used  for various analysis')
plt.show()
plt.savefig('/net/nwebserver/epd/ocean/MainPage/modvsobs/figs/fig1_emoltsites.png')
plt.savefig('/net/nwebserver/epd/ocean/MainPage/modvsobs/figs/fig1_emoltsites.eps')

   
