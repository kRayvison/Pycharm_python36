#!/usr/bin/env python
#encoding:utf-8
# -*- coding: utf-8 -*-
import os,sys,time,re
import subprocess
import socket
import shutil
import platform
import re,json
import winreg

class KeyshotUtil():

    
    @staticmethod
    def SysTemInfo():
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
                pass

            except Exception as e:
                cls_in._run_code_result = False
                cls_in._erorr_code = 'HoudiniUtil.SetRenderer'
                cls_in._erorr_code_info = e
        else:
            cls_in._PluginsSetup_run_info = ["Not any plugins to set."]

    @classmethod
    def KeyshotAppSetup(cls,cls_in=''):
        
        cls_in._app_set_finish = 0
        # return
        if cls_in._run_code_result:
            cls_in.LogsCreat("KeyshotAppSetup start...")
            app_path = "%s/software/KS%s" % (cls_in._keyshot_PLuing_dirt,cls_in._keyshot_version)
            try:                
                _KeyshotServerSetup_run_info,computerid_got = cls.KeyshotServerSetup(cls_in)
                cls.CopySoft(cls_in._keyshot_version,computerid_got,app_path)
                cls.SetScripts(cls_in._code_base_path,cls_in._keyshot_version[:1])
            except Exception as e:
                cls_in._run_code_result = False
                cls_in._erorr_code = 'KeyshotUtil.KeyshotAppSetup'
                cls_in._erorr_code_info = e
            cls_in.LogsCreat("KeyshotAppSetup finished.")
            cls_in._app_set_finish = 1

    @classmethod
    def KeyshotServerSetup(cls,cls_in=''):
        if cls_in._run_code_result:
            cls_in.LogsCreat("KeyshotServerSetup start...")

            data_path = "%s/lib/data/datas.json"%cls_in._keyshot_PLuing_dirt
            version = cls_in._keyshot_version[:1]
            data_dict = eval(open(data_path,"r").read())
            ## temp data path
            reg_temp = "C:/temp/reg_tem.txt"
            if not os.path.exists("C:/temp"):
                os.makedirs("C:/temp")
            try:
                return RegEdit.SetServer(version,data_dict,reg_temp)
            except Exception as e:
                cls_in._run_code_result = False
                cls_in._erorr_code = 'KeyshotUtil.KeyshotServerSetup'
                cls_in._erorr_code_info = e
            cls_in.LogsCreat("KeyshotServerSetup end.")
            

    @staticmethod
    def SetScripts(source,ver='6'):
        Scripts = ["KeyshotUtil.py","KeyshotPlugin.py"]
        basePath = os.path.abspath('%s/function'%source)
        scriptPath = r'C:\Users\enfuzion\Documents\KeyShot %s\Scripts'%ver
        for elm in Scripts:
            baseScript = '"%s\\%s"'%(basePath,elm)
            scripScript = '"%s\\%s"'%(scriptPath,elm)
            os.system("copy %s %s"%(baseScript,scripScript))

    @staticmethod
    def CopySoft(version='7.2',computerid = '',soucer=""):
        # KeyShot 6.7z
        # KeyShot6.7z
        version = version[:1]
        prog_file = "KeyShot%s.zip"%version
        docm_file = "KeyShot %s.zip"%version
        prog = r"C:/Program Files"
        docm = r"C:/Users/enfuzion/Documents"
        if not os.path.exists("%s/%s" % (prog,prog_file)):
            s = '%s/%s'%(soucer,prog_file)
            a = '%s/%s' % (prog,prog_file)
            cmds = 'copy /y "%s" "%s"' % (os.path.abspath(s),os.path.abspath(a))
            print("cp %s --> %s"%(s,a))
            if 0:print(cmds)
            subprocess.call(cmds,shell=1)

        if not os.path.exists("%s/%s" % (docm,docm_file)):
            s = '%s/%s'%(soucer,docm_file)
            a = '%s/%s' % (docm,docm_file)
            cmds = 'copy "%s" "%s"' % (os.path.abspath(s),os.path.abspath(a))
            print("cp %s --> %s"%(s,a))
            if 0:print(cmds)
            subprocess.call(cmds,shell=1)
        
        if not os.path.exists(r"C:\7-Zip"):
            print("Setup tools...")
            zip_s = "B:\tools\7-Zip"
            subprocess.call("robocopy /S /NDL /NFL %s %s %s" % (zip_s, r"C:\7-Zip", "*"))
            
        cmd_unpro = r"C:\7-Zip\7z.exe x -y -aos "
        cmd_unpro += '"%s/%s"' % (prog,prog_file)
        cmd_unpro += " -o%s" % ('"%s"'%prog)
        
        cmd_undocm = r"C:\7-Zip\7z.exe x -y -aos "
        cmd_undocm += '"%s/%s"' % (docm,docm_file)
        cmd_undocm += " -o%s" % ('"%s"'%docm)
        
        cmd_lic = r"copy B:\plugins\KeyShot\KS_license\%s\%s\keyshot%s.lic " % (computerid,version,version)
        cmd_lic += '"%s\KeyShot %s\keyshot%s.lic"' % (docm,version,version)
        
        pro_handle = open("C:/temp/unzip_keyshot_pro.txt","w")
        doc_handle = open("C:/temp/unzip_keyshot_doc.txt","w")
        try:
            if 0:
                print(cmd_unpro)
                print(cmd_undocm)
                print(cmd_lic)
            subprocess.call(cmd_unpro,stdout=pro_handle,shell=True)
            subprocess.call(cmd_undocm,stdout=doc_handle,shell=True)
            subprocess.call(cmd_lic,shell=True)
        finally:
            pro_handle.close()
            doc_handle.close()

    @classmethod
    def print_times(cls,info="",file="",type=""):
        time_point=time.strftime("%b_%d_%Y %H:%M:%S", time.localtime())
        addpoint = "KS"
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

class RegEdit():

    @classmethod
    def SetServer(cls,version='',data_dict='',temp=""):
        computer_elm = data_dict['computer']
        adict_new = data_dict['keyshot %s'%version]
        adict_temp ={}

        print("Try to find the computer_ids.")
        findit = False
        computer_node = ''
        for elm in computer_elm:
            try:
                if winreg.OpenKey(winreg.HKEY_USERS,computer_elm[elm]):
                    findit = True
                    computer_node = elm
            except:
                pass
        print("Final Computer found: %s" % computer_node)
        
        # ----------------------------------------------------------------------------------------------------
        # found whether if the keyshot * is exist
        # ----------------------------------------------------------------------------------------------------
        keyshot_ver = r'%s\Software\Luxion\KeyShot %s' % (computer_elm[computer_node],version)
        it_exit = False
        upnode_exist = False
        try:
            if winreg.OpenKey(winreg.HKEY_USERS,keyshot_ver):
                it_exit = True
        except:
            print("The KeyShot reg key is not found.")
        
        print("KeyShot %s key: %s" % (version,it_exit))
        if it_exit==False:
            up_node = os.path.dirname(keyshot_ver)
            try:
                if winreg.OpenKey(winreg.HKEY_USERS,up_node):
                    upnode_exist = True
            except:
                print("Luxion not exist.")

        if it_exit:
            print("[Back] Try to back the reg_keyshot.")
            try:
                mainkey = winreg.OpenKey(winreg.HKEY_USERS,keyshot_ver)
                i = 0 
                while 1: 
                    name, value, type = winreg.EnumValue(mainkey, i)
                    #print (name,value)
                    adict_temp[name] = value
                    i += 1
            except WindowsError:
                print("[Back] Search finished.")
            if len(adict_temp):
                # print(adict_temp)
                with open(temp,"w") as f:
                    f.write(str(adict_temp))
                    f.close()
                print("[Back] Back reg_keyshot finished.")
            # ---------------------------------------------------------------------------------------------
            # try to  delete it 
            # ---------------------------------------------------------------------------------------------
            print("Try to delete reg_keyshot.")
            try:
                cls.DeleteKeys(keyshot_ver)
                print("DeleteKey reg_keyshot finished.")
            except:
                pass

        elif upnode_exist == False:
            print("Check 'Software'")
            software = "%s\Software" % (computer_elm[computer_node])
            software_exist = False
            try:
                if winreg.OpenKey(winreg.HKEY_USERS,software):
                    software_exist = True
            except:
                print("Software key not exist.")
            if software_exist == False:
                print("Creat '\Software'")
                up_node = os.path.dirname(software)
                thiskey = winreg.OpenKey(winreg.HKEY_USERS,up_node)
                newKey_ks = winreg.CreateKey(thiskey, "Software")
            print("Creat '\Software\*'")
            ks_version = os.path.basename(os.path.basename(keyshot_ver))
            thiskey = winreg.OpenKey(winreg.HKEY_USERS,software)
            newKey = winreg.CreateKey(thiskey,"Luxion")

        up_node = os.path.dirname(keyshot_ver)
        ks_version = os.path.basename(keyshot_ver)
        mainkey = winreg.OpenKey(winreg.HKEY_USERS,up_node)
        newKey_ks = winreg.CreateKey(mainkey,ks_version)
        for elm in adict_new:
            winreg.SetValueEx(newKey_ks,elm,0,1,adict_new[elm])
        print("Creat KeyShot %s key finished." % version)


        return ["Creat KeyShot %s key finished." % version,computer_node]
  
    @staticmethod
    def DeleteKeys(nodekey):
        thiskey = winreg.OpenKey(winreg.HKEY_USERS,nodekey)
        subkeys = []
        try:
            i = 0 
            while 1: 
                this_key = winreg.EnumKey(thiskey, i)
                print(this_key)
                subkeys.append(this_key)
                i += 1
        except WindowsError:
            pass
            #print("finished.")

        if len(subkeys)==0:
            thisNode = os.path.dirname(nodekey)
            ks_version = os.path.basename(nodekey)
            thiskey = winreg.OpenKey(winreg.HKEY_USERS,thisNode)
            winreg.DeleteKey(thiskey, ks_version)
        else:
            if len(subkeys):
                for elm in subkeys:
                    this_node_new = "%s\%s" % (nodekey,elm)
                    print(this_node_new)
                    DeleteKeys("%s"%this_node_new)
                    print("DeleteKeys: %s "%this_node_new)

            thisNode = os.path.dirname(nodekey)
            ks_version = os.path.basename(nodekey)
            thiskey = winreg.OpenKey(winreg.HKEY_USERS,thisNode)
            winreg.DeleteKey(thiskey, ks_version)
