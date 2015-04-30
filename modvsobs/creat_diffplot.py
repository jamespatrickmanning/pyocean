# -*- coding: utf-8 -*-
"""
Created on Thu Feb 21 15:12:47 2013

@author: yacheng and jmanning
plot obs minus model monthly means at X number of sites
generates Fig 5 in manuscript
"""

import pandas as pd
from pandas.core.common import save
import matplotlib.pyplot as plt

#### HARDCODES ###########
inputdir='/net/data5/jmanning/modvsobs/'
outputplotdir='/net/nwebserver/epd/ocean/MainPage/modvsobs/figs/'
#site=['AB01','BA01','BA02','BA03','BF01','BI01','BM01','BN01','CP01','DC01','DJ01']
#site=['AB01','BF01','BM01','BN01','CP01','DC01','DJ01']
site=['AB01','BN01','JS06']
color1='black' #otherwise blue
###############################
if color1=='black':
  color2='black'
  color3='black'
else:
  color2='green'
  color3='red'
df1=pd.read_csv(inputdir+site[0]+'botttemp_mc_mod_mc_obs.csv',index_col=0)
dfmean1=-df1['mean']      
dfstd1=df1['std']
pdmean1=pd.DataFrame(dfmean1,index=df1.index)
pdstd1=pd.DataFrame(dfstd1,index=df1.index)
pdmean1.columns=[site[0]]
pdstd1.columns=[site[0]]
for k in range(len(site)):
    if k!=0:
        #df=pd.read_csv(site[k]+'_wtmp_mc_mod_mc_obs.csv',index_col=0)
        df=pd.read_csv(inputdir+site[k]+'botttemp_mc_mod_mc_obs.csv',index_col=0)
        dfmean=-df['mean']
        dfstd=df['std']
        pdmean=pd.DataFrame(dfmean,index=df.index)
        pdstd=pd.DataFrame(dfstd,index=df.index)
        pdmean.columns=[site[k]]
        pdstd.columns=[site[k]]
        pdmean1=pdmean1.join(pdmean)
        pdstd1=pdstd1.join(pdstd)
#print pdmean1
#pdmean1.to_csv(inputdir+'totalplot.csv',index=True)
#htmlmean=pdmean1.to_html(header=True,index=True)
#save(htmlmean,inputdir+'totalplot.html')
fig=plt.figure()
ax=fig.add_subplot(111)
ax.set_ylabel('Temperature difference (degC)')
ax.set_xlabel('Month')
lines=['--','-',':']
colors=[color1,color2,color3]
for i in range(len(site)):#plot in different ways
    ax.errorbar(pdmean1.index,pdmean1[pdmean1.columns[i]],yerr=pdstd1[pdstd1.columns[i]],
                linestyle=lines[i],color=colors[i],linewidth=4,elinewidth=1)    #here divide 2 because don`t want make std too confused in picture
patches,labels=ax.get_legend_handles_labels()
#ax.legend(set(tso['Year'].values),loc='center left', bbox_to_anchor=(.05, 0.5))
ax.legend(site,loc='best')
#plt.grid()
#plt.title('Model vs Observed Mthly Means at eMOLT sites')
plt.title('Modeled minus observed monthly means')
#pdmean1.plot(figsize=(16,4),x_compat=True,grid=True,linewidth=3,title='Meandiff')
plt.show()
plt.savefig(outputplotdir+'fig5_emoltvsnecofs_diff.png')
plt.savefig(outputplotdir+'fig5_emoltvsnecofs_diff.eps')
