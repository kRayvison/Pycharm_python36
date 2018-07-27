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
class Softimage(RenderBase):
	def __init__(self,**paramDict):
		RenderBase.__init__(self,**paramDict)
		print "Sofimage INIT"
		self.cgfile=""
		self.outputFileName=""
		self.projectPath=""
		self.cgv=""

	def checkFile(self):
		fileList=self.G_FILELIST.split(",")
		sample_list=[]
		for parent,dirnames,filenames in os.walk(self.projectPath):	#三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
			for filename in filenames:						#输出文件信息
				sample_list.append(filename)
		existCount=0
		notExistCount=0
		for files in fileList:
			isExist = False
			files=files.strip()
			for name in sample_list:
				if files==name:
					isExist=True
			if isExist:
				self.G_RENDER_LOG.info(files+'----exists---')
				existCount=existCount+1
			else:
				self.G_RENDER_LOG.info(files+'----not exists---')
				notExistCount=notExistCount+1
		self.G_RENDER_LOG.info(files+'----notExistsCount---'+str(notExistCount)+'----exists----'+str(existCount))
		if notExistCount>0:
			sys.exit(-1)

	def webNetPath(self):
		if os.path.exists(self.G_CONFIG):
			configJson=eval(open(self.G_CONFIG, "r").read())
			print configJson
			self.cgfile=configJson['common']["cgFile"]
			self.outputFileName=configJson['common']["outputFileName"]
			self.projectPath=configJson['renderSettings']["projectPath"]
			self.cgv=configJson['common']["cgv"]
			self.analyseTxt=configJson['common']["analyseTxt"]
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
		self.G_RENDER_LOG.info('[Sofimage.RBrender.start.....]')
		startTime = time.time()
		self.G_FEE_LOG.info('startTime='+str(int(startTime)))

		output=self.G_RENDER_WORK_OUTPUT.replace("/","\\")
		myCgVersion = r"C:/Program Files/Autodesk/Softimage "+self.cgv
		softimageRenderbat=r'B:\plugins\softimage\script\Render.bat'
		
		renderCmd=softimageRenderbat+' "'+self.G_USERID+'" "'+self.G_TASKID+'" "'+myCgVersion+'" "'+self.analyseTxt.replace("mnt","/10.50.244.116").replace("/","\\")+'" "'+self.G_CG_START_FRAME+'" "'+self.projectPath+'" "'+output+'" "'+self.cgfile.replace("/","\\")+'" "'+self.G_CG_LAYER_NAME+'"'
		
		self.G_RENDER_LOG.info(renderCmd)
		self.RBcmd(renderCmd,True,False)
		endTime = time.time()
		self.G_FEE_LOG.info('endTime='+str(int(endTime)))
		self.G_RENDER_LOG.info('[Sofimage.RBrender.end.....]')
		
	def RBexecute(self):#Render
		
		print 'Sofimage.execute.....'
		self.RBBackupPy()
		self.RBinitLog()
		self.G_RENDER_LOG.info('[Sofimage.RBexecute.start.....]')
		
		self.RBprePy()
		self.RBmakeDir()
		self.RBcopyTempFile()
		self.delSubst()
		self.webNetPath()
		self.RBreadCfg()
		self.RBhanFile()
		self.RBrenderConfig()
		self.RBwriteConsumeTxt()
		self.RBrender()
		self.RBconvertSmallPic()
		self.RBhanResult()
		self.RBpostPy()
		self.G_RENDER_LOG.info('[Sofimage.RBexecute.end.....]')