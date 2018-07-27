#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: kaname
# QQ: 1394041054

import os
import subprocess

from CommonUtil import RBCommon as CLASS_COMMON_UTIL
from RenderC4d import *
from RenderBase import *


class RBC4dUtil(object):

    @classmethod
    def kill_c4d(self,parent_id,my_log=None):
        print('parent_id='+str(parent_id))
        cmd_str='wmic process where name="CINEMA 4D 64 Bit.exe" get Caption,ParentProcessId,ProcessId'
        print(cmd_str)
        cmdp=subprocess.Popen(cmd_str,shell = True,stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
        while True:
            buff = cmdp.stdout.readline().strip()
            if buff == '' and cmdp.poll() != None:
                break
            if buff!=None and buff!='' :
                
                CLASS_COMMON_UTIL.log_print(my_log,'c4d process info...')
                CLASS_COMMON_UTIL.log_print(my_log,buff)
                    
                try:
                    buffArr=buff.split()
                    print(str(buffArr))
                    if int(buffArr[1])==parent_id:
                        print('kill...'+buff)
                        os.system("taskkill /f /pid %s" % (buffArr[2]))
                except  Exception as e:
                    CLASS_COMMON_UTIL.log_print(my_log,'taskkill CINEMA 4D 64 Bit.exe exeception')
                    CLASS_COMMON_UTIL.log_print(my_log,e)
                
        try:
            os.system('taskkill /F /IM CINEMA 4D 64 Bit.exe /T')
        except  Exception as e:
            CLASS_COMMON_UTIL.log_print(my_log,'taskkill CINEMA 4D 64 Bit.exe exeception')
            CLASS_COMMON_UTIL.log_print(my_log,e)
        CLASS_COMMON_UTIL.log_print(my_log,'c4dKill...end...\n')
        

    @classmethod
    def c4d_cmd_callback(self,my_popen,my_log):

        while my_popen.poll()==None:
            render_info = my_popen.stdout.readline().strip()
            if render_info == "":
                # self.G_DEBUG_LOG.info(render_info)
                # r_err = render_info
                continue
            CLASS_COMMON_UTIL.log_print(my_log,render_info)
