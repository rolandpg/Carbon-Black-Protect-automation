# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 12:58:29 2019

@author: patrick.roland
"""

import ldap3
import threading as th
import time
 
dictFOREST = {
        'RZ':'rz.nucorsteel.local',
        'BR':'bar.nucorsteel.local',
        'SP':'sps.nucorsteel.local',
        'TH':'th.nucorsteel.local',
        'DJ':'dj.nucorsteel.local',
        'TG':'tg.nucorsteel.local',
        'HS':'hs.nucorsteel.local',
        'VC':'vc.nucorsteel.local',
        'HQ':'hq.nucorsteel.local',
        'FR':'nucorsteel.local'
        }

TARGETS = []

for Domain in dictFOREST:
    TARGETS.append(Domain)
    
print(TARGETS)

def CollectADComputers(Domain_target):
    server = ldap3.Server(
            '{}BNADCRW01.{}'.format(Domain_target,dictFOREST[Domain_target]),
            use_ssl=True,
            get_info=ldap3.ALL
            )
    conn = ldap3.Connection(
            server, auto_bind=True,
            user="",#LDAP username
            password="",#LDAP password
            authentication=ldap3.NTLM,
            check_names=True
            )
    if not conn.bind():
        print('error in bind', conn.result)
    #print(conn.extend.standard.who_am_i())
    #print(conn)
    ADBase = 'DC={},DC=nucorsteel,DC=local'.format(Domain_target)
    ADComps = ldap3.ObjectDef('computer', conn)
    print(ADBase)
    print('\n')
    ADQuery = '(sAMAccountType=805306369)'
    ADReader = ldap3.Reader(conn, ADComps, ADBase, ADQuery)
    ADReader.search()
    with open('C:\\Users\\patrick.roland\\Documents\\MachineList{}.csv'.format(Domain_target), 'w') as txtfile:
        for x in range(0, len(ADReader)):
            txtfile.write(str(ADReader[x].whenCreated) +','+ str(ADReader[x].cn)+','+str(ADReader[x].objectGUID)+','+str(ADReader[x].lastLogon)+','+str(ADReader[x].operatingSystem)+','+str(ADReader[x].whenCreated)+'\n' )
        '''
        print('Created : ' + str(ADReader[x].whenCreated))
        print('Name : ' + str(ADReader[x].cn))
        print('GUID : ' + str(ADReader[x].objectGUID))
        print('Last Logon : ' + str(ADReader[x].lastLogon))
        print('OS : ' + str(ADReader[x].operatingSystem))
        print('Created on : ' + str(ADReader[x].whenCreated))
        print('\n*************\n')
        #print('MacAddress : ' + str(getmac.get_mac_address(hostname=str(ADReader[x].dNSHostName), network_request=True)) + '\n*************\n')
        '''
        

class myThread (th.Thread):
   def __init__(self, threadID, name, counter):
      th.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.counter = counter
   def run(self):
      print ("Starting " + self.name)
      CollectADComputers(self.name)
      # Get lock to synchronize threads
      threadLock.acquire()
      print_time(self.name, self.counter, 3)
      # Free lock to release next thread
      threadLock.release()

def print_time(threadName, delay, counter):
   while counter:
      time.sleep(delay)
      print ("%s: %s" % (threadName, time.ctime(time.time())))
      counter -= 1

threadLock = th.Lock()
threads = []
Processes = []
Tnumber = 0
for tree in dictFOREST:
    Processes.append('Thr_' + tree)

print(Processes)    
# Create new threads
for tree in dictFOREST:
    TTNumber ='Thread' + str(Tnumber)
    Processes[Tnumber] = myThread(Tnumber, tree, Tnumber)
    print(Processes[Tnumber])
    Tnumber += 1
    

# Start new Threads
for number in range(0, Tnumber):
    Processes[number].start()


# Add threads to thread list
for number in range(0, Tnumber):
    threads.append(Processes[number])


# Wait for all threads to complete
for t in threads:
   t.join()
print ("Exiting Main Thread")


    
    
