import time
import os
from apscheduler.schedulers.blocking import BlockingScheduler

utc = 0
# draw all the plot in the waitlist file
def regular():
    # copy waitlistmission to onging
    os.system('cp sysreport/waitlistmission.sh sysreport/ongingmission.sh')
    # delete expired waitlist
    os.system('rm sysreport/waitlistmission.sh')
    # create new waitlist file for further mission
    f = open('sysreport/waitlistmission.sh', 'w+')
    f.close()

    # execute the latest onging mission
    os.system('sh sysreport/ongingmission.sh')

# determine whether there are new waitlist plots
def isnewmission():
    f = open('/root/airchina/status.txt')  # Read waitlist mission
    line = f.readline()
    if line != '':
        f.close()
        return False
    f.close()
    # f = open('/root/qxahz/stations.txt')
    f = open('sysreport/waitlistmission.sh')  # Read waitlist mission
    line = f.readline()
    if line != '':
        f.close()
        return True
    f.close()
    return False

# copy latest prduct to HOME model
def copyfile():
    os.system('rm -rf /home/model/GFS')
    os.system('cp -r product/ /home/model/GFS')

# main program to update all plots to the latest
print('[' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + utc * 60 * 60)) + ']' + '\tPlot System Start')
while True:
    if isnewmission():
        print('[' + time.strftime('%Y-%m-%d %H:%M:%S',
                                  time.localtime(time.time() + utc * 60 * 60)) + ']' + '\tPlot Cycle Start')
        regular()
        copyfile()
    else:
        print('NO new mission or onging mission is in place...')
        time.sleep(60)