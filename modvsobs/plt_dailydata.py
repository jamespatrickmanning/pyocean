# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 10:07:34 2013

@author: jmanning
"""
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

def parse(datet):
        #print datet[0:10]
        dt=datetime.strptime(datet[0:10], '%Y %m %d')
        return dt
###########read-in data as DataFrame###############
df=pd.read_csv('AB01_wtmp_da_mod.csv',sep=',',parse_dates={'datet':[0,1,2]},index_col='datet',date_parser=parse,names=['yy','mm','dd','count','mean','median','min','max','std'])
df00=pd.read_csv('AB01_wtmp_da_obs.csv',sep=',',parse_dates={'datet':[0,1,2]},index_col='datet',date_parser=parse,names=['yy','mm','dd','count','mean','median','min','max','std'])
df1=pd.read_csv('BN01_wtmp_da_mod.csv',sep=',',parse_dates={'datet':[0,1,2]},index_col='datet',date_parser=parse,names=['yy','mm','dd','count','mean','median','min','max','std'])
df11=pd.read_csv('BN01_wtmp_da_obs.csv',sep=',',parse_dates={'datet':[0,1,2]},index_col='datet',date_parser=parse,names=['yy','mm','dd','count','mean','median','min','max','std'])
df2=pd.read_csv('JS06_wtmp_da_mod.csv',sep=',',parse_dates={'datet':[0,1,2]},index_col='datet',date_parser=parse,names=['yy','mm','dd','count','mean','median','min','max','std'])
df22=pd.read_csv('JS06_wtmp_da_obs.csv',sep=',',parse_dates={'datet':[0,1,2]},index_col='datet',date_parser=parse,names=['yy','mm','dd','count','mean','median','min','max','std'])

################plot the figure respectively########################

fig=plt.figure(figsize=(15,10))
ax=fig.add_subplot(311)
ax.plot(df.index,df['mean'].values)
ax.plot(df00.index,df00['mean'].values)
ax.set_ylabel('Temperature (degC)')
ax.set_title('AB01 example of highly variable stratification')
ax.grid(True)
plt.legend(['modeled','observed'],loc='upper right', bbox_to_anchor=(1, 1.30),
          ncol=3, fancybox=True, shadow=True)
##########BN01 site#################

ax1=fig.add_subplot(312,sharex=ax)
ax1.plot(df1.index,df1['mean'].values)
ax1.plot(df11.index,df11['mean'].values)
ax1.set_ylabel('Temperature (degC)')
ax1.set_title('BN01 example of more typical')
ax1.grid(True)

###########JS06 site################

ax2=fig.add_subplot(313,sharex=ax)
ax2.plot(df2.index,df2['mean'].values)
ax2.plot(df22.index,df22['mean'].values)
ax2.set_ylabel('Temperature (degC)')
ax2.set_xlabel('Year')
ax2.set_title('JS06 example of deep site')
ax2.grid(True)
plt.setp(ax1.get_xticklabels(),visible=False)
plt.setp(ax.get_xticklabels(),visible=False)

plt.show()
plt.savefig('three sites temperature plot.png')
