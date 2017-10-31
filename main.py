from datetime import datetime
import time
import urllib.request
from urllib.request import urlretrieve,urlopen
import os

utc = -4

# return the URL of the latest GFS model (4 hours after the initial)
def decideURL(forecasthour):
    global utc
    hourresult = ''

    timechange = -1 * utc
    nowtime = time.time() + timechange * 60 * 60 # struct time of UTC
    result = time.strftime("%H", time.localtime(nowtime))  # hour of UTC time
    print(result)

    if int(result) >= 22:
        hourresult = '18'
    elif int(result) < 4:
        hourresult = '18'
        nowtime = nowtime - 24 * 60 * 60
    elif int(result) < 10:
        hourresult = '00'
    elif int(result) < 16:
        hourresult = '06'
    elif int(result) < 22:
        hourresult = '12'

    #http://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl?file=gfs.t12z.pgrb2.0p25.f000&all_var=on&leftlon=0&rightlon=360&toplat=90&bottomlat=-90&dir=%2Fgfs.2017102712

    result = time.strftime("%Y%m%d", time.localtime(nowtime)) + hourresult  # hour of UTC time
    filename = result
    result = 'http://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl?file=gfs.t'+ hourresult +'z.pgrb2.0p25.f' + forecasthour + '&all_var=on&leftlon=0&rightlon=360&toplat=90&bottomlat=-90&dir=%2Fgfs.' + result
    return [result, 'gfs.'+filename]

#定义下载函数downLoadPicFromURL（本地文件夹，网页URL）
def downLoadPicFromURL(dest_dir,URL):
        try:
          urllib.request.urlopen(URL , dest_dir)
        except:
          print ('\tError retrieving the URL:', URL)


#set the path of the file from GFS
downloadhour = ['000','024','048','072','096','120']
total = len(downloadhour)
count = 0
for i in downloadhour:
    count += 1
    downloadinfo = decideURL(i)
    print('[' + str((count-1)/total) + '%]Dowanloading file... from URL: ' + downloadinfo[0])
    path = 'rawfile/' + downloadinfo[1]
    urlretrieve(downloadinfo[0], path)