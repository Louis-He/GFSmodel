import os
import time

utc = 0

def createsh():
    f = open('/root/GFS/sysreport/running.txt', 'w+')
    f.write('[' + time.strftime('%Y-%m-%d %H:%M:%S',
                              time.localtime(time.time() + utc * 60 * 60)) + ']' + 'System start.')
    f.close()
    print('[' + time.strftime('%Y-%m-%d %H:%M:%S',
                              time.localtime(time.time() + utc * 60 * 60)) + ']' + 'Write script file...')
    f = open('/root/GFS/plot.sh', 'a+')
    f.write(
        'python3 main.py\npython3 productinitialize.py\n')
    f.close()
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
                              time.localtime(time.time() + utc * 60 * 60)) + ']' + 'Script Done. Ready to run.')

def start():
    print('[' + time.strftime('%Y-%m-%d %H:%M:%S',
                              time.localtime(time.time() + utc * 60 * 60)) + ']' + 'Start script.')
    f = open('/root/GFS/sysreport/running.txt', 'a+')
    f.write(
        '[' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + utc * 60 * 60)) + ']' + '\tStart running script.\n')
    f.close()
    os.system('sh plot.sh')

createsh()
start()