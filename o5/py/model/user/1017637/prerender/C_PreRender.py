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
    
    if info_dict["task_id"] in [10534306]:
        for i in pm.ls(type="VRaySettingsNode"):
            if i.hasAttr("sys_message_level"):
                i.sys_message_level.set(4)
                print ("%s sys_message_level.set(4)" %i)
    
    
    




