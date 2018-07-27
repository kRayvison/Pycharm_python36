#!/usr/bin/env python
#encoding:utf-8
# -*- coding: utf-8 -*-
import logging
import os
import sys
import subprocess
import string
import logging
import time
import shutil

reload(sys)
sys.setdefaultencoding('utf-8')

sys.path.append('C:/script/new_py/Base')
sys.path.append('/root/rayvision/script/new_py/Base')

try:
    from AnalyzeBase import *
except:
    pass
try:
    from RenderBase import *
except:
    pass

class RenderAction():
    def __init__(self,**paramDict):
        cg_name=paramDict['G_CG_NAME']
        node_py=paramDict['G_NODE_PY']
        action=paramDict['G_ACTION']
        print 'cg_name=================='+cg_name
        print 'node_py=================='+node_py
        print 'action==================='+action
        
        #-----------append cg py path---------------
        cg_py_path=os.path.join(node_py,'CG',cg_name)
        print ('cg_py_path='+cg_py_path)
        if os.path.exists(cg_py_path):
            print 'append path-------'
            sys.path.append(cg_py_path)
        if os.path.exists(node_py+'/Util'):
            sys.path.append(node_py+'/Util')
        
        module_name = action+cg_name
        if action == 'RenderPhoton' or action == 'MergePic':
            module_name = 'Render '+cg_name
        if action == 'MergePhoton':
            module_name = 'Merge'
            
        class_name = cg_name
        if action == 'Pre':
            class_name = action+cg_name
        
        #-----------import cg py model---------------
        from_str = 'from '+module_name+' import *'
        print ('from_str='+from_str)
        print ('class_name='+class_name)
        exec(from_str)
        
        exec('RenderAction.__bases__=('+class_name+',)')
        exec(class_name+'.__init__(self,**paramDict)')   
        
#-----------------------main-------------------------------
def main(**paramDict):
    render=RenderAction(**paramDict)
    render.RB_EXECUTE()