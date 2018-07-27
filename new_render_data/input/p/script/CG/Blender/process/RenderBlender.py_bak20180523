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
class Blender(RenderBase):
    def __init__(self,**paramDict):
        RenderBase.__init__(self,**paramDict)
        print "Blender INIT"
        self.cgfile=""
        self.outputFileName=""
        self.projectPath=""
        self.cgv=""

    def webNetPath(self):
        if os.path.exists(self.G_CONFIG):
            configJson=eval(open(self.G_CONFIG, "r").read())
            print configJson
            self.cgfile=configJson['common']["cgFile"]
            self.outputFileName=configJson['common']["outputFileName"]
            self.projectPath=configJson['renderSettings']["projectPath"]
            self.cgv=configJson['common']["cgv"]
            self.analyseTxt=configJson['common']["analyseTxt"]
            self.CGSOFT=configJson['common']["cgSoftName"]
            projectName= configJson['common']["projectSymbol"]
            replacePath="\\"+projectName+"\\"+self.CGSOFT+"\\"
            if isinstance(configJson["mntMap"],dict):
                self.RBcmd("net use * /del /y")
                for key in configJson["mntMap"]:
                    newPath =configJson["mntMap"][key].replace("/","\\").replace(replacePath,"\\")
                    # self.RBcmd("net use "+key+" "+newPath)
                    self.RBcmd("net use "+key+" \""+newPath+"\"")

    def RBrender(self):#7
        self.G_RENDER_LOG.info('[Blender.RBrender.start.....]')
        startTime = time.time()
        self.G_FEE_LOG.info('startTime='+str(int(startTime)))

        myCgVersion = "blender-"+self.cgv
        checkPy=r'B:/plugins/blender/script/render.py'
        exePath=os.path.join(r'B:/plugins/blender/Blender Foundation',myCgVersion,r'blender.exe')
        output=self.G_RENDER_WORK_OUTPUT.replace("\\","/")+"/"
        outputrenderlogFile = os.path.join(self.G_LOG_WORK,self.G_TASKID,(self.G_JOB_NAME+'_render.log')).replace("/", "\\")
        renderCmd='"'+exePath.replace("\\","/")+'" -b "'+self.cgfile+'" -o "'+output+'" -P '+checkPy+' -f "'+self.G_CG_START_FRAME+'" -- "'+self.analyseTxt.replace("mnt","/10.50.244.116").replace("\\","/")+'"' + ' >>' + '"' + outputrenderlogFile +'"'
        
        self.G_PROCESS_LOG.info("Cmds: %s"%renderCmd)
        if self.G_RENDEROS=='Linux':
            self.RBcmd(renderCmd,True,1,myLog=True)
        else:
            ## ------------------------------------------------------------------------------------
            #os.system(renderCmd)
            TL_result = subprocess.Popen(renderCmd,stdin = subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
            TL_result.stdin.write('3/n')
            TL_result.stdin.write('4/n')
            r_err = ''
            while TL_result.poll()==None:
                r_info = TL_result.stdout.readline().strip()
                if not r_info == "":
                    self.G_PROCESS_LOG.info(r_info)
                    r_err = r_info
            #r_result = TL_result.wait()
            r_code = TL_result.returncode
            #r_err = TL_result.stderr.read()
            self.G_PROCESS_LOG.info("RenderCmd return:"+str(r_code))
            if r_code:
                self.G_PROCESS_LOG.info("Error Print :")
                self.G_PROCESS_LOG.info("\n"+r_err+"\n")
        
        #self.G_RENDER_LOG.info(renderCmd)
        #self.RBcmd(renderCmd,True,False)
        endTime = time.time()
        self.G_FEE_LOG.info('endTime='+str(int(endTime)))
        self.G_RENDER_LOG.info('[Blender.RBrender.end.....]')
        
    def RBexecute(self):#Render
        
        print 'Blender.execute.....'
        self.RBBackupPy()
        self.RBinitLog()
        self.G_RENDER_LOG.info('[Blender.RBexecute.start.....]')
        self.RBnodeClean()
        self.RBprePy()
        self.RBmakeDir()
        self.RBcopyTempFile()
        self.delSubst()
        self.webNetPath()
        self.RBreadCfg()
        self.RBhanFile()
        self.RBrenderConfig()
        self.RBwriteConsumeTxt()
        self.resourceMonitor()
        self.RBrender()
        self.RBconvertSmallPic()
        self.RBhanResult()
        self.RBpostPy()
        self.G_RENDER_LOG.info('[Blender.RBexecute.end.....]')