import os,sys,subprocess,string,logging,time,shutil
import logging
from AnalysisBase import AnalysisBase

class Katana(AnalysisBase):
	def __init__(self,**paramDict):
		AnalysisBase.__init__(self,**paramDict)
		print "Katana.INIT"
		self.analyse_py_name="katana_analyse.py"
		self.python_path="c:/Python27/python.exe"
		if self.G_RENDEROS=='Linux':
			self.python_path="/usr/bin/python"
		self.script_name="katana_script.py"
		
		self.G_NODE_PY = paramDict['G_NODE_PY']
		self.G_CG_NAME = paramDict['G_CG_NAME']
		
		self.analysePyPath=self.G_NODE_PY + "/" + self.G_CG_NAME + "/lib"
		self.analyseScriptPath=self.analysePyPath

		self.CGFILE=""
		
	def RBhanFile(self):#3 copy script,copy from pool,#unpack
		self.G_ANALYSE_LOG.info('[Katana.RBhanFile.start.....]')

		# scriptPath=r'script\katana'
		# checkPy=os.path.join(self.G_POOL,scriptPath,self.analyse_py_name)
		# checkScript=os.path.join(self.G_POOL,scriptPath,self.script_name)
		
		# if self.G_RENDEROS=='Linux':
			# self.analyseScriptPath='/root/rayvision/script/katana'
			# self.analysePyPath = '/root/rayvision/script/katana'
			# checkPy=checkPy.replace('\\','/')
			# checkScript=checkScript.replace('\\','/')

		# self.pythonCopy(checkPy,self.analysePyPath)
		# self.pythonCopy(checkScript,self.analyseScriptPath)

		self.G_ANALYSE_LOG.info('[Katana.RBhanFile.end.....]')
	
	def webMntPath(self):
		# mountFrom='{"Z:":"//192.168.0.94/d"}'
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
					cmd=cmd='mount -t cifs -o username=administrator,password=Rayvision@2016,codepage=936,iocharset=gb2312 '+configJson["mntMap"][key].replace('\\','/')+' '+key
					self.G_ANALYSE_LOG.info(cmd)
					self.RBcmd(cmd)

	def webNetPath(self):
		if os.path.exists(self.G_CONFIG):
			configJson=eval(open(self.G_CONFIG, "r").read())

			self.CGFILE=configJson['common']["cgFile"]
			self.CGSOFT=configJson['common']["cgSoftName"]
			self.CGV=configJson['common']["cgv"]
			print configJson
			if isinstance(configJson["mntMap"],dict):
				self.RBcmd("net use * /del /y")
				for key in configJson["mntMap"]:
					# self.RBcmd("net use "+key+" "+configJson["mntMap"][key].replace("/","\\"))
					self.RBcmd("net use "+key+" \""+configJson["mntMap"][key].replace("/","\\")+"\"")


	def RBconfig(self):#5
		self.G_ANALYSE_LOG.info('[Katana.RBconfig.start.....]')
		self.G_ANALYSE_LOG.info('[Katana.RBconfig.end.....]')
	
	def RBanalyse(self):#7
		self.G_ANALYSE_LOG.info('[Katana.RBanalyse.start.....]')

		netFile = os.path.join(self.G_WORK_TASK,(self.G_CG_TXTNAME+'_net.txt'))
		netFile=netFile.replace('\\','/')

		analysePyPath=os.path.join(self.analysePyPath,self.analyse_py_name).replace('\\','/')
		analyseScriptPath=os.path.join(self.analyseScriptPath,self.script_name).replace('\\','/')

		self.G_ANALYSE_LOG.info('----analysePyPath----'+analysePyPath)
		self.G_ANALYSE_LOG.info('----analyseScriptPath----'+analyseScriptPath)

		self.G_ANALYSE_LOG.info('----cgfile----'+self.CGFILE)
		#python '/root/tana_analyse.py' 123 456  '/root/tana_script.py' "/opt/foundrytana/demostana_files/aovs_prman.katana" "/hometana.txt"
		# analyseCmd=self.python_path+' "'+analysePyPath+'" "'+self.G_USERID+'" "'+self.G_TASKID+'" "' + analyseScriptPath+'" "' +self.CGFILE+'" "'+netFile+'"'
		analyseCmd=self.python_path+' "'+analysePyPath+'" "'+self.G_USERID+'" "'+self.G_TASKID+'" "'+self.G_PLUGINS+'" "' +self.CGFILE+'" "'+netFile+'"'
		self.RBcmd(analyseCmd,True,1)
		self.G_ANALYSE_LOG.info('[Katana.RBanalyse.end.....]')

	def RBexecute(self):#Render
		self.G_ANALYSE_LOG.info('[Katana.RBexecute.start.....]')
		self.RBBackupPy()
		self.RBinitLog()
		if self.G_RENDEROS=='Linux':
			self.webMntPath()
		else:
			self.delSubst()
			self.webNetPath()
		self.RBmakeDir()
		self.RBcopyTempFile()#copy py.cfg max file
		self.RBreadCfg()
		self.RBhanFile()
		
		self.RBanalyse()
		self.RBhanResult()
		self.G_ANALYSE_LOG.info('[Katana.RBexecute.end.....]')