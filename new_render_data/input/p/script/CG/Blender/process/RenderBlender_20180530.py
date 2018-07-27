#!/usr/bin/env python
#encoding:utf-8
# -*- coding: utf-8 -*-
import logging
import os
import os.path
import sys
import subprocess
import string
import logging
import time
import shutil
from RenderBase import RenderBase
from CommonUtil import RBCommon as CLASS_COMMON_UTIL

class RenderBlender(RenderBase):
    def __init__(self,**paramDict):
        RenderBase.__init__(self,**paramDict)
        print("Blender INIT")
        self.G_CG_VERSION = '%s-%s' % (self.G_CG_CONFIG_DICT['cg_name'], self.G_CG_CONFIG_DICT['cg_version'])
        self.G_RUN_PY = os.path.join(self.G_NODE_PY, 'CG', self.G_CG_NAME, 'script', 'render.py')
        self.G_EXE = os.path.join('B:/plugins/blender/Blender Foundation', self.G_CG_VERSION, 'blender.exe')
        
    '''def FramesAnalyse(cls,frames=''):
        all_frames = frames
        types = 0
        renderjobs = {}
        ## 5 5 1  /  1-10[1]  /  1,3,6  /  1,2-5,9   /  3,2-10[3],5
        k = 0
        if "," in all_frames:
            frames_list = all_frames.split(",")
            types = 2
            for i in range(len(frames_list)):
                if "-" in frames_list[i]:
                    if "[" in frames_list[i]: ## 2-10[3]
                        frame_sp = frames_list[i].split("]")[0].split("[")
                        frame_ah = frame_sp[0].split("-")
                        k,renderjobs = cls.createframeadict(k,[frame_ah[0],frame_ah[-1],frame_sp[-1]],renderjobs)
                        
                    else: ## 2-5
                        frame_ah = frames_list[i].split("-")
                        k,renderjobs = cls.createframeadict(k,[i,i,str(1)],renderjobs)
                        
                else:  ## 1
                    k,renderjobs = cls.createframeadict(k,[frames_list[i],frames_list[i],str(1)],renderjobs)
                    
        elif "-" in all_frames and not "," in all_frames: ## 1-10[1]  /  2-5
            types = 1
            if "[" in all_frames: ## 1-10[3]
                frame_sp = all_frames.split("]")[0].split("[")
                frame_ah = frame_sp[0].split("-")
                k,renderjobs = cls.createframeadict(k,[frame_ah[0],frame_ah[-1],frame_sp[-1]],renderjobs)
            else: ## 2-5
                frame_ah = frames_list[i].split("-")
                k,renderjobs = cls.createframeadict(k,[frame_ah[0],frame_ah[-1],str(1)],renderjobs)
                
        else:
            frames_arr_s=all_frames.split(" ")
            k,renderjobs = cls.createframeadict(k,[frames_arr_s[0],frames_arr_s[1],frames_arr_s[2]],renderjobs)

        return renderjobs,types
        ## ｛0:[1 1 1],1:[2 2 1]｝'''

        
    def RB_RENDER(self):#7
        self.G_DEBUG_LOG.info('[Blender.RB_RENDER.start.....]')
        start_time = int(time.time())
        '''if self.g_one_machine_multiframe is True:
            render_list = CLASS_COMMON_UTIL.need_render_from_frame(self.G_CG_FRAMES)
            self.render_record.update({render_list[0]: {'start_time': start_time, 'end_time': 0}})'''
        
        self.G_FEE_PARSER.set('render', 'start_time', str(start_time))
        
        '''
        if self._render_frame == 1:
            frames="\""+str(self._frames[0])+" "+str(self._frames[1])+" "+str(self._frames[2])+"\""
        elif self._render_frame == 2:
            frames="\""+self.G_CG_FRAMES+"\""
            # frames="\""+"1,3-7[3],15"+"\""
        '''
        output_dir = self.G_WORK_RENDER_TASK_OUTPUT + '/'
        render_cmd = '"{exe_path}" -b "{cg_file}" -o "{output_dir}" -P "{run_py}" -f "{frames..}" -- "{task_json}" '.format(
            exe_path=self.G_EXE,
            cg_file=self.G_INPUT_CG_FILE,
            output_dir=output_dir,
            run_py=self.G_RUN_PY,
            frames=self.G_CG_FRAMES,
            task_json=self.G_TASK_JSON,
        )
        print(render_cmd)
        CLASS_COMMON_UTIL.cmd(render_cmd, my_log=self.G_DEBUG_LOG, continue_on_error=True)
        
        '''if self.g_one_machine_multiframe is True:
            if '[_____render end_____]' in str(info).strip():  # [_____render end_____][1]
                # frame = re.search('\[(\d+)\]', str(info).strip()).group(1)
                frame = str(info).strip().split("][")[-1].split("]")[0]
                self.multiframe_complete_list.append(frame)
                end_time = int(time.time())
                print('[self.render_record]: {}'.format(self.render_record))
                self.render_record[frame]['end_time'] = end_time
                self.render_record[str(int(frame) + int(self.G_CG_BY_FRAME))] = {'start_time': end_time,'end_time': -1}'''
        
        
        end_time = int(time.time())
        self.G_FEE_PARSER.set('render', 'end_time', str(end_time))
        
        self.G_DEBUG_LOG.info('[Blender.RB_RENDER.end.....]')
        