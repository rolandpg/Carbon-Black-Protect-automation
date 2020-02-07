# -*- coding: utf-8 -*-
"""
Created on Wed Aug 21 14:31:24 2019

@author: patrick.roland
"""
import os
import csv
import time
from datetime import date
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--clt", help="selects the Charlotte console and checks publishers", action="store_true")
parser.add_argument("--slc", help="selects the Plano console and checks publishers", action="store_true")
parser.add_argument("--bna", help="selects the Franklin console and checks publishers", action="store_true")
args = parser.parse_args()


#from lib.helper import generateResultFilename
from cbapi.protection import CbEnterpriseProtectionAPI, FileCatalog, Publisher

PUBLISHERS = []

# need to specifiy console:
print("Today's date is : {}".format(date.today()))

if args.clt:
    locale = "CLT"
    print("welcome to CLT")
elif args.slc:
    locale = "SLC"
elif args.bna :
    locale = "BNA"
else:
    print("Which Console do you want to work with?... " )
    locale = input("CLT, SLC, BNA?\n")

cb = CbEnterpriseProtectionAPI(profile="{}".format(locale))


unack_unapp_pubs = cb.select(Publisher)
unack_unapp_pubs = unack_unapp_pubs.where('publisherState:1')
unack_unapp_pubs = unack_unapp_pubs.where('acknowledged:False')
unack_unapp_pubs = unack_unapp_pubs.where('signedFilesCount>0')
unack_unapp_pubs = unack_unapp_pubs.sort('name')

for pub in unack_unapp_pubs:
    #print(pub.name + ": " + str(pub.id) + "    Files:" + str(pub.signedFilesCount))
    PUBLISHERS.append(pub.name)    

print("{} unacknowleged publishers in this console".format(len(unack_unapp_pubs)))

def WritePubsHashes():
    with open('unackpubs{}{}.csv'.format(locale,date.today()), mode='w', newline ='\n') as unackpubs:
        for pubnum in range(0,len(PUBLISHERS)):
            FilesInPub = cb.select(FileCatalog)
            FilesInPub = FilesInPub.where('publisher:{}'.format(PUBLISHERS[pubnum]))

            for file in FilesInPub:
                unackpubs.write(file.sha256 + '\n')
    print("wrote 'unackpubs{}{}.csv' to machine".format(locale,date.today()))            
def ReadResultsCSV(filedate):
    with open('check-results_unackpubs{}{}.csv'.format(locale,filedate), mode='r') as results:
        csv_reader = csv.reader(results, delimiter=';')
        line_count = 0
        for row in csv_reader:
            
            if line_count == 0:
                print("Reading CSV file ...")
                line_count += 1
               
            else:
                if row[1] == "suspicious":
                    suspect_file = cb.select(FileCatalog)
                    suspect_file = suspect_file.where('sha256:{}'.format(row[0]))
                    for file in suspect_file:
                        if file.publisher.acknowledged and file.publisher.publisherState == 1:
                            pass
                        else:
                            try:
                                file.publisher.acknowledged = True
                                file.publisher.publisherState = 1
                                file.publisher.description = "identified as suspicious via munin."
                                file.publisher.save()
                                time.sleep(3)
                            except:
                                print("waiting on server...")
                                time.sleep(5)
                                file.publisher.acknowledged = True
                                file.publisher.publisherState = 1
                                file.publisher.description = "identified as suspicious via munin."
                                file.publisher.save()
                            if file.publisher.acknowledged and file.publisher.publisherState == 1:    
                                print("{} Suspicious file identified".format(file.publisher.name))
                            else:
                                print("write Failure")
                    line_count += 1
                   
                elif row[1] == "malicious":
                    suspect_file = cb.select(FileCatalog)
                    suspect_file = suspect_file.where('sha256:{}'.format(row[0]))
                    for file in suspect_file:
                        if file.publisher.acknowledged and file.publisher.publisherState == 1:
                            pass
                        else:
                            try:
                                file.publisher.acknowledged = True
                                file.publisher.publisherState = 1
                                file.publisher.description = "identified as malicious via munin."
                                file.publisher.save()
                                time.sleep(3)
                            except:
                                print("waiting on server...")
                                time.sleep(5)
                                file.publisher.acknowledged = True
                                file.publisher.publisherState = 1
                                file.publisher.description = "identified as malicious via munin."
                                file.publisher.save()
                            if file.publisher.acknowledged and file.publisher.publisherState == 1: 
                                print("{} Malicious file detected.".format(file.publisher.name))
                            else:
                                print ("write Failure")
                    line_count += 1
                
def UnknownfilesCSV(filedate):
    with open('check-results_unackpubs{}{}.csv'.format(locale,filedate), mode='r') as results:
        csv_reader = csv.reader(results, delimiter=';')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print("Reading CSV file")
                line_count += 1
            else:
                if row[1] == "unknown":
                    suspect_file = cb.select(FileCatalog)
                    suspect_file = suspect_file.where('sha256:{}'.format(row[0]))
                    for file in suspect_file:
                        if file.publisher.acknowledged and file.publisher.publisherState == 1:
                            pass
                        else:
                            try:
                                file.publisher.acknowledged = True
                                file.publisher.publisherState = 1
                                file.publisher.description = "Munin could not categorize this publisher."
                                file.publisher.save()
                                time.sleep(3)
                            except:
                                print("waiting on server...")
                                time.sleep(5)
                                file.publisher.acknowledged = True
                                file.publisher.publisherState = 1
                                file.publisher.description = "Munin could not categorize this publisher."
                                file.publisher.save()
                            if file.publisher.acknowledged and file.publisher.publisherState == 1: 
                                print("{} unable to determine file.".format(file.publisher.name))
                            else:
                                print ("write Failure")
                    line_count += 1
                    
def CleanResultsCSV(filedate):
    with open('check-results_unackpubs{}{}.csv'.format(locale,filedate), mode='r') as results:
        csv_reader = csv.reader(results, delimiter=';')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print("Reading CSV file")
                line_count += 1
            else:
                if row[1] == "clean":
                    suspect_file = cb.select(FileCatalog)
                    suspect_file = suspect_file.where('sha256:{}'.format(row[0]))
                    for file in suspect_file:
                        if file.publisher.acknowledged:
                            pass
                        else:
                            try:
                                file.publisher.publisherState = 2
                                file.publisher.acknowledged = True
                                file.publisher.save()
                                time.sleep(3)
                            except:
                                print("waiting on server...")
                                time.sleep(5)
                                file.publisher.publisherState = 2
                                file.publisher.acknowledged = True
                                file.publisher.save()
                            if file.publisher.publisherState == 2:
                                print("{} is approved and state is {}".format(file.publisher.name, file.publisher.publisherState))
                            
                line_count += 1

if args.clt:
    MODE = "1"
elif args.bna:
    MODE = "1"
elif args.slc:
    MODE = "1"
else:                
    MODE = input("What would you like to do?\n Write Publisher file and process with Munin: 1\n Process a results file: 2\n Quit: 3\n")
    
if MODE == "1":
    WritePubsHashes()
    print("begining munin")
    command = "python c:\\Users\\patrick.roland\\munin\\munin.py -f unackpubs{}{}.csv".format(locale, date.today())
    print(command)
    os.system(command)
    dateoffile = date.today()
    ReadResultsCSV(dateoffile)
    CleanResultsCSV(dateoffile)
    UnknownfilesCSV(dateoffile)
    
elif MODE == "2":
    filedate = input("input file's date in correct format. 'YYYY-MM-DD'\n")
    ReadResultsCSV(filedate)
    CleanResultsCSV(filedate)
    UnknownfilesCSV(filedate)
    
elif MODE == "3":
    pass