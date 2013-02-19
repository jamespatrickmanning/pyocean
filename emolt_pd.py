
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 23 11:37:52 2013

@author: jmanning and Yacheng
"""
'''
Jan/17/2013
this program can read-in different formats files and plot 'Temp-TIME'or'Sali-TIME'or'Inti-TIME'figure, at the mean time generate output file.
step1:read-in data through 'pandas'
step2:choose the approximate start-end points
step3:zoom-in the start-end figure and choose the exactly points
step4:show the final figure and generate the output file.
'''
import pylab
from pylab import *
import pandas
import matplotlib.pyplot as plt
from pandas import *
import numpy as np
import datetime
from datetime import timedelta,datetime
from matplotlib.dates import num2date,date2num
import csv
from conversions import c2f
from utilities import my_x_axis_format
from mpl_toolkits.axes_grid1 import host_subplot
import string
import matplotlib.dates as dates

############## HARDCODES ##############
#Sc=raw_input("please input the sitecode:")
#dep=raw_input("please input the depth (fathoms) of instrument:")
#Ps=raw_input("please input the probsetting:")
#Sn=raw_input("please input the sErname:")
direct='/net/data5/jmanning/hobo/'
#direct='/net/home3/ocn/jmanning/py/yw/emolt/rawdata/'
diroutplt='/net/nwebserver/epd/ocean/MainPage/lob/'
#dirout='/net/data5/jmanning/minilog/dat/'
dirout='/net/data5/jmanning/hobo/'
fn='hbt0404.csv'
#direct='/net/data5/jmanning/minilog/asc/'
#direct='/net/home3/ocn/jmanning/py/yw/emolt/rawdata/'
#diroutplt='/net/nwebserver/epd/ocean/MainPage/lob/'
#dirout='/net/data5/jmanning/minilog/dat/'
#fn='mbn0111.csv'
#Sc='xx01'
Sc=fn[1:3].upper()+fn[3:5]
dep='8.7'
crit=3
#Ps='01'
Ps=fn[5:7]

############ define a def######################
def chooseSE(start,end,skipr):#this function employed to zoom-in picture and choose exactly points
      startfront=start[0]-2 # looking 2 day either side of the point clicked
      startback=start[0]+2
      sfforplot=(num2date(startfront)).replace(minute=0,second=0,microsecond=0).isoformat(" ")#transfer number to date and generate a appropriate date format
      sbforplot=(num2date(startback)).replace(minute=0,second=0,microsecond=0).isoformat(" ")
      ZIF=df[sfforplot[0:19]:sbforplot[0:19]]#get the DataFrame for zoom-in figure.
      fig = plt.figure()
      plt.plot(ZIF.index.to_pydatetime(),ZIF.values)
      #sfinal=pylab.ginput(n=1)#choose an exactly point.
      sfinal=ginput(n=1)#choose an exactly point.
      sfinaltime=(num2date(sfinal[0][0])).replace(tzinfo=None)
      sfinalforplot=sfinaltime.replace(minute=0,second=0,microsecond=0).isoformat(" ")
      print sfinalforplot
      plt.clf()
     #####for end point zoom figure###########
      #below coding is very similar with the up one, it employed to choose exactly point at the end side.
      endfront=end[0]-2 # looking 2 day either side of the point clicked
      endback=end[0]+2
      efforplot=(num2date(endfront)).replace(minute=0,second=0,microsecond=0).isoformat(" ")
      ebforplot=(num2date(endback)).replace(minute=0,second=0,microsecond=0).isoformat(" ")
      ZIB=df[efforplot[0:19]:ebforplot[0:19]]
      fig = plt.figure()
      plt.plot(ZIB.index.to_pydatetime(),ZIB.values)
      efinal=ginput(n=1)
      efinaltime=(num2date(efinal[0][0])).replace(tzinfo=None)
      efinalforplot=efinaltime.replace(minute=0,second=0,microsecond=0).isoformat(" ")
      print efinalforplot
      plt.clf()
     ######for the final figure################
      FF=df[sfinalforplot:efinalforplot]#FF is the DataFrame that include all the records you choosed to plot.
      criteria=crit*FF.values.std() # standard deviations
# criteria=FF.values.std()
      a=0
      for i in range(len(FF)-2):#replace the record value which exceed 3 times standard deviations by 'Nan'.
         diff1=abs(FF.values[i+1]-FF.values[i])
         diff2=abs(FF.values[i+2]-FF.values[i+1])
         if diff1 > criteria and diff2 > criteria:
                print str(FF.index[i])+ ' is replaced by Nan'
                a+=1
                FF.values[i+1]=float('NaN')
      print 'There are ' +str(a)+ ' points have replaced'
      if mark=='*' or mark=='S':
          dt=read_csv(direct+fn,sep=',',skiprows=skipr,parse_dates={'datet':[0,1]},index_col='datet',date_parser=parse,names=['Date','Time','RawTemp'])#creat a new Datetimeindex
      elif mark1=='Intensity':
          dr=read_csv(direct+fn,sep=',',skiprows=2,parse_dates={'datet':[1]},index_col='datet',names=['NO','DataTime','RawTemp','Intensity','CouplerDetached','CouplerAttached','Stopped','EndOfFile'])
          dt=DataFrame(dr['RawTemp'],index=dr.index)
      else:
          dr=read_csv(direct+fn,sep=',',skiprows=2,parse_dates={'datet':[1]},index_col='datet',names=['NO','DataTime','CondHighRng','RawTemp','Salinity','CouplerDetached','CouplerAttached','Stopped','EndOfFile'])
          dt=DataFrame(dr['RawTemp'],index=dr.index)
      draw=dt[sfinalforplot:efinalforplot]
      fig=plt.figure(figsize=(8,5))
      TimeDelta=FF.index[-1]-FF.index[0]
      ax = fig.add_subplot(111)
      my_x_axis_format(ax, TimeDelta)
      ax.set_ylim(min(FF.values),max(FF.values))
      ax.plot(draw.index.to_pydatetime(),draw.values,color='r',label="raw data")
      ax.set_ylabel('celsius')
      if FF.index[0].year<FF.index[-1].year:
         year=str(int(FF.index[0].year))+'-'+str(int(FF.index[-1].year))
      else:
         year=str(int(FF.index[0].year))
      ax.set_xlabel(year)
      #FT=[]
# for k in range(len(FF.index)):#convert C to F
      FT=c2f(FF['Temp'])
      #FT.append(f)
      ax2=ax.twinx()
      my_x_axis_format(ax2, TimeDelta)
      #print FT.min(0)
      ax2.set_ylim(min(FT[0]),max(FT[0]))
      ax2.plot(FT[0].index.to_pydatetime(),FT[0],color='b',label="clean data")
      ax2.set_ylabel('fahrenheit')
      lines, labels = ax.get_legend_handles_labels()
      lines2, labels2 = ax2.get_legend_handles_labels()
      ax2.legend(lines + lines2, labels + labels2, loc=0)
      plt.show()
# plt.tight_layout()
      return FF,FT
      
def chooseSE2(start,end):#this function employed to zoom-in picture and choose exactly points
      startfront=start[0]-2 # looking 2 day either side of the point clicked
      startback=start[0]+2
      sfforplot=(num2date(startfront)).replace(minute=0,second=0,microsecond=0).isoformat(" ")#transfer number to date and generate a appropriate date format
      sbforplot=(num2date(startback)).replace(minute=0,second=0,microsecond=0).isoformat(" ")
      ZIF=df[sfforplot[0:19]:sbforplot[0:19]]#get the DataFrame for zoom-in figure.
      fig = plt.figure()
      plt.plot(ZIF.index.to_pydatetime(),ZIF.values)
      #sfinal=pylab.ginput(n=1)#choose an exactly point.
      sfinal=ginput(n=1)#choose an exactly point.
      sfinaltime=(num2date(sfinal[0][0])).replace(tzinfo=None)
      sfinalforplot=sfinaltime.replace(minute=0,second=0,microsecond=0).isoformat(" ")
      print sfinalforplot
      #plt.close()
      plt.clf()
     #####for end point zoom figure###########
      #below coding is very similar with the up one, it employed to choose exactly point at the end side.
      endfront=end[0]-2 # looking 2 day either side of the point clicked
      endback=end[0]+2
      efforplot=(num2date(endfront)).replace(minute=0,second=0,microsecond=0).isoformat(" ")
      ebforplot=(num2date(endback)).replace(minute=0,second=0,microsecond=0).isoformat(" ")
      ZIB=df[efforplot[0:19]:ebforplot[0:19]]
      fig = plt.figure()
      plt.plot(ZIB.index.to_pydatetime(),ZIB.values)
      efinal=ginput(n=1)
      efinaltime=(num2date(efinal[0][0])).replace(tzinfo=None)
      efinalforplot=efinaltime.replace(minute=0,second=0,microsecond=0).isoformat(" ")
      print efinalforplot
      #plt.close()
      plt.clf()
     ######for the final figure################
      FF=df[sfinalforplot:efinalforplot]#FF is the DataFrame that include all the records you choosed to plot.
      criteria=crit*FF.values.std() # standard deviations
      #print criteria
      a=0
      print FF.values[1],FF.values[0]
      for i in range(len(FF)-2):#replace the record value which exceed 3 times standard deviations by 'Nan'.
         diff1=abs(FF.values[i+1]-FF.values[i])
         diff2=abs(FF.values[i+2]-FF.values[i+1])
         if (diff1 > criteria) and (diff2 > criteria):
              print str(FF.index[i])+ ' is replaced by Nan'
              a+=1
              FF.values[i+1]=float('NaN')
         if i==0:
             print 'now '+str(diff1)
         if (diff1 >criteria) and (i==0):       
              print str(FF.index[i])+ ' is replaced by Nan'
              a+=1
              FF.values[i]=float('NaN')
      print 'There are ' +str(a)+ ' points have replaced'
      fig=plt.figure(figsize=(8,5))
      TimeDelta=FF.index[-1]-FF.index[0]
      ax = fig.add_subplot(111)
      my_x_axis_format(ax, TimeDelta)
      ax.set_ylim(min(FF['Salinity'].values),max(FF['Salinity'].values))
      ax.plot(FF.index.to_pydatetime(),FF.values,color='r',label="raw data")
      ax.set_ylabel('Salinity')
      if FF.index[0].year<FF.index[-1].year:
         year=str(int(FF.index[0].year))+'-'+str(int(FF.index[-1].year))
      else:
         year=str(int(FF.index[0].year))
      ax.set_xlabel(year)
      #FF.plot()
      return FF
def getyearday(FF):#generating 'yd1' which is a number from 0-366.
      y=[]
      m=[]
      d=[]
      hh=[]
      mm=[]
      yd=[]
      for i in range(len(FF[0])):#get the separate year,month,day,hour,minute
          strindex=str(FF[0].index[i])
          y.append(strindex[0:4])
          m.append(strindex[5:7])
          d.append(strindex[8:10])
          hh.append(strindex[11:13])
          mm.append(strindex[14:16])
      for j in range(len(FF[0])):#minus to get the number 0-366
          a=date2num(datetime(int(y[j]),int(m[j]),int(d[j]),int(hh[j]),int(mm[j])))
          b=date2num(datetime(int(y[j]),1,1,0,0))
          yd.append(a-b)
      del y,m,d,hh,mm
      return yd
def outfomat(PFDATA):#generating the format of output file
      output_fmt=['sitecode','sernum','probsetting','Datet','yearday','Temp','Salinity','depth']
      PFDATADF=DataFrame(PFDATA)#convert Series to DataFrame
      PFDATADFNEW=PFDATADF.reindex(columns=output_fmt)
# PFDATADFNEW.to_csv(fn[0:-4]+'.csv',float_format='%10.2f',index=False)
      print "output file is ready!"
      return PFDATADFNEW
def saveTemFig(diroutplt):
     plt.savefig(diroutplt+fn[0:-4]+'.png')
     plt.savefig(diroutplt+fn[0:-4]+'.ps')

#################################################################################################
#f=open('/net/home3/ocn/jmanning/py/yw/emolt/rawdata/'+fn)
f=open(direct+fn)
lines=f.readlines()
mark=lines[0][0]
mark1=lines[1][39:48]
Sn=lines[1][16:20]
Sn1=lines[0][17:21]
Sn2=lines[0][13:21]
if mark=='*' or mark=='S':#if the input file start with the character '*',choose the first method to read-in data.
      def parse(datet):
      #print datet[0:10],datet[11:13],datet[14:16]
        dt=datetime.strptime(datet[0:10],'%Y-%m-%d')
        delta=timedelta(hours=int(datet[11:13]),minutes=int(datet[14:16]))
        return dt+delta
      if mark=='*': # case of old minilog program output
          skipr=7
      else: # case of new LoggerVue output
          skipr=8
          Sn=lines[1][25:29] # serieal number is reassigned
      df=read_csv(direct+fn,sep=',',skiprows=skipr,parse_dates={'datet':[0,1]},index_col='datet',date_parser=parse,names=['Date','Time','Temp'])#creat a new Datetimeindex
      default=0
      fixtime=raw_input('Enter the number of hours to shift: ')
      if not fixtime:
          fixtime=default
      df.index=df.index+timedelta(hours=int(fixtime))
      fig = plt.figure(figsize=(12,4))
# plt.figure()
      plt.plot(df.index.to_pydatetime(),df.values)
      print "click on start and stop times to save date"
      [start,end]=ginput(n=2)
 # plt.close()
      plt.clf()
      FF,FT=chooseSE(start,end,skipr)#calling the chooseSE function.
# plt.show()
      saveTemFig(diroutplt)#dirout
     ############generate the yeardays##############
      yd=getyearday(FF)#calling the getyearday function.
     #############c to f##################
# FT=[]
# for k in range(len(FF.index)):#convert C to F
# f=c2f(FF['Temp'][k])
# FT.append(f)
     ############output file###################
      PFDATA={'sitecode':Series(Sc,index=FF.index),#creat the format
              'depth':Series(dep,index=FF.index),
              'sernum':Series(Sn,index=FF.index),
              'probsetting':Series(Ps,index=FF.index),
              'Temp':Series(FT[0].values,index=FF.index),
              'Salinity':Series('99.999',index=FF.index),
              'Datet':Series(FF.index,index=FF.index),
              'yearday':Series(yd,index=FF.index)}
      PFDATADFNEW=outfomat(PFDATA)
      PFDATADFNEW.to_csv(dirout+string.upper(fn[1:5])+'m'+Sn+Ps.zfill(2)+fn[3:5]+'.dat',float_format='%10.2f',index=False,header=False)
      plt.show()
      
#below is the repeat.
elif mark1=='Intensity':# if input file have the character'Intensity',call this method.
      dr=read_csv(direct+fn,sep=',',skiprows=2,parse_dates={'datet':[1]},index_col='datet',names=['NO','DataTime','Temp','Intensity','CouplerDetached','CouplerAttached','Stopped','EndOfFile'])
      df=DataFrame(dr['Temp'],index=dr.index)
      fig = plt.figure(figsize=(12,4))
# fig = plt.figure()
      plt.plot(df.index.to_pydatetime(),df.values)
      print "click on start and stop times to save date"
      [start,end]=pylab.ginput(n=2)
      #plt.close()
      plt.clf()
      FF=chooseSE(start,end)
      saveTemFig(diroutplt)
      ############generate the yeardays##############
      yd=getyearday(FF)
     #############c to f##################
      FT=[]
      f=c2f(FF['Temp'][k])
      FT.append(f)
     ############output file###################
      PFDATA={'sitecode':Series(Sc,index=FF.index),
              'depth':Series(dep,index=FF.index),
              'sernum':Series(Sn1,index=FF.index),
              'probsetting':Series(Ps,index=FF.index),
              'Temp':Series(FT[0].values,index=FF.index),
              'Salinity':Series('99.999',index=FF.index),
              'Datet':Series(FF.index,index=FF.index),
              'yearday':Series(yd,index=FF.index)}
      PFDATADFNEW=outfomat(PFDATA)
      PFDATADFNEW.to_csv(dirout+fn[0:-4]+'.csv',float_format='%10.2f',index=False)
      plt.show()
      

      Q=raw_input("Do you want to plot Intensity figrue? y/n")
      if Q=='y'or'Y':
          df=DataFrame(dr['Intensity'],index=dr.index)
          fig = plt.figure(figsize=(12,4))
# fig = plt.figure()
          plt.plot(df.index.to_pydatetime(),df.values)
          print "click on start and stop times to save date"
          [start,end]=pylab.ginput(n=2)
          #plt.close()
          plt.clf()
          FF=chooseSE2(start,end)
          plt.savefig(diroutplt+fn[0:-4]+'Intensity.png')
          plt.show()
else:# this is the third method to read-in data.
      skipr=5
      dr=read_csv(direct+fn,sep=',',skiprows=2,parse_dates={'datet':[1]},index_col='datet',names=['NO','DataTime','CondHighRng','Temp','Salinity','CouplerDetached','CouplerAttached','Stopped','EndOfFile'])
      df=DataFrame(dr['Temp'],index=dr.index)
      fig = plt.figure(figsize=(12,4))
# fig = plt.figure()
      plt.plot(df.index.to_pydatetime(),df.values)
      print "click on start and stop times to save date"
      [start,end]=pylab.ginput(n=2)
      #plt.close()
      plt.clf()
      FF=chooseSE(start,end,skipr)
      saveTemFig(diroutplt)
    ############generate the yeardays##############
      print FF
      yd=getyearday(FF)
    #############c to f##################
      #FT=[]
      FT=c2f(FF[0]['Temp'])
      #FT.append(f)
     ############output file###################

      PFDATA={'sitecode':Series(Sc,index=FF[0].index),
              'depth':Series(dep,index=FF[0].index),
              'sernum':Series(Sn1,index=FF[0].index),
              'probsetting':Series(Ps,index=FF[0].index),
              'Temp':Series(FT[0].values,index=FF[0].index),
              'Salinity':Series(dr['Salinity'],index=FF[0].index),
              'Datet':Series(FF[0].index,index=FF[0].index),
              'yearday':Series(yd,index=FF[0].index)}
      PFDATADFNEW=outfomat(PFDATA)
      PFDATADFNEW.to_csv(dirout+string.upper(fn[1:5])+'h'+Sn1+Ps.zfill(2)+fn[3:5]+'.dat',float_format='%10.2f',index=False,header=False)
      #PFDATADFNEW.to_csv(dirout+fn[0:-4]+'.csv',float_format='%10.2f',index=False)
      plt.show()
      
      Q=raw_input("Do you want to plot Salinity figrue? y/n: ")
      
      if Q=='y'or'Y':
          df=DataFrame(dr['Salinity'],index=dr.index)
          fig = plt.figure(figsize=(12,4))
# fig = plt.figure()
          plt.plot(df.index.to_pydatetime(),df.values)
          print "click on start and stop times to save date"
          [start,end]=pylab.ginput(n=2)
          #plt.close()
          plt.clf()
          FF=chooseSE2(start,end)
          plt.savefig(diroutplt+fn[0:-4]+'Salinity.png')
          plt.show()
          