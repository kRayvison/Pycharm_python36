#!/usr/bin/env python
#encoding:utf-8
# -*- coding: utf-8 -*-
import pymel.core as pm
import maya.cmds as cmds
import maya.mel as mel
import os,sys,re
import time

from PreRender import PreRenderBase as CLASS_PRE_BASE

def main(*args):
    PRE_BASE = CLASS_PRE_BASE()
    info_dict = args[0]
    # print (info_dict) #prerender  info   dict
    print (info_dict["user_id"]) #int
    # print (info_dict["start"])   #int
    # print (info_dict["mapping"]) #dict
    print (info_dict["task_id"])  #int
    print (info_dict["plugins"])  #dict
    # print (info_dict["rendersetting"]) #dict
    start = info_dict["start"]
    mel.eval("putenv(\"MAYA_DISABLE_BATCH_RUNUP\",\"1\"); global proc dynRunupForBatchRender() {}; ")
    print ("Set MAYA_DISABLE_BATCH_RUNUP = 1 ")
    mel.eval("optionVar -iv \"evaluationMode\" 1;")
    print "set evaluationMode to dg"
    print int(start)
    if start:
        cmds.currentTime(int(start), edit=True)
        print "update frame"
    
    for i in pm.ls(type="aiOptions"):
        # print "defaultArnoldRenderOptions.abortOnError 0"
        # i.abortOnError.set(0)
        if i.hasAttr("log_verbosity"):
            i.log_verbosity.set(1)
            print "log_verbosity 1"
            if info_dict["task_id"] in [10391487]:
                if i.hasAttr("use_existing_tiled_textures"):
                    i.use_existing_tiled_textures.set(False)
                if i.hasAttr("log_verbosity"):
                    i.log_verbosity.set(2)
                    print "log_verbosity 2"
        if i.hasAttr("autotx"):
            i.autotx.set(False)
        # if i.hasAttr("bucketSize"):
            # i.bucketSize.set(64)
        if i.hasAttr("textureMaxMemoryMB"):
            ar_node = pm.PyNode("defaultArnoldRenderOptions")
            ar_node.textureMaxMemoryMB.set(l=0)
            i.textureMaxMemoryMB.set(20480)    





