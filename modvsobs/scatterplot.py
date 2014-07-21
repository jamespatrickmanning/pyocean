# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 14:02:40 2013

@author: jmanning
"""

import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import numpy as np
from scipy import stats
from pylab import *

### HARDCODES ###
site=['AB01','BN01']#,'JS06']
outputplotdir='/net/nwebserver/epd/ocean/MainPage/modvsobs/figs/'
inputdir='/net/data5/jmanning/modvsobs/'
color1='black'
color2='gray'
####

for i in range(len(site)):
     dfmod=pd.read_csv(inputdir+site[i]+'botttemp_ma_mod.csv',index_col=0,names=['yy','mm','dd','count','mean','median','min','max','std'])
     dfobs=pd.read_csv(inputdir+site[i]+'botttemp_ma_obs.csv',index_col=0,names=['yy','mm','dd','count','mean','median','min','max','std'])
     obsvalues = dfobs['mean'].values
     obsvalues= obsvalues[np.isfinite(obsvalues)]
     modvalues = dfmod['mean'].values
     modvalues= modvalues[np.isfinite(modvalues)]
     gradient, intercept, r_value, p_value, std_err = stats.linregress(obsvalues,modvalues)
     print "Gradient and intercept", gradient, intercept
     print "R-squared", r_value**2
     print "p-value", p_value
     fig=plt.figure()
     ax=fig.add_subplot(111)
     for k in range(len(dfobs)):
          ax.plot(dfobs['mean'].values[k],dfmod['mean'].values[k],'o',color=color1) 
     fit = polyfit(obsvalues,modvalues,1)
     fit_fn = poly1d(fit)
     plot(obsvalues,modvalues, 'ko', obsvalues, fit_fn(obsvalues), '--k')
     xlim(0, int(max(obsvalues)+5))
     ylim(0, int(max(obsvalues)+5))
     diagnal=np.arange(0,int(max(obsvalues)+5))
     plt.plot(diagnal,'--',color=color1)  
     ax.text(.7, 1,"Gradient and intercept:"+str(gradient)[:4]+', '+str(intercept)[:4]+'\n'+'R-squared:'+str(r_value**2)[:4], style='italic',
        bbox={'facecolor':color2,'alpha':3.5, 'pad':30})
     ax.set_ylabel('mod temp(degreeC)')
     ax.set_xlabel('obs temp(degreeC)')
     plt.title(site[i]+' scatter plot')
     if i==0:
         aorb='a'
     else:
         aorb='b'
     plt.show()
     plt.savefig(outputplotdir+'fig8'+aorb+'_'+site[i]+'_scatter.png')
     plt.savefig(outputplotdir+'fig8'+aorb+'_'+site[i]+'_scatter.eps')

