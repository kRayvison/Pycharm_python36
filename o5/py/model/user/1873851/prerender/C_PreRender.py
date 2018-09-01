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
    
    # mel.eval("putenv(\"MAYA_DISABLE_BATCH_RUNUP\",\"1\"); global proc dynRunupForBatchRender() {}; ")
    # print ("Set MAYA_DISABLE_BATCH_RUNUP = 1 ")
    
    # for i in pm.ls(type="VRaySettingsNode"):
        # if i.hasAttr("sys_max_threads"):
            # i.sys_max_threads.set(30)
            # PRE_BASE.log_scene_set("sys_max_threads","30")
    # for i in pm.ls(type="aiOptions"):
        # if i.hasAttr("threads_autodetect"):
            # i.threads_autodetect.set(0)
        
        # if i.hasAttr("threads"):
            # i.threads.set(30) 
            # PRE_BASE.log_scene_set("threads","30")
            
    
    




