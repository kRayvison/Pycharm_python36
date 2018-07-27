#!/usr/bin/env python
#encoding:utf-8
# -*- coding: utf-8 -*-

import threading
import sqlite3 as HQL

class HoudiniThread():

    def __init__(self):        
        pass

    @classmethod
    def CreatThread(cls,functions={}):
        thread_creat=[]
        if len(functions.keys()):
            keys = functions.keys()
        for key in keys:
            thread_creat.append(MyThread(functions[key][0],functions[key][1],key))

        return thread_creat

    @classmethod
    def StartThread(cls,threads=[]):
        dbs = None#cls.CreatDBTable()
        for thr in threads:
            thr.start()
        return [threads,dbs]

    @classmethod
    def JoinThread(cls,elm=[]):
        threads = elm[0]
        dbs = elm[1]
        runs = 1
        i = 1
        for thr in threads:
            # if i==1:
            #     cls.InsertDBTable(dbs,[runs,thr.name])
            # else:
            #     cls.UpdateDBTable(dbs,[runs,thr.name])
            
            thr.join()
            print("[HTS] insert thread end: %s"%thr.name)
            i +=1
            if i>=len(threads):
                runs = 0

    @classmethod
    def CreatDBTable(cls,dbfile=''):
        if dbfile=='':
            hqlib = HQL.connect(":memory:")
            cur =hqlib.cursor()
            cur.execute('CREATE TABLE thr (ID INT PRIMARY KEY  NOT NULL,NAME TEXT  NOT NULL,STATE INT NOT NULL);')
            hqlib.commit()
            return hqlib

    @classmethod
    def InsertDBTable(cls,dbs='',val=[]):
        cur =dbs.cursor()
        cur.execute("INSERT INTO thr (ID,STATE,NAME) VALUES (1,%d, '%s')"%(val[0],val[1]))
        dbs.commit()

    @classmethod
    def SelectDBTable(cls,dbs=''):
        cur =dbs.cursor()
        cursor = cur.execute("SELECT STATE, NAME from thr")
        dbs.commit()
        return cursor

    @classmethod
    def UpdateDBTable(cls,dbs='',val=[]):
        cur =dbs.cursor()
        cur.execute("UPDATE thr set STATE = %d where ID=1"%val[0])
        cur.execute("UPDATE thr set NAME = '%s' where ID=1"%val[1])
        dbs.commit()
    
    @classmethod
    def CloseDB(cls,dbs=''):
        dbs.close()
        

class MyThread(threading.Thread):
    def __init__(self,func,args,name=''):
        super(MyThread,self).__init__()
        self.func = func
        self.args = args
        self.name = name

    def run(self):
        apply(self.func,self.args)