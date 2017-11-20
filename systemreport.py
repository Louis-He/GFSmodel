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

        if sysstatus[0] == 'Running':
            color = '#00FF7F'
        else:
            color = '#ff0000'
        f = open('sysreport.html', 'w+')
        f.write(
            '<html>'
            '<head>'
            '<title>GFS forecast automatic analyzing System status</title>'
            '<style>'
            'title { font-size : 32px;}' 
            'h1 { font-size : 24px;}' 
            'h2 { color : ' + color + '; font-size : 18px;}' 
            'subtitle { font-size : 22px;}' 
            '</style>'
            '</head>'
            '<body>'
            '<title>GFS forecast automatic analyzing system status</title>'
            '<h1> Status of System </h1>'
            '<h2> ·' + sysstatus[0] + ' </h2>'
            '<subtitle> Status of subsystem: </subtitle>'
            '<div> Downloading system: ' + sysstatus[1] + '</div>'
            '<div> Plotting system: ' + sysstatus[2] + '</div>'
            '</body>'
            '</html>'
        )
        f.close()

        return open(r'sysreport.html', 'r').read()
        #return result

if __name__ == "__main__":
    app.run()