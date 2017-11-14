import sys
import pygrib

from mpl_toolkits.basemap import Basemap, cm, shiftgrid
import matplotlib as mpl
mpl.use('Agg')

import matplotlib.pyplot as plt
import numpy as np
import os
import time
import pygrib

utc = 0

# plot the diagram of 10m wind + 2m T + MSLPz
def plotWTP(file):
    #read in files
    grbs = pygrib.open('rawfile/' + file)
    # extract data from grib file
    Temperature = grbs.select(name='2 metre temperature')[0]
    wind10m_u = grbs.select(name='10 metre U wind component')[0]
    wind10m_v = grbs.select(name='10 metre V wind component')[0]
    MSLP = grbs.select(name='MSLP (Eta model reduction)')[0]

    # define longitude and latitude
    lats, lons = Temperature.latlons()
    lats = (lats.T)[0]
    lons = lons[0]

    # define the initial forecast hour
    analysistime = Temperature.analDate
    fcit = analysistime.timetuple() # time.struct_time
    formatfcit = time.strftime('%Hz %m %d %Y', fcit) # formatted initial time
    timestampfcit = time.mktime(fcit) # timestamp of initial time

    fcst = Temperature.forecastTime # integer
    formatvalid = time.strftime('%Hz %m %d %Y', time.localtime(timestampfcit + fcst * 60 * 60)) # formatted validtime

    # extract each data
    subT = Temperature.values - 273.15
    subWU = wind10m_u.values
    subWV = wind10m_v.values
    subMSLP = MSLP.values / 100.0

    # delete unnecessary variables
    del Temperature
    del wind10m_u
    del wind10m_v
    del MSLP
    del grbs

    # generatre basemap
    m = Basemap(llcrnrlon=-125,llcrnrlat=30,urcrnrlon=-55,urcrnrlat=60,projection='lcc',lat_0=40, lon_0=-95,resolution ='l',area_thresh=1)
    lon, lat = np.meshgrid(lons, lats)
    x, y = m(lon, lat)

    fig = plt.figure(figsize=(10,7), dpi=150)
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['left'].set_color('none')
    ax.spines['bottom'].set_color('none')
    ax.spines['top'].set_color('none')

    # generate legend
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

    plt.title('GFS 10m Wind & 2m Air Temperature & MSLP\nlnit:' + formatfcit + ' Forecast Hour[' + str(fcst) + '] valid at ' + formatvalid + '\n@myyd & Louis-He',
                  loc='left', fontsize=11)
    m.drawparallels(np.arange(0, 65, 10), labels=[1,0,0,0], fontsize=8, linewidth=0.5,color='dimgrey',dashes=[1,1])
    m.drawmeridians(np.arange(65., 180., 10), labels=[0,0,0,1], fontsize=8, linewidth=0.5,color='dimgrey',dashes=[1,1])
    m.drawcoastlines(linewidth=0.5)
    m.drawstates(linewidth=0.4,color='dimgrey')
    #m.readshapefile('D:\\shp\\provinces', 'states', drawbounds=True, linewidth=0.5, color='black')
    ax2 = fig.add_axes([0.88, 0.11, 0.018, 0.77])
    cbar=mpl.colorbar.ColorbarBase(ax2, cmap=my_cmap, norm=norm, orientation='vertical', drawedges=False)
    cbar.set_ticks(np.linspace(-60,50,23))
    cbar.ax.set_ylabel('Temperature(℃)', size=8)#Temperature(℃)
    cbar.ax.tick_params(labelsize=8)
    #Temperature(℃)

    #GFS 10m Wind and 2m Air Temperature\nlnit:00z Nov 04 2017 Forecast Hour[36] valid at 12z Sun,Nov 05 2017 6-hour #ERA Interim 850hpa Wind speed and Temperature & 500hpa Geopotential Height#Streamlines
    plt.savefig('product/WTP_NA/' + file + '.png', bbox_inches='tight')

    # delete plot for memory
    del fig
    plt.cla
    plt.clf()
    plt.close(0)
    del subMSLP, subWU, subWV, subT, m, lon, lat, lons, lats, TT, my_cmap, norm, d, d1, cbar, ax, ax2, x, y, skip, analysistime, fcit, formatfcit, timestampfcit, fcst, formatvalid

# run at the beginning of the program
def initialize():

    os.system('rm -rf product/')
    print('['+time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + utc * 60 * 60))+']'+'Erase expired product')
    os.system('mkdir product')
    os.system('mkdir product/WTP')
    print('[' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + utc * 60 * 60)) + ']' + 'Create product folder')
    f = open('/root/GFS/sysreport/plotreport.txt', 'w+')
    f.close()
    print('[' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + utc * 60 * 60)) + ']' + 'Create system report file...')
    f = open('/root/GFS/sysreport/errreport.txt', 'w+')
    f.close()
    print('[' + time.strftime('%Y-%m-%d %H:%M:%S',
                              time.localtime(time.time() + utc * 60 * 60)) + ']' + 'Create system error report file...')
    print('[' + time.strftime('%Y-%m-%d %H:%M:%S',
                              time.localtime(time.time() + utc * 60 * 60)) + ']' + 'Start to plot...')

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
      else:
         print ("ERR: unknown arg:",arg)
   else:
      skip=False

#initialize()
path = 'rawfile/' + file
if file[0:3] == 'gfs':
    try:
        plotWTP(file)
        print('[Compele Plotting] File:' + file)
        f = open('/root/GFS/sysreport/plotreport.txt', 'a+')
        f.write('[' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + utc * 60 * 60)) + ']' + '\t' +
                file + ' PLOT SUCCESS\n')
        f.close()
        f = open('/root/GFS/sysreport/running.txt', 'a+')
        f.write('[' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + utc * 60 * 60)) + ']' + '\t' +
                file + ' PLOT SUCCESS\n')
        f.close()
        del f
    except:
        print('[ERR:unknown] File:' + file)
        f = open('/root/GFS/sysreport/plotreport.txt', 'a+')
        f.write('[' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + utc * 60 * 60)) + ']' + '\t' +
                file + ' PLOT FAILED! PLEASE CHECK\n')
        f.close()
        f = open('/root/GFS/sysreport/errreport.txt', 'a+')
        f.write('[' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + utc * 60 * 60)) + ']' + '\t' +
                file + ' PLOT FAILED! PLEASE CHECK!\n')
        f.close()
        f = open('/root/GFS/sysreport/running.txt', 'a+')
        f.write('[' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + utc * 60 * 60)) + ']' + '\t' +
                file + ' PLOT FAILED! PLEASE CHECK!\n')
        f.close()
        del f