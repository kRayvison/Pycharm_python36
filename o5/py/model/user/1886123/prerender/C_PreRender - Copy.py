#!/usr/bin/env python
#encoding:utf-8
# -*- coding: utf-8 -*-
import pymel.core as pm
import maya.cmds as cmds
import maya.mel as mel
import os,sys,re
import time


def main(*args):
    # mel.eval("putenv(\"MAYA_DISABLE_BATCH_RUNUP\",\"1\"); global proc dynRunupForBatchRender() {}; ")
    mel.eval("optionVar -iv \"evaluationMode\" 1;")
    print "set evaluationMode to dg"
    
    info_dict = args[0]
    start = info_dict["start"]
    mel.eval("putenv(\"MAYA_DISABLE_BATCH_RUNUP\",\"1\"); global proc dynRunupForBatchRender() {}; ")
    print ("Set MAYA_DISABLE_BATCH_RUNUP = 1 ")
    mel.eval("optionVar -iv \"evaluationMode\" 1;")
    print "set evaluationMode to dg"
    print int(start)
    if start:
        cmds.currentTime(int(start)-1, edit=True)
        print "update frame"    
    
    for i in pm.ls(type="aiOptions"):
        print "defaultArnoldRenderOptions.abortOnError 0"
        i.abortOnError.set(0)
        i.log_verbosity.set(1)
        print "set log_verbosity to 1"
        
    # for a in pm.ls(type="VRayScatterTexture"):
        # print a
        # node = pm.PyNode(a)
        # b = node.outColor.get()
        # pm.lockNode( a, lock=True)
        # print "%s is lock" % a
        # print b
    
    
    




