import os,sys,subprocess,string,logging,time,shutil
import logging
import codecs
from AnalysisBase import AnalysisBase

class Keyshot(AnalysisBase):
	def __init__(self,**paramDict):
		AnalysisBase.__init__(self,**paramDict)
		
	def RBhanFile(self):#3 copy script,copy from pool,#unpack
		self.G_ANALYSE_LOG.info('[KeyShot.RBhanFile.start.....]')

		self.G_ANALYSE_LOG.info('[KeyShot.RBhanFile.end.....]')
		
	def RBconfig(self):#5
		self.G_ANALYSE_LOG.info('[KeyShot.RBconfig.start.....]')
		self.G_ANALYSE_LOG.info('[KeyShot.RBconfig.end.....]')
	
	def RBanalyse(self):#7
		self.G_ANALYSE_LOG.info('[KeyShot.RBanalyse.start.....]')

		#myCgVersion=self.cgName + self.cgv
		#exePath=os.path.join(r'D:\Program Files',myCgVersion,r'bin\keyshot6.exe')
		#scriptPath = "B:\\plugins\\KeyShot\\lib\\python\\ks_analy.py"

		#analyseCmd='"'+exePath+'" -script "'+scriptPath.replace("\\","/")+'" '
		mainPyCmd='C:\\Python34\\python.exe "B:\plugins\KeyShot\lib\python\main_analy.py"'

		self.RBcmd(mainPyCmd,True,False)
		#self.RBcmd(analyseCmd,True,False)
		self.G_ANALYSE_LOG.info('[KeyShot.RBanalyse.end.....]')

	def bulidFile(self):
		self.G_ANALYSE_LOG.info('[KeyShot.RBanalyse.start.....]')
		netFile = os.path.join(self.G_WORK_TASK,(self.G_CG_TXTNAME+'_net.txt'))
		netFile=netFile.replace('\\','/')
		infoFolder = "D:\\KS\\"
		analyseFolder = "C:\\work\\render\\"+self.G_TASKID+"\\KS\\"
		infoPath = infoFolder+"INFO.txt"

		if not os.path.exists(infoFolder):
			os.mkdir(infoFolder)

		if not os.path.exists(analyseFolder):
			os.makedirs(analyseFolder)

		if os.path.exists(infoPath):
			os.remove(infoPath)

		AnalyseFilePath = analyseFolder+"FilePath.txt"
		info=codecs.open(infoPath,'w')
		AnalyseFile=codecs.open(AnalyseFilePath,'w')
		try :
			info.write(self.G_TASKID.encode("UTF-8"))
			AnalyseFile.write(self.CGFILE.encode("UTF-8")+"\n")
			AnalyseFile.write(netFile.encode("UTF-8"))
		finally :
			info.close()
			AnalyseFile.close()

		self.G_ANALYSE_LOG.info('[KeyShot.RBanalyse.end.....]')

	def plugin(self):
		self.G_ANALYSE_LOG.info('[self.G_PLUGINS.....]'+self.G_PLUGINS)
		if os.path.exists(self.G_PLUGINS):
			configJson=eval(open(self.G_PLUGINS, "r").read())
			myCgVersion = configJson["renderSoftware"] +" "+configJson["softwareVer"]
			delCmd='B:\\plugins\\Sketchup\\script\\plugin.bat "'+myCgVersion+'" "del"'
			self.RBcmd(delCmd,True,False)
			if isinstance(configJson["plugins"],dict):
				for key in configJson["plugins"]:
					cmd = 'B:\\plugins\\Sketchup\\script\\plugin.bat "'+myCgVersion+'" "'+key+'" "'+key+configJson["plugins"][key]+'"'
					self.RBcmd(cmd,True,False)

	def webNetPath(self):
		if os.path.exists(self.G_CONFIG):
			configJson=eval(open(self.G_CONFIG, "r").read())
			self.cgv=configJson['common']["cgv"]
			self.cgName=configJson['common']["cgSoftName"]
			self.CGFILE=configJson['common']["cgFile"]
			print configJson
			if isinstance(configJson["mntMap"],dict):
				self.RBcmd("net use * /del /y")
				for key in configJson["mntMap"]:
					# self.RBcmd("net use "+key+" "+configJson["mntMap"][key].replace('/','\\'))
					self.RBcmd("net use "+key+" \""+configJson["mntMap"][key].replace('/','\\')+"\"")
		
	def RBexecute(self):#Render
		self.G_ANALYSE_LOG.info('[KeyShot.RBexecute.start.....]')
		self.RBBackupPy()
		self.RBinitLog()
		self.RBmakeDir()
		self.delSubst()
		self.webNetPath()
		self.RBprePy()
		self.RBcopyTempFile()
		self.RBreadCfg()
		self.RBhanFile()
		self.bulidFile()
		#self.plugin()
		self.RBconfig()	
		self.RBanalyse()
		self.RBpostPy()
		self.RBhanResult()
		self.G_ANALYSE_LOG.info('[KeyShot.RBexecute.end.....]')