#!/usr/bin/env python
# -*- coding=utf-8 -*-
# Author: kaname
# QQ: 1394041054
# Update:2018-06-10

import os
import sys
import subprocess
import string
import logging
import time
import shutil
import re
from C4d import C4d
from C4dLoader import C4dLoader
from C4dPluginManager import C4dPlugin, C4dPluginMgr
from CommonUtil import RBCommon as CLASS_COMMON_UTIL
from C4dUtil import RBC4dUtil as CLASS_C4D_UTIL


class RenderC4d(C4d):
    def __init__(self,**paramDict):
        C4d.__init__(self,**paramDict)
        self.format_log('RenderC4d.init','start')

        self.output_filename = ''
        self.multipass = ''
        self.output_avi_movie = []
        
        for key,value in list(self.__dict__.items()):
            self.G_DEBUG_LOG.info(key+'='+str(value))

        self.format_log('done','end')

    '''
    def RB_MAP_DRIVE(self):#2.chongxie
        self.format_log('[映射盘符]','[start]')
        self.G_DEBUG_LOG.info('[c4d.RB_MAP_DRIVE.start.....]')
        
        if self.G_RENDER_OS != '0':
            #delete all mappings
            CLASS_COMMON_UTIL.del_net_use()
            CLASS_COMMON_UTIL.del_subst()
            
            #net use
            b_flag = False
            if self.G_CG_NAME == 'C4d':
                map_root = os.path.basename(self.G_INPUT_PROJECT_PATH)
                print(map_root + '@KANADAmmmmmm')
                map_dict = os.path.join(self.G_INPUT_PROJECT_PATH)
                print(map_root + '@@KANADAnnnnnn')
                map_cmd = 'net use %s: "%s"' % (map_root, map_dict)
                CLASS_COMMON_UTIL.cmd_python3(map_cmd,my_log=self.G_DEBUG_LOG)

            # #base RB_MAP_DRIVE
            # if self.G_CG_NAME != 'Max' and self.G_TASK_JSON_DICT['system_info'].has_key('mnt_map'):
            #     map_dict = self.G_TASK_JSON_DICT['system_info']['mnt_map']
            #     for key,value in map_dict.items():
            #         value = os.path.normpath(value)
            #         map_cmd = 'net use "%s" "%s"' % (key,value)
            #         CLASS_COMMON_UTIL.cmd_python3(map_cmd,my_log=self.G_DEBUG_LOG)
            #         if key.lower() == 'b:':
            #             b_flag = True

            if not b_flag:
                map_cmd_b = 'net use B: "%s"' % (os.path.normpath(self.G_PLUGIN_PATH))
                CLASS_COMMON_UTIL.cmd(map_cmd_b,my_log=self.G_DEBUG_LOG,try_count=3)

        self.G_DEBUG_LOG.info('[c4d.RB_MAP_DRIVE.end.....]')
        self.format_log('done','end')
    '''

    def RB_CONFIG(self):

        self.G_DEBUG_LOG.info('[c4d.render.配置插件开始]')
        self.G_DEBUG_LOG.info('[c4d.render.plugin.config.start......]')
        self.plugin_config()
        self.G_DEBUG_LOG.info('[c4d.render.配置插件完成]')
        self.G_DEBUG_LOG.info('[c4d.render.plugin.config.end......]')       
    
    
    def c4d_cmd_callback(self, my_popen, my_log):
        while my_popen.poll()==None:
            render_info = my_popen.stdout.readline().strip()
            if render_info == "":
                continue
            CLASS_COMMON_UTIL.log_print(my_log, render_info)
     
            if '[Rendering successful:]' in str(render_info):
                CLASS_C4D_UTIL.kill_c4d(my_popen.pid, my_log)
                CLASS_COMMON_UTIL.log_print(my_log,
                                            '\n\n-------------------------------------------End c4d program-------------------------------------------\n\n')
                break
            
    def render_c4d(self):
        pass

        
    def RB_RENDER(self):
        self.format_log('render','start')
        self.format_log('开始渲染','start')
        #start...
        self.G_RENDER_LOG.info('[c4d.RBrender.start.....]')

        #print ('--------------------remove_pyp_script----------------------------')
        
        self.G_DEBUG_LOG.info('[c4d.remove pyp.start.....]')
        
        cgv = self.G_CG_VERSION  # "CINEMA 4D R19"
        C4dLoader.remove_pyp_script(cgv)


        self.G_DEBUG_LOG.info('[c4d.remove pyp.end.....]')


        print ('----------------------cg_file_info------------------------------')
        map_dict = self.G_TASK_JSON_DICT['mnt_map']  # use "/"
        map_dict_reverse = dict(zip(map_dict.values(), map_dict.keys()))
        print('map_dict_reverse: %s' % map_dict_reverse)
        
        # G_INPUT_CG_FILE: os.path.normpath(r'//10.60.100.104/stg_data/input/d/inputdata5/10000000/10000085/c4d/R17_test_ch.c4d')
        # G_INPUT_USER_PATH: os.path.normpath(r'//10.60.100.104/stg_data/input/d/inputdata5/10000000/10000085')
        
        input_cg_file_second_half = self.G_INPUT_CG_FILE[len(self.G_INPUT_USER_PATH):]  # \E\test\C4DR17_Vray19_test\Vray_C4DR17_vray19.c4d
        print('input_cg_file_second_half: ' + input_cg_file_second_half)
        index = input_cg_file_second_half.find(os.sep, 1)  # index begin position:1
        input_cg_file_second_half_front = input_cg_file_second_half[:index]  # \E
        input_cg_file_second_half_behind = input_cg_file_second_half[index:]  # \test\C4DR17_Vray19_test\Vray_C4DR17_vray19.c4d
        print('input_cg_file_second_half_behind: ' + input_cg_file_second_half_behind)

        key = self.G_INPUT_USER_PATH + input_cg_file_second_half_front  # \\10.60.100.104\stg_data\input\d\inputdata5\10000000\10000085\E
        driver = map_dict_reverse.get(key.replace('\\', '/'))  # E:
        print('driver: %s' % driver)

        get_cg_file = driver + input_cg_file_second_half_behind  # local cg file path
        print(get_cg_file + '[.@KANADA999999999999]')

        
        print ('-------------------------cg_version---------------------------------')

        if 'cg_name' in self.G_CG_CONFIG_DICT:
            cg_name = self.G_CG_CONFIG_DICT['cg_name']

        if 'cg_version' in self.G_CG_CONFIG_DICT:
            cg_ver = self.G_CG_CONFIG_DICT['cg_version']


        my_cg_ver = cg_name + ' ' + cg_ver
        print (my_cg_ver)
        # if my_cg_ver.endswith('.64') :
        #     my_cg_ver=my_cg_ver.replace('.64','')
        # if my_cg_ver.endswith('.32') :
        #     my_cg_ver=my_cg_ver.replace('.32','')

        print ('-----------------------scene_info_render-------------------------------')

        if 'scene_info_render' not in self.G_TASK_JSON_DICT:
            self.G_DEBUG_LOG.info("[ERROR]scene_info_render undefined...")
            return

        scene_info_render_common_dict = self.G_TASK_JSON_DICT['scene_info_render']['common']

        cmd_render_width = scene_info_render_common_dict['width']
        cmd_render_height = scene_info_render_common_dict['height']
        cmd_regular_image_format = scene_info_render_common_dict['regular_image_format']
        cmd_multipass_format = scene_info_render_common_dict['multi_pass_format'] 
        cmd_multipass_path = scene_info_render_common_dict['multipass_saveimage_path']
        cmd_multipass_enabled= scene_info_render_common_dict['multipass_save_enabled']
        cmd_regular_image_saveimage_path= scene_info_render_common_dict['regular_image_saveimage_path']
        
        print ('----------------------output_filename------------------------------')
        
        if cmd_regular_image_saveimage_path is None:
            cg_file_name = os.path.basename(self.G_INPUT_CG_FILE)
            get_filename = os.path.splitext(cg_file_name)
            cmd_regular_image_saveimage_path = get_filename[0]
            print((cmd_regular_image_saveimage_path + '[.@KANADA5555555555]'))
        
        
        self.G_JOB_NAME=self.G_JOB_NAME.encode(sys.getfilesystemencoding())

        print ('--------------------------render_info----------------------------------')
        
        start_time = int(time.time())
        self.G_FEE_PARSER.set('render', 'start_time', str(start_time))
        
        if self.g_one_machine_multiframe == None or self.g_one_machine_multiframe == False:
            #C:\work\render\65368\output\0001.jpg
            output_file = self.G_WORK_RENDER_TASK_OUTPUT.replace("/", "\\") + "\\" + cmd_regular_image_saveimage_path + '.' + str(cmd_regular_image_format)
            print(output_file + '4444444444')

            output_renderlog_file = os.path.join(self.G_LOG_WORK +'/' + self.G_TASK_ID + '\\Render_' + self.G_JOB_ID + '_render.log').replace('/', '\\')
            print (output_renderlog_file)
            
            # cmd
            c4d_exe = os.path.join(r'"C:\Program Files\MAXON', my_cg_ver, 'CINEMA 4D 64 Bit.exe"') + ' -noopengl -nogui'
            user_id = ' ' + str(self.G_USER_ID)
            task_id = ' ' + str(self.G_TASK_ID) + ' '
            render_frames = ' -frame ' + self.G_CG_START_FRAME + ' ' + self.G_CG_END_FRAME  + ' '+ self.G_CG_BY_FRAME + ' '
            
            render_option = ''
            if cmd_multipass_enabled == "0" or cmd_multipass_path == None or cmd_multipass_path == "":
                render_option = render_frames + ' -render "' + get_cg_file.replace("/", "\\") + '" -oresolution "' + str(cmd_render_width) \
                            + '" "' + str(cmd_render_height) +'" -oformat "' + str(cmd_regular_image_format) + '" -oimage "' + output_file + '"'
                print('render_option1: %s'%render_option)
            else:
                render_option = render_frames + ' -render "' + get_cg_file.replace("/", "\\") + '" -oresolution "' + str(cmd_render_width) \
                            + '" "' + str(cmd_render_height) +'" -oformat "' + str(cmd_regular_image_format) + '" -oimage "' + output_file + '" -omultipass "' + output_file + '" '
                print('render_option2: %s'%render_option)

            render_cmd = c4d_exe + user_id + task_id + render_option
            #print("Cmds: %s" % render_cmd)
            self.G_RENDER_LOG.info("Cmds: %s" % render_cmd)
            
            self.G_DEBUG_LOG.info('[.@KANADA]')
            # 渲染开始时间
            render_start_time = int(time.time())
            
            if self.G_RENDER_OS=='Linux':
                self.RBcmd(render_cmd, True, 1, myLog=True)
            else:
                print ('\n\n---------------------------------------Start c4d program---------------------------------\n\n')
                CLASS_COMMON_UTIL.cmd(render_cmd,my_log=self.G_RENDER_LOG,continue_on_error=True,my_shell=True,callback_func=self.c4d_cmd_callback)

            # 渲染结束时间
            render_end_time = int(time.time())
            self.render_record[render_frames] = {'start_time': render_start_time,'end_time': render_end_time}
            
        elif self.g_one_machine_multiframe == True:
            render_frame_list = CLASS_COMMON_UTIL.need_render_from_frame(self.G_CG_FRAMES)
            for frame in render_frame_list:
                print("current rendering frame: %s" % frame)
                #C:\work\render\65368\output\0001\0001.jpg
                output_file = self.G_WORK_RENDER_TASK_OUTPUT.replace("/", "\\") + "\\" + frame.zfill(4) +"\\" + cmd_regular_image_saveimage_path + '.' + str(cmd_regular_image_format)
                print(output_file + '4444444444')
                # cmd
                c4d_exe = os.path.join(r'"C:\Program Files\MAXON', my_cg_ver, 'CINEMA 4D 64 Bit.exe"') + ' -noopengl -nogui'
                user_id = ' ' + str(self.G_USER_ID)
                task_id = ' ' + str(self.G_TASK_ID) + ' '
                render_frames = ' -frame ' + frame + ' ' + frame  + ' 1 '
                render_option = ''
                if cmd_multipass_enabled == "0" and cmd_multipass_path == None:
                    render_option = render_frames + ' -render "' + get_cg_file.replace("/", "\\") + '" -oresolution "' + str(cmd_render_width) \
                            + '" "' + str(cmd_render_height) +'" -oformat "' + str(cmd_regular_image_format) + '" -oimage "' + output_file + '"'
                    print('render_option1: %s'%render_option)
                else:
                    render_option = render_frames + ' -render "' + get_cg_file.replace("/", "\\") + '" -oresolution "' + str(cmd_render_width) \
                            + '" "' + str(cmd_render_height) +'" -oformat "' + str(cmd_regular_image_format) + '" -oimage "' + output_file + '" -omultipass "' + output_file + '" '
                    print('render_option2: %s'%render_option)

                render_cmd = c4d_exe + user_id + task_id + render_option
                #print("Cmds: %s" % render_cmd)
                self.G_RENDER_LOG.info("Cmds: %s" % render_cmd)
                
                self.G_DEBUG_LOG.info('[.@KANADA]')
                # 渲染开始时间
                render_start_time = int(time.time())

                
                if self.G_RENDER_OS == 'Linux':
                    self.RBcmd(render_cmd, True, 1, myLog=True)
                else:
                    print ('\n\n---------------------------------------Start c4d program---------------------------------\n\n')
                    CLASS_COMMON_UTIL.cmd(render_cmd,my_log=self.G_DEBUG_LOG,continue_on_error=True,my_shell=True,callback_func=self.c4d_cmd_callback)

                CLASS_COMMON_UTIL.log_print(self.G_DEBUG_LOG, ("current rendering frame: ", frame))
                # 渲染结束时间
                render_end_time = int(time.time())
                self.render_record[frame] = {'start_time': render_start_time,'end_time': render_end_time}
                
                
                self.multiframe_complete_list.append(frame)
            
            #self.G_RENDER_LOG.info('[一机多帧暂时不支持...]')
            #self.G_DEBUG_LOG.info('[一机多帧暂时不支持...]')
        
        end_time = int(time.time())
        self.G_FEE_PARSER.set('render', 'end_time', str(end_time))
        
        self.G_RENDER_LOG.info('[C4D.RBrender.end.....]')
        #end...
        os.system(r'wmic process where name="rlm.exe" delete')
        os.system(r'wmic process where name="rlm_c4dtoa.exe" delete')
        
        self.format_log('done','end')
        self.format_log('结束渲染','end')

    