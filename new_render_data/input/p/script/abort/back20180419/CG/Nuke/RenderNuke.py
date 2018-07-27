import logging
import os
import sys
import subprocess
import string
import logging
import time as time
import shutil



import re

from RenderBase import RenderBase







class Nuke(RenderBase):
    def __init__(self,**paramDict):
        RenderBase.__init__(self,**paramDict)
        print "Nuke INIT"
        self.G_RENDERBAT_NAME='Erender_HD.bat'
        self.G_DRIVERC_7Z='c:/7-Zip/7z.exe'
        self.CGV="";
        self.CGFILE="";
        self.nukeScript='c:/script/nuke'
        self.G_CG_NAME = paramDict['G_CG_NAME']
        self.G_NODE_PY = paramDict['G_NODE_PY']
        
        if os.path.exists(self.G_CONFIG):
            self.RENDER_JSON=eval(open(self.G_CONFIG, "r").read())
            self.CGFILE=self.RENDER_JSON['common']["cgFile"]
            self.CGSOFT=self.RENDER_JSON['common']["cgSoftName"]
            self.CGV=self.RENDER_JSON['common']["cgv"]
            self.RTASKID=self.RENDER_JSON['common']["taskId"]
            self.ANALYSETXT=self.RENDER_JSON['common']["analyseTxt"]
            self.INPUTUSERPATH=self.RENDER_JSON['common']["inputUserPath"]
            self.USEROUTPUTPATH=self.RENDER_JSON['common']["userOutputPath"]
            self.SMALLPATH=self.RENDER_JSON['common']["smallPath"]
            print self.RENDER_JSON
        else:
            sys.exit(-1)



    def RBhanResult(self):#8
        feeLogFile=self.G_USERID+'-'+self.G_TASKID+'-'+self.G_JOB_NAME+'.txt'
        feeTxt=os.path.join(self.G_RENDER_WORK_TASK,feeLogFile)
        feeLogCmd='xcopy /y /f "'+feeTxt+'" "'+self.G_PATH_COST+'/" '                    
        self.RBcmd(feeLogCmd)

        self.G_PROCESS_LOG.info('[BASE.RBhanResult.end.....]')
        self.RBlog('done','end')
        

    def RBrender(self):#7

        self.G_RENDER_LOG.info('[Nuke.RBrender.start.....]')
        startTime = time.time()
        
        self.G_FEE_LOG.info('startTime='+str(int(startTime)))
        
        

        '''
        render script

        '''

        
        _PATH_ORG = os.environ.get('PATH')
        os.environ['PATH'] = (_PATH_ORG if _PATH_ORG else "") + r";C:\Windows\system32"

        # PARMS ORDER


        _CID = self.G_USERID
        _TID = self.RTASKID
        _SFM = self.G_CG_START_FRAME
        _EFM = self.G_CG_END_FRAME
        _BFM = self.G_CG_BY_FRAME
        _NK = self.CGFILE
        _NK = _NK.replace("\\", "/")
        _WRI = self.G_CG_LAYER_NAME
        _WRI = _WRI.replace("\\", "/")
        _OUT = self.USEROUTPUTPATH
        _OUT = _OUT.replace("\\", "/")
        _IN = self.INPUTUSERPATH
        _IN = _IN.replace("\\", "/")
        _CGV = self.CGV
        
        
        print "_CID: %s" % _CID
        print "_TID: %s" % _TID
        print "_SFM: %s" % _SFM
        print "_EFM: %s" % _EFM
        print "_BFM: %s" % _BFM
        print "_NK: %s" % _NK
        print "_WRI: %s" % _WRI
        print "_OUT: %s" % _OUT
        print "_IN: %s" % _IN
        

        
        
        # GENERAL ENV SETUP
        python_version = "%d.%d" % sys.version_info[:2]
        python_version_no_dot = "%d%d" % sys.version_info[:2]
        _PYTHON_V_WITH_DOT = str(python_version)
        _PYTHON_V_NO_DOT = str(python_version_no_dot)
        os.environ['PYTHONPATH'] = r"C:/Python%s" % _PYTHON_V_NO_DOT
        
        filename = sys.argv[0]
        dirname = os.path.dirname(filename)
        abspath = os.path.abspath(dirname)
        
        _SERVER_Plugins = r"B:"
        _SERVER_IP_ROOT = self.G_NODE_PY + r"/" + self.G_CG_NAME
        _NUKE_LIB_NETWORK_PATH = _SERVER_IP_ROOT + r"/lib"
        
        sys.path.append(_NUKE_LIB_NETWORK_PATH)
        
        print("---------------------------------------------------------\n")
        print("NUKE RENDER SETUP")
        
        import RVLIB
        
        _CID_ROOT = RVLIB._RV_retrieveUniqueUserRoot(_CID, _NK)
        if _CID_ROOT is None:
            _CID_ROOT = os.path.dirname(_NK)
        print "\nASSETS SEARCHING PATH: %s" % _CID_ROOT

        #_NK EXIST CHECK
        if os.path.isfile(_NK):
            # 00
            _NK_BASENAME = os.path.splitext(os.path.basename(_NK))[0]

            # 01 rd dir setup
            if not _OUT.endswith(('/')):
                _OUT += "/"
            # if not os.path.exists(_OUT):
                # os.makedirs(_OUT)

            _NUKE_BEST_VERSION_STR = RVLIB._RV_getBestFitNUKEVersionFromNK(_SERVER_IP_ROOT, _NK)

            print("GET _NUKE_BEST_VERSION_STR: " + _NUKE_BEST_VERSION_STR)

            # _NUKE_RUN_PATH = RVLIB._RV_App_Nuke_Setup(_CID,_CGV)
            # print "_NUKE_RUN_PATH=" + _NUKE_RUN_PATH

            

            # 03 TOOLS 7z SETUP
            _TOOL_7Z_RUN_PATH = RVLIB._RV_Tool_7z_Setup(_SERVER_Plugins)
            #print "_TOOL_7Z_RUN_PATH=" + _TOOL_7Z_RUN_PATH
            


            _NUKE_RUN_PATH = RVLIB._RV_App_Nuke_new_Setup(_SERVER_Plugins,True,True)
            print "_NUKE_RUN_PATH=" + _NUKE_RUN_PATH
            
        



            RVLIB._RV_App_Nuke_Env_Setup(_NUKE_RUN_PATH, _PYTHON_V_WITH_DOT, _PYTHON_V_NO_DOT)


            # 07 LOAD NUKE AND RVNUKE MODULES
            import nuke
            import RVNUKE
            import findfiles
            
            if _CID == '1855703':
                Platform_output = "\\".join(_OUT.split("/")[:7])
                
                print "User Platform Path : %s" % Platform_output
                # RBcmd('net use "B:" "\\\\10.60.100.151\\td"')
                cmd='net use O: '+Platform_output       
                RVNUKE.RBcmd(cmd)            
            

            # 08 LOAD NK FILE
            RVNUKE.addenvpath(_CGV)
            RVNUKE._RV_loadNKFile(_NK)
            

            # 09 UPDATE SOME INTERNAL ENVS
            _NK_VAR = os.path.dirname(_NK)



            obj = None
            obj = RVNUKE._RV_renderSetup(_WRI, _SFM, _EFM, _BFM, _IN, _OUT, _NK_BASENAME)
            # node = nuke.toNode("_WRI")
            # filename = nuke.filename(node)
            print '    RENDER SETUP DONE @ %s :' % _WRI




            ### print the files in this scene
            filespath=r"D:/work/render/"+ str(_TID)
            print filespath
            print "-----------------------------------------------------------------"
            print "                           FILES                                 "
            print "-----------------------------------------------------------------"

            #findfiles.DOFILES(filespath,0)
            print "-----------------------------------------------------------------"



            time_render_at=time.time()


            # 13 RENDER IT NOW
            if obj is None:
                print "\nFATAL ERROR: THE SPECIFIED WRITE NOT FOUND."

            else:
                print "\nALL SET, RENDERING ..."
                RVNUKE._RV_renderWrite(obj,_NK,int(_SFM),int(_EFM),int(_BFM),_IN,_OUT,_CGV,_NUKE_RUN_PATH)
                time_render_end=time.time()
                render_time='%.3f'% (time_render_end-time_render_at)
                print ("Rendered with %s s" % render_time)
                



        else:
            print "\nFATAL ERROR: THE SPECIFIED NK FILE NOT FOUND."


        

      
        
        

        endTime = time.time()
        self.G_FEE_LOG.info('endTime='+str(int(endTime)))
        self.G_RENDER_LOG.info('[Nuke.RBrender.end.....]')
    
    def webNetPath(self):
        if os.path.exists(self.G_CONFIG):
            print self.G_CONFIG
            configJson=eval(open(self.G_CONFIG, "r").read())
            self.CGFILE=configJson['common']["cgFile"]
            self.CGSOFT=configJson['common']["cgSoftName"]
            self.CGV=configJson['common']["cgv"]
            self.RTASKID=configJson['common']["taskId"]
            print configJson
            if isinstance(configJson["mntMap"],dict):
                self.RBcmd("net use * /del /y")
                for key in configJson["mntMap"]:
                    # self.RBcmd("net use "+key+" "+configJson["mntMap"][key].replace('/','\\'))
                    self.RBcmd("net use "+key+" \""+configJson["mntMap"][key].replace('/','\\')+"\"")

    def webMntPath(self):
        # mountFrom='{"Z:":"//192.168.0.94/d"}'
        mtabCmd='rm -f /etc/mtab~*'
        self.RBcmd(mtabCmd,False,1)
        exitcode = subprocess.call("mount | grep -v '/mnt_rayvision' | awk '/cifs/ {print $3} ' | xargs umount", shell=1)
        if exitcode not in(0,123):
            sys.exit(exitcode)
        #self.RBcmd(umountcmd)

        self.G_RENDER_LOG.info('[config....]'+self.G_CONFIG)
        self.G_CONFIG = self.G_CONFIG.replace("\\","/")
        if os.path.exists(self.G_CONFIG):
            configJson=eval(open(self.G_CONFIG, "r").read())
            self.CGFILE=configJson['common']["cgFile"]
            print configJson
            if isinstance(configJson["mntMap"],dict):
                for key in configJson["mntMap"]:
                    if not os.path.exists(key):
                        os.makedirs(key)
                    cmd='mount -t cifs -o username=enfuzion,password=ruiyun2016,codepage=936,iocharset=gb2312 '+configJson["mntMap"][key].replace('\\','/')+' '+key
                    self.G_RENDER_LOG.info(cmd)
                    self.RBcmd(cmd,False,1)


    def RBexecute(self):#Render
        
        print 'Nuke.execute.....'
        self.RBBackupPy()
        self.RBinitLog()
        self.G_RENDER_LOG.info('[Nuke.RBexecute.start.....]')
        self.RBprePy()
        self.RBmakeDir()
        self.RBcopyTempFile()
        self.RBreadCfg()
        self.RBhanFile()
        if self.G_RENDEROS=='Linux':
            self.webMntPath()
        else:
            self.delSubst()
            self.webNetPath()
        #self.copyHoudiniFile()
        self.RBrenderConfig()
        self.RBwriteConsumeTxt()
        self.RBrender()
        if self.G_RENDEROS=='Linux':
            print 'no smallpic'
        else:
            self.RBconvertSmallPic()
        self.RBhanResult()
        self.RBpostPy()
        self.G_RENDER_LOG.info('[Nuke.RBexecute.start.....]')