# -*- coding: utf-8 -*-
"""
@author: huanxin in Jan 2013
w/modifications by JiM
"""

print "    1= just codar (getcodar_byrange.ctl)  "
print "    2= codar and sst (getcodar_byrange.ctl)"
print "    3= codar and observed drifter (getcodar_bydrifter.ctl)"
print "    4= codar ,sst and observed drifter (getcodar_bydrifter.ctl)"
print "    5= modeled drifter based on codar (getcodar_bydrifter.ctl)"
print "    6= sst and observed drifter  (getcodar_bydrifter.ctl)"

#option=raw_input('\nMake a selection: ')
option='6'
if option=='1':
    execfile("getcodar.py")
if option=='2':
    execfile("getsst_codar.py")
if option=='3':
    execfile("getcodar_drifter.py")
if option=='4':
    execfile('getsst_codar_drifter.py')
if option=='5':
    execfile('gettrack_codar.py')
if option=='6':
    execfile('getsst_drifter.py')    
    
 