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
class C4D(RenderBase):
	def __init__(self,**paramDict):
		RenderBase.__init__(self,**paramDict)
		print "C4d INIT"
		print "c4d argv"+sys.argv[5]
		self.G_RENDER_LOG.info('[c4d argv]'+sys.argv[5])
		#self.G_IMAGE_WIDTH=""
		#self.G_IMAGE_HEIGHT=""
		self.G_IFORMAT=""
		self.multiPass=""
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
			#self.G_IMAGE_WIDTH=configJson['common']["imageWidth"]
			#self.G_IMAGE_HEIGHT=configJson['common']["imageHeight"]
			self.G_IFORMAT=configJson['common']["iformat"]
			self.multiPass=configJson['common']["multiPass"]
			self.cgfile=configJson['common']["cgFile"]
			self.outputFileName=configJson['common']["outputFileName"]
			self.projectPath=configJson['renderSettings']["projectPath"]
			self.cgv=configJson['common']["cgv"]

			if isinstance(configJson["mntMap"],dict):
				self.RBcmd("net use * /del /y")
				for key in configJson["mntMap"]:
					self.RBcmd("net use "+key+" "+configJson["mntMap"][key])

	def plugin(self):
		if os.path.exists(self.G_PLUGINS):
			configJson=eval(open(self.G_PLUGINS, "r").read())
			if isinstance(configJson["plugins"],dict):
				node=self.getNode()
				myCgVersion = configJson["renderSoftware"] +" "+configJson["softwareVer"]
				for key in configJson["plugins"]:
					cmd = 'B:\\plugins\\C4D\\script\\plugin.bat "'+myCgVersion+'" "'+key+'" "'+configJson["plugins"][key]+'" "'+node+'"'
					self.RBcmd(cmd,True,False)

	def setPluginByPyFile(self):
		if os.path.exists(self.G_PLUGINS):
			configJson=eval(open(self.G_PLUGINS, "r").read())
			if isinstance(configJson["plugins"],dict):
				node=self.getNode()
				myCgVersion = configJson["renderSoftware"] +" "+configJson["softwareVer"]
				for key in configJson["plugins"]:
					self.setPluginByVersion(myCgVersion,key,configJson["plugins"][key],node)
		self.setCustomePlugin()

	def setPluginByVersion(self,softVersion,plugin,pluginVersion,node):
		nomalFilePath = "B:\\plugins\\C4D\\script\\SetCfdPlugin_Normal.py"
		if os.path.exists(nomalFilePath):
			#result = execfile(nomalFilePath)
			cmd = 'python "'+ nomalFilePath +'" "'+softVersion+'" "'+plugin+'" "'+pluginVersion+'" "'+node+'"'
			self.RBcmd(cmd,True,False)
			#if result==1:
				#otherFilePath = "B:\\plugins\\C4D\\other_script\\"+plugin+"\\"+pluginVersion.replace(" ","_")+"\\"+softVersion+"\\SetCfdPlugin_other.py"
				#if os.path.exists(otherFilePath):
					#execfile(otherFilePath,softVersion,plugin,pluginVersion,node)
				#else:
					#self.G_RENDER_LOG.info('[C4D pluginFile not exist....otherFilePath--.]'+otherFilePath)
		else:
			self.G_RENDER_LOG.info('[C4D pluginFile not exist.....nomalFilePath---]'+nomalFilePath)

	def setCustomePlugin(self):
		customFilePath = "B:\\plugins\\C4D\\script\\custom_script\\"+self.G_USERID+"\\SetCfdPlugin_custom.py"
		if os.path.exists(customFilePath):
			#result = execfile(customFilePath)
			cmd = 'python "'+ customFilePath +'"'
			self.RBcmd(cmd,True,False)
			
		else:
			self.G_RENDER_LOG.info('[C4D pluginFile not exist.....customFilePath---]'+customFilePath)	

	def getNode(self):
		node=sys.argv[5]
		if "A" in node or "B" in node or "C" in node or "D" in node or "E" in node or "F" in node:
			return "ABCDEF"
		if "K" in node:
			return "K"
		if "L" in node or "M" in node or "N" in node or "O" in node or "P" in node or "Q" in node:
			return "LNOPQ"
		if "G" in node or "H" in node or "J" in node:
			return "GHJ"
		return "ABCDEF"

	def RBrender(self):#7
		self.G_RENDER_LOG.info('[C4D.RBrender.start.....]')
		startTime = time.time()
		
		self.G_FEE_LOG.info('startTime='+str(int(startTime)))

		if self.outputFileName=="":
			self.outputFileName = os.path.basename(self.cgfile)
		
		myCgVersion = "CINEMA 4D "+self.cgv
		# if myCgVersion.endswith('.64') :
		# 	myCgVersion=myCgVersion.replace('.64','')
		# if myCgVersion.endswith('.32') :
		# 	myCgVersion=myCgVersion.replace('.32','')
		
		outputFile=self.G_RENDER_WORK_OUTPUT.replace("/","\\")+"\\"+self.outputFileName

		c4dExePath=os.path.join(r'C:\Program Files\MAXON',myCgVersion,'CINEMA 4D 64 Bit.exe')
		
		 #C:\Program Files\MAXON\CINEMA 4D R15\CINEMA 4D 64 Bit.exe -noopengl -nogui -frame 1 1 -render \\10.50.1.4\dd\inputData\c4d\162686\Warehouse\pipi\pipi.c4d -oresolution 1920 1080 -oformat TGA -oimage C:\enfwork\213282\output\warehouse_4   
		renderCmd='"'+c4dExePath +'" -noopengl -nogui  -frame '+self.G_CG_START_FRAME+' ' + self.G_CG_END_FRAME +' -render "'+ self.cgfile.replace("/","\\") +'" -oresolution '+self.G_IMAGE_WIDTH+' '+self.G_IMAGE_HEIGHT +' -oformat '+self.G_IFORMAT  +' -oimage "'+outputFile+'"'
		if self.multiPass=="1":
			renderCmd = renderCmd+" -omultipass "+outputFile
		self.G_RENDER_LOG.info(renderCmd)
		#os.system(renderCmd)
		self.RBcmd(renderCmd,True,False)
		endTime = time.time()
		self.G_FEE_LOG.info('endTime='+str(int(endTime)))
		self.G_RENDER_LOG.info('[C4D.RBrender.end.....]')
		
	def RBexecute(self):#Render
		
		print 'C4d.execute.....'
		self.RBBackupPy()
		self.RBinitLog()
		self.G_RENDER_LOG.info('[C4D.RBexecute.start.....]')
		
		self.RBprePy()
		self.RBmakeDir()
		self.RBcopyTempFile()
		self.delSubst()
		self.webNetPath()
		self.RBreadCfg()
		self.RBhanFile()
		self.RBrenderConfig()
		self.RBwriteConsumeTxt()
		#self.plugin()
		self.setPluginByPyFile()
		self.RBrender()
		self.RBconvertSmallPic()
		self.RBhanResult()
		self.RBpostPy()
		self.G_RENDER_LOG.info('[C4D.RBexecute.end.....]')