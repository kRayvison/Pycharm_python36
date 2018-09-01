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
        # print "defaultArnoldRenderOptions.abortOnError 0"
        # i.abortOnError.set()
        i.log_verbosity.set(2)
    
    print "2222222222222222"
    
    print "custome prerender  end ----------- "
    
    
    
    




