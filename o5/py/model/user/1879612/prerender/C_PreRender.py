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
        if i.hasAttr("log_verbosity"):
            i.log_verbosity.set(2)
            print "log_verbosity 2"
        if i.hasAttr("autotx"):
            i.autotx.set(l=0)
            i.autotx.set(False)
            print "autotx false"
        if i.hasAttr("use_existing_tiled_textures"):
            i.use_existing_tiled_textures.set(1)
            print "use_existing_tiled_textures 1"
    
    print "custome prerender  end ----------- "
    
    
    
    




