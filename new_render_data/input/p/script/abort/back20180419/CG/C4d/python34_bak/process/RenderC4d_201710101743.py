#!/usr/bin/env python
# -*- coding=utf-8 -*-
# Author: kaname
# QQ: 1394041054

import os
import sys
import subprocess
import string
import logging
import time
import shutil
from C4d import C4d
from C4dPluginManager import C4dPlugin, C4dPluginMgr
from CommonUtil import RBCommon as CLASS_COMMON_UTIL

reload(sys)
sys.setdefaultencoding('utf-8')

def get_node(node):
        node=sys.argv[5]
        if "A" in node or "B" in node or "C" in node or "D" in node or "E" in node or "F" in node:
            return "ABCDEF"
        if "K" in node:
            return "K"
        if "L" in node or "M" in node or "N" in node or "O" in node or "P" in node or "Q" in node:
            return "LNOPQ"
        if "G" in node or "H" in node or "J" in node:
            return "GHJ"
        return "ABCDEF"   	

class RenderC4d(C4d):
    def __init__(self,**paramDict):
        C4d.__init__(self,**paramDict)
        self.format_log('RenderC4d.init','start')

        if self.G_TASK_JSON_DICT['scene_info']['common'].has_key('image_size'):
            scene_dict = self.G_TASK_JSON_DICT['scene_info']['common']['image_size']
        elif self.G_TASK_JSON_DICT['scene_info']['common'].has_key('render_format'):
            iformat = self.G_TASK_JSON_DICT['scene_info']['common']['render_format']

        self.G_IMAGE_WIDTH = scene_dict['width']
        self.G_IMAGE_HEIGHT = scene_dict['height']
        self.G_REGULAR_FORMAT = iformat['regular_image_format']
        self.G_MULTIPASS_FORMAT = iformat['multi-pass_format']

        for key,value in self.__dict__.items():
            self.G_DEBUG_LOG.info(key+'='+str(value))

        self.format_log('done','end')

    def check_file(self):
        fileList = self.G_FILELIST.split(",")
        sample_list = []
        for parent, dirnames, filenames in os.walk(self.G_INPUT_PROJECT_PATH):  # 三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
            for filename in filenames:  # 输出文件信息
                sample_list.append(filename)
        existCount = 0
        notExistCount = 0
        for files in fileList:
            isExist = False
            files = files.strip()
            for name in sample_list:
                if files == name:
                    isExist = True
            if isExist:
                self.G_DEBUG_LOG.info(files + '----exists---')
                existCount = existCount + 1
            else:
                self.G_DEBUG_LOG.info(files + '----not exists---')
                notExistCount = notExistCount + 1
        self.G_DEBUG_LOG.info(
            files + '----notExistsCount---' + str(notExistCount) + '----exists----' + str(existCount))
        if notExistCount > 0:
            sys.exit(-1)

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
    	self.format_log('渲染','start')
        self.G_RENDER_LOG.info('[C4D.RBrender.start.....]')

        cg_file_project_path = os.path.basename(self.G_INPUT_PROJECT_PATH)
        print cg_file_project_path

        cg_file_name = os.path.basename(self.G_INPUT_CG_FILE)
        print cg_file_name
        
        cg_file = cg_file_project_path + ':\\' + cg_file_name
        print cg_file

        if self.output_filename == "":
            self.output_filename = os.path.basename(self.G_INPUT_CG_FILE)

        cg_name = self.G_CG_CONFIG_DICT.has_key('cg_name')
        cg_ver = self.G_CG_CONFIG_DICT.has_key('cg_version')
        MyCgVersion = cg_name + cg_ver
        print MyCgVersion
        # if MyCgVersion.endswith('.64') :
        #     MyCgVersion=MyCgVersion.replace('.64','')
        # if MyCgVersion.endswith('.32') :
        #     MyCgVersion=MyCgVersion.replace('.32','')

        self.G_JOB_NAME=self.G_JOB_NAME.encode(sys.getfilesystemencoding())

        output_file = self.G_WORK_RENDER_TASK_OUTPUT.replace("/", "\\") + "\\" + self.output_filename

        # output_renderlog_file =  '"' + self.G_WORK_RENDER_TASK_OUTPUT.replace("/", "\\").replace("work", "log").replace("\output", "") + "\\" + self.G_JOB_NAME + '_render.log"'
        output_renderlog_file = os.path.join(self.G_LOG_RENDER,self.G_TASK_ID,(self.G_JOB_NAME+'_render.log')).replace("/", "\\")
        
        C4dExePath = os.path.join(r'C:\Program Files\MAXON', MyCgVersion, 'CINEMA 4D 64 Bit.exe')

        #Cmds: "C:\Program Files\MAXON\CINEMA 4D R17\CINEMA 4D 64 Bit.exe" -noopengl -nogui -frame 0 0 -render "J:\diyagram_animasyon_2.c4d" -oresolution 1920 1080 -oformat TIFF -oimage "C:\work\render\9577212\output\diyagram_animasyon_2.c4d" >>C:\log\render\9577212\frame0000_render.log
        render_cmd = '"' + C4dExePath + '" -noopengl -nogui  -frame ' + self.G_CG_START_FRAME + ' ' + self.G_CG_END_FRAME + ' -render "' + cg_file.replace("/",
        		"\\") + '" -oresolution ' + self.G_IMAGE_WIDTH + ' ' + self.G_IMAGE_HEIGHT + ' -oformat ' + self.G_REGULAR_FORMAT + ' -oimage "' + output_file + '"'
        if self.multiPass == "":
            render_cmd = render_cmd + ' >>' + output_renderlog_file
        if self.multiPass == "1":
            render_cmd = render_cmd + ' -omultipass "' + output_file + '"' + ' >>' + output_renderlog_file

        self.G_DEBUG_LOG.info("Cmds: %s"%render_cmd)
        
        if self.G_RENDER_OS=='Linux':
            self.RBcmd(render_cmd,True,1,myLog=True)
        else:
            ## ------------------------------------------------------------------------------------
            #os.system(render_cmd)
            TL_result = subprocess.Popen(render_cmd,stdin = subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
            TL_result.stdin.write('3/n')
            TL_result.stdin.write('4/n')
            r_err = ''
            while TL_result.poll()==None:
                r_info = TL_result.stdout.readline().strip()
                if not r_info == "":
                    self.G_DEBUG_LOG.info(r_info)
                    r_err = r_info
            #r_result = TL_result.wait()
            r_code = TL_result.returncode
            #r_err = TL_result.stderr.read()
            self.G_DEBUG_LOG.info("render_cmd return:"+str(r_code))
            if r_code:
                self.G_PROCESS_LOG.info("Error Print :")
                self.G_PROCESS_LOG.info("\n"+r_err+"\n")
        # os.system(render_cmd)
        #self.RBcmd(render_cmd, True, False)
        # endTime = time.time()
        # self.G_FEE_LOG.info('endTime=' + str(int(endTime)))
        self.G_RENDER_LOG.info('[C4D.RBrender.end.....]')
        self.format_log('done','end')


