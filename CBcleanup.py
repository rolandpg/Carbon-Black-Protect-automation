# -*- coding: utf-8 -*-
"""
Created on Mon Oct  7 10:56:29 2019

@author: patrick.roland
"""
from cbapi.protection import CbEnterpriseProtectionAPI
from cbapi.protection.models import Computer
import ldap3
import datetime
import sqlalchemy as sqla

server = ldap3.Server(
        'RZBNADCRW01.rz.nucorsteel.local',
        use_ssl=True,
        get_info=ldap3.ALL
        )
conn = ldap3.Connection(
        server, auto_bind=True,
        user="", #LDAP username
        password="" #LDAP Password
        authentication=ldap3.NTLM,
        check_names=True
        )
if not conn.bind():
    print('error in bind', conn.result)
print(conn.extend.standard.who_am_i())
print(conn)
'''
Base = sqla.ext.declarative.declarative_base

class NucorComp(Base):
    __tablename__ = 'NSMACHINES'
    
    Deleted = sqla.Column(sqla.Boolean)
    Description = sqla.Column(sqla.String)
    DistinguishedName = sqla.Column(sqla.String)
    DNSHostName = sqla.Column(sqla.String)
    Enabled = sqla.Column(sqla.Boolean)
    LastLogonDat = sqla.Column(sqla.DateTime)
    Name = sqla.Column(sqla.String)
    ObjectClass = sqla.Column(sqla.String)
    ObjectGUID = sqla.Column(sqla.GUID, primary_key=True)
    OperatingSystem = sqla.Column(sqla.String)
    SamAccountName = sqla.Column(sqla.String)
    SID = sqla.Column(sqla.Varchar)
    UserPrincipalName = sqla.Column(sqla.String)
    
'''
#result = conn.search('o=test','(cn=test-ldif*)', , attributes = ['sn', 'objectClass'])
r = ldap3.Reader(conn,ldap3.ObjectDef('computer', conn), query='(sAMAccountType=805306369)',base='DC=nucorsteel,DC=local' )
r.search()
print(r)
def CheckComps(console):
    cb = CbEnterpriseProtectionAPI(profile="{}".format(console))
    compList = cb.select(Computer).where('daysOffline>30')
  
    for comps in compList:
       # if 'SPS\\' in comps.name:
        #    fixed_name = comps.name[4:]
        #elif 'S\\' in comps.name:
         #   fixed_name = comps.name[2:]
        if '\\' in comps.name:
            start = (comps.name.find('\\') + 1)
            fixed_name = comps.name[start:]
            print(fixed_name)
        print(comps.name + '\t' + comps.osShortName + '\t' + comps.policyName + " Has been Disconnected:{} Day(s) ".format( str(comps.daysOffline)))
        conn.search('DC=*,DC=nucorsteel,DC=local', '(&(objectClass=computer)(cn={}))'.format(fixed_name), search_scope=ldap3.SUBTREE, attributes=['cn', 'ObjectClass', 'ObjectGUID', 'lastLogonTimestamp', 'isDeleted', 'lastLogon', 'lastLogoff','networkaddress' ])
        for entry in conn.entries:
            print(entry)
            #entry.entry_attributes.lastLogonTimestamp - datetime.


#ldap3.ObjectDef('computer', conn)