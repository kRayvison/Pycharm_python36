#!/usr/bin/env python
#encoding:utf-8
# -*- coding: utf-8 -*-
import logging
import os
import sys
import subprocess
import string
import time,datetime
import shutil
import ctypes
import json
import re
#import math

from CommonUtil import RBCommon as CLASS_COMMON_UTIL
from CommonUtil import RBKafka as CLASS_KAFKA

reload(sys)
sys.setdefaultencoding('utf-8')

class RenderBase():

    def __init__(self,**param_dict):
        print '[BASE.init.start.....]'
        
        self.G_RENDER_CORE_TYPE = 'cpu'
        self.G_JOB_ID=param_dict['G_JOB_ID']
        self.G_USER_ID=param_dict['G_USER_ID']
        self.G_USER_ID_PARENT=param_dict['G_USER_ID_PARENT']
        self.G_TASK_ID=param_dict['G_TASK_ID']
        self.G_SCRIPT_POOL=param_dict['G_SCRIPT_POOL']
        self.G_ACTION=param_dict['G_ACTION']
        self.G_CG_FRAMES=param_dict['G_CG_FRAMES']
        self.G_CG_LAYER_NAME=param_dict['G_CG_LAYER_NAME']

        self.G_SYS_ARGVS=param_dict['G_SYS_ARGVS']#taskid,jobindex,jobid,nodeid,nodename
        self.G_JOB_NAME=self.G_SYS_ARGVS[3].replace('"','')
        self.G_NODE_NAME=self.G_SYS_ARGVS[5]
        
        self.G_WORK='c:/work'
        self.G_LOG_WORK='C:/log/render'
        self.G_RENDER_OS = param_dict['G_RENDER_OS']
        if self.G_RENDER_OS=='Linux':
            self.G_LOG_WORK='/tmp/nzs-data/log/render'
            self.G_WORK='/tmp/nzs-data/work'
        
        self.G_CG_TILE='0'
        self.G_CG_TILE_COUNT='1'
        print param_dict
        if 'G_CG_TILE' in param_dict:
            self.G_CG_TILE=param_dict['G_CG_TILE']
        if 'G_CG_TILE_COUNT' in param_dict:
            self.G_CG_TILE_COUNT=param_dict['G_CG_TILE_COUNT']
        
        if 'G_SCHEDULER_CLUSTER_ID' in param_dict:
            self.G_SCHEDULER_CLUSTER_ID=param_dict['G_SCHEDULER_CLUSTER_ID']
        if 'G_SCHEDULER_CLUSTER_NODES' in param_dict:
            self.G_SCHEDULER_CLUSTER_NODES=param_dict['G_SCHEDULER_CLUSTER_NODES']
        
        #-----------------------------------------log-----------------------------------------------
        self.G_DEBUG_LOG=logging.getLogger('debug_log')
        self.G_RENDER_LOG=logging.getLogger('render_log')
        self.init_log()       
        
        #-----------------------------------------work directory-----------------------------------------------
        self.G_WORK_RENDER=os.path.normpath(os.path.join(self.G_WORK,'render'))
        self.G_WORK_RENDER_TASK=os.path.normpath(os.path.join(self.G_WORK_RENDER,self.G_TASK_ID))
        
        #___abort___self.G_WORK_RENDER_TASK_BLOCK=os.path.normpath(os.path.join(self.G_WORK_RENDER_TASK,'block'))
        self.G_WORK_RENDER_TASK_CFG=os.path.normpath(os.path.join(self.G_WORK_RENDER_TASK,'cfg'))
        #___abort___self.G_WORK_RENDER_TASK_GRAB=os.path.normpath(os.path.join(self.G_WORK_RENDER_TASK,'grab'))
        #___abort___self.G_WORK_RENDER_TASK_MAX=os.path.normpath(os.path.join(self.G_WORK_RENDER_TASK,'max'))
        #___abort___self.G_WORK_RENDER_TASK_MAXBAK=os.path.normpath(os.path.join(self.G_WORK_RENDER_TASK,'maxbak'))
        
        self.G_WORK_RENDER_TASK_OUTPUT=os.path.normpath(os.path.join(self.G_WORK_RENDER_TASK,'output'))
        self.G_WORK_RENDER_TASK_OUTPUTBAK=os.path.normpath(os.path.join(self.G_WORK_RENDER_TASK,'outputbak'))
        self.G_WORK_RENDER_TASK_SMALL=os.path.normpath(os.path.join(self.G_WORK_RENDER_TASK,'small'))
        self.make_dir()
        
        #-----------------------------------------kafka-----------------------------------------------
        self.G_KAFKA_HOST='10.60.96.142'
        self.G_KAFKA_PORT=9092
        self.G_KAFKA_TOPIC= 'dev-munu-topic-01'
        self.G_START_TIME=''
        self.G_SMALL_PIC=''
        self.G_END_TIME=''
        
        #-----------------------------------------task.json-----------------------------------------------
        self.G_TASK_JSON=param_dict['G_TASK_JSON']
        self.G_DEBUG_LOG.info(self.G_TASK_JSON)
        if not os.path.exists(self.G_TASK_JSON):
            CLASS_COMMON_UTIL.error_exit_log(self.G_DEBUG_LOG,'task.json not exists')
            
            
        self.G_TASK_JSON_DICT=eval(open(self.G_TASK_JSON, 'r').read())
        #jsonStr = (open(self.G_TASK_JSON, 'r').read())
        #self.G_TASK_JSON_DICT=json.load(jsonStr)
        self.G_ZONE=self.G_TASK_JSON_DICT['system_info']['common']['zone']
        self.G_PLATFORM=self.G_TASK_JSON_DICT['system_info']['common']['platform']
        self.G_TILES_PATH=os.path.normpath(self.G_TASK_JSON_DICT['system_info']['common']['tiles_path'])
        self.G_INPUT_CG_FILE=os.path.normpath(self.G_TASK_JSON_DICT['system_info']['common']['input_cg_file'])
        self.G_CHANNEL=self.G_TASK_JSON_DICT['system_info']['common']['channel']
        self.G_INPUT_PROJECT_PATH=os.path.normpath(self.G_TASK_JSON_DICT['system_info']['common']['input_project_path'])
        self.G_CONFIG_PATH=os.path.normpath(self.G_TASK_JSON_DICT['system_info']['common']['config_path']+'/')
        self.G_SMALL_PATH=os.path.normpath(self.G_TASK_JSON_DICT['system_info']['common']['small_Path'])
        self.G_OUTPUT_USER_PATH=os.path.normpath(self.G_TASK_JSON_DICT['system_info']['common']['output_user_path'])
        self.G_INPUT_USER_PATH=os.path.normpath(self.G_TASK_JSON_DICT['system_info']['common']['input_user_path'])
        self.G_PLUGIN_PATH=os.path.normpath(self.G_TASK_JSON_DICT['system_info']['common']['plugin_path'])
        self.G_TEMP_PATH=os.path.normpath(self.G_TASK_JSON_DICT['system_info']['common']['temp_path'])
        
        self.G_PRE_PY=os.path.join(self.G_WORK_RENDER_TASK_CFG,'pre.py')
        self.G_POST_PY=os.path.join(self.G_WORK_RENDER_TASK_CFG,'post.py')
        
        #-----------------------------------------assert.json-----------------------------------------------
        self.G_TASK_JSON_DIR=os.path.dirname(self.G_TASK_JSON)
        self.G_ASSET_JSON=os.path.join(self.G_TASK_JSON_DIR,'asset.json')
        self.G_ASSET_JSON_DICT=eval(open(self.G_ASSET_JSON, 'r').read())
        
        #-----------------------------------------frames-----------------------------------------------
        self.G_CG_START_FRAME = None
        self.G_CG_END_FRAME = None
        self.G_CG_BY_FRAME = None
        patt = '(-?\d+)(?:-?(-?\d+)(?:\[(-?\d+)\])?)?'
        m = re.match(patt,self.G_CG_FRAMES)
        if m != None:
            self.G_CG_START_FRAME = m.group(1)
            self.G_CG_END_FRAME = m.group(2)
            self.G_CG_BY_FRAME = m.group(3)
            if self.G_CG_END_FRAME == None:
                self.G_CG_END_FRAME = self.G_CG_START_FRAME
            if self.G_CG_BY_FRAME == None:
                self.G_CG_BY_FRAME = '1'
        else:
            print 'frames is not match'

    
    '''
        pre custom
    '''
    def RB_PRE_PY(self):#1
        self.format_log('执行自定义PY脚本','start')
        self.G_DEBUG_LOG.info('[BASE.RB_PRE_PY.start.....]')
        self.G_DEBUG_LOG.info(u'如果以下自定义PY脚本存在，会执行此脚本')
        self.G_DEBUG_LOG.info(self.G_PRE_PY)
        if os.path.exists(self.G_PRE_PY):
            sys.argv=[self.G_USER_ID,self.G_TASK_ID]
            #execfile(self.G_PRE_PY)
            if self.G_RENDER_OS=='Linux':
                os.system('./' + self.G_PRE_PY)
            else:
                os.system('c:/python27/python.exe ' + self.G_PRE_PY)
        self.G_DEBUG_LOG.info('[BASE.RB_PRE_PY.end.....]')
        self.format_log('done','end')
    
    '''
        映射盘符
    '''
    def RB_MAP_DRIVE(self):#2
        self.format_log('映射盘符','start')
        self.G_DEBUG_LOG.info('[BASE.RB_MAP_DRIVE.start.....]')
        
        #check the system drive
        self.check_disk()
        
        #delete all mappings
        CLASS_COMMON_UTIL.del_net_use()
        CLASS_COMMON_UTIL.del_subst()
        
        #net use
        b_flag = False
        if self.G_TASK_JSON_DICT['system_info'].has_key('mnt_map'):
            map_dict = self.G_TASK_JSON_DICT['system_info']['mnt_map']
            for key,value in map_dict.items():
                map_cmd = 'net use "%s" "%s"' % (key,value)
                CLASS_COMMON_UTIL.cmd(map_cmd,my_log=self.G_DEBUG_LOG,try_count=3)
                if key.lower() == 'b:':
                    b_flag = True
        if not b_flag:
            map_cmd_b = 'net use B: "%s"' % (self.G_PLUGIN_PATH)
            CLASS_COMMON_UTIL.cmd(map_cmd_b,my_log=self.G_DEBUG_LOG,try_count=3)
                
        self.G_DEBUG_LOG.info('[BASE.RB_MAP_DRIVE.end.....]')
        self.format_log('done','end')
        
    '''
        拷贝脚本文件
    '''
    def RB_HAN_FILE(self):#3  copy max.7z and so on
        self.format_log('拷贝脚本文件','start')
        self.G_DEBUG_LOG.info('[BASE.RB_HAN_FILE.start.....]'+self.G_RENDER_CORE_TYPE)
        
        CLASS_COMMON_UTIL.python_move(self.G_WORK_RENDER_TASK_OUTPUT,self.G_WORK_RENDER_TASK_OUTPUTBAK)
      
        self.G_DEBUG_LOG.info('[BASE.RB_HAN_FILE.end.....]')
        self.format_log('done','end')
        
    '''
        渲染配置
    '''
    def RB_CONFIG(self):#4
        self.format_log('渲染配置','start')
        self.G_DEBUG_LOG.info('[BASE.RB_RENDER_CONFIG.start.....]')
        
        #copy black.xml
        self.copy_black()
        
        self.G_DEBUG_LOG.info('[BASE.RB_RENDER_CONFIG.end.....]') 
        self.format_log('done','end')
        
    '''
        渲染
    '''
    def RB_RENDER(self):#5
        self.format_log('渲染','start')
        self.G_DEBUG_LOG.info('[BASE.RB_RENDER.start.....]')
        self.G_DEBUG_LOG.info('[BASE.RB_RENDER.end.....]')
        self.format_log('done','end')
        
    '''
        转换缩略图
    '''
    def RB_CONVERT_SMALL_PIC(self):#6
        self.format_log('转换缩略图','start')
        self.G_DEBUG_LOG.info('[BASE.RB_CONVERT_SMALL_PIC.start.....]')
        self.G_DEBUG_LOG.info(self.G_WORK_RENDER_TASK_SMALL)
        self.G_DEBUG_LOG.info(self.G_SMALL_PATH)
        if not os.path.exists(self.G_WORK_RENDER_TASK_SMALL):
            os.makedirs(self.G_WORK_RENDER_TASK_SMALL)
            
        exr_to_jpg=os.path.join(self.G_WORK_RENDER_TASK,'exr2jpg')
        exr_to_jpg_bak=os.path.join(self.G_WORK_RENDER_TASK,'exr2jpgbak')
        self.convert_dir(self.G_WORK_RENDER_TASK_OUTPUT,self.G_WORK_RENDER_TASK_SMALL)
        self.convert_dir(exr_to_jpg,self.G_WORK_RENDER_TASK_SMALL)
        
        move_cmd='c:\\fcopy\\FastCopy.exe /cmd=move /speed=full /force_close  /no_confirm_stop /force_start "' +self.G_WORK_RENDER_TASK_SMALL.replace('/','\\')+'\*.*" /to="'+self.G_SMALL_PATH.replace('/','\\')+'"'
        CLASS_COMMON_UTIL.cmd(move_cmd,my_log=self.G_DEBUG_LOG,continue_on_error=True)

        if  os.path.exists(exr_to_jpg):
            exr_to_jpg_bak_move='c:\\fcopy\\FastCopy.exe /cmd=move /speed=full /force_close  /no_confirm_stop /force_start "' +exr_to_jpg.replace('/','\\')+'\\*.*" /to="'+exr_to_jpg_bak.replace('/','\\')+'"'
            CLASS_COMMON_UTIL.cmd(exr_to_jpg_bak_move,my_log=self.G_DEBUG_LOG)            
        self.G_DEBUG_LOG.info('[BASE.RB_CONVERT_SMALL_PIC.end.....]')
        self.format_log('done','end')
        
    '''
        上传渲染结果和日志
    ''' 
    def RB_HAN_RESULT(self):#7
        self.format_log('结果处理','start')
        self.G_DEBUG_LOG.info('[BASE.RB_HAN_RESULT.start.....]')     
        
        self.result_action()

        self.G_DEBUG_LOG.info('[BASE.RB_HAN_RESULT.end.....]')
        self.format_log('done','end')
        
    def RB_POST_PY(self):#8 pre custom
        self.format_log('渲染完毕执行自定义脚本','start')
        self.G_DEBUG_LOG.info('[BASE.RB_POST_PY.start.....]')
        self.G_DEBUG_LOG.info(u'如果以下路径的脚本存在，则会被执行')
        self.G_DEBUG_LOG.info(self.G_POST_PY)
        if os.path.exists(self.G_POST_PY):
            sys.argv=[self.G_USER_ID,self.G_TASK_ID]
            #execfile(self.G_POST_PY)
            if self.G_RENDER_OS=='Linux':
                os.system('./' + self.G_POST_PY)
            else:
                os.system('c:/python27/python.exe ' + self.G_POST_PY)
        
        # if not self.G_RENDER_CORE_TYPE=="gpu":
        CLASS_COMMON_UTIL.del_net_use()
        CLASS_COMMON_UTIL.del_subst()
        
        self.G_DEBUG_LOG.info('[BASE.RB_POST_PY.end.....]')
        self.format_log('done','end')
        
    '''
        kafka发送消息给平台
    '''

    def RB_KAFKA_NOTIFY(self):#9
        self.format_log('kafka发送消息给平台','start')
        self.G_DEBUG_LOG.info('[BASE.RB_KAFKA_NOTIFY.start.....]')
        
        start_time = time.time()
        params = {}
        params["messageKey"] = self.G_ACTION
        params['platform']=self.G_PLATFORM
        params['messageTime']=str(int(start_time))
        params['messageId']=self.G_TASK_ID+'_'+params["messageKey"]+'_'+self.G_JOB_ID
        message_body_dict={}
        message_body_dict['zone']=self.G_ZONE
        message_body_dict['nodeName']=self.G_NODE_NAME
        message_body_dict['jobId']=self.G_JOB_ID
        message_body_dict['taskId']=self.G_TASK_ID
        message_body_dict['startTime']=self.G_START_TIME
        message_body_dict['smallPic']=self.G_SMALL_PIC
        message_body_dict['endTime']=self.G_END_TIME
        params['messageBody']=message_body_dict
        
        kafka_result=CLASS_KAFKA.produce(params,self.G_KAFKA_HOST, self.G_KAFKA_PORT,self.G_KAFKA_TOPIC)
        self.G_DEBUG_LOG.info('kafka_result='+str(kafka_result))
        
        self.G_DEBUG_LOG.info('[BASE.RB_KAFKA_NOTIFY.end.....]')
        self.format_log('done','end')
            
    '''
        初始化日志
    '''
    def init_log(self):
        log_dir=os.path.join(self.G_LOG_WORK,self.G_TASK_ID)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # debug_log 不能开放给客户查看
        fm=logging.Formatter('%(asctime)s  %(levelname)s - %(message)s','%Y-%m-%d %H:%M:%S')
        debug_log_path=os.path.join(log_dir,(self.G_JOB_NAME+'_debug.log'))
        self.G_DEBUG_LOG.setLevel(logging.DEBUG)
        debug_log_handler=logging.FileHandler(debug_log_path)
        debug_log_handler.setFormatter(fm)
        self.G_DEBUG_LOG.addHandler(debug_log_handler)
        console = logging.StreamHandler()  
        console.setLevel(logging.INFO)  
        self.G_DEBUG_LOG.addHandler(console)
        
        # render_log 可开放给客户查看
        render_log_path=os.path.join(log_dir,(self.G_JOB_NAME+'_render.log'))
        self.G_RENDER_LOG.setLevel(logging.DEBUG)
        render_log_handler=logging.FileHandler(render_log_path)
        render_log_handler.setFormatter(fm)
        self.G_RENDER_LOG.addHandler(render_log_handler)
        console = logging.StreamHandler()  
        console.setLevel(logging.INFO)  
        self.G_RENDER_LOG.addHandler(console)
    
    '''
        创建目录
    '''       
    def make_dir(self):
        self.G_DEBUG_LOG.info('[BASE.make_dir.start.....]')
        self.G_DEBUG_LOG.info(u'创建以下路径的目录：')
        self.G_DEBUG_LOG.info(self.G_WORK_RENDER)
        self.G_DEBUG_LOG.info(self.G_WORK_RENDER_TASK)
        self.G_DEBUG_LOG.info(self.G_WORK_RENDER_TASK_CFG)
        '''
        self.G_DEBUG_LOG.info(self.G_WORK_RENDER_TASK_BLOCK)
        self.G_DEBUG_LOG.info(self.G_WORK_RENDER_TASK_GRAB)
        self.G_DEBUG_LOG.info(self.G_WORK_RENDER_TASK_MAX)
        self.G_DEBUG_LOG.info(self.G_WORK_RENDER_TASK_MAXBAK)
        '''
        self.G_DEBUG_LOG.info(self.G_WORK_RENDER_TASK_OUTPUT)
        self.G_DEBUG_LOG.info(self.G_WORK_RENDER_TASK_OUTPUTBAK)
        self.G_DEBUG_LOG.info(self.G_WORK_RENDER_TASK_SMALL)
        #render
        if not os.path.exists(self.G_WORK_RENDER):
            os.makedirs(self.G_WORK_RENDER)
        #renderwork
        if not os.path.exists(self.G_WORK_RENDER_TASK):
            os.makedirs(self.G_WORK_RENDER_TASK)        
        #renderwork/cfg
        if not os.path.exists(self.G_WORK_RENDER_TASK_CFG):
            os.makedirs(self.G_WORK_RENDER_TASK_CFG)
        '''
        #renderwork/block
        if not os.path.exists(self.G_WORK_RENDER_TASK_BLOCK):
            os.makedirs(self.G_WORK_RENDER_TASK_BLOCK)        
        #renderwork/grab
        if not os.path.exists(self.G_WORK_RENDER_TASK_GRAB):
            os.makedirs(self.G_WORK_RENDER_TASK_GRAB)        
        #renderwork/max
        if not os.path.exists(self.G_WORK_RENDER_TASK_MAX):
            os.makedirs(self.G_WORK_RENDER_TASK_MAX)        
        #renderwork/maxbak
        if not os.path.exists(self.G_WORK_RENDER_TASK_MAXBAK):
            os.makedirs(self.G_WORK_RENDER_TASK_MAXBAK)  
        '''
        #renderwork/output
        if not os.path.exists(self.G_WORK_RENDER_TASK_OUTPUT):
            os.makedirs(self.G_WORK_RENDER_TASK_OUTPUT)            
        #renderwork/outputbak
        if not os.path.exists(self.G_WORK_RENDER_TASK_OUTPUTBAK):
            os.makedirs(self.G_WORK_RENDER_TASK_OUTPUTBAK)
        #renderwork/small
        if not os.path.exists(self.G_WORK_RENDER_TASK_SMALL):
            os.makedirs(self.G_WORK_RENDER_TASK_SMALL)
        self.G_DEBUG_LOG.info('[BASE.make_dir.end.....]')
        
    '''
        格式化日志
    '''
    def format_log(self,log_str,log_type='common'):
        if log_str==None:
            log_str=''
        if log_type!='system':
            log_str=CLASS_COMMON_UTIL.str_to_unicode(log_str)
            
        if log_type=='start':
            self.G_DEBUG_LOG.info('----------------------------['+log_str+']----------------------------\r\n')
        elif log_type=='end':
            self.G_DEBUG_LOG.info('['+log_str+']\r\n')
        else:
            self.G_DEBUG_LOG.info(log_str+'\r\n')
            
    '''
        检测系统盘符
    '''
    def check_disk(self):
        self.G_DEBUG_LOG.info('[BASE.check_disk.start.....]')
        lp_buffer = ctypes.create_string_buffer(78)
        ctypes.windll.kernel32.GetLogicalDriveStringsA(ctypes.sizeof(lp_buffer), lp_buffer)
        vol = lp_buffer.raw.split('\x00')
        for i in vol:
            if i:                             
                self.G_DEBUG_LOG.info('Disk='+str(i))
        self.G_DEBUG_LOG.info('[BASE.check_disk.end.....]')
    
    '''
        拷贝弹窗黑名单 black.xml
    '''
    def copy_black(self):
        self.G_DEBUG_LOG.info('[BASE.copy_black.start.....]')
        block_path = 'B:\\tools\\sweeper\\black.xml'
        base_path='c:\\work\\munu_client\\sweeper\\'
        self.G_DEBUG_LOG.info(block_path+'>'+base_path)
        if os.path.exists(block_path):
            CLASS_COMMON_UTIL.python_copy(block_path,base_path)
        self.G_DEBUG_LOG.info('[BASE.copy_black.end.....]')
    
    def convert_dir(self,dir,work_small_path):
        self.G_DEBUG_LOG.info('[BASE.convert_dir.start.....]')
        if os.path.exists(dir):
            small_size='200'
            # if self.G_KG=='1':
                # small_size='40'            
            list_dirs = os.walk(dir) 
            for root, dirs, files in list_dirs: 
                for name in files:
                    ext=os.path.splitext(name)[1]
                    self.G_DEBUG_LOG.info('name='+name)
                    if ext == '.vrmap' or   ext == '.vrlmap' or ext=='.exr':
                        continue    
                    work_big_pic =os.path.join(root, name)
                    self.G_SMALL_PIC=work_big_pic.replace(dir+'\\','')
                    self.G_SMALL_PIC=self.G_JOB_NAME+"_"+self.G_SMALL_PIC.replace('\\','[_]').replace('.','[-]')+'.jpg'
                    small_tmp_name = self.G_JOB_NAME+'_tmp.jpg'
                    work_small_pic=os.path.join(work_small_path,self.G_SMALL_PIC)
                    work_small_tmp_pic=os.path.join(work_small_path,small_tmp_name)

                    work_big_pic_tmp=os.path.join(root, 'tmp'+os.path.splitext(work_big_pic)[1] )
                    try:
                        os.rename(work_big_pic,work_big_pic_tmp);
                    except Exception, e:
                        self.G_DEBUG_LOG.info('rename failed-----')
                        pass
                    if not os.path.exists(work_big_pic_tmp):
                        work_big_pic_tmp = work_big_pic
                        work_small_tmp_pic = work_small_pic

                    oiio_path='c:\\oiio\\OpenImageIO-1.5.18-bin-vc9-x64\\oiiotool.exe'
                    convert_cmd='c:/ImageMagick/nconvert.exe  -out jpeg -ratio -resize '+small_size+' 0 -overwrite -o "'+work_small_tmp_pic +'" "'+work_big_pic_tmp+'"'
                    if ext=='.exr' and os.path.exists(oiio_path):
                        self.G_DEBUG_LOG.info('exr parse----'+name)
                        convert_cmd=oiio_path+' "'+work_big_pic_tmp+'" -resize '+self.get_convert_r(work_big_pic_tmp,oiio_path)+' -o "'+work_small_tmp_pic+'"'
                    #print work_big_pic
                    try:
                        CLASS_COMMON_UTIL.cmd(convert_cmd,my_log=self.G_DEBUG_LOG,continue_on_error=True)
                    except Exception, e:
                        self.G_DEBUG_LOG.info('parse smallPic failed-----')
                        pass
                    if not work_big_pic_tmp==work_big_pic:
                        os.rename(work_big_pic_tmp,work_big_pic)
                        if os.path.exists(work_small_tmp_pic):
                            os.rename(work_small_tmp_pic,work_small_pic)
                    
                    self.G_DEBUG_LOG.info('work_small_tmp_pic---'+work_small_tmp_pic+'---work_small_pic---'+work_small_pic+'---work_big_pic_tmp---'+work_big_pic_tmp+'---work_big_pic---'+work_big_pic)
        self.G_DEBUG_LOG.info('[BASE.convert_dir.end.....]')
    
    def check_result(self):
        self.G_DEBUG_LOG.info( '================[check_result]===============')
        server_output=self.G_OUTPUT_USER_PATH.encode(sys.getfilesystemencoding())
        node_output=self.G_WORK_RENDER_TASK_OUTPUT.replace('\\','/')
        self.G_DEBUG_LOG.info('')
        self.G_DEBUG_LOG.info(node_output)
        self.G_DEBUG_LOG.info(server_output)
        self.G_DEBUG_LOG.info('')
        node_img_dict={}
        server_img_dict={}
        for root, dirs, files in os.walk(node_output) : 
            for name in files:
                #------------node output file----------------
                node_img_file =os.path.join(root, name).replace('\\','/')
                img_file=node_img_file.replace(node_output,'')
                
                img_file_stat=os.stat(node_img_file)
                img_file_size=str(os.path.getsize(node_img_file))
                node_img_dict[img_file]=img_file_size
                date = datetime.datetime.fromtimestamp(img_file_stat.st_ctime)  
                img_file_ctime= date.strftime('%Y%m%d%H%M%S')  
                #img_file_ctime=str(img_file_stat.st_ctime)
                img_file_info='[node]'+img_file+' ['+img_file_size+'] ['+img_file_ctime+']'
                
                self.G_DEBUG_LOG.info(img_file_info)
                #------------server output file----------------
                server_img_file=(server_output+img_file).replace('/','\\')
                server_img_file_info=''
                if os.path.exists(server_img_file):
                    img_file_stat=os.stat(server_img_file)
                    img_file_size=str(os.path.getsize(server_img_file))
                    
                    date = datetime.datetime.fromtimestamp(img_file_stat.st_ctime)  
                    img_file_ctime= date.strftime('%Y%m%d%H%M%S')
                    server_img_file_info='[server]'+img_file+' ['+img_file_size+'] ['+img_file_ctime+']'
                    server_img_dict[img_file]=img_file_size
                else:
                    server_img_file_info='[server]'+img_file+' [missing]'
                
                self.G_DEBUG_LOG.info(server_img_file_info)
                self.G_DEBUG_LOG.info('')
                
        self.G_DEBUG_LOG.info('')
    
    '''
        上传渲染结果和日志
    '''    
    def result_action(self):
        self.G_DEBUG_LOG.info('[BASE.result_action.start.....]')
        #RB_small
        if not os.path.exists(self.G_SMALL_PATH):
            os.makedirs(self.G_SMALL_PATH)
        if self.G_RENDER_OS=='Linux':
            output_path="/output"
            outputbak_path="/outputbak"
            sp_path = 'outputdata5'
            output_folder=self.G_OUTPUT_USER_PATH[self.G_OUTPUT_USER_PATH.rfind(sp_path)+len(sp_path):len(self.G_OUTPUT_USER_PATH)]
            output_mnt_path = self.G_OUTPUT_USER_PATH.replace(output_folder,'').replace('\\','/')
            output_mnt='mount -t cifs -o username=administrator,password=Rayvision@2016,codepage=936,iocharset=gb2312 '+output_mnt_path+' '+output_path
            
            if not os.path.exists(output_path):
                os.makedirs(output_path)
            CLASS_COMMON_UTIL.cmd(output_mnt,my_log=self.G_DEBUG_LOG,my_shell=True)
            
            output_path=output_path+output_folder.replace("\\","/")
            if not os.path.exists(output_path):
                os.makedirs(output_path)
            CLASS_COMMON_UTIL.python_copy(self.G_WORK_RENDER_TASK_OUTPUT,output_path)
            CLASS_COMMON_UTIL.python_copy(self.G_WORK_RENDER_TASK_OUTPUT,self.G_WORK_RENDER_TASK_OUTPUTBAK)
        else:
            output=self.G_OUTPUT_USER_PATH
            if self.G_CG_TILE_COUNT !='1' and self.G_CG_TILE_COUNT!=self.G_CG_TILE:
                output=self.G_TILES_PATH

            cmd1='c:\\fcopy\\FastCopy.exe  /speed=full /force_close  /no_confirm_stop /force_start "' +self.G_WORK_RENDER_TASK_OUTPUT.replace('/','\\') +'" /to="'+output+'"'
            # cmd2='"' +frame_check + '" "' + self.G_WORK_RENDER_TASK_OUTPUT + '" "'+ output.rstrip()+'"'
            cmd3='c:\\fcopy\\FastCopy.exe /cmd=move /speed=full /force_close  /no_confirm_stop /force_start "' +self.G_WORK_RENDER_TASK_OUTPUT.replace('/','\\')+'\\*.*" /to="'+self.G_WORK_RENDER_TASK_OUTPUTBAK.replace('/','\\')+'"'
            
            CLASS_COMMON_UTIL.cmd(cmd1,my_log=self.G_DEBUG_LOG,try_count=3)
            try:
                self.check_result()
            except Exception, e:
                print '[check_result.err]'
                print e
            # CLASS_COMMON_UTIL.cmd(cmd2,my_log=self.G_DEBUG_LOG)
            CLASS_COMMON_UTIL.cmd(cmd3,my_log=self.G_DEBUG_LOG,try_count=3)
        self.G_DEBUG_LOG.info('[BASE.result_action.end.....]')

    def get_convert_r(self,path,oiio_path):
        try:
            cmd=oiio_path+' -info "'+path+'"'
            small_size = '200x0'
            cmdp = subprocess.Popen(cmd,shell = True,stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
            while cmdp.poll()==None:
                result_line = cmdp.stdout.readline().strip()
                if result_line!='':
                    print "-"+result_line
                    info_array = result_line[result_line.rfind(':')+1:result_line.find(',')].split("x")
                    print info_array
                    if int(info_array[0])<int(info_array[0]):
                        small_size = '0x200'
        except Exception, e:
            print '[getoiiosize.err]'
            print e
        return small_size  
      
    '''
        渲染流程控制函数，子类可以覆盖方法
    '''   
    def RB_EXECUTE(self):#total
    
        self.format_log('\r\n--------------------------------------------小任务开始--------------------------------------------\r\n')        
        self.RB_PRE_PY()
        self.RB_MAP_DRIVE()
        self.RB_HAN_FILE()
        self.RB_CONFIG()
        self.RB_RENDER()
        self.RB_CONVERT_SMALL_PIC()
        self.RB_HAN_RESULT()
        self.RB_POST_PY()
        self.RB_KAFKA_NOTIFY()
        self.format_log('\r\n--------------------------------------------小任务结束--------------------------------------------\r\n')
        self.G_DEBUG_LOG.info('[BASE.RB_EXECUTE.end.....]')
        sys.exit(0)