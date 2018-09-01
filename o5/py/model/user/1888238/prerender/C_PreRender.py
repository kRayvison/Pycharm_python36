#!/usr/bin/env python
#encoding:utf-8
# -*- coding: utf-8 -*-
import pymel.core as pm
import maya.cmds as cmds
import maya.mel as mel
import os,sys,re
import time


def main(*args):

    info_dict = args[0]
    
    for i in pm.ls(type="aiOptions"):

        if i.hasAttr("abortOnError"):
            i.abortOnError.set(0)
            print ('abortOnError is %s') %i.abortOnError.get()

        if i.hasAttr("log_verbosity"):
            i.log_verbosity.set(1)
            print ('log_verbosity is %s') %i.log_verbosity.get()

        if info_dict["task_id"] in [10494201]:
            i.log_verbosity.set(0)
            print ('log_verbosity is %s') %i.log_verbosity.get()
            
            i.force_texture_cache_flush_after_render.set(0)
            print ('force_texture_cache_flush_after_render is %s') %i.force_texture_cache_flush_after_render.get()
            
            i.clear_before_render.set(0)
            print ('clear_before_render is %s') %i.clear_before_render.get()
    
    start = info_dict["start"]
    print int(start)
    cmds.currentTime(int(start)-1,edit=True)
    print "update frame"