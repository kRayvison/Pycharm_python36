#!/usr/bin/env python
#encoding:utf-8
# -*- coding: utf-8 -*-
import os,sys
import time
from RenderBase import RenderBase
from CommonUtil import RBCommon as CLASS_COMMON_UTIL
# from imp import reload

# reload(sys)
# sys.setdefaultencoding('utf-8')
class Houdini(RenderBase):
    def __init__(self,**paramDict):
        print("Houdini class")
        RenderBase.__init__(self,**paramDict)
        self.format_log('Houdini.init','start')
        self.G_RENDER_OPTIONS = {"render_rop":self.G_CG_OPTION} if self.G_CG_OPTION !='' else {}

        dir_list=[]
        CLASS_COMMON_UTIL.make_dirs(dir_list)
        self.Updata()
        self.format_log('done','end')


    def LogsCreat(self,info='',render=False,debug=True):
        if render and debug:
            self.G_RENDER_LOG.info(str(info))
            self.G_DEBUG_LOG.info(str(info))
        elif render and not debug:
            self.G_RENDER_LOG.info(str(info))
        else:
            self.G_DEBUG_LOG.info(str(info))

    def Updata(self):
        print(self.G_INPUT_CG_FILE)
        if 'mnt_map' in self.G_TASK_JSON_DICT:
            map_dict = self.G_TASK_JSON_DICT['mnt_map']
            for elm in map_dict:
                if map_dict[elm].replace("/","\\") in self.G_INPUT_CG_FILE:
                    self.G_INPUT_CG_FILE = self.G_INPUT_CG_FILE.replace(map_dict[elm].replace("/","\\"),elm)
                    print(self.G_INPUT_CG_FILE)

    def CheckNetuse(self,cunt=0):
        check_result = False
        if cunt<5:
            if self.G_RENDER_OS=='0':
                check_result = True
            elif self.G_RENDER_OS=='1':
                # windows
                if 'mnt_map' in self.G_TASK_JSON_DICT:
                    map_dict = self.G_TASK_JSON_DICT['mnt_map']
                    if len(map_dict):
                        dones = []
                        if not os.path.exists("C:/temp"):os.makedirs("C:/temp")
                        check_cmds = "net use>C:/temp/nettemp.txt"
                        os.system(check_cmds)

                        if os.path.exists("C:/temp/nettemp.txt"):
                            with open("C:/temp/nettemp.txt") as f:
                                infos = f.readlines()
                                f.close()
                            if len(infos):
                                for elm in infos:
                                    if "OK" in elm:
                                        for keys in map_dict:
                                            if keys in elm:
                                                dones.append(keys)
                                print("[%s %s]"%(len(dones),len(map_dict)))
                                if len(dones) == len(map_dict):
                                    check_result = True
                                else:
                                    cunt +=1
                                    time.sleep(2)
                                    check_result = self.CheckNetuse(cunt)
                        if cunt == 4:
                            for elm in map_dict.keys():
                                if not elm in dones:
                                    print("Fiald when do net use with disk '%s' "%elm)

        return check_result


        