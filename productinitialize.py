import os
import time

utc = 0

def plotinitialize():
    os.system('rm -rf product/')
    print('['+time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + utc * 60 * 60))+']'+'Erase expired product')
    os.system('mkdir product')
    os.system('mkdir product/WTP')
    print('[' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + utc * 60 * 60)) + ']' + 'Create product folder')
    f = open('/root/GFS/sysreport/plotreport.txt', 'w+')
    f.close()
    print('[' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + utc * 60 * 60)) + ']' + 'Create system plot report file...')
    f = open('/root/GFS/sysreport/errreport.txt', 'w+')
    f.close()
    print('[' + time.strftime('%Y-%m-%d %H:%M:%S',
                              time.localtime(time.time() + utc * 60 * 60)) + ']' + 'Create system plot error report file...')

plotinitialize()