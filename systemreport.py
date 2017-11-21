import web
import os
import time

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

def getdownloadstatus():
    f = open('sysreport/sysrealreport.txt')  # Read waitlist mission
    line = f.readline()
    return line

urls = (
    '/GFS/sysreport', 'sysreport'
)
app = web.application(urls, globals())

class sysreport:
    def GET(self):
        sysstatus = syscheck()
        downloadstatus = getdownloadstatus()
        result = 'Status of the system: ' + sysstatus[0] + '\n'
        result = result + 'Status of Subsystems:\n'
        result = result + 'Downloading system: ' + sysstatus[1] + '\n'
        result = result + 'Plotting system: ' + sysstatus[2] + '\n'

        # analyze system integrity
        if sysstatus[0] == 'Running':
            Tcolor = '#00ff7f'
        else:
            Tcolor = '#ff0000'

        # analyze download status
        if 'In downloading Cycle' in downloadstatus:
            Dcolor = '#00ff7f'
        elif sysstatus[1] != 'Running':
            Dcolor = '#ff0000'
        else:
            Dcolor = '#f2f200'

        f = open('sysreport.html', 'w+')
        f.write(
            '<html>'
            '<head>'
            '<title>GFS forecast automatic analyzing System status</title>'
            '<style>'
            'title { font-size : 32px;}' 
            'h1 { font-size : 24px;}' 
            'h2 { color : ' + Tcolor + '; font-size : 18px;}' 
            'subtitle { font-size : 22px;}'
            '.download {color : ' + Dcolor + ';}' 
            '</style>'
            '</head>'
            '<body>'
            '<title>GFS forecast automatic analyzing system status</title>'
            '<h1> Status of System </h1>'
            '<h1> ' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + ' UTC reporting...</h1>'
            '<h2> >>> ' + sysstatus[0] + ' </h2>'
            '<subtitle> Status of subsystem: </subtitle>'
            '<div> Downloading system: <p class=\"download\">' + sysstatus[1] + '</p></div>'
            '<div>                      ' + downloadstatus + '</div>'
            '<div> Plotting system: ' + sysstatus[2] + '</div>'
            '</body>'
            '</html>'
        )
        f.close()

        return open(r'sysreport.html', 'r').read()
        #return result

if __name__ == "__main__":
    app.run()