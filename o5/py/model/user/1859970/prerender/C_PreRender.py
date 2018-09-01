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

    for i in pm.ls(type="aiOptions"):
        i.abortOnError.set(0)
        print "set defaultArnoldRenderOptions.abortOnError 0"
        if i.hasAttr("log_verbosity"):
            i.log_verbosity.set(2)
        if i.hasAttr("autotx"):
            i.autotx.set(False)
        # if i.hasAttr("textureMaxMemoryMB"):
            # i.textureMaxMemoryMB.set(40960)
    
    
    print "custome prerender  end ----------- "
    
    
    
    




