#!/usr/bin/env python
#encoding:utf-8
# -*- coding: utf-8 -*-
import pymel.core as pm
import maya.cmds as cmds
import maya.mel as mel
import os,sys,re
import time



def main(*args):
    for i in pm.ls(type="aiOptions"):
        # print "defaultArnoldRenderOptions.abortOnError 0"
        # i.abortOnError.set(1)
        if i.hasAttr("log_verbosity"):
            i.log_verbosity.set(1)
        if i.hasAttr("autotx"):
            i.autotx.set(False)
        if i.hasAttr("textureMaxMemoryMB"):
            ar_node = pm.PyNode("defaultArnoldRenderOptions")
            ar_node.textureMaxMemoryMB.set(l=0)
            print i.textureMaxMemoryMB.get()
            i.textureMaxMemoryMB.set(20480)

        
        
    
    




