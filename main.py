from datetime import datetime
import time
import urllib.request
from urllib.request import urlretrieve
from apscheduler.schedulers.blocking import BlockingScheduler
#from apscheduler.schedulers.background import BackgroundScheduler
import os
#import progressbar

utc = 0

#decide the target init forecast time
def targetinittime():
    global downloadhour
    timechange = -1 * utc
    nowtime = time.time() + timechange * 60 * 60  # struct time of UTC
    result = time.strftime("%H", time.localtime(nowtime))  # hour of UTC time
    if int(result) >= 21:
        hourresult = '18'
    elif int(result) < 9:
        hourresult = '00'
    elif int(result) < 15:
        hourresult = '06'
    elif int(result) < 21:
        hourresult = '12'

    returnlist = []
    isdownload = []
    for i in range(0, len(downloadhour)):
        returnlist.append(hourresult)
        isdownload.append(False)

    return returnlist, isdownload

# return the URL of the latest GFS model (3 hours after the initial)
# return [0]:the URL of target file;    [1]:the filename
def decideURL2(forecasthour, isexist):
    global utc
    hourresult = ''

    timechange = -1 * utc
    nowtime = time.time() + timechange * 60 * 60 # struct time of UTC
    result = time.strftime("%H", time.localtime(nowtime))  # hour of UTC time
    #print(result)

    if int(result) >= 18:
        hourresult = '18'
    elif int(result) < 6:
        hourresult = '00'
    elif int(result) < 12:
        hourresult = '06'
    elif int(result) < 18:
        hourresult = '12'
    '''
    elif int(result) < 4:
        hourresult = '18'
        nowtime = nowtime - 24 * 60 * 60
    '''
    assumetime = time.strftime("%Y%m%d", time.localtime(nowtime)) + hourresult + '0000'  # hour of UTC time
    assumetimestamp = time.mktime(time.strptime(assumetime, "%Y%m%d%H%M%S"))
    if not isexist:
        assumetimestamp = assumetimestamp - 6 * 60 * 60

    #http://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl?file=gfs.t12z.pgrb2.0p25.f000&all_var=on&leftlon=0&rightlon=360&toplat=90&bottomlat=-90&dir=%2Fgfs.2017102712

    result = time.strftime("%Y%m%d%H", time.localtime(assumetimestamp)) # final hour of UTC time
    filename = 'GFS' + result + '.f' + forecasthour
    #print(filename)
    result = 'http://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl?file=gfs.t'+ hourresult +'z.pgrb2.0p25.f' + forecasthour + '&all_var=on&leftlon=0&rightlon=360&toplat=90&bottomlat=-90&dir=%2Fgfs.' + result
    return [result, 'gfs.' + filename]

# return the URL of the latest GFS model (4 hours after the initial)
def decideURL(forecasthour):
    global utc
    hourresult = ''

    timechange = -1 * utc
    nowtime = time.time() + timechange * 60 * 60 # struct time of UTC
    result = time.strftime("%H", time.localtime(nowtime))  # hour of UTC time
    #print(result)

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
    #print(filename)
    result = 'http://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl?file=gfs.t'+ hourresult +'z.pgrb2.0p25.f' + forecasthour + '&all_var=on&leftlon=0&rightlon=360&toplat=90&bottomlat=-90&dir=%2Fgfs.' + result
    return [result, 'gfs.' + filename]

#downLoadPicFromURL(local path，source URL)
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
    f = open('sysreport/downloadreport.txt', 'w+')
    f.close()
    print('[' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + utc * 60 * 60)) + ']' + 'Create system download report file...')
    f = open('sysreport/sysrealreport.txt', 'w+')
    f.close()
    print('[' + time.strftime('%Y-%m-%d %H:%M:%S',
                              time.localtime(time.time() + utc * 60 * 60)) + ']' + 'Create system realtime file...')
    f = open('sysreport/ongingmission.sh', 'w+')
    f.close()
    print('[' + time.strftime('%Y-%m-%d %H:%M:%S',
                              time.localtime(time.time() + utc * 60 * 60)) + ']' + 'Create ongingmission script...')
    f = open('sysreport/waitlistmission.sh', 'w+')
    f.close()
    print('[' + time.strftime('%Y-%m-%d %H:%M:%S',
                              time.localtime(time.time() + utc * 60 * 60)) + ']' + 'Create waitlistmission script...')

def downloadfile(forecasthour,isexist):
    #global bar
    downloadinfo = decideURL2(forecasthour,isexist)
    print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time() + utc * 60 * 60)) + ']Dowanloading file... from URL: ' +downloadinfo[0])
    path = 'rawfile/' + downloadinfo[1]
    try:
        urlretrieve(downloadinfo[0], path)
        print('[' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + utc * 60 * 60)) + ']Dowanloading file... from URL: ' + downloadinfo[1] + 'SUCCESS')
        f = open('/root/GFS/sysreport/downloadreport.txt', 'a+')
        f.write('[' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + utc * 60 * 60)) + ']' + '\t' +
                downloadinfo[1] + ' DOWNLOAD SUCCESS\n')
        f.close()
        f = open('/root/GFS/sysreport/running.txt', 'a+')
        f.write('[' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + utc * 60 * 60)) + ']' + '\t' +
                downloadinfo[1] + ' DOWNLOAD SUCCESS\n')
        f.close()
        addmission(downloadinfo[1])
        return True
    except:
        if isexist:
            print('(FILE DO NOT EXIST)[' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + utc * 60 * 60)) + ']Dowanloading file... from URL: ' + downloadinfo[1] + 'ERROR')
        else:
            print('(UNEXPECTED ERR)[' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + utc * 60 * 60)) + ']Dowanloading file... from URL: ' + downloadinfo[1] + 'ERROR')
            f = open('/root/GFS/sysreport/downloadreport.txt', 'a+')
            f.write('[' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + utc * 60 * 60)) + ']' + '\t' +
                    downloadinfo[1] + ' DOWNLOAD FAILED\n')
            f.close()
            f = open('/root/GFS/sysreport/running.txt', 'a+')
            f.write('[' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + utc * 60 * 60)) + ']' + '\t' +
                    downloadinfo[1] + ' DOWNLOAD FAILED\n')
            f.close()
        return False

def istruelist(list):
    result = True
    for i in list:
        if not i:
            result = False

    return result

# main method
def mainmethod():
    #global bar
    global successdownload

    # initialize progressbar
    '''
    bar = progressbar.ProgressBar(widgets=[
        ' [', progressbar.Timer(), '] ',
        progressbar.Bar(),
    ], redirect_stdout=True)
    '''

    global downloadhour
    inittime = time.time() + (-1) * utc * 60 * 60

    #initialize the program
    initialize()

    #set the forecast hour of the file from GFS
    downloadhour = ['000','006', '012', '018', '024','030', '036', '042','048', '054', '060', '066','072', '078', '084',
                    '090','096','102', '108', '114', '120', '126', '132', '138', '144', '150', '156', '162', '168', '174',
                    '180', '186', '192', '198', '204', '210', '216', '222', '228', '234', '240']
    successdownload = 0
    # set progressbar
    #bar.max_value = len(downloadhour)
    #bar.min_value = 0
    #bar.update(0)
    #scheduler = BackgroundScheduler()
    #scheduler.add_job(updateprogessbar, 'interval', seconds = 1)  # 24hr
    #scheduler.start()

    initialprocess = targetinittime()
    isdownload = initialprocess[1] # initial all false, true: isdownload; false: not download yet

    '''
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
    '''

    while not istruelist(isdownload):
    #reqiured download file
        print('[' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(
                time.time() + utc * 60 * 60)) + ']Start downloading cycle.')
        count = 0
        tmpbool = True
        for i in downloadhour:
            if not isdownload[count] and tmpbool:
                f = open('sysreport/sysrealreport.txt', 'w+')
                f.write('In downloading Cycle. Downloading')
                f.close()
                tmpbool = downloadfile(downloadhour[count], True)
                if tmpbool:
                    isdownload[count] = True
                    successdownload += 1
            count += 1
        # print(isdownload)
        print('[' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(
                time.time() + utc * 60 * 60)) + ']No more new file. Start sleeping cycle...[5 min]')
        f = open('sysreport/sysrealreport.txt', 'w+')
        f.write('In downloading Cycle. Sleep for next file')
        f.close()
        time.sleep(120) # sleep 2 mins for another try

    finishtime = time.time() + (-1) * utc * 60 * 60
    f = open('sysreport/sysrealreport.txt', 'w+')
    f.write('Wait For next download window.')
    f.close()
    print('*--------------------------------------------*')
    print('[' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(
                time.time() + utc * 60 * 60)) + ']Download cycle ends.')
    print('TOTAL RUNNING TIME:' + str(finishtime-inittime) + 's')

# decide First start time
def startmain():
    nowtime = time.time()
    result = int(time.strftime("%H%M", time.localtime(nowtime)))  # hour of UTC time
    print('nowtime: (HHMM)' + str(result))
    '''
    forecast1 = 325
    forecast2 = 925
    forecast3 = 1525
    forecast4 = 2125
    '''

    if result > 325 and result < 330:
        return True
    elif result > 925 and result < 930:
        return True
    elif result > 1525 and result < 1530:
        return True
    elif result > 2125 and result < 2130:
        return True
    return False

# add onging mission list
def addmission(filename):
    path = 'rawfile/'
    files = os.listdir(path)
    for i in files:
        if filename[-4:] == i[-4:]:
            os.system('rm product/WTP/' + i)
            os.system('rm product/WGP/' + i)
            os.system('rm product/WTPrain/' + i)
            print('delete same product in the previous hour')
    f = open('sysreport/waitlistmission.sh', 'a+')
    f.write('python3 plotWGP.py --path ' + filename + ' --area CN')
    f.write('python3 plotWTP.py --path ' + filename + ' --area CN')
    f.write('python3 plotrain.py --path ' + filename + ' --area CN')
    f.close()

initialize()
print('[Please Wait]System First Start: Wait for next closest GFS files download time window...')
print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
while not startmain():
    time.sleep(60)
    f = open('sysreport/sysrealreport.txt','w+')
    f.write('Wait For next download window.')
    f.close()
# main operation
scheduler = BlockingScheduler()
scheduler.add_job(mainmethod, 'interval', seconds = 6 * 60 * 60)
print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
mainmethod()
try:
    scheduler.start()
except (KeyboardInterrupt, SystemExit):
    pass