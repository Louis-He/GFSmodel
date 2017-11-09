import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.io.shapereader as shpreader

shpfilename = shpreader.natural_earth(resolution='110m',
                                      category='cultural',
                                      name='admin_0_countries')
plt.figure(figsize=(6, 3))
ax = plt.axes(projection=ccrs.PlateCarree(central_longitude=180))
ax.coastlines(resolution='110m')
ax.gridlines()

'''
scale='10m'
import cartopy
from netCDF4 import Dataset ,date2index
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cmaps
from mpl_toolkits.basemap import cm
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from datetime import datetime

date = datetime(2017,11,9,12)
data1=Dataset('gfs6.nc')
timevar = data1.variables['time']
timeindex = date2index(date,timevar)
lat=data1.variables['latitude'][:].squeeze()
lon=data1.variables['longitude'][:].squeeze()

var=data1.variables['TMP_850mb'][timeindex,:].squeeze()
u=data1.variables['UGRD_850mb'][timeindex,:].squeeze()
v=data1.variables['VGRD_850mb'][timeindex,:].squeeze()
g1=data1.variables['HGT_500mb'][timeindex,:].squeeze()
#clo=data1.variables['tcc'][:][timeindex1,:].squeeze()

#data2=Dataset('500.nc')
#g1=data2.variables['z'][timeindex,:].squeeze()
#u=data2.variables['UGRD_850mb'][:].squeeze()
#data3=Dataset('v.nc')
#v=data3.variables['VGRD_850mb'][:].squeeze()
#data4=Dataset('g.nc')
#g=data4.variables['HGT_500mb'][:].squeeze()
#var=data.variables['TMP_850mb']#[timeindex,:].squeeze()
g=g1/10
t=var-273.15
lati=np.min(lat)
latm=np.max(lat)
loni=np.min(lon)
lonm=np.max(lon)
                 
#ax=plt.axes(projection=ccrs.PlateCarree())
fig, ax = plt.subplots(figsize=(12,6),subplot_kw={'projection': ccrs.PlateCarree()})
ax.set_extent([70, 145, 3, 55])
countries = cfeature.NaturalEarthFeature('cultural', 'countries', scale, edgecolor='black',
                                                              facecolor=cfeature.COLORS['land'])
ax.add_feature(countries, facecolor='none', linewidths=0.3)
provinces = cfeature.NaturalEarthFeature('cultural', 'provinces', scale, edgecolor='black',
                                                              facecolor=cfeature.COLORS['land'])
ax.add_feature(provinces, facecolor='none', linewidths=0.2)
lakes = cfeature.NaturalEarthFeature('physical', 'lakes', scale, edgecolor='black',
                                                              facecolor=cfeature.COLORS['water'])
ax.add_feature(lakes, facecolor='none', linewidths=0.3)
rivers = cfeature.NaturalEarthFeature('physical', 'rivers', scale, edgecolor='black',
                                                              facecolor=cfeature.COLORS['water'])
ax.add_feature(rivers, facecolor='none', linewidths=0.3)

ax.coastlines(scale,linewidth=0.3,color='black')

ax.set_xticks(np.arange(70,145,15), crs=ccrs.PlateCarree())
ax.set_yticks(np.arange(3,55,15), crs=ccrs.PlateCarree())
lon_formatter = LongitudeFormatter(number_format='.0f',
                                       degree_symbol='',zero_direction_label=False)
lat_formatter = LatitudeFormatter(number_format='.0f',
                                      degree_symbol='')
ax.xaxis.set_major_formatter(lon_formatter)
ax.yaxis.set_major_formatter(lat_formatter)

#speed=(u**2+v**2)**0.5
#clevs = [-36, -34, -32, -30, -28, -26, -24, -22, -20, -18, -16, -14, -12, -10, -8, -6, -4, -2, 0, 
              #2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36]
#clevs=[0,0.1,2.5,5,7.5,10,15,20,30,40,50,70,100,150,200,250,300,400,500,600,750]    

#clevs = [-50, -46, -42, -38, -34, -30, -26, -22, -18, -14, -10, -6, -2, 2, 6, 10, 14, 18, 22, 26, 30, 34, 38, 42, 
             #46, 50]   
             

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

c=plt.pcolormesh(lon, lat, t, transform=ccrs.PlateCarree(), cmap=my_cmap,norm=norm)#,norm=norm cmaps.temp_19lev NCV_jaisnd
#d=plt.contour(lon, lat, g, 30, colors = 'whitesmoke', linewidths=0.3)#, alpha=0.8
#d1=plt.contour(lon, lat, t, 110, colors = 'red', linewidths=0.3, levels=0)

#ax.streamplot(lon, lat, u, v, transform=ccrs.PlateCarree(),
                  #linewidth=0.25, density=2, color='black', arrowsize=0.4, arrowstyle='->')
#ax.barbs(lon, lat, u, v, length=3,
             #sizes=dict(emptybarb=0, spacing=0.2, height=0.5),barb_increments=dict(half=2, full=4, flag=20 ), 
             #linewidth=0.25, transform=ccrs.PlateCarree(), color='dimgray', regrid_shape=27)          

#cbar=plt.colorbar(c, shrink=0.8, pad=0.02, aspect=20)    

ax2 = fig.add_axes([0.88, 0.11, 0.018, 0.77])
cbar=mpl.colorbar.ColorbarBase(ax2, cmap=my_cmap, norm=norm, orientation='vertical', drawedges=False)
cbar.set_ticks(np.linspace(-60,50,23))
#cbar.set_label('Temperature(℃)', rotation=90,  fontproperties=font)
cbar.ax.tick_params(labelsize=8)
         
#cbar.ax.set_ylabel('Temperature(℃)', size=5)#Temperature(℃)
#plt.clabel(d, inline = True, fmt='%.0f', colors='whitesmoke', fontsize=1.5)#alpha=0.8,
#plt.clabel(d1, inline = True, fmt='%.0f', fontsize=1.5)
#ax.grid(color='cyan', linestyle='dashed', linewidths=0.3)
plt.title('GFS 850hpa Wind speed and Temperature & 500hpa Geopotential Height\nlnit:00z Nov 07 2017 Forecast Hour[36] valid at 12z Wed,Nov 08 2017',
              loc='left', fontsize=7)#GFS 10m Wind speed and 2m Temperature\nlnit:00z Nov 04 2017 Forecast Hour[36] valid at 12z Sun,Nov 05 2017 6-hour #Averaged Precip Rate #ERA Interim 850hpa Wind speed and Temperature & 500hpa Geopotential Height
#plt.show()
plt.savefig('gfs2.png', bbox_inches='tight', dpi=800)

'''