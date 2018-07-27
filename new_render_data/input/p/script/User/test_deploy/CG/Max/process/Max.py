#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import codecs
import json

from RenderBase import *
from CommonUtil import RBCommon as CLASS_COMMON_UTIL


class Max(RenderBase):
    def __init__(self,**param_dict):
        RenderBase.__init__(self,**param_dict)
        
        #global variable
        if self.G_ACTION != 'Analyze':
            renderer = self.G_TASK_JSON_DICT['scene_info_render']['renderer']
            
            ## kg
            self.G_KG='0'
            if renderer.get('gi', None) == '1':  # 0:gi off / 1:gi on
                if renderer.get('primary_gi_engine', None) == '0' and renderer.get('irradiance_map_mode', None) == '6':  # Animation(prepass)
                    self.G_KG='101'
                elif (renderer.get('primary_gi_engine', None) == '0' and renderer.get('irradiance_map_mode', None) == '4') or (
                        (renderer.get('primary_gi_engine', None) == '3' or renderer.get('secondary_gi_engine', None) == '3') and
                        renderer.get('light_cache_mode', None) == '1'):  # Incremental add to current map/Fly-through
                    self.G_KG='100'
                    if renderer.get('photonnode', None) == '1':  # 0:single node / 1:multi node
                        self.G_KG='102'
                
                    
            ## onlyphoton
            self.G_ONLY_PHOTON = renderer.get('onlyphoton', None)
        
            ## multi camera
            self.G_MULTI_CAMERA = False
            self.G_WORK_RENDER_TASK_OUTPUT_XXX = self.G_WORK_RENDER_TASK_OUTPUT.replace('\\','/')
            if 'renderable_camera' in self.G_TASK_JSON_DICT['scene_info_render']['common']:
                renderable_camera = self.G_TASK_JSON_DICT['scene_info_render']['common']['renderable_camera']  #list
                if len(renderable_camera) > 1:
                   self.G_MULTI_CAMERA = True
                   self.G_WORK_RENDER_TASK_OUTPUT_XXX = self.G_WORK_RENDER_TASK_OUTPUT_XXX + '/' + self.G_SMALL_TASK_ID
                   
            ## task.json(ascii)
            self.G_TASK_JSON_A = os.path.normpath(os.path.join(self.G_WORK_RENDER_TASK_CFG,'task_a.json'))
            if self.G_CG_VERSION=='3ds Max 2012' or self.G_CG_VERSION=='3ds Max 2011' or self.G_CG_VERSION=='3ds Max 2010' or self.G_CG_VERSION=='3ds Max 2009':
                with codecs.open(self.G_TASK_JSON,'rb','utf-8') as fp1:
                    with codecs.open(self.G_TASK_JSON_A,'wb',sys.getfilesystemencoding()) as fp2:
                        content = fp1.read()
                        fp2.write(content)
                
                
        self.G_WORK_RENDER_TASK_BLOCK=os.path.normpath(os.path.join(self.G_WORK_RENDER_TASK,'block'))
        self.G_WORK_RENDER_TASK_GRAB=os.path.normpath(os.path.join(self.G_WORK_RENDER_TASK,'grab'))
        self.G_WORK_RENDER_TASK_MAX=os.path.normpath(os.path.join(self.G_WORK_RENDER_TASK,'max'))
        self.G_WORK_RENDER_TASK_MAXBAK=os.path.normpath(os.path.join(self.G_WORK_RENDER_TASK,'maxbak'))
        self.G_CG_VERSION=self.G_TASK_JSON_DICT['software_config']['cg_name']+' '+self.G_TASK_JSON_DICT['software_config']['cg_version']
        dir_list=[]
        dir_list.append(self.G_WORK_RENDER_TASK_BLOCK)
        dir_list.append(self.G_WORK_RENDER_TASK_GRAB)
        dir_list.append(self.G_WORK_RENDER_TASK_MAX)
        dir_list.append(self.G_WORK_RENDER_TASK_MAXBAK)
        CLASS_COMMON_UTIL.make_dirs(dir_list)
        
        self.G_MAX_B=os.path.normpath('B:/plugins/max')
        self.G_MAX_SCRIPT=os.path.join(self.G_MAX_B,'script')
        
        self.G_NODE_MAXSCRIPT=os.path.normpath(os.path.join(self.G_NODE_PY,'CG/Max/script'))
        # self.G_NODE_PY_CUSTOM=os.path.normpath(os.path.join(self.G_NODE_PY,'custom'))
        self.ASSET_WEB_COOLECT_BY_PATH=False
        
        # handle GPU platform plugins(redshift_GPU)
        if self.G_PLATFORM == '10':  # GPU平台
            plugins_dict = self.G_CG_CONFIG_DICT.get('plugins', {})
            if 'redshift' in plugins_dict:
                plugins_dict['redshift_GPU'] = plugins_dict.pop('redshift')
                self.G_CG_CONFIG_DICT['plugins'] = plugins_dict
        
        # 是否需要GPU机器进行分析、预处理，cpu/gpu
        self.G_ANALYSE_NODE_TYPE = self.G_SYSTEM_JSON_DICT['system_info']['common'].get('analyse_node_type', 'cpu')
        self.G_PRE_NODE_TYPE = self.G_SYSTEM_JSON_DICT['system_info']['common'].get('pre_node_type', 'cpu')
        self.G_RENDER_NODE_TYPE = self.G_SYSTEM_JSON_DICT['system_info']['common'].get('render_node_type', 'cpu')
        