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

sys.path.append('C:/script/py/Base')
sys.path.append('/root/rayvision/script/py/Base')
from RenderBase import RenderBase 

reload(sys)
sys.setdefaultencoding('utf-8')


class RenderAction():
    def __init__(self,**paramDict):
        cgName=paramDict['G_CG_NAME']
        nodePyDir=paramDict['G_NODE_PY']
        print 'cgName=================='+cgName
        print 'nodePyDir=================='+nodePyDir
        
        #-----------apeend cg py path---------------
        
        cgPyPath=nodePyDir+'/'+cgName
        if cgName == 'Preprocess' or cgName == 'MaxClient' or cgName == 'Merge':
            cgPyPath=nodePyDir+'/'+'Max'
        if cgName == 'MayaPre' or cgName == 'MayaClient':
            cgPyPath=nodePyDir+'/'+'Maya'
        print ('cgPyPath='+cgPyPath)
        if os.path.exists(cgPyPath):
            print 'append path-------'
            sys.path.append(cgPyPath)
        if os.path.exists(nodePyDir+'/Util'):
            sys.path.append(nodePyDir+'/Util')
            
        #-----------import cg py model---------------
        fromStr='from Render'+cgName+' import *'
        if cgName=='Preprocess' or cgName=='MayaPre' or cgName=='Merge' :
            fromStr='from '+cgName+' import *'
        elif cgName=='MaxClient':
            fromStr='from RenderMax import *'
        elif cgName=='MayaClient':
            fromStr='from RenderMaya import *'
        print ('fromStr='+fromStr)
        exec(fromStr)
        
        exec('RenderAction.__bases__=('+cgName+',)')
        exec(cgName+'.__init__(self,**paramDict)')
        
        #exec('RenderAction.__bases__=('+cgName+',)')
        #exec(cgName+'.__init__(self,**paramDict)')
    '''
    def RBrender(self):#Render command
        print 'RenderAction..max...render....'
    '''
#-----------------------main-------------------------------
def main(**paramDict):
    render=RenderAction(**paramDict)
    print 'G_POOL_NAME___'+render.G_POOL
    render.RBexecute()