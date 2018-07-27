import os,sys,subprocess,string,logging,time,shutil
import logging
from AnalysisBase import AnalysisBase

class Maya(AnalysisBase):
	def __init__(self,**paramDict):
		AnalysisBase.__init__(self,**paramDict)
		print "MAYA.INIT"
		self.G_CHECKBAT_NAME='check.bat'
		self.G_CHECKMEL_NAME='checkNet.mel'
		self.G_PLUGINBAT_NAME='plugin.bat'
		self.CGFILE=""
		if self.G_RENDEROS=='Linux':
			self.G_PLUGINBAT_NAME='plugin.sh'
			self.G_CHECKBAT_NAME='check.sh'
		
	def RBhanFile(self):#3 copy script,copy from pool,#unpack
		self.G_ANALYSE_LOG.info('[Maya.RBhanFile.start.....]')

		scriptMayaPath=r'script\maya'
		checkBat=os.path.join(self.G_POOL,scriptMayaPath,self.G_CHECKBAT_NAME)
		checkMel=os.path.join(self.G_POOL,scriptMayaPath,self.G_CHECKMEL_NAME)
		pluginBat=os.path.join(self.G_POOL,scriptMayaPath,self.G_PLUGINBAT_NAME)
		mayascript='c:/script/maya'
		if self.G_RENDEROS=='Linux':
			mayascript='/root/rayvision/script/maya'
			checkBat=checkBat.replace('\\','/')
			checkMel=checkMel.replace('\\','/')
			pluginBat=pluginBat.replace('\\','/')

		# copyScriptCmd1='xcopy /y /f "'+checkBat+'" "'+mayascript+'/" '
		# copyScriptCmd2='xcopy /y /f "'+checkMel+'" "'+mayascript+'/" '
		# copyScriptCmd3='xcopy /y /f "'+pluginBat+'" "'+mayascript+'/" '
		self.pythonCopy(checkBat,mayascript)
		self.pythonCopy(checkMel,mayascript)
		#self.pythonCopy(pluginBat,mayascript)
		
		# self.RBcmd(copyScriptCmd1)
		# self.RBcmd(copyScriptCmd2)
		# self.RBcmd(copyScriptCmd3)
		self.G_ANALYSE_LOG.info('[Maya.RBhanFile.end.....]')
	
	def webMntPath(self):
		# mountFrom='{"Z:":"//192.168.0.94/d"}'
		exitcode = subprocess.call("mount | grep -v '/mnt_rayvision' | awk '/cifs/ {print $3} ' | xargs umount", shell=1)
		if exitcode not in(0,123):
			sys.exit(exitcode)
		#self.RBcmd(umountcmd)

		self.G_ANALYSE_LOG.info('[config....]'+self.G_CONFIG)
		if os.path.exists(self.G_CONFIG):
			configJson=eval(open(self.G_CONFIG, "r").read())
			self.CGFILE=configJson['common']["cgFile"]
			print configJson
			if isinstance(configJson["mntMap"],dict):
				for key in configJson["mntMap"]:
					if not os.path.exists(key):
						os.makedirs(key)
					cmd=cmd='mount -t cifs -o username=enfuzion,password=abc123456,codepage=936,iocharset=gb2312 '+configJson["mntMap"][key].replace('\\','/')+' '+key
					self.G_ANALYSE_LOG.info(cmd)
					self.RBcmd(cmd)

	def RBconfig(self):#5
		self.G_ANALYSE_LOG.info('[Maya.RBconfig.start.....]')
		self.G_ANALYSE_LOG.info('[Maya.RBconfig.end.....]')
	
	def RBanalyse(self):#7
		self.G_ANALYSE_LOG.info('[Maya.RBanalyse.start.....]')
		mayaExePath=os.path.join('C:/Program Files/Autodesk',self.G_CG_VERSION,'bin/maya.exe')
		if self.G_RENDEROS=='Linux':
			mayaExePath='/usr/autodesk/'+self.G_CG_VERSION+'-x64/bin/mayapy'
			if not os.path.exists(mayaExePath):
				mayaExePath='/usr/autodesk/'+self.G_CG_VERSION+'/bin/mayapy'
		mayaExePath=mayaExePath.replace('\\','/')
		
		netFile = os.path.join(self.G_WORK_TASK,self.G_CG_TXTNAME+"_net.txt")
		netFile=netFile.replace('\\','/')
		
		cgProject = self.G_PATH_INPUTROJECT.replace('\\','\\\\')
		cgFile=self.G_PATH_INPUTFILE.replace('\\','\\\\')
		mayascript='c:/script/maya/'
		if self.G_RENDEROS=='Linux':
			mayascript='/root/rayvision/script/maya/'
		self.G_ANALYSE_LOG.info('----cgfil----'+self.CGFILE)
		analyseCmd=mayascript+self.G_CHECKBAT_NAME+' "'+self.G_USERID+'" "'+self.G_TASKID+'" "' + mayaExePath+'" "''" "' +self.CGFILE+'" "'+netFile+'" '
		self.RBcmd(analyseCmd,True,1)
		self.G_ANALYSE_LOG.info('[Maya.RBanalyse.end.....]')
		
	def RBexecute(self):#Render
		self.G_ANALYSE_LOG.info('[Maya.RBexecute.start.....]')
		self.RBBackupPy()
		self.RBinitLog()
		if self.G_RENDEROS=='Linux':
			self.webMntPath()
		self.RBmakeDir()
		self.RBprePy()
		self.RBcopyTempFile()#copy py.cfg max file
		self.RBreadCfg()
		self.RBhanFile()
		self.RBconfig()
		
		self.RBanalyse()
		self.RBpostPy()
		self.RBhanResult()
		self.G_ANALYSE_LOG.info('[Maya.RBexecute.end.....]')