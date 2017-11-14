import os
import time

utc = 0

def createsh():
    f = open('/root/GFS/sysreport/running.txt', 'w+')
    f.write('[' + time.strftime('%Y-%m-%d %H:%M:%S',
                              time.localtime(time.time() + utc * 60 * 60)) + ']' + '\tSystem start.\n')
    f.close()
    print('[' + time.strftime('%Y-%m-%d %H:%M:%S',
                              time.localtime(time.time() + utc * 60 * 60)) + ']' + 'Write script file...\n')
    f = open('/root/GFS/process.sh', 'w+')
    f.write(
        'python3 main.py\npython3 productinitialize_WTP.py\npython3 productinitialize_WTP_NA.py\n')
    f.close()


def start():
    print('[' + time.strftime('%Y-%m-%d %H:%M:%S',
                              time.localtime(time.time() + utc * 60 * 60)) + ']' + 'Start script.\n')
    f = open('/root/GFS/sysreport/running.txt', 'a+')
    f.write(
        '[' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + utc * 60 * 60)) + ']' + '\tStart running script.\n')
    f.close()
    os.system('sh process.sh')

createsh()
start()