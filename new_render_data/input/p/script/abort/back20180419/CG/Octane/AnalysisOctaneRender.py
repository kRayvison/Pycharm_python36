import os,sys,subprocess,string,logging,time,shutil
import logging
import codecs
from AnalysisBase import AnalysisBase

class OctaneRender(AnalysisBase):
    def __init__(self,**paramDict):
        AnalysisBase.__init__(self,**paramDict)

    def RBanalyse(self):
        self.G_ANALYSE_LOG.info('[OctaneRender.RBanalyse.start.....]'+self.G_RENDERTYPE)

        netPath = os.path.join(self.G_WORK_TASK,(self.G_CG_TXTNAME))
        if not os.path.exists(netPath):
            os.makedirs(netPath)
        netFile=netPath.replace('\\','/')+'_net.txt'
        open(netFile,"w+").close()
        renderbat = r'B:\plugins\octane_Standalone\script\octane_Standalone.bat';

        analyseCmd=renderbat + ' "' +self.CGSOFT+' '+self.CGV+'" "'+self.G_TASKID+'" "'+self.getRealFile()+'" "'+netFile+'"'
        self.RBcmd(analyseCmd,True,False)

    def webNetPath(self):
        if os.path.exists(self.G_CONFIG):
            configJson=eval(open(self.G_CONFIG, "r").read())
            self.CGFILE=configJson['common']["cgFile"]
            self.CGSOFT=configJson['common']["cgSoftName"]
            self.CGV=configJson['common']["cgv"]
            self.RTASKID=configJson['common']["taskId"]

            if isinstance(configJson["mntMap"],dict):
                if not self.G_RENDERTYPE=="gpu":
                    self.RBcmd("net use * /del /y")
                for key in configJson["mntMap"]:
                    try:
                        # self.RBcmd("net use "+key+" "+configJson["mntMap"][key].replace('/','\\'))
                        self.RBcmd("net use "+key+" \""+configJson["mntMap"][key].replace('/','\\')+"\"")
                    except:
                        self.G_ANALYSE_LOG.info('cannot mapping disk'+key+' is in used'+configJson["mntMap"][key])
                        pass
                    
    def getRealFile(self):
        if "#" in self.CGFILE:
            fileArray = self.CGFILE[self.CGFILE.rfind("ocs"):].split(" ");
            frames = fileArray[1]
            restr = self.CGFILE[self.CGFILE.find("#"):self.CGFILE.rfind("#")+1]
            index = len(restr)
            return self.CGFILE[:self.CGFILE.rfind("ocs")+3].replace(restr, frames[0:1].zfill(index))
        else:
            return self.CGFILE

    def gpuDelNet(self):
        userFilePath = "D:\\work\\user\\userId.txt"
        userId=self.G_USERID
        isSame=False
        if os.path.exists(userFilePath):
            rbModel = codecs.open(userFilePath,"r","utf-8")
            lines = rbModel.readlines()
            for line in lines:
                if userId in line:
                    isSame = True
            rbModel.close()
        if not isSame:
            folder = "D:\\work\\user\\";
            if not os.path.exists(folder):
                os.makedirs(folder)
            self.delNetUse()
            rb=codecs.open(userFilePath,'w') 
            try :
                rb.write(userId.encode("UTF-8"))
            finally :
                rb.close()
        
    def RBexecute(self):#Render
        self.G_ANALYSE_LOG.info('[OctaneRender.RBexecute.start.....]')
        self.RBBackupPy()
        self.RBinitLog()
        self.RBmakeDir()
        self.RBprePy()
        self.RBcopyTempFile()#copy py.cfg max file
        self.RBreadCfg()
        if not self.G_RENDERTYPE=="gpu":
            self.delSubst()
            self.webNetPath()
        else:
            self.gpuDelNet()
            self.webNetPath()
        self.RBhanFile()
        
        self.RBconfig()
        self.RBanalyse()
        self.RBpostPy()
        self.RBhanResult()
        self.G_ANALYSE_LOG.info('[OctaneRender.RBexecute.end.....]')