#!/usr/bin/env python
#encoding:utf-8
# -*- coding: utf-8 -*-
import logging
import os
import sys
import subprocess
import string
import time,datetime
import shutil
import ctypes
import json
#import math
from CheckFrame import CheckFrame

class RenderBase():

    def __init__(self,**paramDict):
        print 'Base.init...-------------------'
        
        self.G_RENDERTYPE = "cpu"
        self.G_LOG_WORK='C:/log/render'
        self.G_RENDER_WORK='C:/work/render'
        self.G_HELPER_WORK='C:/work/helper'
        self.G_RENDEROS = 'Windows'
        if 'G_RENDEROS' in paramDict:
            self.G_RENDEROS = paramDict['G_RENDEROS']
            if self.G_RENDEROS=='Linux':
                self.G_LOG_WORK='/root/rayvision/log/render'
                self.G_RENDER_WORK='/root/rayvision/work/render'
                self.G_HELPER_WORK='/root/rayvision/work/helper'
        self.G_CFG_PY_NAME='py.cfg'
        self.G_CONVERTVBS_NAME='convertNew.vbs'
        self.G_PRE_PYNAME='pre.py'
        self.G_POST_PYNAME='post.py'
        
        self.G_USERID=paramDict['G_USERID']
        self.G_USERID_PARENT=paramDict['G_USERID_PARENT']
        self.G_TASKID=paramDict['G_TASKID']
        self.G_POOL=paramDict['G_POOL']
        # 开始帧 
        self.G_CG_START_FRAME=paramDict['G_CG_START_FRAME']
        self.G_CG_END_FRAME=paramDict['G_CG_END_FRAME']
        self.G_CG_BY_FRAME=paramDict['G_CG_BY_FRAME']
        self.G_CG_LAYER_NAME=paramDict['G_CG_LAYER_NAME']
        self.G_CG_OPTION=paramDict['G_CG_OPTION']
        if 'G_CONFIG' in paramDict:
            self.G_CONFIG = paramDict['G_CONFIG']
            self.G_CONFIG=self.G_CONFIG.replace("/","\\")#.replace("/mnt/p5","\\\\10.50.244.116\\p5")
        if 'G_PLUGINS' in paramDict:
            self.G_PLUGINS = paramDict['G_PLUGINS']

        self.G_CG_TILE="0"
        self.G_CG_TILECOUNT="1"
        print paramDict
        if 'G_CG_TILE' in paramDict:
            self.G_CG_TILE=paramDict['G_CG_TILE']

        if 'G_CG_TILECOUNT' in paramDict:
            self.G_CG_TILECOUNT=paramDict['G_CG_TILECOUNT']

        self.G_SYS_ARGVS=paramDict['G_SYS_ARGVS']#taskid,jobindex,jobid,nodeid,nodename
        self.G_JOB_NAME=self.G_SYS_ARGVS[3].replace("\"","")
        self.G_NODE_NAME=self.G_SYS_ARGVS[5]
        
        #self.G_POOL_TASK=os.path.join(self.G_POOL,'temp',self.G_USERID_PARENT,self.G_USERID,(self.G_TASKID+'_render'))
        self.G_POOL_TASK=os.path.join(self.G_POOL,'temp',(self.G_TASKID+'_render'))
        
        self.G_RENDER_WORK_TASK=os.path.join(self.G_RENDER_WORK,self.G_TASKID)
        self.G_RENDER_WORK_TASK_CFG=os.path.join(self.G_RENDER_WORK,self.G_TASKID,'cfg')

        self.G_HELPER_WORK_TASK=os.path.join(self.G_HELPER_WORK,self.G_TASKID)
        self.G_HELPER_WORK_TASK_CFG=os.path.join(self.G_HELPER_WORK,self.G_TASKID,'cfg')

        self.G_CFG_PYNAME=os.path.join(self.G_RENDER_WORK_TASK_CFG,self.G_CFG_PY_NAME)#c:/renderwork/12343/renderbus/render.txt
        self.G_HELPER_CFG_PYNAME=os.path.join(self.G_HELPER_WORK_TASK_CFG,self.G_CFG_PY_NAME)
        
        self.G_PRE_PY=os.path.join(self.G_RENDER_WORK_TASK_CFG,self.G_PRE_PYNAME)
        self.G_PRE_PY=self.G_PRE_PY.replace('\\','/')
        self.G_POST_PY=os.path.join(self.G_RENDER_WORK_TASK_CFG,self.G_POST_PYNAME)
        self.G_POST_PY=self.G_POST_PY.replace('\\','/')
        #log
        self.G_SIMPLE_LOG=logging.getLogger('renderlog')
        self.G_PROCESS_LOG=logging.getLogger('processlog')
        self.G_RENDER_LOG=logging.getLogger('maxlog')
        self.G_FEE_LOG=logging.getLogger('feeLog')
        
        self.G_RENDER_WORK_OUTPUT = os.path.join(self.G_RENDER_WORK_TASK,'output')
        #if self.G_USERID=='1801684' or self.G_USERID=='1811222' or self.G_USERID=='1811737' or self.G_USERID=='1820421' or self.G_USERID=='1820556':
        #self.G_RENDER_WORK_OUTPUT = os.path.join(self.G_RENDER_WORK_TASK,'output',self.G_CG_START_FRAME+'_'+self.G_CG_END_FRAME+'_'+self.G_CG_BY_FRAME)
            
        self.G_RENDER_WORK_OUTPUTBAK = os.path.join(self.G_RENDER_WORK_TASK,'outputbak')

        '''
        try:
            scriptpath="c:/script/py/"
            if self.G_RENDEROS=='Linux':
                scriptpath="/root/script/py/"
            cleanNodePyPath="\\\\10.50.1.3\\p\\script\\py\\cleanNode.py"
            if not os.path.exists(scriptpath):
                os.makedirs(scriptpath)
            shutil.copy(cleanNodePyPath,scriptpath)
#           os.system('xcopy /y /v /f  "\\\\10.50.1.3\\p\\script\\py\\cleanNode.py" "c:/script/py/"')
            os.system(scriptpath+'cleanNode.py')
        except:
            print 'cleanNode Error'        
        '''

    def RBBackupPy(self): #
        print '[BASE.RBBackupPy.start.....]'
        # runPyPath = C:\agent\tmp\,runPyName= script_2014060400007_4
        runPyPath,runPyName = os.path.split(os.path.abspath(sys.argv[0]))
        tempRunPy=os.path.join(runPyPath,runPyName)
        if not os.path.exists(self.G_RENDER_WORK_TASK_CFG):
            os.makedirs(self.G_RENDER_WORK_TASK_CFG)
        workTaskRunPy=os.path.join(self.G_RENDER_WORK_TASK_CFG,runPyName)
        print 'tempRunPy...',tempRunPy
        print 'workTaskRunPy...',workTaskRunPy
        if os.path.exists(tempRunPy) and not os.path.exists(workTaskRunPy) :
            self.pythonCopy(tempRunPy,workTaskRunPy)
        #copyPyCmd='xcopy /y /f "'+tempRunPy+'" "'+self.G_RENDER_WORK_TASK_CFG+'/" '
        
        print '-----------===-----------------'
        print self.G_SYS_ARGVS
        for arg in self.G_SYS_ARGVS:
            print '------'+arg
        runBatName=os.path.basename(runPyName)+'.bat'
        runBat=os.path.join(self.G_RENDER_WORK_TASK_CFG,runBatName)
        #if  os.path.exists(runBat):
        #    os.remove(runBat)
        fileHandle=open(runBat,'w')
        batCmd='c:/python27/python.exe '+workTaskRunPy+' "'+self.G_SYS_ARGVS[1]+'" "'+self.G_SYS_ARGVS[2]+'" "'+self.G_SYS_ARGVS[3]+'" "'+self.G_SYS_ARGVS[4]+'" "'+self.G_SYS_ARGVS[5]+'"'
        fileHandle.write(batCmd)
        fileHandle.close()
        print '[BASE.RBBackupPy.end.....]'
    '''
        读文件
    '''
    def readFile(self,path):
        if os.path.exists(path):
            fileObject=open(path)
            line=fileObject.readlines()
            for r in line:
                print r
            return line
        pass
    
    '''
        解析py.cfg文件
    '''
    def readPyCfg(self):
        self.RBlog('读py.cfg','start')
        pypath=self.G_CFG_PYNAME
        if self.G_CONFIG !=None and os.path.exists(self.G_CONFIG):
            pypath=self.G_CONFIG
            
        self.RBlog(pypath)
        self.argsmap={}         
        line=self.readFile(pypath)
        for l in line:
            if "=" in l:
                params=l.split("=")
                self.argsmap[(params[0]).replace('\r','').replace('\n','')]=params[1].replace('\n','').replace('\r','')
        
        self.RBlog('done','end')
        
    def readRenderCfg(self):
        self.RBlog('读render.cfg','start')
        print 'readRenderCfg'
        self.RBlog('done','end')
    
    def delSubst(self):
        substDriverList=[]
        cmdp=subprocess.Popen('subst',stdin = subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.STDOUT, shell = False)
        cmdp.stdin.write('3/n')
        cmdp.stdin.write('4/n')
        while cmdp.poll()==None:
            resultLine = cmdp.stdout.readline().strip()
            print resultLine
            if resultLine!='' and (':\:' in resultLine):
                substDriver= resultLine[0:2]
                substDriverList.append(substDriver)
                
        for substDriver in substDriverList:
            print substDriver
            delSubstCmd='subst '+substDriver+ ' /d'
            print delSubstCmd
            self.RBlog(delSubstCmd)
            try:
                self.RBlog(delSubstCmd)
                os.system(delSubstCmd)
            except:
                pass
    '''
        net windows path
    '''
    def netPath(self):
        self.RBlog('映射路径','start')
        try:
            self.delSubst()
        except:
            pass
        # mountFrom='{"Z:":"//192.168.0.94/d"}'
        

        mountFrom=self.argsmap['mountFrom']
        inputDataPath=self.argsmap['inputDataPath']
        

        cleanMountFrom='try3 net use * /del /y'
        self.G_RENDER_LOG.info(cleanMountFrom)
        self.RBcmd(cleanMountFrom)
        s=eval(mountFrom)
        for key in s.keys():
            if not os.path.exists(s[key]):
                cmd='try3 net use '+s[key]+' '+inputDataPath.replace('/','\\')+self.G_USERID_PARENT+key.replace('/','\\')
                self.G_RENDER_LOG.info(cmd)
                self.RBlog(cmd)
                self.RBcmd(cmd)
        pluginPath=self.argsmap['pluginPath']
        cmd='try3 net use B: '+pluginPath.replace('/','\\')
        self.RBlog(cmd)
        self.RBcmd(cmd) 
        self.RBlog('done','end')
        
    '''
        copy black.xml
    '''
    def copyBlack(self):
        self.RBlog('拷贝弹窗黑名单','start')
        blockPath = 'B:\\tools\\sweeper\\black.xml'
        basePath='c:\\work\\munu_client\\sweeper\\'
        self.RBlog(blockPath+'>'+basePath)
        if os.path.exists(blockPath):
            self.pythonCopy(blockPath,basePath)
        self.RBlog('done','end')
    '''
        mount路径函数
    '''
    def mountPath(self):
        mountIp='192.168.0.199:/mnt/'
        mountFrom='{"worker_hhf":"Z:","worker":"A:"}'
        s=json.loads(mountFrom)
        for key in s.keys():
            print key
            print s[key]
            cmd='mount '+mountIp+key+' '+s[key]+''
            self.runCmd(cmd)
            pass
        pass    
    '''
        检测系统盘符
    '''
    def CheckDisk(self):
        self.RBlog('检测系统盘符','start')
        lpBuffer = ctypes.create_string_buffer(78)
        ctypes.windll.kernel32.GetLogicalDriveStringsA(ctypes.sizeof(lpBuffer), lpBuffer)
        vol = lpBuffer.raw.split('\x00')
        for i in vol:
            if i:                             
                self.G_PROCESS_LOG.info('check CheckDisk='+str(i))
                self.RBlog('Disk='+str(i))
        self.RBlog('done','end')
    '''
        调用子进程运行cmd命令
    '''
    def runCmd(self,cmd):
        print 'cmd='+cmd
        cmdp=subprocess.Popen(cmd,shell = True,stdout = subprocess.PIPE, stderr = subprocess.STDOUT)        
        while True:
            buff = cmdp.stdout.readline()
            if buff == '' and cmdp.poll() != None:
                break       
            print buff
            # self.G_RENDERCMD_LOGGER.info(buff)
            # self.G_PROCESS_LOGGER.info(buff)          
        resultCode = cmdp.returncode
        print 'resultCode='+str(resultCode) 
    '''
        初始化日志
    '''
    def RBinitLog(self):#2
        processLogDir=os.path.join(self.G_LOG_WORK,self.G_TASKID)
        if not os.path.exists(processLogDir):
            os.makedirs(processLogDir)
            
        fm=logging.Formatter("%(asctime)s  %(levelname)s - %(message)s","%Y-%m-%d %H:%M:%S")
        #feeFm=logging.Formatter("%(asctime)s  %(levelname)s - %(message)s","%Y-%m-%d %H:%M:%S")
        processLogPath=os.path.join(processLogDir,(self.G_JOB_NAME+'_process.txt'))
        self.G_PROCESS_LOG.setLevel(logging.DEBUG)
        processLogHandler=logging.FileHandler(processLogPath)
        processLogHandler.setFormatter(fm)
        self.G_PROCESS_LOG.addHandler(processLogHandler)
        console = logging.StreamHandler()  
        console.setLevel(logging.INFO)  
        self.G_PROCESS_LOG.addHandler(console)
        
        #fm=logging.Formatter("%(asctime)s - %(message)s\r\n","%Y-%m-%d %H:%M:%S")
        simpleLogPath=os.path.join(processLogDir,(self.G_JOB_NAME+'_render.txt'))
        self.G_SIMPLE_LOG.setLevel(logging.DEBUG)
        self.simpleLogHandler=logging.FileHandler(simpleLogPath,'a',encoding='gbk')
        #simpleLogHandler=logging.FileHandler(simpleLogPath)
        #simpleLogHandler.setFormatter(fm)
        self.G_SIMPLE_LOG.addHandler(self.simpleLogHandler)
        console = logging.StreamHandler()  
        console.setLevel(logging.INFO)  
        self.G_SIMPLE_LOG.addHandler(console)
        
        
        renderLogDir=os.path.join(self.G_LOG_WORK,self.G_TASKID)
        if not os.path.exists(renderLogDir):
            os.makedirs(renderLogDir)
        renderLogPath=os.path.join(renderLogDir,(self.G_JOB_NAME+'_max.txt'))
        self.G_RENDER_LOG.setLevel(logging.DEBUG)
        renderLogHandler=logging.FileHandler(renderLogPath)
        renderLogHandler.setFormatter(fm)
        self.G_RENDER_LOG.addHandler(renderLogHandler)
        console = logging.StreamHandler()  
        console.setLevel(logging.INFO)  
        self.G_RENDER_LOG.addHandler(console)
        
        
        feeLogFile=self.G_USERID+'-'+self.G_TASKID+'-'+self.G_JOB_NAME+'.txt'
        self.G_FEE_LOG.setLevel(logging.DEBUG)
        if not os.path.exists(self.G_RENDER_WORK_TASK):
            os.makedirs(self.G_RENDER_WORK_TASK)
        feeTxt=os.path.join(self.G_RENDER_WORK_TASK,feeLogFile)
        feeLogHandler=logging.FileHandler(feeTxt)
        #feeLogHandler.setFormatter(fm)
        self.G_FEE_LOG.addHandler(feeLogHandler)        
    

    def RBlog(self,logStr,logType='common'):
        if logStr==None:
            logStr=''
        fm=logging.Formatter("%(asctime)s  %(levelname)s - %(message)s","%Y-%m-%d %H:%M:%S")
        self.simpleLogHandler.setFormatter(fm)
        if logType=='start':
            fm=logging.Formatter("\r\n\r\n\r\n%(asctime)s  %(levelname)s - %(message)s","%Y-%m-%d %H:%M:%S")
            self.simpleLogHandler.setFormatter(fm)
            self.G_SIMPLE_LOG.info('----------------------------['+logStr+']----------------------------\r\n')
        elif logType=='end':
            self.G_SIMPLE_LOG.info('['+logStr+']\r\n')
        else:
            self.G_SIMPLE_LOG.info(logStr+'\r\n')
            
    def RBprePy(self):#pre custom
        self.RBlog('执行自定义PY脚本','start')
        self.RBlog(u'如果以下自定义PY脚本存在，会执行此脚本')
        self.RBlog(self.G_PRE_PY)
        if os.path.exists(self.G_PRE_PY):
            sys.argv=[self.G_USERID,self.G_TASKID]
            #execfile(self.G_PRE_PY)
            if self.G_RENDEROS=='Linux':
                os.system('./' + self.G_PRE_PY)
            else:
                os.system('c:/python27/python.exe ' + self.G_PRE_PY)
        self.G_PROCESS_LOG.info('[BASE.RBprePy.end.....]')
        self.RBlog('done','end')
    '''
        创建目录
    '''       
    def RBmakeDir(self):#1
        self.G_PROCESS_LOG.info('[BASE.RBmakeDir.start.....]')
        self.RBlog('创建目录','start')
        self.RBlog('创建以下路径的目录：')
        self.RBlog(self.G_RENDER_WORK_TASK)
        self.RBlog(self.G_RENDER_WORK_OUTPUT)
        self.RBlog(self.G_RENDER_WORK_OUTPUTBAK)
        
        #renderwork
        if not os.path.exists(self.G_RENDER_WORK_TASK):
            os.makedirs(self.G_RENDER_WORK_TASK)
        
        #renderwork/output
        if not os.path.exists(self.G_RENDER_WORK_OUTPUT):
            os.makedirs(self.G_RENDER_WORK_OUTPUT)
            
        #renderwork/outputbak
        if not os.path.exists(self.G_RENDER_WORK_OUTPUTBAK):
            os.makedirs(self.G_RENDER_WORK_OUTPUTBAK)

        #RB_small
        rbSamll = os.path.join(self.G_RENDER_WORK,self.G_TASKID,'RB_small')
        self.RBlog(rbSamll)
        if not os.path.exists(rbSamll):
            os.makedirs(rbSamll)
        self.G_PROCESS_LOG.info('[BASE.RBmakeDir.end.....]')
        self.RBlog('done','end')
        
    def RBhanFile(self):#3 copy script,copy from pool,#unpack
        self.RBlog('拷贝脚本文件','start')
        self.G_PROCESS_LOG.info('[BASE.RBhanFile.start.....]')
        vbsFile=os.path.join(self.G_POOL,r'script\vbs',self.G_CONVERTVBS_NAME)
        if self.G_RENDEROS=='Linux':
            self.pythonCopy(vbsFile,"/root/script/vbs/")
            self.pythonCopy(self.G_RENDER_WORK_OUTPUT.replace('\\','/'),"/root/script/vbs/",self.G_RENDER_WORK_OUTPUTBAK.replace('\\','/'))
        else:
            #shutil.copyfile(vbsFile,"c:/script/vbs/")
            copyVBSCmd='xcopy /y /f "'+vbsFile+'" "c:/script/vbs/" '
            moveOutputCmd='c:\\fcopy\\FastCopy.exe /cmd=move /speed=full /force_close  /no_confirm_stop /force_start '+self.G_RENDER_WORK_OUTPUT.replace('/','\\')+' /to='+self.G_RENDER_WORK_OUTPUTBAK.replace('/','\\')
            
            self.RBlog(copyVBSCmd)
            self.RBlog(moveOutputCmd)
            self.RBcmd(copyVBSCmd)
        #    "c:\\fcopy\\FastCopy.exe /cmd=move /speed=full /force_close  /no_confirm_stop /force_start C:\enfwork\\212869\output\*.*  /to=C:\enfwork\\212869\outputbak"
            self.RBcmd(moveOutputCmd)
        self.G_PROCESS_LOG.info('[BASE.RBhanFile.end.....]')
        self.RBlog('done','end')
    '''
        copy文件
    '''
    def RBcopyTempFile(self):
        self.RBlog('拷贝配置文件','start')
        self.RBlog('拷贝以下配置文件：')
        self.G_PROCESS_LOG.info('[BASE.RBcopyTempFile.start.....]')
        
        tempFull=self.G_POOL_TASK
        self.RBlog(tempFull)
        #if self.G_RENDEROS=='Linux':
        #    tempFull=self.G_POOL_TASK
        self.pythonCopy(tempFull.replace('\\','/'),self.G_RENDER_WORK_TASK.replace('\\','/'))
        self.G_PROCESS_LOG.info('[BASE.RBcopyTempFile.end.....]')
        self.RBlog('done','end')
    '''
        读render.cfg文件
    '''        
    def RBreadCfg(self):#4
        self.G_PROCESS_LOG.info('[BASE.RBreadCfg.start.....]')
    
        renderTxt=self.G_CFG_PYNAME
        txtFile=open(renderTxt, 'r')
        allLines=txtFile.readlines()
        for eachLine in allLines:
            if eachLine.startswith('#') or eachLine=='\n' or eachLine.startswith('self.'):
                continue
            execStr='self.'+eachLine.strip()
            print execStr
            exec(execStr)
        self.G_PROCESS_LOG.info('[BASE.RBreadCfg.end.....]')            
            
    def RBrenderConfig(self):#5
        self.RBlog('渲染配置','start')
        self.G_PROCESS_LOG.info('[BASE.RBrenderConfig.start.....]')
        self.G_PROCESS_LOG.info('[BASE.RBrenderConfig.end.....]') 
        self.RBlog('done','end')
    '''
        写扣费文本
    '''    
    def RBwriteConsumeTxt(self):#6
        self.RBlog('写扣费信息','start')
        self.G_PROCESS_LOG.info('[BASE.RBwriteConsumeTxt.start.....]')
        self.G_FEE_LOG.info('zone='+self.G_ZONE)
        self.G_FEE_LOG.info('nodeName='+self.G_NODE_NAME)

        if self.G_RENDERTYPE=="gpu":
            self.G_FEE_LOG.info('renderType=gpu')
            self.G_PROCESS_LOG.info('[BASE.G_RENDERTYPE.....]'+self.G_RENDERTYPE)
        if self.G_USERID=='1801684' or self.G_USERID=='1811222' or self.G_USERID=='1811737' or self.G_USERID=='1820421' or self.G_USERID=='1820556' or self.G_USERID=='1821671':
            self.G_FEE_LOG.info('renderType=gpu')
        if self.G_CG_TILECOUNT !='1':
            self.G_FEE_LOG.info('tile='+self.G_CG_TILE)
            self.G_FEE_LOG.info('tileCount='+self.G_CG_TILECOUNT)
        if hasattr(self,'G_FIRST_FRAME'):
            self.G_FEE_LOG.info('firstFrame='+self.G_FIRST_FRAME)
        self.G_FEE_LOG.info('frames='+self.G_CG_START_FRAME)
        self.G_PROCESS_LOG.info('[BASE.RBwriteConsumeTxt.end.....]')
        self.RBlog('done','end')
        
    def RBrender(self):#7
        self.RBlog('渲染','start')
        self.G_PROCESS_LOG.info('[BASE.RBrender.start.....]')
        self.G_PROCESS_LOG.info('[BASE.RBrender.end.....]')
        self.RBlog('done','end')
    
    def RBpostPy(self):#pre custom
        self.RBlog('渲染完毕执行自定义脚本','start')
        self.RBlog('如果以下路径的脚本存在，则会被执行')
        self.RBlog(self.G_POST_PY)
        self.G_PROCESS_LOG.info('[BASE.RBpostPy.start.....]')
        if os.path.exists(self.G_POST_PY):
            sys.argv=[self.G_USERID,self.G_TASKID]
            #execfile(self.G_POST_PY)
            if self.G_RENDEROS=='Linux':
            	os.system('./' + self.G_POST_PY)
            else:
            	os.system('c:/python27/python.exe ' + self.G_POST_PY)
        self.G_PROCESS_LOG.info('[BASE.RBpostPy.end.....]')
        self.delNetUse()
        self.RBlog('done','end')
        
    def RvMakeDirs(self,path):
        print 'create dirs :'+path
        self.G_PROCESS_LOG.info('create dirs:'+str(path))
        try:
            if not os.path.exists(path):
                os.makedirs(path)
            return path
        except Exception, e:
            print 'create dirs :'+path+'  failed'
            self.G_PROCESS_LOG.info('create dirs:'+str(path)+' failed')

    def RBconvertDir(self,dir,workSmallPath):
        if  os.path.exists(dir):
            smallSize='200'
            if self.G_KG=='1':
                smallSize='40'
            #self.G_PROCESS_LOG.info('RBconvertDir1')
            #if int(self.G_CG_TILECOUNT)>1:
                #self.G_PROCESS_LOG.info('RBconvertDir2')
                #sqrtTile=int(math.sqrt(int(self.G_CG_TILECOUNT)))
                #self.G_PROCESS_LOG.info('RBconvertDir3')
                #smallSize=str(int(200/sqrtTile))
                #self.G_PROCESS_LOG.info('RBconvertDir4')

            
            list_dirs = os.walk(dir) 
            for root, dirs, files in list_dirs: 
                
                for name in files:
                    ext=os.path.splitext(name)[1]
                    self.G_PROCESS_LOG.info('name='+name)
                    if ext == '.vrmap' or   ext == '.vrlmap' or ext=='.exr':
                        continue    
                    workBigPic =os.path.join(root, name)
                    smallName=workBigPic.replace(dir+'\\','')
                    smallName=self.G_JOB_NAME+"_"+smallName.replace('\\','[_]').replace('.','[-]')+'.jpg'
                    workSmallPic=os.path.join(workSmallPath,smallName)
                    convertCmd='c:/ImageMagick/nconvert.exe  -out jpeg -ratio -resize '+smallSize+' 0 -overwrite -o "'+workSmallPic +'" "'+workBigPic+'"'
                    #print workBigPic
                    self.RBcmd(convertCmd,True,False)
                    self.G_FEE_LOG.info('smallPic='+smallName)
    '''
        转换缩略图
    '''
    def RBconvertSmallPic(self):    
        self.RBlog('转换缩略图','start')
        self.G_PROCESS_LOG.info('[BASE.RBconvertSmallPic.start.....]')
        workSmallPath=os.path.join(self.G_RENDER_WORK_TASK,'small')  
        self.RBlog(workSmallPath)
        self.RBlog(self.G_PATH_SMALL)
        if not os.path.exists(workSmallPath):
            os.makedirs(workSmallPath)
            
        exrToJpg=os.path.join(self.G_RENDER_WORK_TASK,'exr2jpg')
        exrToJpgBak=os.path.join(self.G_RENDER_WORK_TASK,'exr2jpgbak')
        self.RBconvertDir(self.G_RENDER_WORK_OUTPUT,workSmallPath)
        self.RBconvertDir(exrToJpg,workSmallPath)
        
        
        moveCmd='c:\\fcopy\\FastCopy.exe /cmd=move /speed=full /force_close  /no_confirm_stop /force_start "' +workSmallPath.replace('/','\\')+'\*.*" /to="'+self.G_PATH_SMALL.replace('/','\\')+'"'
        self.RBcmd(moveCmd,True,False)

        if  os.path.exists(exrToJpg):
            exrToJpgBakMove='c:\\fcopy\\FastCopy.exe /cmd=move /speed=full /force_close  /no_confirm_stop /force_start "' +exrToJpg.replace('/','\\')+'\\*.*" /to="'+exrToJpgBak.replace('/','\\')+'"'
            self.RBcmd(exrToJpgBakMove)        
        #convertCmd='cscript /nologo c:\\script\\vbs\\' + self.G_CONVERTVBS_NAME + '  '+self.G_USERID+' '+self.G_TASKID + ' "'+ self.G_JOB_NAME  +'" "'+self.G_PATH_SMALL +'\" '
        self.G_PROCESS_LOG.info('[BASE.RBconvertSmallPic.end.....]')
        self.RBlog('done','end')
    '''
        上传渲染结果和日志
    '''    
    def RBresultAction(self):
        self.G_PROCESS_LOG.info('[BASE.RBresultAction.start.....]')
        #RB_small
        if not os.path.exists(self.G_PATH_SMALL):
            os.makedirs(self.G_PATH_SMALL)
        frameCheck = os.path.join(self.G_POOL,'tools',"SingleFrameCheck.exe")
        feeLogFile=self.G_USERID+'-'+self.G_TASKID+'-'+self.G_JOB_NAME+'.txt'
        feeTxt=os.path.join(self.G_RENDER_WORK_TASK,feeLogFile)
        if self.G_RENDEROS=='Linux':
            outputPath="/output"
            ouputbakPath="/outputbak"
            feePath="/fee"
            outputFolder=self.G_PATH_USER_OUTPUT[self.G_PATH_USER_OUTPUT.rfind("\\")+1:len(self.G_PATH_USER_OUTPUT)]
            outputmnt='mount -t cifs -o username=administrator,password=Ruiyun@2012,codepage=936,iocharset=gb2312 '+self.G_PATH_USER_OUTPUT.replace(outputFolder,'').replace('\\','/')+' '+outputPath
            feemnt='mount -t cifs -o username=administrator,password=Ruiyun@2012,codepage=936,iocharset=gb2312 '+self.G_PATH_COST.replace('\\','/')+' '+feePath
            if not os.path.exists(outputPath):
                os.makedirs(outputPath)
            if not os.path.exists(feePath):
                os.makedirs(feePath)
            self.RBcmd(outputmnt,False,1)
            self.RBcmd(feemnt,False,1)
            outputPath=outputPath+"/"+outputFolder
            if not os.path.exists(outputPath):
                os.makedirs(outputPath)

            self.pythonCopy(self.G_RENDER_WORK_OUTPUT.replace('\\','/'),outputPath)
            self.pythonCopy(self.G_RENDER_WORK_OUTPUT.replace('\\','/'),self.G_RENDER_WORK_OUTPUTBAK.replace('\\','/'))
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
            
            try:
                self.checkResult()
            except Exception, e:
                print '[checkResult.err]'
                print e
            
            
            self.RBcmd(cmd2)
            self.RBTry3cmd(cmd3)
            self.RBcmd(cmd4)
        self.G_PROCESS_LOG.info('[BASE.RBresultAction.end.....]')
    '''
        上传渲染结果和日志
    ''' 
    def RBhanResult(self):#8
        self.RBlog('结果处理','start')
        self.G_PROCESS_LOG.info('[BASE.RBhanResult.start.....]')        
        if hasattr(self,'argsmap'):
            # 只渲染光子
            
            if self.argsmap.has_key('onlyphoton'):
                if self.argsmap['onlyphoton'] in 'true' and self.argsmap['kg'] != '102':
                    self.RBresultAction()
                    pass
                else:
                    if self.argsmap.has_key('currentTask'):
                        if self.argsmap['currentTask'] in 'photon':
                            photonPath=self.argsmap['inputDataPath']+self.G_USERID_PARENT+"/"+self.G_USERID+"/"+self.argsmap['projectSymbol']+"/max/photon/"
                            frameCheck = os.path.join(self.G_POOL,'tools',self.G_SINGLE_FRAME_CHECK)
                            uploadPath=photonPath+self.G_TASKID+'/'
                            #uploadCmd='c:\\fcopy\\FastCopy.exe /cmd=move /speed=full /force_close  /no_confirm_stop /force_start "' +self.G_RENDER_WORK_OUTPUT.replace('/','\\')+'\*.*" /to="'+uploadPath.replace('/','\\')+'"'
                            uploadCmd='c:\\fcopy\\FastCopy.exe /speed=full /force_close  /no_confirm_stop /force_start "' +self.G_RENDER_WORK_OUTPUT.replace('/','\\')+'\*.*" /to="'+uploadPath.replace('/','\\')+'"'
                            frameCheckcmd='"' +frameCheck + '" "' + self.G_RENDER_WORK_OUTPUT + '" "'+ uploadPath.rstrip()+'"'
                            bakCmd='c:\\fcopy\\FastCopy.exe /cmd=move /speed=full /force_close  /no_confirm_stop /force_start "' +self.G_RENDER_WORK_OUTPUT.replace('/','\\')+'\*.*" /to="'+self.G_RENDER_WORK_OUTPUTBAK.replace('/','\\')+'"'
                            self.RvMakeDirs(uploadPath)
                            feeLogFile=self.G_USERID+'-'+self.G_TASKID+'-'+self.G_JOB_NAME+'.txt'
                            feeTxt=os.path.join(self.G_RENDER_WORK_TASK,feeLogFile)
                            feeLogCmd='xcopy /y /f "'+feeTxt+'" "'+self.G_PATH_COST+'/" '
                            self.RBcmd(uploadCmd)
                            self.RBcmd(frameCheckcmd)
                            self.RBcmd(bakCmd)
                            self.RBcmd(feeLogCmd)
                            pass
                        else:
                            self.RBresultAction()
                            pass
                        pass
                    else:
                        self.RBresultAction()                   
                    
            else:
                self.RBresultAction()
                pass   
        else:
            self.RBresultAction()
        
        
        
             
        # if hasattr(self,'G_KG'):
        #     if self.G_KG=='2' or self.G_KG=='3':#inc or animation 
            
        #         workMap=os.path.join(self.G_RENDER_WORK_OUTPUT,'*.vrmap')
        #         renderTemp=os.path.join(self.G_POOL,'temp',(self.G_FATHERID+'_render'))
        #         copyCmdStr='c:\\fcopy\\FastCopy.exe /cmd=diff /speed=full /force_close  /no_confirm_stop /force_start "'+workMap.replace('/','\\')+'" /to="'+renderTemp.replace('/','\\')+'\\"'
        #         self.RBcmd(copyCmdStr)
                
        #         self.RBresultAction()
        #     elif self.G_KG=='4':#fast photon
        #         print 'fast photon'
        #         workMap = os.path.join(self.G_RENDER_WORK_OUTPUT,'*.vrmap')
        #         mergePoolTemp=os.path.join(self.G_POOL,'temp',(self.G_MERGE_TASKID+'_mergephoton'),'temp')
        #         cmdStr='c:\\fcopy\\FastCopy.exe  /speed=full /force_close  /no_confirm_stop /force_start "' +workMap.replace('/','\\') +'" /to="'+mergePoolTemp+'"'
        #         self.RBcmd(cmdStr)
        #         frameCheck = os.path.join(self.G_POOL,'tools',self.G_SINGLE_FRAME_CHECK)
        #         cmd2='"' +frameCheck + '" "' + self.G_RENDER_WORK_OUTPUT + '" "'+ mergePoolTemp+'"'
        #         cmd3='c:\\fcopy\\FastCopy.exe /cmd=move /speed=full /force_close  /no_confirm_stop /force_start "' +self.G_RENDER_WORK_OUTPUT.replace('/','\\')+'\*.*" /to="'+self.G_RENDER_WORK_OUTPUTBAK.replace('/','\\')+'"'
                
        #         feeLogFile=self.G_USERID+'-'+self.G_TASKID+'-'+self.G_JOB_NAME+'.txt'
        #         feeTxt=os.path.join(self.G_RENDER_WORK_TASK,feeLogFile)
        #         cmd4='xcopy /y /f "'+feeTxt+'" "'+self.G_PATH_COST+'/" '
                
        #         self.RBcmd(cmd2)
        #         self.RBcmd(cmd3)
        #         self.RBcmd(cmd4)
        #         self.G_PROCESS_LOG.info('[BASE.RBresultAction.end.....]')
        #     else:
        #         self.RBresultAction()
        # else:
        #     self.RBresultAction()
        
        self.G_PROCESS_LOG.info('[BASE.RBhanResult.end.....]')
        self.RBlog('done','end')
    
    def checkResult(self):
        self.G_PROCESS_LOG.info( '================[checkResult]===============')
        serverOutput=self.G_PATH_USER_OUTPUT.encode(sys.getfilesystemencoding())
        nodeOutput=self.G_RENDER_WORK_OUTPUT.replace('\\','/')
        self.G_PROCESS_LOG.info('')
        self.G_PROCESS_LOG.info(nodeOutput)
        self.G_PROCESS_LOG.info(serverOutput)
        self.G_PROCESS_LOG.info('')
        nodeImgDict={}
        serverImgDict={}
        for root, dirs, files in os.walk(nodeOutput) : 
            for name in files:
                #------------node output file----------------
                nodeImgFile =os.path.join(root, name).replace('\\','/')
                imgFile=nodeImgFile.replace(nodeOutput,'')
                
                imgFileStat=os.stat(nodeImgFile)
                imgFileSize=str(os.path.getsize(nodeImgFile))
                nodeImgDict[imgFile]=imgFileSize
                date = datetime.datetime.fromtimestamp(imgFileStat.st_ctime)  
                imgFileCtime= date.strftime('%Y%m%d%H%M%S')  
                #imgFileCtime=str(imgFileStat.st_ctime)
                imgFileInfo='[node]'+imgFile+' ['+imgFileSize+'] ['+imgFileCtime+']'
                
                self.G_PROCESS_LOG.info(imgFileInfo)
                #------------server output file----------------
                serverImgFile=(serverOutput+imgFile).replace('/','\\')
                serverImgFileInfo=''
                if os.path.exists(serverImgFile):
                    imgFileStat=os.stat(serverImgFile)
                    imgFileSize=str(os.path.getsize(serverImgFile))
                    
                    date = datetime.datetime.fromtimestamp(imgFileStat.st_ctime)  
                    imgFileCtime= date.strftime('%Y%m%d%H%M%S')
                    serverImgFileInfo='[server]'+imgFile+' ['+imgFileSize+'] ['+imgFileCtime+']'
                    serverImgDict[imgFile]=imgFileSize
                else:
                    serverImgFileInfo='[server]'+imgFile+' [missing]'
                
                self.G_PROCESS_LOG.info(serverImgFileInfo)
                self.G_PROCESS_LOG.info('')
                
                
        checkObj=CheckFrame(self.G_PROCESS_LOG)
        self.G_PROCESS_LOG.info('\r\n\r\n-----------------CheckFrame---------------')
        self.G_PROCESS_LOG.info("\nFinal chech result: ",checkObj.checkFrames(nodeOutput,serverOutput))
        self.G_PROCESS_LOG.info('')

    '''
        调用子进程运行cmd命令
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
                sys.exit(resultCode)
        return resultStr

    def pythonCopy(self,soure,to,continueOnErr=False,myShell=False):
        self.G_PROCESS_LOG.info('copy...from..'+soure+'....to..'+to)
        to = to.replace('\\','/')
        soure = soure.replace('\\','/')
        try:
            if not os.path.exists(to):
                os.makedirs(to)
            if not os.path.isdir(soure):
                self.G_PROCESS_LOG.info('file...copy..')
                shutil.copy(soure,to)
            else:
                self.G_PROCESS_LOG.info('dir...copy..')
                self.copyPyFolder(soure,to)
        except:
            self.G_PROCESS_LOG.info('copy...error.')
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


    def RBTry3cmd(self,cmdStr,continueOnErr=False,myShell=False):#continueOnErr=true-->not exit ; continueOnErr=false--> exit 
        print str(continueOnErr)+'--->>>'+str(myShell)
        self.G_PROCESS_LOG.info('cmd...'+cmdStr)
        #self.G_PROCESS_LOG.info('try3...')
        l=0
        resultStr=''
        resultCode=0
        while l < 3:
            l=l+1;
            cmdp=subprocess.Popen(cmdStr,stdin = subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.STDOUT, shell = myShell)
            cmdp.stdin.write('3/n')
            cmdp.stdin.write('4/n')
            while cmdp.poll()==None:
                resultLine = cmdp.stdout.readline().strip()
                if resultLine!='':
                    self.G_PROCESS_LOG.info(resultLine)
                
            resultStr = cmdp.stdout.read()
            resultCode = cmdp.returncode
            if resultCode==0:
                break
            else:
                time.sleep(1)
        
        self.G_PROCESS_LOG.info('resultStr...'+resultStr)
        self.G_PROCESS_LOG.info('resultCode...'+str(resultCode))
        
        if not continueOnErr:
            if resultCode!=0:
                sys.exit(resultCode)
        return resultStr

    def RBgetPluginDict(self):
        self.G_PROCESS_LOG.info('[Max.RVgetPluginDict start]')
        self.G_RAYVISION_PLUGINSCFG=os.path.join(self.G_RENDER_WORK_TASK,'cfg','plugins.cfg')
        self.G_PROCESS_LOG.info(self.G_RAYVISION_PLUGINSCFG)
        print self.G_RAYVISION_PLUGINSCFG
        plginInfoDict=None
        if  os.path.exists(self.G_RAYVISION_PLUGINSCFG):
            fp = open(self.G_RAYVISION_PLUGINSCFG)

            if fp:
                self.G_PROCESS_LOG.info('plugins file is exists')
                listOfplgCfg = fp.readlines()
                removeNL = [(i.rstrip('\n')) for i in listOfplgCfg]
                combinedText = ''.join(removeNL)
                plginInfoDict = eval('dict(%s)' % combinedText)
                print plginInfoDict
                self.G_PROCESS_LOG.info(plginInfoDict)
                for i in plginInfoDict.keys():
                    print i
                    print plginInfoDict[i]
        self.G_PROCESS_LOG.info('[Max.RVgetPluginDict end]')
        return plginInfoDict
        
    def delNetUse(self):
        try:
            self.RBcmd("net use * /del /y")
        except:
            pass
        
    '''
        渲染流程控制函数，子类可以覆盖方法
    '''    
    def RBexecute(self):#total
    
        self.RBBackupPy()
        self.RBinitLog()  
        self.RBlog('\r\n--------------------------------------------小任务开始--------------------------------------------\r\n')        
        self.RBprePy()
        self.RBmakeDir()
        self.RBcopyTempFile()
        self.readPyCfg()
        self.readRenderCfg()
        self.netPath() 
        self.copyBlack()        
        self.CheckDisk()
        # self.RBreadCfg()
        self.RBhanFile()
        self.RBrenderConfig()
        self.RBwriteConsumeTxt()
        self.RBrender()
        self.RBconvertSmallPic()
        self.RBhanResult()
        self.RBpostPy()
        self.RBlog('\r\n--------------------------------------------小任务结束--------------------------------------------\r\n')
        self.G_PROCESS_LOG.info('[BASE.RBexecute.end.....]')
        sys.exit(0)