import web
import os

def syscheck():
    integrity = False
    mainpro = False
    plotpro = False

    plotstatus = 'Error, NOT OPEATING!'
    mainstatus = 'Error, NOT OPEATING!'
    sysstatus = 'Error, NOT OPEATING!'

    command = 'ps -ef |grep python3' #check python3 program
    r = os.popen(command)
    info = r.readlines()
    for line in info:
        line = line.strip('\r\n')
        if 'python3 regularmission.py' in line:
            plotpro = True
            plotstatus = 'Running'
        if 'python3 main.py' in line:
            mainpro = True
            mainstatus = 'Running'
        if plotpro and mainpro:
            integrity = True
            sysstatus = 'Running'

    return plotstatus,mainstatus,sysstatus

urls = (
    '/GFS/sysreport', 'sysreport'
)
app = web.application(urls, globals())

class sysreport:
    def GET(self):
        sysstatus = syscheck()
        result = 'Status of the system: ' + sysstatus[0] + '\n'
        result = result + 'Status of Subsystems:\n'
        result = result + 'Downloading system: ' + sysstatus[1] + '\n'
        result = result + 'Plotting system: ' + sysstatus[2] + '\n'
        return result

if __name__ == "__main__":
    app.run()