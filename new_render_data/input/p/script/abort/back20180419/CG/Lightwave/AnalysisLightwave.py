import os,sys,subprocess,string,logging,time,shutil
import logging
from AnalysisBase import AnalysisBase

class Lightwave(AnalysisBase):
	def __init__(self,**paramDict):
		AnalysisBase.__init__(self,**paramDict)
		print "MAYA.INIT"
		self.G_CHECKBAT_NAME='check.bat'
		self.G_CHECKMEL_NAME='checkNet.mel'
		self.G_PLUGINBAT_NAME='plugin.bat'
		self.CGFILE=""
		self.CGSOFT=""
		self.CGV=""
		self.RTASKID=""
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

		self.pythonCopy(checkBat,mayascript)
		self.pythonCopy(checkMel,mayascript)
		self.G_ANALYSE_LOG.info('[Maya.RBhanFile.end.....]')
	
	def webMntPath(self):
		exitcode = subprocess.call("mount | grep -v '/mnt_rayvision' | awk '/cifs/ {print $3} ' | xargs umount", shell=1)
		if exitcode not in(0,123):
			sys.exit(exitcode)

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

	def webNetPath(self):
		if os.path.exists(self.G_CONFIG):
			configJson=eval(open(self.G_CONFIG, "r").read())

			self.CGFILE=configJson['common']["cgFile"]
			self.CGSOFT=configJson['common']["cgSoftName"]
			self.CGV=configJson['common']["cgv"]
			self.RTASKID=configJson['common']["taskId"]
			projectName= configJson['common']["projectSymbol"]
			replacePath="\\"+projectName+"\\"+self.CGSOFT+"\\"
			print configJson
			if isinstance(configJson["mntMap"],dict):
				self.RBcmd("net use * /del /y")
				for key in configJson["mntMap"]:
					newPath =configJson["mntMap"][key].replace("/","\\").replace(replacePath,"\\")
					# self.RBcmd("net use "+key+" "+newPath)
					self.RBcmd("net use "+key+" \""+newPath+"\"")					


	def RBconfig(self):#5
		self.G_ANALYSE_LOG.info('[Maya.RBconfig.start.....]')
		self.G_ANALYSE_LOG.info('[Maya.RBconfig.end.....]')
	
	def RBanalyse(self):#7
		self.G_ANALYSE_LOG.info('[Maya.RBanalyse.start.....]')
		
		mayaExePath = self.cgSoftAddr()
		
		netFile = os.path.join(self.G_WORK_TASK,self.G_CG_TXTNAME+"_net.txt")
		netFile=netFile.replace('\\','/')
		
		cgProject = self.G_PATH_INPUTROJECT.replace('\\','\\\\')
		cgFile=self.G_PATH_INPUTFILE.replace('\\','\\\\')
		mayascript='c:/script/maya/'
		if self.G_RENDEROS=='Linux':
			mayascript='/root/rayvision/script/maya/'
		self.G_ANALYSE_LOG.info('----cgfil----'+self.CGFILE)
		analyseCmd=mayascript+self.G_CHECKBAT_NAME+' "'+self.G_USERID+'" "'+str(self.RTASKID)+'" "' + mayaExePath+'" "''" "' +self.CGFILE+'" "'+netFile+'" '
		# analyseCmd=r'"C:\Python27\python.exe" "'+py_path+r'\check_all.py" --cgfile "'+self.CGFILE+r'" --cg_info_file "'+netFile+r'" --cgsw LightWave --ti '+str(self.RTASKID)
		self.RBcmd(analyseCmd,True,1)
		self.G_ANALYSE_LOG.info('[Maya.RBanalyse.end.....]')
		
	def cgSoftAddr(self):
		mayaExePath=os.path.join('B:/NewTek/',"LightWave_"+self.CGV,'bin/lwsn.exe')
		mayaExePath=mayaExePath.replace('\\','/')
		return mayaExePath

	def RBexecute(self):#Render
		self.G_ANALYSE_LOG.info('[Maya.RBexecute.start.....]')
		self.RBBackupPy()
		self.RBinitLog()
		if self.G_RENDEROS=='Linux':
			self.webMntPath()
		else:
			self.delSubst()
			self.webNetPath()
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