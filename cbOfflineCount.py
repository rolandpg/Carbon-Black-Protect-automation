# -*- coding: utf-8 -*-
"""
Created on Tue Sep 24 09:24:26 2019

@author: patrick.roland
"""
#import csv
from multiprocessing import Pool
from datetime import date
from cbapi.protection import CbEnterpriseProtectionAPI, Computer, Policy
CONSOLES = ["CLT", "BNA", "SLC"]



def greaterThan30(locale):
    cb = CbEnterpriseProtectionAPI(profile="{}".format(locale))
    cb.credential_profile_name = locale
    CbPolicies = cb.select(Policy) # returns a Query object in this case carbon black policies
    CbPolicies = CbPolicies.sort("name")
    
    with open('Offline30days{}{}.csv'.format(locale,date.today()), mode='w', newline ='\n') as offline30days:
        offline30days.write("CompID,Name,DaysOffline,DateCreated\n")
        for policy in CbPolicies:
            query = cb.select(Computer)
            query = query.where("policyName:{}".format(policy.name))
            query = query.where("daysOffline>29")
            query = query.sort("name")
            print("Id\,Name\,DaysOffline\,DateCreated\n".format(policy.name, len(query)))
            for comps in query:
                print("\t{}.....OFFLINE {} Day(s)".format(comps.name, comps.daysOffline))
                offline30days.write("{},{},{},{}\n".format(comps.id, comps.name, comps.daysOffline, comps.dateCreated))
if __name__=='__main__':
    p = Pool(5)
    p.map(greaterThan30, ["CLT", "BNA", "SLC"])