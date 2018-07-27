#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: kaname
# QQ: 1394041054

import logging
import os
import sys
import subprocess
import string
import time
import shutil
import threading
import time

reload(sys)
sys.setdefaultencoding('utf-8')

class C4dThread(threading.Thread):

    def __init__(self,interval,taskId,jobName,nodeName,workTask,grabOutput,logObj):  
        threading.Thread.__init__(self)
        self.interval = interval  
        self.thread_stop = False
        self.RENDER_LOG=logObj
        self.TASK_ID=taskId
        self.JOB_NAME=jobName
        self.NODE_NAME=nodeName
        self.WORK_TASK=workTask
    
    def run(self): 
        time.sleep(200)
        
    def stop(self):  
        self.thread_stop = True
        self.RENDER_LOG.info('[Thread].stop...')
        try:
            print 'end'
        except Exception, e:
            print '[Thread.err]'
            print e