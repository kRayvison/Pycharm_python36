import os,sys,subprocess,string,logging,time,shutil
import logging
from AnalysisBase import AnalysisBase
# import nuke
# import RVNUKE
class Nuke(AnalysisBase):
    def __init__(self,**paramDict):
        AnalysisBase.__init__(self,**paramDict)
        print "Nuke.INIT"
        self.G_ANALYSEBAT_NAME='Enalyze.py'
        self.G_DRIVERC_7Z='c:/7-Zip/7z.exe'
        self.CGV=''
        self.G_NODE_PY = paramDict['G_NODE_PY']
        self.G_CG_NAME = paramDict['G_CG_NAME']
        
        print 'self.G_CONFIG-----',self.G_CONFIG
        if os.path.exists(self.G_CONFIG):
            self.RENDER_JSON=eval(open(self.G_CONFIG, "r").read())
            self.CGFILE=self.RENDER_JSON['common']["cgFile"]
            self.CGSOFT=self.RENDER_JSON['common']["cgSoftName"]
            self.CGV=self.RENDER_JSON['common']["cgv"]
            self.USERID=self.RENDER_JSON['common']["userId"]
            self.RTASKID=self.RENDER_JSON['common']["taskId"]
            self.ANALYSETXT=self.RENDER_JSON['common']["analyseTxt"]
            print self.RENDER_JSON
        else:
            sys.exit(-1)
        
    def RBhanFile(self):#3 copy script,copy from pool,#unpack
        self.G_ANALYSE_LOG.info('[Nuke.RBhanFile.start.....]')

        self.G_ANALYSE_LOG.info('[Nuke.RBhanFile.end.....]')
        
    def RBconfig(self):#5
        self.G_ANALYSE_LOG.info('[Nuke.RBconfig.start.....]')
        self.G_ANALYSE_LOG.info('[Nuke.RBconfig.end.....]')
    
    def RBanalyse(self):#7
        self.G_ANALYSE_LOG.info('[Nuke.RBanalyse.start.....]')
        #TODO


        '''
        analyze script
        
        '''

        import sys,os,subprocess,string,re

        _PATH_ORG = os.environ.get('PATH')
        os.environ['PATH'] = (_PATH_ORG if _PATH_ORG else "") + r";C:\Windows\system32"
        netFile = os.path.join(self.G_WORK_TASK,(self.G_CG_TXTNAME+'_net.txt'))
        # PARMS ORDER
        _CID = self.G_USERID
        _TID = self.RTASKID
        _NK = self.CGFILE
        _NK = _NK.replace("\\", "/")
        _INF = netFile
        _INF = _INF.replace("\\", "/")
        _CGV = self.CGV

        print "_CID: %s" % _CID
        print "_TID: %s" % _TID
        print "_NK: %s" % _NK
        print "_INF: %s" % _INF

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
        
        print _NUKE_LIB_NETWORK_PATH
        
        sys.path.append(_NUKE_LIB_NETWORK_PATH)
        print sys.path
   
        
        import RVLIB
        _CID_ROOT = RVLIB._RV_retrieveUniqueUserRoot(_CID, _NK)
        if _CID_ROOT is None:
            _CID_ROOT = os.path.dirname(_NK)
        print "\nASSETS SEARCHING PATH: %s" % _CID_ROOT

        #_NK EXIST CHECK
        if os.path.isfile(_NK):
            
            RVLIB._RV_changeNUKEVersion(_NK,_CGV)

            _NK_BASENAME = os.path.splitext(os.path.basename(_NK))[0]

            _NUKE_BEST_VERSION_STR = RVLIB._RV_getBestFitNUKEVersionFromNK(_SERVER_IP_ROOT, _NK)
            print("GET _NUKE_BEST_VERSION_STR: " + _NUKE_BEST_VERSION_STR)

            print _CGV
            
            
            
            # _NUKE_RUN_PATH = RVLIB._RV_App_Nuke_Setup(_CID,_CGV)
            # print "_NUKE_RUN_PATH=" + _NUKE_RUN_PATH

            
            

            # 03 TOOLS 7z SETUP
            _TOOL_7Z_RUN_PATH = RVLIB._RV_Tool_7z_Setup(_SERVER_Plugins)
            #print "_TOOL_7Z_RUN_PATH=" + _TOOL_7Z_RUN_PATH
            
            


            _NUKE_RUN_PATH = RVLIB._RV_App_Nuke_new_Setup(_SERVER_Plugins,True,True)
            print "_NUKE_RUN_PATH=" + _NUKE_RUN_PATH
            
        
             
            
            

            # 06 ENV SETUP
            RVLIB._RV_App_Nuke_Env_Setup(_NUKE_RUN_PATH, _PYTHON_V_WITH_DOT, _PYTHON_V_NO_DOT)

            # 07 LOAD NUKE AND RVNUKE MODULES
            import nuke
            import RVNUKE
            RVNUKE.addenvpath(_CGV)
            RVNUKE._RV_loadNKFile(_NK)

            RVNUKE._RV_write_Frame_Info(_INF, _NK_BASENAME)



        else:
            print "\nFATAL ERROR: THE SPECIFIED NK FILE NOT FOUND."



        self.G_ANALYSE_LOG.info('[Nuke.RBanalyse.end.....]')

        
        

    def webNetPath(self):
        if os.path.exists(self.G_CONFIG):
        
            self.CGFILE=self.RENDER_JSON['common']["cgFile"]
            self.CGSOFT=self.RENDER_JSON['common']["cgSoftName"]
            self.CGV=self.RENDER_JSON['common']["cgv"]
            self.RTASKID=self.RENDER_JSON['common']["taskId"]
            
            if isinstance(self.RENDER_JSON["mntMap"],dict):
                self.RBcmd("net use * /del /y")
                for key in self.RENDER_JSON["mntMap"]:
                    # self.RBcmd("net use "+key+" "+self.RENDER_JSON["mntMap"][key].replace('/','\\'))
                    self.RBcmd("net use "+key+" \""+self.RENDER_JSON["mntMap"][key].replace('/','\\')+"\"")

    def webMntPath(self):
        # mountFrom='{"Z:":"//192.168.0.94/d"}'
        mtabCmd='rm -f /etc/mtab~*'
        self.RBcmd(mtabCmd,False,1)
        exitcode = subprocess.call("mount | grep -v '/mnt_rayvision' | awk '/cifs/ {print $3} ' | xargs umount", shell=1)
        if exitcode not in(0,123):
            sys.exit(exitcode)

        self.G_ANALYSE_LOG.info('[config....]'+self.G_CONFIG)
        if os.path.exists(self.G_CONFIG):
            self.CGFILE=self.RENDER_JSON['common']["cgFile"]

            if isinstance(self.RENDER_JSON["mntMap"],dict):
                for key in self.RENDER_JSON["mntMap"]:
                    if not os.path.exists(key):
                        os.makedirs(key)
                    cmd=cmd='mount -t cifs -o username=enfuzion,password=ruiyun2016,codepage=936,iocharset=gb2312 '+self.RENDER_JSON["mntMap"][key].replace('\\','/')+' '+key
                    self.G_ANALYSE_LOG.info(cmd)
                    self.RBcmd(cmd)

                    
        
    def RBexecute(self):#Render
        self.G_ANALYSE_LOG.info('[Houdini.RBexecute.start.....]')
        self.RBBackupPy()
        self.RBinitLog()
        self.RBmakeDir()
        if self.G_RENDEROS=='Linux':
            self.webMntPath()
        else:
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
        self.G_ANALYSE_LOG.info('[Houdini.RBexecute.end.....]')