#!/usr/bin/env python
#encoding:utf-8
# -*- coding: utf-8 -*-
import os,sys,time,re
import subprocess
import socket
import json
import threading

class HoudiniJob():

    @classmethod
    def SysTemInfo(cls):
        _hostname = socket.gethostname()
        _plant = sys.platform
        _ip_end = re.findall(r"\d+",_hostname)
        _ip_a = _ip_end[0]
        z_num = 0
        for i in range(0,len(_ip_a)):
            if not _ip_a[i]=="0":
                z_num=i
                break
        _ip_a =_ip_a[z_num:]
        _ipList = socket.gethostbyname_ex(_hostname)
        _this_ip = ''
        for elm in _ipList[-1]:
            _ip_ss = elm.split(".")
            if _ip_a in _ip_ss:
                _this_ip = elm
                break
        return _plant,_hostname,_this_ip

    @classmethod
    def PluginsSetup(cls,houdiniversion='',plugin_adict={},plugins_dirt='',plugins_surpose=[]):

        if len(plugin_adict):
            _plugin_dirt = '%s/plugins'%plugins_dirt
            sys.path.append(_plugin_dirt)
            for key in plugin_adict:
                if key in plugins_surpose: # surpose
                    import Script
                    if os.path.exists('%s/Script/%s/%s_set.py'%(_plugin_dirt,key,key)):
                        hfs_ver = houdiniversion[:2]+"."+houdiniversion[2:3]+"."+houdiniversion[3:]
                        cmds_py = 'GetIfon = Script.%s.%s_set.SET_ENV(hfs_ver,plugin_adict[key])'%(key,key)
                        
                        exec(cmds_py)
                        return GetIfon
                        


    @classmethod
    def LogExcute(cls):
        pass

    @classmethod
    def GetSaveHipInfo(cls,hipfile='',_app_path=''):
        with open(hipfile, 'rb') as src:
            Not_find = True
            search_elm = 2
            search_elm_cunt = 0
            while Not_find:
                line = src.readline()
                # Save version 
                if re.match('^set -g _HIP_SAVEVERSION = ', line):                    
                    _HV = re.search("\'.*\'", line).group()[1:-1]
                    _VS = _HV.split('.')
                    _hfs_save_version = int(_VS[0] + _VS[1] + _VS[2])
                    search_elm_cunt += 1

                # The $HIP val with this file saved
                if re.match('^set -g HIP = ', line):                    
                    _Hip = re.search("\'.*\'", line).group()[1:-1]
                    _hip_save_val = _Hip.replace("\\","/")
                    search_elm_cunt += 1
                if search_elm_cunt >= search_elm:
                    Not_find = False
        
        # get the bast version for running
        if not  Not_find:
            _files_name = []
            _ver_list = []            
            for (dirpath, dirnames, filenames) in os.walk(_app_path):
                _files_name.extend(filenames)
            if len(_files_name):
                for elm in _files_name:
                    ver = elm.split(".7z")[0] if ".7z" in elm else ''
                    try:
                        _ver_list.append(int(ver))
                    except:
                        pass

 
            if len(_ver_list):
                _ver_list = sorted(_ver_list)
                mid = len(_ver_list)
                if int(_hfs_save_version)>=_ver_list[mid/2]:
                    min_ver = _ver_list[mid/2]
                    max_ver = _ver_list[mid-1]
                    much_ver = 0
                    get_ver = 0
                    if int(_hfs_save_version)<max_ver:
                        for i in xrange(mid/2,len(_ver_list)):
                            if int(_hfs_save_version)==_ver_list[i]:
                                get_ver = _ver_list[i]
                                break
                            elif int(_hfs_save_version)>_ver_list[i]:
                                min_ver = _ver_list[i]
                            elif int(_hfs_save_version)<_ver_list[i] and much_ver==0:
                                much_ver = _ver_list[i]
                        _hfs_version = get_ver if get_ver else much_ver
                    else:
                        _hfs_version = max_ver
                else:
                    min_ver = _ver_list[0]
                    max_ver = _ver_list[(mid/2)-1]
                    much_ver = 0
                    get_ver = 0
                    if int(_save_version)<max_ver:
                        for i in xrange(0,mid/2):
                            if int(_save_version)==_ver_list[i]:
                                get_ver = _ver_list[i]
                                break
                            elif int(_save_version)>_ver_list[i]:
                                min_ver = _ver_list[i]
                            elif int(_save_version)<_ver_list[i] and much_ver==0:
                                much_ver = _ver_list[i]
                        _hfs_version = get_ver if get_ver else much_ver
                    else:
                        _hfs_version = max_ver
                _hfs_version = str(_hfs_version)

                return [_hfs_save_version,_hfs_version,_hip_save_val]

            else:
                _erorr_code_info = 'The app folder is emplty.'
                return [_erorr_code_info]
        else:
            _erorr_code_info = 'Bad hip file.'
            return [_erorr_code_info]


    @classmethod
    def KillApps(cls,Killapps=[],platform='win'):
        for app in Killapps:
            if not platform=='Linux':
                cmds = r'c:\windows\system32\cmd.exe /c c:\windows\system32\TASKKILL.exe /F /IM %s'%app
            elif platform=='Linux':
                cmds = ''
            subprocess.call(cmds,shell=True)
           


class MyThread(threading.Thread):
    def __init__(self,func,args,name=''):
        super(MyThread,self).__init__()
        self.func = func
        self.args = args
        self.name = name

    def run(self):
        apply(self.func,self.args)