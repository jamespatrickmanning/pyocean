# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 10:07:34 2013

@author: yacheng and  jmanning
Generates a daily average time series plot like Fig 2, for example, in manuscript
but also is used for other cases such as Fig 6
"""
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.dates as dates

#############################
# first a few hardcodes
w_fig=92 # figure number in manuscript which will control what gets plotted and outputfilename
site='E01' # first site to plot
color2='gray' # if you want color make this red
#############################

if color2=='gray': # for black and white case
  color1='black'
else:
  color1='blue' # for colored case


if w_fig==2 or w_fig==3:
  surforbot='bott'
  var='temp'
elif w_fig==61 or w_fig==62: # actuall 6a and 6b
  surforbot='surf'
  var='temp'
elif w_fig==91 or w_fig==92:
  surforbot='bott'
  var='salinity'

# Function used to parse date
def parse(datet):
        #print datet[0:10]
        dt=datetime.strptime(datet[0:10], '%Y %m %d')
        return dt

###########read-in data as DataFrames###############
if  w_fig==92:# fig 9b
  df1o=pd.read_csv("/net/data5/jmanning/modvsobs/E01bottsalinity_da_obs.csv",sep=',',parse_dates={'datet':[0,1,2]},index_col='datet',date_parser=parse,names=['yy','mm','dd','count','mean','median','min','max','std','rms'])
  df1m=pd.read_csv('/net/data5/jmanning/modvsobs/E01bottsalinity_da_mod.csv',sep=',',parse_dates={'datet':[0,1,2]},index_col='datet',date_parser=parse,names=['yy','mm','dd','count','mean','median','min','max','std','rms'])
elif (site=='RS01'): # figs 9a 
  df1o=pd.read_csv("/net/data5/jmanning/modvsobs/"+site+surforbot+var+"_da_obs.csv",sep=',',parse_dates={'datet':[0,1,2]},index_col='datet',date_parser=parse,names=['yy','mm','dd','count','mean','median','min','max','std'])
  df1m=pd.read_csv("/net/data5/jmanning/modvsobs/"+site+surforbot+var+"_da_mod.csv",sep=',',parse_dates={'datet':[0,1,2]},index_col='datet',date_parser=parse,names=['yy','mm','dd','count','mean','median','min','max','std'])
  df2o=pd.read_csv("/net/data5/jmanning/modvsobs/TA15"+surforbot+var+"_da_obs.csv",sep=',',parse_dates={'datet':[0,1,2]},index_col='datet',date_parser=parse,names=['yy','mm','dd','count','mean','median','min','max','std'])
  df2m=pd.read_csv("/net/data5/jmanning/modvsobs/TA15"+surforbot+var+"_da_mod.csv",sep=',',parse_dates={'datet':[0,1,2]},index_col='datet',date_parser=parse,names=['yy','mm','dd','count','mean','median','min','max','std'])
elif (site=='AB01'): # figs 2 and 3
  df1o=pd.read_csv("/net/data5/jmanning/modvsobs/"+site+surforbot+var+"_da_obs.csv",sep=',',parse_dates={'datet':[0,1,2]},index_col='datet',date_parser=parse,names=['yy','mm','dd','count','mean','median','min','max','std'])
  df1m=pd.read_csv("/net/data5/jmanning/modvsobs/"+site+surforbot+var+"_da_mod.csv",sep=',',parse_dates={'datet':[0,1,2]},index_col='datet',date_parser=parse,names=['yy','mm','dd','count','mean','median','min','max','std'])
  if w_fig==2:
    df2o=pd.read_csv("/net/data5/jmanning/modvsobs/BN01"+surforbot+var+"_da_obs.csv",sep=',',parse_dates={'datet':[0,1,2]},index_col='datet',date_parser=parse,names=['yy','mm','dd','count','mean','median','min','max','std'])
    df2m=pd.read_csv("/net/data5/jmanning/modvsobs/BN01"+surforbot+var+"_da_mod.csv",sep=',',parse_dates={'datet':[0,1,2]},index_col='datet',date_parser=parse,names=['yy','mm','dd','count','mean','median','min','max','std'])
    df3o=pd.read_csv("/net/data5/jmanning/modvsobs/JS06"+surforbot+var+"_da_obs.csv",sep=',',parse_dates={'datet':[0,1,2]},index_col='datet',date_parser=parse,names=['yy','mm','dd','count','mean','median','min','max','std'])
    df3m=pd.read_csv("/net/data5/jmanning/modvsobs/JS06"+surforbot+var+"_da_mod.csv",sep=',',parse_dates={'datet':[0,1,2]},index_col='datet',date_parser=parse,names=['yy','mm','dd','count','mean','median','min','max','std'])
elif (site=='AG01') or (site=='BA01'): # fig 6
  #df=pd.read_csv("/data5/jmanning/modvsobs/"+site+surforbot+var+"_da_obs.csv",sep=',',parse_dates={'datet':[0,1,2]},index_col='datet',date_parser=parse,names=['yy','mm','dd','count','mean','median','min','max','std','rms'])
  df1o=pd.read_csv("/data5/jmanning/modvsobs/"+site+surforbot+var+"_da_obs.csv",sep=',',parse_dates={'datet':[0,1,2]},index_col='datet',date_parser=parse,names=['yy','mm','dd','count','mean','median','min','max','std'])
  df1m=pd.read_csv("/data5/jmanning/modvsobs/"+site+surforbot+var+"_da_mod.csv",sep=',',parse_dates={'datet':[0,1,2]},index_col='datet',date_parser=parse,names=['yy','mm','dd','count','mean','median','min','max','std'])

################plot the first panel regardless of w_fig ########################
fig=plt.figure(figsize=(15,10))#figsize=(15,10))
if w_fig==61 or w_fig==62 or w_fig==91:
  ax1=fig.add_subplot(211)
if w_fig==2:
  ax1=fig.add_subplot(311)
  ax1.set_title('Bottom Temperature at '+site,fontsize=18)
if w_fig==3:
  ax1=fig.add_subplot(111)
  df1o=df1o[df1o.index > datetime(2004,5,20,0,0,0)]
  df1o=df1o[df1o.index < datetime(2004,10,15,0,0,0)]
  df1m=df1m[df1m.index > datetime(2004,5,20,0,0,0)]
  df1m=df1m[df1m.index < datetime(2004,10,15,0,0,0)]
  ax1.set_title('example summer (2004) bottom temperature at '+site,fontsize=20)
if w_fig==61 or w_fig==62:
  ax1.set_title('Surface '+var+' at '+site,fontsize=18)
  ax1.set_ylabel(var+' (degC)',fontsize=20)
if w_fig==91:
  df1o=df1o[df1o.index > datetime(2002,8,20,0,0,0)]
  df1o=df1o[df1o.index < datetime(2004,2,15,0,0,0)]
  df1m=df1m[df1m.index > datetime(2002,8,20,0,0,0)]
  df1m=df1m[df1m.index < datetime(2004,2,15,0,0,0)]
  ax1.set_ylabel(var,fontsize=20)
  ax1.set_title('Bottom '+var+' at '+site,fontsize=18)
if w_fig==92:
  ax1=fig.add_subplot(111)
  df1o=df1o[df1o.index > datetime(2003,1,1,0,0,0)]
  df1o=df1o[df1o.index < datetime(2004,3,1,0,0,0)]
  df1m=df1m[df1m.index > datetime(2003,1,1,0,0,0)]
  df1m=df1m[df1m.index < datetime(2004,3,1,0,0,0)]
  ax1.set_ylabel(var,fontsize=20)
  ax1.set_title('Bottom '+var+' at '+site,fontsize=18)

ax1.plot(df1m.index,df1m['mean'].values,'--',color=color1)
ax1.plot(df1o.index,df1o['mean'].values,color=color2)
ax1.grid(True)
ax1.lines[0].set_linewidth(3)
ax1.lines[1].set_linewidth(3)
ax1.tick_params(axis='both', which='major', labelsize=20)
plt.legend(['modeled','observed'],loc='upper right',# bbox_to_anchor=(1.01, 1.20),
          ncol=3, fancybox=True, shadow=True,prop={'size':14})

##########BN01 site mid-panel fig 2################# 
if w_fig==2:
  #BN01 site mid-panel fig 2
  ax2=fig.add_subplot(312,sharex=ax1)
  ax2.plot(df2m.index,df2m['mean'].values,color=color1)
  ax2.plot(df2o.index,df2o['mean'].values,color=color2)
  ax2.set_title('Bottom Temperature at BN01',fontsize=18)
  #for i in range(len(ax2.lines)):#plot in same way
  #     ax2.lines[i].set_linewidth(2)
  ax2.lines[0].set_linewidth(2)
  ax2.lines[1].set_linewidth(2)
  ax2.tick_params(axis='both', which='major', labelsize=20)
  ax2.grid(True)
  ###########JS06 site################
  ax3=fig.add_subplot(313,sharex=ax1)
  ax3.plot(df3m.index,df3m['mean'].values,color=color1)
  ax3.plot(df3o.index,df3o['mean'].values,color=color2)
  ax3.lines[0].set_linewidth(2)
  ax3.lines[1].set_linewidth(2)
  ax3.set_xlabel('Year',fontsize=20)
  ax3.set_title('Bottom Temperature at JS06',fontsize=18)
  ax3.grid(True)
  plt.setp(ax1.get_xticklabels(),visible=False)
  plt.setp(ax2.get_xticklabels(),visible=False)
  plt.tick_params(axis='both', which='major', labelsize=20)
  plt.show()
  plt.savefig('/net/nwebserver/epd/ocean/MainPage/modvsobs/figs/fig2_AB01BN01JS06.png')
  plt.savefig('/net/nwebserver/epd/ocean/MainPage/modvsobs/figs/fig2_AB01BN01JS06.eps')

if w_fig==3:
  ax1.xaxis.set_minor_locator(dates.MonthLocator(bymonth=None, bymonthday=1, interval=1, tz=None))
  ax1.xaxis.set_minor_formatter(dates.DateFormatter('%b'))
  ax1.xaxis.set_major_locator(dates.YearLocator())
  ax1.xaxis.set_major_formatter(dates.DateFormatter(' '))
  ax1.tick_params(axis='both', which='minor', labelsize=20)
  plt.show()
  plt.savefig('/net/nwebserver/epd/ocean/MainPage/modvsobs/figs/fig3_AB01summer04.png')
  plt.savefig('/net/nwebserver/epd/ocean/MainPage/modvsobs/figs/fig3_AB01summer04.eps')
if w_fig==61 or w_fig==62:
  ### 2nd panel fig 6 (AG01 or BA01 Bottom)
  surforbot='bott'
  df=pd.read_csv("/data5/jmanning/modvsobs/"+site+surforbot+var+"_da_obs.csv",sep=',',parse_dates={'datet':[0,1,2]},index_col='datet',date_parser=parse,names=['yy','mm','dd','count','mean','median','min','max','std'])
  df00=pd.read_csv("/data5/jmanning/modvsobs/"+site+surforbot+var+"_da_mod.csv",sep=',',parse_dates={'datet':[0,1,2]},index_col='datet',date_parser=parse,names=['yy','mm','dd','count','mean','median','min','max','std'])
  ax=fig.add_subplot(212,sharex=ax1,sharey=ax1)
  ax.plot(df00.index,df00['mean'].values,color=color1) 
  ax.plot(df.index,df['mean'].values,color=color2)
  ax.set_ylabel(var+' (degC)',fontsize=20)
  ax.set_title('Bottom '+var+' at '+site,fontsize=18)
  ax.grid(True)
  ax.lines[0].set_linewidth(3)
  ax.lines[1].set_linewidth(1)
  ax.tick_params(axis='both', which='major', labelsize=20)
  plt.setp(ax1.get_xticklabels(), visible=False)
  plt.show()
  if site=='AG01':
      aorb='a'
  else:
      aorb='b'
  plt.show()
  plt.savefig('/net/nwebserver/epd/ocean/MainPage/modvsobs/figs/fig6'+aorb+'_'+site+'_surf_and_bot'+'_'+var+'.png')
  plt.savefig('/net/nwebserver/epd/ocean/MainPage/modvsobs/figs/fig6'+aorb+'_'+site+'_surf_and_bot'+'_'+var+'.eps')
if w_fig==91:
  aorb='a'
  df2o=df2o[df2o.index > datetime(2002,2,20,0,0,0)]
  df2o=df2o[df2o.index < datetime(2003,7,15,0,0,0)]
  df2m=df2m[df2m.index > datetime(2002,2,20,0,0,0)]
  df2m=df2m[df2m.index < datetime(2003,7,15,0,0,0)]
  ax2=fig.add_subplot(212)
  ax2.set_ylabel(var,fontsize=20)
  ax2.plot(df2m.index,df2m['mean'].values,'--',color=color1)
  ax2.plot(df2o.index,df2o['mean'].values,color=color2)
  ax2.grid(True)
  ax2.lines[0].set_linewidth(3)
  ax2.lines[1].set_linewidth(3)
  ax2.tick_params(axis='both', which='major', labelsize=20)
  ax2.set_title('Bottom '+var+' at TA15',fontsize=18)
  plt.show()
  plt.savefig('/net/nwebserver/epd/ocean/MainPage/modvsobs/figs/fig9'+aorb+'_'+site+'_surf_and_bot'+'_'+var+'.png')
  plt.savefig('/net/nwebserver/epd/ocean/MainPage/modvsobs/figs/fig9'+aorb+'_'+site+'_surf_and_bot'+'_'+var+'.eps')
if w_fig==92:
  aorb='b'
  plt.show()
  plt.savefig('/net/nwebserver/epd/ocean/MainPage/modvsobs/figs/fig9'+aorb+'_'+site+'_surf_and_bot'+'_'+var+'.png')
  plt.savefig('/net/nwebserver/epd/ocean/MainPage/modvsobs/figs/fig9'+aorb+'_'+site+'_surf_and_bot'+'_'+var+'.eps')

#  grouping was used when comparing 2003 when comparing BF01 and NERACOOS I but I'll leave it commented out
#grouperdf00 = df00.groupby(df00.index < pd.Timestamp('2003-01-1'))
#beforedf00, afterdf00 = grouperdf00.get_group(True), grouperdf00.get_group(False)

#df1=pd.read_csv('BN01botttemp_da_mod.csv',sep=',',parse_dates={'datet':[0,1,2]},index_col='datet',date_parser=parse,names=['yy','mm','dd','count','mean','median','min','max','std'])
#df11=pd.read_csv('BN01botttemp_da_obs.csv',sep=',',parse_dates={'datet':[0,1,2]},index_col='datet',date_parser=parse,names=['yy','mm','dd','count','mean','median','min','max','std'])

#df2=pd.read_csv('all_text_outputfile/BF01botttemp_da_mod_da_obs.csv',sep=',',skiprows=1,index_col='date',parse_dates=True,names=['date','mean','median','min','max','std','rms'])
#df22=pd.read_csv('all_text_outputfile/I01botttemp_da_mod_da_obs.csv',sep=',',skiprows=1,index_col='date',parse_dates=True,names=['date','mean','median','min','max','std','rms'])
#grouperdf22 = df22.groupby(df22.index < pd.Timestamp('2003-01-1'))
#beforedf22, afterdf22 = grouperdf22.get_group(True), grouperdf22.get_group(False)


