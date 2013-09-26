# -*- coding: utf-8 -*-
"""
Created on Tue May 14 10:32:46 2013

@author: hxu
"""
from matplotlib.dates import date2num, num2date
import datetime as dt

import matplotlib.mlab as ml
import numpy as np
from pydap.client import open_url
from pandas import *

def get_neracoos_ctl(inputfilename):# get data input from a txt file
   f=open(inputfilename)  
   select=f.readline()
   select=select[0:select.index(']')].strip('[').split(' ')
   select1=select[0]
   select2=select[1]
   select3=select[2]
   
   if select1 =='1':# get time period
       dtime=f.readline()
       dtime=dtime[0:dtime.index(']')].strip('[').split(';')
       mindtime=dt.datetime.strptime(dtime[0],'%Y,%m,%d,%H,%M')
       maxdtime=dt.datetime.strptime(dtime[1],'%Y,%m,%d,%H,%M') 
   else:
       dtime=f.readline()
       mindtime=dt.datetime.strptime('2001,1,1,0,0','%Y,%m,%d,%H,%M')
       maxdtime=dt.datetime.strptime('2017,1,1,0,0','%Y,%m,%d,%H,%M') #w
   model=f.readline() #get mooring model
   model=model[0:model.index(']')].strip('[')
   if select2 =='1': #get depth_range
       idepth=f.readline()
       idepth=idepth[0:idepth.index(']')].strip('[').split(',')
       i_mindepth=float(idepth[0])
       i_maxdepth=float(idepth[1])
   else:
       i_mindepth=0
       i_maxdepth=2000
       dtime=f.readline()
       
   if select3 =='1': #get sites
       site=f.readline()
       sites=site[0:site.index(']')].strip('[').split(',') 
   else:
       site=f.readline()
       site=''
       
   return  mindtime,maxdtime,i_mindepth,i_maxdepth,model,sites
def get_neracoos_ctl_id(url,datetime_wanted): #accroding time you input,get a index of that
    
        dtime=open_url(url+'?time')
        #dd=dtime['time']
        ddd=[]
        for i in list(dtime['time']):
            i=round(i,7)
            ddd.append(i)
        #print "This option has data from "+str(num2date(dd[0]+date2num(datetime.datetime(2001, 1, 1, 0, 0))))+" to "+str(num2date(dd[-1]+date2num(datetime.datetime(2001, 1, 1, 0, 0)))) 
        #print 'This option has data from '+num2date(dd[0]).strftime("%B %d, %Y")+' to '+num2date(dd[-1]).strftime("%B %d, %Y")          
        f = lambda a,l:min(l,key=lambda x:abs(x-a)) #match datetime_wanted
        datetime_wanted=f(datetime_wanted, ddd)
        id=[i for i,x in enumerate(ddd) if x == datetime_wanted]       
        #id=ml.find(np.array(ddd)==round(datetime_wanted,7))
        #id_max=ml.find(np.array(ddd)==round(max(ddd),7))
        for i in id:
          id=str(i) 
        #print 'codar id is  '+id

        return id
def get_neracoos_ctl_id_max(url):  #get the max datetime , min datetime and index of max datetime
        try:
            dtime=open_url(url+'?time')
        except:
            print 'no data that you want in this '+url
            
            return '','',''
        ddd=[]
        for i in list(dtime['time']):
            i=round(i,7)
            ddd.append(i)
            
        #print "This option has data from "+str(num2date(dd[0]+date2num(datetime.datetime(2001, 1, 1, 0, 0))))+" to "+str(num2date(dd[-1]+date2num(datetime.datetime(2001, 1, 1, 0, 0)))) 
        #print 'This option has data from '+num2date(dd[0]).strftime("%B %d, %Y")+' to '+num2date(dd[-1]).strftime("%B %d, %Y")  
                
        #id_max=[m for m,x in enumerate(ddd) if x == 1]     
        id_max=ml.find(np.array(ddd)==round(max(ddd),7)) # match the lastest datetime
        for i in id_max:
          id_max=str(i) 
        #print 'codar id is  '+id

        return id_max,max(ddd),min(ddd)
def get_id_s_id_e_id_max_url(url,sdtime_n,edtime_n): # get id of start time and end time, and get max datetime , min datetime and index of max datetime from get_neracoos_ctl_id
        id_max_url,maxtime,mintime=get_neracoos_ctl_id_max(url)
        if sdtime_n<mintime:
            id_s=0
            if edtime_n<mintime:
                id_e=''
            if mintime<=edtime_n<=maxtime:
                id_e=get_neracoos_ctl_id(url,edtime_n)
            if edtime_n>maxtime:
                id_e=id_max_url
        if mintime<=sdtime_n<=maxtime:
            id_s=get_neracoos_ctl_id(url,sdtime_n)
            if mintime<=edtime_n<=maxtime:
                id_e=get_neracoos_ctl_id(url,edtime_n)
            if edtime_n>maxtime:
                id_e=id_max_url
        if sdtime_n>maxtime:
            id_s=''
            id_e=''
        
        return id_s,id_e,id_max_url,maxtime,mintime
def get_depth_index(i_mindepth,i_maxdepth,depth_box): #this function works for "depth_select",According depth range you input, get depth which we have
    depth_index1=ml.find(depth_box<=i_maxdepth)
    depth_index2=ml.find(depth_box>=i_mindepth)
    depth_index=list(set(depth_index2).intersection(set(depth_index1)))
    return depth_index
'''
def depth_add(depth_box):
   depth_index=ml.find(i_mindepth<=depth_box<=i_maxdepth)
   for i in depth_index:
       depths.append(depth_box[depth_index])
   return depths
'''
def depth_select(sites,i_mindepth,i_maxdepth): #select depth which we have in web . 
    depths=[]
    site_d=[]
    for k in range(len(sites)):
        if sites[k]=='A01' or 'B01' or 'E01' or 'E02' or 'F01' or 'I01':
            
            depth_box=[1,20,50]
            depth_index=[i for i,x in enumerate(depth_box) if i_maxdepth >= x >=i_mindepth] #split sites in different depth
            for i in depth_index:
                depths.append(str(depth_box[i]))
                site_d.append(sites[k])
        if sites[k]=='D02':
            depth_box=[1,2,10]
            depth_index=[i for i,x in enumerate(depth_box) if i_maxdepth >= x >=i_mindepth]
            for i in depth_index:
                depths.append(str(depth_box[i]))
                site_d.append(sites[k])
        if sites[k]=='F02':
            depth_box=[1]
            depth_index=[i for i,x in enumerate(depth_box) if i_maxdepth >= x >=i_mindepth]
            for i in depth_index:
                depths.append(str(depth_box[i]))
                site_d.append(sites[k])
        if sites[k]=='M01':
            depth_box=[1,20,50,100,150,200,250,283]
            depth_index=[i for i,x in enumerate(depth_box) if i_maxdepth >= x >=i_mindepth]
            for i in depth_index:
                depths.append(str(depth_box[i]))
                site_d.append(sites[k])
        if sites[k]=='N01':
            depth_box=[1,20,50,100,150,180]
            depth_index=[i for i,x in enumerate(depth_box) if i_maxdepth >= x >=i_mindepth]
            for i in depth_index:
                depths.append(str(depth_box[i]))
                site_d.append(sites[k])
        '''
        else:
            print sites[k]+' is not here,please check  your input '
        '''
    return depths,site_d
def get_neracoos_temp_data(url,id_s,id_e,id_max_url): #get temperature data from neracoos.
          url=url+'temperature[0:1:'+id_max_url+'][0:1:0][0:1:0][0:1:0]'
          database=open_url(url)['temperature'][int(id_s):int(id_e)]
          #lat=database['lat']
          #lat=round(lat[0],2)
          #lon=database['lon']
          #lon=round(lon[0],2)
          depth=database['depth']
          period=database['time']
          temp=database['temperature']
          temp=temp[0:].tolist()
          period=num2date(period[0:]+date2num(dt.datetime(1858, 11, 17, 0, 0)))
          period_str,depth_temp=[],[]
    
          for i in range(len(period)): #convert format to list
             period_str.append(dt.datetime.strftime(period[i],'%Y-%m-%d-%H-%M'))
           
             depth_temp.append([round(depth[0],1),round(temp[i][0][0][0],2)])
          temp1=[] #get rid of bad data
          for i in range(len(depth_temp)):
            temp1.append(depth_temp[i][1])
      
          id_bad=ml.find((np.array(temp1)>30) | (np.array(temp1)<-4))
          #print id_bad
          id_bad=list(id_bad)
          id_bad.reverse()
          for m in id_bad:
             del period_str[m]
             del depth_temp[m]
          for i in range(len(depth_temp)):
              if i>=len(depth_temp):
                  break
              if abs(depth_temp[i-1][1]-depth_temp[i][1])>2:
                  del depth_temp[i]
                  del period_str[i]
                  depth_temp=depth_temp    
                  period_str=period_str
                  i=i-1
          #df=DataFrame(np.array(depth_temp),index=period_str,columns=['depth','temp','lat','lon'])
          return depth_temp,period_str
def get_neracoos_wind_data(url,id_s,id_e,id_max_url): #get wind data from neracoos.
         url1=url+'wind_speed[0:1:'+id_max_url+'][0:1:0][0:1:0][0:1:0],wind_direction[0:1:'+id_max_url+'][0:1:0][0:1:0][0:1:0]'
         database_s=open_url(url1)['wind_speed'][int(id_s):int(id_e)]
         database_d=open_url(url1)['wind_direction'][int(id_s):int(id_e)]
         #lat=database_s['lat']
         #lat=round(lat[0],2)
         #lon=database_s['lon']
         #lon=round(lon[0],2)
         depth=database_s['wind_depth']
         period=database_s['time']
         speed=database_s['wind_speed']
         speed=speed[0:].tolist()
         period=num2date(period[0:]+date2num(dt.datetime(1858, 11, 17, 0, 0)))
         direction=database_d['wind_direction']
         direction=direction[0:].tolist()
         period_str,wind_all=[],[]
         for i in range(len(period)): #convert format to list
             period_str.append(dt.datetime.strftime(period[i],'%Y-%m-%d-%H-%M'))
             wind_all.append([round(depth[0],1),round(speed[i][0][0][0],2),round(direction[i][0][0][0],2)])
         wind,direction=[],[] # figure out bad data and delete
         for i in range(len(wind_all)):
           wind.append(wind_all[i][1])
           direction.append(wind_all[i][2])
         id_bad=ml.find((np.array(wind)>300) | (np.array(wind)<-1) | (np.array(direction)<0)| (np.array(direction)>360))
         #print id_bad
         id_bad=list(id_bad)
         id_bad.reverse()
         for m in id_bad:
            del period_str[m]
            del wind_all[m]
         return period_str,wind_all
def get_neracoos_current_data(url,id_s,id_e,id_max_url): #get wind data from neracoos.
         url1=url+'current_speed[0:1:'+id_max_url+'][0:1:0][0:1:0][0:1:0],current_direction[0:1:'+id_max_url+'][0:1:0][0:1:0][0:1:0],current_u[0:1:'+id_max_url+'][0:1:0][0:1:0][0:1:0],current_v[0:1:'+id_max_url+'][0:1:0][0:1:0][0:1:0]'
         database_s=open_url(url1)['current_speed'][int(id_s):int(id_e)] 
         database_d=open_url(url1)['current_direction'][int(id_s):int(id_e)]
         database_u=open_url(url1)['current_u'][int(id_s):int(id_e)]
         database_v=open_url(url1)['current_v'][int(id_s):int(id_e)]
         #lat=database_s['lat']
         #lat=round(lat[0],2)
         #lon=database_s['lon']
         #lon=round(lon[0],2)
         
         period=database_s['time']
         speed=database_s['current_speed']
         speed=speed[0:].tolist()
         period=num2date(period[0:]+date2num(dt.datetime(1858, 11, 17, 0, 0)))
         direction=database_d['current_direction']
         direction=direction[0:].tolist()
         u=database_u['current_u']
         u=u[0:].tolist()    
         v=database_v['current_v']
         v=v[0:].tolist() 
         period_str,current_all=[],[]
         for i in range(len(period)): #convert format to list
             period_str.append(dt.datetime.strftime(period[i],'%Y-%m-%d-%H-%M'))
             current_all.append([round(speed[i][0][0][0],2),round(direction[i][0][0][0],2),round(u[i][0][0][0],2),round(v[i][0][0][0],2)])
         current,u,v,direction=[],[],[],[]# figure out bad data and delete
         for i in range(len(current_all)):
             current.append(current_all[i][0])
             direction.append(current_all[i][1])
             u.append(current_all[i][2])
             v.append(current_all[i][3])
         id_bad=ml.find((np.array(current)>200) | (np.array(current)<-1)|(np.array(direction)<0)| (np.array(direction)>360)|(np.array(u)<-200)| (np.array(u)>200)|(np.array(v)<-200)| (np.array(v)>200))
         #print id_bad
         id_bad=list(id_bad)
         id_bad.reverse()
         for m in id_bad:
            del period_str[m]
            del current_all[m]         
         return period_str,current_all
         
         
         
         
         
         
         
         
         
         
         
         
         
         
         