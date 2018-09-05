#!/usr/bin/python3.5
# -*- coding: utf-8 -*-
 
import sys
import requests
import time
import datetime
import json

#readlist = open("appidlist.sql", "r")
#filecontents = readlist()
#readlist.close()

req    = requests.get('https://store.steampowered.com/api/appdetails/?appids=730&cc=EE&l=english&v=1')

print(req.status_code)
#print("Probed on: ", datetime.datetime.now().strftime("%d/%m/%y::%H-%M-%S"))

#730
firstVal = req.json()
try:
    subDict = firstVal['730']
    secondVal = subDict['data']
    thirdVal = secondVal['package_groups']
    fourthVal = thirdVal[0]
    fithVal = fourthVal['subs']
    sixVal = fithVal[0]
    seventhVal = sixVal['percent_savings_text']

    print(seventhVal)
except:
    print("Unknown json config \n")

#try:
#except ValueError:
#    print("Unknown json configuration \n")

#for val in fithVal:
#    print("pass")
#    print(val['percent_savings_text'])

#Put this in to see nice json things
#print(json.dumps(fithVal, sort_keys=True, indent=4))

#file = open("testlist.log", "w")
#file.write("INSERT INTO appIdTable ( appId, productName ) VALUES \n")
#for key in thirdVal:
#    file.write("(" + str(key) + ")" + "," + "\n")
#file.close()    
