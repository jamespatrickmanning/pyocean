"""
Conversion functions

"""
import numpy as np
import math
from matplotlib.dates import num2date


def c2f(*c):
    """
    convert Celsius to Fahrenheit
    accepts multiple values
    """
    if not c:
        c = input ('Enter Celsius value:')
        f = 1.8 * c + 32
        return f
    else:
        f = [(i * 1.8 + 32) for i in c]
        return f

def f2c(*f):
    """
    convert Fahrenheit to Celsius
    accepts multiple values
    """
    if not f:
        f = input('Enter Farenheit value:')
        c = (f-32)/1.8
        return c
    else:
        c = [(i - 32)/ 1.8 for i in f]
        return c

def cmps2knots(cmps):
    """
    convert centimeter per second to knots
    """
    knots = float(cmps) / 51.444444
    return knots

def knots2ms(knots):
    """
    convert knots to m/s
    """
    kmperhour = knots*1.8535
    meterspersecond = kmperhour*1000./3600.
    return meterspersecond
  
def date2yd(datetime_nums):
    """
    convert date to yearday
    input float value which gives one plus the number of days
    """
   ################### Check - not sure if it works
    yearday=[]
    for datetime_num in datetime_nums:
      year_day=num2date(datetime_num).strftime('%j')
      year_time=float(num2date(datetime_num).hour+(float(num2date(datetime_num).minute)/float(60))+(float(num2date(datetime_num).second)/float(3600)))/float(24)
      yearday.append(float(year_day)+year_time)
    #yearday = datetime.now().timetuple().tm_yday - this works
    return yearday


def dd2dm(lat,lon):
    """
    convert lat, lon from decimal degrees to degrees,minutes
    """
    lat_d = int(abs(lat))                #calculate latitude degrees
    lat_m = (abs(lat) - lat_d) * 60. #calculate latitude minutes

    lon_d = int(abs(lon))
    lon_m = (abs(lon) - lon_d) * 60.
    
    la=lat_d*100.+lat_m
    lo=lon_d*100.+lon_m
    return la,lo

def dm2dd(lat,lon):
    """
    convert lat, lon from decimal degrees,minutes to decimal degrees
    """
    (a,b)=divmod(float(lat),100.)   
    aa=int(a)
    bb=float(b)
    lat_value=aa+bb/60.

    if float(lon)<0:
        (c,d)=divmod(abs(float(lon)),100.)
        cc=int(c)
        dd=float(d)
        lon_value=cc+(dd/60.)
        lon_value=-lon_value
    else:
        (c,d)=divmod(float(lon),100.)
        cc=int(c)
        dd=float(d)
        lon_value=cc+(dd/60.)
    return lat_value, -lon_value

def dd2dms(lat,lon):
    """
    convert lat, lon from decimal degrees to degrees,minutes,seconds
    """
    lat,lon=np.asarray(lat),np.asarray(lon)
    lat_dd=abs(lat)
    lat_d=math.floor(lat_dd)
    lat_m=math.floor((lat_dd-lat_d)*60)
    lat_s=((lat_dd-lat_d)*60-lat_m)*60
    if lon<0:
        lon_dd=abs(lon)
        lon_d=math.floor(lon_dd)
        lon_m=math.floor((lon_dd-lon_d)*60)
        lon_s=((lon_dd-lon_d)*60-lon_m)*60
        lon_d=-lon_d
    else:
        lon_dd=abs(lon)
        lon_d=math.floor(lon_dd)
        lon_m=math.floor((lon_dd-lon_d)*60)
        lon_s=((lon_dd-lon_d)*60-lon_m)*60
    return int(lat_d),int(lat_m),float(lat_s), int(lon_d),int(lon_m),float(lon_s)

def dens0(s, t):
    """
    Density of Sea Water at atmospheric pressure
    input: salinity, temperature
    
    """
    b0 =  8.24493e-1
    b1 = -4.0899e-3
    b2 =  7.6438e-5
    b3 = -8.2467e-7
    b4 =  5.3875e-9

    c0 = -5.72466e-3
    c1 =  1.0227e-4
    c2 = -1.6546e-6

    d0 = 4.8314e-4
    T68  = T68conv(t)
    dens0 = smow(t) + ( b0 + ( b1 + ( b2 + ( b3 + b4 * T68 ) * T68 ) * T68 ) * T68 ) * \
    s + ( c0 + ( c1 + c2 * T68 ) * T68 ) * s * (s)**0.5 + d0 * s**2
    return dens0

def dens(s, t, p):
    """
    Density of Sea Water using UNESCO 1983 (EOS 80) polynomial
    """
    s, t, p = np.asarray(s), np.asarray(t), np.asarray(p)
    densP0 = dens0(s, t)
    K = seck(s, t, p)
    p = p / 10.0 # convert from db to atm pressure units
    dens = densP0 / ( 1-p / K )
    return dens
  
def depth(p, lat):
    p, lat = np.asarray(p), np.asarray(lat)
    # Eqn 25, p26.  UNESCO 1983.
    C1 =  9.72659
    C2 = -2.2512E-5
    C3 =  2.279E-10
    C4 = -1.82E-15
    gam_dash = 2.184E-6

    lat = abs(lat)
    X   = np.sin( np.deg2rad(lat) )
    X   = X * X

    bot_line = 9.780318 * (1.0 + (5.2788E-3 + 2.36E-5 * X) * X) + \
               gam_dash * 0.5 * p
    top_line = (((C4 * p + C3) * p + C2) * p + C1) * p
    depth = top_line / bot_line
    return depth


def distance(origin, destination):
    """ 
    Calculates both distance and bearing
    """
    lat1, lon1 = origin
    lat2, lon2 = destination
    if lat1>1000:
        (lat1,lon1)=dm2dd(lat1,lon1)
        (lat2,lon2)=dm2dd(lat2,lon2)
        print 'converted to from ddmm to dd.ddd'
    radius = 6371 # km
    

    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c
    
    def calcBearing(lat1, lon1, lat2, lon2):
       dLon = lon2 - lon1
       y = math.sin(dLon) * math.cos(lat2)
       x = math.cos(lat1) * math.sin(lat2) \
           - math.sin(lat1) * math.cos(lat2) * math.cos(dLon)
       return math.atan2(y, x)
       
    bear= math.degrees(calcBearing(lat1, lon1, lat2, lon2))  
    return d,bear
    
def dist(lat1, lon1, lat2, lon2):
    """
    compute distance between two points
    input: coordinate(lat,lon) of both points
    Problem discovered May 2013
    """
    print 'WARNING: THIS DIST FUNCTION SHOULD BE REPLACED WITH DISTANCE'
    """
    if 1000 > lon1 > 0:
        (lat1,lon1) = dd2dm(lat1,lon1)
    if 1000 > lon2 > 0: 
        (lat2,lon2) = dd2dm(lat2,lon2)
    """    
    pid180 = math.pi/180
    alat = (lat1)*pid180
    alon = (lon1)*pid180
    blat = (lat2)*pid180
    blon = (lon2)*pid180
  
    cix = math.cos(alat)*math.cos(alat)*math.cos(alon-blon)+math.sin(alat)*math.sin(alat)
    distkmx = 6371*math.tan(math.sqrt(abs(1-cix*cix)/cix))
    ciy = math.cos(alat)*math.cos(blat)*math.cos(alon-alon)+math.sin(alat)*math.sin(blat) 
    distkmy = 6371*math.tan(math.sqrt(abs(1-ciy*ciy)/ciy))

    if distkmx > 0.001:   
        bear = abs(math.atan(distkmy/distkmx))
        if blon > alon and blat > alat:
            bear = 90-bear*180/math.pi 
        elif blon > alon and blat <= alat:
            bear = 90+bear*180/math.pi
        elif blon < alon and blat <= alat:        
            bear = 270-bear*180/math.pi
        elif blon < alon and blat > alat:  
            bear = 270+bear*180/math.pi

    else:
        if blat >= alat:
            bear = 0
        else:
            bear = 180

    ci = math.cos(alat)*math.cos(blat)*math.cos(alon-blon)+math.sin(alat)*math.sin(blat)
    distkm = 6371*math.tan(math.sqrt(abs(1-ci*ci)/ci))
    return distkm, bear



def fth2m(fth):
    m = fth * 1.8288
    return m

def m2fth(m):
    fth = m / 1.8288
    return fth
  
def ll2uv(jd,lat,lon):#jd is yearday
    "based on yearday,lat,lon.  you can get latitude speed and longitude speed "
    time=list(np.diff(jd))
    diff_time_list = []
    for i in time:
        diff_time_list.append(float(i)*24*60*60)
   
    u,v,jdn,spd=[],[],[],[]
    for i in range(1,len(jd)):
        (dkm,bear)=distance([lat[i-1],lon[i-1]],[lat[i],lon[i]])
        u.append(sd2uv(float(dkm*100000)/diff_time_list[i-1],bear)[0])
        v.append(sd2uv(float(dkm*100000)/diff_time_list[i-1],bear)[1])
        spd.append(np.sqrt(u[i-1]**2+v[i-1]**2))
        jdn.append(float(diff_time_list[i-1])/2/24/60/60+jd[i-1])
    return u,v,spd,jdn

def sd2uv(s,d):
    u = float(s)*math.sin(math.pi*float(d)/180.)
    v = float(s)*math.cos(math.pi*float(d)/180.)
    return u,v

def uv2sd(u,v):
    if u <> 0:
        d = math.atan(float(v/u))*180/math.pi
        if u>0 and v>0:
            d = 90-d
        if u>0 and v<=0:
            d = 90 + abs(d)
        if u<0 and v>0:
            d = 270 + abs(d)
        if u<0 and v<=0:
            d = 270 - abs(d)
    if u==0:
        if v<0:
            d=180
        else:
            d = 0
    s = math.sqrt(u**2+v**2)
    return s,d
"""
The previous two functions can be substituted with:

def d2r(d):
    r = d * math.pi / 180.0
    return (r)


def r2d(r):
    d = r * 180.0 / math.pi
    return (d)


def sd2uv(s,d):
    r = d2r(d)
    u = s * math.sin(r)
    v = s * math.cos(r)
    return (u,v)  


def uv2sd(u,v):
    s = math.sqrt((u*u)+(v*v))
    r = math.atan2(u,v)
    d = r2d(r)
    if d < 0:
        d = 360 + d
    return (s,d)


"""
def smow(t):
    """
    Denisty of standard mean ocean water (pure water)
    input: T = temperature[degree C (ITS-90)]
    output: density [kg/m^3]
    """
    A0 = 999.842594
    A1 = 6.793952e-2
    A2 = -9.095290e-3
    A3 = 1.001685e-4
    A4 = -1.120083e-6
    A5 = 6.536332e-9
    T68 = T68conv(t)
    dens = A0 + (A1 + (A2 + (A3 + (A4 + A5 * T68) * T68 ) * T68) * T68) * T68
    return dens

def seck(s, t, p=0):
    """
    Secant Bulk Modulus (K) of Sea Water using Equation of state 1980
    """
    s, t, p = np.asarray(s), np.asarray(t), np.asarray(p)
    p   = p/10.0 # convert from db to atmospheric pressure units
    T68 = T68conv(t)

    # Pure water terms of the secant bulk modulus at atmos pressure.
    # UNESCO eqn 19 p 18
    H3 = -5.77905E-7
    H2 =  1.16092E-4
    H1 =  1.43713E-3
    H0 =  3.239908   #[-0.1194975]
    AW = H0 + (H1 + (H2 + H3 * T68) * T68) * T68

    K2 =  5.2787E-8
    K1 = -6.12293E-6
    K0 =  8.50935E-5  #[+3.47718E-5]
    BW = K0 + (K1 + K2 * T68) * T68

    E4 = -5.155288E-5
    E3 = 1.360477E-2
    E2 = -2.327105
    E1 = 148.4206
    E0 = 19652.21    #[-1930.06]
    KW  = E0 + (E1 + (E2 + (E3 + E4 * T68) * T68) * T68) * T68 # eqn 19

    # Sea water terms of secant bulk modulus at atmos. pressure
    J0 = 1.91075E-4
    J2 = -1.6078E-6
    J1 = -1.0981E-5
    I0 =  2.2838E-3
    SR = (s)**0.5
    A  = AW + (I0 + (I1 + I2 * T68) * T68 + J0 * SR) * s
    M2 =  9.1697E-10
    M1 =  2.0816E-8
    M0 = -9.9348E-7
    B = BW + (M0 + (M1 + M2 * T68) * T68) * s # eqn 18
    F3 =  -6.1670E-5
    F2 =   1.09987E-2
    F1 =  -0.603459
    F0 =  54.6746
    G2 = -5.3009E-4
    G1 =  1.6483E-2
    G0 =  7.944E-2
    K0 = KW + (F0 + (F1 + (F2 + F3 * T68) * T68) * T68 \
            + (G0 + (G1 + G2 * T68) * T68) * SR) * s # eqn 16
    K = K0 + (A + B * p) * p # eqn 15
    return K


def sigmat(s, t, p):
    s, t, p = np.asarray(s), np.asarray(t), np.asarray(p)
    sgmt = dens(s, t, p) - 1000.0
    return sgmt
  
def T68conv(T90):
    T90 = np.asarray(T90)
    T68 = T90 * 1.00024
    return T68


