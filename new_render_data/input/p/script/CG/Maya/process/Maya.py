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
        #maya版本
        self.G_CG_VERSION=self.G_TASK_JSON_DICT['software_config']['cg_name']+self.G_TASK_JSON_DICT['software_config']['cg_version']
        #提交时的 render_layer_type
        self.RENDER_LAYER_TYPE = self.G_SYSTEM_JSON_DICT['system_info']['common']['render_layer_type']

        #c:\script\new_py\CG\Maya\script
        self.G_NODE_MAYASCRIPT=os.path.normpath(os.path.join(self.G_NODE_PY,'CG/Maya/script'))
        # c:\script\new_py\CG\Maya\function
        self.G_NODE_MAYAFUNCTION=os.path.normpath(os.path.join(self.G_NODE_PY,'CG/Maya/function'))

        #maya文件路径
        self.G_INPUT_CG_FILE = self.G_INPUT_CG_FILE.replace("\\","/")
        #工程目录 //10.60.100.104/d/inputdata5/100000000/100000189/Z
        self.G_INPUT_PROJECT_PATH = self.G_INPUT_PROJECT_PATH.replace("\\","/")

        #将 IP 路径 改成 映射盘符路径
        if 'mnt_map' in self.G_TASK_JSON_DICT:        #处理斜杠问题
            index = 0
            map_dict = self.G_TASK_JSON_DICT['mnt_map']
            for key, value in list(map_dict.items()):
                if value in self.G_INPUT_PROJECT_PATH:
                    index +=1
                    self.G_INPUT_PROJECT_PATH = re.sub(value, key, self.G_INPUT_PROJECT_PATH)
                if value in self.G_INPUT_CG_FILE:
                    index +=1
                    self.G_INPUT_CG_FILE = re.sub(value, key, self.G_INPUT_CG_FILE)
                if index == 2:
                    break

        #处理斜杠问题
        self.G_INPUT_PROJECT_PATH = os.path.normpath(self.G_INPUT_PROJECT_PATH)
        self.G_INPUT_CG_FILE = os.path.normpath(self.G_INPUT_CG_FILE)
        self.format_log('done','end')
        
        
        
        
        
        