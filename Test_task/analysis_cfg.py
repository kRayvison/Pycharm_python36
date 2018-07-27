# -*- coding: utf-8 -*-
import json
import os
class analysisCfg():
    def __init__(self):
        cfg_jsonPath = r'D:\cfg\cfg\task.json'
        self.k_cfg_json = json.loads(open(cfg_jsonPath).read())

        sys_jsonPath = r'D:\cfg\sys_cfg\system.json'
        self.k_sys_json = json.loads(open(sys_jsonPath).read())

    def analysisPlugins(self):
        k_plugins = {}
        k_plugins = (self.k_cfg_json['software_config']['plugins'] if self.k_cfg_json['software_config']['plugins'] else '')
        return k_plugins

    def analysisSoft(self):
        k_mayaver = ''
        if self.k_cfg_json['software_config']['cg_name'] == 'Maya':
            k_mayaver = self.k_cfg_json['software_config']['cg_version']
        else : k_mayaver = 'It is not maya task!!!'
        return k_mayaver

    def analysisMapping(self):
        k_mapping = {}
        k_mapping = (self.k_cfg_json['mnt_map'] if self.k_cfg_json['mnt_map'] else '')

        return k_mapping

    def analysisPath(self):
        k_path = {}
        k_path = (self.k_sys_json['system_info']['common'] if self.k_sys_json['system_info']['common'] else '')

        return k_path



if __name__ == '__main__':
    a=analysisCfg()
    print (a.analysisMnt())