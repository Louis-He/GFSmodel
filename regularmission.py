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
    # f = open('/root/qxahz/stations.txt')
    f = open('sysreport/waitlistmission.sh')  # Read waitlist mission
    line = f.readline()
    if line != '':
        f.close()
        return True
    f.close()
    return False

# main program to update all plots to the latest
while True:
    if isnewmission():
        regular()
    else:
        time.sleep(60)