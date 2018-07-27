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
import codecs
from RenderBase import RenderBase
class Sketchup(RenderBase):
	def __init__(self,**paramDict):
		RenderBase.__init__(self,**paramDict)
		self.renderRbModel=os.path.join(self.G_RENDER_WORK_TASK_CFG,'sketchupRenderModel.rb')
		self.renderRb=os.path.join(self.G_RENDER_WORK_TASK_CFG,'sketchupRender.rb')
		self.G_SKETCHUP_RENDERFILE_NAME='SketchupRenderModule.rb' 
		self.cgfile_local=os.path.join("D:\\work\\render",self.G_TASKID,"sketchup")

	def webNetPath(self):
		if os.path.exists(self.G_CONFIG):
			configJson=eval(open(self.G_CONFIG, "r").read())
			self.cgfile=configJson['common']["cgFile"]
			self.projectPath=configJson['renderSettings']["projectPath"]
			self.cgv=configJson['common']["cgv"]
			self.cgName=configJson['common']["cgSoftName"]

			if isinstance(configJson["mntMap"],dict):
				self.RBcmd("net use * /del /y")
				for key in configJson["mntMap"]:
					self.RBcmd("net use "+key+" \""+configJson["mntMap"][key].replace('/','\\')+"\"")

	def copyCgFile(self):
		self.G_RENDER_LOG.info('[Sketchup.copyFile.....]'+self.cgfile)
		path = self.cgfile
		copyCmd = 'c:\\fcopy\\FastCopy.exe /speed=full /force_close  /no_confirm_stop /force_start "'+path.replace('/','\\')+'" /to="'+self.cgfile_local.replace('/','\\')+'"'
		self.G_RENDER_LOG.info('[Sketchup.copyFile.cmd....]'+copyCmd)
		self.RBcmd(copyCmd.encode(sys.getfilesystemencoding()))

	def bulidRenderRb(self):
		if os.path.exists(self.renderRbModel):
			renderLogDir=os.path.join(self.G_LOG_WORK,self.G_TASKID)
			renderLogPath=os.path.join(renderLogDir,(self.G_JOB_NAME+'_render.txt'))
			rb=codecs.open(self.renderRb,'w') 
			renderType = "1"
			rbModel = codecs.open(self.renderRbModel,"r","utf-8")
			pageName=""
			cgfile_local_name = os.path.join(self.cgfile_local,os.path.basename(self.cgfile))
			try :
				lines = rbModel.readlines()
				for line in lines:
					linestr = line
					if line.startswith("$openfile="):
						linestr='$openfile="'+cgfile_local_name.replace("\\","/")+'"\n'
					elif line.startswith("$currentframe="):
						if renderType=="1":
							linestr='$currentframe='+self.G_CG_START_FRAME+'\n'
						else:
							linestr='$currentframe=0\n'
					elif line.startswith("$logpath"):
						linestr='$logpath="'+renderLogPath.replace("\\","/")+'"\n'
					elif line.startswith("$output_directory") or line.startswith("$outputinf"):
						if renderType=="2":
							path = self.G_RENDER_WORK_OUTPUT.replace("\\","/")+'/'+pageName.replace('"','').replace(' ','')+"/"
							if not os.path.exists(path):
								os.makedirs(path)
							linestr='$output_directory="'+path+'"\n'
						else:
							linestr='$output_directory="'+self.G_RENDER_WORK_OUTPUT.replace("\\","/")+'/"\n'
					elif line.startswith("$use_vray"):
						linestr='$use_vray="'+self.useVray.replace("\\","/")+'"\n'
					#elif line.startswith("$output_name"):
					#	linestr='$output_name="test"\n'
					elif line.startswith("$format") and '"' in line:
						linestr=line.split('"')
						if not linestr[1] =='':
							linestr='$format=".'+linestr[1]+'"\n'
						else:
							linestr='$format=".png"\n'
					elif line.startswith("$renderType="):
						renderType = line.replace('$renderType=','').strip()
					elif line.startswith("$page_name="):
						if renderType=="2":
							pageArray=line.replace('$page_name=','').replace('[','').replace(']','').split(",")
							pageName = pageArray[int(self.G_CG_START_FRAME)].replace("\n","").replace("\r","")
							linestr='$page_name=['+pageName+']\n'
							print 'page_name----'+linestr

					rb.write(linestr.encode("UTF-8"))
			finally :
				rb.close()
				rbModel.close()

	def copyRenderFile(self):
		self.G_RENDER_LOG.info('[Sketchup.copyRenderFile.start.....]')
		renderFile=os.path.join(self.G_POOL,r'script\sketchup',self.G_SKETCHUP_RENDERFILE_NAME)

		copyVBSCmd='xcopy /y /f "'+renderFile+'" "c:/script/sketchup/" '
		self.RBcmd(copyVBSCmd)
		self.G_RENDER_LOG.info('[Sketchup.copyRenderFile.end.....]')

	def plugin(self):
		self.G_RENDER_LOG.info('[self.G_PLUGINS.....]'+self.G_PLUGINS)
		self.useVray='False'
		if os.path.exists(self.G_PLUGINS):
			configJson=eval(open(self.G_PLUGINS, "r").read())
			myCgVersion = configJson["renderSoftware"] +" "+configJson["softwareVer"]
			delCmd='B:\\plugins\\Sketchup\\script\\plugin.bat "'+myCgVersion+'" "del"'
			self.RBcmd(delCmd,True,False)
			if isinstance(configJson["plugins"],dict):
				for key in configJson["plugins"]:
					self.useVray='True'
					cmd = 'B:\\plugins\\Sketchup\\script\\plugin.bat "'+myCgVersion+'" "'+key+'" "'+key+configJson["plugins"][key]+'"'
					self.RBcmd(cmd,True,False)

	def RBrender(self):#7
		self.G_RENDER_LOG.info('[Sketckup.RBrender.start.....]')
		startTime = time.time()
		
		self.G_FEE_LOG.info('startTime='+str(int(startTime)))
		
		#myCgVersion = 'SketchUp '+self.cgv
		myCgVersion=self.cgName +" "+self.cgv
		
		exePath=os.path.join(r'C:\Program Files\SketchUp',myCgVersion,'Sketchup.exe')

		if os.path.exists(exePath):
			print 'exeExist'
		if os.path.exists(self.renderRb.replace("\\","/")):
			print 'rb.exists'
		
		renderCmd='"'+exePath +'" -RubyStartup "'+self.renderRb.replace("\\","/")+'"'
		
		self.G_RENDER_LOG.info(renderCmd)
		
		self.RBcmd(renderCmd,True,False)
		endTime = time.time()
		self.G_FEE_LOG.info('endTime='+str(int(endTime)))
		self.G_RENDER_LOG.info('[Sketckup.RBrender.end.....]')
		
	def RBexecute(self):#Render
		
		print 'Sketckup.execute.....'
		self.RBBackupPy()
		self.RBinitLog()
		self.G_RENDER_LOG.info('[Sketckup.RBexecute.start.....]')
		
		self.RBprePy()
		self.RBmakeDir()
		self.RBcopyTempFile()
		self.delSubst()
		self.webNetPath()
		self.copyCgFile()
		self.RBreadCfg()
		self.RBhanFile()
		self.RBrenderConfig()
		self.RBwriteConsumeTxt()

		self.plugin()
		self.copyRenderFile()
		self.bulidRenderRb()

		self.RBrender()
		self.RBconvertSmallPic()
		self.RBhanResult()
		#self.RBpostPy()
		self.G_RENDER_LOG.info('[Sketckup.RBexecute.end.....]')