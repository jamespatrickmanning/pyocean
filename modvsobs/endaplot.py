# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 12:32:00 2013

@author: jmanning
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 10:07:34 2013

@author: jmanning
"""
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# HARDCODES ##########
#input_dir_n='/net/home3/ocn/jmanning/py/yw/gmri_2013/all_text_outputfile/'
#input_dir_e='/net/home3/ocn/jmanning/py/yw/gmri_2013/all_text_outputfile_new/'
input_dir='/net/data5/jmanning/modvsobs/'
color1='black'
########################
if color1=='black':
  color2='gray'
else:
  color2='red'

def parse(datet):
        #print datet[0:10]
        dt=datetime.strptime(datet[0:10], '%Y %m %d')
        return dt
###########read-in data as DataFrame###############
#dfemod=pd.read_csv('BF01botttemp_da_mod.csv',sep=',',parse_dates={'datet':[0,1,2]},index_col='datet',date_parser=parse,names=['yy','mm','dd','count','mean','median','min','max','std','rms'])
#dfeobs=pd.read_csv(input_dir+'BF01botttemp_da_obs.csv',sep=',',parse_dates={'datet':[0,1,2]},index_col='datet',date_parser=parse,names=['yy','mm','dd','count','mean','median','min','max','std','rms'])
dfeobs=pd.read_csv(input_dir+'BF01botttemp_da_obs.csv',sep=',',parse_dates={'datet':[0,1,2]},index_col='datet',date_parser=parse,names=['yy','mm','dd','count','mean','median','min','max','std'])
#dfnmod=pd.read_csv('I01botttemp_da_mod.csv',sep=',',parse_dates={'datet':[0,1,2]},index_col='datet',date_parser=parse,names=['yy','mm','dd','count','mean','median','min','max','std','rms'])
dfnobs=pd.read_csv(input_dir+'I01botttemp_da_obs.csv',sep=',',parse_dates={'datet':[0,1,2]},index_col='datet',date_parser=parse,names=['yy','mm','dd','count','mean','median','min','max','std','rms'])
grouper1 = dfnobs.groupby(dfnobs.index < pd.Timestamp('2003-01-1'))
nbefore1, nafter1 = grouper1.get_group(True), grouper1.get_group(False)


#dfeom=pd.read_csv(input_dir+'BF01botttemp_da_mod_da_obs.csv',sep=',',skiprows=1,parse_dates=True,index_col=[0],names=['date','mean','median','min','max','std','rms'])
dfeom=pd.read_csv(input_dir+'BF01botttemp_da_mod_da_obs.csv',sep=',',skiprows=1,parse_dates=True,index_col=[0],names=['date','mean','median','min','max','std'])
dfnom=pd.read_csv(input_dir+'I01botttemp_da_mod_da_obs.csv',sep=',',skiprows=1,parse_dates=True,index_col=[0],names=['date','mean','median','min','max','std','rms'])
grouper2 = dfnom.groupby(dfnom.index < pd.Timestamp('2003-01-1'))
nbefore2, nafter2 = grouper2.get_group(True), grouper2.get_group(False)
################plot the figure respectively########################

fig=plt.figure(figsize=(15,10))
ax1=fig.add_subplot(211)
ax1.plot(dfeobs.index,dfeobs['mean'].values,'-',color=color1,linewidth=2)
ax1.plot(nafter1.index,nafter1['mean'].values,color=color2,linewidth=3)
ax1.set_ylabel('temperature')
ax1.set_title('I01(50meter) VS BF01(60meter) bottom observed temperature')
ax1.grid(True)
#ax1.lines[0].set_linewidth(2)
#ax1.lines[2].set_linewidth(2)
plt.legend(['eMOLT','NERACOOS'],loc='upper right', #bbox_to_anchor=(1.01, 1.20),
          ncol=3, fancybox=True, shadow=True)
ax2=fig.add_subplot(212)
ax2.plot(dfeom.index,dfeom['mean'].values,'-',color=color1,linewidth=2)
ax2.plot(nafter2.index,nafter2['mean'].values,color=color2,linewidth=3)
ax2.set_ylabel('temperature difference')
ax2.set_title('I01 VS BF01 bottom observed-modeled temperature')
ax2.grid(True)
##########BN01 site#################
plt.show()
plt.savefig('/net/nwebserver/epd/ocean/MainPage/modvsobs/figs/fig10_I01VSBF01.png')
plt.savefig('/net/nwebserver/epd/ocean/MainPage/modvsobs/figs/fig10_I01VSBF01.eps')
