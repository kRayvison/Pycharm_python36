#!/usr/bin/env python
# -*- coding:utf-8 -*-
import logging
import os
import os.path
import sys
import subprocess
import string
import logging
import time
import shutil
from RenderBase import RenderBase
from C4DPluginManager import C4DPlugin, C4DPluginManagerCenter


class C4D(RenderBase):
    def __init__(self, **paramDict):
        RenderBase.__init__(self, **paramDict)
        print "C4d INIT"
        print "c4d argv" + sys.argv[5]
        self.G_RENDER_LOG.info('[c4d argv]' + sys.argv[5])
        # self.G_IMAGE_WIDTH=""
        # self.G_IMAGE_HEIGHT=""
        self.G_JOB_NAME = ""
        self.G_IFORMAT = ""
        self.multiPass = ""
        self.cgfile = ""
        self.outputFileName = ""
        self.projectPath = ""
        self.cgv = ""

    def checkFile(self):
        fileList = self.G_FILELIST.split(",")
        sample_list = []
        for parent, dirnames, filenames in os.walk(self.projectPath):  # 三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
            for filename in filenames:  # 输出文件信息
                sample_list.append(filename)
        existCount = 0
        notExistCount = 0
        for files in fileList:
            isExist = False
            files = files.strip()
            for name in sample_list:
                if files == name:
                    isExist = True
            if isExist:
                self.G_RENDER_LOG.info(files + '----exists---')
                existCount = existCount + 1
            else:
                self.G_RENDER_LOG.info(files + '----not exists---')
                notExistCount = notExistCount + 1
        self.G_RENDER_LOG.info(
            files + '----notExistsCount---' + str(notExistCount) + '----exists----' + str(existCount))
        if notExistCount > 0:
            sys.exit(-1)

    def webNetPath(self):
        if os.path.exists(self.G_CONFIG):
            configJson = eval(open(self.G_CONFIG, "r").read())
            print configJson
            # self.G_IMAGE_WIDTH=configJson['common']["imageWidth"]
            # self.G_IMAGE_HEIGHT=configJson['common']["imageHeight"]
            self.G_IFORMAT = configJson['common']["iformat"]
            self.multiPass = configJson['common']["multiPass"]
            self.cgfile = configJson['common']["cgFile"]
            self.outputFileName = configJson['common']["outputFileName"]
            self.projectPath = configJson['renderSettings']["projectPath"]
            self.cgv = configJson['common']["cgv"]

            if isinstance(configJson["mntMap"], dict):
                self.RBcmd("net use * /del /y",myLog=True)
                for key in configJson["mntMap"]:
                    # self.RBTry3cmd("net use " + key + " " + configJson["mntMap"][key].replace('/','\\'))
                    self.RBTry3cmd("net use " + key + " \"" + configJson["mntMap"][key].replace('/','\\')+"\"")

    def setPluginByPyFile(self):
        self.G_PROCESS_LOG.info('[...Plugin config begin...]')
        if os.path.exists(self.G_PLUGINS):
            configJson = eval(open(self.G_PLUGINS, "r").read())
            self.G_PROCESS_LOG.info(configJson)
            if isinstance(configJson["plugins"], dict):
                node = self.getNode()
                myCgVersion = configJson["renderSoftware"] + " " + configJson["softwareVer"]
                plugin_mgr = C4DPluginManagerCenter(self.G_USERID)
                plugin_mgr.copy_R18_exe(myCgVersion)
                self.G_PROCESS_LOG.info('copy_R18_exe was done!!!')
                
                #plugin_list = ()
                for key in configJson["plugins"]:
                    plugin = C4DPlugin()
                    plugin.plugin_name = key
                    plugin.plugin_version = configJson["plugins"][key]
                    plugin.soft_version = configJson["renderSoftware"] + ' ' + configJson["softwareVer"]
                    plugin.node = node
                    
                    self.G_PROCESS_LOG.info('[ python = "B:\\plugins\\C4D\\script\\C4DPluginManager.py" "%s" "%s" "%s" "%s" ]' % (plugin.plugin_name, \
                                                                                plugin.plugin_version, \
                                                                                plugin.soft_version, \
                                                                                plugin.node))
                    #plugin_list.append(plugin)  
                    plugin_mgr.get_dll(plugin.soft_version)
                    self.G_PROCESS_LOG.info('libmmd.dll copy done!!!')
                    
                    result = plugin_mgr.set_custom_env(plugin)

                #result = plugin_mgr.set_custom_envs(plugin_list)     
        
        self.G_PROCESS_LOG.info('[...Plugin config end...]')            

    def getNode(self):
        node=sys.argv[5]
        if "A" in node or "B" in node or "C" in node or "D" in node or "E" in node or "F" in node:
            return "ABCDEF"
        if "K" in node:
            return "K"
        if "L" in node or "M" in node or "N" in node or "O" in node or "P" in node or "Q" in node:
            return "LNOPQ"
        if "G" in node or "H" in node or "J" in node:
            return "GHJ"
        return "ABCDEF"

    def __init__(self,**paramDict):
        RenderBase.__init__(self,**paramDict)
        if paramDict.has_key('G_JOB_ID'):
            self.G_JOB_NAME=paramDict['G_JOB_ID']
            
        if paramDict.has_key('G_SCHEDULER_CLUSTER_NODES'):
            self.G_SCHEDULER_CLUSTER_NODES = paramDict['G_SCHEDULER_CLUSTER_NODES']
   
        self.G_MUNU_ID=self.G_SYS_ARGVS[1]
        self.G_JOB_ID=self.G_SYS_ARGVS[2]
        
        print '--------------jobid-------------'
        print type(self.G_JOB_NAME)
        self.G_JOB_NAME_STR=self.G_JOB_NAME
        self.G_JOB_NAME=self.G_JOB_NAME.encode(sys.getfilesystemencoding())
        print type(self.G_JOB_NAME)

    def RBrender(self):  # 7
        self.G_RENDER_LOG.info('[C4D.RBrender.start.....]')
        startTime = time.time()

        self.G_FEE_LOG.info('startTime=' + str(int(startTime)))

        if self.outputFileName == "":
            self.outputFileName = os.path.basename(self.cgfile)

        myCgVersion = "CINEMA 4D " + self.cgv
        # if myCgVersion.endswith('.64') :
        #     myCgVersion=myCgVersion.replace('.64','')
        # if myCgVersion.endswith('.32') :
        #     myCgVersion=myCgVersion.replace('.32','')

        self.G_JOB_NAME=self.G_JOB_NAME.encode(sys.getfilesystemencoding())

        outputFile = self.G_RENDER_WORK_OUTPUT.replace("/", "\\") + "\\" + self.outputFileName

        frame_number = self.G_CG_START_FRAME
        # outputrenderlogFile =  '"' + self.G_RENDER_WORK_OUTPUT.replace("/", "\\").replace("work", "log").replace("\output", "") + "\\" + self.G_JOB_NAME + '_render.log"'
        outputrenderlogFile = os.path.join(self.G_LOG_WORK,self.G_TASKID,(self.G_JOB_NAME+'_render.log')).replace("/", "\\")
        
        c4dExePath = os.path.join(r'C:\Program Files\MAXON', myCgVersion, 'CINEMA 4D 64 Bit.exe')

        # C:\Program Files\MAXON\CINEMA 4D R15\CINEMA 4D 64 Bit.exe -noopengl -nogui -frame 1 1 -render \\10.50.1.4\dd\inputData\c4d\162686\Warehouse\pipi\pipi.c4d -oresolution 1920 1080 -oformat TGA -oimage C:\enfwork\213282\output\warehouse_4
        renderCmd = '"' + c4dExePath + '" -noopengl -nogui  -frame ' + self.G_CG_START_FRAME + ' ' + self.G_CG_END_FRAME + ' -render "' + self.cgfile.replace(
            "/",
            "\\") + '" -oresolution ' + self.G_IMAGE_WIDTH + ' ' + self.G_IMAGE_HEIGHT + ' -oformat ' + self.G_IFORMAT + ' -oimage "' + outputFile + '"'
        if self.multiPass == "":
            renderCmd = renderCmd + ' >>' + outputrenderlogFile
        if self.multiPass == "1":
            renderCmd = renderCmd + ' -omultipass "' + outputFile + '"' + ' >>' + outputrenderlogFile

        self.G_PROCESS_LOG.info("Cmds: %s"%renderCmd)
        if self.G_RENDEROS=='Linux':
            self.RBcmd(renderCmd,True,1,myLog=True)
        else:
            ## ------------------------------------------------------------------------------------
            #os.system(renderCmd)
            TL_result = subprocess.Popen(renderCmd,stdin = subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
            TL_result.stdin.write('3/n')
            TL_result.stdin.write('4/n')
            r_err = ''
            while TL_result.poll()==None:
                r_info = TL_result.stdout.readline().strip()
                if not r_info == "":
                    self.G_PROCESS_LOG.info(r_info)
                    r_err = r_info
            #r_result = TL_result.wait()
            r_code = TL_result.returncode
            #r_err = TL_result.stderr.read()
            self.G_PROCESS_LOG.info("RenderCmd return:"+str(r_code))
            if r_code:
                self.G_PROCESS_LOG.info("Error Print :")
                self.G_PROCESS_LOG.info("\n"+r_err+"\n")
        # os.system(renderCmd)
        #self.RBcmd(renderCmd, True, False)
        endTime = time.time()
        self.G_FEE_LOG.info('endTime=' + str(int(endTime)))
        self.G_RENDER_LOG.info('[C4D.RBrender.end.....]')

    def RBexecute(self):  # Render

        print 'C4d.execute.....'
        self.RBBackupPy()
        self.RBinitLog()
        self.G_RENDER_LOG.info('[C4D.RBexecute.start.....]')

        self.RBprePy()
        self.RBmakeDir()
        self.RBcopyTempFile()
        self.delSubst()
        self.webNetPath()
        self.RBreadCfg()
        self.RBhanFile()
        self.RBrenderConfig()
        self.RBwriteConsumeTxt()
        self.copyBlack()
    
        # self.plugin()
        self.setPluginByPyFile()
        self.RBrender()
        self.RBconvertSmallPic()
        self.RBhanResult()
        self.RBpostPy()
        self.G_RENDER_LOG.info('[C4D.RBexecute.end.....]')