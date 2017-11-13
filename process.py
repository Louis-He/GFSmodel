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
    f = open('/root/GFS/plot.sh', 'w+')
    f.close()
    f = open('/root/GFS/process.sh', 'w+')
    f.write(
        'python3 main.py\npython3 productinitialize.py\n')
    f.close()


def start():
    print('[' + time.strftime('%Y-%m-%d %H:%M:%S',
                              time.localtime(time.time() + utc * 60 * 60)) + ']' + 'Start script.')
    f = open('/root/GFS/sysreport/running.txt', 'a+')
    f.write(
        '[' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + utc * 60 * 60)) + ']' + '\tStart running script.\n')
    f.close()
    os.system('sh process.sh')

createsh()
start()