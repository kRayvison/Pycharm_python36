import sys,os,subprocess,string,re,time,shutil
import json

def hou_lic(houdini_vis,HS_ip):
    print "houdini_vis:%s, HS_ip:%s" % (houdini_vis, HS_ip)
    strcmd = 'sc query HoudiniLicenseServer|findstr "STATE"'
    HLS_popen = subprocess.Popen(strcmd, stdout=subprocess.PIPE, shell=1)
    HLS = HLS_popen.stdout.read()
    HLS_popen.wait()
    
    HLS_src = os.path.join(r"b:\plugins\houdini\lic", houdini_vis, "sesinetd.exe")
    HLS_dst = os.path.join("C:\Windows\System32", "sesinetd.exe")
    HLS_stop_cmd = 'SC STOP "HoudiniLicenseServer"'
    HLS_start_cmd = 'SC start "HoudiniLicenseServer"'
    HLS_creat_cmd = "sc create HoudiniLicenseServer binPath= " + HLS_dst + " START= auto " + " DISPLAYNAME= HoudiniLicenseServer " + " TYPE= own "
    
    if len(HLS) > 5 and HLS.find("STATE"):
        print "the HoudiniLicenseServer is exist"
        HLS_stop_popen = subprocess.Popen(HLS_stop_cmd, stdout=subprocess.PIPE, shell=1)
        HLS_stop_popen.wait()
        time.sleep(5)
        shutil.copy(HLS_src, HLS_dst)
    else:
        print "the HoudiniLicenseServer is not  exist"
        shutil.copy(HLS_src, HLS_dst)
        HLS_creat_popen = subprocess.Popen(HLS_creat_cmd, stdout=subprocess.PIPE, shell=1)
        HLS_creat_popen.wait()
        time.sleep(3)
    
    #add by neil 2017-6-2 3pm
    HLS_start_popen = subprocess.Popen(HLS_creat_cmd, stdout=subprocess.PIPE, shell=1)
    HLS_start_popen.wait()
    time.sleep(3)
    #add by neil 2017-6-2 3pm
    
    HLS_start_popen = subprocess.Popen(HLS_start_cmd, stdout=subprocess.PIPE, shell=1)
    HLS_start_popen.wait()
    time.sleep(3)
    
    HS_strcmd = 'sc query HoudiniServer|findstr "STATE"'
    HS_popen = subprocess.Popen(HS_strcmd, stdout=subprocess.PIPE, shell=1)
    HS = HS_popen.stdout.read()
    HS_popen.wait()
    
    HS_src = os.path.join(r"b:\plugins\houdini\lic", houdini_vis, "hserver.exe")
    HS_dst = os.path.join("C:\Windows\System32", "hserver.exe")
    
    HS_stop_cmd = 'SC STOP "HoudiniServer"'
    HS_start_cmd = 'SC start "HoudiniServer"'
    HS_creat_cmd = "SC create HoudiniServer binPath= " + HS_dst + " START= auto " + " DISPLAYNAME= HoudiniServer " + " TYPE= own "
    HS_s_ip_cmd = HS_dst + " -S " + HS_ip
    
    if len(HS) > 5 and HS.find("STATE"):
        print "the HoudiniServer is exist"
        HS_stop_popen = subprocess.Popen(HS_stop_cmd, stdout=subprocess.PIPE, shell=1)
        HS_stop_popen.wait()
        time.sleep(10)
        shutil.copy(HS_src, HS_dst)
    else:
        print "the HoudiniServer is not  exist"
        shutil.copy(HS_src, HS_dst)
        HS_creat_popen = subprocess.Popen(HS_creat_cmd, stdout=subprocess.PIPE, shell=1)
        HS_creat_popen.wait()
        time.sleep(10)
    
    HS_start_popen = subprocess.Popen(HS_start_cmd, stdout=subprocess.PIPE, shell=1)
    print "HS_start_popen     " +  HS_start_popen.stdout.read()
    HS_start_popen.wait()
    time.sleep(15)
    
    HS_s_ip_cmd_popen = subprocess.Popen(HS_s_ip_cmd, stdout=subprocess.PIPE, shell=1)
    print "HS_s_ip_cmd_popen     " +  HS_s_ip_cmd_popen.stdout.read()
    HS_s_ip_cmd_popen.wait()
    time.sleep(15)
    os.system(HS_s_ip_cmd)
    time.sleep(15)
    #print "the houdini  hserver is 10.50.10.231"
if __name__ == '__main__':
    base_dir = os.path.abspath(sys.argv[1])
    print("\n"+base_dir)
    _info_file = "%s/temp/lic_info.json"%base_dir
    _plugin_info = {}
    if os.path.exists(_info_file):
        with open(_info_file,"r")as f:
            _plugin_info = json.load(f)
            f.close()

    hou_lic(_plugin_info["hver"],_plugin_info["server"])
    print("Server setup done")