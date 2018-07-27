import os,sys,subprocess,string,logging,time,shutil
import logging
from AnalysisBase import AnalysisBase

class SketchUp(AnalysisBase):
	def __init__(self,**paramDict):
		AnalysisBase.__init__(self,**paramDict)

		self.analyseRb=os.path.join(self.G_WORK_TASK_CFG,'sketchupSubmit.rb')
		self.G_SKETCHUP_ANALYSEFILE_NAME='SketchupSubmitModule.rb'
		
	def RBhanFile(self):#3 copy script,copy from pool,#unpack
		self.G_ANALYSE_LOG.info('[Sketchup.RBhanFile.start.....]')

		self.G_ANALYSE_LOG.info('[Sketchup.RBhanFile.end.....]')
		
	def RBconfig(self):#5
		self.G_ANALYSE_LOG.info('[Sketchup.RBconfig.start.....]')
		self.G_ANALYSE_LOG.info('[Sketchup.RBconfig.end.....]')
	
	def copyAnalyseFile(self):
		self.G_ANALYSE_LOG.info('[Sketchup.copyAnalyseFile.start.....]')
		analyseFile=os.path.join(self.G_POOL,r'script\sketchup',self.G_SKETCHUP_ANALYSEFILE_NAME)
		copyVBSCmd='xcopy /y /f "'+analyseFile+'" "c:/script/sketchup/" '
		self.RBcmd(copyVBSCmd)
		self.G_ANALYSE_LOG.info('[Sketchup.copyAnalyseFile.end.....]')

	def RBanalyse(self):#7
		self.G_ANALYSE_LOG.info('[Sketchup.RBanalyse.start.....]')
		#
		#myCgVersion='SketchUp '+self.cgv
		myCgVersion=self.cgName +" "+self.cgv
		
		sketchupExePath=os.path.join(r'C:\Program Files\SketchUp',myCgVersion,'SketchUp.exe')

		analyseCmd='"'+sketchupExePath+'" -RubyStartup "'+self.analyseRb.replace("\\","/")+'" '
		self.RBcmd(analyseCmd,True,False)
		self.G_ANALYSE_LOG.info('[Sketchup.RBanalyse.end.....]')

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
			projectName= configJson['common']["projectSymbol"]
			replacePath="\\"+projectName+"\\"+self.cgName+"\\"
			print configJson
			if isinstance(configJson["mntMap"],dict):
				self.RBcmd("net use * /del /y")
				for key in configJson["mntMap"]:
					newPath =configJson["mntMap"][key].replace("/","\\").replace(replacePath,"\\")
					# self.RBcmd("net use "+key+" "+newPath)
					self.RBcmd("net use "+key+" \""+newPath+"\"")
		
	def RBexecute(self):#Render
		self.G_ANALYSE_LOG.info('[Sketchup.RBexecute.start.....]')
		self.RBBackupPy()
		self.RBinitLog()
		self.RBmakeDir()
		self.delSubst()
		self.webNetPath()
		self.RBprePy()
		self.RBcopyTempFile()
		self.RBreadCfg()
		self.RBhanFile()
		self.plugin()
		self.copyAnalyseFile()
		self.RBconfig()	
		self.RBanalyse()
		self.RBpostPy()
		self.RBhanResult()
		self.G_ANALYSE_LOG.info('[Sketchup.RBexecute.end.....]')