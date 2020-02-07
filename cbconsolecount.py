#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 13:38:10 2019

@author: patrick.roland
"""
from cbapi.protection import CbEnterpriseProtectionAPI, Policy
from openpyxl import Workbook
from openpyxl.worksheet.table import Table, TableStyleInfo
#cb = CbEnterpriseProtectionAPI()

CONSOLES = ["CLT", "BNA", "SLC"]
POLICES_IN_CONSOLE = []
PRODUCT_GROUP = ""
TOTAL_VISIBILITY = 0
TOTAL_INSTALL = 0
TOTAL_HERO = 0
TOTAL_HIGH_ENFC = 0
VIS_POL = []
INS_POL = []
HERO_POL = []

WB = Workbook()
WS = WB.active

DATA = [
    ['Install', 10000, 5000, 8000, 6000],
    ['Visibility', 2000, 3000, 4000, 5000],
    ['HERO', 6000, 6000, 6500, 6000],
    ['High Enforcement', 500, 300, 200, 700],
]


    
def table_write():# writing to totals to data
    """
    interates through data to stage infomation to be written to table.
    """
    if locale == "CLT":
        print("\nWriting CLT table...")
        DATA[0][1] = NumInsPol
        DATA[1][1] = NumVisPol
        DATA[2][1] = NumHeroPol
        DATA[3][1] = NumHePol
        print("Done.")
    if locale == "BNA":
        print("\nWriting BNA table...")
        DATA[0][2] = NumInsPol
        DATA[1][2] = NumVisPol
        DATA[2][2] = NumHeroPol
        DATA[3][2] = NumHePol
        print("Done.")
    if locale == "SLC":
        print("\nWriting SLC table...")
        DATA[0][3] = NumInsPol
        DATA[1][3] = NumVisPol
        DATA[2][3] = NumHeroPol
        DATA[3][3] = NumHePol
        print("Done.")
        
for locale in CONSOLES:
    cb = CbEnterpriseProtectionAPI(profile="{}".format(locale))
    cb.credential_profile_name = locale
    query = cb.select(Policy) # returns a Query object in this case carbon black policies
    query = query.sort("name")
    NumHePol = 0
    NumHeroPol = 0
    NumInsPol = 0
    NumVisPol = 0
    # list all policies in the console
    for poli in query:
        POLICES_IN_CONSOLE.append([poli.id, poli.name, poli.totalComputers])
        if poli.enforcementLevel == 60:
            NumVisPol = NumVisPol + poli.totalComputers
            VIS_POL.append([poli.id, poli.name, poli.totalComputers])
        elif poli.enforcementLevel == 80:
            NumInsPol = NumInsPol + poli.totalComputers
            INS_POL.append([poli.id, poli.name, poli.totalComputers])
        elif "HE Report Only" in str(poli.name):
            NumHeroPol = NumHeroPol + poli.totalComputers
            HERO_POL.append([poli.id, poli.name, poli.totalComputers])
        elif poli.enforcementLevel == 20:
            if "HE Report Only" in str(poli.name):
                continue
            else:
                NumHePol = NumHePol + poli.totalComputers

    # -2 forSccm test Installations
    if locale == "CLT":
        NumInsPol = NumInsPol - 2
    # Total Number of machines in given console
    NumInstalledMac = NumHeroPol + NumHePol + NumInsPol + NumVisPol
    # Total Number in all consoles
    TOTAL_VISIBILITY = TOTAL_VISIBILITY + NumVisPol
    TOTAL_INSTALL = TOTAL_INSTALL + NumInsPol
    TOTAL_HERO = TOTAL_HERO + NumHeroPol
    TOTAL_HIGH_ENFC = TOTAL_HIGH_ENFC + NumHePol
    # write all totals to "data" to be written to table later in code
    table_write()
    # command line outputs for tool
    print("\nIn the {} Console there are:\n".format(locale))
    print("\t" + str(NumInsPol) + " in the \"Install\" policy")
    print("\t" + str(NumVisPol) + " in the \"Visibility\" policy")
    print("\t" + str(NumHeroPol) + " in the \"H.E. Report only\" policy")
    print("\t" + str(NumHePol) + " in the \"High Enforcement\" policy")
    print("\nTOTAL in {} Console: {}\n".format(locale, NumInstalledMac))


print("\nConsole totals: \n")
print("\t" + str(TOTAL_INSTALL) + " in the \"Install\" policy")
print("\t" + str(TOTAL_VISIBILITY) + " in the \"Visibility\" policy")
print("\t" + str(TOTAL_HERO) + " in the \"H.E. Report only\" policy")
print("\t" + str(TOTAL_HIGH_ENFC) + " in the \"High Enforcement\" policy")

DATA[0][4] = TOTAL_INSTALL
DATA[1][4] = TOTAL_VISIBILITY
DATA[2][4] = TOTAL_HERO
DATA[3][4] = TOTAL_HIGH_ENFC

MACHINE_TOTAL = TOTAL_HIGH_ENFC + TOTAL_HERO + TOTAL_INSTALL + TOTAL_VISIBILITY
print("\nCONSOLE TOTAL INSTALLED: {} ".format(MACHINE_TOTAL))

# add column headings. NB. these must be strings
WS.append(["Policy mode", "CLT", "BNA", "SLC", "TOTAL"])
# write "data" to table
for row in DATA:
    WS.append(row)

CONSOLE_TOTAL_TABLE = Table(displayName="Console_Totals", ref="A1:E5")

# Add a default style with striped rows and banded columns
STYLE = TableStyleInfo(name="TableStyleMedium9", showFirstColumn=False,
                       showLastColumn=False, showRowStripes=True, showColumnStripes=True)
CONSOLE_TOTAL_TABLE.tableStyleInfo = STYLE

WS.add_table(CONSOLE_TOTAL_TABLE)
WB.save("CBpolicyTotals.xlsx")

def comp_in_policy(p_group, div):
    """
    sort through policies to show wanted infomation.
    """
    for policy in POLICES_IN_CONSOLE:
        if p_group in policy[1]:
            if div in policy[1]:
                print(policy)
            elif div == "ALL":
                print(policy)
        elif p_group == "QUIT":
            break
        elif p_group == "ALL":
            print(policy)

def find_policy_status():
    current_mode = input("Search for Install (INS), Visibility (VIS) or High Enforcement Report only (HERO):\n")
    current_mode = current_mode.upper()
    if current_mode == "INS":
        for policy in INS_POL:
            if policy[2] > 0:
                print(policy)
    elif current_mode == "VIS":
        for policy in VIS_POL:
            if policy[2] > 0:
                print(policy)
    elif current_mode == "HERO":
        for policy in HERO_POL:
            if policy[2] > 0:
                print(policy)
    

while PRODUCT_GROUP != "QUIT":
    print("\nAt any time type \'search\' to identify policy numbers...")
    PRODUCT_GROUP = input("Enter product group you wish to check or enter \"quit\": ")
    PRODUCT_GROUP = PRODUCT_GROUP.upper()
    if PRODUCT_GROUP == "QUIT":
        break
    elif PRODUCT_GROUP == "SEARCH":
        find_policy_status()
    DIVISION = input("Enter Division you want to check or \'all\'.: ")
    DIVISION = DIVISION.upper()
    if DIVISION == "QUIT":
        break
    elif PRODUCT_GROUP == "SEARCH":
        find_policy_status()
    comp_in_policy(PRODUCT_GROUP, DIVISION)
