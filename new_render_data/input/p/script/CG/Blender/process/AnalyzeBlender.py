#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os
import sys
import subprocess
import time
import shutil
import logging
from RenderBase import RenderBase
from CommonUtil import RBCommon as CLASS_COMMON_UTIL

class AnalyzeBlender(RenderBase):
    def __init__(self, **param_dict):
        RenderBase.__init__(self, **param_dict)
        print("Blender.INIT")
        self.G_CG_VERSION = '%s-%s' % (self.G_CG_CONFIG_DICT['cg_name'], self.G_CG_CONFIG_DICT['cg_version'])
        self.G_RUN_PY = os.path.join(self.G_NODE_PY, 'CG', self.G_CG_NAME, 'script', 'check.py')
        self.G_EXE = os.path.join('B:/plugins/blender/Blender Foundation', self.G_CG_VERSION, 'blender.exe')
    
    def RB_RENDER(self):#7
        self.G_DEBUG_LOG.info('[Blender.RB_RENDER.start.....]')
        
        
        analyse_cmd = '"{exe_path}" -b "{cg_file}" -P "{run_py}" -- "{task_json}" "{tips_json}" "{asset_json}"'.format(
            exe_path=self.G_EXE,
            cg_file=self.G_INPUT_CG_FILE,
            run_py=self.G_RUN_PY,
            task_json=self.G_TASK_JSON,
            tips_json=self.G_TIPS_JSON,
            asset_json=self.G_ASSET_JSON,
        )
        
        CLASS_COMMON_UTIL.cmd(analyse_cmd, my_log=self.G_DEBUG_LOG, continue_on_error=True)

        self.G_DEBUG_LOG.info('[Blender.RB_RENDER.end.....]')

        