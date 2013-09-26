# -*- coding: utf-8 -*-
"""
Created on Fri Sep 20 12:08:54 2013

@author: jmanning
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 11:49:25 2013

@author: jmanning
"""

import pandas as pd
import matplotlib.pyplot as plt

###########AB01 site###############
df=pd.read_csv('AB01botttemp_mc_mod.csv',sep=',',index_col=1,names=['yy','mm','dd','count','mean','median','min','max','std'])
fig=plt.figure(figsize=(15,10))
ax=fig.add_subplot(311)
ax.plot(df.index,df['mean'].values)
df00=pd.read_csv('AB01botttemp_mc_obs.csv',sep=',',index_col=1,names=['yy','mm','dd','count','mean','median','min','max','std'])
ax.plot(df00.index,df00['mean'].values,color='r')
#ax.set_ylabel('Monthly Mean Temperature')
#ax.set_title('Bottom Monthly Mean Temperature')
for i in range(len(ax.lines)):#plot in different ways
     ax.lines[i].set_linewidth(4)
plt.figtext(.5,.92,' Monthly Mean Temperature ', fontsize=18, ha='center')
ax.text(.5, 12.5, 'AB01', style='italic',
        bbox={'facecolor':'yellow', 'alpha':3.5, 'pad':30})
ax.grid(True)
plt.legend(['modeled','observed'],loc='upper right', bbox_to_anchor=(1.01, 1.20),
          ncol=3, fancybox=True, shadow=True)

##########BN01 site#################

df1=pd.read_csv('BN01botttemp_mc_mod.csv',sep=',',index_col=1,names=['yy','mm','dd','count','mean','median','min','max','std'])
ax1=fig.add_subplot(312,sharex=ax)
ax1.text(.5, 9.5, 'BN01', style='italic',
        bbox={'facecolor':'yellow','alpha':3.5, 'pad':30})
ax1.plot(df1.index,df1['mean'].values)
df11=pd.read_csv('BN01botttemp_mc_obs.csv',sep=',',index_col=1,names=['yy','mm','dd','count','mean','median','min','max','std'])
ax1.plot(df11.index,df11['mean'].values,color='r')
for i in range(len(ax1.lines)):#plot in different ways
     ax1.lines[i].set_linewidth(4)
ax1.set_ylabel('Monthly Mean Temperature',fontsize=20)
#ax1.set_title('BN01 site monthly mean temperature')
ax1.grid(True)

##########JS06 site#################

df2=pd.read_csv('JS06botttemp_mc_mod.csv',sep=',',index_col=1,names=['yy','mm','dd','count','mean','median','min','max','std'])
ax2=fig.add_subplot(313,sharex=ax)
ax2.text(.5, 8.5, 'JS06', style='italic',
        bbox={'facecolor':'yellow','alpha':3.5, 'pad':30})
ax2.plot(df2.index,df2['mean'].values)
df22=pd.read_csv('JS06botttemp_mc_obs.csv',sep=',',index_col=1,names=['yy','mm','dd','count','mean','median','min','max','std'])
ax2.plot(df22.index,df22['mean'].values,color='r')
#ax2.set_ylabel('Monthly Mean Salinity')
#ax2.set_title('Bottom Monthly Mean Salinity at TA15')
for i in range(len(ax2.lines)):#plot in different ways
     ax2.lines[i].set_linewidth(4)
ax2.grid(True)
ax2.set_xlabel('Month')
#plt.setp(ax1.get_xticklabels(),visible=False)
#plt.setp(ax.get_xticklabels(),visible=False)
ax.tick_params(axis='both', which='major', labelsize=15)
#ax1.tick_params(axis='both', which='major', labelsize=15)
plt.tick_params(axis='both', which='major', labelsize=15)

plt.show()
plt.savefig('threesitestemperaturemonthlyplot.png')
