# -*- coding: utf-8 -*-
"""
Read an eMOLT data either:
    -remote data on the web (pydap via OPeNDAP)
    -from a local ascii file
    
Created on Sun Nov 18 06:33:34 2012

@author: JiM
"""
#### HARDCODES ###
site=['DMF2','DMF6']
source='opendap' #alternative is 'ascii'
outdir='/net/nwebserver/epd/ocean/MainPage/lob/'
##################
#from getdata import getemolt_latlon
from datetime import datetime, timedelta
from pandas import Series
from conversions import fth2m
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from numpy import mean
import datetime as dt
import scipy
from getdata import get_dataset, getemolt_temp
from pandas.core.common import save

for k in range(len(site)):
    if site[k][0:3]=='DMF':
        minnumperday=10 # had to use this in DMF case since they only record every two hours
        numperday=12
    else:
        minnumperday=18
        numperday=24
    [datet,temp,depth_i]=getemolt_temp(site,k,input_time=[dt.datetime(1880,1,1),dt.datetime(2020,1,1)], dep=[0,1000])
    depth=int(fth2m(mean(depth_i)))# mean depth of instrument to be added to outputfilename
    for m in range(len(temp)):
           temp[m]=(temp[m]-32.0)/1.8
    tso=Series(temp,index=datet)
    tsod=tso.resample('D',how=['count','mean','median','min','max','std'],loffset=timedelta(hours=-12))
    tsod.ix[tsod['count']<minnumperday,['mean','median','min','max','std']] = 'NaN'
    #add columns for custom date format
    tsod['yy']=tsod.index.year
    tsod['mm']=tsod.index.month
    tsod['dd']=tsod.index.day
    output_fmt=['yy','mm','dd','count','mean','median','min','max','std']
    tsodp=tsod.reindex(columns=output_fmt)  
    tsodp.to_csv(outdir+site[k]+'_wtmp_da_'+str(depth)+'.csv',index=False,header=False,na_rep='NaN',float_format='%10.2f')

    #create a monthly mean
    tsom=tso.resample('m',how=['count','mean','median','min','max','std'],kind='period')
    tsom.ix[tsom['count']<25*numperday,['mean','median','min','max','std']] = 'NaN'
   #add columns for custom date format
    tsom['yy']=tsom.index.year
    tsom['mm']=tsom.index.month
    tsom['dd']=15
    output_fmt=['yy','mm','dd','count','mean','median','min','max','std']
    tsomp=tsom.reindex(columns=output_fmt)# found I needed to generate a new dataframe to print in this order
    tsomp.to_csv(outdir+site[k]+'_wtmp_ma_'+str(depth)+'.csv',index=False,header=False,na_rep='NaN',float_format='%10.2f')
 
   #create daily climatolgies
    newindex=[]
    for j in range(len(tsod)):    
        newindex.append(tsod['mean'].index[j].replace(year=2000)) # puts all observations in the same year
    tsodnew=Series(tsod['mean'].values,index=newindex)
#    tsdc=tsodnew.resample('D',how=['count','mean','median','min','max','std'],loffset=timedelta(hours=-12))
    tsdc=tsodnew.resample('D',how=['count','mean','median','min','max','std'])    #add columns for custom date format
    tsdc['yy']=0
    tsdc['mm']=tsdc.index.month
    tsdc['dd']=tsdc.index.day
    output_fmt=['yy','mm','dd','count','mean','median','min','max','std']
    tsdcp=tsdc.reindex(columns=output_fmt)# found I needed to generate a new dataframe to print in this order
    tsdcp.to_csv(outdir+site[k]+'_wtmp_dc_'+str(depth)+'.csv',index=False,header=False,na_rep='NaN',float_format='%10.2f')
   #create monthly climatologies the new way 
    #tsmc=tsdc['mean'].resample('m',how=['count','mean','median','min','max','std'],loffset=timedelta(days=-15))
    tsmc=tsdc['mean'].resample('m',how=['mean','median'],loffset=timedelta(days=-15))
    tsmc['count']=0
    tsmc['min']=0.
    tsmc['max']=0.
    tsmc['std']=0.
    ##########get each month's count,min,max,std mean value###############
    tcount=tsdc['count'].resample('m',how=['mean'],loffset=timedelta(days=-15)).values
    tmi=tsdc['min'].resample('m',how=['mean'],loffset=timedelta(days=-15)).values
    tma=tsdc['max'].resample('m',how=['mean'],loffset=timedelta(days=-15)).values
    tstd=tsdc['std'].resample('m',how=['mean'],loffset=timedelta(days=-15)).values
    for kk in range(len(tsmc)):
       tsmc['count'].values[kk]=tcount[kk]
       tsmc['min'].values[kk]=tmi[kk]
       tsmc['max'].values[kk]=tma[kk]
       tsmc['std'].values[kk]=tstd[kk]
    tsmc['yy']=0
    tsmc['mm']=tsmc.index.month
    tsmc['dd']=0
    output_fmt=['yy','mm','dd','count','mean','median','min','max','std']
    tsmcp=tsmc.reindex(columns=output_fmt)# found I needed to generate a new dataframe to print in this order
    tsmcp.to_csv(outdir+site[k]+'_wtmp_mc_'+str(int(depth))+'.csv',index=False,header=False,na_rep='NaN',float_format='%10.2f')
    output_fmt_html=['mm','count','mean','median','min','max','std']
    outhtml=tsmcp.to_html(header=True,index=False,na_rep='NaN',float_format=lambda x: '%10.2f' % x,columns=output_fmt_html)
    save(outhtml,'/net/home3/ocn/jmanning/py/'+site[k]+'_wtmp_mc_'+str(int(depth))+'.html')
    #make some plots
    plt.figure()
    tsod['mean'].plot() #plot daily mean
    plt.title(site[k]+' daily means')
    plt.show()
    plt.savefig('/net/nwebserver/epd/ocean/MainPage/lob/'+site[k]+'_jt.png')
    plt.figure()
    tt=tsmc['mean'].plot() #plot mthly clim
    tt.xaxis.set_major_formatter(DateFormatter('%b'))
    plt.title(site[k]+' Monthly Climatology')
    plt.show()
    plt.savefig('/net/nwebserver/epd/ocean/MainPage/lob/'+site[k]+'_seacycle.png')
  
