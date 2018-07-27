#!/usr/bin/env python
#encoding:utf-8
# -*- coding: utf-8 -*-
import os
import sys
from RenderBase import *
from CommonUtil import RBCommon as CLASS_COMMON_UTIL
from imp import reload
reload(sys)
# sys.setdefaultencoding('utf-8')


class Maya(RenderBase):
    def __init__(self,**param_dict):
        RenderBase.__init__(self,**param_dict)
        self.format_log('Maya.init','start')
        
        
        #global variable
        
        self.G_CG_VERSION=self.G_TASK_JSON_DICT['software_config']['cg_name']+self.G_TASK_JSON_DICT['software_config']['cg_version']
        self.RENDER_LAYER_TYPE = self.G_TASK_JSON_DICT['system_info']['common']['render_layer_type']

        self.G_NODE_MAYASCRIPT=os.path.normpath(os.path.join(self.G_NODE_PY,'CG/Maya/script'))
        self.G_NODE_MAYAFUNCTION=os.path.normpath(os.path.join(self.G_NODE_PY,'CG/Maya/function'))
        self.G_WORK_RENDER_TASK_OUTPUT_XXX = self.G_WORK_RENDER_TASK_OUTPUT.replace('\\', '/')

        self.format_log('done','end')
        
        
        
        
        
        