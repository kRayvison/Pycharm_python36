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
import shutil,re
from RenderBase import RenderBase
from CommonUtil import RBCommon as CLASS_COMMON_UTIL

class RenderBlender(RenderBase):
    def __init__(self,**paramDict):
        RenderBase.__init__(self,**paramDict)
        print("Blender INIT")
        self.G_CG_VERSION = '%s-%s' % (self.G_CG_CONFIG_DICT['cg_name'], self.G_CG_CONFIG_DICT['cg_version'])
        self.G_RUN_PY = os.path.join(self.G_NODE_PY, 'CG', self.G_CG_NAME, 'script', 'render.py')
        self.G_EXE = os.path.join('B:/plugins/blender/Blender Foundation', self.G_CG_VERSION, 'blender.exe')

    def FramesAnalyse(self,frames=''):
        all_frames = frames
        types = 0
        renderjobs = {}
        ## 5 5 1  /  1-10[1]  /  1,3,6  /  1,2-5,9   /  3,2-10[3],5
        k = 0
        if "-" in all_frames and not "," in all_frames: ## 1-10[1]  /  2-5
            types = 1
            if "[" in all_frames: ## 1-10[3]
                frame_sp = all_frames.split("]")[0].split("[")
                frame_ah = frame_sp[0].split("-")
                renderjobs = [frame_ah[0],frame_ah[-1],frame_sp[-1]]
            else: ## 2-5
                frame_ah = frames_list[i].split("-")
                renderjobs =[frame_ah[0],frame_ah[-1],str(1)]
        else:
            renderjobs = [self.G_CG_START_FRAME,self.G_CG_END_FRAME,self.G_CG_BY_FRAME]

        return renderjobs
        ## [1 5 1]

    def copyfiles(self,pathin,frame,aim_name):
        source_path = os.path.abspath(pathin)
        frame_folder = str(frame).zfill(4)

        for dirpath,dirnames,filenames in os.walk(source_path):
            if dirpath == source_path:
                print(dirpath)
                print(dirnames)
                print(filenames)
                if len(dirnames):
                    for fd in dirnames:
                        if fd not in aim_name:
                            path_new = os.path.join(dirpath,fd)
                            path_aim = os.path.join(dirpath,frame_folder)
                            print(path_new,path_aim)
                            os.system ("robocopy /e /ns /nc /nfl /ndl /np /move %s %s" % (path_new, path_aim))
                if len(filenames):
                    for pic in filenames:
                        path_new = os.path.join(dirpath,pic)
                        path_aim = os.path.join(dirpath,frame_folder,pic)
                        if not os.path.exists(os.path.join(dirpath,frame_folder)):os.makedirs(os.path.join(dirpath,frame_folder))
                        print(path_new,path_aim)
                        os.system ('copy /y  "%s" "%s"' % (path_new, path_aim))
                        os.remove(path_new)
        aim_name.append(frame_folder)
        return aim_name

    def FiltLog(self,my_popen='',pid=''):
        error_calls = 0
        frame_ah = ''
        while my_popen.poll()==None:
            info = my_popen.stdout.readline().strip()
            if info!='':
                self.G_RENDER_LOG.info(str(info))
                self.G_RENDER_LOG.info(frame_ah)
                if self.g_one_machine_multiframe is True:
                    if 'Saved:' in str(info).strip():
                        if "Fra:" in str(frame_ah):
                            frame = re.findall('Fra:(\d+)', str(frame_ah).strip())[0]
                            self.aim_names = self.copyfiles(self.G_WORK_RENDER_TASK_OUTPUT,frame,self.aim_names)
                            if frame not in self.multiframe_complete_list:
                                self.multiframe_complete_list.append(frame)
                            self.G_DEBUG_LOG.info("[callback]multiframe_complete_list={}\nframe={}".format(self.multiframe_complete_list, frame))
                            end_time = int(time.time())
                            self.G_DEBUG_LOG.info('[self.render_record]: {}'.format(self.render_record))
                            self.render_record[frame]['end_time'] = end_time
                            self.render_record[str(int(frame) + int(self.G_CG_BY_FRAME))] = {'start_time': end_time,'end_time': -1}
                frame_ah = info

    def RB_RENDER(self):#7
        self.G_DEBUG_LOG.info('[Blender.RB_RENDER.start.....]')
        start_time = int(time.time())
        if self.g_one_machine_multiframe is True:
            render_list = CLASS_COMMON_UTIL.need_render_from_frame(self.G_CG_FRAMES)
            self.render_record.update({render_list[0]: {'start_time': start_time, 'end_time': 0}})
        self.G_FEE_PARSER.set('render', 'start_time', str(start_time))

        _frames = self.FramesAnalyse(self.G_CG_FRAMES)
        self.G_RENDER_LOG.info(str(_frames))
        self.aim_names = []
        output_dir = self.G_WORK_RENDER_TASK_OUTPUT + '/'
        render_cmd = '"{exe_path}" -b "{cg_file}" -o "{output_dir}" -P "{run_py}" -s "{frame_s}" -e "{frame_e}" -j "{frame_j}" -a -- "{task_json}" '.format(
            exe_path=self.G_EXE,
            cg_file=self.G_INPUT_CG_FILE,
            output_dir=output_dir,
            run_py=self.G_RUN_PY,
            frame_s=_frames[0],
            frame_e=_frames[1],
            frame_j=_frames[2],
            task_json=self.G_TASK_JSON,
        )
        print(render_cmd)
        result_code, _ = CLASS_COMMON_UTIL.cmd(render_cmd, None,1,True,True,self.FiltLog)
        self.cg_return_code = result_code

        end_time = int(time.time())
        self.G_FEE_PARSER.set('render', 'end_time', str(end_time))

        self.G_DEBUG_LOG.info('[Blender.RB_RENDER.end.....]')
