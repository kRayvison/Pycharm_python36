#!/usr/bin/env python
#encoding:utf-8
# -*- coding: utf-8 -*-
import logging
import os
import sys
import subprocess
import string
import time
import shutil
import codecs
import configparser
import threading
import time
import json
import socket
import re
import math
import multiprocessing
from imp import reload
reload(sys)
# sys.setdefaultencoding('utf-8')
from Maya import Maya
from MayaPlugin import MayaPlugin                             

from CommonUtil import RBCommon as CLASS_COMMON_UTIL
from MayaUtil import RBMayaUtil as CLASS_MAYA_UTIL
from MayaUtil import NukeMerge

class RenderMaya(Maya):
    def __init__(self,**paramDict):
        Maya.__init__(self,**paramDict)
        self.format_log('RenderMaya.init','start')
        for key,value in self.__dict__.items():
            self.G_DEBUG_LOG.info(key+'='+str(value))
        self.format_log('done','end')
               
        self.G_CUSTOM_CONFIG_NAME ='CustomConfig.py'
        self.G_PRE_NAME ='Pre.py'
        self.G_POST_NAME ='Post.py'
        self.G_PRERENDER_NAME ='Render.py'
        self.G_POSTRENDER_NAME = 'PostRender.py'
        self.CG_PLUGINS_DICT = self.G_CG_CONFIG_DICT['plugins']
        self.CG_NAME =self.G_CG_CONFIG_DICT['cg_name']
        self.CG_VERSION =self.G_CG_CONFIG_DICT['cg_version']
        self.ENABLE_LAYERED = self.G_TASK_JSON_DICT['scene_info_render']['enable_layered']
        self.TEMP_PATH = self.G_TASK_JSON_DICT['system_info']['common']['temp_path']
        if self.G_CG_TILE_COUNT == self.G_CG_TILE:
            self.IMAGE_MERGE_FRAME = "1"
        else:
            self.IMAGE_MERGE_FRAME = "0"
        # --------------一机多帧----------------------
        if "G_RENDER_MUL_NUM" in paramDict:  # 主图有此键
            if self.G_RENDER_MUL_NUM == "1":
                self.g_one_machine_multiframe = "1"
            elif self.G_RENDER_MUL_NUM == "0":
                self.g_one_machine_multiframe = "0"
        else:
            self.g_one_machine_multiframe = "0"

        # 完成队列
        self.multiframe_complete_list = []
        self.monitor_complete_thread = None
        # 记录文件
        self.render_record_json = os.path.join(self.G_WORK_RENDER_TASK_MULTIFRAME, "{task_id}_{munu_task_id}_{munu_job_id}_{frames}".format(
            munu_task_id=self.G_MUNU_ID,
            munu_job_id=self.G_JOB_ID,
            task_id=self.G_TASK_ID,
            frames=self.G_CG_FRAMES,
        ))
        # --------------------------------------------
        self.render_record = {}

        # self.MAYA_BASE_RENDER_CMD = ''
        # self.MAYA_FINAL_RENDER_CMD = ''



    def maya_cmd_callback(self, my_popen, my_log):
        while my_popen.poll() is None:
            result_line = my_popen.stdout.readline().strip()
            result_line = result_line.decode('utf-8')
            if result_line == '':
                continue
            CLASS_COMMON_UTIL.log_print(my_log, result_line)

            if '[_____render end_____]' in result_line:  # [_____render end_____][1]
                frame = re.search('\[(\d+)\]', result_line).group(1)
                self.multiframe_complete_list.append(frame)
                end_time = int(time.time())
                self.render_record[frame]['end_time'] = end_time
                self.render_record[str(int(frame) + 1)] = {'start_time': end_time, 'end_time': -1}


    def RB_CONFIG(self):
        self.G_DEBUG_LOG.info('[Maya.RBconfig.start.....]')
        if self.G_CG_TILE_COUNT != self.G_CG_TILE:
            print("----------------------------------------loading plugins start ------------------------------------------")
            #kill maya
            CLASS_MAYA_UTIL.killMayabatch(self.G_DEBUG_LOG)  #kill mayabatch.exe
            # ----------------set env  -------------------
            os.environ["MAYA_UI_LANGUAGE"] = "en_US"
            os.environ['MAYA_DISABLE_CIP'] = '1'
            os.environ['MAYA_DISABLE_CLIC_IPM'] = '1'
            os.environ['MAYA_DISABLE_CER'] = '1'
            if int(self.CG_VERSION)>=2016:
                os.environ['MAYA_OPENCL_IGNORE_DRIVER_VERSION'] = '1'
                os.environ['MAYA_VP2_DEVICE_OVERRIDE'] = 'VirtualDeviceDx11'
            if int(self.RENDER_LAYER_TYPE):
                os.environ['MAYA_ENABLE_LEGACY_RENDER_LAYERS'] = "0"
            else:
                os.environ['MAYA_ENABLE_LEGACY_RENDER_LAYERS'] = "1"
            # ----------------load maya plugin-------------------
            self.G_DEBUG_LOG.info('插件配置')
            if self.G_CG_CONFIG_DICT:
                sys.stdout.flush()
                custom_config = os.path.join(self.G_NODE_MAYAFUNCTION,self.G_CUSTOM_CONFIG_NAME).replace('\\','/')
                if self.G_NODE_MAYAFUNCTION:
                    if os.path.exists(custom_config):
                        sys.stdout.flush()
                        print("custom_config is: " + custom_config)
                        sys.stdout.flush()
                    else:
                        print("Can not find the CustomConfig file: %s." % custom_config)
                print("plugin path:")
                print(self.G_CG_CONFIG_DICT)
                sys.stdout.flush()
                maya_plugin = MayaPlugin(self.G_CG_CONFIG_DICT,[custom_config],self.G_USER_ID,self.G_TASK_ID,self.G_DEBUG_LOG)
                maya_plugin.config()
                sys.stdout.flush()
            print("----------------------------------------loading plugins end ------------------------------------------")
            self.G_DEBUG_LOG.info('[Maya.RBconfig.end.....]')

            # #------------get render cmd----------
            self.MAYA_FINAL_RENDER_CMD = self.get_render_cmd()
            self.G_DEBUG_LOG.info(self.MAYA_FINAL_RENDER_CMD)
        else:
            self.G_DEBUG_LOG.info("[RenderNuke  Comp...........................]")
        self.G_DEBUG_LOG.info('[RenderMaya.RB_CONFIG.end.....]')
        self.format_log('done','end')        
        

    def RB_PRE_PY(self):#1
    
        self.format_log('执行自定义PY脚本','start')
        self.G_DEBUG_LOG.info('[BASE.RB_PRE_PY.start.....]')
        self.G_DEBUG_LOG.info(u'如果以下自定义PY脚本存在，会执行此脚本')
        pre_py=os.path.join(self.G_NODE_PY,'CG',self.G_CG_NAME,'function','pre.py')
        self.G_DEBUG_LOG.info(pre_py)
        if os.path.exists(pre_py):
            import pre as PRE_PY_MODEL
            self.PRE_DICT=PRE_PY_MODEL.main()
        self.G_DEBUG_LOG.info('[BASE.RB_PRE_PY.end.....]')
        self.format_log('done','end')        
        
        
    '''
        渲染
    '''
    def RB_RENDER(self):#5    
    
        self.format_log('渲染','start')
        if int(self.G_CG_TILE_COUNT) != int(self.G_CG_TILE):
            self.G_DEBUG_LOG.info('[RenderMaya.RB_RENDER.start.....]')
            # if self.PRE_DICT == None:
                # render_cmd = self.MAYA_FINAL_RENDER_CMD

            # elif self.PRE_DICT['RENDER_CMD']:
                # render_cmd = self.PRE_DICT['RENDER_CMD']
                # print ("The custom render cmd: ")
                # print (render_cmd)

            # else:
                # render_cmd = self.MAYA_FINAL_RENDER_CMD


            # 是否一机多帧
            if self.g_one_machine_multiframe is True:
                if int(self.G_RECOMMIT_FLAG) > 0:
                    cmd = r'c:\fcopy\FastCopy.exe /cmd=force_copy /speed=full /force_close /no_confirm_stop /force_start "{}" /to="{}"'.format(
                        os.path.join(self.G_REMOTE_TASK_CFG, self.render_record_json),
                        self.G_WORK_RENDER_TASK_MULTIFRAME,
                    )
                    CLASS_COMMON_UTIL.cmd(cmd, my_log=self.G_DEBUG_LOG)
                # 监控线程
                frames = self.remain_frames()
                render_list = CLASS_COMMON_UTIL.need_render_from_frame(frames)
                t = threading.Thread(target=self.loop_handle_complete, args=(render_list,))
                t.start()
                self.monitor_complete_thread = t

            # ------------get render cmd----------
            render_cmd = self.MAYA_FINAL_RENDER_CMD
            sys.stdout.flush()
            self.G_DEBUG_LOG.info(render_cmd)
            start_time = int(time.time())
            if self.g_one_machine_multiframe is True:
                self.render_record.update({frames[0]: {'start_time': start_time, 'end_time': 0}})
                pass
            self.G_FEE_PARSER.set('render', 'start_time', str(start_time))

            self.G_DEBUG_LOG.info(
                "\n\n-------------------------------------------Start maya program-------------------------------------\n\n")
            result_code, _ = CLASS_COMMON_UTIL.cmd(render_cmd, my_log=self.G_DEBUG_LOG, continue_on_error=True, my_shell=True,
                                  callback_func=self.maya_cmd_callback)

            self.cg_return_code = result_code
            end_time = int(time.time())
            self.G_FEE_PARSER.set('render', 'end_time', str(end_time))

            CLASS_MAYA_UTIL.kill_lic_all(my_log=self.G_DEBUG_LOG)
            self.G_FEE_PARSER.set('render', 'end_time', str(end_time))
            self.G_DEBUG_LOG.info('[RenderMaya.RB_RENDER.end.....]')

        else:
            self.G_DEBUG_LOG.info('[RenderNuke.RB_RENDER.start.....]')
            self.G_FEE_PARSER.set('render','start_time',str(int(time.time())))
            options = {}
            options["func_path"] = self.G_NODE_MAYAFUNCTION
            options["tiles"] = int(self.G_CG_TILE_COUNT)
            options["tile_index"] = int(self.G_CG_TILE)
            options["width"] = int(self.G_TASK_JSON_DICT['scene_info_render'][self.G_CG_LAYER_NAME]['common']['width'])
            options["height"] = int(self.G_TASK_JSON_DICT['scene_info_render'][self.G_CG_LAYER_NAME]['common']['height'])
            options["output"] = self.G_WORK_RENDER_TASK_OUTPUT
            options["g_tiles_path"] = self.G_TILES_PATH
            options["g_task_id"] = self.G_TASK_ID
            options["g_cg_start_frame"] = self.G_CG_START_FRAME
            print (options)
            nuke_merge = NukeMerge(options)
            nuke_merge.render(self.G_DEBUG_LOG)
            CLASS_MAYA_UTIL.kill_lic_all(my_log=self.G_DEBUG_LOG)
            self.G_FEE_PARSER.set('render','end_time',str(int(time.time())))
            self.G_DEBUG_LOG.info('[RenderNuke.RB_RENDER.end.....]')

        self.format_log('done', 'end')


        # #------------render--------------------------
        # render_cmd = render_cmd.encode(sys.getfilesystemencoding())
        # self.G_FEE_PARSER.set('render','start_time',str(int(time.time())))
        # self.G_DEBUG_LOG.info("\n\n-------------------------------------------Start maya program-------------------------------------\n\n")
        # print ("render cmd info:")
        # print (render_cmd)
        # CLASS_COMMON_UTIL.cmd(render_cmd,my_log=self.G_DEBUG_LOG,continue_on_error=True,my_shell=True)
        # sys.stdout.flush()
        # CLASS_MAYA_UTIL.kill_lic_all(my_log=self.G_DEBUG_LOG)
        # #----------clear  all--------------------
        #
        # self.G_FEE_PARSER.set('render','end_time',str(int(time.time())))
        # self.G_DEBUG_LOG.info('[RenderMaya.RB_RENDER.end.....]')
        # self.format_log('done','end')
        # 

    def handle_file(self, frame):
        """result_action 的复制版, 去掉了帧检查"""
        self.G_DEBUG_LOG.info('[Maya.result_action.start.....]')
        output = self.G_OUTPUT_USER_PATH
        if not os.path.exists(output):
            os.makedirs(output)

        frame = frame.zfill(4)
        if self.G_CG_TILE_COUNT != '1' and self.G_CG_TILE_COUNT != self.G_CG_TILE:
            output = self.G_TILES_PATH

        cmd1 = '{fcopy_path} /speed=full /force_close /no_confirm_stop /force_start "{source}" /to="{destination}"'.format(
            fcopy_path='c:\\fcopy\\FastCopy.exe',
            source=os.path.join(self.G_WORK_RENDER_TASK_OUTPUT.replace('/', '\\'), frame),
            destination=output.replace('/', '\\'),
        )

        cmd3 = '{fcopy_path} /speed=full /cmd=move /force_close /no_confirm_stop /force_start "{source}" /to="{destination}"'.format(
            fcopy_path='c:\\fcopy\\FastCopy.exe',
            source=os.path.join(self.G_WORK_RENDER_TASK_OUTPUT.replace('/', '\\'), frame),
            destination=self.G_WORK_RENDER_TASK_OUTPUTBAK.replace('/', '\\'),
        )
        CLASS_COMMON_UTIL.cmd(cmd1, my_log=self.G_DEBUG_LOG, try_count=3, continue_on_error=True)
        CLASS_COMMON_UTIL.cmd(cmd3, my_log=self.G_DEBUG_LOG, try_count=3, continue_on_error=True)
        self.G_DEBUG_LOG.info('[Max.result_action.end.....]')



    def get_region(self, tiles, tile_index, width, height):
        n = int(math.sqrt(tiles))
        for i in sorted(range(2, n + 1), reverse=1):
            if tiles % i != 0:
                continue
            else:
                n = i
                break
        n3 = tiles / n
        n1 = tile_index / n3
        n2 = tile_index % n3

        top = height / n * (n1 + 1)
        left = width / n3 * n2
        bottom = height / n * n1
        right = width / n3 * (n2 + 1)
        if right == width:
            right -= 1
        if top == height:
            top -= 1
        return int(left), int(right), int(bottom), int(top)

    def get_render_cmd(self):
        self.renderSettings = {}
        self.mappings = {}
        render_cmd = ''                 

        if self.G_RENDER_OS== '0':
            if float(self.CG_VERSION) < 2016:
                version_name = "%s-x64" % (self.CG_VERSION)
            else:
                version_name = self.CG_VERSION
            self.renderSettings["render.exe"] = "/usr/autodesk/" \
                "maya%s/bin/Render" % (version_name)
            self.renderSettings["mayabatch.exe"] = "/usr/autodesk/" \
                "maya%s/bin/maya -batch" % (version_name)
        self.renderSettings["render.exe"] = "C:/Program Files/Autodesk/" \
            "maya%s/bin/render.exe" % (self.CG_VERSION)
        self.renderSettings["output"] = os.path.normpath(self.G_WORK_RENDER_TASK_OUTPUT).replace("\\","/")

        # 一机多帧
        self.renderSettings["g_one_machine_multiframe"] = self.g_one_machine_multiframe
        if self.g_one_machine_multiframe is True:
            self.renderSettings["output"] = os.path.join(os.path.normpath(self.G_WORK_RENDER_TASK_OUTPUT),"temp_out").replace("\\","/")
        self.renderSettings["output_frame"] = os.path.normpath(self.G_WORK_RENDER_TASK_OUTPUT).replace("\\","/")


        if not os.path.exists(self.renderSettings["output"]):
            os.makedirs(self.renderSettings["output"])



        print (self.renderSettings["output"])
        print (self.renderSettings["output_frame"])


        self.renderSettings["tile_region"] = ""
        self.renderSettings["tiles"] = int(self.G_CG_TILE_COUNT)
        self.renderSettings["tile_index"] = int(self.G_CG_TILE)
        # -----------render tiles------------
        if self.renderSettings["tiles"] > 1:
            tile_region = self.get_region(int(self.G_CG_TILE_COUNT),
                                          int(self.G_CG_TILE),
                                          int(self.G_TASK_JSON_DICT['scene_info_render'][self.G_CG_LAYER_NAME]['common']['width']),
                                          int(self.G_TASK_JSON_DICT['scene_info_render'][self.G_CG_LAYER_NAME]['common']['height']))
            self.renderSettings["tile_region"] = " ".join([str(i) for i in tile_region])

            self.renderSettings["output"] = "%s/%s/%s/" % \
                (os.path.normpath(self.G_WORK_RENDER_TASK_OUTPUT).replace("\\", "/"),self.G_CG_START_FRAME,
                 self.renderSettings["tile_index"])
            self.renderSettings["output"] = os.path.normpath(self.renderSettings["output"])
            if not os.path.exists(self.renderSettings["output"]):
                os.makedirs(self.renderSettings["output"])

        self.G_RN_MAYA_PRERENDER  = os.path.join(self.G_NODE_MAYASCRIPT,self.G_PRERENDER_NAME).replace('\\','/')
        self.G_RN_MAYA_POSTRENDER = os.path.join(self.G_NODE_MAYASCRIPT,self.G_POSTRENDER_NAME).replace('\\', '/')
    
        if self.G_INPUT_PROJECT_PATH:
            if os.path.exists(self.G_INPUT_PROJECT_PATH):
                os.chdir(self.G_INPUT_PROJECT_PATH)

        self.renderSettings["maya_file"] = os.path.normpath(self.G_INPUT_CG_FILE)
        self.renderSettings["start"] = self.G_CG_START_FRAME
        self.renderSettings["end"] = self.G_CG_END_FRAME
        self.renderSettings["by"] = self.G_CG_BY_FRAME
                
        self.renderSettings["renderableCamera"] = self.G_CG_OPTION
        self.renderSettings["renderableLayer"] = self.G_CG_LAYER_NAME
        self.renderSettings["projectPath"] = os.path.normpath(self.G_INPUT_PROJECT_PATH)
        self.renderSettings["renderType"] = "render.exe"
        if self.ENABLE_LAYERED == "1":
            self.renderSettings["width"] = int(self.G_TASK_JSON_DICT['scene_info_render'][self.G_CG_LAYER_NAME]['common']['width'])
            self.renderSettings["height"] = int(self.G_TASK_JSON_DICT['scene_info_render'][self.G_CG_LAYER_NAME]['common']['height'])
        else:
            self.renderSettings["width"] = int(self.G_TASK_JSON_DICT['scene_info_render']['defaultRenderLayer']['common']['width'])
            self.renderSettings["height"] = int(self.G_TASK_JSON_DICT['scene_info_render']['defaultRenderLayer']['common']['height'])

        #"-----------------------------cmd--------------------------------"
        cmd = "\"%(render.exe)s\" -s %(start)s -e %(end)s -b %(by)s " \
            "-proj \"%(projectPath)s\" -rd \"%(output)s\"" \
            % self.renderSettings
        if self.G_CG_OPTION:
            cmd += " -cam \"%(renderableCamera)s\"" % self.renderSettings
        if self.G_CG_LAYER_NAME:
            cmd += " -rl \"%(renderableLayer)s\"" % self.renderSettings

        # self.MAYA_BASE_RENDER_CMD = cmd
                
        # cmd += " -preRender \"python \\\"user_id=%s;mapping=%s;plugins=%s;taskid=%s;rendersetting=%s;execfile(\\\\\\\"%s\\\\\\\")\\\"\"" % (self.G_USER_ID,self.mappings,self.CG_PLUGINS_DICT,self.G_TASK_ID,self.renderSettings,self.G_RN_MAYA_PRERENDER)



        # cmd += " -preRender \"python \\\"user_id=%s;mapping=%s;plugins=%s;taskid=%s;rendersetting=%s;execfile(\\\\\\\"%s\\\\\\\");import sys;sys.path.append('%s');import PostRender; reload(PostRender)\\\"\"" % (self.G_USER_ID,self.mappings,self.CG_PLUGINS_DICT,self.G_TASK_ID,self.renderSettings,self.G_RN_MAYA_PRERENDER,self.G_NODE_MAYASCRIPT)

        # cmd += " -preRender \"python \\\"user_id=%s;mapping=%s;plugins=%s;taskid=%s;rendersetting=%s;start=%s;execfile(\\\\\\\"//10.60.100.101/o5/py/model/prerender.py\\\\\\\")\\\"\"" % (self["common"]["userId"],self["mappings"],self["plugins"]["plugins"],self["common"]["taskId"],self["renderSettings"],self["renderSettings"]["start"])

        #---------------render cmd-------------------------
        if "RenderMan_for_Maya" in self.CG_PLUGINS_DICT:
            cmd += " -r rman"

        elif "redshift_GPU" in self.CG_PLUGINS_DICT:

            cmd += " -preRender \"python \\\"user_id=%s;mapping=%s;plugins=%s;taskid=%s;rendersetting=%s;execfile(\\\\\\\"%s\\\\\\\")\\\"\" -r redshift -logLevel 2 " % (self.G_USER_ID,self.mappings,self.CG_PLUGINS_DICT,self.G_TASK_ID,self.renderSettings)

            # cmd += " -preRender \"_RV_RSConfig;\" -r redshift -logLevel 2"
            if "gpuid" in os.environ:
                gpu_n= int(os.environ["gpuid"]) - 1
            else :
                gpu_n="0"

            gpu_n="0,1"
            cmd += " -gpu {%s}" % (gpu_n)
            
        elif "vrayformaya" in self.CG_PLUGINS_DICT:
            pass
        # -------mentalray---------------
        # ----------render tile------------


        if self.renderSettings["tile_region"]:
            self.renderer = self.G_TASK_JSON_DICT['scene_info_render'][self.G_CG_LAYER_NAME]['common']['renderer']
            if self.renderer in ["mentalRay", "arnold", "vray"]:
                if self.renderer == "mentalRay" and int(self.CG_VERSION) < 2017:
                    cmd += " -r mr -reg %(tile_region)s" % self.renderSettings
                elif self.renderer == "mentalRay" and int(self.CG_VERSION) > 2016.5 and "mentalray" in self.CG_PLUGINS_DICT:
                    cmd += " -r mr -reg %(tile_region)s" % self.renderSettings

                elif self.renderer == "arnold" and "mtoa" in self.CG_PLUGINS_DICT:
                    cmd += " -r arnold -reg %(tile_region)s" % self.renderSettings

                elif self.renderer == "vray" and "vrayformaya" in self.CG_PLUGINS_DICT:
                    cmd += " -r vray -reg %(tile_region)s" % self.renderSettings

                else:
                    print("please confirm the renderer is correct!")
                    print("current render layer \'s render is %s ,not in [mentalRay,arnold,vray]" % (self.renderer))
                    sys.exit(555)
            else:
                cmd += " -r mr -reg %(tile_region)s" % self.renderSettings

        max_threads_number = int(multiprocessing.cpu_count())
        
        if " -r " not in cmd and float(self.CG_VERSION) < 2017:            
            # cmd += " -mr:art -mr:aml"
            cmd += " -mr:rt %s -mr:aml" %max_threads_number

        # cmd += " \"%(maya_file)s\"" % self.renderSettings    
      
        # self.RENDERCMD = cmd
        options = {}
        options["output"] = self.renderSettings["output"]
        options["output_frame"] = self.renderSettings["output_frame"]
        options["g_one_machine_multiframe"] = self.renderSettings["g_one_machine_multiframe"]

        #-------------get custom render cmd-------------
        cmd += " -postFrame \"python \\\"user_id=%s;mapping=%s;plugins=%s;taskid=%s;options=%s;execfile(\\\\\\\"%s\\\\\\\")\\\";\"" % (self.G_USER_ID,self.mappings,self.CG_PLUGINS_DICT,self.G_TASK_ID,options,self.G_RN_MAYA_POSTRENDER)
        # cmd += " -postFrame \"python \\\"execfile(\\\\\\\"//10.90.100.101/o5/py/model/rendered_frames.py\\\\\\\");set_rendered_frame(\\\\\\\"%s\\\\\\\")\\\";\"" % (self["platform"]["cfg_path"])
        # if int(self.renderSettings["end"]) > int(self.renderSettings["start"]):
        #     cmd += " -postFrame \"python \\\"rendersetting=%s;execfile(\\\\\\\"%s\\\\\\\")\\\";\"" % (self.renderSettings,self.G_RN_MAYA_POSTRENDER)
        # cmd += " -postFrame \"python \\\"execfile(\\\\\\\"//10.90.100.101/o5/py/model/PostRender.py\\\\\\\");set_rendered_frame(save_path=\\\\\\\"%s\\\\\\\")\\\"\"" % (self.renderSettings['output'])
        #
        # cmd += " -postFrame \"python \\\"execfile(\\\\\\\"//10.90.100.101/o5/py/model/PostRender.py\\\\\\\");set_rendered_frame(save_path=\\\\\\\"%s\\\\\\\",task_id=\\\\\\\"%s\\\\\\\",rd=\\\\\\\"%s\\\\\\\",use_id=\\\\\\\"%s\\\\\\\")\\\";\"" % (
        # self["platform"]["cfg_path"], self["common"]["taskId"], self["renderSettings"]['output'],
        # self["server"]["user_id"])

        if "-r rman" in cmd:
            cmd += " -setAttr Format:resolution \"%(width)s %(height)s\" \"%(maya_file)s\"" % self.renderSettings
        else:
            cmd += " -x %(width)s -y %(height)s \"%(maya_file)s\"" % self.renderSettings

        print ("render cmd info:")
        print (cmd)
        sys.stdout.flush()
        return cmd




