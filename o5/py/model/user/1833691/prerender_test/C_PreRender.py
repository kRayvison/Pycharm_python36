#!/usr/bin/env python
#encoding:utf-8
# -*- coding: utf-8 -*-
import pymel.core as pm
import maya.cmds as cmds
import maya.mel as mel
import os,sys,re
import time



print "<<<<<<<<<<<<<<<custome prerender  start >>>>>>>>>>>>>>>> "


for i in pm.ls(type="aiOptions"):
    if i.hasAttr("log_verbosity"):
        log_verbosity = i.log_verbosity.get()
        print "Scene log_verbosity is %s" % log_verbosity
        i.log_verbosity.set(1)
        print "Set log_verbosity as 1"
        print "\n"
    if i.hasAttr("autotx"):
        autotx = i.autotx.get()
        print "Scene autotx is %s" % autotx
        i.autotx.set(False)
        print "Set autotx OFF"
        print "\n"
    if i.hasAttr("use_existing_tiled_textures"):
        use_existing_tiled_textures = i.use_existing_tiled_textures.get()
        print "Scene use_existing_tiled_textures is %s" % use_existing_tiled_textures
        i.use_existing_tiled_textures.set(True)
        print "Set use_existing_tiled_textures True"
        print "\n"
    # if i.hasAttr("textureMaxMemoryMB"):
        # i.textureMaxMemoryMB.set(20480)
        
print("MAYA_DISABLE_BATCH_RUNUP=1")
mel.eval("putenv(\"MAYA_DISABLE_BATCH_RUNUP\",\"1\"); global proc dynRunupForBatchRender() {}; ")

for i in pm.ls(type="VRaySettingsNode"):
    if i.hasAttr("srdml"):
        org_srdml = i.srdml.get()
        print "Your scens originalvray srdml is %s " % (org_srdml)
        if "vrayformaya" in info_dict["plugins"]:
            print type(info_dict["plugins"]["vrayformaya"])
            if info_dict["plugins"]["vrayformaya"] >= "3.10":
                print "Your task vray version >= 3.10,set srdml to 0 "
                i.srdml.set(0)
            else:
                i.srdml.set(20480)
                print "Your vray version lower than  3.10.01,set srdml to 20480MB"

print "<<<<<<<<<<<<<<<custome prerender  end >>>>>>>>>>>>>>>> "








