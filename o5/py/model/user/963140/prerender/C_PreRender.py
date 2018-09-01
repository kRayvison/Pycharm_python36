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
    print ("custome prerender  start ----------- ")
    info_dict = args[0]
    # print (info_dict) #prerender  info   dict
    print (info_dict["user_id"]) #int
    # print (info_dict["start"])   #int
    # print (info_dict["mapping"]) #dict
    print (info_dict["task_id"])  #int
    # print (info_dict["plugins"])  #dict
    # print (info_dict["rendersetting"]) #dict
    
    
    for i in pm.ls(type="aiOptions"):
        # print "defaultArnoldRenderOptions.abortOnError 0"
        # i.abortOnError.set(1)
        if i.hasAttr("log_verbosity"):
            i.log_verbosity.set(1)
        if i.hasAttr("autotx"):
            i.autotx.set(False)
        if i.hasAttr("textureMaxMemoryMB"):
            i.textureMaxMemoryMB.set(20480)
        if info_dict["task_id"] in [10358458,10378581,10378755,10382721,10381174,10381224]:
            if i.hasAttr("use_existing_tiled_textures"):
                i.use_existing_tiled_textures.set(0)
                print "Set use_existing_tiled_textures OFF "
    
    
    print ("custome prerender  end ----------- ")
    
    
    
    




