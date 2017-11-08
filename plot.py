import pygrib

from mpl_toolkits.basemap import Basemap, cm
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import numpy as np
import os

def plot(filepath):
    grbs = pygrib.open('rawfile/' + filepath)
    grb = grbs.select(name='Maximum temperature')[0]
    maxt = grb.values.T
    lats, lons = grb.latlons()


    maxt, lats, lons = grb.data(lat1=-90,lat2=90,lon1=0,lon2=359.75)
    maxt2=[]
    for i in range(maxt.shape[0]):
        maxt2.append(maxt[maxt.shape[0]-i-1])

    maxt = np.array(maxt2)
    #print(maxt)

    # create figure and axes instances
    fig = plt.figure(figsize=(11,7))
    ax = fig.add_axes([0.1,0.1,0.8,0.8])
    '''
    m = Basemap(llcrnrlon=0., llcrnrlat=-90., urcrnrlon=359.75, urcrnrlat=90., \
                  rsphere=(6378137.00, 6356752.3142), \
                  resolution='l', projection='merc', \
                  lat_0=0.25, lon_0=0.25, lat_ts=20.)
    '''
    m = Basemap(llcrnrlon=0., llcrnrlat=-90., urcrnrlon=359.75, urcrnrlat=90.)
    #m = Basemap(projection='robin',lon_0=0,resolution='c')
    # draw coastlines, state and country boundaries, edge of map.
    m.drawcoastlines()
    m.drawstates()
    m.drawcountries()
    # draw parallels.
    parallels = np.arange(-90.,90.,20.)
    m.drawparallels(parallels,labels=[1,0,0,0],fontsize=10)
    # draw meridians
    meridians = np.arange(0.,360.,20.)
    m.drawmeridians(meridians,labels=[0,0,0,1],fontsize=10)

    ny = maxt.shape[0]; nx = maxt.shape[1]
    lons, lats = m.makegrid(nx, ny) # get lat/lons of ny by nx evenly space grid.
    x, y = m(lons, lats) # compute map proj coordinates.

    # draw filled contours.
    clevs = [-40,-36,-32,-28,-24,-20,-16,-12,-8,-4,0,4,8,12,16,20,24,28,32,36,40]
    cs = m.contourf(x,y,maxt - 273.15,clevs,cmap=cm.GMT_haxby)
    # add colorbar.
    cbar = m.colorbar(cs,location='bottom',pad="5%")
    cbar.set_label('°C')
    # add title
    plt.title('example plot: ' + filepath + 'z global 2m maximum Temprature (°C)')

    plt.save('product/' + filepath + '.png')

path = 'rawfile/'
files= os.listdir(path)
print(files)
for file in files:
    if file[0:3] == 'gfs':
        plot(file)