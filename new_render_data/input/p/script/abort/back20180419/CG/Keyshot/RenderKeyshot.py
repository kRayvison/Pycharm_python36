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
class Keyshot(RenderBase):
	def __init__(self,**paramDict):
		RenderBase.__init__(self,**paramDict)

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
					# self.RBcmd("net use "+key+" "+configJson["mntMap"][key].replace('/','\\'))
					self.RBcmd("net use "+key+" \""+configJson["mntMap"][key].replace('/','\\')+"\"")

	def bulidFile(self):
		self.G_RENDER_LOG.info('[KeyShot.Render.start.....]')
		infoFolder = "D:\\KS\\"
		renderFolder = "C:\\work\\render\\"+self.G_TASKID+"\\KS\\"
		infoPath = infoFolder+"INFO.txt"

		if not os.path.exists(infoFolder):
			os.mkdir(infoFolder)

		if not os.path.exists(renderFolder):
			os.makedirs(renderFolder)

		if os.path.exists(infoPath):
			os.remove(infoPath)

		renderFilePath = renderFolder+"FilePath.txt"
		info=codecs.open(infoPath,'w')
		renderFile=codecs.open(renderFilePath,'w')
		try :
			info.write(self.G_TASKID.encode("UTF-8"))
			renderFile.write(self.cgfile.encode("UTF-8")+"\n")
			renderFile.write(self.G_RENDER_WORK_OUTPUT.encode("UTF-8"))
		finally :
			info.close()
			renderFile.close()

		self.G_RENDER_LOG.info('[KeyShot.Render.end.....]')

	def bulidRenderInfo(self):
		infoModel=os.path.join(self.G_RENDER_WORK_TASK_CFG,'renderinfoModel.txt')
		if os.path.exists(infoModel):
			infoForder="C:\\work\\render\\"+self.G_TASKID+"\\KS\\ifo\\"
			infoFile=infoForder+"renderinfo.txt"
			if not os.path.exists(infoForder):
				os.makedirs(infoForder)
			rb=codecs.open(infoFile,'w') 
			rbModel = codecs.open(infoModel,"r","utf-8")
			try :
				lines = rbModel.readlines()
				for line in lines:
					linestr = line.replace("\r\n","\n")
					if line.startswith("frames"):
						linestr=self.G_CG_START_FRAME+'  ' + self.G_CG_END_FRAME +'  '+self.G_CG_BY_FRAME+'  '+'1\n'
					rb.write(linestr.encode("UTF-8"))
			finally :
				rb.close()
				rbModel.close()

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
		self.G_RENDER_LOG.info('[Keyshot.RBrender.start.....]')
		startTime = time.time()
		
		self.G_FEE_LOG.info('startTime='+str(int(startTime)))
		
		#myCgVersion=self.cgName + self.cgv
		#exePath=os.path.join(r'D:\Program Files',myCgVersion,r'bin\keyshot6.exe')
		#scriptPath = "B:\\plugins\\KeyShot\\lib\\python\\ks_render.py"

		#renderCmd='"'+exePath+'" -script "'+scriptPath.replace("\\","/")+'" '
		mainPyCmd='C:\\Python34\\python.exe "B:\plugins\KeyShot\lib\python\main_render.py"'

		self.RBcmd(mainPyCmd,True,False)
		#self.RBcmd(renderCmd,True,False)

		endTime = time.time()
		self.G_FEE_LOG.info('endTime='+str(int(endTime)))
		self.G_RENDER_LOG.info('[Keyshot.RBrender.end.....]')
		
	def RBexecute(self):#Render
		
		print 'Keyshot.execute.....'
		self.RBBackupPy()
		self.RBinitLog()
		self.G_RENDER_LOG.info('[Keyshot.RBexecute.start.....]')
		
		self.RBprePy()
		self.RBmakeDir()
		self.RBcopyTempFile()
		self.delSubst()
		self.webNetPath()
		self.RBreadCfg()
		self.RBhanFile()
		self.RBrenderConfig()
		self.RBwriteConsumeTxt()

		self.bulidFile()
		self.bulidRenderInfo()
		#self.plugin()

		self.RBrender()
		self.RBconvertSmallPic()
		self.RBhanResult()
		#self.RBpostPy()
		self.G_RENDER_LOG.info('[Keyshot.RBexecute.end.....]')