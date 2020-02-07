from cbapi.protection import CbEnterpriseProtectionAPI, Policy
cb = CbEnterpriseProtectionAPI()
query = cb.select(Policy) # returns a Query object in this case carbon black policies

NumHePol = 0
NumHeroPol = 0
NumInsPol = 0
NumVisPol = 0
#list all policies in the console
for poli in query: 
    print(str(poli.name) + ": " + str(poli.totalComputers))
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
NumInsPol = NumInsPol - 2        

print("\nIn the Charlotte Console there are:\n")
print("\t" + str(NumInsPol) + " in the \"Install\" policy")
print("\t" + str(NumVisPol) + " in the \"Visibility\" policy")
print("\t" + str(NumHeroPol) + " in the \"H.E. Report only\" policy")
print("\t" + str(NumHePol) + " in the \"High Enforcement\" policy")
