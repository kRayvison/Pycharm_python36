import os,sys,subprocess,string,logging,time,shutil

import logging

class AnalysisBase():

	def __init__(self,**paramDict):
		print '[BASE.init.start.....]'
		
		self.G_DOPY_NAME='do.py'
		
		self.G_USERID=paramDict['G_USERID']
		self.G_USERID_PARENT=paramDict['G_USERID_PARENT']
		self.G_TASKID=paramDict['G_TASKID']
		self.G_POOL=paramDict['G_POOL']

		self.G_SYS_ARGVS=paramDict['G_SYS_ARGVS']#taskid,jobindex,jobid,nodeid,nodename
		self.G_JOB_NAME=self.G_SYS_ARGVS[3]
		self.G_NODE_NAME=self.G_SYS_ARGVS[5]
		self.G_CONFIG=paramDict['G_CONFIG']
		
		self.G_LOG_WORK='C:/LOG/helper'
		self.G_HELPER_WORK='C:/WORK/helper'
		self.G_RENDEROS = 'Windows'
		if 'G_RENDEROS' in paramDict:
			self.G_RENDEROS = paramDict['G_RENDEROS']
			if self.G_RENDEROS=='Linux':
				self.G_LOG_WORK='/root/rayvision/log/helper'
				self.G_HELPER_WORK='/root/rayvision/work/helper'
		
		self.G_WORK_TASK=os.path.join(self.G_HELPER_WORK,self.G_TASKID)
		self.G_WORK_TASK_CFG=os.path.join(self.G_WORK_TASK,'cfg')
		self.G_CFG_PY=os.path.join(self.G_WORK_TASK_CFG,'py.cfg')
		self.G_PRE_PY=os.path.join(self.G_WORK_TASK_CFG,'pre.py')
		self.G_POST_PY=os.path.join(self.G_WORK_TASK_CFG,'post.py')
		
		#log
		self.G_ANALYSE_LOG=logging.getLogger('analyseLog')
		
		'''
		G_KG=0
		G_CG_VERSION='3ds Max 2012'
		G_CG_RENDER_VERSION='vray2.10.01'
		G_CG_MULTISCATTER_VERSION='multiscatter1.1.07a'
		G_PATH_INPUTFILE
		G_CG_PROJECT
		G_WORK_FILENAME='310239.max'
		G_CG_TXTNAME='fdfdabc_max'
		G_PATH_SMALL=r'\\10.50.10.5\d\outputData\small'
		G_PATH_USER_OUTPUT=r'\\10.50.10.5\d\outputData'
		G_PATH_COST=r'\\10.50.10.5\d\transfer\txt\test'
		G_SINGLE_FRAME_CHECK='singleFrameCheck.exe'
		'''
		print '[BASE.init.end.....]'

	def RBBackupPy(self):
		print '[BASE.RBBackupPy.start.....]'
		runPyPath,runPyName = os.path.split(os.path.abspath(sys.argv[0]))
		tempRunPy=os.path.join(runPyPath,runPyName)
		if not os.path.exists(self.G_WORK_TASK_CFG):
			os.makedirs(self.G_WORK_TASK_CFG)
		workTaskRunPy=os.path.join(self.G_WORK_TASK_CFG,runPyName)
		if not os.path.exists(workTaskRunPy):
			shutil.copyfile(tempRunPy,workTaskRunPy)
		#copyPyCmd='xcopy /y /f "'+tempRunPy+'" "'+self.G_WORK_TASK_CFG+'/" '
		
		print '-----------===-----------------'
		print self.G_SYS_ARGVS
		for arg in self.G_SYS_ARGVS:
			print '------'+arg
		runBatName=os.path.basename(runPyName)+'.bat'
		runBat=os.path.join(self.G_WORK_TASK_CFG,runBatName)
		fileHandle=open(runBat,'w')
		if self.G_RENDEROS=='Linux':
			batCmd='./'+workTaskRunPy+' "'+self.G_SYS_ARGVS[1]+'" "'+self.G_SYS_ARGVS[2]+'" "'+self.G_SYS_ARGVS[3]+'" "'+self.G_SYS_ARGVS[4]+'" "'+self.G_SYS_ARGVS[5]+'"'
		else:
			batCmd='c:/python27/python.exe '+workTaskRunPy+' "'+self.G_SYS_ARGVS[1]+'" "'+self.G_SYS_ARGVS[2]+'" "'+self.G_SYS_ARGVS[3]+'" "'+self.G_SYS_ARGVS[4]+'" "'+self.G_SYS_ARGVS[5]+'"'
		fileHandle.write(batCmd)
		fileHandle.close()
		print '[BASE.RBBackupPy.end.....]'
			
	def RBmakeDir(self):#1
		print '[BASE.RBmakeDir.start.....]'
					
		#renderwork
		if not os.path.exists(self.G_WORK_TASK):
			os.makedirs(self.G_WORK_TASK)
		print '[BASE.RBmakeDir.end.....]'	
			
	def RBinitLog(self):#2
		print '[BASE.RBinitLog.start.....]'
		fm=logging.Formatter("%(asctime)s  %(levelname)s - %(message)s","%Y-%m-%d %H:%M:%S")
		analyseLogPath = os.path.join(self.G_LOG_WORK,self.G_TASKID)
		analyseLog=os.path.join(analyseLogPath,(self.G_JOB_NAME+'.txt'))
		if not os.path.exists(analyseLogPath):
			os.makedirs(analyseLogPath)
		self.G_ANALYSE_LOG.setLevel(logging.DEBUG)
		renderLogHandler=logging.FileHandler(analyseLog)
		renderLogHandler.setFormatter(fm)
		self.G_ANALYSE_LOG.addHandler(renderLogHandler)
		console = logging.StreamHandler()  
		console.setLevel(logging.INFO)  
		self.G_ANALYSE_LOG.addHandler(console)		
		print '[BASE.RBinitLog.end.....]'
		

		
	def RBprePy(self):#pre custom
		self.G_ANALYSE_LOG.info('[BASE.RBprePy.start.....]')	
		self.G_ANALYSE_LOG.info(self.G_PRE_PY)
		if os.path.exists(self.G_PRE_PY):
			sys.argv=[self.G_USERID,self.G_TASKID]
			execfile(self.G_PRE_PY)
		self.G_ANALYSE_LOG.info('[BASE.RBprePy.end.....]')
		
	def RBhanFile(self):#3 copy script,copy from pool,#unpack
		self.G_ANALYSE_LOG.info('[BASE.RBhanFile.start.....]')
		self.G_ANALYSE_LOG.info('[BASE.RBhanFile.end.....]')
	
	def RBcopyTempFile(self):
		self.G_ANALYSE_LOG.info('[BASE.RBcopyTempFile.start.....]')		
		#tempFile=os.path.join(self.G_POOL,'temp',self.G_USERID_PARENT,self.G_USERID,(self.G_TASKID+'_analyse'),'*.*')
		tempFile=os.path.join(self.G_POOL,'temp',(self.G_TASKID+'_analyse'),'*.*')
		if self.G_RENDEROS=='Linux':
			tempFile=os.path.join(self.G_POOL,'temp',(self.G_TASKID+'_analyse'))
			self.pythonCopy(tempFile.replace('\\','/'),self.G_WORK_TASK.replace('\\','/'))
		else:
			tempFile=os.path.join(self.G_POOL,'temp',(self.G_TASKID+'_analyse'))
			self.pythonCopy(tempFile.replace('/','\\'),self.G_WORK_TASK.replace('/','\\'))
		# copyPoolCmd='c:\\fcopy\\FastCopy.exe /speed=full /force_close  /no_confirm_stop /force_start "'+tempFile.replace('/','\\')+'" /to="'+self.G_WORK_TASK.replace('/','\\')+'"'		
		# self.RBcmd(copyPoolCmd)
		self.G_ANALYSE_LOG.info('[BASE.RBcopyTempFile.end.....]')	
	
	def RBreadCfg(self):#4
		self.G_ANALYSE_LOG.info('[BASE.RBreadCfg.start.....]')		
		txtFile=open(self.G_CFG_PY, 'r')
		allLines=txtFile.readlines()

		for eachLine in allLines:
			if eachLine.startswith('#') or eachLine=='\n':
				continue
			execStr='self.'+eachLine.strip()
			print execStr
			exec(execStr)
		self.G_ANALYSE_LOG.info('[BASE.RBreadCfg.end.....]')
			
	def RBconfig(self):#5
		self.G_ANALYSE_LOG.info('[BASE.RBconfig.start.....]')
		self.G_ANALYSE_LOG.info('[BASE.RBconfig.end.....]')
	
	def RBanalyse(self):#7
		self.G_ANALYSE_LOG.info('[BASE.RBanalyse.start.....]')
		self.G_ANALYSE_LOG.info('[BASE.RBanalyse.end.....]')
		
	def RBhanResult(self):#8
		self.G_ANALYSE_LOG.info('[BASE.RBhanResult.start.....]')
		netFile = os.path.join(self.G_WORK_TASK,(self.G_CG_TXTNAME+'_net.txt'))
		errFile = os.path.join(self.G_WORK_TASK,(self.G_CG_TXTNAME+'_err.txt'))
		self.G_ANALYSE_LOG.info('[BASE.RBhanResult.file.....]'+netFile)
		if  os.path.exists(netFile) and (not os.path.exists(errFile)):#copy ok
			self.pythonCopy(netFile,self.G_PATH_INPUTTXT)
			# copyCmd='xcopy /y /f "'+netFile+'" "'+self.G_PATH_INPUTTXT+'\\" '
			# self.RBcmd(copyCmd)
		else:
			#error
			sys.exit(-1)
		self.G_ANALYSE_LOG.info('[BASE.RBhanResult.end.....]')

	def RBcmd(self,cmdStr,continueOnErr=False,myShell=1):#continueOnErr=true-->not exit ; continueOnErr=false--> exit 
		self.G_ANALYSE_LOG.info(cmdStr)
		cmdp=subprocess.Popen(cmdStr,stdin = subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.STDOUT, shell = myShell)
		cmdp.stdin.write('3/n')
		cmdp.stdin.write('4/n')
		while cmdp.poll()==None:
			resultLine = cmdp.stdout.readline().strip()
			if resultLine!='':
				self.G_ANALYSE_LOG.info(resultLine)
			
		resultStr = cmdp.stdout.read()
		resultCode = cmdp.returncode
		
		self.G_ANALYSE_LOG.info('resultStr...'+resultStr)
		self.G_ANALYSE_LOG.info('resultCode...'+str(resultCode))
		
		if not continueOnErr:
			if resultCode!=0:
				sys.exit(resultCode)
		return resultStr
	
	def pythonCopy(self,soure,to,continueOnErr=False,myShell=False):
		self.G_ANALYSE_LOG.info('copy...from..'+soure+'....to..'+to)
		try:
			if not os.path.exists(to):
				os.makedirs(to)
			if not os.path.isdir(soure):
				self.G_ANALYSE_LOG.info('file...copy..')
				shutil.copy(soure,to)
			else:
				self.G_ANALYSE_LOG.info('dir...copy..')
				self.copyPyFolder(soure,to)
		except:
			self.G_ANALYSE_LOG.info('copy...error.')
			sys.exit(1)

	def copyPyFolder(self,pyFolder,to):
		if not os.path.exists(to):
			os.makedirs(to)
		if os.path.exists(pyFolder):
			for root, dirs, files in os.walk(pyFolder):
				print 'copyBasePy...'
				for dirname in  dirs:
					tdir=os.path.join(root,dirname)
					if not os.path.exists(tdir):
						os.makedirs(tdir)
				for i in xrange (0, files.__len__()):
					sf = os.path.join(root, files[i])
					folder=to+root[len(pyFolder):len(root)]+"/"
					if not os.path.exists(folder):
						os.makedirs(folder)
					shutil.copy(sf,folder)

	def RBpostPy(self):#post custom
		self.G_ANALYSE_LOG.info('[BASE.RBpostPy.start.....]')
		if os.path.exists(self.G_POST_PY):
			sys.argv=[self.G_USERID,self.G_TASKID]
			execfile(self.G_POST_PY)
		self.G_ANALYSE_LOG.info('[BASE.RBpostPy.end.....]')
		
	def RBexecute(self):#total
		print 'BASE.execute.....'
		self.RBBackupPy()
		self.RBinitLog()
		self.G_ANALYSE_LOG.info('[BASE.RBexecute.start.....]')
		self.RBprePy()		
		self.RBmakeDir()	
		self.RBcopyTempFile()
		self.RBreadCfg()		
		self.RBhanFile()
		self.RBconfig()		
		self.RBanalyse()
		self.RBhanResult()		
		self.RBpostPy()
		self.G_ANALYSE_LOG.info('[BASE.RBexecute.end.....]')