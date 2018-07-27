#!/usr/bin/env python
#encoding:utf-8
# -*- coding: utf-8 -*-
## create by shen,2018.06.22
import os,sys,time
import subprocess
import argparse
# import socket
# import shutil
# import platform
import re,json

class HfsBase():

    def __init__(self,analysis=0,**args):
        # print(args)
        if analysis:
            self._args = args
            print("_args",self._args)
        elif len(args):
            ## {"hipFile":"","hfsBin":""}
            self._hipFile = args["cg_file"]
            self._hfsBin = args["exe_path"]
            self._task_json = args["task_json"]
            self._asset_json = args["asset_json"]
            self._tips_json = args["tips_json"]
            self._hfsbase_path = args["hfsbase_path"]
        else:
            self._hipFile = ""
            self._hfsBin = ""

    def WriteFile(self,something,file):
        pass

        
    @staticmethod
    def GetSaveVersion(hipfile=""):
        if os.path.exists(hipfile):
            with open(hipfile, "rb") as hipf:
                Not_find = True
                search_elm = 2
                search_elm_cunt = 0
                while Not_find:
                    line = str(hipf.readline()).encode("utf-8")
                    if "set -g _HIP_SAVEVERSION = " in  str(line):
                        # print(str(line))
                        pattern = re.compile("[\d+\d+\d+]")
                        _HV = pattern.findall(str(line))
                        if len(_HV)>6: _HV = _HV[:6]
                        _hfs_save_version = int(''.join(elm for elm in _HV))
                        _hfs_save_version = "%s.%s.%s" % (str(_hfs_save_version)[:2],
                                      str(_hfs_save_version)[2:3],str(_hfs_save_version)[3:])
                        search_elm_cunt += 1

                    # The $HIP val with this file saved
                    if "set -g HIP = " in  str(line):
                        pattern = re.compile("\\'.*\\'") if sys.version[:1]=="2" else re.compile(r"\\'.*\\'")
                        _Hip = pattern.search(str(line)).group()
                        _hip_save_val = _Hip.split("\'")[1].replace("\\","/")
                        search_elm_cunt += 1
                    if search_elm_cunt >= search_elm:
                        Not_find = False
        else:
            print("The .hip file is not exist.")
            _hfs_save_version,_hip_save_val = ("","")
        return _hfs_save_version,_hip_save_val

    def GetAssets(self):
        # softCmd=self._houdini_client_dir+"/"+self._hfs_version+"/bin/%s"%hython
        # renderPy=r' %s/script/analyse.py '% self._code_base_path
        # renderproject='-project "%s"' % self._hip_file
        # renderout=' -outdir "%s"' % self._task_folder
        # plugindir=' -plugindir "%s"' % self._houdini_PLuing_dirt
        # cust_id = ' -custid %s'%self.user_id

        renderCmd=softCmd+renderPy+renderproject+renderGPU+renderout+plugindir+cust_id
        cmds = ""
        print(cmds)
        

    @staticmethod
    def isFile(pathvale):
        isFilepath = False
        persent = 0
        drive_spl = os.path.splitdrive(pathvale)
        ext_spl = os.path.splitext(pathvale)
        along_spl = os.path.split(pathvale)
        if pathvale.replace("\\","/").startswith("//"):persent += 7
        if len(drive_spl[0]) and len(drive_spl[-1]):persent += 7
        if "/" in along_spl[0].replace("\\","/"):
            persent += 4
            ss = re.findall("[/*,//]",ext_spl[0].replace("\\","/"))
            if len(ss)>1:persent += 1
        if len(ext_spl[-1]):persent += 5
        if persent>9:isFilepath = True
        # print("persent",persent)
        # print(drive_spl)
        # print(ext_spl)
        # print(along_spl)

        return isFilepath

def SetArgs():

    parser = argparse.ArgumentParser()
    parser.add_argument('-project', type=str, required=True, help='.hip file to load')
    parser.add_argument('-task', type=str, required=True, help='the asset file .json path')
    parser.add_argument('-asset', type=str, required=True, help='the asset file .json path')
    parser.add_argument('-tips', type=str, required=True, help='the asset file .json path')
    args = parser.parse_args()
    print(args)

if __name__ == "__main__":

    print(sys.version)
    f="E:/houdini_test/sphere.hip"
    hfs_version = HfsBase.GetSaveVersion(f)
    
    print("Houdini: %s"%hfs_version[0])
    print("Hip: %s"%hfs_version[1])


    p="D:/Program Files/Side Effects Software/Houdini 16.5.268/bin/hython.exe"
    task=""
    ass=""
    tips=""
    hf = ""
    hfss = HfsBase(cg_file=f,exe_path=p,task_json=task,asset_json=ass,
                tips_json=tips,hfsbase_path=hf)
    
    # print(hfss.isFile(f))