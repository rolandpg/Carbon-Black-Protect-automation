#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 14:11:10 2019

@author: patrick.roland
"""
from cbapi.protection import CbEnterpriseProtectionAPI, Policy
from cbapi.protection.models import Computer

POLICY_AND_NUM = []
with open('policyID.txt') as policies_and_numbers:
    for line in policies_and_numbers.readlines():
        POLICY_AND_NUM.append(line)
for item in range(len(POLICY_AND_NUM)):    
    POLICY_AND_NUM[item] =POLICY_AND_NUM[item].strip('[,],\n')

CLT_POLICIES = []
BNA_POLICIES = []
SLC_POLICIES = []

for item in range(len(POLICY_AND_NUM)):  
    if 'CLT' in POLICY_AND_NUM[item]:
        policy = POLICY_AND_NUM[item]
        CLT_POLICIES.append(policy)
    elif 'BNA' in POLICY_AND_NUM[item]:
        policy = POLICY_AND_NUM[item]
        BNA_POLICIES.append(policy)
    elif 'SLC' in POLICY_AND_NUM[item]:
        policy = POLICY_AND_NUM[item]
        SLC_POLICIES.append(policy)
        
#CLT_POLICIES.sort()
#BNA_POLICIES.sort()
#SLC_POLICIES.sort()

print('\n',"CLT:")
for policy in range(len(CLT_POLICIES)):
    print(CLT_POLICIES[policy])
print('\n',"BNA:")
for policy in range(len(BNA_POLICIES)):
    print(BNA_POLICIES[policy])
print('\n',"SLC:")
for policy in range(len(SLC_POLICIES)):
    print(SLC_POLICIES[policy])



CONSOLES = ["CLT", "BNA" "SLC"]
POLICES_IN_CONSOLE = []
PRODUCT_GROUP = ""
VisibilityPolicies = []

# Console Selection
console_choice = input("Select \"CLT\", \"BNA\", or \"SLC\":\n")
console_choice = console_choice.upper()
# for locale in CONSOLES:

#Query the CB server for  policy states    
cb = CbEnterpriseProtectionAPI(profile="{}".format(console_choice)) 
cb.credential_profile_name = console_choice
CB_Policy = cb.select(Policy) # returns all carbon black policies
CB_Policy = CB_Policy.sort("id") 
CB_Computers = cb.select(Computer) # return carbon black computers
CB_Computers = CB_Computers.sort("name") # 

Computers_in_vis_ins = 0
Computers_in_vis_ins = int(input("Enter policy ID of machine :"))
Desired_policy = 0
Desired_policy = int(input("What policy do you want to change to? :"))

for comp in CB_Computers:
    try:
        Pol_ID = int(comp.policyId)
        if Computers_in_vis_ins == Pol_ID:
            print("\n", comp.name, " ", comp.policyId, ", ", comp.policyName)
            newPolicy = Desired_policy
            print("Will now change to: {}".format(newPolicy))
            comp.policyId = Desired_policy 
            comp.save() #This will write to the CB console.
            print(comp.name, " ", comp.policyId, ", ", comp.policyName, "/n")
    except:
        print("Server Error")
        continue