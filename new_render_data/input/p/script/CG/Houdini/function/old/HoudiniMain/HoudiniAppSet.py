import sys,os,subprocess,string,re
from threading import Timer
import time,socket,json
from os import path 

base_dir = path.dirname(path.abspath(sys.path[0]))
print(base_dir)
sys.path.append(base_dir)

class HfsSetup():
    def __init__(self,hver='',plants='',adict={}):
        self._run_code = True
        self._plants = plants
        self._hfs_version = hver
        self._servers = ['10.60.96.203']
        self._server = self._servers[0]
        self._Kapps = ["houdinifx.exe","hython.exe"]
        self._folders = ["temp"]
        self.Makerdir()
        self._temp = "%s/temp"%base_dir
        self._code_base_path = adict['codebase'] # C:/script/CG/Houdini
        self._B_plugin_path = adict['plugingase']  # B:/plugins/houdini
        self._D_houdini_path = adict['hfsbase']  # D:/plugins/houdini

        self._info_return = []



    def getcustip(self):
        self._hostname = socket.gethostname()
        ## print(self._hostname)
        _ip_end = re.findall(r"\d+",self._hostname)
        _ip_a = _ip_end[0]
        z_num = 0
        for i in range(0,len(_ip_a)):
            if not _ip_a[i]=="0":
                z_num=i
                break
        _ip_a =_ip_a[z_num:]
        _ipList = socket.gethostbyname_ex(self._hostname)
        self._this_ip = ''
        for elm in _ipList[-1]:
            _ip_ss = elm.split(".")
            if _ip_a in _ip_ss:
                self._this_ip = elm
                break

    def Makerdir(self):
        for elm in self._folders:
            _elm = "%s/%s"%(base_dir,elm)
            if not os.path.exists(_elm):
                os.makedirs(_elm)

    def ConfigApp_win(self):
        self._CopyHfs = True
        self._info_return.append("Server tyr to chang to: %s"%self._server)
        ## copy files
        # 7z tools
        localpath = r"D:/plugins/tools/7z"
        z7 = "D:/plugins/tools/7z/7z.exe"
        fromdir = self._B_plugin_path.replace("/plugins/houdini","") + r"/tools/7-Zip"
        h_source = os.path.abspath("%s/apps/win/%s.7z"%(self._B_plugin_path,self._hfs_version))
        h_amd = os.path.abspath("%s/%s.7z"%(self._D_houdini_path,self._hfs_version))
        if os.path.exists(h_amd):
            self._CopyHfs = False
        
        ## set hfs server
        version_base = self._hfs_version[:2]
        py_path = os.path.abspath("%s/function/HoudiniLibs/hfsserver.py %s"%(self._code_base_path,base_dir))
        _lic_info = {"hver":version_base,"server":self._server}
        _lic_info_f = "%s/temp/lic_info.json"%base_dir
        with open(_lic_info_f,"w")as f:
            json.dump(_lic_info,f)
            f.close()
        server_cmds = py_path

        ## unzip houdini 
        cmd_un7z = z7 + " x -y -aos "
        cmd_un7z += "%s/%s.7z"%(self._D_houdini_path,self._hfs_version) # D:/plugins/houdini
        cmd_un7z += " -o%s" % ("%s/%s"%(self._D_houdini_path,self._hfs_version))
        
        
        ## subprocess
        # creat the handl 
        setserver_log = open(r'%s/Server_info.txt'%self._temp,'wt')
        copy7ztool_log = open(r'%s/Copy_ziptool.txt'%self._temp,'wt')
        Uzi_Houdini_log = open(r'%s/Uzip_Houdini.txt'%self._temp,'wt')

        set_server = subprocess.Popen(server_cmds,stdout=setserver_log,shell=True)
        copy7ztool = subprocess.Popen("robocopy /S /NDL /NFL %s %s %s" % (fromdir, localpath, "*"),stdout=copy7ztool_log,shell=True)
        if self._CopyHfs:
            copyhoudini = subprocess.Popen("copy %s %s" % (h_source, h_amd),shell=True)
            copyhoudini.wait()
        copy7ztool.wait()

        UzipHoudini = subprocess.Popen(cmd_un7z,stdout=Uzi_Houdini_log,shell=True)
        _s_result = set_server.wait()
        if not _s_result:
            # print("License server changed to: %s"%self._server)
            self._info_return.append("License server changed to: %s"%self._server)
        UzipHoudini.wait()

        # finish,close the handl
        setserver_log.close()
        copy7ztool_log.close()
        Uzi_Houdini_log.close()
        _h_result = UzipHoudini.returncode

        ## os.remove(h_amd)
        if not _h_result:
            print("Houdini setup finished. ")


    def KillApps(self):
        for app in self._Kapps:
            if self._plants == "win":
                cmds = r'c:\windows\system32\cmd.exe /c c:\windows\system32\TASKKILL.exe /F /IM %s'%app
            elif self._plants == "Linux":
                cmds = ''
            subprocess.call(cmds,shell=True)

    def Extued(self):
        # print("Try to kill the houdinifx and hython before houdini app setup")
        self._info_return.append("Try to kill the houdinifx and hython before houdini app setup")
        try:
            self.KillApps()
        except:
            pass
        if self._run_code and self._plants=="win":
            self.ConfigApp_win()
        elif self._run_code and self._plants=="Linux":
            self.ConfigApp_Linux()

def main(version='',plants='win',adict={}):

    s_time = time.time()
    app = HfsSetup(version,plants,adict)
    app.Extued()
    n_time = time.time()
    print("Times for apps setup: %d s"%(n_time-s_time))
    app._info_return.append("Times for apps setup: %d s"%(n_time-s_time))

    return app._info_return

if __name__ == '__main__':
    main('160557','win')

'''
    _info_file = "%s/temp/app_info.json"%base_dir
    _plugin_info = {}
    if os.path.exists(_info_file):
        with open(_info_file,"r")as f:
            _plugin_info = json.load(f)
            f.close()
'''