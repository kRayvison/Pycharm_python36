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
from C4dLoader import C4dLoader
from C4dPluginManager import C4dPlugin, C4dPluginMgr
from CommonUtil import RBCommon as CLASS_COMMON_UTIL
from C4dUtil import RBC4dUtil as CLASS_C4D_UTIL

reload(sys)
sys.setdefaultencoding('utf-8')


class RenderC4d(C4d):
    def __init__(self,**paramDict):
        C4d.__init__(self,**paramDict)
        self.format_log('RenderC4d.init','start')

        self.output_filename = ''
        self.multipass = ''

        for key,value in self.__dict__.items():
            self.G_DEBUG_LOG.info(key+'='+str(value))

        self.format_log('done','end')

    def RB_CONFIG(self):
        self.G_DEBUG_LOG.info('[.hldoing]')
        self.G_DEBUG_LOG.info('[.配置插件开始]')
        self.G_DEBUG_LOG.info('[C4d.Plugin.config.begin......]')
        
        self.plugin_config()
        self.G_DEBUG_LOG.info('[.hldone]')
        self.G_DEBUG_LOG.info('[.配置插件完成]')
        self.G_DEBUG_LOG.info('[C4d.Plugin.config.end......]')         

    def RB_RENDER(self):
        self.format_log('render','start')
    	self.format_log('开始渲染','start')
        
        self.G_RENDER_LOG.info('[C4D.RBrender.start.....]')

        print '--------------------remove_pyp_script----------------------------'
        
        self.G_DEBUG_LOG.info('[C4D.remove pyp.start.....]')
        
        cgv = self.G_CG_VERSION
        C4dLoader.remove_pyp_script(cgv)

        print '--------------------remove_pyp_script----------------------------'

        self.G_DEBUG_LOG.info('[C4D.remove pyp.end.....]')


        print '----------------------cg_file_info------------------------------'

        cg_project_path = os.path.basename(self.G_INPUT_PROJECT_PATH)
        print cg_project_path
        cg_file = self.G_INPUT_CG_FILE[len(self.G_INPUT_PROJECT_PATH):]
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
         + str(cmd_multipass) + '"'
        
        render_cmd = c4d_exe + render_option

        ##"C:\Program Files\MAXON\CINEMA 4D R18\CINEMA 4D 64 Bit.exe" -noopengl -nogui -frame 0 0 1 -render "F:\R18_test.c4d" -oresolution 192 108 -oformat "TGA" -oimage "c:\work\render\111\output\8888.PNG" -omultipass "c:\work\render\111\output\22222.PNG" >>C:\log\render\111\Render_111281_render.log

        #render_cmd = c4d_exe + ' -noopengl -nogui  -frame ' + self.G_CG_START_FRAME + ' ' + self.G_CG_END_FRAME + ' -render "' + cg_file.replace("/", "\\") + '" -oresolution ' + str(cmd_render_width) + ' ' + str(cmd_render_height) + ' -oformat ' + cmd_regular_image_format + ' -oimage "' + output_file + '"'
        #print render_cmd

        # if self.multipass == '':
        #     render_cmd = render_cmd + ' >>' + output_renderlog_file
        # if self.multipass == '1':
        #     render_cmd = render_cmd + ' -oMulti-Pass "' + output_file + '"' + ' >>' + output_renderlog_file
       
        #self.G_DEBUG_LOG.info('Cmd: %s' % render_cmd)
        self.G_DEBUG_LOG.info('[.HL]')
        # self.G_KAFKA_MESSAGE_DICT['startTime']=str(int(time.time()))
        self.G_FEE_PARSER.set('render','start_time',str(int(time.time())))

        if self.G_RENDER_OS=='Linux':
            self.RBcmd(render_cmd, True, 1, myLog=True)
        else:

            print '---------------------------------------Start c4d program---------------------------------'
        
            CLASS_COMMON_UTIL.cmd(render_cmd,my_log=self.G_DEBUG_LOG,continue_on_error=True,my_shell=True,callback_func=self.c4d_cmd_callback)
            

        # self.G_KAFKA_MESSAGE_DICT['endTime']=str(int(time.time()))
        self.G_FEE_PARSER.set('render','end_time',str(int(time.time())))

        self.G_RENDER_LOG.info('[C4D.RBrender.end.....]')
        self.format_log('done','end')
        self.format_log('结束渲染','end')

    def c4d_cmd_callback(self,my_popen,my_log):
        while my_popen.poll()==None:
            render_info = my_popen.stdout.readline().strip()
            if render_info == "":
                continue
            self.G_RENDER_LOG.info(render_info)