#!/usr/bin/env python
#encoding:utf-8
# -*- coding: utf-8 -*-
import pymel.core as pm
import maya.cmds as cmds
import maya.mel as mel
import os,sys,re
import time
print "+++++++++++++++++++++++++++++++++the prerender strat++++++++++++++++++++++++++++++++++++++++++++++++"
premel_start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
print "the prerender strat time :: %s \n" % premel_start_time

#renderableCamera ="BOFB_51001_005_000:Cam1LShape"
#maya_file = "Y:/BB/show/BOFB_FILM/Maya/scenes/Shots/BOFB_51/Sc001/BOFB_51001_005_000/BOFB_51001_005_000_ra44.mb"
mel.eval("putenv(\"MAYA_DISABLE_BATCH_RUNUP\",\"1\"); global proc dynRunupForBatchRender() {}; ")
if taskid in [10175926]:
    for i in pm.ls(type="VRaySettingsNode"):            
        if i.hasAttr("srdml"):
            i.srdml.set(40960)
            print "change vray srdml to  %s MB" %(i.srdml.get())
        if i.hasAttr("sys_texture_cache_size"):
            i.sys_texture_cache_size.set(8192)

print renderableCamera
print maya_file
if "," not  in renderableCamera:
    cam_name = renderableCamera
else:
    cam_name = renderableCamera.split(',')[0]
print cam_name
if  maya_file:    
    scene_name = maya_file
else:
    scene_name = pm.system.sceneName()
print scene_name
cam_p = re.compile(r"(.*)Cam(.*)",re.I)        
cam_r = cam_p.findall(cam_name)

if re.findall(r'R|L', cam_name):
    if cam_r:
        if re.findall(r'R|L',cam_r[0][1],re.I):
            cam = re.findall(r'R|L',cam_r[0][1],re.I)[0]
            
        else:
            cam = re.findall(r'R|L', cam_name)[-1]
    else:
        cam = re.findall(r'R|L', cam_name)[-1]
else:
    cam = cam_name
    
p = re.compile(r"(.*)Shots(.*)",re.I)
r = p.findall(os.path.dirname(scene_name))

if r:    
    print r[0][1]
    new_path = "%s%s/cam_%s/<Layer>/%s_<Layer>_%s" % ("BOFB_FILM",r[0][1],cam,r[0][1].split("/")[-1],cam)
    print new_path
    register_node_types = pm.ls(nodeTypes=1)
    if "VRaySettingsNode" in register_node_types:
        for i in pm.ls(type="VRaySettingsNode"):
            i.fnprx.set(new_path)
        
    #pm.PyNode("vraySettings").fnprx.set(new_path)
    pm.PyNode("defaultRenderGlobals").imageFilePrefix.set(new_path)
    print "New output path: " + str(pm.PyNode("defaultRenderGlobals").imageFilePrefix.get())
if not r:
    print "New output path: Failed"
premel_end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
print "the prerender end time :: %s \n" % premel_end_time
print "+++++++++++++++++++++++++++++++++the prerender end++++++++++++++++++++++++++++++++++++++++++++++++"