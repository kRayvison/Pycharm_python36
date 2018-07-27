import os,sys,subprocess,string,logging,time,shutil
import logging
from AnalysisBase import AnalysisBase

class Blender(AnalysisBase):
	def __init__(self,**paramDict):
		AnalysisBase.__init__(self,**paramDict)
		print "Blender.INIT"
		
		self.CGV=''

	def RBhanFile(self):#3 copy script,copy from pool,#unpack
		self.G_ANALYSE_LOG.info('[Blender.RBhanFile.start.....]')

		self.G_ANALYSE_LOG.info('[Blender.RBhanFile.end.....]')
		
	def RBconfig(self):#5
		self.G_ANALYSE_LOG.info('[Blender.RBconfig.start.....]')
		self.G_ANALYSE_LOG.info('[Blender.RBconfig.end.....]')
	
	def RBanalyse(self):#7
		self.G_ANALYSE_LOG.info('[Blender.RBanalyse.start.....]')
		
		netFile = os.path.join(self.G_WORK_TASK,(self.G_CG_TXTNAME+'_net.txt'))
		netFile=netFile.replace('\\','/')

		myCgVersion = self.CGSOFT+"-"+self.CGV
		checkPy=r'B:/plugins/blender/script/check.py'
		exePath=os.path.join(r'B:/plugins/blender/Blender Foundation',myCgVersion,r'blender.exe')

		analyseCmd='"'+exePath+'" -b "'+self.CGFILE+'" -P '+checkPy+' -- "'+netFile+'" '
		self.RBcmd(analyseCmd,True,False)
		self.G_ANALYSE_LOG.info('[Blender.RBanalyse.end.....]')

	def webNetPath(self):
		if os.path.exists(self.G_CONFIG):
			configJson=eval(open(self.G_CONFIG, "r").read())
			self.CGFILE=configJson['common']["cgFile"]
			self.CGSOFT=configJson['common']["cgSoftName"]
			self.CGV=configJson['common']["cgv"]
			projectName= configJson['common']["projectSymbol"]
			replacePath="\\"+projectName+"\\"+self.CGSOFT+"\\"
			print configJson
			if isinstance(configJson["mntMap"],dict):
				self.RBcmd("net use * /del /y")
				for key in configJson["mntMap"]:
					newPath =configJson["mntMap"][key].replace("/","\\").replace(replacePath,"\\")
					# self.RBcmd("net use "+key+" "+newPath)
					self.RBcmd("net use "+key+" \""+newPath+"\"")
		
	def RBexecute(self):#Render
		self.G_ANALYSE_LOG.info('[Blender.RBexecute.start.....]')
		self.RBBackupPy()
		self.RBinitLog()
		self.RBmakeDir()
		self.delSubst()
		self.webNetPath()
		self.RBprePy()
		self.RBcopyTempFile()#copy py.cfg max file
		self.RBreadCfg()
		self.RBhanFile()
		self.RBconfig()		
		self.RBanalyse()
		self.RBpostPy()
		self.RBhanResult()
		self.G_ANALYSE_LOG.info('[Blender.RBexecute.end.....]')