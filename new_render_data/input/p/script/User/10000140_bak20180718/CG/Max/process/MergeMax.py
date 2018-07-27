#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import logging
import time
import subprocess
import sys
import codecs
import configparser
import shutil
from Max import Max

from CommonUtil import RBCommon as CLASS_COMMON_UTIL

class MergeMax(Max):

    '''
        初始化构造函数
    '''
    def __init__(self,**param_dict):
        Max.__init__(self,**param_dict)
        self.temp_mark=0
        
        ## clear directory
        if os.path.exists(self.G_WORK_RENDER_TASK_OUTPUT):
            try:
                shutil.rmtree(self.G_WORK_RENDER_TASK_OUTPUT)
            except Exception as e:
                print('[err]delete directory failed : %s' % self.G_WORK_RENDER_TASK_OUTPUT)
                print(e)
        
        photon_directory = os.path.join(self.G_WORK_RENDER_TASK,'photon')
        if os.path.exists(photon_directory):
            try:
                shutil.rmtree(photon_directory)
            except Exception as e:
                print('[err]delete directory failed : %s' % photon_directory)
                print(e)
            
        if not os.path.exists(self.G_WORK_RENDER_TASK_OUTPUT):
            os.makedirs(self.G_WORK_RENDER_TASK_OUTPUT)
        if not os.path.exists(photon_directory):
            os.makedirs(photon_directory)
                
        print('Merge init')        
                
    '''
        合并光子入口
    '''
    def RB_RENDER(self):
        self.format_log('合并光子开始','start')
        self.G_DEBUG_LOG.info('[Merge.RB_RENDER start]')
        self.G_FEE_PARSER.set('render','start_time',str(int(time.time())))
        
        # 调用合并光子方法
        photon_path=os.path.join(self.G_WORK_RENDER_TASK,'photon','source')
        photon_user_path=os.path.join(self.G_TEMP_PATH,'photon')
        if self.G_MULTI_CAMERA:
            photon_user_path=os.path.join(self.G_TEMP_PATH,'photon',self.G_SMALL_TASK_ID)
        
        if not os.path.exists(photon_path):
            os.makedirs(photon_path)
        
        self.G_DEBUG_LOG.info(photon_path)
        self.G_DEBUG_LOG.info(photon_user_path)
            
        if os.path.exists(photon_user_path):            
            copy_vrmap_cmd=r'c:\fcopy\FastCopy.exe /speed=full /force_close /no_confirm_stop /force_start "'+photon_user_path+'\\*.vr*map" /to="'+photon_path+'"'
            CLASS_COMMON_UTIL.cmd(copy_vrmap_cmd,my_log=self.G_DEBUG_LOG)
            
            
        self.G_DEBUG_LOG.info('photon_path ='+str(photon_path))
        self.show_path_file(photon_path)
        
        #-----------------------------------------merge photon-----------------------------------------------
        self.merge_photon(photon_path)
        self.G_FEE_PARSER.set('render','end_time',str(int(time.time())))
        self.G_DEBUG_LOG.info('[Merge.RB_RENDER end]')
        self.format_log('合并光子结束','end')
       
        
    '''
        合成光子函数，参数说明：path光子所在路径
    '''
    def merge_photon(self,path):
        self.temp_mark=self.temp_mark+1
        photon_output = os.path.join(self.G_WORK_RENDER_TASK,'photon','temp'+str(self.temp_mark))
        if not os.path.exists(photon_output):
            os.makedirs(photon_output)
        self.G_DEBUG_LOG.info('photon output path='+photon_output)
        
        render_output=self.G_WORK_RENDER_TASK_OUTPUT
        self.G_DEBUG_LOG.info('render output path='+render_output)
        
        if 'plugins' in self.G_CG_CONFIG_DICT and 'vray' in self.G_CG_CONFIG_DICT['plugins']:
            stand_render = 'vray'+self.G_CG_CONFIG_DICT['plugins']['vray']        
            # vray='b:/plugins/max/imv/'+stand_render+'/imapviewer.exe'
            vray = os.path.join(self.G_MAX_B,'imv',stand_render,'imapviewer.exe')
            self.G_DEBUG_LOG.info('vray='+vray)
            
            # merge vrmap
            file_array=self.filter_photon_file(path, type='vrmap')
            file_array.sort()
            self.G_DEBUG_LOG.info(file_array)
            number=len(file_array)
            self.G_DEBUG_LOG.info('number='+str(number))
            # print 'number='+str(number)
            if 0<number<=10:
                cmd='"'+vray+'"'
                for p in file_array:
                    cmd=cmd+' -load '+path+'/'+p
                    pass
                cmd=cmd+' -save '+render_output+'/'+self.G_SMALL_TASK_ID+'_irrmap.vrmap -nodisplay '
                # self.RVCmd(cmd)
                CLASS_COMMON_UTIL.cmd(cmd,my_log=self.G_DEBUG_LOG)
                # CLASS_COMMON_UTIL.cmd_python3(cmd,my_log=self.G_DEBUG_LOG)
                self.show_path_file(render_output)
                pass
            elif number>10:
                j=0
                k=0
                while j<number:
                    k=k+1
                    i=0
                    cmd='"'+vray+'"'
                    while i<10:
                        
                        if j==number:
                            break
                        # print 'file_array['+str(j)+']='+file_array[j]
                        self.G_DEBUG_LOG.info('file_array['+str(j)+']='+file_array[j])
                        cmd=cmd+' -load '+path+'/'+file_array[j]
                        i=i+1
                        j=j+1
                        pass
                    cmd=cmd+' -save '+photon_output+'/'+str(k)+'.vrmap '+' -nodisplay'
                    # self.RVCmd(cmd)
                    CLASS_COMMON_UTIL.cmd(cmd,my_log=self.G_DEBUG_LOG)
                    # CLASS_COMMON_UTIL.cmd_python3(cmd,my_log=self.G_DEBUG_LOG)
                # print 'j='+str(j)
                self.G_DEBUG_LOG.info('j='+str(j))
                self.show_path_file(photon_output)
                self.merge_photon(photon_output)
                
            # merge vrlmap
            file_array=self.filter_photon_file(path, type='vrlmap')
            file_array.sort()
            self.G_DEBUG_LOG.info(file_array)
            number=len(file_array)
            self.G_DEBUG_LOG.info('number='+str(number))
            # print 'number='+str(number)
            if 0<number<=10:
                cmd='"'+vray+'"'
                for p in file_array:
                    cmd=cmd+' -load '+path+'/'+p
                    pass
                cmd=cmd+' -save '+render_output+'/'+self.G_SMALL_TASK_ID+'_lightcache.vrlmap -nodisplay '
                # self.RVCmd(cmd)
                CLASS_COMMON_UTIL.cmd(cmd,my_log=self.G_DEBUG_LOG)
                # CLASS_COMMON_UTIL.cmd_python3(cmd,my_log=self.G_DEBUG_LOG)
                self.show_path_file(render_output)
                pass
            elif number>10:
                j=0
                k=0
                while j<number:
                    k=k+1
                    i=0
                    cmd='"'+vray+'"'
                    while i<10:
                        
                        if j==number:
                            break
                        # print 'file_array['+str(j)+']='+file_array[j]
                        self.G_DEBUG_LOG.info('file_array['+str(j)+']='+file_array[j])
                        cmd=cmd+' -load '+path+'/'+file_array[j]
                        i=i+1
                        j=j+1
                        pass
                    cmd=cmd+' -save '+photon_output+'/'+str(k)+'.vrlmap '+' -nodisplay'
                    # self.RVCmd(cmd)
                    CLASS_COMMON_UTIL.cmd(cmd,my_log=self.G_DEBUG_LOG)
                    # CLASS_COMMON_UTIL.cmd_python3(cmd,my_log=self.G_DEBUG_LOG)
                # print 'j='+str(j)
                self.G_DEBUG_LOG.info('j='+str(j))
                self.show_path_file(photon_output)
                self.merge_photon(photon_output)
            
    '''
        过滤tga 扩展名的文件，这些文件不进行合并光子
    '''
    def filter_photon_file(self, path, type='vrmap'):
        file_array=os.listdir(path)
        tempArray=[]
        for nameStr in file_array:
            
            if nameStr.endswith('.{}'.format(type)):
                self.G_DEBUG_LOG.info('nameStr='+nameStr)
                tempArray.append(nameStr)
        return tempArray
        
    def show_path_file(self,path):
        for p in os.listdir(path):
            self.G_DEBUG_LOG.info('file='+path+'/'+p)
            # self.G_RENDERCMD_LOGGER.info('file='+path+'/'+p)

    '''
        上传渲染结果和日志
    ''' 
    def RB_HAN_RESULT(self):#8
        self.G_DEBUG_LOG.info('[BASE.RB_HAN_RESULT.start.....]')
        # 只渲染光子
        if self.G_ONLY_PHOTON == 'true':
            self.result_action()
        else:
            self.result_action_photon()
        self.G_DEBUG_LOG.info('[BASE.RB_HAN_RESULT.end.....]')
            
        
    def result_action_photon(self):

        upload_path = os.path.join(self.G_INPUT_PROJECT_PATH,'photon',self.G_SMALL_TASK_ID)

        cmd1='c:\\fcopy\\FastCopy.exe  /speed=full /force_close  /no_confirm_stop /force_start "' +self.G_WORK_RENDER_TASK_OUTPUT.replace('/','\\') +'" /to="'+upload_path+'"'
        # cmd2='"' +frame_check + '" "' + self.G_WORK_RENDER_TASK_OUTPUT + '" "'+ upload_path.rstrip()+'"'
        cmd3='c:\\fcopy\\FastCopy.exe /cmd=move /speed=full /force_close  /no_confirm_stop /force_start "' +self.G_WORK_RENDER_TASK_OUTPUT.replace('/','\\')+'\\*.*" /to="'+self.G_WORK_RENDER_TASK_OUTPUTBAK.replace('/','\\')+'"'
        
        CLASS_COMMON_UTIL.cmd(cmd1,my_log=self.G_DEBUG_LOG,try_count=3)

        CLASS_COMMON_UTIL.cmd(cmd3,my_log=self.G_DEBUG_LOG,try_count=3,continue_on_error=True)
        

    '''
        get dir size
    '''
    def getDirFileSize(self,path):
        list_dirs = os.walk(path)
        fileNum=len(os.listdir(path))
        fileSizeSum=0
        fileSizeArray=[]
        flag=True
        for root, dirs, files in list_dirs:   
            for name in files:
                absolutePathFiles=os.path.join(root,name)
                size=os.path.getsize(absolutePathFiles)
                fileSizeSum=fileSizeSum+size
                fileSizeArray.append(size)
                self.G_DEBUG_LOG.info("filename="+absolutePathFiles)
                self.G_DEBUG_LOG.info("filesize="+str(size)) 
        self.G_DEBUG_LOG.info("fileNum="+str(fileNum))
        self.G_DEBUG_LOG.info("fileSizeSum="+str(fileSizeSum))
        if len(fileSizeArray)<=0:
            flag=False
        else:
            for f in fileSizeArray:
                if float(f) <=0:
                    flag=False
                    break
                pass
        self.G_DEBUG_LOG.info("flag="+str(flag))
        return flag
