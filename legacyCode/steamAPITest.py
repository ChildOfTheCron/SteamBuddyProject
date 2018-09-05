#!/usr/bin/python3.5
# -*- coding: utf-8 -*-
 
import sys
import requests
import time
import datetime
import threading
import time

#sqlContentTest = []
#exitFlag = 0
#hackyCount = 0

class myThread (threading.Thread):
   #def __init__(self, threadID, name, val):
   def __init__(self, val):
      threading.Thread.__init__(self)
      #self.threadID = threadID
      #self.name = name
      self.val = val
   def run(self):
      #print ("Starting " + self.name)
      getDisc(self.val)
      #print ("Exiting " + self.name)

def threadChecker():

    time.sleep(5)
    #print("Checking threads \n")
    if (threading.active_count() == 1):
        print("Probed run end on: ", datetime.datetime.now().strftime("%d/%m/%y::%H-%M-%S"))
    else:
        threadChecker()

def getAppIdList():
   
    req4 = requests.get('http://api.steampowered.com/ISteamApps/GetAppList/v2')
    
    firstVal = req4.json()
    subDict = firstVal['applist']
    secondVal = subDict['apps']

    return secondVal

def lookUpDiscount(sndVal):

    thread = myThread(sndVal)
    thread.start()
    #thread.join()

def getDisc(val):

    s = requests.Session() # Remove this??

    jsonAppID = val['appid']
    appreq    = s.get('https://store.steampowered.com/api/appdetails/?appids=' + str(val['appid']) + '&cc=EE&l=english&v=1')
    print(appreq.status_code)
    appfirstVal = appreq.json()

    tmpdisc = '0%'

    try:
        appsubDict = appfirstVal[str(val['appid'])]
        appsecondVal = appsubDict['data']
        appthirdVal = appsecondVal['package_groups']
        appfourthVal = appthirdVal[0]
        appfithVal = appfourthVal['subs']
        appsixVal = appfithVal[0]
        appseventhVal = appsixVal['percent_savings_text']
        tmpdisc = appseventhVal
        print(appseventhVal)
        #break <-- Debug stuff, uncomment this to jump out when you hit the first discount
    except:
        print("Unknown json found, will set to 0%")

    if (tmpdisc == ""):
        tmpdisc = "0%"

    sqlContentTest.append([val['appid'], val['name'], tmpdisc])

# Grab a list of all steam app id's using the web API, not sure if this is returning them all
# but I got no control over that
#req4    = requests.get('http://api.steampowered.com/ISteamApps/GetAppList/v2')

#Note start time so I can see how long this takes
print("Probed run start on: ", datetime.datetime.now().strftime("%d/%m/%y::%H-%M-%S"))

appList = getAppIdList()

sqlContentTest = []
exitFlag = 0
hackyCount = 0

for val in appList:
    if (hackyCount < 100): 
        lookUpDiscount(val)
        hackyCount = hackyCount + 1
    else:
        time.sleep(600)
        print("system up")
        hackyCount = hackyCount - 100 
        print(threading.active_count())
        lookUpDiscount(val)

#time.sleep(1)
#print(threading.activeCount())
threadChecker()

#time.sleep(10)
#for thread in threading.enumerate(): print(thread.name)
#for thread in threading.enumerate():
#    if thread.isAlive(): 
#        thread.join()
#if (threading.enumerate() <= 1)
#    print("Probed run end on: ", datetime.datetime.now().strftime("%d/%m/%y::%H-%M-%S"))    

file = open("appidlist.sql", "w")
file.write("INSERT INTO appIdTable ( appId, productName, discount ) VALUES \n")
for key in sqlContentTest:
    # Debug stuff
    #print("Key:" + str(key['appid'])  + "\n")
    #print("Name:" + key['name'] + "\n")
    
    # Don't print a comma on the last line of the SQL
    if set(key) == set(sqlContentTest[-1]):
        file.write("(" + str(key[0]) + "," + "'" + key[1] + "'" + "," + "'" + key[2] + "'" + ")" + "\n")
    else:    
        file.write("(" + str(key[0]) + "," + "'" + key[1] + "'" + "," + "'" + key[2] + "'" + ")" + "," + "\n")
file.close()    
