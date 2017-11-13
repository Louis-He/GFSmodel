from datetime import datetime
import time
import urllib.request
from urllib.request import urlretrieve,urlopen
import os

utc = 0

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

    result = time.strftime("%Y%m%d", time.localtime(nowtime)) + hourresult # hour of UTC time
    filename = 'GFS' + result + '.f' + forecasthour
    print(filename)
    result = 'http://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl?file=gfs.t'+ hourresult +'z.pgrb2.0p25.f' + forecasthour + '&all_var=on&leftlon=0&rightlon=360&toplat=90&bottomlat=-90&dir=%2Fgfs.' + result
    return [result, 'gfs.' + filename]

#定义下载函数downLoadPicFromURL（本地文件夹，网页URL）
def downLoadPicFromURL(dest_dir,URL):
        try:
          urllib.request.urlopen(URL , dest_dir)
        except:
          print ('\tError retrieving the URL:', URL)

# run at the beginning of the program
def initialize():
    os.system('rm -rf rawfile/')
    print('['+time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + utc * 60 * 60))+']'+'Erase expired rawfile')
    os.system('mkdir rawfile')
    print('[' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + utc * 60 * 60)) + ']' + 'Create rawfile folder')
    print('[' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + utc * 60 * 60)) + ']' + 'Start downloading file...')
    f = open('/root/GFS/sysreport/downloadreport.txt', 'w+')
    f.close()
    print('[' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + utc * 60 * 60)) + ']' + 'Create system download report file...')


#initialize the program
initialize()


#set the forecast hour of the file from GFS
downloadhour = ['000','006', '012', '018', '024','030', '036', '042','048', '054', '060', '066','072', '078', '084',
                '090','096','102', '108', '114', '120', '126', '132', '138', '144', '150', '156', '162', '168', '174',
                '180', '186', '192', '198', '204', '210', '216', '222', '228', '234', '240']

#reqiured download file
total = len(downloadhour)
count = 0
for i in downloadhour:
    count += 1
    downloadinfo = decideURL(i)
    print('' + str((count-1) / total * 100) + '%[' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + utc * 60 * 60)) + ']Dowanloading file... from URL: ' + downloadinfo[0])
    path = 'rawfile/' + downloadinfo[1]
    try:
        urlretrieve(downloadinfo[0], path)
        f = open('/root/GFS/sysreport/downloadreport.txt', 'a+')
        f.write('['+time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + utc * 60 * 60))+']' + '\t' + downloadinfo[1] + ' DOWNLOAD SUCCESS\n')
        f.close()
        f = open('/root/GFS/sysreport/running.txt', 'a+')
        f.write('[' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + utc * 60 * 60)) + ']' + '\t' +
                downloadinfo[1] + ' DOWNLOAD SUCCESS\n')
        f.close()
    except:
        print('(UNEXPECTED ERR)[' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(
            time.time() + utc * 60 * 60)) + ']Dowanloading file... from URL: ' + downloadinfo[1] + 'ERROR')
        f = open('/root/GFS/sysreport/downloadreport.txt', 'a+')
        f.write('[' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + utc * 60 * 60)) + ']' + '\t' +
                downloadinfo[1] + ' DOWNLOAD FAILED\n')
        f.close()
        f = open('/root/GFS/sysreport/running.txt', 'a+')
        f.write('[' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + utc * 60 * 60)) + ']' + '\t' +
                downloadinfo[1] + ' DOWNLOAD FAILED\n')
        f.close()
