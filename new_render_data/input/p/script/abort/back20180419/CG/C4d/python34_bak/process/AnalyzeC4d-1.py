#!/usr/bin/env python
# -*- coding=utf-8 -*-
# Author: kaname
# QQ: 1394041054

""" C4d analyzer """

import os
import sys
import subprocess
import logging

reload(sys)
sys.setdefaultencoding('utf-8')

from C4d import C4d
from C4dPluginManager import C4dPlugin, C4dPluginMgr
from CommonUtil import RBCommon as CLASS_COMMON_UTIL
from C4dUtil import RBC4dUtil as CLASS_C4D_UTIL


def get_node(node):
    if "A" in node or "B" in node or "C" in node or "D" in node or "E" in node or "F" in node:
        return "ABCDEF"
    if "K" in node:
        return "K"
    if "L" in node or "M" in node or "N" in node or "O" in node or "P" in node or "Q" in node:
        return "LNOPQ"
    if "G" in node or "H" in node or "J" in node:
        return "GHJ"

    return "ABCDEF"

class AnalyzeC4d(C4d):
    def __init__(self, **paramDict):
        C4d.__init__(self, **paramDict)
        self.format_log('AnalyzeC4d.init', 'start')
        
        self.G_TIPS_TXT_NODE=os.path.join(self.G_WORK_RENDER_TASK_CFG, 'tips.json').replace('\\','/')

        for key, value in self.__dict__.items():
            self.G_DEBUG_LOG.info(key + '=' + str(value))
            
        self.format_log('done','end')

    def RB_CONFIG(self):
        self.G_DEBUG_LOG.info('[C4d.Plugin.config.begin......]')
        if self.G_CG_CONFIG_DICT.has_key('plugins'):
            print self.G_CG_CONFIG_DICT
            plugin_dict = self.G_CG_CONFIG_DICT['plugins']
            
            for plugins_key in plugin_dict.keys():
                plugin_str = plugins_key + plugin_dict[plugins_key]
                node = get_node(self.G_NODE_NAME)

                plugin_mgr = C4dPluginMgr(self.G_USER_ID, self.G_PLUGIN_PATH)
                #plugin_mgr.copy_R18_exe(self.G_CG_VERSION)
                #self.G_DEBUG_LOG.info('copy_R18_exe was done!!!')
                for key, value in self.G_CG_CONFIG_DICT['plugins'].items():
                    print key, value, self.G_CG_VERSION
                    plugin = C4dPlugin()
                    plugin.plugin_name = key
                    plugin.plugin_version = value
                    plugin.soft_version = self.G_CG_VERSION
                    plugin.node = node
                    
                    self.G_DEBUG_LOG.info(r'[ python = "C:\script\new_py\CG\C4d\function\C4dPluginManager.py" "%s" "%s" "%s" "%s" ]' % (plugin.plugin_name, \
                                                                                plugin.plugin_version, \
                                                                                plugin.soft_version, \
                                                                                plugin.node))
     
                    result = plugin_mgr.set_custom_env(plugin)

        else:
            print 'There is no key with plugins in the task.json'
        
        self.G_DEBUG_LOG.info('[C4d.Plugin.config.end......]')

    def RB_RENDER(self):
        self.G_DEBUG_LOG.info('[c4d.RBanalyse.start.....]')

        cg_ver = self.G_CG_VERSION
        task_id = self.G_TASK_ID
        cg_file = self.G_INPUT_CG_FILE
        task_json = self.G_TASK_JSON
        asset_json = self.G_ASSET_JSON
        tips_json = self.G_TIPS_TXT_NODE

        c4d_loader = C4dLoader(cg_ver, task_id, cg_file, task_json, asset_json, tips_json)
        c4d_loader.execute()

        self.G_DEBUG_LOG.info('[c4d.RBanalyse.end.....]')

