# -*- coding: utf-8 -*-
"""
Created on Thu Feb 21 15:12:47 2013

@author: yacheng and jmanning
"""

import pandas as pd
from pandas.core.common import save
import matplotlib.pyplot as plt

## HARDCODES ###
inputdir='/net/data5/jmanning/modvsobs/'
outputplotdir='/net/nwebserver/epd/ocean/MainPage/modvsobs/figs/'
site=['AG01surf','AG01bott']
color1='black' # otherwise red
###################
if color1=='black': # B&W case
  color2='gray'
else:
  color2='blue'

df1=pd.read_csv(inputdir+site[0]+'temp_mc_mod_mc_obs.csv',index_col=0)
dfmean1=df1['mean']
pdmean1=pd.DataFrame(dfmean1,index=df1.index)
pdmean1.columns=[site[0]]
for k in range(len(site)):
    if k!=0:
        df=pd.read_csv(inputdir+site[k]+'temp_mc_mod_mc_obs.csv',index_col=0)
        dfmean=df['mean']
        pdmean=pd.DataFrame(dfmean,index=df.index)
        pdmean.columns=[site[k]]
        pdmean1=pdmean1.join(pdmean)
print pdmean1


site2=['BA01surf','BA01bott']
df2=pd.read_csv(inputdir+site2[0]+'temp_mc_mod_mc_obs.csv',index_col=0)
dfmean2=df2['mean']
pdmean2=pd.DataFrame(dfmean2,index=df2.index)

pdmean2.columns=[site2[0]]
for k in range(len(site2)):
    if k!=0:
        df3=pd.read_csv(inputdir+site2[k]+'temp_mc_mod_mc_obs.csv',index_col=0)
        dfmean3=df3['mean']
        pdmean3=pd.DataFrame(dfmean3,index=df3.index)
        pdmean3.columns=[site2[k]]
        pdmean2=pdmean2.join(pdmean3)
print pdmean2


#pdmean1.to_csv('totalplot.csv',index=True)
#pdmean1.to_csv('surface_bottom.csv',index=True)
#htmlmean=pdmean1.to_html(header=True,index=True)
#save(htmlmean,'surface_bottom.html')

fig=plt.figure()
ax=fig.add_subplot(211)
#ax.plot(pdmean1.index,pdmean1.values)
ax.plot(pdmean1.index,pdmean1['AG01surf'],color=color1)
ax.plot(pdmean1.index,pdmean1['AG01bott'],color=color2)
ax.set_ylabel('Temperature difference (degC)')
plt.title('observed minus model at AG01')
plt.grid()
#ax.set_xlabel('Month')
plt.setp(ax.get_xticklabels(),visible=False)
ax.lines[0].set_linestyle('-')
ax.lines[1].set_linestyle('--')
for i in range(len(ax.lines)):#plot in different ways
     ax.lines[i].set_linewidth(4)
plt.legend(['surface','bottom'],loc='upper right',
          ncol=3, fancybox=True, shadow=True)
'''
    if i<int(len(ax.lines)/2):
        ax.lines[i].set_linestyle('--')
        ax.lines[i].set_linewidth(4)
    elif i>=int(len(ax.lines)/2):
        ax.lines[i].set_linestyle('-')
        ax.lines[i].set_linewidth(4)
'''
ax2=fig.add_subplot(212,sharex=ax)
#ax2.plot(pdmean2.index,pdmean2.values)
ax2.plot(pdmean2.index,pdmean2['BA01surf'],color=color1)
ax2.plot(pdmean2.index,pdmean2['BA01bott'],color=color2)
ax2.set_ylabel('Temperature difference (degC)')
ax2.set_xlabel('Month')

for i in range(len(ax2.lines)):#plot in different ways
     ax2.lines[i].set_linewidth(4)
ax2.lines[0].set_linestyle('-')
ax2.lines[1].set_linestyle('--')
plt.title('observed minus model at BA01')
plt.grid()

#pdmean1.plot(figsize=(16,4),x_compat=True,grid=True,linewidth=3,title='Meandiff')
plt.show()
plt.savefig(outputplotdir+'fig7_modvsobs_surf_bot.png')
plt.savefig(outputplotdir+'fig7_modvsobs_surf_bot.eps')

