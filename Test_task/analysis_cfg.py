# -*- coding: utf-8 -*-
import json
import os
class analysisCfg():
    def __init__(self,platform,taskID,userID):

        self.k_jsonerror = False

        platform_address = {'W2rb':r'\\10.60.100.101','W9rb':r'\\10.80.100.101','GPUrb':r'\\10.90.100.101'}

        #cfg_jsonPath = r'D:\Work\cfg\cfg\task.json'
        #sys_jsonPath = r'D:\Work\cfg\sys_cfg\system.json'

        userID_up =''

        if int(userID[-3:]) >= 500:
            userID_up = str(int(userID) - int(userID[-3:]) + 500)
        else:
            userID_up = str(int(userID) - int(userID[-3:]))

        cfg_jsonPath = os.path.join(platform_address[platform],'render_p','config',userID_up,userID,taskID,'cfg','task.json')
        sys_jsonPath = os.path.join(platform_address[platform],'render_p','config',userID_up,userID,taskID,'sys_cfg','system.json')
        cfg_jsonPath = os.path.normpath(cfg_jsonPath)
        sys_jsonPath = os.path.normpath(sys_jsonPath)
        print (cfg_jsonPath,sys_jsonPath)

        if os.path.exists(cfg_jsonPath) and os.path.exists(sys_jsonPath):

            self.k_cfg_json = json.loads(open(cfg_jsonPath).read())
            self.k_sys_json = json.loads(open(sys_jsonPath).read())

        else:self.k_jsonerror = True



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