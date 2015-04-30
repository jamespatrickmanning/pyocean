import pytz
import netCDF4
from datetime import datetime, timedelta
import sys
sys.path.append('../webtrack/Track_alisan')
from track_functions import get_drifter,get_fvcom,get_roms,draw_basemap,uniquecolors
GRID='30yr'
point1 = (41.9188, -70.2207)
model_days=3
start_time = datetime(2013,11,17,0,0,0,0,pytz.UTC) 
end_time = start_time + timedelta(model_days)
get_obj = get_fvcom(GRID)
url_fvcom = get_obj.get_url(start_time,end_time)
lons,lats,lonc,latc,b_points,h,siglay = get_obj.get_data(url_fvcom)
u,v = get_obj.get_uv(url_fvcom1)

