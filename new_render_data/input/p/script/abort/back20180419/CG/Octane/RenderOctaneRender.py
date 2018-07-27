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
class OctaneRender(RenderBase):
	def __init__(self,**paramDict):
		RenderBase.__init__(self,**paramDict)
		print "OctaneRender INIT"
		self.G_RENDER_LOG.info('[OctaneRender argv]'+sys.argv[5])
		self.G_IFORMAT=""
		self.multiPass=""
		self.cgfile=""
		self.outputFileName=""
		self.projectPath=""
		self.cgv=""

	def webNetPath(self):
		if os.path.exists(self.G_CONFIG):
			configJson=eval(open(self.G_CONFIG, "r").read())
			self.G_IMAGE_WIDTH=configJson['common']["imageWidth"]
			self.G_IMAGE_HEIGHT=configJson['common']["imageHeight"]
			self.G_IFORMAT=configJson['common']["iformat"]
			self.multiPass=configJson['common']["multiPass"]
			self.cgfile=configJson['common']["cgFile"]
			self.outputFileName=configJson['common']["outputFileName"]
			self.projectPath=configJson['renderSettings']["projectPath"]
			self.cgv=configJson['common']["cgv"]

			if isinstance(configJson["mntMap"],dict):
				if not self.G_RENDERTYPE=="gpu":
					self.RBcmd("net use * /del /y")
				for key in configJson["mntMap"]:
					try:
						# self.RBcmd("net use "+key+" "+configJson["mntMap"][key].replace('/','\\'))
						self.RBcmd("net use "+key+" \""+configJson["mntMap"][key].replace('/','\\')+"\"")
					except:
						self.G_RENDER_LOG.info('cannot mapping disk'+key+' is in used'+configJson["mntMap"][key])
						pass

	def RBrender(self):#7
		self.G_RENDER_LOG.info('[OctaneRender.RBrender.start.....]')

		startTime = time.time()
		self.G_FEE_LOG.info('startTime='+str(int(startTime)))
		
		myCgVersion = "OctaneRender "+self.cgv
		exePath=os.path.join(r'C:\Program Files\OTOY',myCgVersion,'octane.exe')
		option=""
		fileName = self.G_CG_LAYER_NAME+self.G_CG_START_FRAME.zfill(4)
		output = os.path.join(self.G_RENDER_WORK_OUTPUT,self.G_CG_LAYER_NAME).replace('/','\\')
		if not os.path.exists(output):
			os.makedirs(output)
		#if self.G_CG_OPTION.startswith("-o"):
		option = self.G_CG_OPTION.replace(".iformat",".png").replace(".exr-tm",".exr").replace(".png16",".png")
	
		if "outputPath-" in self.G_CG_OPTION:
			option = option.replace('outputPath-',output+"\\")
			option = option.replace("####",self.G_CG_START_FRAME.zfill(4))
		if "outputFile-" in self.G_CG_OPTION:
			option = option.replace('outputFile-',os.path.join(output,fileName))
		
		print option
		 #C:\Program Files\MAXON\CINEMA 4D R15\CINEMA 4D 64 Bit.exe -noopengl -nogui -frame 1 1 -render \\10.50.1.4\dd\inputData\c4d\162686\Warehouse\pipi\pipi.c4d -oresolution 1920 1080 -oformat TGA -oimage C:\enfwork\213282\output\warehouse_4   
		renderCmd='"'+exePath +'" "'+ self.getRealFile().replace("/","\\") +'" -t "'+self.G_CG_LAYER_NAME+'" '+option+' -e'
		if self.multiPass=="1":
			renderCmd = renderCmd+" -omultipass "+outputFile
		self.G_RENDER_LOG.info(renderCmd)
		#os.system(renderCmd)
		self.RBcmd(renderCmd,True,False)
		endTime = time.time()
		self.G_FEE_LOG.info('endTime='+str(int(endTime)))
		self.G_RENDER_LOG.info('[OctaneRender.RBrender.end.....]')

	def getRealFile(self):
		if "#" in self.cgfile:
			restr = self.cgfile[self.cgfile.find("#"):self.cgfile.rfind("#")+1]
			index = len(restr)
			return self.cgfile[:self.cgfile.rfind("ocs")+3].replace(restr, self.G_CG_START_FRAME.zfill(index))
		else:
			return self.cgfile

	def gpuDelNet(self):
		self.G_PROCESS_LOG.info('gpu...delNetUse')
		userFilePath = "D:\\work\\user\\userId.txt"
		userId=self.G_USERID
		isSame=False
		if os.path.exists(userFilePath):
			rbModel = codecs.open(userFilePath,"r","utf-8")
			lines = rbModel.readlines()
			for line in lines:
				if userId in line:
					isSame = True
			rbModel.close()
		if not isSame:
			folder = "D:\\work\\user\\";
			if not os.path.exists(folder):
				os.makedirs(folder) 
			self.delNetUse()
			rb=codecs.open(userFilePath,'w') 
			try :
				rb.write(userId.encode("UTF-8"))
			finally :
				rb.close()
	
	def exepy(self):
		pypath="B:\plugins\octane_Standalone\script\Octane_lic_copy.py";
		pycmd = 'python "'+pypath+'"'
		self.RBcmd(pycmd)

	def RBexecute(self):#Render
		
		print 'OctaneRender.execute.....'
		self.RBBackupPy()
		self.RBinitLog()
		self.G_RENDER_LOG.info('[OctaneRender.RBexecute.start.....]')
		
		self.RBprePy()
		self.RBmakeDir()
		self.RBcopyTempFile()
		if not self.G_RENDERTYPE=="gpu":
			print 'no Subst-------sdsd'
			self.delSubst()
			self.delNetUse()
		else:
			self.gpuDelNet()
		self.webNetPath()
		self.exepy()
		self.RBreadCfg()
		self.RBhanFile()
		self.RBrenderConfig()
		self.RBwriteConsumeTxt()
		self.RBrender()
		self.RBconvertSmallPic()
		self.RBhanResult()
		self.RBpostPy()
		self.G_RENDER_LOG.info('[OctaneRender.RBexecute.end.....]')