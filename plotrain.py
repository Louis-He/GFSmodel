import sys
from mpl_toolkits.basemap import Basemap, cm, shiftgrid
import matplotlib as mpl
mpl.use('Agg')

import matplotlib.pyplot as plt
import numpy as np
import os
import time
import pygrib
import color
from area import *

if __name__ == "__main__":
    ra=color.rain
    fr=color.freezing
    sn=color.sonw

utc = 0

# plot the diagram of 10m wind + 2m T + MSLPz
def plotRain(file, areatype):
    # set boundary through areatype
    boundary = ''
    tmpstr = 'boundary=' + areatype
    ldict = locals()
    exec(tmpstr, globals(), ldict)
    boundary = ldict['boundary']
    #print(boundary)

    #read in files
    grbs = pygrib.open('rawfile/' + file)
    # extract data from grib file
    Temperature = grbs.select(name='2 metre temperature')[0]
    Precipitation = grbs.select(name='Total Precipitation')[0]
    subP = Precipitation.values
    del Precipitation
    rain = grbs.select(name='Categorical rain')[0]
    subR = rain.values
    del rain
    snow = grbs.select(name='Categorical snow')[0]
    subS = snow.values
    del snow
    freezing = grbs.select(name='Categorical freezing rain')[0]
    subF = freezing.values
    del freezing
    ice = grbs.select(name='Categorical ice pellets')[0]
    subI = ice.values
    del ice
    # define longitude and latitude
    lats, lons = Precipitation.latlons()
    lats = (lats.T)[0]
    lons = lons[0]

    # define the initial forecast hour
    analysistime = Temperature.analDate
    fcit = analysistime.timetuple() # time.struct_time
    formatfcit = time.strftime('%Hz %m %d %Y', fcit) # formatted initial time
    timestampfcit = time.mktime(fcit) # timestamp of initial time

    fcst = Temperature.forecastTime # integer
    formatvalid = time.strftime('%Hz %m %d %Y', time.localtime(timestampfcit + fcst * 60 * 60)) # formatted validtime

    #calculate
    rain1 = subP*(subR+subS+subF+subI)
    snow1 = subP*(subS+subF+subI)
    freezing1 = subP*(subF+subI)
    del subP, subR, subS, subF, subI

    nrain=np.ma.array(rain1,mask=(rain1==0))
    nsnow=np.ma.array(snow1,mask=(snow1==0))
    nfreezingice=np.ma.array(freezing1,mask=(freezing1==0))
    # generatre basemap
    m = Basemap(llcrnrlon=boundary[0], llcrnrlat=boundary[1], urcrnrlon=boundary[2], urcrnrlat=boundary[3],
                projection='lcc', lat_0=boundary[4], lon_0=boundary[5], resolution='l', area_thresh=100)
    lon, lat = np.meshgrid(lons, lats)
    x, y = m(lon, lat)

    fig = plt.figure(figsize=(10,7), dpi=150)
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['left'].set_color('none')
    ax.spines['bottom'].set_color('none')
    ax.spines['top'].set_color('none')

    # generate legend
    
    y1 = mpl.colors.LinearSegmentedColormap('my_colormap',ra,256)
    y2 = mpl.colors.LinearSegmentedColormap('my_colormap',sn,256)
    y3 = mpl.colors.LinearSegmentedColormap('my_colormap',fr,256)
    norm=mpl.colors.Normalize(0, 750)

    #c=plt.contourf(x, y, rt, 750, cmap=my_cmap, norm=norm)
    plt.contourf(x, y, nrain, 750, cmap=y1, norm=norm)
    plt.contourf(x, y, nsnow, 750, cmap=y2, norm=norm)
    plt.contourf(x, y, nfreezingice, 750, cmap=y3, norm=norm)
    #, alpha=0.6

    plt.title('GFS 6-hour Averaged Precip Rate\nlnit:' + formatfcit + ' Forecast Hour[' + str(fcst) + '] valid at ' + formatvalid + '\n@Myyd & Louis-He',
                  loc='left', fontsize=11)
    m.drawparallels(np.arange(-90., 90., 10), labels=[1,0,0,0], fontsize=8, linewidth=0.5,color='dimgrey',dashes=[1,1])
    m.drawmeridians(np.arange(0., 180., 10), labels=[0,0,0,1], fontsize=8, linewidth=0.5,color='dimgrey',dashes=[1,1])
    m.drawcoastlines(linewidth=0.5)
    m.drawstates(linewidth=0.4,color='dimgrey')
    #m.readshapefile('/mnt/c/Users/10678/Desktop/GFS/shp/cnhimap', 'states', drawbounds=True, linewidth=0.5, color='black')
    ax2 = fig.add_axes([0.85, 0.13, 0.012, 0.23])
    clevs1=[0,0.1,10,25,50,100,250,400,750]
    cmap1=mpl.colors.ListedColormap([[1, 1, 1], [144/255, 238/255, 144/255],
                                  [34/255, 139/255, 34/255], [0, 191/255, 1],
                                    [0, 0, 1],[1, 0, 1],
                                     [205/255, 18/255, 118/255],[104/255, 39/255, 139/255]])
    norm1=mpl.colors.BoundaryNorm(clevs1, cmap1.N)                                     
    cbar1=mpl.colorbar.ColorbarBase(ax2, cmap=cmap1, spacing='uniform', norm=norm1, ticks=clevs1,
                                        orientation='vertical', drawedges=False)                                  
    cbar1.ax.set_ylabel('rain(mm)', size=4)
    cbar1.ax.tick_params(labelsize=4) 

    clevs2=[0,0.1,10,25,50,100,250,750]
    ax3 = fig.add_axes([0.85, 0.38, 0.012, 0.23])
    cmap2=mpl.colors.ListedColormap([[1, 1, 1], [253/255, 216/255, 213/255],
                                  [251/255, 174/255, 185/255], [247/255, 109/255, 163/255],
                                    [211/255, 47/255, 146/255],[146/255, 1/255, 122/255],
                                     [81/255, 0, 108/255]])
    norm2=mpl.colors.BoundaryNorm(clevs2, cmap2.N)                                     
    cbar2=mpl.colorbar.ColorbarBase(ax3, cmap=cmap2, spacing='uniform', norm=norm2, ticks=clevs2,
                                        orientation='vertical', drawedges=False)                                  
    cbar2.ax.set_ylabel('freezing/ice(mm)', size=4)
    cbar2.ax.tick_params(labelsize=4)

    clevs3=[0,0.1,2.5,5,10,20,30,750]
    ax4 = fig.add_axes([0.85, 0.64, 0.012, 0.23])
    cmap3=mpl.colors.ListedColormap([[1, 1, 1], [234/255, 234/255, 234/255],
                                  [200/255, 200/255, 200/255], [154/255, 154/255, 154/255],
                                    [108/255, 108/255, 108/255],[58/255, 58/255, 58/255],
                                     [6/255, 6/255, 6/255]])
    norm3=mpl.colors.BoundaryNorm(clevs3, cmap3.N)                                     
    cbar3=mpl.colorbar.ColorbarBase(ax4, cmap=cmap3, spacing='uniform', norm=norm3, ticks=clevs3,
                                        orientation='vertical', drawedges=False)                                  
    cbar3.ax.set_ylabel('snow(mm)', size=4)
    cbar3.ax.tick_params(labelsize=4)
    #Temperature(℃)

    #GFS 10m Wind and 2m Air Temperature\nlnit:00z Nov 04 2017 Forecast Hour[36] valid at 12z Sun,Nov 05 2017 6-hour #ERA Interim 850hpa Wind speed and Precipitation & 500hpa Geopotential Height#Streamlines
    plt.savefig('product/RAIN/' + areatype + file + '.png', bbox_inches='tight')

    # delete plot for memory
    del fig
    plt.cla
    plt.clf()
    plt.close(0)
    del m, lon, lat, lons, lats, y1, y2, y3, norm, norm1, norm2, norm3, cbar1, cbar2, cbar3, ax, ax2, ax3, ax4, x, y, analysistime, fcit, formatfcit, timestampfcit, fcst, formatvalid

nargs=len(sys.argv)
skip=False
for i in range(1,nargs):
   if not skip:
      arg=sys.argv[i]
      #print ("INFO: processing",arg)
      if arg == "--path":
         if i != nargs-1:
            file = sys.argv[i+1]
            skip=True
      elif arg == "--area":
         if i != nargs-1:
            pic=sys.argv[i+1]
            skip=True
      else:
         print ("ERR: unknown arg:",arg)
   else:
      skip=False

path = 'rawfile/' + file
if file[0:3] == 'gfs':
    #try:
    plotRain(file, areatype=pic)
    print('[Compele Plotting] File:' + file)
    f = open('sysreport/plotreport.txt', 'a+')
    f.write('[' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + utc * 60 * 60)) + ']' + '\t' +
            file + ' Rain PLOT SUCCESS\n')
    f.close()
    f = open('sysreport/running.txt', 'a+')
    f.write('[' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + utc * 60 * 60)) + ']' + '\t' +
            file + ' Rain PLOT SUCCESS\n')
    f.close()
    del f
    '''
    except:
        print('[ERR:unknown] File:' + file)
        f = open('sysreport/plotreport.txt', 'a+')
        f.write('[' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + utc * 60 * 60)) + ']' + '\t' +
                file + ' Rain PLOT FAILED! PLEASE CHECK\n')
        f.close()
        f = open('sysreport/errreport.txt', 'a+')
        f.write('[' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + utc * 60 * 60)) + ']' + '\t' +
                file + ' Rain PLOT FAILED! PLEASE CHECK!\n')
        f.close()
        f = open('sysreport/running.txt', 'a+')
        f.write('[' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + utc * 60 * 60)) + ']' + '\t' +
                file + ' Rain PLOT FAILED! PLEASE CHECK!\n')
        f.close()
        del f
    '''