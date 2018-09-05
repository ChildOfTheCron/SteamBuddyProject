#!/usr/bin/python3.5

import sys
from subprocess import call

containerRunning = call('docker inspect -f {{.State.Running}} postdbcont', shell=True)

print(containerRunning)

if (containerRunning == 0):
    print(containerRunning)
    print("Debug: Container running!\n")
    call('docker stop postdbcont', shell=True)
    call('docker container rm postdbcont', shell=True)
else:
    print("Container not running\n")

print ("Debug: copying new SQL content. \n")
call('cp appidlist.sql /root/SysAdminStuff/myDockerFileMods/appidlist.sql', shell=True)

print ("Building new Database Container Image \n")
call('docker image build --tag pgdbtest /root/SysAdminStuff/myDockerFileMods/', shell=True)

print ("Starting new database container. \n")
call('docker run --restart unless-stopped --net steamnetwork --ip 172.18.0.3 --name postdbcont -di pgdbtest', shell=True)

