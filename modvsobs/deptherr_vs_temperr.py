# -*- coding: utf-8 -*-
"""
Created on Fri Mar 21 11:50:39 2014

compares depth error with temperature error

@author: jmanning
"""
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

dft=pd.read_csv('/net/data5/jmanning/modvsobs/totalcalculate_25Mar2014.csv',index_col=0)
dfd=pd.read_csv('/net/data5/jmanning/modvsobs/compare_depths.out',index_col=0)
f=plt.figure()
ax1=f.add_subplot(211)
ax2=f.add_subplot(212)
for k in range(len(dft)):
   for j in range(len(dfd)):
       if dft.index[k]==dfd.index[j]:
           #plt.plot(dft['mean'][k],abs(dfd['perc_diff'][j]),'*')
           ax1.plot(dft['mean'][k],dfd['perc_diff'][j],'*')
           #ax1.annotate(dft.index[k],(dft['mean'][k],dfd['perc_diff'][j]),fontsize=6)
           ax2.plot(dft['rms'][k],dfd['perc_diff'][j],'*')
           #ax2.annotate(dft.index[k],(dft['rms'][k],dfd['perc_diff'][j]),fontsize=6)
plt.xlabel('mean temperature diff')
plt.ylabel('mean depth diff')
plt.show()
plt.savefig('/net/nwebserver/epd/ocean/MainPage/modvsobs/deptherr_vs_temperr.png')

