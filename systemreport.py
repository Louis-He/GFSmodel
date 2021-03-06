import web
import os
import time

def checkplotprocess():
    mission = []
    result = ''
    f = open('sysreport/ongingmission.sh')  # Read waitlist mission
    lines = f.readlines()
    for i in lines:
        try:
            i = i[i.index('--path ')+len('--path '):i.index(' --area CN')]
            repete = False
            for j in mission:
                if i == j:
                    repete = True
            if not repete:
                mission.append(i)
        except:
            result = 'NO MISSION'

    for i in mission:
        result = result + i +'\n'
    return result

def syscheck():
    integrity = False
    mainpro = False
    plotpro = False

    plotstatus = 'Error, NOT OPEATING!'
    mainstatus = 'Error, NOT OPEATING!'
    sysstatus = 'Error, at least one of the subsystem is NOT OPEATING!'
    plotstatusdetail = 'No plot mission at this time.'

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

        if 'python3 plotWGP.py' in line:
            plotstatusdetail = 'Geopotential height plotting is working.'
        elif 'python3 plotWTP.py' in line:
            plotstatusdetail = 'Ground condition plotting is working.'
        elif 'python3 plotrain.py' in line:
            plotstatusdetail = 'Forecast precipitation plotting is working.'

    return sysstatus, mainstatus, plotstatus, plotstatusdetail

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
        detail = checkplotprocess()

        plotdetail = sysstatus[3]
        result = 'Status of the system: ' + sysstatus[0] + '\n'
        result = result + 'Status of Subsystems:\n'
        result = result + 'Downloading system: ' + sysstatus[1] + '\n'
        result = result + 'Plotting system: ' + sysstatus[2] + '\n'
        result = result + 'Plotting system(Detail): ' + sysstatus[3] + '\n'

        # analyze system integrity
        if sysstatus[0] == 'Running':
            Tcolor = '32CD32'
        else:
            Tcolor = '#ff0000'

        # analyze download status
        if 'In downloading Cycle' in downloadstatus:
            Dcolor = '#32CD32'
        else:
            Dcolor = '#ffd700'
        if sysstatus[1] != 'Running':
            Dcolor = '#ff0000'
            downloadstatus = '[Error]Please Check!'


        # analyze plot status
        if 'working' in sysstatus[3]:
            Pcolor = '#32CD32'
        elif sysstatus[2] != 'Running':
            Pcolor = '#ff0000'
            plotdetail = '[Error]Please Check!'
        else:
            Pcolor = '#ffd700'

        # analyze subsystem status
        if sysstatus[1] == 'Running':
            scolor1 = '#32CD32'
        else:
            scolor1 = '#ff0000'
        # analyze subsystem status
        if sysstatus[2] == 'Running':
            scolor2 = '#32CD32'
        else:
            scolor2 = '#ff0000'
        if plotdetail == 'No plot mission at this time.':
            detail = 'No mission in waitlist.'

        f = open('sysreport.html', 'w+')
        f.write(
            '<html>'
            '<head>'
            '<title>GFS forecast automatic analyzing System status</title>'
            '<style>'
            'title { font-size : 32px;}' 
            'h1 { font-size : 24px;}' 
            'h2 { color : ' + Tcolor + '; font-size : 22px;}' 
            'subtitle { font-size : 22px;}'
            'download {color : ' + Dcolor + ';}'
            'plot {color : ' + Pcolor + ';}'
            'sub1 {color : ' + scolor1 + ';}'
            'sub2 {color : ' + scolor2 + ';}'
            '</style>'
            '</head>'
            '<body>'
            '<title>GFS forecast automatic analyzing system status</title>'
            '<h1> Status of System </h1>'
            '<h1> ' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + ' UTC reporting...</h1>'
            '<h2> >>> ' + sysstatus[0] + ' </h2>'
            '<subtitle> Status of subsystem: </subtitle>'
            '<br><div> Downloading system: <sub1>>>>' + sysstatus[1] + '</sub1></div>'
            '<div>&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;Status: <download>' + downloadstatus + '</download></div></br>'
            '<br><div> Plotting system: <sub2>>>>' + sysstatus[2] + '</sub2></div>'
            '<div>&emsp;&emsp;&emsp;&emsp;Status: <plot>' + plotdetail + '</plot></div></br>'
            '<br><div>&emsp;&emsp;&emsp;Working list: <sub2>>>>' + detail + '</sub2></div></br>'
            '</body>'
            '</html>'
        )
        f.close()

        return open(r'sysreport.html', 'r').read()
        #return result

if __name__ == "__main__":
    app.run()