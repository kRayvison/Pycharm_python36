#!/usr/bin/env python
#encoding:utf-8
# -*- coding: utf-8 -*-
import os,sys,time
import subprocess
from Keyshot import Keyshot
from KeyshotUtil import KeyshotUtil
from KeyshotPlugin import KeyshotPlugin
from CommonUtil import RBCommon as CLASS_COMMON_UTIL
from imp import reload

#reload(sys)
#sys.setdefaultencoding('utf-8')

class AnalyzeKeyshot(Keyshot):
    def __init__(self,**paramDict):
        Keyshot.__init__(self,**paramDict)
        self.format_log('AnalyzeKeyshot.init','start')
        for key,value in self.__dict__.items():
            self.G_DEBUG_LOG.info(key+'='+str(value))

        # --------------------------------------------------------------------
        self._run_code_result = True
        self._erorr_code = ''
        self._erorr_code_info = ''
        self._plugins_surpose = ['Redshift','Arnold']
        self._Killapps =[]
        self._plant = 'Linux' if self.G_RENDER_OS=='0' else ("win" if self.G_RENDER_OS=='1' else "2")
        KeyshotPlugin.BaseDataSetup(self)
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
    
    
    
    def AnalyzeCallBack(self):
        # to Analyse
        self.LogsCreat("AnalyzeCallBack start...")
        if self._plant == "win":
            exepro = "keyshot.exe"
        elif self._plant == "Linux":
            pass
        # cmds 
        softCmd='"%s/KeyShot%s/bin/%s" -script '%(self._keyshot_client_dir,self._keyshot_version[:1],exepro)
        renderPy=r' %s/script/analyse.py '% self._code_base_path
        renderproject='-project "%s"' % self._bip_file
        renderout=' -outdir "%s"' % self._task_folder
        plugindir=' -plugindir "%s"' % self._keyshot_PLuing_dirt
        cust_id = ' -custid %s'%self.user_id

        renderCmd=softCmd+renderPy+renderproject+renderout+plugindir+cust_id
        self.LogsCreat("Cmds: %s"%renderCmd)
        self.LogsCreat("Keyshot AnalyzeCallBack process start...")
        self.LogsCreat("...\n")
        self.LogsCreat("Loading Keyshot software...")
        # Anacmdcode=subprocess.Popen(renderCmd,stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)

        returncode,final_info = CLASS_COMMON_UTIL.cmd(renderCmd,None,1,True,True,self.FiltLog)

        if not returncode==0:
            self._Killapps.append("keyshot.exe")
            self._run_code_result = False
            self._erorr_code = 'AnalyzeCallBack process'
            self._erorr_code_info = final_info

        self.LogsCreat("[Finished.]",True,False)
        self.LogsCreat("RenderChildren return:"+str(returncode))
        self.LogsCreat("Function end.")

    def FiltLog(self,my_popen='',pid=''):
        error_calls = 0
        while my_popen.poll()==None:
            info = my_popen.stdout.readline().strip()
            if info!='':
                torenderlog,todebug = (True,False) if "[HTS]" not in str(info).strip() else (False,True)
                if torenderlog and "Traceback (most recent call last):" in str(info):
                    error_calls += 1
                    self.LogsCreat("Error calls...",torenderlog,todebug)
                if todebug and "tlspace" in str(info): info = "\n"
                self.LogsCreat(info,torenderlog,todebug) if not error_calls else self.LogsCreat(info,False,True)


    def Execute_Hfs(self):
        KeyshotPlugin.DataInfo(self)
        ## --setup keyshot software--
        if self._run_code_result:
            KeyshotUtil.KeyshotAppSetup(self)

        ## -------------------------------------------------------------------------------------
        sys.stdout.flush()
        time.sleep(1)
        if self._app_set_finish:
            pass
        if not self._run_code_result:
            self.LogsCreat('')
            self.LogsCreat("Eroor Information: %s"%self._erorr_code_info)
            self.LogsCreat("Eroor Called Code: %s"%self._erorr_code)
            self.LogsCreat('')
            self.LogsCreat('')
        ## ------------------------------------------------------------------------------------


    ## -----------------------------------------------------
    ## Rebult 
    def RB_CONFIG(self):#4
        self.format_log('渲染配置','start')
        self.G_DEBUG_LOG.info('[BASE.RB_CONFIG.start.....]')

        ## setup Keyshot software and plugins for analysis
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
        
    ## Rebult
    def RB_RENDER(self):#5
        self.format_log('渲染','start')
        self.G_DEBUG_LOG.info('[BASE.RB_RENDER.start.....]')

        self.AnalyzeCallBack()
        if not self._run_code_result:
            self.LogsCreat("Errors calls,try to kill apps...")
        else:
            self.LogsCreat("Job finished,try to kill apps...")
        if len(self._Killapps):
            mainapp = []
            self._Killapps.extend(mainapp)
            try:
                CLASS_COMMON_UTIL.kill_app_list(self._Killapps)
            except:
                pass
            self.LogsCreat("[kill apps done]")

        # if errors
        if not self._run_code_result:
            CLASS_COMMON_UTIL.error_exit_log(self.G_DEBUG_LOG,"AnalyzeCallBack()",456)

        self.G_DEBUG_LOG.info('[BASE.RB_RENDER.end.....]')
        self.format_log('done','end')

    ## -----------------------------------------------------