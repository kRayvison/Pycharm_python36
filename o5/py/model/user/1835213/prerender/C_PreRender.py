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
        print "defaultArnoldRenderOptions.abortOnError 0"
        i.abortOnError.set(0)
        i.log_verbosity.set(1)
        print "set log_verbosity to 1"
    
    
    




