import logging
import os
import sys
import subprocess
import string
import logging
import time
import shutil
import commands
from RenderBase import RenderBase

class Maya(RenderBase):
	def __init__(self,**paramDict):
		RenderBase.__init__(self,**paramDict)
		print "MAYA INIT"
		self.G_SCRIPT_NAME='maya_preRender5.mel'
		self.G_RENDERBAT_NAME='render5.bat'
		self.G_PLUGINBAT_NAME='plugin.bat'
		if self.G_RENDEROS=='Linux':
			self.G_RENDERBAT_NAME='render5.sh'
			self.G_PLUGINBAT_NAME='plugin.sh'

	'''
		copy black.xml
	'''
	def copyBlack(self):
		# cmd="xcopy /y /f \"\\\\10.50.1.22\\td\\tools\\sweeper\\black.xml\" \"c:\\work\\munu_client\\sweeper\\\""
		# self.RBcmd(cmd)
		sweeper="c:\\work\\munu_client\\sweeper\\"
		blackPath="\\\\10.50.1.22\\td\\tools\\sweeper\\black.xml"
		if self.G_RENDEROS=='Linux':
			sweeper="/root/rayvision/work/munu_client/sweeper/"
			blackPath="\\B\\tools\\sweeper\\black.xml"
		self.pythonCopy(blackPath,sweeper)

	def RBhanFile(self):#3 copy script,copy from pool,#unpack
		self.G_RENDER_LOG.info('[Maya.RBhanFile.start.....]')
		# moveOutputCmd='c:\\fcopy\\FastCopy.exe /cmd=move /speed=full /force_close  /no_confirm_stop /force_start '+self.G_RENDER_WORK_OUTPUT.replace('/','\\')+' /to='+self.G_RENDER_WORK_OUTPUTBAK.replace('/','\\')
		# self.RBcmd(moveOutputCmd)
		self.pythonCopy(self.G_RENDER_WORK_OUTPUT.replace('\\',"/"),self.G_RENDER_WORK_OUTPUTBAK.replace('\\','/'))
		
		scriptmaya=r'script\maya'
		melFile=os.path.join(self.G_POOL,scriptmaya,self.G_SCRIPT_NAME)
		renderBat=os.path.join(self.G_POOL,scriptmaya,self.G_RENDERBAT_NAME)
		pluginBat=os.path.join(self.G_POOL,scriptmaya,self.G_PLUGINBAT_NAME)
		vbsFile=os.path.join(self.G_POOL,r'script\vbs',self.G_CONVERTVBS_NAME)
		
		mayascript='c:/script/maya'
		vbs="c:/script/vbs/"
		# copyScriptCmd1='xcopy /y /f "'+melFile+'" "'+mayascript+'/" '
		# copyScriptCmd2='xcopy /y /f "'+renderBat+'" "'+mayascript+'/" '
		# copyScriptCmd3='xcopy /y /f "'+pluginBat+'" "'+mayascript+'/" '
		# copyVBSCmd='xcopy /y /f "'+vbsFile+'" "c:/script/vbs/" '
		if self.G_RENDEROS=='Linux':
			mayascript='/root/rayvision/script/maya'
			vbs="/root/rayvision/script/vbs/"
			self.webMntPath()
		else:
			self.webNetPath()
		self.pythonCopy(melFile,mayascript)
		self.pythonCopy(renderBat,mayascript)
		#self.pythonCopy(pluginBat,mayascript)
		self.pythonCopy(vbsFile,vbs)
		
		# self.RBcmd(copyScriptCmd1)
		# self.RBcmd(copyScriptCmd2)
		# self.RBcmd(copyScriptCmd3)
		# self.RBcmd(copyVBSCmd)
		self.G_RENDER_LOG.info('[Maya.RBhanFile.end.....]')
		
	def webMntPath(self):
		# mountFrom='{"Z:":"//192.168.0.94/d"}'
		exitcode = subprocess.call("mount | grep -v '/mnt_rayvision' | awk '/cifs/ {print $3} ' | xargs umount", shell=1)
		if exitcode not in(0,123):
			sys.exit(exitcode)
		#self.RBcmd(umountcmd)

		self.G_RENDER_LOG.info('[config....]'+self.G_CONFIG)
		if os.path.exists(self.G_CONFIG):
			configJson=eval(open(self.G_CONFIG, "r").read())
			self.CGFILE=configJson['common']["cgFile"]
			print configJson
			if isinstance(configJson["mntMap"],dict):
				for key in configJson["mntMap"]:
					if not os.path.exists(key):
						os.makedirs(key)
					cmd='mount -t cifs -o username=enfuzion,password=abc123456,codepage=936,iocharset=gb2312 '+configJson["mntMap"][key].replace('\\','/')+' '+key
					self.G_RENDER_LOG.info(cmd)
					self.RBcmd(cmd,False,1)
					
	def webNetPath(self):
		if os.path.exists(self.G_CONFIG):
			configJson=eval(open(self.G_CONFIG, "r").read())
			print configJson
			if isinstance(configJson["mntMap"],dict):
				self.RBcmd("net use * /del /y")
				for key in configJson["mntMap"]:
					self.RBcmd("net use "+key+" "+configJson["mntMap"][key])		

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
		# self.G_RENDER_LOG.info('kill sweeper.exe')
		# retcode = subprocess.call(r"taskkill /F /IM sweeper.exe /T ",shell=True)
		# self.G_RENDER_LOG.info('start sweeper.exe')
		# retcode = subprocess.call(r"start C:\sweeper\sweeper.exe",shell=True)
		startTime = time.time()
		
		self.G_FEE_LOG.info('startTime='+str(int(startTime)))

		mayaExePath=os.path.join('C:/Program Files/Autodesk',self.G_CG_VERSION,'bin/Render.exe')
		mayaExePath=mayaExePath.replace('\\','/')
		renderTxtFile = os.path.join(self.G_RENDER_WORK_TASK_CFG,os.path.basename(self.G_RENDER_TXTNAME))

		mayascript='c:/script/maya'
		vbs="c:/script/vbs/"
		if self.G_RENDEROS=='Linux':
			mayascript='/root/rayvision/script/maya'
			vbs="/root/rayvision/script/vbs/"
			mayaExePath='/usr/autodesk/'+self.G_CG_VERSION+'-x64/bin/mayapy'
			if not os.path.exists(mayaExePath):
				mayaExePath='/usr/autodesk/'+self.G_CG_VERSION+'/bin/mayapy'
			renderTxtFile = os.path.join(self.G_RENDER_WORK_TASK_CFG,self.G_RENDER_TXTNAME[self.G_RENDER_TXTNAME.rfind("\\")+1:len(self.G_RENDER_TXTNAME)])
		renderTxtFile=renderTxtFile.replace('\\','/')

		melFile=os.path.join(mayascript,self.G_SCRIPT_NAME)
		renderBat=os.path.join(mayascript,self.G_RENDERBAT_NAME)
		pluginBat=os.path.join(mayascript,self.G_PLUGINBAT_NAME)
		vbsFile=os.path.join(vbs,self.G_CONVERTVBS_NAME)
		if os.path.exists(self.G_CONFIG):
			configJson=eval(open(self.G_CONFIG, "r").read())
			if isinstance(configJson["common"],dict):
				self.G_PATH_INPUTFILE=configJson["common"]["cgFile"]
				print self.G_PATH_INPUTFILE
		
		 #C:/script/maya/Render4.bat "$userId"  "$taskId"  "$enginePath/bin/Render.exe" "C:/enfwork/$taskId/sc13_bg_scenes_TXCQ_SQ013_bg_lt_color_0210_cam_M.mb_20140210154833_487211732" $frame  $frame 1  "$projectPath"  "$filePath"  >>$logDir$ENFJOBNAME.txt 2>&1  
		renderCmd=renderBat +' "'+self.G_USERID+'"  "'+self.G_TASKID+'"  "'+mayaExePath+'" "'+renderTxtFile+'" "'+self.G_CG_START_FRAME+'" "' + self.G_CG_END_FRAME +'" "'+self.G_CG_BY_FRAME +'" "'+ self.G_PATH_INPUTPROJECT +'" "'+ self.G_PATH_INPUTFILE+'" "'+ self.G_CONFIG+'" "'+ self.G_PLUGINS+'" '
		
		#os.system(renderCmd)
		self.RBcmd(renderCmd,False,1)
		endTime = time.time()
		self.G_FEE_LOG.info('endTime='+str(int(endTime)))
		self.G_RENDER_LOG.info('[Maya.RBrender.end.....]')
		
	def RBexecute(self):#Render
		self.RBBackupPy()
		self.RBinitLog()
		self.G_RENDER_LOG.info('[MAYA.RBexecute.start...]')
		self.RBprePy()
		self.RBmakeDir()
		self.RBcopyTempFile()
		self.RBreadCfg()
		self.RBhanFile()
		self.copyBlack()
		
		self.RBrenderConfig()
		self.RBwriteConsumeTxt()
		self.RBrender()
	#	self.RBconvertSmallPic()
		self.RBhanResult()
		self.RBpostPy()
		self.G_RENDER_LOG.info('[Maya.RBexecute.end.....]')

#--------------------- maya express--------------------	
class MayaExpress(Maya):
	def RBrender(self):#7
		self.G_RENDER_LOG.info('[Maya.RBrender.start.....]')
		# self.G_RENDER_LOG.info('kill sweeper.exe')
		# retcode = subprocess.call(r"taskkill /F /IM sweeper.exe /T ",shell=True)
		# self.G_RENDER_LOG.info('start sweeper.exe')
		# retcode = subprocess.call(r"start C:\sweeper\sweeper.exe",shell=True)
		startTime = time.time()
		
		self.G_FEE_LOG.info('startTime='+str(int(startTime)))

		mayaExePath=os.path.join('C:/Program Files/Autodesk',self.G_CG_VERSION,'bin/Render.exe')
		mayascript='c:/script/maya'
		vbs="c:/script/vbs/"
		if self.G_RENDEROS=='Linux':
			mayaExePath='/usr/autodesk/'+self.G_CG_VERSION+'-x64/bin/mayapy'
			if not os.path.exists(mayaExePath):
				mayaExePath='/usr/autodesk/'+self.G_CG_VERSION+'/bin/mayapy'
			mayascript='/root/rayvision/script/maya'
			vbs="/root/rayvision/script/vbs/"
		mayaExePath=mayaExePath.replace('\\','/')
			
		melFile=os.path.join(mayascript,self.G_SCRIPT_NAME)
		renderBat=os.path.join(mayascript,self.G_RENDERBAT_NAME)
		pluginBat=os.path.join(mayascript,self.G_PLUGINBAT_NAME)
		vbsFile=os.path.join(vbs,self.G_CONVERTVBS_NAME)
		 #C:/script/maya/Render4.bat "$userId"  "$taskId"  "$enginePath/bin/Render.exe" "C:/enfwork/$taskId/sc13_bg_scenes_TXCQ_SQ013_bg_lt_color_0210_cam_M.mb_20140210154833_487211732" $frame  $frame 1  "$projectPath"  "$filePath"  >>$logDir$ENFJOBNAME.txt 2>&1  
		renderCmd=renderBat +' "'+self.G_USERID+'"  "'+self.G_TASKID+'"  "'+mayaExePath+'" "" "'+self.G_CG_START_FRAME+'" "' + self.G_CG_END_FRAME +'" "'+self.G_CG_BY_FRAME +'" "'+ self.G_PATH_INPUTPROJECT +'" "'+ self.G_PATH_INPUTFILE+'" "'+ self.G_CONFIG+'" '
		
		#os.system(renderCmd)
		self.RBcmd(renderCmd,False,False)
		endTime = time.time()
		self.G_FEE_LOG.info('endTime='+str(int(endTime)))
		self.G_RENDER_LOG.info('[Maya.RBrender.end.....]')
		
		
#--------------------- maya Client--------------------	
class MayaClient(Maya):
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