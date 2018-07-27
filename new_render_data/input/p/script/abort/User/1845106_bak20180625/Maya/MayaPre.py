#!/usr/bin/env python
#encoding:utf-8
# -*- coding: utf-8 -*-
import logging
import os
import os.path
import sys
import subprocess
import _subprocess
import string
import logging
import time
import shutil
import codecs
import ConfigParser
from RenderBase import RenderBase
class MayaPre(RenderBase):
    def __init__(self,**paramDict):
        RenderBase.__init__(self,**paramDict)

    def readRenderCfg(self):
        self.G_PROCESS_LOG.info('[Max.readRenderCfg.start.....]'+self.G_RENDER_WORK_TASK_CFG)
        renderCfg=os.path.join(self.G_RENDER_WORK_TASK_CFG,'render.cfg').replace('/','\\')
        self.RENDER_CFG_PARSER = ConfigParser.ConfigParser()
        
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
        
        self.G_PROCESS_LOG.info('[maya.readRenderCfg.end.....]')

    def getPackFile(self):
        if self.RENDER_CFG_PARSER.has_option('common','cgFile'):
            self.packFile=self.RENDER_CFG_PARSER.get('common','render_file').replace("/","\\")
            self.cgFileName=os.path.basename(self.RENDER_CFG_PARSER.get('common','cgFile'))
            self.cgFilePath=os.path.dirname(self.packFile)
            self.cgFile=os.path.join(self.cgFilePath,self.cgFileName)
            self.G_PROCESS_LOG.info('[maya.readRenderCfg.end.....]')

    def mountFrom(self):
        mountFrom=self.RENDER_CFG_PARSER.get('common','mountFrom')
        s=eval(mountFrom)
        projectPath = self.G_PATH_INPUTPROJECT[0:self.G_PATH_INPUTPROJECT.index(self.G_USERID_PARENT)-1]
        for key in s.keys():
            if not os.path.exists(s[key]):
                cmd='try3 net use '+s[key]+' '+projectPath.replace('/','\\')+key.replace('/','\\')
                self.G_PROCESS_LOG.info(cmd)
                self.RBcmd(cmd)

    def RBrender(self):#7
        self.G_PROCESS_LOG.info('[MayaPre.RBrender.start.....]')
        filePath = ""
        result = 0
        self.exe = "C:\\7-Zip\\7z.exe"
        if os.path.exists(self.cgFile):
            result = self.is_same(self.packFile,self.cgFile)
        if result==0:
            unpackCmd=self.exe +' e "'+self.packFile+'" -o"'+self.cgFilePath+'" -y'    

            self.RBcmd(unpackCmd,False,False)
        else:
            self.G_PROCESS_LOG.info('[fileExist.....]')

        self.G_PROCESS_LOG.info('[MayaPre.RBrender.end.....]')

    def run_command(self,cmd):
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= _subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = _subprocess.SW_HIDE

        p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, startupinfo=startupinfo)

        while 1:
            #returns None while subprocess is running
            return_code = p.poll()
            if return_code == 0:
                break
            # elif return_code == 1:
            #     raise Exception(cmd + " was terminated for some reason.")
            elif return_code != None:
                print "exit return code is: " + str(return_code)
                break
                # raise Exception(cmd + " was crashed for some reason.")
            line = p.stdout.readline()
            yield line

    def get_zip_info(self, zip_file):
        {'Attributes': 'A',
        'Block': '0',
        'Blocks': '1',
        'CRC': '836CB95D',
        'Encrypted': '-',
        'Headers Size': '138',
        'Method': 'LZMA2:20',
        'Modified': '2015-03-28 15:59:26',
        'Packed Size': '29191866',
        'Path': 'M02_P04_S046.mb',
        'Physical Size': '29192004',
        'Size': '138382876',
        'Solid': '-',
        'Type': '7z'}

        cmd = "\"%s\" l -slt \"%s\"" % (self.exe, zip_file)
        print cmd
        result = {}
        for line in self.run_command(cmd):
            if "=" in line:
                line_split = [i.strip() for i in line.strip().split("=")]
                result[line_split[0]] = line_split[1]

        return result

    def is_same(self, zip_file, src):
        if os.path.exists(zip_file) and os.path.exists(src):
            zip_info = self.get_zip_info(zip_file)

            z_time = zip_info["Modified"]
            z_size = zip_info["Size"]

            f_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(os.path.getmtime(src)))
            f_size = str(os.path.getsize(src))

            if z_time == f_time and z_size == f_size:
                return 1
        
    def RBexecute(self):#Render
        #self.RBBackupPy()
        self.RBinitLog()
        self.G_RENDER_LOG.info('[MayaPre.RBexecute.start.....]')
        
        self.RBprePy()
        self.RBcopyTempFile()

        self.RBreadCfg()
        #self.RBhanFile()
        self.RBrenderConfig()
        self.readRenderCfg()
        self.delNetUse()
        self.mountFrom()
        self.getPackFile()
        self.RBrender()

        #self.RBresultAction()
        #self.RBpostPy()
        self.G_RENDER_LOG.info('[MayaPre.RBexecute.end.....]')