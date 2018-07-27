#!/usr/bin/env python
#encoding:utf-8
# -*- coding: utf-8 -*-
import logging
import os
import sys
import subprocess
import string
import logging
import time
import shutil
import commands
import re
import time
from RenderBase import RenderBase

reload(sys)
sys.setdefaultencoding('utf-8')

class Katana(RenderBase):
	def __init__(self,**paramDict):
		RenderBase.__init__(self,**paramDict)
		print "Katana INIT"
		self.render_py_name="katana_render.py"
		self.python_path="python"
		self.script_name="katana_script.py"
		self.denoiseRender_py_name="denoise_render.py"

		# self.renderPyPath="c:/script/katana"
		# self.renderScriptPath="c:/script/katana"
		self.G_NODE_PY = paramDict['G_NODE_PY']
		self.G_CG_NAME = paramDict['G_CG_NAME']
		
		self.renderPyPath=self.G_NODE_PY + "/" + self.G_CG_NAME + "/lib"
		self.renderScriptPath=self.renderPyPath
		
		#self.G_RENDER_WORK_OUTPUT = self.G_CG_OPTION.replace("\\","/")+"/"
		print self.G_RENDER_WORK_OUTPUT

	'''
		copy black.xml
	'''
	def copyBlack(self):
		sweeper="c:\\work\\munu_client\\sweeper\\"
		blackPath="\\\\10.50.1.22\\td\\tools\\sweeper\\black.xml"
		if self.G_RENDEROS=='Linux':
			sweeper="/root/rayvision/work/munu_client/sweeper/"
			blackPath="\\B\\tools\\sweeper\\black.xml"
		self.pythonCopy(blackPath,sweeper)

	def RBhanFile(self):#3 copy script,copy from pool,#unpack
		self.G_RENDER_LOG.info('[Katana.RBhanFile.start.....]')
		
		self.pythonCopy(self.G_RENDER_WORK_OUTPUT.replace('\\',"/"),self.G_RENDER_WORK_OUTPUTBAK.replace('\\','/'))

		# scriptPath=r'script\katana'
		# renderPy=os.path.join(self.G_POOL,scriptPath,self.render_py_name)
		# renderScript=os.path.join(self.G_POOL,scriptPath,self.script_name)
		
		
		# if self.G_RENDEROS=='Linux':
			# self.renderScriptPath='/root/rayvision/script/katana'
			# self.renderPyPath = '/root/rayvision/script/katana'
			# renderPy=renderPy.replace('\\','/')
			# renderScript=renderScript.replace('\\','/')
			
		# self.pythonCopy(renderPy,self.renderPyPath)
		# self.pythonCopy(renderScript,self.renderScriptPath)
		# if 'denoise' in self.G_CG_OPTION:
			# denoisePy=os.path.join(self.G_POOL,scriptPath,self.denoiseRender_py_name)
			# denoisePy=denoisePy.replace('\\','/')
			# print 'denoisePy----'+denoisePy
			# self.pythonCopy(denoisePy,self.renderScriptPath)
		
		self.G_RENDER_LOG.info('[Katana.RBhanFile.end.....]')

	def copyDenoisePy(self):
		scriptPath=r'script\katana'
		
		
		self.pythonCopy(renderPy,self.renderPyPath)
		
	def webMntPath(self):
		# mountFrom='{"Z:":"//192.168.0.94/d"}'
		exitcode = subprocess.call("mount | grep -v '/mnt_rayvision' | awk '/cifs/ {print $3} ' | xargs umount", shell=1)
		if exitcode not in(0,123):
			sys.exit(exitcode)
		#self.RBcmd(umountcmd)

		self.G_RENDER_LOG.info('[config....]'+self.G_CONFIG)
		self.G_CONFIG=self.G_CONFIG.replace("\\","/")
		if os.path.exists(self.G_CONFIG):
			configJson=eval(open(self.G_CONFIG, "r").read())
			self.CGFILE=configJson['common']["cgFile"]
			self.analyseFile_path=configJson['common']["analyseTxt"]
			print configJson
			if isinstance(configJson["mntMap"],dict):
				for key in configJson["mntMap"]:
					if not os.path.exists(key):
						os.makedirs(key)
					cmd='mount -t cifs -o username=administrator,password=Rayvision@2016,codepage=936,iocharset=gb2312 '+configJson["mntMap"][key].replace('\\','/')+' '+key
					self.G_RENDER_LOG.info(cmd)
					self.RBcmd(cmd,False,1)
					
	def webNetPath(self):
		if os.path.exists(self.G_CONFIG):
			configJson=eval(open(self.G_CONFIG, "r").read())
			self.CGFILE=configJson['common']["cgFile"]
			self.analyseFile_path=configJson['common']["analyseTxt"]
			print configJson
			if isinstance(configJson["mntMap"],dict):
				self.RBcmd("net use * /del /y")
				for key in configJson["mntMap"]:
					# self.RBcmd("net use "+key+" "+configJson["mntMap"][key].replace("/","\\"))
					self.RBcmd("net use "+key+" \""+configJson["mntMap"][key].replace("/","\\")+"\"")
	
	def getFinalList(self,renderNode):
		self.finalList=[]
		print "self.analyseFile_path----------------"+self.analyseFile_path
		if os.path.exists(self.analyseFile_path):
			analyseJson=eval(open(self.analyseFile_path, "r").read())
			print '=============='+str(analyseJson[renderNode])
			if isinstance(analyseJson[renderNode],dict):
				self.finalList = analyseJson[renderNode]["Final"]

		
	def denoise(self,renderNode):
		print "self.analyseFile_path----------------"+self.analyseFile_path+"-------"+renderNode
		self.analyseFile_path = self.analyseFile_path.replace("\\","/")
		print os.path.exists(self.analyseFile_path)
		if os.path.exists(self.analyseFile_path.replace("\\","/")):
			analyseJson=eval(open(self.analyseFile_path, "r").read())
			self.finalList=[]
			#print renderNode
			#print str(analyseJson[renderNode])
			if isinstance(analyseJson[renderNode],dict):#hasattr(,):
				#print 'have node-----'
				slist = analyseJson[renderNode]["Source"]
				#self.finalList=slist
				vriance =analyseJson[renderNode]["Variance"]
				self.denoiseByNode(slist,vriance)
			else:
				for key in analyseJson:
					#print 'key----------------'+key
					#print str(key==renderNode)
					slist = analyseJson[key]["Source"]
					vriance =analyseJson[key]["Variance"]
					self.denoiseByNode(slist,vriance)
	def denoiseByNode(self,sourceList,vriance):
		# python="c:\python27\python.exe"
		denoisePy=self.renderScriptPath+"/"+self.denoiseRender_py_name
		vrianceStr = ''
		
		print str(vriance)
		if len(vriance)>0:
			vrianceStr = re.sub('[0-9]+(?=[^0-9]*$)', '*',vriance[0])
		for sourceStr in sourceList:
			print "sourceStr-----"+sourceStr
			if sourceStr !='':
				if not self.G_CG_OPTION =='denoise':
					sourceInfo = '/'+self.G_CG_OPTION[8:len(self.G_CG_OPTION)]
					print "--------"+sourceInfo
					if not sourceInfo in sourceStr:
						continue
				print 'denoise start--'+sourceStr+'-------'+time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
				source=re.sub('[0-9]+(?=[^0-9]*$)', '*',sourceStr)
				final=self.G_RENDER_WORK_OUTPUT  +source[0:source.find("/Source/")]+"/Final"
				#python '/root/Desktop/denoise_render.py'  123 456 
				#'/mnt/projects/super_builder_tvquences/Seq03/Seq03_shot100/Comp/publish/elements/CH/MC_AC/CH_Variance/Final/image_variance.*.exr'  
				#'/mnt/projects/super_builder_tvquences/Seq03/Seq03_shot100/Comp/publish/elements/CH/MC_AC/CH_KeyLight/Source/CH_KeyLight.*.exr' 
				#"/mnt/denoise/test"
				cmd ='python "'+denoisePy+'" '+self.G_USERID+' '+self.G_TASKID+' "'+vrianceStr+'" "'+source+'" "'+final+'"'+self.G_PLUGINS 
				self.RBcmd(cmd,False,1)
				print 'denoise end--'+sourceStr+'-------'+time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))


	def RBrender(self):#7

		self.G_RENDER_LOG.info('[Katana.RBrender.start.....]'+self.G_CG_OPTION)
		
		startTime = time.time()
		self.G_FEE_LOG.info('startTime='+str(int(startTime)))

		
		if 'denoise' in self.G_CG_OPTION:
			if not os.path.exists(self.G_RENDER_WORK_OUTPUT):
				os.makedirs(self.G_RENDER_WORK_OUTPUT)
			self.denoise(self.G_CG_LAYER_NAME)
		else:
			renderPyPath=os.path.join(self.renderPyPath,self.render_py_name)
			analyseScriptPath=os.path.join(self.renderScriptPath,self.script_name)

			#python '/root/tana_render.py' 123 456  "/opt/foundrytana/demostana_files/aovs_prman.katana" Render_test 1 1
			renderCmd=self.python_path+' "'+renderPyPath+'" '+self.G_USERID+' '+self.G_TASKID+' "'+self.CGFILE+'" "'+self.G_CG_LAYER_NAME+'" '+self.G_CG_START_FRAME+' ' + self.G_CG_END_FRAME +' "' + self.G_PLUGINS + '"'
			
			self.RBcmd(renderCmd,False,1)
			self.getFinalList(self.G_CG_LAYER_NAME)
		endTime = time.time()
		self.G_FEE_LOG.info('endTime='+str(int(endTime)))
		self.G_RENDER_LOG.info('[Katana.RBrender.end.....]')


	def RBresultAction(self):
		self.G_PROCESS_LOG.info('[BASE.RBresultAction.start.....]')
		#RB_small
		if not os.path.exists(self.G_PATH_SMALL):
			os.makedirs(self.G_PATH_SMALL)
		frameCheck = os.path.join(self.G_POOL,'tools',"SingleFrameCheck.exe")
		feeLogFile=self.G_USERID+'-'+self.G_TASKID+'-'+self.G_JOB_NAME+'.txt'
		feeTxt=os.path.join(self.G_RENDER_WORK_TASK,feeLogFile)
		if self.G_RENDEROS=='Linux':
			if 'denoise' in self.G_CG_OPTION:
				print 'copy start--'+time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
				self.outputMnt()
				self.pythonCopy(self.G_RENDER_WORK_OUTPUT.replace('\\','/'),self.outputPath+"/"+self.outputFolder)
				self.pythonCopy(self.G_RENDER_WORK_OUTPUT.replace('\\','/'),self.G_RENDER_WORK_OUTPUTBAK.replace('\\','/'))
				print 'copy end--'+ time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
			else:
				if len(self.finalList)>0:
					self.outputMnt()
					self.outputPath=self.outputPath+"/"+self.outputFolder
					if not os.path.exists(self.outputPath):
						os.makedirs(self.outputPath)
					
					for finalPath in self.finalList:
						finalPath=re.sub('[0-9]+(?=[^0-9]*$)', "%04d"%(int(self.G_CG_START_FRAME)),finalPath)
						self.pythonCopy(finalPath,self.outputPath+finalPath[0:finalPath.index("/Final/")+1]+"Final/")
			#self.pythonCopy(self.G_RENDER_WORK_OUTPUT.replace('\\','/'),self.G_RENDER_WORK_OUTPUTBAK.replace('\\','/'))
			self.pythonCopy(feeTxt,"/fee")
		else:
			output=self.G_PATH_USER_OUTPUT
			if self.G_CG_TILECOUNT !='1' and self.G_CG_TILECOUNT!=self.G_CG_TILE:
				output=self.G_PATH_TILES

			cmd1='c:\\fcopy\\FastCopy.exe  /speed=full /force_close  /no_confirm_stop /force_start "' +self.G_RENDER_WORK_OUTPUT.replace('/','\\') +'" /to="'+output+'"'
			cmd2='"' +frameCheck + '" "' + self.G_RENDER_WORK_OUTPUT + '" "'+ output.rstrip()+'"'
			cmd3='c:\\fcopy\\FastCopy.exe /cmd=move /speed=full /force_close  /no_confirm_stop /force_start "' +self.G_RENDER_WORK_OUTPUT.replace('/','\\')+'\\*.*" /to="'+self.G_RENDER_WORK_OUTPUTBAK.replace('/','\\')+'"'
		
			cmd4='xcopy /y /f "'+feeTxt+'" "'+self.G_PATH_COST.replace('/','\\')+'/" '
			
			self.RBTry3cmd(cmd1)
			self.RBcmd(cmd2)
			self.RBTry3cmd(cmd3)
			self.RBcmd(cmd4)
		self.G_PROCESS_LOG.info('[BASE.RBresultAction.end.....]')

	def outputMnt(self):
		self.outputPath="/output"
		self.feePath="/fee"
		self.outputFolder=self.G_PATH_USER_OUTPUT[self.G_PATH_USER_OUTPUT.rfind("\\")+1:len(self.G_PATH_USER_OUTPUT)]
		outputmnt='mount -t cifs -o username=administrator,password=Rayvision@2016,codepage=936,iocharset=gb2312 '+self.G_PATH_USER_OUTPUT.replace(self.outputFolder,'').replace('\\','/')+' '+self.outputPath
		feemnt='mount -t cifs -o username=administrator,password=Rayvision@2016,codepage=936,iocharset=gb2312 '+self.G_PATH_COST.replace('\\','/').replace("/mnt","//10.50.244.116")+' '+self.feePath
		if not os.path.exists(self.outputPath):
			os.makedirs(self.outputPath)
		if not os.path.exists(self.feePath):
			os.makedirs(self.feePath)
		self.RBcmd(outputmnt,False,1)
		self.RBcmd(feemnt,False,1)
	
	'''
		copy final file to common outputFolder
	'''
	def RBcopyFinalFile(self):
		# G_CONFIG = r'\\10.60.100.101\p5\config\119500\119768\9397302\render.json'
		# configJson = eval(open(self.G_CONFIG, "r").read())
		# self.analyseFile_path = configJson['common']["analyseTxt"]
		# G_CG_LAYER_NAME = 'AO_big'
		# self.G_CG_START_FRAME,self.G_CG_END_FRAME
		self.G_RENDER_LOG.info('[Katana.RBcopyFinalFile.start.....]')
		self.analyseFile_path = self.analyseFile_path.replace("\\","/")
		if os.path.exists(self.analyseFile_path):
			analyseJson=eval(open(self.analyseFile_path, "r").read())
			print analyseJson
			if analyseJson[self.G_CG_LAYER_NAME]:
				print 'analyseJson:'+str(analyseJson[self.G_CG_LAYER_NAME]) #[{'primary': 'F:/farm/render/v024/ao_big/ao_big_1064.exr'}, {'start': 1.0, 'end': 1.0}]
				fromPathDict = analyseJson[self.G_CG_LAYER_NAME][0]
				if fromPathDict:
					for key in fromPathDict:
						fromPathModel = fromPathDict[key]
						pattern = r'.*[\W_](\d+)\..*?'
						m = re.match(pattern,fromPathModel)
						if m:
							numStr = m.group(1)
							numLen = len(numStr)
							print self.G_CG_START_FRAME,self.G_CG_END_FRAME
							# startLen = len(self.G_CG_START_FRAME)
							# endLen = len(self.G_CG_END_FRAME)
							if int(self.G_CG_START_FRAME) <= int(self.G_CG_END_FRAME):
								for frame in xrange(int(self.G_CG_START_FRAME),int(self.G_CG_END_FRAME)+1):
									numStrNew = '0'*(numLen-len(str(frame))) + str(frame)
									fromPath = fromPathModel.replace(numStr,numStrNew)
									print fromPath
									if os.path.exists(fromPath):
										self.pythonCopy(fromPath.replace('\\','/'),self.G_RENDER_WORK_OUTPUT.replace('\\','/'))
									else:
										print fromPath + ' is not exist'
							else:
								print 'error:START_FRAME > END_FRAME'
						else:
							print 'm match error'
				else:
					print 'fromPathDict is empty'
			else:
				print 'analyseJson[self.G_CG_LAYER_NAME] is not exist'
		else:
			print self.analyseFile_path + ' is not exist'
		self.G_RENDER_LOG.info('[Katana.RBcopyFinalFile.end.....]')
		
	def RBexecute(self):#Render
		self.RBBackupPy()
		self.RBinitLog()
		self.G_RENDER_LOG.info('[Katana.RBexecute.start...]')
		self.RBprePy()
		self.RBmakeDir()
		self.RBcopyTempFile()
		self.RBreadCfg()
		self.RBhanFile()
		if self.G_RENDEROS=='Linux':
			self.webMntPath()
		else:
			self.delSubst()
			self.webNetPath()
		self.RBwriteConsumeTxt()
		self.RBrender()
		self.RBcopyFinalFile()
		if self.G_RENDEROS=='Linux':
			print 'no smallpic'
		else:
			self.RBconvertSmallPic()
		self.RBhanResult()
		self.G_RENDER_LOG.info('[Katana.RBexecute.end.....]')