#!/usr/bin/env python
#encoding:utf-8
# -*- coding: utf-8 -*-
import os
import logging
import time
import subprocess
import ConfigParser
import codecs
import sys
import shutil
from distutils.version import LooseVersion, StrictVersion
from RenderBase import RenderBase
from MaxDog import DogUtil
from MaxPlugin import MaxPlugin 
#update20151013\\10.50.8.15\p5\script\py\newpy\962712


class RenderbusPath():
    def __init__(self,userPath):
        self.G_INPUT_USER=userPath
        

        
        

    
    def InterPath(self,p):
        firstTwo = p[0:2]
        if firstTwo == '//' or firstTwo == '\\\\':
            normPath = p.replace('\\', '/')
            index = normPath.find('/', 2)
            if index <= 2:
                return False
            return True
        
    def parseInterPath(self,p):
        firstTwo = p[0:2]
        if firstTwo == '//' or firstTwo == '\\\\':
            normPath = p.replace('\\', '/')
            index = normPath.find('/', 2)
            if index <= 2:
                return ''
            
            return p[:index],p[index:]

    def convertToRenderbusPath(self,itemPath):

        absPath=[['a:/','/a/'],
            ['b:/','/b/'],
            ['c:/','/c/'],
            ['d:/','/d/']]
            
        resultMaxFile = itemPath
        src_max_lowercase = os.path.normpath(itemPath.lower()).replace('\\', '/')
        is_abcd_path = False;
        is_InterPath = False;
        
        if self.InterPath(src_max_lowercase):
            start,rest = self.parseInterPath(src_max_lowercase)
            resultMaxFile= self.G_INPUT_USER + '/net' + start.replace('//', '/') + rest.replace('\\', '/') 
        else:
            resultMaxFile= self.G_INPUT_USER + '\\' + itemPath.replace('\\', '/').replace(':','')

        return os.path.normpath(resultMaxFile)
        
        
    def convertToUserPath(self,sourceFile):
        resultFile = sourceFile
        userInput=self.G_INPUT_USER
        userInput=userInput.replace('/','\\')
        sourceFile=sourceFile.replace('/','\\').replace(userInput,'')
        
        if sourceFile.startswith('net'):
            resultFile = '\\\\'+sourceFile[3:]
        elif sourceFile.startswith('a\\') or sourceFile.startswith('b\\') or sourceFile.startswith('c\\') or sourceFile.startswith('d\\'):
            resultFile = sourceFile[0]+':'+sourceFile[1:]
        else:
            resultFile=sourceFile[0]+':'+sourceFile[1:]
        
        resultFile=resultFile.replace('\\','/')
        return resultFile
        
        
        
class Preprocess(RenderBase):

    '''
        初始化构造函数
    '''
    def __init__(self,**paramDict):
        RenderBase.__init__(self,**paramDict)
        self.tempMark=0
        print 'PreprocessTasK init'
        self.G_PLUGINS_MAX_SCRIPT='B:/plugins/max/script'
        self.G_HELPER=r'c:\work\helper'
        self.G_HELPER_TASK=os.path.join(self.G_HELPER,self.G_TASKID)
        self.G_HELPER_TASK_MAX=os.path.join(self.G_HELPER_TASK,'max')
        self.G_HELPER_TASK_MAX2=os.path.join(self.G_HELPER_TASK,'max2')
        self.G_HELPER_TASK_MAXBAK=os.path.join(self.G_HELPER_TASK,'maxbak')
        self.G_HELPER_TASK_CFG=os.path.join(self.G_HELPER_TASK,'cfg')
        
        self.G_RENDER=r'c:\work\render'
        self.G_RENDER_TASK=os.path.join(self.G_RENDER,self.G_TASKID)
        self.G_RENDER_TASK_MAX=os.path.join(self.G_RENDER_TASK,'max')
        
        self.G_RAYVISION_PLUGINSCFG=os.path.join(self.G_HELPER_TASK_CFG,'plugins.cfg')
        print self.G_HELPER_TASK_MAX
        self.tempFileFolder=os.path.join(self.G_POOL,'temp',(self.G_TASKID+'_render'),'max')
        self.G_DRIVERC_7Z='c:/7-Zip/7z.exe'
        #self.packFileName=os.path.join(self.G_HELPER_TASK_MAX,'max.full');
        self.fileCount=0
        
        self.MAX_PREPROCESS=False
        self.ASSET_WEB_COOLECT_BY_PATH=False
        self.ASSET_INPUT_DIR=''
        self.ASSET_INPUT_DIR_DICT={}
        
        pySitePackagesPool=os.path.join(self.G_POOL,'script','pySitePackages').replace('/','\\')
        cScript=r'c:\script\\'
        pySitePackagesNode=cScript+'pySitePackages'
        copyPySitePackagesCmd=r'c:\fcopy\FastCopy.exe /speed=full /force_close /no_confirm_stop /force_start "'+pySitePackagesPool+'" /to="'+cScript+'"'
        print copyPySitePackagesCmd
        self.simpleCmd(copyPySitePackagesCmd)
        sys.path.append(pySitePackagesNode)
        self.chardet = __import__('chardet')
        
        if os.path.exists(self.G_HELPER_TASK):
            shutil.rmtree(self.G_HELPER_TASK)
        pass
        
        self.G_MAX_B='B:/plugins/max'
        self.G_MAXSCRIPT=self.G_MAX_B+'/script'
           
    def checkFileCode(self,myFile):
        print myFile
        if os.path.exists(myFile):
            f = open(myFile,'r')
            fencoding=self.chardet.detect(f.read())
            f.close()
            print fencoding
            print fencoding['encoding']
            return fencoding['encoding']
        
    def simpleCmd(self,cmdStr,myShell=False):#continueOnErr=true-->not exit ; continueOnErr=false--> exit
        print cmdStr
        cmdp=subprocess.Popen(cmdStr,stdin = subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.STDOUT, shell = myShell)
        while cmdp.poll()!=None:
            resultLine = cmdp.stdout.readline().strip()
        resultStr = cmdp.stdout.read()
        resultCode = cmdp.returncode
        return resultStr
        
    def isScriptUpdateOk(self,flagUpdate):
        if self.RENDER_CFG_PARSER.has_option('common','update'):
            scriptupdateStr=self.RENDER_CFG_PARSER.get('common','update')
            scriptupdate=int(scriptupdateStr)
            if scriptupdate>flagUpdate or scriptupdate==flagUpdate:
                return True
        return False
        

    '''
        预处理任务，根据配置文件的文件，添加预处理的压缩max文件
    '''
    def RBrender(self):
        self.G_FEE_LOG.info('startTime='+str(int(time.time())))
        self.G_FEE_LOG.info('endTime='+str(int(time.time())))
        self.G_RENDER_LOG.info('startTime='+str(int(time.time())))
        self.G_RENDER_LOG.info('endTime='+str(int(time.time())))
        
        
        
        netRenderTxt=os.path.join(self.G_PLUGINS_MAX_SCRIPT,'user',self.G_USERID,'netrender.txt').replace('\\','/')
        self.G_PROCESS_LOG.info('netRenderTxt-------'+netRenderTxt)
        if  os.path.exists(netRenderTxt):
            self.G_PROCESS_LOG.info('------Net render process--------')
            propath= self.G_USERID_PARENT+"\\"+self.G_USERID
            if self.argsmap.has_key('from') and self.argsmap['from']=='web':
                if self.RENDER_CFG_PARSER.has_section('max'):
                    
                    userInput=self.G_PATH_USER_INPUT.replace('/','\\')+propath
                    maxKeyList=self.RENDER_CFG_PARSER.options('max')
                    for maxKey in maxKeyList:
                        maxFile=self.RENDER_CFG_PARSER.get('max',maxKey)
                        if os.path.exists(maxFile):
                            targetPath=self.G_HELPER_TASK_MAX.replace('/','\\')#+os.path.dirname(maxFile).replace(userInput,'')
                            self.G_PROCESS_LOG.info('unicode')
                            cmd=u'c:\\fcopy\\FastCopy.exe  /speed=full /force_close  /no_confirm_stop /force_start "'+maxFile+'" /to="'+targetPath+'"'
                            self.G_PROCESS_LOG.info('[PreprocessTasK.copyFile.cmd.....]'+cmd.encode(sys.getfilesystemencoding()))
                            self.RBcmd(cmd.encode(sys.getfilesystemencoding()))
                            
                            #cmd='c:/exdupe.exe -t16f '+self.G_HELPER_TASK_MAX+' '+self.G_HELPER_TASK_MAX+'.full'
                            cmdPack=r'"'+self.G_DRIVERC_7Z+'" a -t7z "'+self.G_HELPER_TASK_MAX+'.7z" "'+self.G_HELPER_TASK_MAX+'\*"  -mmt -r'
                            self.G_PROCESS_LOG.info(cmdPack)
                            #print cmd
                            self.RBcmd(cmdPack)
            else:
                self.G_PROCESS_LOG.info('submit from Client')
                if self.RENDER_CFG_PARSER.has_section('texture'):
                    textureKeyList=self.RENDER_CFG_PARSER.options('texture')
                    for textureKey in textureKeyList:
                        
                        files=self.RENDER_CFG_PARSER.get('texture',textureKey)
                        file1=(files.split('>>')[1]).replace('/','\\')
                        if file1.endswith('.max') or file1.endswith('.max.7z'):
                            filedir=file1[file1.find(propath)+len(propath):file1.rfind("\\")]
                            filePath=(self.G_PATH_USER_INPUT+file1[1:len(file1)]).replace('/','\\')
                            self.G_PROCESS_LOG.info(filePath)
                            if os.path.exists(filePath):
                                targetPath=self.G_HELPER_TASK_MAX.replace('/','\\')#+filedir
                                self.G_PROCESS_LOG.info('unicode')
                                cmd=u'c:\\fcopy\\FastCopy.exe  /speed=full /force_close  /no_confirm_stop /force_start "'+filePath+'" /to="'+targetPath+'"'
                                self.G_PROCESS_LOG.info('[PreprocessTasK.copyFile.cmd.....]'+cmd.encode(sys.getfilesystemencoding()))
                                self.RBcmd(cmd.encode(sys.getfilesystemencoding()))
                                
                                #filePath=\\10.50.241.9\d\inputdata5\1015500\1015735\d\work\HS\max\Volcano_03max_001_fumefx02_gai02_06_08.max.7z
                                #self.G_HELPER_TASK_MAX
                                filePath2=os.path.join(self.G_HELPER_TASK_MAX,filePath.split("\\")[-1])
                                print self.G_HELPER_TASK_MAX
                                print filePath2
                                #if file1.endswith('.max.7z'):
                                if filePath2.endswith('.max.7z'):
                                    #maxZipPath,maxZipPathName=os.path.split(file1)
                                    maxZipPath,maxZipPathName=os.path.split(filePath2)
                                    #unPackMaxCmd=self.G_DRIVERC_7Z+' e "'+file1+'" -o"'+maxZipPath+'/" -y ' 
                                    unPackMaxCmd=self.G_DRIVERC_7Z+' e "'+filePath2+'" -o"'+maxZipPath+'/" -y ' 
                                    unPackMaxCmd=unPackMaxCmd.encode(sys.getfilesystemencoding())
                                    self.RBcmd(unPackMaxCmd)
                                    
                                    moveToMaxBakCmd='c:\\fcopy\\FastCopy.exe /cmd=move /speed=full /force_close  /no_confirm_stop /force_start "'+filePath2.replace('/','\\')+'" /to="'+self.G_HELPER_TASK_MAXBAK.replace('/','\\')+'"'
                                    moveToMaxBakCmd=moveToMaxBakCmd.encode(sys.getfilesystemencoding())
                                    self.RBcmd(moveToMaxBakCmd)
                                    
                                cmdPack=r'"'+self.G_DRIVERC_7Z+'" a -t7z "'+self.G_HELPER_TASK_MAX+'.7z" "'+self.G_HELPER_TASK_MAX+'\*"  -mmt -r'
                                self.G_PROCESS_LOG.info(cmdPack)
                                #print cmd
                                self.RBcmd(cmdPack)
                                
                                
        else:
            self.iflList=[]
            #if self.RENDER_CFG_PARSER.has_section('asset_input'):
            if self.argsmap.has_key('from') and self.argsmap['from']=='web':
                self.copyFileWeb()
            else:
                self.CopyFile2()
            self.unpackMax7z()
            self.handleIfl()
            self.runMax()
            self.PackFile2()
            
    def RBrenderConfig(self):
        self.G_PROCESS_LOG.info('[PreprocessTasK.RBrenderConfig.start.....]')
        
        
        pluginPath=self.argsmap['pluginPath']
        zip=os.path.join(pluginPath,'tools','7-Zip')
        copy7zCmd=r'c:\fcopy\FastCopy.exe /speed=full /force_close /no_confirm_stop /force_start "'+zip.replace('/','\\')+'" /to="c:\\"'
        self.RBcmd(copy7zCmd)
        
        
        self.G_PROCESS_LOG.info('[PreprocessTasK.RBrenderConfig.end.....]')
            
            
    
    def getMaxFile(self,sourceMaxFile):
        if self.argsmap.has_key('from') and self.argsmap['from']=='web':
            return self.getMaxFileWeb(sourceMaxFile)
        else:
            return self.getMaxFileClient(sourceMaxFile)
            
        
    def InterPath(self,p):
        firstTwo = p[0:2]
        if firstTwo == '//' or firstTwo == '\\\\':
            normPath = p.replace('\\', '/')
            index = normPath.find('/', 2)
            if index <= 2:
                return False
            return True
            
    def getMaxFileWeb(self,sourceMaxFile):
        self.G_PROCESS_LOG.info('\r\n\r\n\r\n-----------[-getMaxFileWeb-]--------------\r\n\r\n\r\n')
        
        if self.ASSET_WEB_COOLECT_BY_PATH:
            resultMaxFile = sourceMaxFile
            userInput=self.argsmap['inputDataPath']+self.G_USERID_PARENT+"/"+self.G_USERID+"/"
            userInput=userInput.replace('/','\\')
            sourceMaxFile=sourceMaxFile.replace('/','\\').replace(userInput,'')
            
            self.G_PROCESS_LOG.info(sourceMaxFile)
            if sourceMaxFile.startswith('__'):
                resultMaxFile = self.G_HELPER_TASK_MAX+'/'+sourceMaxFile
            elif sourceMaxFile.startswith('a') or sourceMaxFile.startswith('b') or sourceMaxFile.startswith('c') or sourceMaxFile.startswith('d'):
                resultMaxFile = self.G_HELPER_TASK_MAX+'/'+sourceMaxFile
            else:
                resultMaxFile=sourceMaxFile[0]+':'+sourceMaxFile[1:]
            
            resultMaxFile=resultMaxFile.replace('\\','/')
            self.G_PROCESS_LOG.info(resultMaxFile)
            return resultMaxFile
        else:
            resultMaxFile = self.G_HELPER_TASK_MAX+'/'+os.path.basename(sourceMaxFile)
            return resultMaxFile
        
    def getMaxFileClient(self,sourceMaxFile):
        self.RBlog('-----getMaxFileClient-----')
        self.RBlog(sourceMaxFile)
        netRenderTxt=os.path.join(self.G_MAXSCRIPT,'user',self.G_USERID,'netrender.txt').replace('\\','/')
        self.RBlog(netRenderTxt)
        if  os.path.exists(netRenderTxt):
            self.RBlog('net render')
            cgFileName=os.path.basename(sourceMaxFile)
            cgFile=os.path.join(self.G_HELPER_TASK_MAX,cgFileName).replace('\\','/')
            self.RBlog(cgFile)
            return cgFile
            
        absPath=[['a:/','/a/'],
            ['b:/','/b/'],
            ['c:/','/c/'],
            ['d:/','/d/']]
            
        resultMaxFile = sourceMaxFile
        src_max_lowercase = os.path.normpath(sourceMaxFile.lower()).replace('\\', '/')
        is_abcd_path = False;
        is_InterPath = False;
       
        for prefix in absPath:
            if src_max_lowercase.startswith(prefix[0]):
                is_abcd_path = True
                resultMaxFile = self.G_HELPER_TASK_MAX + src_max_lowercase.replace(prefix[0], prefix[1])
                break;
            
        if not is_abcd_path:
            if self.InterPath(src_max_lowercase):
                start,rest = self.parseInterPath(src_max_lowercase)
                resultMaxFile= self.G_HELPER_TASK_MAX + '/net' + start.replace('//', '/') + rest.replace('\\', '/') 
            else:
                resultMaxFile= sourceMaxFile.replace('\\', '/') 

        return os.path.normpath(resultMaxFile)

        
    def writeMsFile(self,msFile,sceneFile):

        msFileObject=codecs.open(msFile,'w',"utf-8")
        scriptMsName='processU.ms'
        if self.G_CG_VERSION=='3ds Max 2012' or self.G_CG_VERSION=='3ds Max 2011' or self.G_CG_VERSION=='3ds Max 2010' or self.G_CG_VERSION=='3ds Max 2009':
            #msFileObject=codecs.open(msFile,'w',"gbk")
            msFileObject=codecs.open(msFile,'w',sys.getfilesystemencoding())
            scriptMsName='processA.ms'
            
        userMsScript=self.G_MAXSCRIPT+'/user/'+self.G_USERID+'/'+scriptMsName
        msScript=self.G_MAXSCRIPT+'/'+scriptMsName
        if os.path.exists(userMsScript):
            msScript=userMsScript
        msFileObject.write('(DotNetClass "System.Windows.Forms.Application").CurrentCulture = dotnetObject "System.Globalization.CultureInfo" "zh-cn"\r\n')
        msFileObject.write('filein @"'+msScript+'"\r\n')
        
        if self.argsmap.has_key('from') and self.argsmap['from']=='web':
            myCamera= self.RENDER_CFG_PARSER.get('common','renderablecamera')
            
        else:
            myCamera= self.RENDER_CFG_PARSER.get('renderSettings','renderablecamera')
            if self.RENDER_CFG_PARSER.has_option('renderSettings','renderablecameras'):
                renderableCameraStr = self.RENDER_CFG_PARSER.get('renderSettings','renderablecameras')
                myCamera=self.G_CG_OPTION
        clientArrayStr= '#("'+self.G_USERID+'","'+self.G_USERID_PARENT+'","'+self.G_TASKID+'","'
        clientArrayStr=clientArrayStr+self.G_JOB_NAME+'","'+sceneFile+'","'+self.G_PLATFORM+'","'+myCamera+'","client")\r\n'
        mystr='doFN '+clientArrayStr#+self.G_USERID+'" "'+self.G_TASKID+'" "'+notRender+'" "'+renderFrame+'" "'+self.G_CG_TILE+'" "'+self.G_CG_TILECOUNT+'" "'+self.G_KG+'" "'+self.G_JOB_NAME+'"  "'+renderOutput+'/" '+arrayStr+' "'+self.CURRENT_TASK+'"\r\n'

        msFileObject.write(mystr)
        msFileObject.close()
        self.G_PROCESS_LOG.info('[Max.writeMsFile.end.....]')
        return msFile
       
       
        
        
    def runMax(self):
        if self.MAX_PREPROCESS:
            #self.substPath()
            
            self.PLUGIN_DICT=self.RBgetPluginDict()
            self.G_CG_VERSION=self.PLUGIN_DICT['renderSoftware']+' '+self.PLUGIN_DICT['softwareVer']
            self.G_PROCESS_LOG.info(self.G_CG_VERSION)
            maxPlugin=MaxPlugin(self.G_RAYVISION_PLUGINSCFG,self.G_PROCESS_LOG)
            maxPlugin.config()
            
            msFile=os.path.join(self.G_HELPER_TASK_CFG,'preproces.ms').replace('\\','/')
            cgFile=self.RENDER_CFG_PARSER.get('max','max').replace('\\','/')
            #self.MAX_FILE=self.getMaxFile(cgFile)
            
            #max2File=os.path.join(self.G_HELPER_TASK_MAX2,os.path.basename(self.MAX_FILE))
            #max2File2=os.path.join(self.G_HELPER_TASK_MAX2,(self.G_TASKID+'.max'))
            #self.G_PROCESS_LOG.info(max2File)
            #self.G_PROCESS_LOG.info(max2File2)
            self.G_PROCESS_LOG.info(cgFile)
            #os.rename(max2File,max2File2)
            #self.writeMsFile(msFile,max2File2.replace('\\','/'))
            #self.writeMsFile(msFile,self.MAX_FILE.replace('\\','/'))
            self.writeMsFile(msFile,cgFile.replace('\\','/'))
            
            maxExe =  'C:/Program Files/Autodesk/'+self.G_CG_VERSION+'/3dsmax.exe'
            preCmd = '"'+maxExe +'" -silent  -U MAXScript "'+msFile+'"'
            preCmd = preCmd.encode(sys.getfilesystemencoding())
            print preCmd
            DogUtil.maxCmd(preCmd,self.G_SIMPLE_LOG)
            #DogUtil.runCmd(preCmd)
    
            
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
        读文件
    '''
    def readFileByCode(self,path,code):
        if os.path.exists(path):
                    
            fileObj=codecs.open(path,'r',code)
            lines=fileObj.readlines()
            return lines
        pass

    
    def writeFile(self,filePath,list,code):
        fileObject=codecs.open(filePath,'w',code)
        for line in list :
            fileObject.write(line)
        fileObject.close()
        
    def convertStr2Unicode(self,str):
        if not isinstance(str, unicode):
            str=str.decode(sys.getfilesystemencoding())
        return str
        
            
    def convertIfl(self,sourceIfl,targetIfl):

        print 'targetIfl=',targetIfl
        print 'sourceIfl=',sourceIfl
        
        if os.path.exists(targetIfl):
            os.remove(targetIfl)
        
        #renderCfgFileObj=codecs.open(v,'r',encoding=sys.getfilesystemencoding())

        sourceObj=codecs.open(sourceIfl,'r')
        sourceResult=sourceObj.read()
        targetObj=codecs.open(targetIfl,'a','UTF-8')
        try:
            sourceResult2=sourceResult.decode('gbk')#.decode('utf-8')
        except Exception, e:
            try:
                sourceResult2=sourceResult.decode('utf-8')
            except Exception, e:
                print 'exception...'
        targetObj.write(sourceResult2)
        sourceObj.close()
        
        targetObj.close()
        
    def handleIfl(self):
        self.G_PROCESS_LOG.info('[[PreprocessTasK.IFL.start.....]')
        for ifl in self.iflList:
            self.G_PROCESS_LOG.info(ifl)
            fileCode=self.checkFileCode(ifl)
            iflbak=ifl+'.bak'
            os.rename(ifl,iflbak)
            
            if fileCode=='EUC-TW':
                fileCode='gb2312'
            try:
                imgList=self.readFileByCode(iflbak,fileCode)
            except Exception, e:
                print 'exception...'+fileCode
                fileCode='gb2312'
                imgList=self.readFileByCode(iflbak,fileCode)
                          
            imgBasenameList=[]
            if imgList:
                for img in imgList:
                    imgBasename=os.path.basename(img)
                    self.G_PROCESS_LOG.info(img+'......'+imgBasename)
                    imgBasenameList.append(imgBasename)
                    self.writeFile(ifl,imgBasenameList,fileCode)
            
    def handleIfl_bakutf(self):
        self.G_PROCESS_LOG.info('[[PreprocessTasK.IFL.start.....]')
        for ifl in self.iflList:
        
            self.G_PROCESS_LOG.info(ifl)
            ifl2=ifl+'.utf'
            if os.path.exists(ifl):
            
                self.convertIfl(ifl,ifl2)
                os.rename(ifl,ifl+'.bak')
                
                self.G_PROCESS_LOG.info(ifl2)
                #shutil.copyfile(ifl,ifl+'.bak')
                
                imgList=self.readFile2(ifl2)
                imgBasenameList=[]
                for img in imgList:
                    
                    imgBasename=os.path.basename(img)
                    self.G_PROCESS_LOG.info(img+'......'+imgBasename)
                    imgBasenameList.append(imgBasename)
                    self.writeFile(ifl,imgBasenameList,'utf-8')
                
    def unpackMax7z(self):
        self.G_PROCESS_LOG.info('[[PreprocessTasK.unpackMax7z.start.....]')
        if self.maxZipList:
            for maxZip in self.maxZipList:
                self.G_PROCESS_LOG.info(maxZip)
                if os.path.exists(maxZip):
                    maxZipPath,maxZipPathName=os.path.split(maxZip)
                    unPackMaxCmd=self.G_DRIVERC_7Z+' e "'+maxZip+'" -o"'+maxZipPath+'/" -y ' 
                    if self.MAX_PREPROCESS:
                        if not os.path.exists(self.G_HELPER_TASK_MAX2):
                            os.makedirs(self.G_HELPER_TASK_MAX2)
                        #unPackMaxCmd=self.G_DRIVERC_7Z+' e "'+maxZip+'" -o"'+self.G_HELPER_TASK_MAX2+'/" -y ' 
                    unPackMaxCmd=unPackMaxCmd.encode(sys.getfilesystemencoding())
                    self.RBcmd(unPackMaxCmd)
                    
                    
                    
                    moveToMaxBakCmd='c:\\fcopy\\FastCopy.exe /cmd=move /speed=full /force_close  /no_confirm_stop /force_start "'+maxZip.replace('/','\\')+'" /to="'+self.G_HELPER_TASK_MAXBAK.replace('/','\\')+'"'
                    moveToMaxBakCmd=moveToMaxBakCmd.encode(sys.getfilesystemencoding())
                    self.RBcmd(moveToMaxBakCmd)
                else:
                    self.G_PROCESS_LOG.info('max.7z missing!!!')
                
        self.G_PROCESS_LOG.info('[[PreprocessTasK.unpackMax7z.end.....]')
        
        
    def PackFile2(self):
        self.G_PROCESS_LOG.info('[[PreprocessTasK.packFile.start.....]')
        
        packMaxFolder=self.G_HELPER_TASK_MAX
        if self.MAX_PREPROCESS:
            packMaxFolder=self.G_RENDER_TASK_MAX
        self.G_PROCESS_LOG.info(packMaxFolder)
        if os.path.exists(packMaxFolder):
            
            #cmd='c:/exdupe.exe -t16f '+self.G_HELPER_TASK_MAX+' '+self.G_HELPER_TASK_MAX+'.full'
            cmd=r'"'+self.G_DRIVERC_7Z+'" a -t7z "'+self.G_HELPER_TASK_MAX+'.7z" "'+packMaxFolder+'\*"  -mmt -r'
            self.G_PROCESS_LOG.info(cmd)
            #print cmd
            self.RBcmd(cmd)
        self.G_PROCESS_LOG.info('[PreprocessTasK.packFile.end....]')

    def GetFileList(self,fileList,propath):
        projectPath=(self.G_PATH_USER_INPUT+propath).replace('/','\\')
        self.G_PROCESS_LOG.info('[[--------project file list------]')
        self.G_PROCESS_LOG.info('[[PreprocessTasK.projectPath.....]'+projectPath)
        sample_list=[]
        for parent,dirnames,filenames in os.walk(projectPath):    #三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
            for filename in filenames:                        #输出文件信息
                ff=os.path.join(parent,filename).decode('gbk')
                sample_list.append(ff)
                self.G_PROCESS_LOG.info(ff)
                #self.G_PROCESS_LOG.info(type(ff))
                
        pretxt=self.G_HELPER+self.G_TASKID

        if os.path.exists(pretxt):
            pass
        else:
            os.makedirs(pretxt)
        fh = open(pretxt+"\\pretxt.txt", 'w')
        notExistFileList=[]
        for files in fileList:
            #self.G_PROCESS_LOG.info(type(files))
            file1=(files.split('>>')[1]).replace('/','\\')
            if file1=="":
                self.G_PROCESS_LOG.info('files----'+files+"---false")
                sys.exit(-1)                  
            filePath=(self.G_PATH_USER_INPUT+file1[1:len(file1)]).replace('/','\\')
            isExists=0
            if self.isOutFile(filePath):
                self.G_PROCESS_LOG.info('[PreprocessTasK.isRendOutputFilename]'+filePath.encode(sys.getfilesystemencoding())+"--pass")
                continue
            if os.path.exists(filePath):
                #self.G_PROCESS_LOG.info('[[PreprocessTasK.packFile.renderFilePath.....]'+file1.encode('gbk'))
                fh.write(filePath+"\r\n") 
                self.fileCount=self.fileCount+1
                isExists=1
            else:
                #self.G_PROCESS_LOG.info('[[PreprocessTasK.packFile.checkProFileName-----]'+file1.encode('gbk'))
                filename=filePath[filePath.rfind("\\")+1:len(filePath)]
                for profilepath in sample_list:
                    #self.G_PROCESS_LOG.info('[[PreprocessTasK.packFile.fileName.....]'+profilepath)
                    profilename=profilepath[profilepath.rfind("\\")+1:len(profilepath)]
                    if profilename.lower()==filename.lower():
                        fh.write(profilepath+"\r\n")
                        self.fileCount=self.fileCount+1
                        isExists=1
            if isExists==0:
                notExistFileList.append(file1.encode('gbk'))
                #self.G_PROCESS_LOG.info('[[PreprocessTasK.packFile.file.....]'+filePath.encode('utf-8')+'...[not  exists]')
            else:
                self.G_PROCESS_LOG.info('[[PreprocessTasK.packFile.file.....]'+file1.encode('gbk')+'...[exists]')
        if len(notExistFileList)>0:
            for f in notExistFileList:
                self.G_PROCESS_LOG.info('[[PreprocessTasK.packFile.file.....]'+f+'...[not  exists]')
            return '-1'

        fh.close()
        return pretxt+"\\pretxt.txt"

    #rendOutputFilename
    def getOutFileName(self):
        self.rendOutputFilename = ''
        if self.RENDER_CFG_PARSER.has_option('renderSettings','rendOutputFilename'):
            self.rendOutputFilename = self.RENDER_CFG_PARSER.get('renderSettings','rendOutputFilename')
            self.G_PROCESS_LOG.info('[PreprocessTasK.rendOutputFilename......]'+self.rendOutputFilename)
        

    def isOutFile(self,filePath):
        if self.rendOutputFilename=='':
            return False
        if filePath.endswith(self.rendOutputFilename):
            return True
        return False

        
    
    def getAnimationVrmap(self,fileList,animationFile):
        print animationFile
        animationPath=os.path.dirname(animationFile)
        print animationPath
        if os.path.exists(animationPath):
            animationFileName=os.path.basename(animationFile)
            animationBaseName,animationType=os.path.splitext(animationFileName)
            print animationBaseName
            animationList=os.listdir(animationPath)
            for animationFile2 in animationList:
                if animationFile2.endswith('.vrmap'):
                    animationBaseName2=os.path.basename(animationFile2)
                    if animationBaseName2.startswith(animationBaseName):
                        print animationFile2
                        fileList.append(os.path.join(animationPath,animationFile2))
            
    
    def copyFileWeb(self):
        if self.ASSET_WEB_COOLECT_BY_PATH:
            self.copyFileWebByPath()
        else:
            self.copyFileWebByName()
        
    def copyFileWebByPath(self):
        self.G_PROCESS_LOG.info('[PreprocessTasK.copyFileWeb.start.....]')
        fileList=[]
        self.maxZipList=[]
        
        
        
        propath= self.G_USERID_PARENT+"\\"+self.G_USERID
        userInput=self.G_PATH_USER_INPUT.replace('/','\\')+propath
        self.G_PROCESS_LOG.info('[[PreprocessTasK.packFile.userInput.....]'+userInput)
        if self.RENDER_CFG_PARSER.has_section('asset_input'):
            textureKeyList=self.RENDER_CFG_PARSER.options('asset_input')
            for textureKey in textureKeyList:
                if textureKey.endswith('.vrmap') or  textureKey.endswith('.vrlmap'):
                    continue
                fileList.append(self.RENDER_CFG_PARSER.get('asset_input',textureKey))
        if self.RENDER_CFG_PARSER.has_section('max'):
            maxKeyList=self.RENDER_CFG_PARSER.options('max')
            for maxKey in maxKeyList:
                fileList.append(self.RENDER_CFG_PARSER.get('max',maxKey))
        
        
        #---------------------------render.cfg vrmap vrlmap-------------
        if self.RENDER_CFG_PARSER2.has_option('vray','gi') and  self.RENDER_CFG_PARSER2.get('vray','gi')=='true':
            if self.RENDER_CFG_PARSER2.has_option('vray','primarygiengine') and self.RENDER_CFG_PARSER2.get('vray','primarygiengine')=='0':
                #--------------------------Irradiance map_____from file--------------------------
                if self.RENDER_CFG_PARSER2.has_option('vray','irradiancemapmode') and self.RENDER_CFG_PARSER2.get('vray','irradiancemapmode')=='2':
                    print 'irrmapmode from file'
                    irrmapFile=self.RENDER_CFG_PARSER2.get('vray','irrmapfile')
                    fileList.append(self.RENDERBUS_PATH.convertToRenderbusPath(irrmapFile))
                #--------------------------Irradiance map_____Animation(rendering)--------------------------
                elif self.RENDER_CFG_PARSER2.has_option('vray','irradiancemapmode') and self.RENDER_CFG_PARSER2.get('vray','irradiancemapmode')=='7':
                    print 'irrmapmode animation (rendering)'
                    animationFile=self.RENDER_CFG_PARSER2.get('vray','irrmapfile')
                    animationFile=self.RENDERBUS_PATH.convertToRenderbusPath(animationFile)
                    self.getAnimationVrmap(fileList,animationFile)
                    
            elif self.RENDER_CFG_PARSER2.has_option('vray','primarygiengine') and self.RENDER_CFG_PARSER2.get('vray','primarygiengine')=='3':
            
                #--------------------------Light cache_____from file--------------------------
                if self.RENDER_CFG_PARSER2.has_option('vray','lightcachemode') and self.RENDER_CFG_PARSER2.get('vray','lightcachemode')=='2':
                    print 'light cache from file'
                    lightCacheFile=self.RENDER_CFG_PARSER2.get('vray','lightcachefile')
                    fileList.append(self.RENDERBUS_PATH.convertToRenderbusPath(lightCacheFile))
            
            #--------------------------Light cache_____from file--------------------------        
            if self.RENDER_CFG_PARSER2.has_option('vray','secondarygiengine') and self.RENDER_CFG_PARSER2.get('vray','secondarygiengine')=='3': 
                if self.RENDER_CFG_PARSER2.has_option('vray','lightcachemode') and self.RENDER_CFG_PARSER2.get('vray','lightcachemode')=='2':
                    print 'light cache from file'
                    lightCacheFile=self.RENDER_CFG_PARSER2.get('vray','lightcachefile')
                    fileList.append(self.RENDERBUS_PATH.convertToRenderbusPath(lightCacheFile))
        
        if fileList:
            
            for files in fileList:
                
                if self.isOutFile(files):
                    self.G_PROCESS_LOG.info('[PreprocessTasK.isRendOutputFilename]'+files.encode(sys.getfilesystemencoding())+"--pass")
                    continue
                    
                files=files.replace('/','\\')
                
                if os.path.exists(files):
                    targetPath=self.G_HELPER_TASK_MAX.replace('/','\\')+os.path.dirname(files).replace(userInput,'')
                    self.G_PROCESS_LOG.info('unicode')
                    cmd=u'c:\\fcopy\\FastCopy.exe  /speed=full /force_close  /no_confirm_stop /force_start "'+files+'" /to="'+targetPath+'"'
                    self.G_PROCESS_LOG.info('[PreprocessTasK.copyFile.cmd.....]'+cmd.encode(sys.getfilesystemencoding()))
                    self.RBcmd(cmd.encode(sys.getfilesystemencoding()))
                    
                    if files.endswith('.max.7z'):
                        maxZipName=os.path.basename(files)
                        maxZip=os.path.join(targetPath,maxZipName)
                        self.maxZipList.append(maxZip.replace('\\','/'))
                        
                else:
                    self.G_PROCESS_LOG.info('[PreprocessTasK.copyFile.files.....]'+files.encode(sys.getfilesystemencoding())+"[not exists]")
                    #sys.exit(-1)
                    #break
                
                    
        self.G_PROCESS_LOG.info('[PreprocessTasK.copyFile.end.....]')
        
    def loopInputAsset(self):
        print '\r\n\r\n\r\n----------loop user input--------'
        maxFile=self.RENDER_CFG_PARSER.get('max','max')
        print maxFile
        
        listDirs = os.walk(os.path.dirname(maxFile)) 
        for root, dirs, files in listDirs: 
            for f in files: 
                print f,os.path.join(root, f)
                self.ASSET_INPUT_DIR_DICT[f]=os.path.join(root,f)
                    
    def copyFileWebByName(self):
        self.G_PROCESS_LOG.info('[PreprocessTasK.copyFileWebByName.start.....]')
        fileList=[]
        self.maxZipList=[]
        
        propath= self.G_USERID_PARENT+"\\"+self.G_USERID
        userInput=self.G_PATH_USER_INPUT.replace('/','\\')+propath
        self.G_PROCESS_LOG.info('[[PreprocessTasK.packFile.userInput.....]'+userInput)
        
        #---------------------------------asset_input---------------------------------
        assetInputList=[]
        self.loopInputAsset()
        inputDirList=self.ASSET_INPUT_DIR_DICT.keys()
        if self.RENDER_CFG_PARSER.has_section('asset_input'):
            assetInputKeyList=self.RENDER_CFG_PARSER.options('asset_input')
            for assetKeyInput in assetInputKeyList:
                assetFile=self.RENDER_CFG_PARSER.get('asset_input',assetKeyInput)
                if assetFile.endswith('.vrmap') or  assetFile.endswith('.vrlmap'):
                    continue
                if self.isOutFile(assetFile):
                    self.G_PROCESS_LOG.info('[PreprocessTasK.isRendOutputFilename]'+assetFile.encode(sys.getfilesystemencoding())+"--pass")
                    continue
                
                assetFileName=os.path.basename(assetFile)
                if assetFileName in inputDirList:
                    assetInputFile=self.ASSET_INPUT_DIR_DICT[assetFileName]
                    assetInputList.append(assetInputFile)
                else:
                    self.G_PROCESS_LOG.info('[PreprocessTasK.copyFile.files.....]'+assetFile.encode(sys.getfilesystemencoding())+"[not exists]")
                    
        #---------------------------------max---------------------------------
        if self.RENDER_CFG_PARSER.has_section('max'):
            maxKeyList=self.RENDER_CFG_PARSER.options('max')
            for maxKey in maxKeyList:
                fileList.append(self.RENDER_CFG_PARSER.get('max',maxKey))
        
        #---------------------------------realflow---------------------------------
        if self.RENDER_CFG_PARSER.has_section('realflow'):
            self.G_PROCESS_LOG.info('............realflow..............')
            realflowKeyList=self.RENDER_CFG_PARSER.options('realflow')
            for realflowKey in realflowKeyList:
                realflowStr = self.RENDER_CFG_PARSER.get('realflow',realflowKey)
                splitedArray = realflowStr.split('|')
                startFrame  = splitedArray[0]
                endFrame    = splitedArray[1]
                paddingSize = splitedArray[2] 
                format      = splitedArray[3]
                baseDir     = splitedArray[4]
                prefix      = splitedArray[5]
                # build sequence number
                start = int(startFrame);
                end   = int(endFrame);
                fileName =  format.replace('#', '').replace('name', prefix).replace('ext', '') .replace('.', '') 
                self.G_PROCESS_LOG.info(fileName)
                for inputFile in inputDirList:
                    if inputFile.endswith('.bin') and fileName in inputFile:
                        self.G_PROCESS_LOG.info(inputFile)
                        assetInputFile=self.ASSET_INPUT_DIR_DICT[inputFile]
                        assetInputList.append(assetInputFile)
                #fileList.append(self.RENDER_CFG_PARSER.get('realflow',realflowKey))
                
        
        #---------------------------render.cfg vrmap vrlmap-------------
        if self.RENDER_CFG_PARSER2.has_option('vray','gi') and  self.RENDER_CFG_PARSER2.get('vray','gi')=='true':
            if self.RENDER_CFG_PARSER2.has_option('vray','primarygiengine') and self.RENDER_CFG_PARSER2.get('vray','primarygiengine')=='0':
                #--------------------------Irradiance map_____from file--------------------------
                if self.RENDER_CFG_PARSER2.has_option('vray','irradiancemapmode') and self.RENDER_CFG_PARSER2.get('vray','irradiancemapmode')=='2':
                    print 'irrmapmode from file'
                    irrmapFile=self.RENDER_CFG_PARSER2.get('vray','irrmapfile')
                    fileList.append(self.RENDERBUS_PATH.convertToRenderbusPath(irrmapFile))
                #--------------------------Irradiance map_____Animation(rendering)--------------------------
                elif self.RENDER_CFG_PARSER2.has_option('vray','irradiancemapmode') and self.RENDER_CFG_PARSER2.get('vray','irradiancemapmode')=='7':
                    print 'irrmapmode animation (rendering)'
                    animationFile=self.RENDER_CFG_PARSER2.get('vray','irrmapfile')
                    animationFile=self.RENDERBUS_PATH.convertToRenderbusPath(animationFile)
                    self.getAnimationVrmap(fileList,animationFile)
                    
            elif self.RENDER_CFG_PARSER2.has_option('vray','primarygiengine') and self.RENDER_CFG_PARSER2.get('vray','primarygiengine')=='3':
            
                #--------------------------Light cache_____from file--------------------------
                if self.RENDER_CFG_PARSER2.has_option('vray','lightcachemode') and self.RENDER_CFG_PARSER2.get('vray','lightcachemode')=='2':
                    print 'light cache from file'
                    lightCacheFile=self.RENDER_CFG_PARSER2.get('vray','lightcachefile')
                    fileList.append(self.RENDERBUS_PATH.convertToRenderbusPath(lightCacheFile))
            
            #--------------------------Light cache_____from file--------------------------        
            if self.RENDER_CFG_PARSER2.has_option('vray','secondarygiengine') and self.RENDER_CFG_PARSER2.get('vray','secondarygiengine')=='3': 
                if self.RENDER_CFG_PARSER2.has_option('vray','lightcachemode') and self.RENDER_CFG_PARSER2.get('vray','lightcachemode')=='2':
                    print 'light cache from file'
                    lightCacheFile=self.RENDER_CFG_PARSER2.get('vray','lightcachefile')
                    fileList.append(self.RENDERBUS_PATH.convertToRenderbusPath(lightCacheFile))
        
        
        for files in assetInputList:
            files=files.replace('/','\\')
            targetPath=self.G_HELPER_TASK_MAX.replace('/','\\')
            self.G_PROCESS_LOG.info('unicode')
            cmd=u'c:\\fcopy\\FastCopy.exe  /speed=full /force_close  /no_confirm_stop /force_start "'+files+'" /to="'+targetPath+'"'
            self.G_PROCESS_LOG.info('[PreprocessTasK.copyFile.cmd.....]'+cmd.encode(sys.getfilesystemencoding()))
            self.RBcmd(cmd.encode(sys.getfilesystemencoding()))
            
                
        for files in fileList:
                
            files=files.replace('/','\\')
            
            if os.path.exists(files):
                targetPath=self.G_HELPER_TASK_MAX.replace('/','\\')
                self.G_PROCESS_LOG.info('unicode')
                cmd=u'c:\\fcopy\\FastCopy.exe  /speed=full /force_close  /no_confirm_stop /force_start "'+files+'" /to="'+targetPath+'"'
                self.G_PROCESS_LOG.info('[PreprocessTasK.copyFile.cmd.....]'+cmd.encode(sys.getfilesystemencoding()))
                self.RBcmd(cmd.encode(sys.getfilesystemencoding()))
                
                if files.endswith('.max.7z'):
                    maxZipName=os.path.basename(files)
                    maxZip=os.path.join(targetPath,maxZipName)
                    self.maxZipList.append(maxZip.replace('\\','/'))
                    
            else:
                self.G_PROCESS_LOG.info('[PreprocessTasK.copyFile.files.....]'+files.encode(sys.getfilesystemencoding())+"[not exists]")
                #sys.exit(-1)
                #break
                
                    
        self.G_PROCESS_LOG.info('[PreprocessTasK.copyFile.end.....]')
        
    def CopyFile2(self):
        self.G_PROCESS_LOG.info('[PreprocessTasK.copyFile2.start.....]')
        fileList=[]
        self.maxZipList=[]
        textureKeyList=self.RENDER_CFG_PARSER.options('texture')
        
        propath= self.G_USERID_PARENT+"\\"+self.G_USERID
        self.G_PROCESS_LOG.info('[[PreprocessTasK.packFile.propath.....]'+propath)
        #self.G_PROCESS_LOG.info('[PreprocessTasK.copyFile.textureKeyList]')
        if self.RENDER_CFG_PARSER.has_section('texture'):
            for textureKey in textureKeyList:
                fileList.append(self.RENDER_CFG_PARSER.get('texture',textureKey))
                
                
        
        guyVersion=self.RENDER_CFG_PARSER.get('common','guyversion')
        
        
        if LooseVersion(guyVersion)>LooseVersion('4.0.2.10'):
            if self.RENDER_CFG_PARSER.has_section('vrmap'):
                self.G_PROCESS_LOG.info('---vrmap---')
                vrmapfileList=self.RENDER_CFG_PARSER.options('vrmap')
                for vrmapfileKey in vrmapfileList:
                    fileList.append(self.RENDER_CFG_PARSER.get('vrmap',vrmapfileKey))
            if self.RENDER_CFG_PARSER.has_section('vrlmap'):
                self.G_PROCESS_LOG.info('---vrlmap---')
                vrlmapfileList=self.RENDER_CFG_PARSER.options('vrlmap')
                for vrlmapfileKey in vrlmapfileList:
                    fileList.append(self.RENDER_CFG_PARSER.get('vrlmap',vrlmapfileKey))
                    
        else:
            if self.RENDER_CFG_PARSER.has_section('customfile'):
                self.G_PROCESS_LOG.info('---pre4.0.2.10.customfile---')
                customfileList=self.RENDER_CFG_PARSER.options('customfile')
                for customfileKey in customfileList:
                    fileList.append(self.RENDER_CFG_PARSER.get('customfile',customfileKey))
                    
                
        #self.G_PROCESS_LOG.info('[PreprocessTasK.copyFile.start.fileList.....]'+self.G_PATH_USER_INPUT)
        if fileList:
            commonCfg=self.RENDER_CFG_PARSER.options('common')#skipUpload
            skipUpload="0"
            if self.RENDER_CFG_PARSER.has_option('common','skipUpload'):
                skipUpload=self.RENDER_CFG_PARSER.get('common','skipUpload')
            self.G_PROCESS_LOG.info('[[PreprocessTasK.packFile.skipUpload.....]'+skipUpload)
            if skipUpload=="1":
                preFileTxt=self.GetFileList(fileList,propath)
                self.G_PROCESS_LOG.info('[[PreprocessTasK.packFile.preFileTxt.....]'+preFileTxt)
                if preFileTxt=="-1":
                    sys.exit(-1)
                else:
                    self.G_PROCESS_LOG.info('[PreprocessTasK.copyFile.fileCount.....]'+str(self.fileCount))
                    cmd=u'c:\\fcopy\\FastCopy.exe  /speed=full /force_close  /no_confirm_stop /force_start /srcfile="'+preFileTxt+'" /to="'+self.G_HELPER_TASK_MAX.replace('/','\\')+'"'
                    self.G_PROCESS_LOG.info('[PreprocessTasK.copyFile.cmd.....]'+cmd)
                    if isinstance(cmd,unicode):
                        cmd.encode('utf-8')
                    else:
                        cmd.decode('gbk').encode('utf-8')
                    self.RBcmd(cmd)
            else:
                for files in fileList:
                    #if files.endswith('.fxd')
                    file1=(files.split('>>')[1]).replace('/','\\') 
                    if file1=="":
                        self.G_PROCESS_LOG.info('files----'+files+"---false")
                        sys.exit(-1)   
                    filePath=(self.G_PATH_USER_INPUT+file1[1:len(file1)]).replace('/','\\')
                    #self.G_PROCESS_LOG.info('[[PreprocessTasK.packFile.filePath.....]'+filePath)
                    filedir=file1[file1.find(propath)+len(propath):file1.rfind("\\")]
                    #self.G_PROCESS_LOG.info('[[PreprocessTasK.packFile.filePath.....]'+filedir)
                    #print os.path.exists(filePath)
                    #filePath=self.GetFileList(propath,filePath)
                    if self.isOutFile(filePath):
                        self.G_PROCESS_LOG.info('[PreprocessTasK.isRendOutputFilename]'+filePath.encode(sys.getfilesystemencoding())+"--pass")
                        continue
                    if os.path.exists(filePath):
                        targetPath=self.G_HELPER_TASK_MAX.replace('/','\\')+filedir
                        self.G_PROCESS_LOG.info('unicode')
                        cmd=u'c:\\fcopy\\FastCopy.exe  /speed=full /force_close  /no_confirm_stop /force_start "'+filePath+'" /to="'+targetPath+'"'
                        self.G_PROCESS_LOG.info('[PreprocessTasK.copyFile.cmd.....]'+cmd.encode(sys.getfilesystemencoding()))
                        self.RBcmd(cmd.encode(sys.getfilesystemencoding()))
                        
                        if filePath.endswith('.max.7z'):
                            maxZipName=os.path.basename(filePath)
                            maxZip=os.path.join(targetPath,maxZipName)
                            self.maxZipList.append(maxZip.replace('\\','/'))
                            
                        elif filePath.endswith('.ifl'):
                            iflName=os.path.basename(filePath)
                            ifl=os.path.join(targetPath,iflName)
                            self.iflList.append(ifl.replace('\\','/'))
                    else:
                        self.G_PROCESS_LOG.info('[PreprocessTasK.copyFile.filePath.....]'+filePath.encode(sys.getfilesystemencoding())+"not exists")
                        sys.exit(-1)
                        #break
                
                    
        self.G_PROCESS_LOG.info('[PreprocessTasK.copyFile.end.....]')
        

        
        
    def RBresultAction(self):
        self.G_PROCESS_LOG.info('[BASE.RBresultAction.start.....]')
        tempFolder=os.path.join(self.G_TEMP,self.G_TASKID).replace('/','\\')
        if not os.path.exists(tempFolder):
            os.makedirs(tempFolder)
        #RB_small
        if not os.path.exists(self.tempFileFolder):
            os.makedirs(self.tempFileFolder)
        cmd='c:\\fcopy\\FastCopy.exe  /speed=full /force_close  /no_confirm_stop /force_start "'+self.G_HELPER_TASK_MAX+'.7z" /to="'+os.path.join(self.G_TEMP,self.G_TASKID).replace('/','\\')+'"'
        feeLogFile=self.G_USERID+'-'+self.G_TASKID+'-'+self.G_JOB_NAME+'.txt'
        feeTxt=os.path.join(self.G_RENDER_WORK_TASK,feeLogFile)
        cmd4='xcopy /y /f "'+feeTxt+'" "'+self.G_PATH_COST+'/" '
        
        netRenderTxt=os.path.join(self.G_PLUGINS_MAX_SCRIPT,'user',self.G_USERID,'netrender.txt').replace('\\','/')
        #if not os.path.exists(netRenderTxt):
        self.RBcmd(cmd)
        self.RBcmd(cmd4)
        
        #----------------------xcopy render_utf16.cfg to pool---------------------------
        if self.argsmap.has_key('from') and self.argsmap['from']=='web':
            tempFull=os.path.join(self.G_POOL_TASK,'cfg').replace('/','\\')
            renderCfgFile=os.path.join(self.G_HELPER_TASK_CFG,'render_max.cfg').replace('\\','/')
            cmdStr='xcopy /y /f "'+renderCfgFile+'" "'+tempFull+'\\" '
            self.RBcmd(cmdStr)
        self.G_PROCESS_LOG.info('[BASE.RBresultAction.end.....]')
    def readByCode(self,code):
        print 'read by code'
        
        
    def convertCode(self):
        renderCfgFile=os.path.join(self.G_HELPER_TASK_CFG,'render_max.cfg').replace('\\','/')
        renderTempCfgFile=os.path.join(self.G_HELPER_TASK_CFG,'render.cfg')
        print 'renderCfgFile=',renderCfgFile
        print 'renderTempCfgFile=',renderTempCfgFile
        
        if os.path.exists(renderCfgFile):
            os.remove(renderCfgFile)
        
        #renderCfgFileObj=codecs.open(renderCfgFile,'r',encoding=sys.getfilesystemencoding())

        renderTempCfgFileObj=codecs.open(renderTempCfgFile,'r')
        renderCfgFileResult=renderTempCfgFileObj.read()
        renderCfgFileResult=renderCfgFileResult.decode('utf-8')
        renderTempCfgFileObj.close()
        
        print type(renderCfgFileResult)
        #print renderCfgFileResult
        
        #print renderCfgFileResult
        renderCfgFileObj=codecs.open(renderCfgFile,'a','UTF-16')
        renderCfgFileObj.write(renderCfgFileResult)
        renderCfgFileObj.close()
        
    def readRenderCfg(self):
        self.G_PROCESS_LOG.info('[Max.readRenderCfg.start.....]'+self.G_HELPER_TASK_CFG)
        renderCfg=os.path.join(self.G_HELPER_TASK_CFG,'render.cfg').replace('/','\\')
        
        if self.argsmap.has_key('from') and self.argsmap['from']=='web':
            self.convertCode()
            
            analyseTxt=os.path.join(self.G_HELPER_TASK_CFG,'analyse_net.txt').replace('/','\\')
            unicodeList=['UTF-16','UTF-16-be','UTF-16-le','UTF-8','gbk','']
            self.RENDER_CFG_PARSER2 = ConfigParser.ConfigParser()
            parseResult=False
            if os.path.exists(analyseTxt):
                self.G_PROCESS_LOG.info('-----RENDER_CFG_PARSER2-----')
                self.G_PROCESS_LOG.info(renderCfg)
                for code in unicodeList:
                    try:
                        print code
                        self.G_PROCESS_LOG.info(code)
                        if code=='':
                            self.RENDER_CFG_PARSER2.readfp(codecs.open(renderCfg, "r"))
                            parseResult=True
                            break
                        else:
                            self.RENDER_CFG_PARSER2.readfp(codecs.open(renderCfg, "r",code))
                            parseResult=True
                            break
                    except Exception, e:
                        print 'exception...',code
                        pass
            renderCfg=analyseTxt
            
        self.RENDER_CFG_PARSER = ConfigParser.ConfigParser()
        self.G_PROCESS_LOG.info('-----RENDER_CFG_PARSER-----')
        self.G_PROCESS_LOG.info(renderCfg)
        try:
            self.G_PROCESS_LOG.info('read rendercfg by utf16')
            self.RENDER_CFG_PARSER.readfp(codecs.open(renderCfg, "r", "UTF-16"))
            
        except Exception, e:
            self.G_PROCESS_LOG.info(e)
            try:
                self.G_PROCESS_LOG.info('read rendercfg by  utf8')
                self.RENDER_CFG_PARSER.readfp(codecs.open(renderCfg, "r", "UTF-8"))
                
            except Exception, e:
                self.G_PROCESS_LOG.info(e)
                self.RENDER_CFG_PARSER.readfp(codecs.open(renderCfg, "r"))
                self.G_PROCESS_LOG.info('read rendercfg by default')
        #self.RENDER_CFG_PARSER.read(renderCfg)
        
        
        if self.RENDER_CFG_PARSER.has_option('vray','distribute') and self.RENDER_CFG_PARSER.get('vray','distribute')=='true':
            self.MAX_PREPROCESS=True
        
        
        self.G_PROCESS_LOG.info('[Max.readRenderCfg.end.....]')


    '''
        copy文件
    '''
    def RBcopyTempFile(self):
        self.G_PROCESS_LOG.info('[BASE.RBcopyTempFile.start.....]')
        #copy temp file
        #if not os.path.exists(os.path.join(self.G_RENDER_WORK_TASK,'zzz.txt')):
        tempFull=os.path.join(self.G_POOL_TASK,'*.*')
        copyPoolCmd='c:\\fcopy\\FastCopy.exe  /cmd=diff /speed=full /force_close  /no_confirm_stop /force_start "'+tempFull.replace('/','\\')+'" /to="'+self.G_HELPER_WORK_TASK.replace('/','\\')+'"'
        self.RBcmd(copyPoolCmd)
        echoCmd = 'echo ...>>'+os.path.join(self.G_HELPER_WORK_TASK,'zzz.txt').replace('\\','/')
        self.RBcmd(echoCmd,False,True)
        self.G_PROCESS_LOG.info('[BASE.RBcopyTempFile.end.....]')

    '''
        解析py.cfg文件
    '''
    def readPyCfg(self):
        self.argsmap={}         
        line=self.readFile(self.G_HELPER_CFG_PYNAME)
        for l in line:
            if "=" in l:
                params=l.split("=")
                self.argsmap[(params[0]).replace('\r','').replace('\n','')]=params[1].replace('\n','').replace('\r','')
        pass
        
        self.G_PLATFORM=self.argsmap['platform']
        self.G_PATH_USER_INPUT=self.argsmap['inputDataPath']
        self.G_PATH_COST=self.argsmap['pathCost']
        self.G_PROJECT_NAME=self.argsmap['projectSymbol']
        self.G_TEMP=self.argsmap['tempPath']
        
        userInput=self.G_PATH_USER_INPUT+self.G_USERID_PARENT+"\\"+self.G_USERID
        self.RENDERBUS_PATH=RenderbusPath(userInput)
    
    def netPath(self):
        cleanMountFrom='try3 net use * /del /y'
        self.RBcmd(cleanMountFrom)
        
        pluginPath=self.argsmap['pluginPath']
        cmd='try3 net use B: '+pluginPath.replace('/','\\').replace("10.60.100.151","10.60.100.152")
        self.G_PROCESS_LOG.info(cmd)
        self.RBcmd(cmd)  
        
    def substPath(self):
        self.G_PROCESS_LOG.info('[Max.substPath start]')
        batStr='net use * /del /y \r\n'
        pluginPath=self.argsmap['pluginPath']
        batStr=batStr+'net use B: '+pluginPath.replace('/','\\').replace("10.60.100.151","10.60.100.152")+' \r\n'
        substDriver='efghijklmnopqrstuvwxyz'
        for dd in substDriver:
            batStr=batStr+'subst '+dd+': /d\r\n'
        for fileName in os.listdir(self.G_HELPER_TASK_MAX):
            self.G_PROCESS_LOG.info(fileName)
            if os.path.isfile(os.path.join(self.G_HELPER_TASK_MAX,fileName)):
                continue
            dirName=fileName.lower()
            dirPath=os.path.join(self.G_HELPER_TASK_MAX,fileName).lower()
            print dirName        
            if dirName=='net':
                continue
            if dirName=='default':
                continue
            
            if dirName=='b' or dirName=='c' or dirName=='d':
                continue
            
            #e,f,g...
            if len(dirName)==1:
                substCmd='subst '+dirName+': '+dirPath
                self.RBlog(substCmd)
                self.G_PROCESS_LOG.info(substCmd)
                os.system(substCmd)
                batStr=batStr+substCmd+'\r\n'
        batFile=os.path.join(self.G_HELPER_TASK_CFG,('substDriver.bat')).replace('\\','/')
        self.writeBat(batFile,batStr)
        self.G_PROCESS_LOG.info('[Max.substPath end]')
            
    def writeBat(self,batFile,cmdStr):
        #subst
        #batFile=os.path.join(self.G_RENDER_WORK_TASK_CFG,('render'+renderFrame+'_notrender.bat')).replace('\\','/')
        batFileObject=codecs.open(batFile,'w',"utf-8")
        batFileObject.write(cmdStr+'\r\n')
        batFileObject.close()
        
    def RBexecute(self):#total    
        self.RBBackupPy()
        self.RBinitLog()
        self.G_PROCESS_LOG.info('[BASE.RBexecute.start.....]')        
        self.RBprePy()
        self.RBmakeDir()
        self.RBcopyTempFile()
        self.readPyCfg()
        self.readRenderCfg()
        self.netPath()        
        self.CheckDisk()
        # self.RBreadCfg()
        
        #self.RBhanFile()
        
        self.RBrenderConfig()
        
        self.getOutFileName()
        self.RBrender()
        # self.RBconvertSmallPic()
        self.RBresultAction()
        self.RBpostPy()
        self.G_PROCESS_LOG.info('[BASE.RBexecute.end.....]')
