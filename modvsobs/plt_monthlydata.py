# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 11:49:25 2013

@author: jmanning
"""

import pandas as pd
import matplotlib.pyplot as plt

###########AB01 site###############
df=pd.read_csv('AB01_wtmp_mc_mod.csv',sep=',',index_col=1,names=['yy','mm','dd','count','mean','median','min','max','std'])
fig=plt.figure(figsize=(15,10))
ax=fig.add_subplot(311)
ax.plot(df.index,df['mean'].values)
df00=pd.read_csv('AB01_wtmp_mc_obs.csv',sep=',',index_col=1,names=['yy','mm','dd','count','mean','median','min','max','std'])
ax.plot(df00.index,df00['mean'].values)
#ax.set_ylabel('Monthly Mean Temperature(degC)')
ax.set_title('AB01 site monthly mean temperature')
ax.grid(True)
plt.legend(['modeled','observed'],loc='upper right', bbox_to_anchor=(1, 1.30),
          ncol=3, fancybox=True, shadow=True)
##########BN01 site#################
df1=pd.read_csv('BN01_wtmp_mc_mod.csv',sep=',',index_col=1,names=['yy','mm','dd','count','mean','median','min','max','std'])
ax1=fig.add_subplot(312,sharex=ax)
ax1.plot(df1.index,df1['mean'].values)
df11=pd.read_csv('BN01_wtmp_mc_obs.csv',sep=',',index_col=1,names=['yy','mm','dd','count','mean','median','min','max','std'])
ax1.plot(df11.index,df11['mean'].values)
ax1.set_ylabel('Monthly Mean Temperature(degC)',fontsize=20)
ax1.set_title('BN01 site monthly mean temperature')
ax1.grid(True)
##########JS06 site#################
df2=pd.read_csv('JS06_wtmp_mc_mod.csv',sep=',',index_col=1,names=['yy','mm','dd','count','mean','median','min','max','std'])
ax2=fig.add_subplot(313,sharex=ax)
ax2.plot(df2.index,df2['mean'].values)
df22=pd.read_csv('JS06_wtmp_mc_obs.csv',sep=',',index_col=1,names=['yy','mm','dd','count','mean','median','min','max','std'])
ax2.plot(df22.index,df22['mean'].values)
#ax2.set_ylabel('Monthly Mean Temperature(degC)')
ax2.set_title('JS06 site monthly mean temperature')
ax2.grid(True)
ax2.set_xlabel('Month')
plt.setp(ax1.get_xticklabels(),visible=False)
plt.setp(ax.get_xticklabels(),visible=False)
ax.tick_params(axis='both', which='major', labelsize=15)
ax1.tick_params(axis='both', which='major', labelsize=15)
plt.tick_params(axis='both', which='major', labelsize=15)
plt.show()
plt.savefig('Monthly mean temperature plot.png')
