
import pygrib

from mpl_toolkits.basemap import Basemap, cm, shiftgrid
import matplotlib as mpl
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import numpy as np
import os
import time
import pygrib

#from netCDF4 import Dataset ,date2index
#import numpy as np
#import matplotlib as mpl
#import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap,shiftgrid
from datetime import datetime

def plot():
    #read in files
    grbs = pygrib.open('rawfile/gfs.GFS2017111012.f000')
    # extract data from grib file
    Temperature = grbs.select(name='2 metre temperature')[0]
    wind10m_u = grbs.select(name='10 metre U wind component')[0]
    wind10m_v = grbs.select(name='10 metre V wind component')[0]
    MSLP = grbs.select(name='MSLP (Eta model reduction)')[0]
    lats, lons = Temperature.latlons()
    lats = lats.T
    lons = lons[0]

    subT = Temperature.values - 273.15
    subWU = wind10m_u.values
    subWV = wind10m_v.values
    subMSLP = MSLP.values / 100.0

    # extract data and get lat/lon values for a subset over China
    '''
    latL = 13
    latH = 52
    lonR = 145
    lonL = 77
    subT, lats, lons = Temperature.data(lat1=latL, lat2=latH, lon1=lonL, lon2=lonR)
    subWU, lats, lons = wind10m_u.data(lat1=latL, lat2=latH, lon1=lonL, lon2=lonR)
    subWV, lats, lons = wind10m_v.data(lat1=latL, lat2=latH, lon1=lonL, lon2=lonR)
    subMSLP, lats, lons = MSLP.data(lat1=latL, lat2=latH, lon1=lonL, lon2=lonR)
    '''



    '''
    date = datetime(2017,11,14,12)
    data1=Dataset('gfs.nc')
    timevar = data1.variables['time']
    timeindex = date2index(date,timevar)
    '''
    '''
    #data2=Dataset('gfs2.nc')
    #data3=Dataset('gfs3.nc')
    #data4=Dataset('gfs4.nc')
    lats=data1.variables['latitude'][:].squeeze()
    lons=data1.variables['longitude'][:].squeeze()

    var=data1.variables['TMP_2maboveground'][timeindex,:].squeeze()
    u=data1.variables['UGRD_10maboveground'][timeindex,:].squeeze()
    v=data1.variables['VGRD_10maboveground'][timeindex,:].squeeze()
    g1=data1.variables['PRMSL_meansealevel'][timeindex,:].squeeze()
    #r1=data1.variables['APCP_surface'][:].squeeze()
    #r2=data2.variables['APCP_surface'][:].squeeze()
    #r3=data3.variables['APCP_surface'][:].squeeze()
    #r4=data4.variables['APCP_surface'][:].squeeze()

    #data2=Dataset('500.nc')
    #g1=data2.variables['z'][timeindex,:].squeeze()
    #u=data2.variables['UGRD_850mb'][:].squeeze()
    #data3=Dataset('v.nc')
    #v=data3.variables['VGRD_850mb'][:].squeeze()
    #data4=Dataset('g.nc')
    #g=data4.variables['HGT_500mb'][:].squeeze()
    #var=data.variables['TMP_850mb']#[timeindex,:].squeeze()
    #rt=r1+r2+r3+r4
    g=g1/100
    t=var-273.15
    '''

    m = Basemap(llcrnrlon=77,llcrnrlat=13,urcrnrlon=145,urcrnrlat=52,
                projection='lcc',lat_0=30, lon_0=105,
                resolution ='f',area_thresh=1)
    lon, lat = np.meshgrid(lons, lats)
    x, y = m(lon, lat)

    fig=plt.figure(figsize=(10,7), dpi=500)
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['left'].set_color('none')
    ax.spines['bottom'].set_color('none')
    ax.spines['top'].set_color('none')

    TT = {'red': ((0, 246/255, 246/255),
                     (20/110, 241/255, 241/255),#CDG-81
                     (35/110, 188/255, 188/255),#CMG-80.9
                     (40/110, 123/255, 123/255),#CMG-76
                     (45/110, 183/255, 183/255),#LG-63.9
                     (50/110, 76/255, 76/255),#LG-54
                     (55/110, 44/255, 44/255),#MG-53.9
                     (599/1100, 4/255, 4/255),#MG-42
                     (60/110, 109/255, 109/255),#DG-41.9
                     (67/110, 21/255, 21/255),#DG-31
                     (75/110, 253/255, 253/255),#OW-30.9
                     (85/110, 191/255, 191/255),#OW+9
                     (90/110, 159/255, 159/255),#WMG+9
                     (100/110, 246/255, 246/255),#WMG+9
                     (105/110, 118/255, 118/255),#WMG+9
                     (1.0, 145/255, 145/255)),
            'green':((0, 183/255, 183/255),
                     (20/110, 18/255, 18/255),#CDG-81
                     (35/110, 114/255, 114/255),#CMG-80.9
                     (40/110, 81/255, 81/255),#CMG-76
                     (45/110, 184/255, 184/255),#LG-63.9
                     (50/110, 73/255, 73/255),#LG-54
                     (55/110, 144/255, 144/255),#MG-53.9
                     (599/1100, 255/255, 255/255),#MG-42
                     (60/110, 231/255, 231/255),#DG-41.9
                     (67/110, 167/255, 167/255),#DG-31
                     (75/110, 235/255, 235/255),#OW-30.9
                     (85/110, 31/255, 31/255),#OW+9
                     (90/110, 32/255, 32/255),#WMG+9
                     (100/110, 183/255, 183/255),#WMG+9
                     (105/110, 114/255, 114/255),#WMG+9
                     (1.0, 40/255, 40/255)),
            'blue': ((0, 244/255, 244/255),
                     (20/110, 134/255, 134/255),#CDG-81
                     (35/110, 199/255, 199/255),#CMG-80.9
                     (40/110, 169/255, 169/255),#CMG-76
                     (45/110, 226/255, 226/255),#LG-63.9
                     (50/110, 182/255, 182/255),#LG-54
                     (55/110, 254/255, 254/255),#MG-53.9
                     (599/1100, 255/255, 255/255),#MG-42
                     (60/110, 153/255, 153/255),#DG-41.9
                     (67/110, 31/255, 31/255),#DG-31
                     (75/110, 118/255, 118/255),#OW-30.9
                     (85/110, 17/255, 17/255),#OW+9
                     (90/110, 51/255, 51/255),#WMG+9
                     (100/110, 244/255, 244/255),#WMG+9
                     (105/110, 199/255, 199/255),#WMG+9
                     (1.0, 139/255, 139/255))}

    my_cmap = mpl.colors.LinearSegmentedColormap('my_colormap',TT,256)
    norm=mpl.colors.Normalize(-60, 50)

    #c=plt.contourf(x, y, rt, 750, cmap=my_cmap, norm=norm)
    m.contourf(x, y, subT, 110, cmap=my_cmap, norm=norm)#,norm=norm cmaps.temp_19lev NCV_jaisnd
    d=m.contour(x, y, subT, 110, colors = 'red', linewidths=0.6, levels=0)
    d1=m.contour(x, y, subMSLP, 70, colors = 'whitesmoke', linewidths=0.5)#, alpha=0.6
    plt.clabel(d, inline = True, fmt='%.0f', fontsize=2)
    plt.clabel(d1, inline = True, fmt='%.0f', colors='whitesmoke', fontsize=2)#alpha=0.6,


    skip=slice(None,None,5)
    #m.streamplot(x, y, u, v, linewidth=0.25, density=4, color='black', arrowsize=0.4, arrowstyle='->')

    m.barbs(x[skip,skip], y[skip,skip], subWU[skip,skip], subWV[skip,skip], length=3.5,
                 sizes=dict(emptybarb=0, spacing=0.2, height=0.5),barb_increments=dict(half=2, full=4, flag=20 ),
                 linewidth=0.2, color='black')


    plt.title('GFS 10m Wind & 2m Air Temperature & MSLP\nlnit:00z Nov 13 2017 Forecast Hour[36] valid at 12z Tue,Nov 14 2017',
                  loc='left', fontsize=11)
    m.drawparallels(np.arange(0, 65, 10), labels=[1,0,0,0], fontsize=8, linewidth=0.5,color='dimgrey',dashes=[1,1])
    m.drawmeridians(np.arange(65., 180., 10), labels=[0,0,0,1], fontsize=8, linewidth=0.5,color='dimgrey',dashes=[1,1])
    m.drawcoastlines(linewidth=0.5)
    m.drawstates(linewidth=0.4,color='dimgrey')
    m.readshapefile('D:\\shp\\provinces', 'states', drawbounds=True, linewidth=0.5, color='black')
    ax2 = fig.add_axes([0.88, 0.11, 0.018, 0.77])
    cbar=mpl.colorbar.ColorbarBase(ax2, cmap=my_cmap, norm=norm, orientation='vertical', drawedges=False)
    cbar.set_ticks(np.linspace(-60,50,23))
    cbar.ax.set_ylabel('Temperature(℃)', size=8)#Temperature(℃)
    cbar.ax.tick_params(labelsize=8)
    #Temperature(℃)

    #GFS 10m Wind and 2m Air Temperature\nlnit:00z Nov 04 2017 Forecast Hour[36] valid at 12z Sun,Nov 05 2017 6-hour #ERA Interim 850hpa Wind speed and Temperature & 500hpa Geopotential Height#Streamlines
    plt.savefig('gfs.png', bbox_inches='tight')