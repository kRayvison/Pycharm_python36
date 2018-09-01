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
    
    start = info_dict["start"]
    print int(start)
    cmds.currentTime(int(0),edit=True)
    print "update frame"