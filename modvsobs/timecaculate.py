# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 10:50:31 2013

@author: jmanning
"""
import pandas as pd
from datetime import datetime, timedelta
import datetime as dt
from pydap.client import open_url
from pylab import unique
##########################################
minhour=12
minday=24
minyear=6
minmonthcount=6
##########################################
f = open('timereport.csv', 'w')
#g=open('timereportsite.csv','w')
'''
urllatlon = 'http://gisweb.wh.whoi.edu:8080/dods/whoi/emolt_site?emolt_site.SITE'
dataset = open_url(urllatlon)
print dataset
var = dataset['emolt_site']
SITE = list(var.SITE)
print "SITE list has been generated"
#for i in range(len([0,1])):
'''   
SITE=['AB01','AG01','BA01','BA02','BC01','BD01','BF01','BI02','BI01','BM01','BM02','BN01','BS02','CJ01','CP01','DC01','DJ01','DK01','DMF1','ET01','GS01','JA01','JC01','JS06','JT04','KO01','MF02','MM01','MW01','NL01','PF01','PM02','PM03','PW01','RA01','RM02','RM04','SJ01','TA14','TA15','TS01']
for i in range(len(SITE)):   
    print SITE[i]
    url='http://gisweb.wh.whoi.edu:8080/dods/whoi/emolt_sensor?emolt_sensor.TIME_LOCAL&emolt_sensor.SITE='
    dataset=open_url(url+'"'+SITE[i]+'"')
    var=dataset['emolt_sensor']
    print 'hold on  ... extracting your eMOLT mooring data'
    year_month_day = list(var.TIME_LOCAL)
    timelocal=[]
    for j in range(len(year_month_day)):
         timelocal.append(datetime.strptime(year_month_day[j],"%Y-%m-%d"))  
    index = range(len(timelocal))
    index.sort(lambda x, y:cmp(timelocal[x], timelocal[y]))
    timelocal = [timelocal[ii] for ii in index]
    print 'now generating a datetime'
    timepd=pd.DataFrame(range(len(timelocal)),index=timelocal)
    timepd['Year']=timepd.index.year
    year=unique(timepd['Year'])
    monthall=[]
    if len(year)>=minyear:
        for k in range(len(year)):
            timemonth=timepd.ix[timepd.index.year==year[k]]
            timemonth=timemonth.resample('m',how=['count'],kind='period')
            timemonth=timemonth.ix[timemonth[0,'count']>minhour*minday]
            month=unique(timemonth.index.month)
            print year[k],month
#            f.write(str(SITE[i])+','+str(year[k])+','+str(month)+'\n')
            monthall.append(month)
        common=[]
        for jj in range(1,13):
                num=0
                for kk in range(len(monthall)):
                    if jj in monthall[kk]:
                        num+=1
                if num>=minyear:
                    print jj
                    common.append(jj)
#        f.write(str(common)+'\n')
#        print len(common)
    if len(year)>=minyear and len(common)>=minmonthcount:
        for k in range(len(year)):
            timemonth=timepd.ix[timepd.index.year==year[k]]
            timemonth=timemonth.resample('m',how=['count'],kind='period')
            timemonth=timemonth.ix[timemonth[0,'count']>minhour*minday]
            month=unique(timemonth.index.month)
            f.write(str(SITE[i])+','+str(year[k])+','+str(month)+'\n')            
        f.write('common month nomber:'+str(len(common))+str(common)+'\n')
#             g.write(str(SITE[i])+'\n')    
f.close()
#g.close()
#    timeclassify=timeclassify.ix[timeclassify[0,'count']>minhour*minday]
