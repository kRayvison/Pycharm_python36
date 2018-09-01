#!/usr/bin/env python
#encoding:utf-8
# -*- coding: utf-8 -*-
import pymel.core as pm
import maya.cmds as cmds
import maya.mel as mel
import os,sys,re
import time



def main(*args):
    print "custome prerender  start ----------- "
    info_dict = args[0]
    # print (info_dict) #prerender  info   dict
    print (info_dict["user_id"]) #int
    print (info_dict["start"])   #int
    # print (info_dict["mapping"]) #dict
    print (info_dict["task_id"])  #int
    print (info_dict["plugins"])  #dict
    # print (info_dict["rendersetting"]) #dict
    rendersetting = info_dict["rendersetting"]
    

    for i in pm.ls(type="aiOptions"):
        if i.hasAttr("log_verbosity"):
            i.log_verbosity.set(1)
        if i.hasAttr("autotx"):
            i.autotx.set(False)
        if info_dict["start"]:
            cmds.currentTime(int(info_dict["start"] - 1), edit=True)
        if info_dict["task_id"] in [10473600]:
            if i.hasAttr("lock_sampling_noise"):
                i.lock_sampling_noise.set(True)
                print "Set lock_sampling_noise to  True!!! "
                
    # mel.eval("putenv(\"MAYA_DISABLE_BATCH_RUNUP\",\"1\"); global proc dynRunupForBatchRender() {}; ")
        # if i.hasAttr("textureMaxMemoryMB"):
            # i.textureMaxMemoryMB.set(20480)

    
    for i in pm.ls(type="VRaySettingsNode"):
        if i.hasAttr("srdml"):
            org_srdml = i.srdml.get()
            print "Your scens originalvray srdml is %s " % (org_srdml)
            if "vrayformaya" in info_dict["plugins"]:
                print type(info_dict["plugins"]["vrayformaya"])
                if info_dict["plugins"]["vrayformaya"] >= "3.10":
                    print "Your task vray version >= 3.10,set srdml to 0 "
                    if info_dict["task_id"] == 10479713:
                        i.srdml.set(40960)
                        print ("%s.srdml.set(40960)" %i)
                    else:
                        i.srdml.set(0)
                else:
                    i.srdml.set(20480)
                    print "Your vray version lower than  3.10.01,set srdml to 20480MB"
        if rendersetting:
            if 'width' in rendersetting and i.hasAttr("width"):
                i.width.set(rendersetting['width'])
            if 'height' in rendersetting and i.hasAttr("height"):
                i.height.set(rendersetting['height'])
            print "Reset scene vray Resolution attributes according to your render.cfg file !!! "
    

    print "custome prerender  end ----------- "
    
    
    
    




