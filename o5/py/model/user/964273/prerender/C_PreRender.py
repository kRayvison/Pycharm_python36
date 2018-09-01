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
                
    # mel.eval("putenv(\"MAYA_DISABLE_BATCH_RUNUP\",\"1\"); global proc dynRunupForBatchRender() {}; ")
        # if i.hasAttr("textureMaxMemoryMB"):
            # i.textureMaxMemoryMB.set(20480)


    print "custome prerender  end ----------- "
    
    
    
    




