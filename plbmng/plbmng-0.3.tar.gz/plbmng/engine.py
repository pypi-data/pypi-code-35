#! /usr/bin/env python3
# Author: Martin Kacmarcik
#License: MIT
# For my Diploma thesis at Faculty of Electrical Engineering -- Brno, University of Technology

import webbrowser
import folium
import subprocess
import signal
import re
import locale
from dialog import Dialog
import hashlib
import sqlite3
from platform import system
from multiprocessing import Pool, Lock, Value
import sys
import os
import csv


# local imports
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
from lib import full_map
from lib import port_scanner


# Constant definition
OPTION_LOCATION = 0
OPTION_IP = 1
OPTION_DNS = 2
OPTION_CONTINENT = 3
OPTION_COUNTRY = 4
OPTION_REGION = 5
OPTION_CITY = 6
OPTION_URL = 7
OPTION_NAME = 8
OPTION_LAT = 9
OPTION_LON = 10
VERSION = "0.3"

#global variables
base = None
increment = None
path = ""

# Initial settings
locale.setlocale(locale.LC_ALL, '')
d = Dialog(dialog="dialog")
d.set_background_title("Planetlab Server Manager "+VERSION)


def signal_handler(sig, frame):
    clear()
    print('Terminating program. You have pressed Ctrl+C')
    exit(1)


def getPath():
    global path
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    path = os.path.dirname(os.path.realpath(__file__))
    return path


def clear():
    os.system("clear")


def testPing(target, returnbool=False):
    pingPacketWaitTime = 800
    if system().lower() == 'windows':
        pingParam = '-n'
    else:
        pingParam = '-c'
    command = ['ping', pingParam, '1', target, '-W', str(pingPacketWaitTime)]
    p = subprocess.Popen(command, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    # prepare the regular expression to get time
    if system().lower() == 'windows':
        avg = re.compile('Average = ([0-9]+)ms')
    else:
        avg = re.compile(
            'min/avg/max/[a-z]+ = [0-9.]+/([0-9.]+)/[0-9.]+/[0-9.]+')
    avgStr = avg.findall(str(p.communicate()[0]))
    if p.returncode != 0:
        if not returnbool:
            return "Not reachable via ICMP"
        return False
    else:
        p.kill()
        if not returnbool:
            return avgStr[0]+" ms"
        return True


def testSsh(target, printwarn=True):
    result = port_scanner.testPortAvailability(target, 22)
    if (result is True or result is False):
        return result
    elif result is 98:
        if printwarn is True:
            d.msgbox("Hostname could not be resolved. Either the server has been removed, \
                     your network is not working or you have wrongly set DNS.", height=0, width=0)
        return result
    elif result is 97:
        if printwarn is True:
            d.msgbox(
                "Error while connecting to server. Please check your network settings.")
        return result


def verifyApiCredentialsExist():
    with open(path+"/conf/plbmng.conf", 'r') as config:
        for line in config:
            if re.search('USERNAME', line):
                username = re.sub('USERNAME="(.*)"', r'\1', line).rstrip()
                if not username:
                    return False
            elif re.search('PASSWORD', line):
                password = re.sub('PASSWORD="(.*)"', r'\1', line).rstrip()
                if not password:
                    return False
    return True


def verifySshCredentialsExist():
    with open(path+"/conf/plbmng.conf", 'r') as config:
        for line in config:
            if re.search('SLICE', line):
                planetlab_slice = re.sub('SLICE="(.*)"', r'\1', line).rstrip()
                if not planetlab_slice:
                    return False
            elif re.search('SSH_KEY', line):
                key = re.sub('SSH_KEY="(.*)"', r'\1', line).rstrip()
                if not key:
                    return False
    return True

# parent function to update availability DB that controls multiple processes


def updateAvailabilityDatabaseParent(mode=None):
    if mode == 'cron':
        path = getPath()
    nodes = getNodes(False)
    increment = Value('f', 0)
    increment.value = float(100/len(nodes))
    base = Value('f', 0)
    lock = Lock()
    d.gauge_start()
    pool = Pool(50, initializer=multiProcessingInit,
                initargs=(lock, base, increment, ))
    pool.map(updateAvailabilityDatabase, nodes)
    pool.close()
    pool.join()
    d.gauge_update(100, "Completed")
    exit_code = d.gauge_stop()
    d.msgbox("Availability database has been successfully updated")


def multiProcessingInit(l, b, i):
    global lock
    lock = l
    global base
    base = b
    global increment
    increment = i


def updateProgressBarMultiProcessing(increment_number):
    global d
    d.gauge_update(int(increment_number))


def updateAvailabilityDatabase(node):
    # inint block
    db = sqlite3.connect('database/internal.db')
    cursor = db.cursor()
    # action block
    hash_object = hashlib.md5(node[2].encode())
    ssh_result = 'T' if testSsh(node[2], False) == True else 'F'
    ping_result = 'T' if testPing(node[1], True) == True else 'F'
    # find if object exists in the database
    cursor.execute('SELECT nkey from AVAILABILITY where \
            shash = \"'+str(hash_object.hexdigest())+'\";')
    if cursor.fetchone() is None:
        # the object yet doesn't exist
        cursor.execute("INSERT into AVAILABILITY(shash, shostname, bssh, bping) VALUES\
                        (\""+hash_object.hexdigest()+"\", \""+node[2]+"\",\
                        \""+ssh_result+"\", \""+ping_result+"\")")
    else:
        # object exists, just update results
        cursor.execute("UPDATE availability SET bssh=\""+ssh_result+"\", bping=\"" +
                       ping_result+"\" WHERE shash=\""+hash_object.hexdigest()+"\"")
    lock.acquire()
    base.value = base.value + increment.value
    updateProgressBarMultiProcessing(base.value)
    lock.release()
    # clean up
    db.commit()
    db.close()


def getSshKey():
    sshPath = ""
    with open(path+"/conf/plbmng.conf", 'r') as config:
        for line in config:
            if re.search('SSH_KEY', line):
                sshPath = (re.sub('SSH_KEY=', '', line)).rstrip()
    return sshPath


def getSshUser():
    user = ""
    with open(path+"/conf/plbmng.conf", 'r') as config:
        for line in config:
            if re.search('SLICE=', line):
                user = (re.sub('SLICE=', '', line)).rstrip()
    return user


def getUser():
    user = ""
    with open(path+"/conf/plbmng.conf", 'r') as config:
        for line in config:
            if re.search('USERNAME=', line):
                user = (re.sub('USERNAME=', '', line)).rstrip()
    return user


def getPasswd():
    passwd = ""
    with open(path+"/conf/plbmng.conf", 'r') as config:
        for line in config:
            if re.search('PASSWORD=', line):
                passwd = (re.sub('PASSWORD=', '', line)).rstrip()
    return passwd


def getNodes(checkConfiguration=True, chooseAvailabilityOption=None):
    # Initialize filtering settings
    db = sqlite3.connect('database/internal.db')
    cursor = db.cursor()
    if chooseAvailabilityOption is None:
        cursor.execute('SELECT * from configuration where senabled=\'T\';')
        configuration = cursor.fetchall()
        if not configuration:
            sql = 'select shostname from availability'
        else:
            sql = 'select shostname from availability where'
            for item in configuration:
                if re.match(r'.*where$', sql):
                    sql = sql + ' b'+item[1]+'=\'T\''
                else:
                    sql = sql + ' and b'+item[1]+'=\'T\''
    elif chooseAvailabilityOption == 1:
        sql = "select shostname from availability where bping='T'"
    elif chooseAvailabilityOption == 2:
        sql = "select shostname from availability where bssh='T'"
    elif chooseAvailabilityOption == 3:
        sql = "select shostname from availability"
    cursor.execute(sql)
    returnedValuesSql = cursor.fetchall()
    # convert returned tuples to list
    serverList = []
    for item in returnedValuesSql:
        serverList.append(item[0])
    # open node file and append to the nodes if the element exists in the serverList
    nodeFile = path+'/database/default.node'
    nodes = []
    with open(nodeFile) as tsv:
        for line in csv.reader(tsv, delimiter='\t'):
            if line[0] == '# ID':
                continue
            try:
                if checkConfiguration:
                    if line[2] in serverList:
                        nodes.append(line)
                else:
                    nodes.append(line)
            except ValueError:
                pass
    # clean up block
    db.close()
    return nodes


def getAllNodes():
    user = getUser()
    passwd = getPasswd()
    if user != "" and passwd != "":
        os.system("myPwd=$(pwd); cd "+path+"; python3 lib/planetlab_list_creator.py -u \"" +
                  user+"\" -p \""+passwd+"\" -o ./; cd $(echo $myPwd)")
    else:
        needToFillPasswdFirstInfo()


def isFirstRun():
    isFirst = path+'/database/first.boolean'
    with open(isFirst, 'r') as isFirstFile:
        bIsFirst = isFirstFile.read().strip('\n')
    if bIsFirst == "True":
        with open(isFirst, 'w') as isFirstFile:
            isFirstFile.write("False")
        return True
    else:
        return False


def lastServerMenu():
    infoAboutNodeDic, chosenNode = getLastServerAccess()
    returnedChoice = printServerInfo(infoAboutNodeDic)
    if returnedChoice == None:
        return
    elif not returnedChoice:
        return
    elif int(returnedChoice) == 1:
        connect(int(returnedChoice), chosenNode)
    elif int(returnedChoice) == 2:
        connect(int(returnedChoice), chosenNode)
    elif int(returnedChoice) == 3:
        showOnMap(chosenNode, infoAboutNodeDic)


def updateLastServerAccess(infoAboutNodeDic, chosenNode):
    lastServerFile = path+'/database/last_server.node'
    with open(lastServerFile, 'w') as lastServerFile:
        lastServerFile.write(repr((infoAboutNodeDic, chosenNode)))


def getLastServerAccess():
    lastServerFile = path+'/database/last_server.node'
    with open(lastServerFile, 'r') as lastServerFile:
        infoAboutNodeDic, chosenNode = eval(lastServerFile.read().strip('\n'))
    return infoAboutNodeDic, chosenNode


def searchNodes(option, regex=None):
    nodes = getNodes()
    answers = []
    choices = []
    counter = 1
    # non-LOCATION search
    if option is not OPTION_LOCATION:
        for item in nodes:
            if re.search(regex, item[option]):
                answers.append(item)
        if len(answers) == 0:
            returnedChoice = searchNodesGui(False)
        else:
            # prepare choices for GUI
            for item in answers:
                choices.append((str(counter), item[option]))
                counter += 1
            returnedChoice = searchNodesGui(choices)
    # LOCATION based search
    else:
        for item in nodes:
            answers.append(item[OPTION_CONTINENT])
        continents = sorted(set(answers))
        # prepare choices for GUI
        for item in continents:
            choices.append((str(counter), item))
            counter += 1
        returnedChoice = searchNodesGui(choices)
        if returnedChoice == None:
            return
        answers = []
        choices = []
        counter = 1
        for item in nodes:
            if re.search(continents[int(returnedChoice)-1], item[OPTION_CONTINENT]):
                answers.append(item[OPTION_COUNTRY])
        countries = sorted(set(answers))
        # prepare choices for GUI
        for item in countries:
            choices.append((str(counter), item))
            counter += 1
        returnedChoice = searchNodesGui(choices)
        if returnedChoice == None:
            return
        answers = []
        choices = []
        counter = 1
        for item in nodes:
            if re.search(countries[int(returnedChoice)-1], item[OPTION_COUNTRY]):
                answers.append(item[OPTION_DNS])
        hostnames = sorted(set(answers))
        # prepare choices for GUI
        for item in hostnames:
            choices.append((str(counter), item))
            counter += 1
        returnedChoice = searchNodesGui(choices)
    if returnedChoice == None:
        return
    else:
        returnedChoice, infoAboutNodeDic, chosenNode = getServerInfo(
            choices[int(returnedChoice)-1][1], option, nodes)
    if returnedChoice == None:
        return
    elif not returnedChoice:
        return
    elif int(returnedChoice) == 1:
        connect(int(returnedChoice), chosenNode)
    elif int(returnedChoice) == 2:
        connect(int(returnedChoice), chosenNode)
    elif int(returnedChoice) == 3:
        showOnMap(chosenNode, infoAboutNodeDic)


def connect(mode, node):
    clear()
    key = getSshKey()
    user = getSshUser()
    if mode == 1:
        return_value = os.system(
            "ssh -o \"StrictHostKeyChecking = no\" -o \"UserKnownHostsFile=\
            /dev/null\" -i "+key+" "+user+"@"+node[OPTION_IP])
        if return_value is not 0:
            d.msgbox("Error while connecting. Please verify your credentials.")
    elif mode == 2:
        return_value = os.system("mc sh://"+user+"@"+node[OPTION_IP]+":/home")
        if return_value is not 0:
            d.msgbox("Error while connecting. Please verify your credentials.")
    else:
        return


def showOnMap(node, nodeInfo=""):
    _stderr = os.dup(2)
    os.close(2)
    _stdout = os.dup(1)
    os.close(1)
    fd = os.open(os.devnull, os.O_RDWR)
    os.dup2(fd, 2)
    os.dup2(fd, 1)
    latitude = float(node[-2])
    longitude = float(node[-1])
    name = node[OPTION_DNS]
    nodeMap = folium.Map(location=[latitude, longitude],
                         zoom_start=2, min_zoom=2)
    if nodeInfo == "":
        folium.Marker([latitude, longitude], popup=name).add_to(nodeMap)
    else:
        folium.Marker([latitude, longitude], popup=(
            nodeInfo["text"].replace('\n', '<br>'))).add_to(nodeMap)
    nodeMap.save('/tmp/map_plbmng.html')
    try:
        webbrowser.get().open('file://' + os.path.realpath('/tmp/map_plbmng.html'))
    finally:
        os.close(fd)
        os.dup2(_stderr, 2)
        os.dup2(_stdout, 1)


def plotServersOnMap(mode):
    _stderr = os.dup(2)
    os.close(2)
    _stdout = os.dup(1)
    os.close(1)
    fd = os.open(os.devnull, os.O_RDWR)
    os.dup2(fd, 2)
    os.dup2(fd, 1)
    # update base_data.txt file based on latest database with nodes
    nodes = getNodes(True, int(mode))
    with open('/tmp/base_data.txt', "w") as baseDataFile:
        for node in nodes:
            baseDataFile.write(node[2]+'\t'+node[-2]+'\t'+node[-1]+'\n')
    os.system('cat /tmp/base_data.txt | sort -n -k2 -u > ' +
              path+'/lib/base_data.txt')
    full_map.plot_server_on_map()
    mapFile = "map_full.html"
    try:
        webbrowser.get().open('file://' + os.path.realpath(path+"/"+mapFile))
    finally:
        os.close(fd)
        os.dup2(_stderr, 2)
        os.dup2(_stdout, 1)


def getServerInfo(serverId, option, nodes=None):
    if nodes == None:
        nodes = getNodes()
    if option == 0:
        option = OPTION_DNS
    if isinstance(serverId, str):
            # in nodes find the chosenOne node
        chosenOne = ""
        for item in nodes:
            if re.search(serverId, item[option]):
                chosenOne = item
                break
        if chosenOne == "":
            print("Internal error, please file a bug report via PyPi")
            exit(99)
        # get information about servers
        infoAboutNodeDic = dict()
        region, city, url, fullname, lat, lon = getInfoFromNode(chosenOne)
        infoAboutNodeDic["region"] = region
        infoAboutNodeDic["city"] = city
        infoAboutNodeDic["url"] = url
        infoAboutNodeDic["fullname"] = fullname
        infoAboutNodeDic["lat"] = lat
        infoAboutNodeDic["lon"] = lon
        infoAboutNodeDic["icmp"] = testPing(chosenOne[OPTION_IP])
        infoAboutNodeDic["sshAvailable"] = testSsh(chosenOne[OPTION_DNS])
        infoAboutNodeDic["text"] = """
            NODE: %s
            IP: %s
            CONTINENT: %s
            COUNTRY: %s
            REGION: %s
            CITY: %s
            URL: %s
            FULL NAME: %s
            LATITUDE: %s
            LONGITUDE: %s
            ICMP RESPOND: %s
            SSH AVAILABLE: %r
            """ % (chosenOne[OPTION_DNS],
                   chosenOne[OPTION_IP],
                   chosenOne[OPTION_CONTINENT],
                   chosenOne[OPTION_COUNTRY],
                   infoAboutNodeDic["region"],
                   infoAboutNodeDic["city"],
                   infoAboutNodeDic["url"],
                   infoAboutNodeDic["fullname"],
                   infoAboutNodeDic["lat"],
                   infoAboutNodeDic["lon"],
                   infoAboutNodeDic["icmp"],
                   infoAboutNodeDic["sshAvailable"])
        if infoAboutNodeDic["sshAvailable"] is True or infoAboutNodeDic["sshAvailable"] is False:
            # update last server access database
            updateLastServerAccess(infoAboutNodeDic, chosenOne)
            return printServerInfo(infoAboutNodeDic), infoAboutNodeDic, chosenOne
        else:
            return False, False, False


def getInfoFromNode(node):
    region = node[5]
    city = node[6]
    url = node[7]
    fullname = node[8]
    lat = node[9]
    lon = node[10]
    return region, city, url, fullname, lat, lon


def removeCron():
    os.system("crontab -l | grep -v \"plbmng crontab\" | crontab -")


def addToCron(mode):
    if int(mode) == 2:
        line = "@daily plbmng crontab"
    elif int(mode) == 3:
        line = "@weekly plbmng crontab"
    elif int(mode) == 4:
        line = "@monthly plbmng crontab"
    os.system("echo \"$(crontab -l ; echo "+line+")\" | crontab -")

###################
#  GUI functions  #
###################


def printServerInfo(infoAboutNodeDic):
    if not verifySshCredentialsExist():
        preparedChoices = [("1", "Connect via SSH (Credentials not set!)"),
                           ("2", "Connect via MC (Credentials not set!)"),
                           ("3", "Show on map")]
    else:
        preparedChoices = [("1", "Connect via SSH"),
                           ("2", "Connect via MC"),
                           ("3", "Show on map")]
    code, tag = d.menu(
        infoAboutNodeDic["text"], height=0, width=0, menu_height=0, choices=preparedChoices)
    if code == d.OK:
        return tag
    else:
        return None


def searchNodesGui(prepared_choices):
    if not prepared_choices:
        d.msgbox("No results found.", width=0, height=0)
        return None
    while True:
        code, tag = d.menu("These are the results:",
                           choices=prepared_choices,
                           title="Search results")
        if code == d.OK:
            return tag
        else:
            return None


def firstRunMessage():
    d.msgbox("This is your first run of the application. Please go to 'Set Credentials' menu and set your credentials now.", height=0, width=0)


def needToFillPasswdFirstInfo():
    d.msgbox("Credentials are not set. Please go to menu and set them now")


def initInterface():
    getPath()
    signal.signal(signal.SIGINT, signal_handler)
    if isFirstRun():
        firstRunMessage()
    while True:
        # Main menu
        code, tag = d.menu("Choose one of the following options:",
                           choices=[("1", "Access servers"),
                                    ("2", "Monitor servers"),
                                    ("3", "Plot map"),
                                    ("4", "Set credentials"),
                                    ("5", "About")],
                           title="MAIN MENU")

        if code == d.OK:
            # Acess servers
            if tag == "1":
                accessServersGui()
            # Meausre servers
            elif tag == "2":
                monitorServersGui()
            # Plot servers on map
            elif tag == "3":
                plotServersOnMapGui()
            # Set crdentials
            elif tag == "4":
                setCredentialasGui()
            elif tag == "5":
                aboutGui()
        else:
            clear()
            exit(0)


def setCredentialasGui():
    code, text = d.editbox(path+'/conf/plbmng.conf', height=0, width=0)
    if code == d.OK:
        with open(path+'/conf/plbmng.conf', "w") as configFile:
            configFile.write(text)


def filteringOptionsGui():
    # inint the database to pull configuration data
    db = sqlite3.connect('database/internal.db')
    cursor = db.cursor()
    cursor.execute("select senabled from configuration where sname='ssh'")
    ssh_enabled = True if cursor.fetchone()[0] == 'T' else False
    cursor.execute("select senabled from configuration where sname='ping'")
    ping_enabled = True if cursor.fetchone()[0] == 'T' else False
    # Render the GUI
    code, t = d.checklist(
        "Press SPACE key to choose filtering options", height=0, width=0, list_height=0,
        choices=[("1", "Enable SSH accessible machines", ssh_enabled),
                 ("2", "Enable PING accessible machines", ping_enabled)], )
    # Detect changes using simple combination and update the database based on result
    if '1' in t and not ssh_enabled:
        cursor.execute(
            'UPDATE configuration SET senabled="T" where sname="ssh"')
        db.commit()
    elif '1' not in t and ssh_enabled:
        cursor.execute(
            'UPDATE configuration SET senabled="F" where sname="ssh"')
        db.commit()
    if '2' in t and not ping_enabled:
        cursor.execute(
            'UPDATE configuration SET senabled="T" where sname="ping"')
        db.commit()
    elif '2' not in t and ping_enabled:
        cursor.execute(
            'UPDATE configuration SET senabled="F" where sname="ping"')
        db.commit()
    # Clean up database
    db.close()


def aboutGui():
    d.msgbox("""
            PlanetLab Server Manager is an interactive graphical enabled server inventory tool.
            Project supervisor:
                Dan Komosny
            Authors:
                Tomas Andrasov
                Filip Suba
                Martin Kacmarcik

            Version """+VERSION+"""
            This application is under MIT license.
            """, width=0, height=0, title="About")

# Plot servers on map part of GUI


def plotServersOnMapGui():
    while True:
        code, tag = d.menu("Choose one of the following options:",
                           choices=[("1", "Plot servers reponding to ping"),
                                    ("2", "Plot ssh available servers"),
                                    ("3", "Plot all servers")],
                           title="Map menu")
        if code == d.OK:
            plotServersOnMap(tag)
            return
        else:
            return

# Monitor servers part of GUI


def monitorServersGui():
    if not verifyApiCredentialsExist():
        d.msgbox("Warning! Your credentials for PlanetLab API are not set. Please use 'Set credentials' option in main menu to set them.")
    while True:
        code, tag = d.menu("Choose one of the following options:",
                           choices=[("1", "Set automatic update of availability database"),
                                    ("2", "Update node database"),
                                    ("3", "Update availability database")],
                           title="Monitoring menu", height=0, width=0)
        if code == d.OK:
            if tag == "1":
                code, tag = d.menu("Choose one of the following options:",
                                   choices=[("1", "Set monitoring daily"),
                                            ("2", "Set monitoring weekly"),
                                            ("3", "Set monitoring monthly"),
                                            ("4", "Remove all monitoring from cron")],
                                   title="Crontab menu")
                if code == d.OK:
                    if tag == "1":
                        addToCron(tag)
                    elif tag == "2":
                        addToCron(tag)
                    elif tag == "3":
                        addToCron(tag)
                    elif tag == "4":
                        removeCron()
                else:
                    continue
            elif tag == "2":
                if d.yesno("This is going to take around 20 minutes") == d.OK:
                    getAllNodes()
                else:
                    continue
            elif tag == "3":
                if d.yesno("This can take few minutes. Do you want to continue?") == d.OK:
                    if not verifySshCredentialsExist():
                        d.msgbox(
                            "Error! Your ssh credentials are not set. Please use 'Set credentials' option in main menu to set them.")
                        continue
                    else:
                        updateAvailabilityDatabaseParent()
                else:
                    continue
        else:
            return


# Acess servers part of GUI
def accessServersGui():
    while True:
        code, tag = d.menu("Choose one of the following options:",
                           choices=[("1", "Serach by DNS"),
                                    ("2", "Search by IP"),
                                    ("3", "Search by location"),
                                    ("4", "Access last server"),
                                    ("5", "Filtering options")],
                           title="ACCESS SERVERS")
        if code == d.OK:
            # Search by DNS
            if tag == "1":
                code, answer = d.inputbox("Search for:", title="Search")
                if code == d.OK:
                    searchNodes(OPTION_DNS, answer)
                else:
                    continue
            # Search by IP
            elif tag == "2":
                code, answer = d.inputbox("Search for:", title="Search")
                if code == d.OK:
                    searchNodes(OPTION_IP, answer)
                else:
                    continue
            # Search by location
            elif tag == "3":
                # Grepuje se default node
                searchNodes(OPTION_LOCATION)
            # Access last server
            elif tag == "4":
                lastServerMenu()
            # Filtering options
            elif tag == "5":
                filteringOptionsGui()

        else:
            return


if __name__ == "__main__":
    initInterface()
    exit(0)
