import matplotlib.pyplot as plt
from matplotlib.dates import  DateFormatter, WeekdayLocator, MONDAY,date2num,num2date
import matplotlib as mpl
import numpy as np
import time
import datetime as dt
def set_date_locator(xaxis):

   # locator = mpl.dates.AutoDateLocator()
  #  xaxis.set_major_locator(locator)
  #  Formatter = mpl.dates.AutoDateFormatter(locator, tz=None)
    mondays = WeekdayLocator(MONDAY)        # major ticks on the mondays
    #alldays    = DayLocator()              # minor ticks on the days
    #ask_axis=raw_input("do you want display 'year' on xaxis?")
    ask_axis="n"
    if ask_axis=="y":
        weekFormatter = DateFormatter('%b %d %Y')
    else:
        weekFormatter = DateFormatter('%b %d')  # Eg, Jan 12
   #    weekFormatter = DateFormatter('%b %d %Y')  # Eg, Jan 12
   # dayFormatter = DateFormatter('%d')  
    # edit the format strings to remove the TZ spec
    # this only works with my cutom version of AutoDateLocator

    xaxis.set_major_formatter(weekFormatter)
   # xaxis.set_major_locator(alldays)
    xaxis.set_minor_locator(mondays)
    
    
# lat,lon and quiver plot (u and v)
def multiple_stick_plot(jd_num_year,y,u,v,lon,lat,yeartime):# jd_num_year is a list of time, y is a list of 0
  fig=plt.figure()
  ax1=fig.add_subplot(211)
  ax1.set_xlabel('Longitude N')
  ax1.set_ylabel('Latitude W')
  ax1.plot(lon,lat, color = 'blue', lw = 1)
  plt.title("stick plot",fontsize=30,color="red")
  ax = fig.add_subplot(212)
  ax.quiver(jd_num_year,y,u,v,scale=450,color="blue")
  fig.autofmt_xdate()
  set_date_locator(ax.xaxis)
  plt.grid(True)
  ax.set_xlabel(yeartime,fontsize=17)
  ax.set_ylabel('m/s',fontsize=17)
  plt.show()
  
  # quiver plot:multiple pannels, uu,vv is moving average 
def multiple_panels_movavg_plot(jd_num_year,y,u,v,uu,vv,yeartime,filename):
  #yeartime is year, jd_num_year is a list of number yearday.
  # jd_num_year is a list of time, y is a list of 0
  plots_of_quiver=raw_input("how many panels should be an input?")
  yd_per_panel=len(jd_num_year)/int(plots_of_quiver)
  fig=plt.figure()
  for ii in range(1, int(plots_of_quiver)+1):
    subplot_num=plots_of_quiver+"1"+str(ii)
    jd_num_year_i=jd_num_year[yd_per_panel*(ii-1):yd_per_panel*ii]
    y_i=y[yd_per_panel*(ii-1):yd_per_panel*ii]
    u_i=u[yd_per_panel*(ii-1):yd_per_panel*ii]
    v_i=v[yd_per_panel*(ii-1):yd_per_panel*ii]
    uu_i=uu[yd_per_panel*(ii-1):yd_per_panel*ii]
    vv_i=vv[yd_per_panel*(ii-1):yd_per_panel*ii]
    ax = fig.add_subplot(int(subplot_num))
    p=ax.quiver(jd_num_year_i,y_i,u_i,v_i,scale=450,color="blue")
    q=ax.quiver(jd_num_year_i,y_i,uu_i,vv_i,scale=450,color="red")
    ax.axis(xmin=jd_num_year[yd_per_panel*(ii-1)],xmax=jd_num_year[yd_per_panel*ii])
    set_date_locator(ax.xaxis)
    if ii==1:
          ax.quiverkey(q,0.90,1.09,30,
                    label="moving average",labelcolor="red")#fontproperties={'weight': 'bold'})
          ax.quiverkey(p,0.74,1.1,30,
                    label="raw data",labelcolor="blue")#fontproperties={'weight': 'bold'})
          ax.set_title(filename,color='black',fontsize=20)
    plt.grid(True)
  ax.set_ylabel('m/s',fontsize=17)
  ax.set_xlabel(yeartime,fontsize=17)
  plt.show()

def multiquiver(panels,time,u,v,color,title,xlabel):
  # where panels is the number of panels
  # time is in the form of numbers
  # u & v are in cm/sec
  y=[]
  for i in range(len(time)):
     y.append(0) # generates a dummy y vector needed for quiver stickplots
  yd_per_panel=len(time)/panels
  if float(len(time))/panels>len(time)/panels:
      yd_per_panel=yd_per_panel+1
  fig=plt.figure()
  for ii in range(1, panels+1):
    subplot_num=str(panels)+"1"+str(ii)
    datenum=time[yd_per_panel*(ii-1):yd_per_panel*ii]
    y_i=y[yd_per_panel*(ii-1):yd_per_panel*ii]
    u_i=u[yd_per_panel*(ii-1):yd_per_panel*ii]
    v_i=v[yd_per_panel*(ii-1):yd_per_panel*ii]
    ax = fig.add_subplot(int(subplot_num))
    p=ax.quiver(datenum,y_i,u_i,v_i,scale=max(v)*10,color=color)
    ax.yaxis.set_major_locator(mpl.ticker.NullLocator())
    #locator = mpl.dates.AutoDateLocator()
    #ax.xaxis.set_major_locator(locator)
    #monthsFmt = DateFormatter('%b/%d') 
    #ax.xaxis.set_major_formatter(monthsFmt)
    set_date_locator(ax.xaxis)
    #  ax.axis(xmin=time[interval*(ii-1)],xmax=time[interval*ii])
    # ax.quiverkey(p, X=0.12, Y=0.95, U=label_scale, label=str(label_scale)+' cm/s ('+label_str+' knots)', coordinates='axes', labelpos='S')
    if ii==1:
          ax.quiverkey(p,X=0.95, Y=1.05, U=int(max(v)),
                    label=str(int(max(v)))+"cm/s",labelcolor="blue")#fontproperties={'weight': 'bold'})
          ax.set_title(title,color='black',fontsize=20)
    if ii==panels/2:
       ax.set_ylabel('Note: 25 cm/s ~= half knot',labelpad=20)
    if ii==panels:
        ax.set_xlabel(xlabel)
  plt.show()

# plot u and v
#def quiverplot(jd,y,u,v,color,scale,title,figure):
#  import matplotlib as mpl 
#  fig=plt.figure(figure)
#  ax=fig.add_subplot(111)
#  q=plt.quiver(jd,y,u,v,scale=scale,color=color)
#  p=plt.quiverkey(q,X=0.1,Y=1.01,U=0.5,
#                    label="quiver",labelcolor="blue")
#  ax.yaxis.set_major_locator(mpl.ticker.NullLocator())
#  locator = mpl.dates.AutoDateLocator()
#  ax.xaxis.set_major_locator(locator)
#  monthsFmt = DateFormatter('%m/%d')
#  ax.xaxis.set_major_formatter(monthsFmt)
#  fig.autofmt_xdate(bottom=0.18)
#  plt.title(title,fontsize=20,color='red')

#simple quiver plot
def quiver_uv(time,u,v):
    #get 0, length of 0 is same with time
    y=[]
    for i in range(len(u)):
        y.append(0)
    fig=plt.figure()
    fig.canvas.set_window_title('quiver u&v')
    ax = fig.add_subplot(111)
    p=ax.quiver(time,np.array(y),u,v,scale=max(v)*10,color='red')
    #ax.yaxis.set_major_locator(mpl.ticker.NullLocator())
    #locator = mpl.dates.AutoDateLocator()
    #ax.xaxis.set_major_locator(locator)
    #monthsFmt = DateFormatter('%b/%d') 
    #ax.xaxis.set_major_formatter(monthsFmt)
    ax.quiverkey(p,X=0.95, Y=1.05, U=int(max(v)),
                    label=str(float(max(v)))+"m/s",labelcolor="red")
    #  ax.set_xlabel(num2date(time[0]).year,fontsize=17)
    ax.set_ylim(-50,50)
    plt.show()
