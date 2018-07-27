import os,sys,subprocess,string,logging,time,shutil
import logging
from AnalysisBase import AnalysisBase

class Softimage(AnalysisBase):
	def __init__(self,**paramDict):
		AnalysisBase.__init__(self,**paramDict)
		print "Sofimage.INIT"
		
		self.CGV=''

	def RBhanFile(self):#3 copy script,copy from pool,#unpack
		self.G_ANALYSE_LOG.info('[Sofimage.RBhanFile.start.....]')

		self.G_ANALYSE_LOG.info('[Sofimage.RBhanFile.end.....]')
		
	def RBconfig(self):#5
		self.G_ANALYSE_LOG.info('[Sofimage.RBconfig.start.....]')
		self.G_ANALYSE_LOG.info('[Sofimage.RBconfig.end.....]')
	
	def RBanalyse(self):#7
		self.G_ANALYSE_LOG.info('[Sofimage.RBanalyse.start.....]')
		
		netFile = os.path.join(self.G_WORK_TASK,(self.G_CG_TXTNAME+'_net.txt'))
		netFile=netFile.replace('\\','/')

		myCgVersion = "Softimage "+self.CGV
		softimageCheckbat=r'B:\plugins\softimage\script\checkXSI.bat'
		softimagePath=os.path.join(r'C:\Program Files\Autodesk',myCgVersion,r'Application\bin\XSIBATCH.exe')
		softimagebat=os.path.join(r'C:\Program Files\Autodesk',myCgVersion,r'Application\bin\setenv.bat')
		vbs=r"B:\plugins\softimage\script\checkNet.vbs"

		analyseCmd=softimageCheckbat+' "'+softimagebat+'" "'+softimagePath+'" "'+vbs+'" "' +self.PROPATH+'" "' +self.CGFILE+'" "'+netFile+'" '
		self.RBcmd(analyseCmd,True,False)
		self.G_ANALYSE_LOG.info('[Sofimage.RBanalyse.end.....]')

	def webNetPath(self):
		if os.path.exists(self.G_CONFIG):
			configJson=eval(open(self.G_CONFIG, "r").read())
			self.CGFILE=configJson['common']["cgFile"]
			self.CGSOFT=configJson['common']["cgSoftName"]
			self.CGV=configJson['common']["cgv"]
			self.RTASKID=configJson['common']["taskId"]
			self.PROPATH=configJson['renderSettings']["projectPath"]
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
		self.G_ANALYSE_LOG.info('[Sofimage.RBexecute.start.....]')
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
		self.G_ANALYSE_LOG.info('[Sofimage.RBexecute.end.....]')