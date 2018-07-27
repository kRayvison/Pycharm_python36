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
class Vray(RenderBase):
	def __init__(self,**paramDict):
		RenderBase.__init__(self,**paramDict)
		print "Vray INIT"
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
			self.iformat=configJson['common']["iformat"]
			self.cgName=configJson['common']["cgSoftName"]
			projectName= configJson['common']["projectSymbol"]
			replacePath="\\"+projectName+"\\"+self.cgName+"\\"
			if isinstance(configJson["mntMap"],dict):
				self.RBcmd("net use * /del /y")
				for key in configJson["mntMap"]:
					newPath =configJson["mntMap"][key].replace("/","\\").replace(replacePath,"\\")
					# self.RBcmd("net use "+key+" "+newPath)
					self.RBcmd("net use "+key+" \""+newPath+"\"")

	def getPlugin(self):
		if os.path.exists(self.G_PLUGINS):
			configJson=eval(open(self.G_PLUGINS, "r").read())
			if isinstance(configJson["plugins"],dict):
				for key in configJson["plugins"]:
					self.pluginName=key
					self.pluginVersion=configJson["plugins"][key]

	def parseFileName(self,nameStr,frames):
		if "#" in nameStr:
			nameArray=nameStr.split(" ")
			name=nameArray[0]
			end=name.rindex("#")+1
			start=name.index("#")
			restr=name[start:end]
			frameStr=self.formatFrame(frames,"0",end-start,False)
			return name.replace(restr,frameStr)
		else:
			return nameStr

	def formatFrame(self,frame,fillstr,length,append):
		s=frame
		for i in range(length-len(frame)):
			if append:
				s=s+fillstr
			else:
				s=fillstr+s
		return s

	def RBrender(self):#7
		self.G_RENDER_LOG.info('[Vray.RBrender.start.....]')
		startTime = time.time()
		self.G_FEE_LOG.info('startTime='+str(int(startTime)))

		output = self.G_RENDER_WORK_OUTPUT.replace('/','\\')+"\\"+self.outputFileName+"."+self.iformat

		bat='B:\\plugins\\V-Ray_standalone\\vray_stan.bat'

		filePath=self.parseFileName(self.cgfile,self.G_CG_START_FRAME)
		
		renderCmd=bat+' "'+self.G_USERID+'" "'+self.G_TASKID+'" "'+self.pluginName.replace(" for x64","")+'" "'+self.pluginVersion.replace("Vray ","")+'" "'+self.G_CG_START_FRAME+'" "' + self.G_CG_END_FRAME +'" "'+self.G_CG_BY_FRAME +'" "'+filePath+'" "'+output+'"'
		
		self.G_RENDER_LOG.info(renderCmd)
		self.RBcmd(renderCmd,True,False)
		endTime = time.time()
		self.G_FEE_LOG.info('endTime='+str(int(endTime)))
		self.G_RENDER_LOG.info('[Vray.RBrender.end.....]')
		
	def RBexecute(self):#Render
		
		print 'Vray.execute.....'
		self.RBBackupPy()
		self.RBinitLog()
		self.G_RENDER_LOG.info('[Vray.RBexecute.start.....]')
		
		self.RBprePy()
		self.copyBlack()
		self.RBmakeDir()
		self.RBcopyTempFile()
		self.delSubst()
		self.webNetPath()
		self.getPlugin()
		self.RBreadCfg()
		self.RBhanFile()
		self.RBrenderConfig()
		self.RBwriteConsumeTxt()
		self.RBrender()
		self.RBconvertSmallPic()
		self.RBhanResult()
		self.RBpostPy()
		self.G_RENDER_LOG.info('[Blender.RBexecute.end.....]')