# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 13:47:20 2013

@author: jmanning
"""
from getdata import get_dataset
import datetime as dt
import numpy as np
from matplotlib.dates import num2date
def getobs_tempsalt(site,input_time,dep):
    """
    get data from url, return datetime, temperature, and start and end times
    input_time can either contain two values: start_time & end_time OR one value:interval_days
    """
    url = 'http://gisweb.wh.whoi.edu:8080/dods/whoi/emolt_sensor?emolt_sensor.SITE,emolt_sensor.YRDAY0_LOCAL,emolt_sensor.TIME_LOCAL,emolt_sensor.TEMP,emolt_sensor.DEPTH_I,emolt_sensor.SALT&emolt_sensor.SITE='
    dataset = get_dataset(url + '"' + site + '"')
    var = dataset['emolt_sensor']
    print 'extracting eMOLT data using PyDap... hold on'
    temp = list(var.TEMP)
    depth = list(var.DEPTH_I)
    time0 = list(var.YRDAY0_LOCAL)
    year_month_day = list(var.TIME_LOCAL)
    salt=list(var.SALT)
  
    print 'Generating a datetime ... hold on'
    datet = []
    for i in np.arange(len(time0)):
        #datet.append(num2date(time0[i]+1.0).replace(year=time.strptime(year_month_day[i], '%Y-%m-%d').tm_year).replace(day=time.strptime(year_month_day[i], '%Y-%m-%d').tm_mday))
        datet.append(num2date(time0[i]+1.0).replace(year=dt.datetime.strptime(year_month_day[i], '%Y-%m-%d').year).replace(month=dt.datetime.strptime(year_month_day[i],'%Y-%m-%d').month).replace(day=dt.datetime.strptime(year_month_day[i],'%Y-%m-%d').day).replace(tzinfo=None))
    #get the index of sorted date_time
    print 'Sorting mooring data by time'
    index = range(len(datet))
    index.sort(lambda x, y:cmp(datet[x], datet[y]))
    #reorder the list of date_time,u,v
    datet = [datet[i] for i in index]
    temp = [temp[i] for i in index]
    depth = [depth[i] for i in index]
    salt=[salt[i] for i in index]

    print 'Delimiting mooring data according to user-specified time'
    part_t,part_time,part_salt = [], [],[]
    if len(input_time) == 2:
        start_time = input_time[0]
        end_time = input_time[1]
    if len(input_time) == 1:
        start_time = datet[0]
        end_time = start_time + input_time[0]
    if len(input_time) == 0:
        start_time = datet[0]
        end_time=datet[-1]
    print datet[0], datet[-1]
    for i in range(0, len(temp)):
        if (start_time <= datet[i] <= end_time) & (dep[0]<=depth[i]<= dep[1]):
            part_t.append(temp[i])
            part_time.append(datet[i])
            part_salt.append(salt[i])
    temp=part_t
    datet=part_time
    salt=part_salt
    return datet,temp,salt