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
class Clarisse(RenderBase):
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

	def webMntPath(self):
		# mountFrom='{"Z:":"//192.168.0.94/d"}'
		exitcode = subprocess.call("mount | grep -v '/mnt_rayvision' | awk '/cifs/ {print $3} ' | xargs umount", shell=1)
		if exitcode not in(0,123):
			sys.exit(exitcode)
		#self.RBcmd(umountcmd)

		self.G_RENDER_LOG.info('[config....]'+self.G_CONFIG)
		self.G_CONFIG = self.G_CONFIG.replace("\\","/")
		if os.path.exists(self.G_CONFIG):
			configJson=eval(open(self.G_CONFIG, "r").read())
			self.cgfile=configJson['common']["cgFile"]
			self.projectPath=configJson['renderSettings']["projectPath"]
			self.cgv=configJson['common']["cgv"]
			self.cgName=configJson['common']["cgSoftName"]
			print configJson
			if isinstance(configJson["mntMap"],dict):
				for key in configJson["mntMap"]:
					if not os.path.exists(key):
						os.makedirs(key)
					cmd='mount -t cifs -o username=enfuzion,password=ruiyun2016,codepage=936,iocharset=gb2312 '+configJson["mntMap"][key].replace('\\','/')+' '+key
					self.G_RENDER_LOG.info(cmd)
					self.RBcmd(cmd,False,1)
		
	def RBrender(self):#7
		self.G_PROCESS_LOG.info('[Clarisse.RBrender.start.....]'+self.G_CG_OPTION)
		startTime = time.time()
		
		self.G_FEE_LOG.info('startTime='+str(int(startTime)))
		
		myCgVersion = self.cgName.replace("_"," ")+self.cgv

		exePath=os.path.join(r'D:\plugins\clarisse',myCgVersion,r'Clarisse\cnode.exe')
		if self.G_RENDEROS=='Linux':
			exePath=r'/usr/isotropix/'+self.cgName[:-1]+'/clarisse_'+self.cgv+'/clarisse/cnode'

		fileName = self.G_CG_OPTION+".####.exr"
		#if fileName=="":
		#	fileName='.####.exr'
		folder = os.path.join(self.G_RENDER_WORK_OUTPUT,os.path.basename(self.G_CG_LAYER_NAME))
		output = os.path.join(folder,fileName)#
		if not os.path.exists(folder):
			os.makedirs(folder)

		if os.path.exists(exePath):
			print 'exeExist'
		pypath = "/B/plugins/clarisee/lib/python/clarisee_render.py"

		#B:\plugins\clarisee\lib\python
		renderCmd='"'+exePath +'" "'+self.cgfile.replace("\\","/")+'" -image "'+ self.G_CG_LAYER_NAME +'" -texture_cache 51200 -start_frame "'+self.G_CG_START_FRAME+'" -end_frame "'+self.G_CG_END_FRAME+'" -output "'+output.replace("\\","/")+'"'
		if self.G_RENDEROS=='Linux':
			renderCmd = 'python "'+pypath +'" -project "'+self.cgfile.replace("\\","/")+'" -image "'+ self.G_CG_LAYER_NAME +'" -frame "'+self.G_CG_START_FRAME+'" -outdir "'+self.G_RENDER_WORK_OUTPUT.replace("\\","/")+'"'
		
		self.G_RENDER_LOG.info(renderCmd)
		
		self.RBcmd(renderCmd,False,1)
		endTime = time.time()
		self.G_FEE_LOG.info('endTime='+str(int(endTime)))
		self.G_RENDER_LOG.info('[Clarisse.RBrender.end.....]')

	def clean(self):
		myCgVersion = self.cgName.replace("_"," ")+self.cgv
		cleanCmd='"C:/Python27/python.exe" "B:\\plugins\\clarisee\\lib\\python\\clearnlic.py" "'+myCgVersion+'"'
		self.RBcmd(cleanCmd,True)

	def copySoft(self):
		cmd = 'c:\\python27\\python.exe "B:\\plugins\\clarisee\\lib\\python\\Setupapps_win.py" "'+self.cgName.replace("_"," ")+self.cgv +'"' 
		self.G_RENDER_LOG.info('[cmd....]'+cmd)
		self.RBcmd(cmd,False,1)
	
	'''
		
	'''	
	def RBcmd(self,cmdStr,continueOnErr=False,myShell=False):#continueOnErr=true-->not exit ; continueOnErr=false--> exit 
		print str(continueOnErr)+'--->>>'+str(myShell)
		self.G_PROCESS_LOG.info('cmd...'+cmdStr)
		cmdp=subprocess.Popen(cmdStr,stdin = subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.STDOUT, shell = myShell)
		cmdp.stdin.write('3/n')
		cmdp.stdin.write('4/n')
		while cmdp.poll()==None:
			resultLine = cmdp.stdout.readline().strip()
			if resultLine!='':
				self.G_PROCESS_LOG.info(resultLine)
			
		resultStr = cmdp.stdout.read()
		resultCode = cmdp.returncode
		
		self.G_PROCESS_LOG.info('resultStr...'+resultStr)
		self.G_PROCESS_LOG.info('resultCode...'+str(resultCode))
		
		if not continueOnErr:
			if resultCode!=0:
				self.clean()
				sys.exit(resultCode)
		return resultStr

	def RBexecute(self):#Render
		
		print 'Clarisse.execute.....'
		self.RBBackupPy()
		self.RBinitLog()
		self.G_RENDER_LOG.info('[Clarisse.RBexecute.start.....]')
		self.RBprePy()
		self.RBmakeDir()
		self.RBcopyTempFile()
		if self.G_RENDEROS=='Linux':
			self.webMntPath();
		else:
			self.delSubst()
			self.webNetPath()
			self.copySoft()
		self.RBreadCfg()
		self.RBhanFile()
		self.RBrenderConfig()
		self.RBwriteConsumeTxt()
		self.RBrender()
		self.clean()
		if not self.G_RENDEROS=='Linux':
			self.RBconvertSmallPic()
		self.RBhanResult()
		#self.RBpostPy()
		self.G_RENDER_LOG.info('[Clarisse.RBexecute.end.....]')