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
######################################################   
threesite=['AB01','JS06','BN01']
surfacesite=['AG01','BA01','BA02','BA03']
salinitysite=['NL01','JT04','DJ02','RS01','TA15','SK01']
NERACOOS=['A01','B01','D02','E01','F01','I01','M01','N01']
df=pd.read_csv('ProcessedSite.csv',sep=',',skiprows=1,index_col=0,names=['site','lat','lon'])
for i in range(len(df)-3):
    (a,b)=divmod(float(df['lat'][i]),100)   
    aa=int(a)
    bb=float(b)
    df['lat'][i]=aa+bb/60
    (c,d)=divmod(float(df['lon'][i]),100)
    cc=int(c)
    dd=float(d)
    df['lon'][i]=cc+(dd/60)
latsize=[39.7,45.0]
lonsize=[-72.,-66.0]
plt.figure(figsize=(7,6))
m = Basemap(projection='cyl',llcrnrlat=min(latsize)-0.01,urcrnrlat=max(latsize)+0.01,\
            llcrnrlon=min(lonsize)-0.01,urcrnrlon=max(lonsize)+0.01,resolution='h')#,fix_aspect=False)
m.drawparallels(np.arange(int(min(latsize)),int(max(latsize))+1,1),labels=[1,0,0,0])
m.drawmeridians(np.arange(int(min(lonsize)),int(max(lonsize))+1,1),labels=[0,0,0,1])
m.drawcoastlines()
m.fillcontinents(color='grey')
m.drawmapboundary()
x, y = m(-df['lon'].values,df['lat'].values)
m.scatter(x,y,20,marker='o',color='r')
for i in range(len(x)):
    if df.index[i] in threesite:
             print df.index[i],df['lat'][i],df['lon'][i]
             m.scatter(x[i],y[i],20,marker='o',color='blue')
             if df.index[i]=='BN01':
                 plt.annotate(df.index[i],xy=(x[i],y[i]),xytext=(x[i]+0.81,y[i]-0.35),arrowprops=dict(facecolor='blue', shrink=0.1))#facecolor='black',));
             else:
                 plt.annotate(df.index[i],xy=(x[i],y[i]),xytext=(x[i]-0.31,y[i]-0.75),arrowprops=dict(facecolor='blue', shrink=0.1))#facecolor='black',));
                 #plt.annotate(df.index[i],xy=(x[i],y[i]),xytext=(x[i]-0.31,y[i]-0.75),arrowprops=dict(arrowstyle="-|>",shrink=0.1))#connectionstyle="arc3,rad=-0.2",fc="w"));
    if df.index[i] in surfacesite:
             print df.index[i],df['lat'][i],df['lon'][i]
             m.scatter(x[i],y[i],20,marker='o',color='magenta')
             if df.index[i]=='BA01':
                 plt.annotate(df.index[i],xy=(x[i],y[i]),xytext=(x[i]-0.91,y[i]-0.55),arrowprops=dict(shrink=0.1,facecolor='magenta'))#connectionstyle="arc3,rad=-0.2",fc="w"));
             elif df.index[i]=='AG01':
                 plt.annotate(df.index[i],xy=(x[i],y[i]),xytext=(x[i]+0.71,y[i]-0.45),arrowprops=dict(shrink=0.1,facecolor='magenta'))#connectionstyle="arc3,rad=-0.2",fc="w"));

    if df.index[i] in salinitysite:
             print df.index[i],df['lat'][i],df['lon'][i]
             m.scatter(x[i],y[i],20,marker='o',color='green')
             if df.index[i]=='RS01':
                 plt.annotate(df.index[i],xy=(x[i],y[i]),xytext=(x[i]-1.01,y[i]+0.55),arrowprops=dict(shrink=0.1,facecolor='green'))
             elif df.index[i]=='TA15':
                 plt.annotate(df.index[i],xy=(x[i],y[i]),xytext=(x[i]-0.11,y[i]+0.75),arrowprops=dict(shrink=0.1,facecolor='green'))
    if df.index[i] in NERACOOS:
             print df.index[i],df['lat'][i],df['lon'][i]
             m.scatter(x[i],y[i],20,marker='o',color='yellow')
             if df.index[i]=="M01":
                  plt.annotate(df.index[i],xy=(x[i],y[i]),xytext=(x[i]-0.31,y[i]-0.75),arrowprops=dict(shrink=0.1,facecolor='yellow'))
             else:
                  plt.annotate(df.index[i],xy=(x[i],y[i]),xytext=(x[i]-1.01,y[i]+0.55),arrowprops=dict(shrink=0.1,facecolor='yellow'))

if len(x)<=10:
     for i in range(len(x)):
         plt.text(x[i],y[i],df.index[i],fontsize=13,fontweight='normal',ha='right',va='baseline',color='b')
plt.title('emolt temperature site')
plt.show()
plt.savefig('EmoltSite.png')

   