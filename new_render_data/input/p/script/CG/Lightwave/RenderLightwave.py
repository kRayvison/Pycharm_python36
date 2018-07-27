import logging
import os
import sys
import subprocess
import string
import logging
import time
import shutil
from RenderBase import RenderBase

class Lightwave(RenderBase):
	def __init__(self,**paramDict):
		RenderBase.__init__(self,**paramDict)
		print "MAYA INIT"
		self.G_SCRIPT_NAME='maya_preRender5.mel'
		self.G_RENDERBAT_NAME='render5.bat'
		self.G_PLUGINBAT_NAME='plugin.bat'

	
	def RBhanFile(self):#3 copy script,copy from pool,#unpack
		self.delSubst()
		self.G_RENDER_LOG.info('[Maya.RBhanFile.start.....]')
		moveOutputCmd='c:\\fcopy\\FastCopy.exe /cmd=move /speed=full /force_close  /no_confirm_stop /force_start '+self.G_RENDER_WORK_OUTPUT.replace('/','\\')+' /to='+self.G_RENDER_WORK_OUTPUTBAK.replace('/','\\')
		self.RBcmd(moveOutputCmd)
		
		scriptmaya=r'script\maya'
		melFile=os.path.join(self.G_POOL,scriptmaya,self.G_SCRIPT_NAME)
		renderBat=os.path.join(self.G_POOL,scriptmaya,self.G_RENDERBAT_NAME)
		pluginBat=os.path.join(self.G_POOL,scriptmaya,self.G_PLUGINBAT_NAME)
		vbsFile=os.path.join(self.G_POOL,r'script\vbs',self.G_CONVERTVBS_NAME)
		
		mayascript='c:/script/maya'
		copyScriptCmd1='xcopy /y /f "'+melFile+'" "'+mayascript+'/" '
		copyScriptCmd2='xcopy /y /f "'+renderBat+'" "'+mayascript+'/" '
		copyScriptCmd3='xcopy /y /f "'+pluginBat+'" "'+mayascript+'/" '
		copyVBSCmd='xcopy /y /f "'+vbsFile+'" "c:/script/vbs/" '
		
		if os.path.exists(self.G_CONFIG):
			configJson=eval(open(self.G_CONFIG, "r").read())
			print configJson
			self.CGSOFT=configJson['common']["cgSoftName"]
			projectName= configJson['common']["projectSymbol"]
			replacePath="\\"+projectName+"\\"+self.CGSOFT+"\\"
			if isinstance(configJson["mntMap"],dict):
				self.RBcmd("net use * /del /y")
				for key in configJson["mntMap"]:
					newPath =configJson["mntMap"][key].replace("/","\\").replace(replacePath,"\\")
					# self.RBcmd("net use "+key+" "+newPath)
					self.RBcmd("net use "+key+" \""+newPath+"\"")

		
		self.RBcmd(copyScriptCmd1)
		self.RBcmd(copyScriptCmd2)
		self.RBcmd(copyScriptCmd3)
		self.RBcmd(copyVBSCmd)
		self.G_RENDER_LOG.info('[Maya.RBhanFile.end.....]')
		
		
	def RBrenderConfig(self):#5
		self.G_RENDER_LOG.info('[Maya.RBrenderConfig.start.....]')
		#multicatter = getattr(self,'G_CG_SCATTER')
		if hasattr(self,'G_CG_RENDER_VERSION'):
			if self.G_CG_RENDER_VERSION.startswith('arnold'):
				self.G_RENDER_LOG.info('[Maya.RBrenderConfig.arnold.start.....]')
				shortRenderVersion=self.G_CG_RENDER_VERSION.replace('arnold','')
				configMultCmd='c:/script/maya/'+self.G_PLUGINBAT_NAME+' "'+self.G_CG_VERSION+'" '+' "arnold" "' +shortRenderVersion+'"'
				self.RBcmd(configMultCmd)
				self.G_RENDER_LOG.info('[Maya.RBrenderConfig.arnold.end.....]')
		self.G_RENDER_LOG.info('[Maya.RBrenderConfig.end.....]')
		
	def RBrender(self):#7
		self.G_RENDER_LOG.info('[Maya.RBrender.start.....]')
		startTime = time.time()
		
		self.G_FEE_LOG.info('startTime='+str(int(startTime)))

		mayaExePath=os.path.join('B:/NewTek/',self.G_CG_VERSION,'bin/lwsn.exe')
		mayaExePath=mayaExePath.replace('\\','/')
		renderTxtFile = ""
		#os.path.join(self.G_RENDER_WORK_TASK_CFG,os.path.basename(self.G_RENDER_TXTNAME))
		#renderTxtFile=renderTxtFile.replace('\\','/')
		
		mayascript='c:/script/maya'
		melFile=os.path.join(mayascript,self.G_SCRIPT_NAME)
		renderBat=os.path.join(mayascript,self.G_RENDERBAT_NAME)
		pluginBat=os.path.join(mayascript,self.G_PLUGINBAT_NAME)
		vbsFile=os.path.join(r'c:/script/vbs',self.G_CONVERTVBS_NAME)
		 #C:/script/maya/Render4.bat "$userId"  "$taskId"  "$enginePath/bin/Render.exe" "C:/enfwork/$taskId/sc13_bg_scenes_TXCQ_SQ013_bg_lt_color_0210_cam_M.mb_20140210154833_487211732" $frame  $frame 1  "$projectPath"  "$filePath"  >>$logDir$ENFJOBNAME.txt 2>&1  
		renderCmd=renderBat +' "'+self.G_USERID+'"  "'+self.G_TASKID+'"  "'+mayaExePath+'" "'+renderTxtFile+'" "'+self.G_CG_START_FRAME+'" "' + self.G_CG_END_FRAME +'" "'+self.G_CG_BY_FRAME +'" "'+ self.G_PATH_INPUTPROJECT +'" "'+ self.G_PATH_INPUTFILE+'" "'+ self.G_CONFIG+'" "'+ self.G_PLUGINS+'" '
		
		#os.system(renderCmd)
		self.RBcmd(renderCmd,False,False)
		endTime = time.time()
		self.G_FEE_LOG.info('endTime='+str(int(endTime)))
		self.G_RENDER_LOG.info('[Maya.RBrender.end.....]')

	def RBresultAction(self):
		self.G_PROCESS_LOG.info('[BASE.RBresultAction.start.....]')
		#RB_small
		if not os.path.exists(self.G_PATH_SMALL):
			os.makedirs(self.G_PATH_SMALL)
		frameCheck = os.path.join(self.G_POOL,'tools',self.G_SINGLE_FRAME_CHECK)
		feeLogFile=self.G_USERID+'-'+self.G_TASKID+'-'+self.G_JOB_NAME+'.txt'
		feeTxt=os.path.join(self.G_RENDER_WORK_TASK,feeLogFile)
		
		cmd1='c:\\fcopy\\FastCopy.exe  /speed=full /force_close  /no_confirm_stop /force_start "' +self.G_RENDER_WORK_OUTPUT.replace('/','\\') +'" /to="'+self.G_PATH_USER_OUTPUT+'"'
		cmd2='"' +frameCheck + '" "' + self.G_RENDER_WORK_OUTPUT + '" "'+ self.G_PATH_USER_OUTPUT+'"'
		cmd3='c:\\fcopy\\FastCopy.exe /cmd=move /speed=full /force_close  /no_confirm_stop /force_start "' +self.G_RENDER_WORK_OUTPUT.replace('/','\\')+'\\*.*" /to="'+self.G_RENDER_WORK_OUTPUTBAK.replace('/','\\')+'"'

		cmd4='xcopy /y /f "'+feeTxt+'" "'+self.G_PATH_COST+'/" '

		self.RBTry3cmd(cmd1)
		self.RBcmd(cmd2)
		self.RBTry3cmd(cmd3)
		self.RBcmd(cmd4)
		self.G_PROCESS_LOG.info('[BASE.RBresultAction.end.....]')
		
	def RBexecute(self):#Render
		self.RBBackupPy()
		self.RBinitLog()
		self.G_RENDER_LOG.info('[MAYA.RBexecute.start...]')
		self.RBprePy()
		self.RBmakeDir()
		
		self.RBcopyTempFile()
		self.RBreadCfg()
		self.RBhanFile()
		
		
		self.RBrenderConfig()
		self.RBwriteConsumeTxt()
		self.RBrender()
		self.RBconvertSmallPic()
		self.RBhanResult()
		self.RBpostPy()
		self.G_RENDER_LOG.info('[Maya.RBexecute.end.....]')

#--------------------- maya express--------------------	
class LightwaveExpress(Lightwave):
	def RBrender(self):#7
		self.G_RENDER_LOG.info('[Maya.RBrender.start.....]')
		startTime = time.time()
		
		self.G_FEE_LOG.info('startTime='+str(int(startTime)))

		mayaExePath=os.path.join('C:/Program Files/Autodesk',self.G_CG_VERSION,'bin/Render.exe')
		mayaExePath=mayaExePath.replace('\\','/')
		mayascript='c:/script/maya'
		melFile=os.path.join(mayascript,self.G_SCRIPT_NAME)
		renderBat=os.path.join(mayascript,self.G_RENDERBAT_NAME)
		pluginBat=os.path.join(mayascript,self.G_PLUGINBAT_NAME)
		vbsFile=os.path.join(r'c:/script/vbs',self.G_CONVERTVBS_NAME)
		 #C:/script/maya/Render4.bat "$userId"  "$taskId"  "$enginePath/bin/Render.exe" "C:/enfwork/$taskId/sc13_bg_scenes_TXCQ_SQ013_bg_lt_color_0210_cam_M.mb_20140210154833_487211732" $frame  $frame 1  "$projectPath"  "$filePath"  >>$logDir$ENFJOBNAME.txt 2>&1  
		renderCmd=renderBat +' "'+self.G_USERID+'"  "'+self.G_TASKID+'"  "'+mayaExePath+'" "" "'+self.G_CG_START_FRAME+'" "' + self.G_CG_END_FRAME +'" "'+self.G_CG_BY_FRAME +'" "'+ self.G_PATH_INPUTPROJECT +'" "'+ self.G_PATH_INPUTFILE+'" "'+ self.G_CONFIG+'" '
		
		#os.system(renderCmd)
		self.RBcmd(renderCmd,False,False)
		endTime = time.time()
		self.G_FEE_LOG.info('endTime='+str(int(endTime)))
		self.G_RENDER_LOG.info('[Maya.RBrender.end.....]')
		
		
#--------------------- maya Client--------------------	
class LightwaveClient(Lightwave):
	def __init__(self,**paramDict):
		RenderBase.__init__(self,**paramDict)
		print "MAYA INIT"
		self.G_SCRIPT_NAME='maya_preRender5.mel'
		self.G_RENDERBAT_NAME='crender.bat'
		self.G_PLUGINBAT_NAME='plugin.bat'
	def RBrender(self):#7
		self.G_RENDER_LOG.info('[Maya.RBrender.start.....]')
		startTime = time.time()
		
		self.G_FEE_LOG.info('startTime='+str(int(startTime)))
		self.G_RENDER_LOG.info('[G_CG_VERSION.....]'+self.G_CG_VERSION)
		mayaExePath=os.path.join('C:/Program Files/Autodesk',self.G_CG_VERSION,'bin/Render.exe')
		self.G_RENDER_LOG.info('[G_CG_VERSION.....]'+mayaExePath)
		mayaExePath=mayaExePath.replace('\\','/')
		mayascript='c:/script/maya'
		melFile=os.path.join(mayascript,self.G_SCRIPT_NAME)
		renderBat=os.path.join(mayascript,self.G_RENDERBAT_NAME)
		pluginBat=os.path.join(mayascript,self.G_PLUGINBAT_NAME)
		vbsFile=os.path.join(r'c:/script/vbs',self.G_CONVERTVBS_NAME)
		 #C:/script/maya/Render4.bat "$userId"  "$taskId"  "$enginePath/bin/Render.exe" "C:/enfwork/$taskId/sc13_bg_scenes_TXCQ_SQ013_bg_lt_color_0210_cam_M.mb_20140210154833_487211732" $frame  $frame 1  "$projectPath"  "$filePath"  >>$logDir$ENFJOBNAME.txt 2>&1  
		renderCmd=renderBat +' "'+self.G_USERID+'"  "'+self.G_TASKID+'"  "'+mayaExePath+'" "" "'+self.G_CG_START_FRAME+'" "' + self.G_CG_END_FRAME +'" "'+self.G_CG_BY_FRAME +'" "'+ self.G_PATH_INPUTPROJECT +'" "'+ self.G_PATH_INPUTFILE+'" '
		
		#os.system(renderCmd)
		self.RBcmd(renderCmd,False,False)
		endTime = time.time()
		self.G_FEE_LOG.info('endTime='+str(int(endTime)))
		self.G_RENDER_LOG.info('[Maya.RBrender.end.....]')