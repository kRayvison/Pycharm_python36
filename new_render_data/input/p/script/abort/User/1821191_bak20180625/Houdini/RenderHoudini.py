import logging
import os
import sys
import subprocess
import string
import logging
import time
import shutil
from RenderBase import RenderBase

class Houdini(RenderBase):
    def __init__(self,**paramDict):
        RenderBase.__init__(self,**paramDict)
        print "Houdini INIT"
        self.G_RENDERBAT_NAME='Erender_HD.bat'
        self.G_DRIVERC_7Z='c:/7-Zip/7z.exe'
        self.CGV="";
        self.CGFILE="";
        self.houdiniScript='c:/script/houdini'

    
    def RBhanFile(self):#3 copy script,copy from pool,#unpack
        self.G_RENDER_LOG.info('[Maya.RBhanFile.start.....]')

        moveOutputCmd='c:\\fcopy\\FastCopy.exe /cmd=move /speed=full /force_close  /no_confirm_stop /force_start '+self.G_RENDER_WORK_OUTPUT.replace('/','\\')+' /to='+self.G_RENDER_WORK_OUTPUTBAK.replace('/','\\')
        self.RBcmd(moveOutputCmd)
        
        scriptHoudini=r'script\houdini'
        renderBat=os.path.join(self.G_POOL,scriptHoudini,self.G_RENDERBAT_NAME)
        
        vbsFile=os.path.join(self.G_POOL,r'script\vbs',self.G_CONVERTVBS_NAME)
        
        copyScriptCmd='xcopy /y /f "'+renderBat+'" "'+self.houdiniScript+'/" '
        copyVBSCmd='xcopy /y /f "'+vbsFile+'" "c:/script/vbs/" '
        
        self.RBcmd(copyScriptCmd)
        self.RBcmd(copyVBSCmd)
        self.G_RENDER_LOG.info('[Maya.RBhanFile.end.....]')
        
    def RBrender(self):#7
        self.G_RENDER_LOG.info('[Maya.RBrender.start.....]')
        startTime = time.time()
        
        self.G_FEE_LOG.info('startTime='+str(int(startTime)))

        renderBat=os.path.join(self.houdiniScript,self.G_RENDERBAT_NAME)
        vbsFile=os.path.join(r'c:/script/vbs',self.G_CONVERTVBS_NAME)
        # "c:/script/Houdini/Erender.bat" "$userId" "$taskId" "$startFrame" "$endFrame" "$frameStep" "$cgv" "$projectPath" "$filePath" "$output"  "$layerName" "$option"" 
        #renderCmd='c:\\Python27\\python.exe '+renderPy +' "'+self.G_USERID+'"  "'+self.G_TASKID+'" "'+self.G_CG_START_FRAME+'" "' + self.G_CG_END_FRAME +'" "'+self.G_CG_BY_FRAME +'" "'+ self.CGFILE+'" "'+self.G_CG_LAYER_NAME+'" "'+self.G_RENDER_WORK_OUTPUT.replace('/','\\')+'" "'+self.G_CG_OPTION+'"' 
        renderCmd ='B:\\plugins\\houdini\\Erender.bat "'+self.G_USERID+'"  "'+self.G_TASKID+'" "'+self.G_CG_START_FRAME+'" "' + self.G_CG_END_FRAME +'" "'+self.G_CG_BY_FRAME +'" "'+ self.CGFILE+'" "'+self.G_CG_LAYER_NAME+'" "'+self.G_RENDER_WORK_OUTPUT.replace('/','\\')+'" "'+self.G_CG_OPTION+'"' 
        if "-R" in self.G_CG_OPTION:
            renderCmd=renderBat +' "'+self.G_USERID+'"  "'+self.G_TASKID+'" "'+self.G_CG_START_FRAME+'" "' + self.G_CG_END_FRAME +'" "'+self.G_CG_BY_FRAME +'" "'+self.CGV+'" "'+ self.G_PATH_INPUTPROJECT +'" "'+ self.CGFILE+'" "' +self.G_RENDER_WORK_OUTPUT+'"  "'+self.G_CG_LAYER_NAME+'" "'+self.G_CG_OPTION+'"' 
        self.G_RENDER_LOG.info(renderCmd)
        #os.system(renderCmd)
        self.RBcmd(renderCmd,True,False)
        endTime = time.time()
        self.G_FEE_LOG.info('endTime='+str(int(endTime)))
        self.G_RENDER_LOG.info('[Maya.RBrender.end.....]')
    
    def webNetPath(self):
        if os.path.exists(self.G_CONFIG):
            print self.G_CONFIG
            configJson=eval(open(self.G_CONFIG, "r").read())
            self.CGFILE=configJson['common']["cgFile"]
            self.CGSOFT=configJson['common']["cgSoftName"]
            self.CGV=configJson['common']["cgv"]
            self.RTASKID=configJson['common']["taskId"]
            print configJson
            if isinstance(configJson["mntMap"],dict):
                self.RBcmd("net use * /del /y")
                for key in configJson["mntMap"]:
                    self.RBcmd("net use "+key+" "+configJson["mntMap"][key])

    def copyHoudiniFile(self):
        cgvName =self.CGV.replace(".","")
        pluginPath="B:\\plugins\\houdini\\apps\\7z\\"+cgvName+".7z"
        localPath = "D:\\plugins\\houdini\\";
        if not os.path.exists(localPath+cgvName+"\\") or not os.listdir(localPath+cgvName+"\\"):
            if not os.path.exists(localPath+cgvName+".7z"):
                copyCmd = 'c:\\fcopy\\FastCopy.exe  /speed=full /force_close  /no_confirm_stop /force_start "' +pluginPath +'" /to="'+localPath+'"'
                self.RBcmd(copyCmd)
            unpackCmd=self.G_DRIVERC_7Z+' x "'+localPath+cgvName+".7z"+'" -y -aos -o"'+localPath+cgvName+'\\"' 
            self.RBcmd(unpackCmd)

    def RBresultAction(self):
        self.G_PROCESS_LOG.info('[BASE.RBresultAction.start.....]')
        #RB_small
        if not os.path.exists(self.G_PATH_SMALL):
            os.makedirs(self.G_PATH_SMALL)
        frameCheck = os.path.join(self.G_POOL,'tools',"SingleFrameCheck.exe")
        feeLogFile=self.G_USERID+'-'+self.G_TASKID+'-'+self.G_JOB_NAME+'.txt'
        feeTxt=os.path.join(self.G_RENDER_WORK_TASK,feeLogFile)
        output=self.G_PATH_USER_OUTPUT
        if self.G_CG_TILECOUNT !='1' and self.G_CG_TILECOUNT!=self.G_CG_TILE:
            output=self.G_PATH_TILES

        cmd1='c:\\fcopy\\FastCopy.exe  /speed=full /force_close  /no_confirm_stop /force_start "' +self.G_RENDER_WORK_OUTPUT.replace('/','\\') +'" /to="'+output+'"'
        cmd2='"' +frameCheck + '" "' + self.G_RENDER_WORK_OUTPUT + '" "'+ output.rstrip()+'"'
        cmd3='c:\\fcopy\\FastCopy.exe /cmd=move /speed=full /force_close  /no_confirm_stop /force_start "' +self.G_RENDER_WORK_OUTPUT.replace('/','\\')+'\\*.*" /to="'+self.G_RENDER_WORK_OUTPUTBAK.replace('/','\\')+'"'
       
        cmd4='xcopy /y /f "'+feeTxt+'" "'+self.G_PATH_COST.replace('/','\\')+'/" '
        
        self.RBTry3cmd(cmd1)
        
        try:
            self.checkResult()
        except Exception, e:
            print '[checkResult.err]'
            print e
        if float(self.G_CG_OPTION) <0:
            self.RBcmd(cmd2)

        self.RBTry3cmd(cmd3)
        self.RBcmd(cmd4)
        self.G_PROCESS_LOG.info('[BASE.RBresultAction.end.....]')

    def RBexecute(self):#Render
        
        print 'Houdini.execute.....'
        self.RBBackupPy()
        self.RBinitLog()
        self.G_RENDER_LOG.info('[Maya.RBexecute.start.....]')
        self.RBprePy()
        self.RBmakeDir()		
        self.RBcopyTempFile()
        self.RBreadCfg()
        self.RBhanFile()
        self.delSubst()
        self.webNetPath()
        #self.copyHoudiniFile()
        self.RBrenderConfig()
        self.RBwriteConsumeTxt()
        self.RBrender()
        self.RBconvertSmallPic()
        self.RBhanResult()
        self.RBpostPy()
        self.G_RENDER_LOG.info('[Maya.RBexecute.start.....]')