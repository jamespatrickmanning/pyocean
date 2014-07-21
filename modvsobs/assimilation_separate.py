# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 15:02:24 2013

@author: yacheng and jmanning
plots before and after assimilation with Jan 2008 being the cutoff
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from datetime import datetime, timedelta
import matplotlib.dates as mdates
import sys
sys.path.append('../modules')
from utilities import my_x_axis_format


# HARDCODES #########
datadir='/net/data5/jmanning/modvsobs/'  
site1='AB01'
site2='BN01'
site3='JS06' # assumes plotting 3 sites in 3 panels
color1='black'
######################

if color1=='black': # case of B&W figure
  color2='gray'
else:
  color2='blue'

def parse(datet):
        #print datet[0:10]
        dt=datetime.strptime(datet[0:10], '%Y %m %d')
        return dt
def resamdc(resamda):
        newindex=[]
        for j in range(len(resamda)):    
                newindex.append(resamda['mean'].index[j].replace(year=2000)) # puts all observations in the same year
        repd=pd.DataFrame(resamda['mean'].values,index=newindex)
        resamdc=repd[0].resample('D',how=['count','mean','median','min','max','std'])    #add columns for custom date format
        resamdc['yy']=0
        resamdc['mm']=resamdc.index.month
        resamdc['dd']=resamdc.index.day
        output_fmt=['yy','mm','dd','count','mean','median','min','max','std']
        resamdcf=resamdc.reindex(columns=output_fmt)# found I needed to generate a new dataframe to print in this order
        return resamdcf        
def resammc(resamdc):
        resammc=resamdc['mean'].resample('m',how=['mean','median'],loffset=timedelta(days=-15))
        resammc['count']=0
        resammc['min']=0.
        resammc['max']=0.
        resammc['std']=0.   
        recount=resamdc['count'].resample('m',how=['mean'],loffset=timedelta(days=-15)).values
        remi=resamdc['min'].resample('m',how=['mean'],loffset=timedelta(days=-15)).values
        rema=resamdc['max'].resample('m',how=['mean'],loffset=timedelta(days=-15)).values
        restd=resamdc['std'].resample('m',how=['mean'],loffset=timedelta(days=-15)).values
        for kk in range(len(resammc)):
           resammc['count'].values[kk]=recount[kk]
           resammc['min'].values[kk]=remi[kk]
           resammc['max'].values[kk]=rema[kk]
           resammc['std'].values[kk]=restd[kk]
        resammc['yy']=0
        resammc['mm']=resammc.index.month
        resammc['dd']=0
        output_fmt=['yy','mm','dd','count','mean','median','min','max','std']
        resammcf=resammc.reindex(columns=output_fmt)# found I needed to generate a new dataframe to print in this order
        return resammcf

def group(dfmod,dfobs):
     grouper = dfmod.groupby(dfmod.index < pd.Timestamp('2008-01-01'))
     beforemod, aftermod = grouper.get_group(True), grouper.get_group(False)
     grouper = dfobs.groupby(dfobs.index < pd.Timestamp('2008-01-01'))
     beforeobs, afterobs = grouper.get_group(True), grouper.get_group(False)
     return beforemod, aftermod,beforeobs, afterobs
     
def diff(beforeobs,afterobs,beforemod,aftermod):
     obsbefore=resamdc(beforeobs)
     obsafter=resamdc(afterobs)
     modbefore=resamdc(beforemod)
     modafter=resamdc(aftermod)
     diffbefore=obsbefore-modbefore
     diffafter=obsafter-modafter
     return diffbefore,diffafter
     
def xaxix(ax):
     ax.xaxis.set_minor_locator(mdates.DayLocator(interval=30))
     ax.xaxis.set_minor_formatter(mdates.DateFormatter('%b'))
     years= mdates.YearLocator() # every year
     yearsFmt = mdates.DateFormatter('')
     ax.xaxis.set_major_locator(years)
     ax.xaxis.set_major_formatter(yearsFmt) 
     return ax

def mean(diff):
    container=[]
    container=diff['mean'].fillna(0)
    k=0
    for i in range(len(container)):
        if container[i]!=0:
            k+=1
    print k
    summean=(sum(container))/k
    print " mean values is "+str(summean)
    return summean

     
dfmod=pd.read_csv(datadir+site1+'botttemp_da_mod.csv',sep=',',parse_dates={'datet':[0,1,2]},index_col='datet',date_parser=parse,names=['yy','mm','dd','count','mean','median','min','max','std'])        
dfobs=pd.read_csv(datadir+site1+'botttemp_da_obs.csv',sep=',',parse_dates={'datet':[0,1,2]},index_col='datet',date_parser=parse,names=['yy','mm','dd','count','mean','median','min','max','std'])
dfmod1=pd.read_csv(datadir+site2+'botttemp_da_mod.csv',sep=',',parse_dates={'datet':[0,1,2]},index_col='datet',date_parser=parse,names=['yy','mm','dd','count','mean','median','min','max','std'])        
dfobs1=pd.read_csv(datadir+site2+'botttemp_da_obs.csv',sep=',',parse_dates={'datet':[0,1,2]},index_col='datet',date_parser=parse,names=['yy','mm','dd','count','mean','median','min','max','std'])
dfmod2=pd.read_csv(datadir+site3+'botttemp_da_mod.csv',sep=',',parse_dates={'datet':[0,1,2]},index_col='datet',date_parser=parse,names=['yy','mm','dd','count','mean','median','min','max','std'])        
dfobs2=pd.read_csv(datadir+site3+'botttemp_da_obs.csv',sep=',',parse_dates={'datet':[0,1,2]},index_col='datet',date_parser=parse,names=['yy','mm','dd','count','mean','median','min','max','std'])    

(beforemod, aftermod,beforeobs, afterobs)=group(dfmod,dfobs) # separates into period before and after Jan 2008
(diffbefore,diffafter)=diff(beforeobs,afterobs,beforemod,aftermod) # make climatalogic differences
(beforemod1, aftermod1,beforeobs1, afterobs1)=group(dfmod1,dfobs1) # same as above but for different site
(diffbefore1,diffafter1)=diff(beforeobs1,afterobs1,beforemod1,aftermod1)
(beforemod2, aftermod2,beforeobs2, afterobs2)=group(dfmod2,dfobs2)# same as above but for different site
(diffbefore2,diffafter2)=diff(beforeobs2,afterobs2,beforemod2,aftermod2)

fig=plt.figure()
ax=fig.add_subplot(311)
ax=xaxix(ax)
ax.axes.get_xaxis().set_visible(False)
ax.set_title(site1)
ax.grid(True)
#ax.plot(diffbefore.index,diffbefore['mean'].values)
rmt=pd.rolling_mean(diffbefore['mean'],30)
ax.plot(diffbefore.index,rmt.values,'--',color=color1,linewidth=3)
ax.plot(diffafter.index,pd.rolling_mean(diffafter['mean'],30).values,color=color2,linewidth=3)
plt.legend(['before assimilation','after assimilation'],loc='upper right', bbox_to_anchor=(1.01, 1.46),
          ncol=3, fancybox=True, shadow=True)  
          
ax1=fig.add_subplot(312,sharex=ax)
ax1.set_title(site2)
ax1=xaxix(ax1)
ax1.set_yticks(np.arange(-1.5,.5,.5))
ax1.axes.get_xaxis().set_visible(False)
ax1.grid(True)
ax1.set_ylabel('Obs-Mod Monthly Mean Temperature(degC)')
#ax1.plot(diffbefore1.index,diffbefore1['mean'].values)
#ax1.plot(diffafter1.index,diffafter1['mean'].values,color='r')
ax1.plot(diffbefore1.index,pd.rolling_mean(diffbefore1['mean'],30).values,'--',color=color1,linewidth=3)
ax1.plot(diffafter1.index,pd.rolling_mean(diffafter1['mean'],30).values,color=color2,linewidth=3)
 
ax2=fig.add_subplot(313,sharex=ax)
ax2=xaxix(ax2)
ax2.set_title(site3)
ax2.grid(True)
#ax2.plot(diffbefore2.index,diffbefore2['mean'].values)
#ax2.plot(diffafter2.index,diffafter2['mean'].values,color='r')
ax2.plot(diffbefore2.index,pd.rolling_mean(diffbefore2['mean'],30).values,'--',color=color1,linewidth=3)
ax2.plot(diffafter2.index,pd.rolling_mean(diffafter2['mean'],30).values,color=color2,linewidth=3)

summeanbef=mean(diffbefore)
summeanaft=mean(diffafter)
summeanbef1=mean(diffbefore1)
summeanaft1=mean(diffafter1)
summeanbef2=mean(diffbefore2)
summeanaft2=mean(diffafter2)

print summeanbef,summeanaft,summeanbef1,summeanaft1,summeanbef2,summeanaft2

plt.show()
plt.savefig('/net/nwebserver/epd/ocean/MainPage/modvsobs/figs/assimilate_separate.png')
plt.savefig('/net/nwebserver/epd/ocean/MainPage/modvsobs/figs/assimilate_separate.eps')
