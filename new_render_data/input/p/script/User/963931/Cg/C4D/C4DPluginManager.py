#!/usr/bin/python  
#coding=utf-8
#__author__:'kaname' QQ:1394041054

import os,sys,socket,subprocess

class C4DPlugin(object): 
    #初始化对象, 读取json来得出这些参数
    def __init__(self): 
        self.plugin_name    = ""
        self.plugin_version = ""
        self.soft_version   = ""
        self.node           = 'ABCDEF'

class C4DPluginManagerCenter(object):
    def __init__(self, user_id):
        self.user_id     = user_id
        self.plugin_root = r"B:\plugins\C4D"
        self.plugin      = C4DPlugin()
        self.plugin_path = ''
        
    def set_custom_envs(self, plugin_list):
        pass
        
    def set_custom_env(self, plugin):
        self.plugin = plugin
        plugin_c4d_path = self.__get_c4d_path()
        c4d_library_path = self.__get_c4d_library_path()
        
        ###
        old_plugin_env = ''
        
        if os.environ.get('C4D_PLUGINS_DIR') is not None:
            old_plugin_env = os.environ["C4D_PLUGINS_DIR"] 
        
        self.plugin_path = self.__get_plugin_path()
        #print '================================' + self.plugin_path
        
        # 检查路径有效性
        os.environ["C4D_PLUGINS_DIR"] = old_plugin_env + ';' + self.plugin_path + ';' 
        print os.environ["C4D_PLUGINS_DIR"]

        ###
        old_library_env = ''
        if os.environ.get('C4D_BROWSERLIBS') is not None:
            old_library_env = os.environ["C4D_BROWSERLIBS"]
            
        library_path = self.__get_c4d_library_path()
        # 检查路径有效性
        os.environ["C4D_BROWSERLIBS"] = old_library_env + ';' + library_path + ';' 
        print os.environ["C4D_BROWSERLIBS"]
        
        if plugin.plugin_name == 'c4dtoa':
            # copy ai.dll&solidangle.lic
            c4d_installed_path = os.path.join(r"C:/Program Files/MAXON", \
                                            self.plugin.soft_version) 
            
            ai_path  = plugin_c4d_path + r"\\ai.dll"
            lic_path = os.path.join(plugin_c4d_path, r"solidangle.lic")
            arnold_path = plugin_c4d_path + r"\\*.*"
            os.system('echo f | xcopy /f /y "%s" "%s"' % (ai_path, c4d_installed_path))
            os.system('echo f | xcopy /f /y "%s" "%s"' % (lic_path, c4d_installed_path))
            os.system('echo f | xcopy /f /y /e "%s" "%s"' % (arnold_path, c4d_installed_path))
            

        elif plugin.plugin_name == 'vray':
            # copy VrayBridge.key
            vray_installed_path = os.path.join(r"C:/Program Files/MAXON", \
                                            self.plugin.soft_version) 
                                            
            # 这里判断node 匹配出key，例如：VrayBridge.key.ABCDEFGHJ  w2一个镜像无需匹配，w5现在只用ABCDEF即可
             
            vray_key_path = os.path.join(plugin_c4d_path, r'vray_key', self.plugin.node, r"VrayBridge.key")
            print vray_key_path
            vray_key_dest_path = os.path.join(vray_installed_path, r"VrayBridge.key")
            print vray_key_dest_path
            os.system('echo f | xcopy /f /y "%s" "%s"' % (vray_key_path,  vray_key_dest_path))
            
        elif plugin.plugin_name == 'octane_GPU':
            #copy bak file
            myname, myaddr = self.__check_gpu()
            if myname.startswith('GPU'):
                octane_b_path = os.path.join(plugin_c4d_path, myname)
                octane_src_path = octane_b_path
                print '111' + octane_src_path
                octane_dest_path = os.path.join(r'C:/Users/enfuzion/AppData/Roaming/')
                print '222' + octane_src_path, octane_dest_path
                os.system('echo f | xcopy /y /e /f "%s" "%s"' % (octane_src_path, octane_dest_path))
            else:
                return False
        else:
            pass
            
        return True
    
    
    def __get_plugin_path(self):
        plugin_full_path =  os.path.join(self.plugin_root, \
                                        self.plugin.plugin_name, \
                                        self.plugin.plugin_name + '_' + self.plugin.plugin_version, \
                                        self.plugin.soft_version, r'plugins')
        return plugin_full_path
        
        
    def __get_c4d_path(self):
        plugin_c4d_path =  os.path.join(self.plugin_root, \
                                        self.plugin.plugin_name, \
                                        self.plugin.plugin_name + '_' + self.plugin.plugin_version, \
                                        self.plugin.soft_version)
        return plugin_c4d_path
        

    def __get_c4d_library_path(self):
        c4d_library_path =  os.path.join(self.__get_c4d_path(),r"library\browser")
        return c4d_library_path
        
        
    def __check_gpu(self):
        myname = socket.getfqdn(socket.gethostname(  ))
        myaddr = socket.gethostbyname(myname)
        return myname, myaddr
    
    def copy_R18_exe(self,soft_version):
        if soft_version == "CINEMA 4D R18":
            src_path = r"B:\plugins\C4D\hot4d\fftwdll"
            dest_path = r"C:\Program Files\MAXON\CINEMA 4D R18\\"
            os.system('echo f | xcopy /f /y "%s" "%s"' % (src_path, dest_path))
            
            if not os.path.exists(r"C:\Program Files\MAXON\CINEMA 4D R18\CINEMA 4D 64 Bit.exe"):
                c4d_exe_path = r"B:\plugins\C4D\c4d_R18_exe\CINEMA 4D 64 Bit.exe"
                c4d_exec_dest_path = 'C:\Program Files\MAXON\CINEMA 4D R18\\'
                print '8888' + c4d_exe_path, c4d_exec_dest_path
                os.system('xcopy /f /v /y /i "%s" "%s" ' % (c4d_exe_path, c4d_exec_dest_path))
                
               
if __name__ == "__main__":
    plugin_name    = sys.argv[1]
    plugin_version = sys.argv[2]
    soft_version   = sys.argv[3]
    node           = sys.argv[4]
    
    print plugin_name,plugin_version,soft_version,node

    plugin_mgr = C4DPluginManagerCenter('100000')
    plugin1 = C4DPlugin()
    plugin1.plugin_name      = plugin_name
    plugin1.plugin_version   = plugin_version
    plugin1.soft_version     = soft_version
    plugin1.node             = node 

    plugin_mgr.set_custom_env(plugin1)
    
    plugin2 = C4DPlugin()
    plugin2.plugin_name      = "gsg_hdri_studio_pack"
    plugin2.plugin_version   = "2.142"
    plugin2.soft_version     = "CINEMA 4D R17"
    plugin2.node             = "ABCDEF" 
    plugin_mgr.set_custom_env(plugin2)
    
    plugin_mgr.copy_R18_exe(soft_version)
    print ('...copy_R18_exe was done...')

    c4d_exec_path = '"C:\Program Files\MAXON\%s\CINEMA 4D 64 Bit.exe"' % (plugin2.soft_version)
    print '9999' + c4d_exec_path
    os.system (os.path.normpath(c4d_exec_path))
    print 'done!!!'
    
    
###test  -noopengl -nogui
'''
if __name__ == "__main__":
    soft_ver  = 'R16'
    plugin_mgr = C4DPluginManagerCenter("100001")
    plugin = C4DPlugin("c4dtoa", "1.0.14.1", 'CINEMA 4D', soft_ver)
    plugin_mgr.set_custom_env(plugin)
    c4d_exec_path = '"C:/Program Files/MAXON/CINEMA 4D %s/CINEMA 4D 64 Bit.exe" ' % (soft_ver)
    os.system(os.path.normpath(c4d_exec_path))
'''
#test:
# "C4DPluginManager.py" "CINEMA 4D R17" "c4depot_real_sky_studio" "1.11" "ABCDEF"

#C4D_PLUGINS_DIR
#B:\plugins\C4D\vray\vray_1.9\CINEMA 4D R17\plugins;B:\plugins\C4D\c4dtoa\c4dtoa_1.6.2.0\CINEMA 4D R17\plugins;B:\plugins\C4D\realflow\realflow_2015\CINEMA 4D R17\plugins;

#C4D_BROWSERLIBS
#B:\plugins\C4D\gsg_hdri_studio_pack\gsg_hdri_studio_pack_2.0\CINEMA 4D R17\library\browser;B:\plugins\C4D\c4dtoa\c4dtoa_1.4.0.0\CINEMA 4D R17\library\browser;

#B:\plugins\C4D\vray\vray_1.9\CINEMA 4D R17\VrayBridge.key 
#B:\plugins\C4D\c4dtoa\c4dtoa_1.0.14.1\CINEMA 4D R17\ai.dll
#B:\plugins\C4D\c4dtoa\c4dtoa_1.0.14.1\CINEMA 4D R17\solidangle.lic




