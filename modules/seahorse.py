# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 12:35:51 2012
These functions are used to process "SeaHorse" current meter data

@author: Xiuling and JiM
"""

def read_name_sn(input_file_user,input_file_name,input_path,output_path):
  days_per_panel=7
  panel_per_page=3
  input_file=input_file_name
  input_file_suffix='_100926.dat'
  input_file_user=input_file_user
  input_filename=input_file+input_file_suffix
  input_path=input_path#'C:/xiuling/seahorse_data/'
  output_path=output_path#'C:/xiuling/seahorse_figure/'
  #path="Y:/tilt/oct2010/"
  #get yearday, u,v from the function
  data=read_seahorse(input_path+input_filename)
  date_time=data[0]
  u=data[1]
  v=data[2]
  location_u,location_v=[],[]
  for ui,u_i in zip(u,xrange(len(u))):
    if abs(ui) > np.std(u)*2:
      location_u.append(u_i)
  location_u_reverse=location_u.reverse()
  for i_location_u in location_u:
    del u[i_location_u]
    del v[i_location_u]
    del date_time[i_location_u] 
    
  for vi,v_i in zip(v,xrange(len(v))):
    if abs(vi) > np.std(v)*2:
      location_v.append(v_i)
  location_v_reverse=location_v.reverse()
  for i_location_v in location_v:
    del u[i_location_v]
    del v[i_location_v]
    del date_time[i_location_v]

  #calculate the number of figures,panels
  num_panel=math.ceil((int(max(date_time))-int(min(date_time)))/days_per_panel)
  num_figs=int(num_panel/panel_per_page)
  add_panel=int(num_panel%panel_per_page)
  # plot, each figures has penel_per_page(3) panels
  for f in range(1,(num_figs+1)):
    fig=plt.figure(f,figsize=(10,8),dpi=60)
    fig.suptitle(input_file_user, fontsize=20)
    for i in range(1,4):
      panel_plot_date,panel_u,panel_v,panel_y=[],[],[],[]
      for plot_date, ii in zip(date_time, xrange(len(date_time))):
        if int(math.ceil(min(date_time)+days_per_panel*((i-1)+(f-1)*panel_per_page)))<plot_date<int(math.ceil(min(date_time)+days_per_panel*(i+(f-1)*panel_per_page))):
          panel_plot_date.append(date_time[ii])
          panel_u.append(u[ii])
          panel_v.append(v[ii])
          panel_y.append(0)        
      subplot_num=str("31"+str(i))
      ax = fig.add_subplot(subplot_num)
      Q=ax.quiver(panel_plot_date,panel_y,panel_u,panel_v,color="blue",scale=max(v)*10)
      label_scale=int(max(v)/2)
      if i==1:
        knots=cmps2knots(label_scale)
        label_str='%5.1f'%(knots)
        ax.quiverkey(Q, X=0.12, Y=0.95, U=label_scale, label=str(label_scale)+' cm/s ('+label_str+' knots)', coordinates='axes', labelpos='S')
      ax.yaxis.set_major_locator(mpl.ticker.NullLocator())
   # fig.autofmt_xdate()
      locator = mpl.dates.AutoDateLocator()
      ax.xaxis.set_major_locator(locator)
      monthsFmt = DateFormatter('%m/%d')
      ax.xaxis.set_major_formatter(monthsFmt)
  #  plt.grid(True)
    ax.set_xlabel(num2date(date_time[0]).year,fontsize=17)
  #  ax.set_ylabel('m/s',fontsize=17)
    plt.savefig(output_path+input_file+str(f)+'.png',orientation='landscape')
    plt.savefig(output_path+input_file+str(f)+'.ps',orientation='landscape')
    plt.close()
  # plt.savefig('Y:/tilt/oct2010/'+file+"_"+str(f)+'.ps',orientation='landscape')
  if add_panel<>0:
    fig=plt.figure(num_figs+1,figsize=(10,8),dpi=60)
    fig.suptitle(input_file_user, fontsize=20)
    for i_i in range(1,add_panel+1):
      panel_plot_date,panel_u,panel_v,panel_y=[],[],[],[]
      for plot_date, ii in zip(date_time, xrange(len(date_time))):
        if int(math.ceil(min(date_time)+days_per_panel*((i_i-1)+((num_figs)*panel_per_page))))<plot_date<int(math.ceil(min(date_time)+days_per_panel*(i_i+(num_figs)*panel_per_page))):
          panel_plot_date.append(date_time[ii])
          panel_u.append(u[ii])
          panel_v.append(v[ii])
          panel_y.append(0)  
      subplot_num=str(str(int(add_panel))+"1"+str(i_i))
      ax = fig.add_subplot(subplot_num)
      label_scale=int(max(v)/2)
      p=ax.quiver(panel_plot_date,panel_y,panel_u,panel_v,color="blue",scale=50)
      if i_i==1:
        knots=cmps2knots(label_scale)
        label_str='%5.1f'%(knots)
        ax.quiverkey(p, X=0.12, Y=0.95, U=label_scale, label=str(label_scale)+' cm/s ('+label_str+' knots)', coordinates='axes', labelpos='S')
      ax.yaxis.set_major_locator(mpl.ticker.NullLocator())
      locator = mpl.dates.AutoDateLocator()
      ax.xaxis.set_major_locator(locator)
      monthsFmt = DateFormatter('%m/%d')
      ax.xaxis.set_major_formatter(monthsFmt)
      if 0<len(panel_u)<100:
        for date_i in panel_plot_date:
          if num2date(date_i).hour==00:
            monthsFmt = DateFormatter('%H:\n%m/%d')
            ax.xaxis.set_major_formatter(monthsFmt)
   # plt.grid(True)
    ax.set_xlabel(num2date(date_time[0]).year,fontsize=17)
    plt.savefig(output_path+input_file+'.ps',orientation='landscape')
    plt.savefig(output_path+input_file+'.png',orientation='landscape')
    plt.close()

# read the data  exmaple:"Y:\tilt\oct2010\9672592_100926.dat
def read_seahorse(filename):
  dataReader = csv.reader(open(filename,'rb'))
  verts=[]
  for row in dataReader:
    verts.append(row)
  u,v,year_day,time=[],[],[],[]

  for i in range(0,len(verts)):
    #convert "space delimite" to comma
    year_day.append(verts[i][0].split()[0])
    time.append(verts[i][0].split()[1])
    u.append(verts[i][0].split()[2])
    v.append(verts[i][0].split()[3])

  date_time=[]
  for i in range(0,len(year_day)):
    datetime=dt.datetime.strptime(year_day[i]+ " " +time[i], '%d-%b-%Y %H:%M:%S')
    date_time.append(date2num(datetime))
  u=[float(i) for i in u]
  v=[float(i) for i in v]
  return date_time, u,v

