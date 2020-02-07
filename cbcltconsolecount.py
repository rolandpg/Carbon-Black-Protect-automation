from cbapi.protection import CbEnterpriseProtectionAPI, Policy
#cb = CbEnterpriseProtectionAPI()
Consoles = ["CLT", "BNA", "SLC"]

TotalInVisPol = 0
TotalInInsPol = 0
TotalInHeroPol = 0
TotalInHEPol = 0

for x in Consoles:
    cb = CbEnterpriseProtectionAPI(profile="{}".format(x))
    cb.credential_profile_name = x
    query = cb.select(Policy) # returns a Query object in this case carbon black policies

    NumHePol = 0
    NumHeroPol = 0
    NumInsPol = 0
    NumVisPol = 0
    #list all policies in the console
    for poli in query: 
        #print(str(poli.name) + ": " + str(poli.totalComputers))
        if "Visibility" in str(poli.name):
            NumVisPol = NumVisPol + poli.totalComputers
        elif "Install" in str(poli.name):
            NumInsPol = NumInsPol + poli.totalComputers
        elif "HE Report Only" in str(poli.name):
            NumHeroPol = NumHeroPol + poli.totalComputers
        elif "Workstations" in str(poli.name) or "Servers" in str(poli.name):
            if "HE Report Only" in str(poli.name):
                continue
            NumHePol = NumHePol + poli.totalComputers

    # -2 forSccm test Installations
    if x == "CLT": 
        NumInsPol = NumInsPol - 2        
    
    TotalInVisPol = TotalInVisPol + NumVisPol
    TotalInInsPol = TotalInInsPol + NumInsPol
    TotalInHeroPol = TotalInHeroPol + NumHeroPol
    TotalInHEPol = TotalInHEPol + NumHePol
    
    print("\nIn the {} Console there are:\n".format(x))
    print("\t" + str(NumInsPol) + " in the \"Install\" policy")
    print("\t" + str(NumVisPol) + " in the \"Visibility\" policy")
    print("\t" + str(NumHeroPol) + " in the \"H.E. Report only\" policy")
    print("\t" + str(NumHePol) + " in the \"High Enforcement\" policy")
    
print("\nConsole totals: \n")
print("\t" + str(TotalInInsPol) + " in the \"Install\" policy")
print("\t" + str(TotalInVisPol) + " in the \"Visibility\" policy")
print("\t" + str(TotalInHeroPol) + " in the \"H.E. Report only\" policy")
print("\t" + str(TotalInHEPol) + " in the \"High Enforcement\" policy")