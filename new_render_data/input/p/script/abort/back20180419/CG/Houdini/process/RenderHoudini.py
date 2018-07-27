#!/usr/bin/env python
#encoding:utf-8
# -*- coding: utf-8 -*-
import os,sys,time
import subprocess
from Houdini import Houdini
from HoudiniUtil import HoudiniUtil
from HoudiniPlugin import HoudiniPlugin
from CommonUtil import RBCommon as CLASS_COMMON_UTIL

reload(sys)
sys.setdefaultencoding('utf-8')
class RenderHoudini(Houdini):
    def __init__(self,**paramDict):
        Houdini.__init__(self,**paramDict)
        self.format_log('RenderHoudini.init','start')
        for key,value in self.__dict__.items():
            self.G_DEBUG_LOG.info(key+'='+str(value))


        # --------------------------------------------------------------------

        self._run_code_result = True
        self._erorr_code = ''
        self._erorr_code_info = ''
        self._plugins_surpose = ['Redshift','Arnold']
        self._Killapps =[]
        self._render_frame = 1 # 1: normal,2: mult
        self._error_traceback = []
        self._plant = 'Linux' if self.G_RENDER_OS=='0' else ("win" if self.G_RENDER_OS=='1' else "2")
        HoudiniPlugin.BaseDataSetup(self)

        # --------------------------------------------------------------------

        self.format_log('done','end')


    def ConfigSetup(self):
        self.LogsCreat("ConfigSetup start...")
        try:
            self._ConfigSetup_run_info = ['ConfigSetup']
        except Exception as e:
            self._run_code_result = False
            self._erorr_code = 'ConfigSetup'
            self._erorr_code_info = e



    def RenderCallBack(self):
        # to Render 
        self.LogsCreat("RenderCallBack start...")
        if self._plant == "win":
            hython = "hython.exe" 
        elif self._plant == "Linux":
            hython = "hython"
            source = "%s/function/source.sh"%self._code_base_path
            source_cmd = '%s "%s/%s"'%(source,self._houdini_client_dir,self._hfs_version)
            print(source_cmd)
            os.system(source_cmd)

        if not self.G_ACTION == "Render":
            self._Killapps.append(hython)
            self._run_code_result = False
            self._erorr_code = 'HoudiniFunction process'
            self._erorr_code_info = "Only for render."            

        # cmds 
        softCmd=self._houdini_client_dir+"/"+self._hfs_version+"/bin/%s"%hython
        renderPy=r' %s/script/render.py '% self._code_base_path
        renderproject='-project "%s"' % self._hip_file
        renderrop=' -rop "%s"'%self._rop_node
        renderGPU=' -GPU 1'
        if self._render_frame == 1:
            frames="\""+str(self._frames[0])+" "+str(self._frames[1])+" "+str(self._frames[2])+"\""
        elif self._render_frame == 2:
            frames="\""+str(self._frames[0])+"\""
            # frames="\""+"1,3-7[3],15"+"\""
        renderFrame=' -frame %s' % frames
        renderout=' -outdir "%s"' % self._output
        renderHIP=' -HIP "%s"' % self._hip_save_val
        rendertask = ' -taskbase "%s"'%self._task_folder
        plugindir=' -plugindir "%s"' % self._houdini_PLuing_dirt
        cust_id = ' -custid %s'%self.user_id

        renderCmd=softCmd+renderPy+renderproject+renderrop+renderGPU+renderFrame+renderout+renderHIP+rendertask+plugindir+cust_id
        print("Cmds: %s"%renderCmd)

        self.LogsCreat("Houdini Function process start...")
        self.LogsCreat("...")
        self.LogsCreat(" ")
        self.LogsCreat("Loading Houdini software...")
        # Anacmdcode=subprocess.Popen(renderCmd,stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        returncode,final_info = CLASS_COMMON_UTIL.cmd(renderCmd,None,1,True,True,self.FiltLog)

        if not returncode==0:
            self._Killapps.append("hython.exe")
            self._run_code_result = False
            self._erorr_code = 'HoudiniFunction process'
            self._erorr_code_info = final_info

        self.LogsCreat("[Finished.]",True,False)
        self.LogsCreat("RenderChildren return:"+str(returncode))

        self.LogsCreat("RenderCallBack end.")


    def FiltLog(self,my_popen='',pid=''):
        error_calls = 0
        while my_popen.poll()==None:
            info = my_popen.stdout.readline().strip()
            if info!='':
                torenderlog,todebug = (True,False) if "[HTS]" not in info.strip() else (False,True)
                if torenderlog and "Traceback (most recent call last):" in info:
                    error_calls += 1
                    self.LogsCreat("Error calls...",torenderlog,todebug)
                self.LogsCreat(info,torenderlog,todebug) if not error_calls else (self.LogsCreat(info,False,True),self._error_traceback.append(info))
  
    def Execute_Hfs(self):
        HoudiniPlugin.DataInfo(self)
        if self._run_code_result:
            from HoudiniThread import HoudiniThread
            function_all = {"PluginsSetup":[HoudiniUtil.PluginsSetup,[self]],'AssetSetup':[HoudiniUtil.AssetSetup,[self]],
            'ConfigSetup':[self.ConfigSetup,''],'HoudiniAppSetup':[HoudiniUtil.HoudiniAppSetup,[self]],
            "HoudiniServerSetup":[HoudiniUtil.HoudiniServerSetup,[self]]}
            threads = HoudiniThread.StartThread(HoudiniThread.CreatThread(function_all))
            # HoudiniThread.JoinThread(threads)
        ## -----------------------------------------------------------
        ## ------------- wait to the threads to finish ---------------
            self.LogsCreat(" ")
            for thr in threads[0]:
                thrnmae = thr.name
                self.LogsCreat("%s information:"%thrnmae)
                self.LogsCreat("...")
                thr.join()
                try:
                    exec("info_list =self._%s_run_info"%thrnmae)
                    for info in info_list: self.LogsCreat(info)
                    self.LogsCreat("%s end.\n"%thrnmae)
                except Exception, e:
                    break

        while True:
            if self._app_set_finish==1:
                break
        sys.stdout.flush()
        time.sleep(1)

        if not self._run_code_result:
            self.LogsCreat('')
            self.LogsCreat("Eroor Information: %s"%self._erorr_code_info)
            self.LogsCreat("Eroor Called Code: %s"%self._erorr_code)
            self.LogsCreat('')
            self.LogsCreat('')


    '''
        Rebult 
    '''
    def RB_CONFIG(self):#4
        self.format_log('渲染配置','start')
        self.G_DEBUG_LOG.info('[BASE.RB_CONFIG.start.....]')

        ## setup Houdini software and plugins for analysis
        self.Execute_Hfs()

        if not self._run_code_result:
            self.LogsCreat("Errors calls,try to kill apps...")
            print(self._Killapps)
            if len(self._Killapps):
                mainapp = []
                self._Killapps.extend(mainapp)
                try:
                    CLASS_COMMON_UTIL.kill_app_list(self._Killapps)
                except:
                    pass
                self.G_DEBUG_LOG.info('[BASE.RB_RENDER.end.....]')
            CLASS_COMMON_UTIL.error_exit_log(self.G_DEBUG_LOG,"Execute_Hfs()",123)

        self.G_DEBUG_LOG.info('[BASE.RB_CONFIG.end.....]') 
        self.format_log('done','end')
        
    '''
        Rebult
    '''
    def RB_RENDER(self):#5
        self.format_log('渲染','start')
        self.G_DEBUG_LOG.info('[BASE.RB_RENDER.start.....]')

        self.RenderCallBack()
        if not self._run_code_result:
            self.LogsCreat("Errors calls,try to kill apps...")
        else:
            self.LogsCreat("Job finished,try to kill apps...")
        if len(self._Killapps):
            mainapp = ["hython.exe"]
            self._Killapps.extend(mainapp)
            try:
                CLASS_COMMON_UTIL.kill_app_list(self._Killapps)
            except:
                pass
            self.LogsCreat("[kill apps done]")

        # if errors
        if not self._run_code_result:
            CLASS_COMMON_UTIL.error_exit_log(self.G_DEBUG_LOG,"RenderCallBack()",456)

        self.G_DEBUG_LOG.info('[BASE.RB_RENDER.end.....]')
        self.format_log('done','end')