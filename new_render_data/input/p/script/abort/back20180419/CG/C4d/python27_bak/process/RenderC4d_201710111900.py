#!/usr/bin/env python
# -*- coding=utf-8 -*-
# Author: kaname
# QQ: 1394041054
# DATE:2017-09-15

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

        self.output_filename = ''
        self.multipass = ''

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

    
        print '----------------------cg_file_info------------------------------'

        cg_project_path = os.path.basename(self.G_INPUT_PROJECT_PATH)
        print cg_project_path
        cg_file= self.G_INPUT_CG_FILE[len(self.G_INPUT_PROJECT_PATH):]
        print cg_file + '8888888888888'

        get_cg_file = cg_project_path + ':' + cg_file
        print get_cg_file + '999999999999'

        

        print '----------------------output_filename------------------------------'
        cg_file_name = os.path.basename(self.G_INPUT_CG_FILE)
        get_filename = os.path.splitext(cg_file_name)
        print get_filename
        self.output_filename = get_filename[0]
        print self.output_filename + '5555555555'

        print '-------------------------cg_version---------------------------------'

        if self.G_CG_CONFIG_DICT.has_key('cg_name'):
            cg_name = self.G_CG_CONFIG_DICT['cg_name']

        if self.G_CG_CONFIG_DICT.has_key('cg_version'):
            cg_ver = self.G_CG_CONFIG_DICT['cg_version']

        my_cg_ver = cg_name + ' ' + cg_ver
        print my_cg_ver
        # if my_cg_ver.endswith('.64') :
        #     my_cg_ver=my_cg_ver.replace('.64','')
        # if my_cg_ver.endswith('.32') :
        #     my_cg_ver=my_cg_ver.replace('.32','')

        print '-----------------------scene_info_dict-------------------------------'

        if not self.G_TASK_JSON_DICT.has_key('scene_info'):
            self.G_DEBUG_LOG.info("[ERROR]scene_info undefined...")
            return

        scene_info_common_dict = self.G_TASK_JSON_DICT['scene_info']['common']

        cmd_render_width = scene_info_common_dict['image_size']['width']
        cmd_render_height = scene_info_common_dict['image_size']['height']
        cmd_regular_image_format = scene_info_common_dict['render_format']['regular_image_format']

        cmd_multipass_format = scene_info_common_dict['render_format']['multi-pass_format'] 
        cmd_multipass = scene_info_common_dict['multi_pass']

        #cmd_output_render_format = scene_info_common_dict['render_format']['regular_image_format']

        self.G_JOB_NAME=self.G_JOB_NAME.encode(sys.getfilesystemencoding())


        print '--------------------------render_info----------------------------------'
        output_file = self.G_WORK_RENDER_TASK_OUTPUT.replace("/", "\\") + "\\" + self.output_filename + '.' + str(cmd_regular_image_format)
        print output_file + '4444444444'

        output_renderlog_file = os.path.join(self.G_LOG_WORK +'/' + self.G_TASK_ID + '\\Render_' + self.G_JOB_ID + '_render.log').replace('/', '\\')
        print output_renderlog_file

        c4d_exe = os.path.join(r'"C:\Program Files\MAXON', my_cg_ver, 'CINEMA 4D 64 Bit.exe"') + ' -noopengl -nogui'
        render_frames = ' -frame ' + self.G_CG_START_FRAME + ' ' + self.G_CG_END_FRAME  + ' '+ self.G_CG_BY_FRAME + ' '
        render_option = str(render_frames) + ' -render "' + get_cg_file.replace("/", "\\") + '" -oresolution ' + str(cmd_render_width) \
         + ' ' + str(cmd_render_height) +'  -oformat "' + str(cmd_regular_image_format) + '" -oimage "' + output_file + ' -oMulti-Pass "' \
         + str(cmd_multipass) + '" >>' + output_renderlog_file
        render_cmd = c4d_exe + render_option

        ##"C:\Program Files\MAXON\CINEMA 4D R18\CINEMA 4D 64 Bit.exe" -noopengl -nogui -frame 0 0 1 -render "F:\R18_test.c4d" -oresolution 192 108 -oformat "TGA" -oimage "c:\work\render\111\output\8888.PNG" -omultipass "c:\work\render\111\output\22222.PNG" >>C:\log\render\111\Render_111281_render.log

        #render_cmd = c4d_exe + ' -noopengl -nogui  -frame ' + self.G_CG_START_FRAME + ' ' + self.G_CG_END_FRAME + ' -render "' + cg_file.replace("/", "\\") + '" -oresolution ' + str(cmd_render_width) + ' ' + str(cmd_render_height) + ' -oformat ' + cmd_regular_image_format + ' -oimage "' + output_file + '"'
        #print render_cmd

        # if self.multipass == '':
        #     render_cmd = render_cmd + ' >>' + output_renderlog_file
        # if self.multipass == '1':
        #     render_cmd = render_cmd + ' -oMulti-Pass "' + output_file + '"' + ' >>' + output_renderlog_file

        self.G_DEBUG_LOG.info('Cmd: %s'%render_cmd)
        
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
                self.G_DEBUG_LOG.info("Error Print :")
                self.G_DEBUG_LOG.info("\n"+r_err+"\n")
        # os.system(render_cmd)
        #self.RBcmd(render_cmd, True, False)
        # endTime = time.time()
        # self.G_FEE_LOG.info('endTime=' + str(int(endTime)))
        self.G_RENDER_LOG.info('[C4D.RBrender.end.....]')
        self.format_log('done','end')



