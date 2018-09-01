#!/usr/bin/env python
#encoding:utf-8
# -*- coding: utf-8 -*-
import pymel.core as pm
import maya.cmds as cmds
import maya.mel as mel
import os,sys,re
import time


def main(*args):

    mel.eval("optionVar -iv \"evaluationMode\" 1;")
    print "set evaluationMode to dg"
    for i in pm.ls(type="aiOptions"):
        # i.use_existing_tiled_textures.set(0)
        i.motion_blur_enable.set(0)
        i.log_verbosity.set(1)

    
    
    




