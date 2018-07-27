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
class Mrstand(RenderBase):
	def __init__(self,**paramDict):
		RenderBase.__init__(self,**paramDict)
		print "Mrstand INIT"
		self.cgfile=""
		self.imageWidth=""
		self.imageHeight=""
		self.projectPath=""
		self.cgv=""
		self.cgName=""

	def webNetPath(self):
		if os.path.exists(self.G_CONFIG):
			configJson=eval(open(self.G_CONFIG, "r").read())
			print configJson
			self.cgfile=configJson['common']["cgFile"]
			self.imageWidth=configJson['common']["imageWidth"]
			self.imageHeight=configJson['common']["imageHeight"]
			self.projectPath=configJson['renderSettings']["projectPath"]
			self.cgv=configJson['common']["cgv"]
			self.cgName=configJson['common']["cgSoftName"]
			projectName= configJson['common']["projectSymbol"]
			replacePath="\\"+projectName+"\\"+self.cgName+"\\"

			if isinstance(configJson["mntMap"],dict):
				self.RBcmd("net use * /del /y")
				for key in configJson["mntMap"]:
					newPath =configJson["mntMap"][key].replace("/","\\").replace(replacePath,"\\")
					# self.RBcmd("net use "+key+" "+newPath)
					self.RBcmd("net use "+key+" \""+newPath+"\"")

	def RBrender(self):#7
		self.G_RENDER_LOG.info('[Mrstand.RBrender.start.....]')
		startTime = time.time()
		self.G_FEE_LOG.info('startTime='+str(int(startTime)))

		output = self.G_RENDER_WORK_OUTPUT.replace('/','\\')

		cgsoft = self.cgName+self.cgv

		bat='B:\\plugins\mentalray_standalone\\mr_stand.bat'
		
		renderCmd=bat+' '+self.G_USERID+' '+self.G_TASKID+' '+self.G_CG_START_FRAME+' ' + self.G_CG_END_FRAME +' '+self.G_CG_BY_FRAME +' '+cgsoft+' "'+output+'" "'+self.projectPath+'" "'+self.cgfile+'" "'+self.imageWidth+'" "'+self.imageHeight+'"'
		self.G_RENDER_LOG.info(renderCmd)
		self.RBcmd(renderCmd,True,False)
		endTime = time.time()
		self.G_FEE_LOG.info('endTime='+str(int(endTime)))
		self.G_RENDER_LOG.info('[Mrstand.RBrender.end.....]')
		
	def RBexecute(self):#Render
		
		print 'Mrstand.execute.....'
		self.RBBackupPy()
		self.RBinitLog()
		self.G_RENDER_LOG.info('[Mrstand.RBexecute.start.....]')
		
		self.RBprePy()
		self.copyBlack()
		self.RBmakeDir()
		self.RBcopyTempFile()
		self.webNetPath()
		self.RBreadCfg()
		self.delSubst()
		self.RBhanFile()
		self.RBrenderConfig()
		self.RBwriteConsumeTxt()
		self.RBrender()
		self.RBconvertSmallPic()
		self.RBhanResult()
		self.RBpostPy()
		self.G_RENDER_LOG.info('[Mrstand.RBexecute.end.....]')