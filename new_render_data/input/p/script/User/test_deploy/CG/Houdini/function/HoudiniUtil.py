#!/usr/bin/env python
#encoding:utf-8
# -*- coding: utf-8 -*-
# edit 201806141615
import os,sys,time
import subprocess
import socket
import shutil
import platform
import re,json


class HoudiniUtil():

    
    @classmethod
    def SysTemInfo(cls):
        this_hostname = socket.gethostname()
        this_plant = sys.platform
        this_ip_end = re.findall(r"\d+",this_hostname)
        _ip_a = this_ip_end[0]
        z_num = 0
        for i in range(0,len(_ip_a)):
            if not _ip_a[i]=="0":
                z_num=i
                break
        _ip_a =_ip_a[z_num:]
        this_ipList = socket.gethostbyname_ex(this_hostname)
        this_ip = ''
        for elm in this_ipList[-1]:
            _ip_ss = elm.split(".")
            if _ip_a in _ip_ss:
                this_ip = elm
                break
        return this_plant,this_hostname,this_ip


    @classmethod
    def CustomSetup(cls,cls_in=''):
        cls_in.LogsCreat("CustomSetup start...")
        try:
            cls_in._CustomSetup_run_info = ['CustomSetup']
        except Exception as e:
            cls_in._run_code_result = False
            cls_in._erorr_code = 'CustomSetup'
            cls_in._erorr_code_info = e


    @classmethod
    def PluginsSetup(cls,cls_in=''):
        cls_in.LogsCreat("PluginsSetup start...")
        if len(cls_in._plugins):
            try:
                returninfo = cls.SetRenderer(cls_in._hfs_version,cls_in._plugins,cls_in._houdini_PLuing_dirt,cls_in._plugins_surpose)
                cls_in._PluginsSetup_run_info = []
                if len(returninfo):
                    for elm in returninfo:
                        if len(elm):
                            for plu in elm:
                                infos_get = [plu]
                                if "info" in elm[plu]:
                                    infos_get.append(elm[plu]["info"][-1])
                                    cls_in._PluginsSetup_run_info.extend(infos_get)
                                    if not elm[plu]["info"][0]:
                                        cls_in._run_code_result = False
                                        cls_in._erorr_code = 'HoudiniUtil.SetRenderer'
                                        cls_in._erorr_code_info = elm[plu]["info"][-1]

                                if "app" in elm[plu]:cls_in._Killapps.extend(elm[plu]["app"])
            except(Exception) as e:
                cls_in._run_code_result = False
                cls_in._erorr_code = 'HoudiniUtil.SetRenderer'
                cls_in._erorr_code_info = e
        else:
            cls_in._PluginsSetup_run_info = ["Not any plugins to set."]

    @staticmethod
    def SetRenderer(houdiniversion='',plugin_adict={},plugins_dirt='',plugins_surpose=[]):

        # if len(plugin_adict):
        _plugin_dirt = '%s/plugins'%plugins_dirt
        sys.path.append(_plugin_dirt)
        import Script
        GetIfon= []
        ## [{"Arnold":{"app":[""],"info":[""]}},{}]
        plugin_cunt = 0
        for key in plugin_adict:
            if key in plugins_surpose: # surpose
                if os.path.exists('%s/Script/%s/%s_set.py'%(_plugin_dirt,key,key)):
                    hfs_ver = houdiniversion[:2]+"."+houdiniversion[2:3]+"."+houdiniversion[3:]
                    plu_ver = plugin_adict[key]
                    _locals = locals() ## python 3+
                    exec('GetIfon = Script.%s.%s_set.SET_ENV(hfs_ver,plu_ver)'%(key,key))
                    GetIfon.append({key:_locals['GetIfon']})
                    plugin_cunt += 1
        if plugin_cunt == 0:
            GetIfon.append({"Warning:":{'info':[1,'The plugins are not surposed.']}})
        return GetIfon


    @classmethod
    def HoudiniAppSetup(cls,cls_in=''):
        
        cls_in._app_set_finish = 0
        # return
        if cls_in._run_code_result:
            cls_in.LogsCreat("HoudiniAppSetup start...")
            try:                
                path_adict = {'codebase':cls_in._code_base_path,'hfsbase':cls_in._houdini_client_dir,'plugingbase':cls_in._houdini_PLuing_dirt}
                path_adict['temp'] = '%s/temp'%cls_in._task_folder
                cls_in._HoudiniAppSetup_run_info = cls.SetHoudiniApp(cls_in._hfs_version,path_adict)
            except Exception as e:
                cls_in._run_code_result = False
                cls_in._erorr_code = 'HoudiniUtil.SetHoudiniApp'
                cls_in._erorr_code_info = e
        cls_in._app_set_finish = 1


    @classmethod
    def SetHoudiniApp(cls,hfs_version='160600',path_adict={}):
        ## path_adict= {'codebase':'C:/script/CG/Houdini','hfsbase':'D:/plugins/houdini',
        ##              'plugingase':'B:/plugins/houdini','temp':'C:/work/render'}
        returninfo = []
        plantfrom = platform.system()

        if plantfrom == "Windows":
            returninfo = cls.SetHoudiniApp_win(hfs_version,path_adict)
        elif plantfrom == "Linux":
            returninfo = cls.SetHoudiniApp_Linux(hfs_version,path_adict)
        return returninfo

       
    @staticmethod
    def SetHoudiniApp_win(hfs_version='160600',path_adict={}):
        houdini_plugin_path = path_adict['plugingbase']       
        houdini_client_dir = path_adict['hfsbase']
        houdini_version = hfs_version
        temp_path = path_adict['temp']
        zip_tool = r'C:\7-Zip\7z.exe'
        ToCopyHfs = True
        for elm in [houdini_client_dir,temp_path]:
            if not os.path.exists(elm):
                os.makedirs(elm)

        h_source = os.path.abspath("%s/apps/win/%s.7z"%(houdini_plugin_path,houdini_version))
        houdini_app_path_zip = os.path.abspath("%s/%s.7z"%(houdini_client_dir,houdini_version))
        if os.path.exists(houdini_app_path_zip):
            ToCopyHfs = False
        
        ## unzip houdini 
        cmd_un7z = zip_tool + " x -y -aos "
        cmd_un7z += "%s/%s.7z"%(houdini_client_dir,houdini_version) # D:/plugins/houdini
        cmd_un7z += " -o%s" % ("%s/%s"%(houdini_client_dir,houdini_version))        
        
        ## subprocess
        Uzi_Houdini_log = open(r'%s/Uzip_Houdini.txt'%temp_path,'wt')     
        if ToCopyHfs:
            copyhoudini = subprocess.Popen("copy %s %s" % (h_source, houdini_app_path_zip),shell=True)
            copyhoudini.wait()

        UzipHoudini = subprocess.Popen(cmd_un7z,stdout=Uzi_Houdini_log,shell=True)
        UzipHoudini.wait()

        # finish,close the handl
        Uzi_Houdini_log.close()
        _h_result = UzipHoudini.returncode

        if not _h_result:
            print("Houdini setup finished. ")
            return ["Houdini%s setup finished. "%houdini_version]
        else:
            return ["Faild!"]

    @staticmethod
    def SetHoudiniApp_Linux(hfs_version='160600',path_adict={}):
        houdini_plugin_path = path_adict['plugingbase']       
        houdini_client_dir = path_adict['hfsbase']
        houdini_version = hfs_version
        temp_path = path_adict['temp']
        ToCopyHfs = True
        for elm in [houdini_client_dir,temp_path]:
            if not os.path.exists(elm):
                os.makedirs(elm)

        h_source = os.path.abspath("%s/apps/linux/%s.zip"%(houdini_plugin_path,houdini_version))
        houdini_app_path_zip = os.path.abspath("%s/%s.zip"%(houdini_client_dir,houdini_version))
        if os.path.exists(houdini_app_path_zip):
            ToCopyHfs = False
        
        ## unzip houdini 
        cmd_un7z = "/usr/bin/unzip -o -a "
        cmd_un7z += "%s/%s.zip"%(houdini_client_dir,houdini_version) # /usr/plugins/houdini
        cmd_un7z += " -d %s" % ("%s/%s"%(houdini_client_dir,houdini_version))        
        
        ## subprocess
        Uzi_Houdini_log = open(r'%s/Uzip_Houdini.txt'%temp_path,'wt')     
        if ToCopyHfs:
            copyhoudini = subprocess.Popen("cp %s %s" % (h_source, houdini_app_path_zip),shell=True)
            copyhoudini.wait()

        UzipHoudini = subprocess.Popen(cmd_un7z,stdout=Uzi_Houdini_log,shell=True)
        UzipHoudini.wait()

        # finish,close the handl
        Uzi_Houdini_log.close()
        _h_result = UzipHoudini.returncode

        if not _h_result:
            print("Houdini setup finished. ")
            return ["Houdini%s setup finished. "%houdini_version]
        else:
            return ["Faild!"]

    @classmethod
    def HoudiniServerSetup(cls,cls_in=''):
        cls_in._license_set_finished = 0
        # return
        if cls_in._run_code_result:
            cls_in.LogsCreat("HoudiniServerSetup start...")
            app_path = "%s/%s"%(cls_in._houdini_client_dir,cls_in._hfs_version)
            try:
                servers="10.60.96.203"
                cls_in._HoudiniServerSetup_run_info = HoudiniUtil.SetServer(cls_in._hfs_version,servers,app_path)
            except Exception as e:
                cls_in._run_code_result = False
                cls_in._erorr_code = 'HoudiniUtil.SetServer'
                cls_in._erorr_code_info = e
        cls_in._license_set_finished = 1

    @classmethod
    def SetServer(cls,houdini_vis='',HS_ip='',app_path=''):
        returncode = []
        hfs_version = houdini_vis[:2]
        plantfrom = platform.system()
        if plantfrom == "Windows":
            try_code = True
            cunt = 0
            while try_code:
                try:
                    returncode = cls.SetServer_win(hfs_version,HS_ip)
                    if returncode[0]==0:
                        ## start hkey.exe and the close it
                        # hkey = "%s/bin/hkey.exe"%app_path
                        # op = subprocess.Popen(hkey,shell=True)
                        # time.sleep(10)
                        # cls.KillApps(["hkey.exe"])
                        cunt =3
                    else:
                        cunt+1
                except Exception as e:
                    cunt +=1
                    returncode.append(e)
                if cunt>=3:
                    try_code = False

        elif plantfrom == "Linux":
            try_code = True
            cunt = 0
            while try_code:
                try:
                    returncode = cls.SetServer_Linux(hfs_version,HS_ip,app_path)
                    cunt =3 if returncode[0]==0 else cunt+1
                except Exception as e:
                    cunt +=1
                    returncode.append(e)
                if cunt>=3:
                    try_code = False

        return [returncode[1]]

    @classmethod
    def SetServer_win(cls,houdini_vis='',HS_ip=''):
        ## --------------------------------------------------------------------------
        ## infos list here
        ## --------------------------------------------------------------------------
        not_install = "The specified service does not exist as an installed service"
        to_install = False
        not_start = "The service has not been started"
        sc = r'C:\Windows\system32\sc.exe'
        findstr = r'C:\Windows\system32\findstr.exe'
        ## --------------------------------------------------------------------------
        ## --------------------------------------------------------------------------
        ## Try to stop HoudiniLicenseServer and HoudiniServer, if not exist,pass
        print("[lic] Tyr to stop HoudiniLicenseServer...")
        HLS,state_return = cls.SetServerAction("HoudiniLicenseServer","stop",True)
        if state_return == 1:
            print("[lic] The HoudiniLicenseServer is not exist.")
        else:
            print("[lic] The HoudiniLicenseServer is exist.")
            info = cls.SetServerAction("HoudiniLicenseServer","delete")

        print("[lic] Try to stop HoudiniServer...")
        HS_stop_cmd = '%s stop "HoudiniServer"'%sc
        HS,state_return = cls.SetServerAction("HoudiniServer","stop",True)
        if state_return == 1:
            print("[lic] The HoudiniServer is not exist.")
        else:
            print("[lic] HoudiniServer is exist.")
            info = cls.SetServerAction("HoudiniServer","delete")

        ## ctreat server
        # HoudiniLicenseServer
        print("[lic] Waitting for license stoped. 6s")
        time.sleep(6)
        print("[lic] HoudiniLicenseServer rebult...")
        HLS_src = os.path.join(r"B:\plugins\houdini\lic\win", houdini_vis, "sesinetd.exe")
        HLS_dst = os.path.join("C:\Windows\system32", "sesinetd.exe")    
        HLS_creat_cmd = "%s create HoudiniLicenseServer binPath= C:\Windows\system32\sesinetd.exe START= auto DISPLAYNAME= HoudiniLicenseServer TYPE= own"%sc
        print("[lic] cp sesinetd --> cline")
        resul = os.system('copy /y %s %s'%(HLS_src, HLS_dst))
        cp_resul = resul>>8
        if cp_resul:
            print("[lic] Canot do sesinetd cp.")
        else:
            print("[lic] cp suseece.")
        print("[lic] Create HoudiniLicenseServer...")
        creat_popen = subprocess.Popen(HLS_creat_cmd, stdout=subprocess.PIPE, shell=1)
        creat_popen.wait()

        # HoudiniServer
        print("[lic] HoudiniServer rebult...")
        HS_src = os.path.join(r"B:\plugins\houdini\lic\win", houdini_vis, "hserver.exe")
        HS_dst = os.path.join("C:\Windows\system32", "hserver.exe")
        HS_creat_cmd = "%s create HoudiniServer binPath= C:\Windows\system32\hserver.exe START= auto DISPLAYNAME= HoudiniServer TYPE= own"%sc
        print("[lic] cp hserver --> cline")
        resul_hs = os.system('copy /y %s %s'%(HS_src, HS_dst))
        cp_returncode = resul_hs>>8
        if cp_returncode:
            print("[lic] Canot do hserver cp.")
        else:
            print("[lic] cp suseece.")
        print("[lic] Create HoudiniServer...")
        creat_popen = subprocess.Popen(HS_creat_cmd, stdout=subprocess.PIPE, shell=1)
        creat_popen.wait()
        time.sleep(5)

        ## --------------------------------------------------------------------------------
        ## check the server whether installed
        # HoudiniLicenseServer
        ## --------------------------------------------------------------------------------
        print("[lic] HoudiniLicenseServer check install...")
        checkcmd = 'C:\Windows\system32\sc.exe query HoudiniLicenseServer|%s "STATE"'%findstr
        check_popen = subprocess.Popen(checkcmd, stdout=subprocess.PIPE, shell=1)
        check_popen.wait()
        check_info = check_popen.stdout.readlines()
        for elm in check_info:
            if "STOPPED" in str(elm).strip():
                to_install = False
                print("[lic] HoudiniLicenseServer install state: OK <STOPPED>.")
        # HoudiniServer
        print("[lic] HoudiniServer check install...")
        checkcmd = 'C:\Windows\system32\sc.exe query HoudiniServer|%s "STATE"'%findstr
        check_popen = subprocess.Popen(checkcmd, stdout=subprocess.PIPE, shell=1)
        check_popen.wait()    
        check_info = check_popen.stdout.readlines()
        for elm in check_info:
            if "STOPPED" in str(elm).strip():
                to_install = False
                print("[lic] HoudiniServer install state: OK <STOPPED>.")

        ## start sever
        print("[lic] to_install state: %s."%str(to_install))
        if to_install==False:
            predone = 0
            print("[lic] HoudiniLicenseServer start...")
            cls.SetServerAction("HoudiniLicenseServer","start")

            print("[lic] HoudiniServer start...")
            cls.SetServerAction("HoudiniServer","start")
            time.sleep(5)
            
            ## check the state
            print("[lic] HoudiniLicenseServer check...")
            checkcmd = 'C:\Windows\system32\sc.exe query HoudiniLicenseServer|%s "STATE"'%findstr
            check_popen = subprocess.Popen(checkcmd, stdout=subprocess.PIPE, shell=1)
            check_popen.wait()
            check_info = check_popen.stdout.readlines()
            for elm in check_info:
                if "RUNNING" in str(elm).strip():
                    predone +=1
                    print("[lic] HoudiniLicenseServer start state: OK <RUNNING>.")

            print("[lic] HoudiniServer check...")
            checkcmd = 'C:\Windows\system32\sc.exe query HoudiniServer|%s "STATE"'%findstr
            check_popen = subprocess.Popen(checkcmd, stdout=subprocess.PIPE, shell=1)
            check_popen.wait()
            check_info = check_popen.stdout.readlines()
            for elm in check_info:
                if "RUNNING" in str(elm).strip():
                    predone +=1
                    print("[lic] HoudiniServer start state: OK <RUNNING>.")

            print("[lic] Predone<pre set for change lic>: %s."%("True" if predone>=2 else "False"))
            if predone >=2:
                ## change license
                change_ip_cmd = HS_dst + " -S " + HS_ip
                change_popen = subprocess.Popen(change_ip_cmd, stdout=subprocess.PIPE, shell=1)
                change_popen.wait()
                time.sleep(5)
                change_info=change_popen.stdout.readlines()
                returninfo = ''
                for elm in change_info:
                    if "changed to " in str(elm).strip():
                        returninfo = str(elm).strip()
                        print("[lic] %s"%str(elm).strip())
                cls.SetServerAction("HoudiniServer","stop")
                time.sleep(2)
                cls.SetServerAction("HoudiniServer","start")
                time.sleep(2)
                        

        print("[lic] Server setup finished.")
        return [0,returninfo]

    @staticmethod
    def SetServerAction(server_name,action,findstr=False):
        not_install = "The specified service does not exist as an installed service"
        not_start = "The service has not been started"
        
        ## tools
        sc = r'C:\Windows\system32\sc.exe'
        findstr = r'C:\Windows\system32\findstr.exe'
        ## --------------------------------------------------------------------------
        ## ------------------------- actions ----------------------------------------
        print("[SetServerAction] Action: %s"%action)
        serv_cmd = '%s %s "%s"'%(sc,action,server_name)
        HLS_popen = subprocess.Popen(serv_cmd, stdout=subprocess.PIPE, shell=1)
        HLS_popen.wait()
        HLS = HLS_popen.stdout.readlines()
        if findstr:
            state_return = 0
            for elm in HLS:
                if not_install in str(elm).strip():
                    to_install = True
                    state_return = 1
                elif not_start in str(elm).strip():
                    state_return = 2
            return HLS,state_return
        else:
            return HLS


    @staticmethod
    def SetServer_Linux(houdini_vis='',HS_ip='',app_path=''):
        lic_path = r'/B/plugins/houdini/lic/linux'
        lic_bin = os.path.join(lic_path, houdini_vis, "sesinetd")
        lic_ini = os.path.join(lic_path, houdini_vis, "init", "sesinetd")

        sesi_path = r'/usr/lib/sesi'
        inid_path = r'/etc/init.d'
        if not os.path.exists(sesi_path):
            os.makedirs(sesi_path)
        if not os.path.exists(inid_path):
            os.makedirs(inid_path)

        HLS_dst = os.path.join(sesi_path, "sesinetd")
        HLS_server= '/etc/init.d/sesinetd'
        HLS_stop_cmd = '/etc/init.d/sesinetd stop'
        HLS_start_cmd = '/etc/init.d/sesinetd start'

        if os.path.exists(HLS_dst) and os.path.exists(HLS_server):
            print("License is exist, try to kill it. ")
            HLS_stop_popen = subprocess.Popen(HLS_stop_cmd, stdout=subprocess.PIPE, shell=1)
            HLS_stop_popen.wait()
            time.sleep(3)

        shutil.copy(lic_bin, HLS_dst)
        shutil.copy(lic_ini, HLS_server)

        HLS_start_popen = subprocess.Popen(HLS_start_cmd, stdout=subprocess.PIPE, shell=1)
        HLS_start_popen.wait()
        time.sleep(3)

        ### To change the server ips
        ### kill hserver if it is running 
        get_pid = 'ps -ef | grep -v grep | grep \'hserver\''
        pid_popen= subprocess.Popen(get_pid, stdout=subprocess.PIPE, shell=1)
        pid_popen.wait()
        hserver_pid=''
        print (pid_popen.stdout.read())
        if len(pid_popen.stdout.read())>5:
            pid_str = pid_popen.stdout.read()
            print(pid_str)
            hserver_pid=re.findall('\d+',pid_str)[0]

        ### The hserver just in the /hfs*/bin folder in linux
        HS_dst = os.path.join(app_path,"bin/hserver")
        HS_start_cmd = HS_dst
        HS_s_ip_cmd = HS_dst + " -S " + HS_ip
        if not hserver_pid=="":
            HS_kill = 'kill -9 ' + hserver_pid
            HS_stop_popen = subprocess.Popen(HS_kill, stdout=subprocess.PIPE, shell=1)
            HS_stop_popen.wait()
            time.sleep(3)
        if os.path.exists(HS_start_cmd):
            chmod="chmod 777 "+HS_start_cmd
            subprocess.call(chmod, stdout=subprocess.PIPE, shell=1)
            HS_start_popen = subprocess.Popen(HS_start_cmd, stdout=subprocess.PIPE, shell=1)
            HS_start_popen.wait()
            time.sleep(3)

            HS_s_ip_cmd_popen = subprocess.Popen(HS_s_ip_cmd, stdout=subprocess.PIPE, shell=1)
            HS_s_ip_cmd_popen.wait()
            time.sleep(5)
            change_info=HS_s_ip_cmd_popen.stdout.readlines()
            returninfo = ''
            for elm in change_info:
                if "already set to" in elm.strip():
                    returninfo = elm.strip()
        else:
            print("ERROR: CORRESPONDING hserver DOESNT EXIST.")
            print(HS_start_cmd)
            print(HS_dst)
            return ["Server dosnt exist."]
            sys.exit(1)

        print("Server setup finished.")
        return [0,returninfo]

    @classmethod
    def AssetSetup(cls,cls_in=''):
        cls_in.LogsCreat("AssetSetup start...")
        try:
            cls_in._AssetSetup_run_info = ['AssetSetup']
        except Exception as e:
            cls_in._run_code_result = False
            cls_in._erorr_code = 'AssetSetup'
            cls_in._erorr_code_info = e


    @classmethod
    def print_times(cls,info="",file="",type=""):
        time_point=time.strftime("%b_%d_%Y %H:%M:%S", time.localtime())
        addpoint = "HTS"
        infos = "["+str(addpoint) + "] " + str(info)
        print (infos)

        if type=="w":
            if not os.path.exists(file):
                if not os.path.exists(os.path.dirname(file)):
                    os.makedirs(os.path.dirname(file))
                with open(file,"w") as f:
                    f.close()
            else:
                with open(file,"a") as f:
                    f.write(infos)
                    f.close()

    @classmethod
    def GetSaveHipInfo(cls,hipfile='',_app_path=''):
        with open(hipfile, "rb") as hipf:
            Not_find = True
            search_elm = 2
            search_elm_cunt = 0
            while Not_find:
                line = str(hipf.readline()).encode("utf-8")
                #print(line)
                # Save version 
                #if re.match('^set -g _HIP_SAVEVERSION = ', str(line)):
                if "set -g _HIP_SAVEVERSION = " in  str(line):
                    # print(str(line))
                    pattern = re.compile("[\d+\d+\d+]")
                    _HV = pattern.findall(str(line))
                    if len(_HV)>6: _HV = _HV[:6]
                    _hfs_save_version = int(''.join(elm for elm in _HV))
                    search_elm_cunt += 1

                # The $HIP val with this file saved
                #if re.match('^set -g HIP = ', str(line)):
                if "set -g HIP = " in  str(line):
                    pattern = re.compile(r"\\'.*\\'")
                    _Hip = pattern.search(str(line)).group()[1:-1]
                    _hip_save_val = _Hip.split("\'")[1].replace("\\","/")
                    search_elm_cunt += 1
                if search_elm_cunt >= search_elm:
                    Not_find = False
        
        # get the bast version for running
        if not  Not_find:
            _files_name = []
            _ver_list = []            
            for (dirpath, dirnames, filenames) in os.walk(_app_path):
                _files_name.extend(filenames)

            if len(_files_name):
                for elm in _files_name:
                    ver = elm.split(".7z")[0] if ".7z" in elm else (elm.split(".zip")[0] if "" in elm else '')
                    print(ver)
                    try:
                        _ver_list.append(int(ver))
                    except:
                        pass
 
            if len(_ver_list):
                _ver_list = sorted(_ver_list)
                mid = len(_ver_list)
                if int(_hfs_save_version)>=_ver_list[int(mid/2)]:
                    min_ver = _ver_list[int(mid/2)]
                    max_ver = _ver_list[mid-1] if mid >2 else _ver_list[int(mid/2)]
                    much_ver = 0
                    get_ver = 0
                    if int(_hfs_save_version)<max_ver:
                        for i in range(int(mid/2),len(_ver_list)):
                            if int(_hfs_save_version)==_ver_list[i]:
                                get_ver = _ver_list[i]
                                break
                            elif int(_hfs_save_version)>_ver_list[i]:
                                min_ver = _ver_list[i]
                            elif int(_hfs_save_version)<_ver_list[i] and much_ver==0:
                                much_ver = _ver_list[i]
                        _hfs_version = get_ver if get_ver else much_ver
                    else:
                        _hfs_version = max_ver
                else:
                    min_ver = _ver_list[0]
                    max_ver = _ver_list[int(mid/2)-1] if mid > 2 else _ver_list[int(mid/2)]
                    much_ver = 0
                    get_ver = 0
                    if int(_hfs_save_version)<max_ver:
                        for i in range(0,int(mid/2)+1):
                            if int(_hfs_save_version)==_ver_list[i]:
                                get_ver = _ver_list[i]
                                break
                            elif int(_hfs_save_version)>_ver_list[i]:
                                min_ver = _ver_list[i]
                            elif int(_hfs_save_version)<_ver_list[i] and much_ver==0:
                                much_ver = _ver_list[i]
                        _hfs_version = get_ver if get_ver else much_ver
                    else:
                        _hfs_version = max_ver
                _hfs_version = str(_hfs_version)

                return [_hfs_save_version,_hfs_version,_hip_save_val]

            else:
                _erorr_code_info = 'The app folder is emplty.'
                return [_erorr_code_info]
        else:
            _erorr_code_info = 'Bad hip file.'
            return [_erorr_code_info]

    @classmethod
    def KillApps(cls,Killapps=[],platform='win'):
        for app in Killapps:
            if not platform=='Linux':
                cmds = r'c:\windows\system32\cmd.exe /c c:\windows\system32\TASKKILL.exe /F /IM %s'%app
                subprocess.call(cmds,shell=True)
            elif platform=='Linux':
                cmds = ''
                get_pid_cmd = 'ps -ef | grep -v grep | grep '
                get_pid_cmd = get_pid_cmd+"'"+proc+"'"
                pid_popen= subprocess.Popen(get_pid_cmd, stdout=subprocess.PIPE, shell=1)
                hserver_pid=''
                if len(pid_popen.stdout.read())>5:
                    pid_str = pid_popen.stdout.read()
                    hserver_pid=re.findall('\d+',pid_str)[0]
                if not hserver_pid=="":
                    HS_kill = 'kill -9 '+hserver_pid
                    HS_stop_popen = subprocess.Popen(HS_kill, stdout=subprocess.PIPE, shell=1)
                    HS_stop_popen.wait()

    @classmethod
    def SequenceCheck(cls,cls_in='',dirs='',file='',nodepath='',keyw="files"):

        if not file=="":
            in_adict,to_check,findit,infos,return_file = cls.check_adict(dirs,file,cls_in.foler_adict)
            """returns:  in_adict,check,findit,is_exist  """

            if in_adict:
                '''
                If folder dirt in the adict of this folder,try to find whether the file in it,
                if in it and had checked onece,passed 
                '''
                if to_check and findit: ## in the "other" list
                    is_sequence,sequence_adict,dif_list = cls.issequence(dirs,file,infos)
                elif to_check==False and findit: ## in the "folder" adict,dont check again
                    is_sequence=3
                    dif_list = []
                elif findit==False and infos==False: ## Not exist, miss
                    is_sequence=2
                    dif_list = []

            else:
                is_sequence,sequence_adict,dif_list = cls.issequence(dirs,file)
            if is_sequence==0:   ## exist , is sequence
                """
                sequence_adict:
                {"abc":[["abc.0001","abc.0002"..."abc.0010"],1,10,4,abc.$F3.exr]}
                """
                full_path = os.path.join(dirs,sequence_adict[sequence_adict.keys()[0]][4]).replace("\\","/")
                temp_list_n = [full_path,[sequence_adict[sequence_adict.keys()[0]][1],
                            sequence_adict[sequence_adict.keys()[0]][2]]]
                cls.asset_adict_edit(cls_in.asset_adict,"Normal",keyw,nodepath,temp_list_n)

                ## ------------------------------------------------------------------------------
                """  get the miss files in sequence   """
                ## ------------------------------------------------------------------------------
                miss_adict,file_miss_adict = cls.getmiss_elm(sequence_adict)
                
                if len(file_miss_adict):  ## folder_adict
                    if dirs in cls_in.foler_adict:
                        if "sequences" in cls_in.foler_adict[dirs]:
                            copy_adict = cls_in.foler_adict[dirs]["sequences"]
                            dictMerged=dict(copy_adict.items()+file_miss_adict.items())
                            cls_in.foler_adict[dirs]["sequences"]=dictMerged
                        else:
                            copy_adict = cls_in.foler_adict[dirs]
                            cls_in.foler_adict[dirs]["sequences"]=file_miss_adict
                    else:
                        copy_adict ={"sequences":file_miss_adict}
                        cls_in.foler_adict[dirs]=copy_adict
                
                if len(miss_adict): ## asset_adict
                    full_path = os.path.join(dirs,miss_adict.keys()[0]).replace("\\","/")
                    temp_list_m = [full_path,miss_adict[miss_adict.keys()[0]]]
                    cls.asset_adict_edit(cls_in.asset_adict,"Miss",keyw,nodepath,temp_list_m)

            elif is_sequence==1: ## exist ,not sequence
                file=sequence_adict
                if dirs in cls_in.foler_adict: ## foler_adict
                    if "singles" in cls_in.foler_adict[dirs]:
                        copy_list = cls_in.foler_adict[dirs]["singles"]
                        if file not in copy_list:
                            copy_list_new = copy_list.append(file)
                            cls_in.foler_adict[dirs]["singles"]=copy_list_new
                    else:
                        copy_list = [file]
                        cls_in.foler_adict[dirs]["singles"]=copy_list
                else:
                    copy_list ={"singles":[file]}
                    cls_in.foler_adict[dirs]=copy_list

                ## asset_adict
                full_path_single = [os.path.join(dirs,file).replace("\\","/")]
                cls.asset_adict_edit(cls_in.asset_adict,"Normal",keyw,nodepath,full_path_single)

            elif is_sequence==2: ## not exist,single file
                file=sequence_adict
                # ----------------------- foler_adict ----------------------------------------
                if dirs in cls_in.foler_adict:
                    if "miss" in cls_in.foler_adict[dirs]:
                        copy_list = cls_in.foler_adict[dirs]["miss"]
                        if not copy_list == None:
                            cls_in.foler_adict[dirs]["miss"]=copy_list.append(file)
                    else:
                        copy_list = [file]
                        cls_in.foler_adict[dirs]["miss"]=copy_list
                else:
                    copy_list ={"miss":[file]}
                    cls_in.foler_adict[dirs]=copy_list

                # ----------------------- asset_adict ----------------------------------------
                full_path_single = [os.path.join(dirs,file).replace("\\","/")]
                cls.asset_adict_edit(cls_in.asset_adict,"Miss",keyw,nodepath,full_path_single)

            elif is_sequence==3: ## from the adict
                """
                first, got the node path in check_history,then,cp the node val from asset
                """
                node_path = ''
                for key in cls_in.check_history:
                    if return_file in cls_in.check_history[key]:
                        node_path = cls_in.check_history[key][0]
                        break
                if not node_path == '':
                    search_adict = cls_in.asset_adict["Normal"]
                    search_val = None
                    for key1 in search_adict:
                        for key2 in search_adict[key1]:
                            if node_path in search_adict[key1][key2]:
                                search_val = search_adict[key1][key2]
                                break
                    if search_val != None:
                        # print(search_val)
                        cls.asset_adict_edit(cls_in.asset_adict,"Normal",keyw,nodepath,search_val)
                    else:
                        print("Cant find. HoudiniUtil.SequenceCheck.is_sequence==3")
                else:
                    print("Cant find the file, Error calls! HoudiniUtil.SequenceCheck.is_sequence==3")
            else:
                """
                something else
                """
                pass

            if len(dif_list):
                
                if not in_adict:
                    reset_adict = cls.GetBadFile(dif_list)
                else:
                    reset_adict=[{},dif_list]

                """  bad file in this folder """
                if len(reset_adict[0]):
                    if dirs in cls_in.foler_adict:
                        cls_in.foler_adict[dirs]["badfiles"]=reset_adict[0]
                    else:
                        copy_adict ={"badfiles":reset_adict[0]}
                        cls_in.foler_adict[dirs]=copy_adict
                    # print("-"*50)
                    # print("Bad file in : %s"%dirs)
                    # print(str(reset_adict[0]))
                    # print("-"*50)

                """  other file in this folder  """
                if len(reset_adict[1]):
                    if dirs in cls_in.foler_adict:
                        cls_in.foler_adict[dirs]["others"]=reset_adict[1]
                    else:
                        copy_adict ={"others":reset_adict[1]}
                        cls_in.foler_adict[dirs]=copy_adict
                    # print(reset_adict[1])
        else:
            """ Get all the sequence in this folder """
            pass

    @staticmethod
    def asset_adict_edit(adict_in='',first_key='',sec_key='',thr_kry='',val_in=[]):
        if first_key in adict_in:
            if sec_key in adict_in[first_key]:
                if not thr_kry in adict_in[first_key][sec_key]:
                    copy_adict = adict_in[first_key][sec_key]  
                    copy_adict[thr_kry] = val_in
                    adict_in[first_key][sec_key] = copy_adict
            else:
                copy_adict = {thr_kry:val_in}
                adict_in[first_key][sec_key] = copy_adict
        else:
            copy_adict ={sec_key:{thr_kry:val_in}}
            adict_in[first_key] = copy_adict

    @classmethod
    def issequence(cls,dirt='',filename='',adict_in={}):
        is_sequence = 1
        if filename != "":
            sequence_adict={}
            maby_sequence = True
            dif_list = []
            maby_sequence,split_str,num = cls.getnumber(filename)
            All_files = os.listdir(dirt) if not len(adict_in) and os.path.exists(dirt) else adict_in
            if maby_sequence:
                sequence_list = []
                for elm in All_files:
                    filename_list=filename.split(split_str)
                    if filename_list[0] in elm:
                        split_str_elm = cls.getnumber(elm)[1]
                        elm_split = elm.split(split_str_elm)
                        if elm_split[0]==filename_list[0] and elm_split[-1]==filename_list[-1]:
                            sequence_list.append(elm)
                        else:
                            dif_list.append(elm)
                    else:
                        dif_list.append(elm)

                if len(sequence_list)>3:
                    is_sequence = 0
                    i=0
                    seq_name = ''
                    seq_len = 0
                    min_num=0
                    max_num=0
                    first_elm = ''
                    for elm in sequence_list:
                        num = cls.getnumber(elm)[2]
                        if i==0:
                            min_num = int(num)
                            first_elm = elm
                        if i==len(sequence_list)-1:seq_len_end = len(num)
                        if int(num)<min_num:
                            min_num=int(num)
                            first_elm = elm
                        if int(num)>max_num:max_num=int(num)
                        i +=1
                    # print("%s sequence from %d to %d"%(seq_name,min_num,max_num))
                    maybes,split_str_1,num_1 = cls.getnumber(first_elm)
                    seq_name = first_elm.split(split_str_1)[0]
                    end_with = first_elm.split(split_str_1)[-1]
                    if len(num_1)>1:
                        file_replace_name = seq_name+split_str_1.replace(num_1,"$F%d"%len(num_1))+end_with
                    else:
                        file_replace_name = seq_name+split_str_1.replace(num_1,"$F")+end_with

                    """ put into adict """
                    """ {"abc":[["abc.0001","abc.0002"..."abc.0010"],1,10,4,abc.$F3.exr]} """
                    sequence_adict[seq_name]=[sequence_list,min_num,max_num,len(num_1),file_replace_name]
                    return is_sequence,sequence_adict,dif_list
                else:
                    maby_sequence=False
            if not maby_sequence:
                file_path = os.path.abspath(os.path.join(dirt,filename))
                if os.path.exists(file_path):
                    ### exist , not a sequence
                    if len(adict_in):
                        adict_in.remove(filename)
                        dif_list.extend(adict_in)
                    else:
                        All_files.remove(filename)
                        dif_list.extend(All_files)
                    return is_sequence,filename,dif_list
                else:
                    # print("this file is not exist.")
                    return 2,filename,[]
        else:
            print("Please set the filename for this function.")
            return 3,"Please set the filename for this function.",[]

    @staticmethod
    def getmiss_elm(adictin={}):
        miss_adict = {}
        files_adict = {}
        for key in adictin.keys():
            num_list = []
            miss_list = []
            list_sequ = adictin[key][0]
            for elm in list_sequ:
                num_list.append(int(re.findall("\d+",elm)[-1]))
            num_list = sorted(num_list)
            min_num = adictin[key][1]
            max_num = adictin[key][2]
            for i in range(len(num_list)):
                if num_list[i] >=min_num and num_list[i]<=max_num:
                    if i==0 and num_list[i] == min_num:curent_val = min_num
                    if not curent_val in num_list:
                        miss_list.append(curent_val)
                    curent_val += 1
            miss_adict[adictin[key][4]] = miss_list
            files_adict[key] = {"start":min_num,"end":max_num,"miss":miss_list}
        return miss_adict,files_adict

    @classmethod
    def getnumber(cls,filename=''):
        maby_sequence = True
        split_str = ''
        num = ''
        with_num = re.findall("\d+",filename)
        if len(with_num)>0:
            num = with_num[-1]
            num_len = len(with_num[-1])
            if ("."+with_num[-1]+".") in filename:
                split_str = "."+with_num[-1]+"."
            elif (with_num[-1]+".") in filename:
                split_str = with_num[-1]+"."
            else:
                maby_sequence = False
                # print("Not sequence")
        else:
            maby_sequence = False
            # print("Without Numbers")
        return maby_sequence,split_str,num

    @classmethod
    def GetBadFile(cls,adict=''):
        bad_end = ['kkk','aspk']
        bad_list = []
        other_list = []
        bad_adict = {}
        if len(adict):
            for elm in adict:
                if elm.split(".")[-1] in bad_end:
                    bad_list.append(elm)
                else:
                    other_list.append(elm)
        if len(bad_list):
            for elm in bad_list:
                copy_list = []
                maby_sequence,split_str,num = cls.getnumber(elm)
                if maby_sequence:
                    filename = elm.split(split_str)[0]
                    if "sequence" in bad_adict.keys():
                        copy_adict = bad_adict["sequence"]
                        if filename in copy_adict.keys():
                            copy_list=copy_adict[filename]
                            copy_list.append(elm)
                            copy_adict[filename]=copy_list
                        else:
                            copy_list=[elm]
                            copy_adict[filename]=copy_list
                        bad_adict["sequence"]=copy_adict
                    else:
                        copy_list=[elm]
                        bad_adict["sequence"]={filename:copy_list}
                else:
                    filename = elm.split(".")[0]
                    if "single" in bad_adict.keys():
                        copy_list=bad_adict["single" ]
                        if not filename in copy_list:
                            copy_list.append(elm)
                        bad_adict["single"]=copy_list
                    else:
                        copy_list=[elm]
                        bad_adict["single" ]=copy_list
        return bad_adict,other_list

    @classmethod
    def check_adict(cls,dirt="",filename="",adict_in={}):
        ## adict_in={"sequences":{},"singles":[],"badfiles":{"single":[],"sequence":{}},"others":[]}
        in_adict = False
        check = True
        findit = False
        is_exist = True
        types = ''
        infos = ''
        f_name = ''
        if dirt in adict_in:
            maby_sequence,split_str,num = cls.getnumber(filename)
            if maby_sequence:
                seq_name = filename.split(split_str)[0]
                if "sequences" in adict_in[dirt]:
                    if seq_name in adict_in[dirt]["sequences"]:
                        in_adict = True
                        check = False
                        findit = True
                        f_name = seq_name
                        # infos = [findit,"sequence",[seq_name,adict_in[dirt]["sequences"][seq_name]]]
                elif "badfiles" in adict_in[dirt]:
                    if "sequence" in adict_in[dirt]["badfiles"]:
                        if seq_name in adict_in[dirt]["badfiles"]["sequence"]:
                            in_adict = True
                            check = False
                            findit = True
                            f_name = seq_name

            if findit==False:
                if "singles" in adict_in[dirt]:
                    if filename in adict_in[dirt]["singles"]:
                        in_adict = True
                        check = False
                        findit = True
                        f_name = filename
                        # infos = [findit,"single"]
                if "badfiles" in adict_in[dirt]:
                    if "single" in adict_in[dirt]["badfiles"]:
                        if filename in adict_in[dirt]["badfiles"]["single"]:
                            in_adict = True
                            check = False
                            findit = True
                            f_name = filename
                            # infos = [findit,"badfile"]
                if "others" in adict_in[dirt].keys():
                    if filename in adict_in[dirt]["others"]:
                        ## to check
                        in_adict = True
                        findit = True
                        infos = adict_in[dirt]["others"]

            if findit==False:
                if not os.path.exists(os.path.abspath(os.path.join(dirt,filename))):
                    is_exist = False
                    check = False
                    infos=is_exist
                    # print("Not exist!")

        return in_adict,check,findit,infos,f_name

    @classmethod
    def WriteFile(cls,info="",file="",types='txt'):
        if types == 'txt':
            with open(file,"w") as f:
                f.write(info)
                f.close()
        elif types == 'json':
            with open(file,"w")as f:
                json.dump(info,f)
                f.close()
        cls.print_times("Infomations write to %s" %file)

    @staticmethod
    def copyfiles(pathin,frame,aim_name):
        source_path = os.path.abspath(pathin)
        frame_folder = str(frame).zfill(4)

        for dirpath,dirnames,filenames in os.walk(source_path):
            if dirpath == source_path:
                print(dirpath)
                print(dirnames)
                print(filenames)
                if len(dirnames):
                    for fd in dirnames:
                        if fd not in aim_name:
                            path_new = os.path.join(dirpath,fd)
                            path_aim = os.path.join(dirpath,frame_folder,fd)
                            print(path_new,path_aim)
                            os.system ("robocopy /e /ns /nc /nfl /ndl /np /move %s %s" % (path_new, path_aim))
                if len(filenames):
                    for pic in filenames:
                        path_new = os.path.join(dirpath,pic)
                        path_aim = os.path.join(dirpath,frame_folder,pic)
                        if not os.path.exists(os.path.join(dirpath,frame_folder)):os.makedirs(os.path.join(dirpath,frame_folder))
                        print(path_new,path_aim)
                        os.system ('copy /y  "%s" "%s"' % (path_new, path_aim))
                        os.remove(path_new)
        aim_name.append(frame_folder)
        return aim_name