# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 13:59:04 2013

Generates Figure 15 in 2013 version  which plots change in temp due to assimilation as a function if distance away from site

@author: yacheng and jmanning
"""

import pandas as pd
import matplotlib.pyplot as plt
ddir='/net/data5/jmanning/modvsobs/'
df=pd.read_csv(ddir+'BN01distance_affect.csv',index_col=0,names=['degree','meandiff','rms'])
df1=pd.read_csv(ddir+'TA14distance_affect.csv',index_col=0,names=['degree','meandiff','rms'])
df2=pd.read_csv(ddir+'JS06distance_affect.csv',index_col=0,names=['degree','meandiff','rms'])
fig=plt.figure()
plt.plot(df.degree.values,df.meandiff.values,'o-',color='blue',label='BN01') 
plt.plot(df1.degree.values,df1.meandiff.values,'o-',color='red',label='TA14') 
plt.plot(df2.degree.values,df2.meandiff.values,'o-',color='green',label='JS06')     
#plt.plot(df.degree.values,df.meandiff.values+df.rms.values,'--',color='blue',label="TA14") 
#plt.plot(df.degree.values,df.meandiff.values+df.rms.values,'--',color='blue',label="TA14") 
#plt.plot(df1.degree.values,df1.meandiff.values,'o-',color='red',label='BN01') 
#plt.plot(df2.degree.values,df2.meandiff.values,'o-',color='green',label='JS06')     
plt.grid()
plt.ylabel(r'$\|Model_{before} - Model_{after}\|$', fontsize=20)
plt.xlabel('degree distance',fontsize=20)
plt.title('Assimilation influence with distance',fontsize=20)
plt.legend()
plt.show() 
