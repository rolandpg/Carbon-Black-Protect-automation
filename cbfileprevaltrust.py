# -*- coding: utf-8 -*-
"""
Created on Fri Aug 23 08:47:29 2019

@author: patrick.roland
"""
#import time
from cbapi.protection import CbEnterpriseProtectionAPI, FileCatalog, FileRule
#import threading
from multiprocessing import Process, Pool
import os

def f(x):
    return x*x



locale = ["CLT", "BNA", "SLC"]



def info(title):
    print(title)
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())

def fileprevapp(loc):
    info('Console: {}'.format(loc))
    cb = CbEnterpriseProtectionAPI(profile="{}".format(loc))
    cb2 = CbEnterpriseProtectionAPI(profile="{}".format(loc))
    approvalfiles = cb.select(FileRule)
    approvalfiles = approvalfiles.where('fileState:1')
    for filerule in approvalfiles:
        filecat = cb2.select(FileCatalog).where('id:{}'.format(filerule.fileCatalogId))
        filecat = filecat.where('trust>7')
        filecat = filecat.where('prevalence>10')
        filecat = filecat.where('threat:0')
        for file in filecat:
            if filerule.fileState == 2:
                pass
            else:
                #print("approving: {}".format(file.fileName))
                filerule.fileState = 2
                filerule.save()
                print("{} has changed state to {}".format(file.fileName, filerule.fileState))

def GKY_appoval():
    cba = CbEnterpriseProtectionAPI(profile="BNA")
    gkyfiles = cba.select(FileCatalog)
    gkyfiles = gkyfiles.where('fileState:1')
    gkyfiles = gkyfiles.where('publisherOrCompany:Gallatin Steel Company')
    print(len(gkyfiles))
    for files in gkyfiles:
        if files.fileState == 2:
            pass
        else:
            print("approving: {}".format(files.fileName))
            files.fileState = 2
            files.save()
'''
for console in locale:
    th = threading.Thread(target=fileprevapp, args=(console,))
    th.start
'''
if __name__ == '__main__':
    p = Pool(5)
    p.map(fileprevapp, ['CLT','BNA','SLC'])
'''
if __name__ == '__main__':
    info('main line')
    p = Process(target=fileprevapp, args=('CLT','BNA','SLC'))
    p2 = Process(target=GKY_appoval)
    p.start()
    p2.start
    print("starting process")
    p.join()
    p2.join
print("joining")
print("complete")
'''