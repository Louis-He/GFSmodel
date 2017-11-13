import os
import time

utc = 0

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
    f = open('/root/GFS/plot.sh', 'w+')
    f.close()
    print('[' + time.strftime('%Y-%m-%d %H:%M:%S',
                              time.localtime(time.time() + utc * 60 * 60)) + ']' + 'Initialize script file...')
    print('[' + time.strftime('%Y-%m-%d %H:%M:%S',
                              time.localtime(time.time() + utc * 60 * 60)) + ']' + 'Initialized. Ready to plot.')

def createsh():
    print('[' + time.strftime('%Y-%m-%d %H:%M:%S',
                              time.localtime(time.time() + utc * 60 * 60)) + ']' + 'Write script file...')
    path = 'rawfile/'
    files = os.listdir(path)
    print(files)
    for file in files:
        if file[0:3] == 'gfs':
            try:
                f = open('/root/GFS/plot.sh', 'a+')
                f.write(
                    'python3 plotWTP.py --path ' + file + '\n')
                f.close()
            except:
                print('[FATAL ERR] PROGRAM STOP' + file)
                f = open('/root/GFS/sysreport/errreport.txt', 'a+')
                f.write(
                    '[' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + utc * 60 * 60)) + ']' + '\t' +
                    file + ' SCRIPT INITIALIZE FAILED! PLEASE CHECK\n')
                f.close()
    print('[' + time.strftime('%Y-%m-%d %H:%M:%S',
                              time.localtime(time.time() + utc * 60 * 60)) + ']' + 'Script Done. Ready to plot.')

def plot():
    print('[' + time.strftime('%Y-%m-%d %H:%M:%S',
                              time.localtime(time.time() + utc * 60 * 60)) + ']' + 'Start script.')
    f = open('/root/GFS/sysreport/plotreport.txt', 'a+')
    f.write(
        '[' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + utc * 60 * 60)) + ']' + '\tStart plot.\n')
    f.close()
    os.system('sh plot.sh')

initialize()
createsh()