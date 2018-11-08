# -*- coding: utf-8 -*-
import pymel.core as pm
import maya.cmds as cmds
import maya.mel as mel
import os,sys,re
import time

k_hairSystems = cmds.ls(type = 'hairSystem')

for k_hairSystem in k_hairSystems:
    if cmds.getAttr('%s.simulationMethod' %k_hairSystem) <= 1:
        pass
    elif cmds.getAttr('%s.simulationMethod' %k_hairSystem) == 2:
        print(k_hairSystem)
    elif cmds.getAttr('%s.simulationMethod' % k_hairSystem) == 3:
        print(k_hairSystem)
