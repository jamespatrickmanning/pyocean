# -*- coding: utf-8 -*-
"""
Created on Tue Dec 24 10:41:05 2013

@author: jmanning
"""

import pandas as pd
of=open('sitelist.dat','w')
df=pd.read_csv('/net/home3/ocn/jmanning/py/yw/gmri_2013/totalcaculate.csv')
for k in range(len(df)):
    print df['site'][k]+','
    of.write(df['site'][k]+',')
of.close()    