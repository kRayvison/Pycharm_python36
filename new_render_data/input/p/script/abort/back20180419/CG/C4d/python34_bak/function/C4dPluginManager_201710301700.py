#!/usr/bin/python  
#coding=utf-8
#__author__:'kaname' QQ:1394041054

import os,sys,socket,subprocess,shutil

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
    
    def get_dll(self,soft_version):
        print '-----------start libmmd.dll---------------'
        dll_src = 'B:/plugins/C4D/libmmd'
        soft_src = os.path.join(r"C:\Program Files\MAXON", soft_version) 
        os.system('echo f | xcopy /y /e /f "%s" "%s"' % (dll_src, soft_src))
        print '-----------copy libmmd.dll done---------------'
        
        #if soft_version == "CINEMA 4D R18":
        #    src_path1 = r"B:\plugins\C4D\libmmd"
        #    dest_path1 = r"C:\Program Files\MAXON\CINEMA 4D R18\\"
        #    os.system('echo f | xcopy /f /y "%s" "%s"' % (src_path1, dest_path1))
        #if soft_version == "CINEMA 4D R17":
        #    src_path2 = r"B:\plugins\C4D\libmmd"
        #    dest_path2 = r"C:\Program Files\MAXON\CINEMA 4D R17\\"
        #    os.system('echo f | xcopy /f /y "%s" "%s"' % (src_path2, dest_path2))
        
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
        
        #plugin_name = plugin.plugin_name.lower()
        #print plugin_name
        
        if plugin.plugin_name == 'c4dtoa':
            # copy ai.dll&solidangle.lic
            c4d_installed_path = os.path.join(r"C:/Program Files/MAXON", \
                                            self.plugin.soft_version)
            
            ai_path  = plugin_c4d_path + r"\\ai.dll"
            lic_path = os.path.join(plugin_c4d_path, r"solidangle.lic")
            os.system('echo f | xcopy /f /y "%s" "%s"' % (ai_path, c4d_installed_path))
            os.system('echo f | xcopy /f /y "%s" "%s"' % (lic_path, c4d_installed_path))
            print 'c4dtoa...HL...plugin already done!!'

        elif plugin.plugin_name == 'gsg_hdri_studio_pack':
            print 'gsg_hdri_studio_pack'
            HDRI_Studio = plugin_c4d_path + r"\\*.*"
            HDRI_C4DPlugin = os.path.join(r"C:/Program Files/MAXON", \
                                        self.plugin.soft_version)
            os.system('echo f | xcopy /f /y /e "%s" "%s"' % (HDRI_Studio, HDRI_C4DPlugin))
            print 'gsg_hdri_studio_pack...HL...plugin already done!!'
            
        elif plugin.plugin_name == 'rollit':
            print 'Rollit'
            Rollit_path = plugin_c4d_path + r"\\*.*"
            print Rollit_path  + '====Rollit==='
            Rollit_C4DPlugin = os.path.join(r"C:/Program Files/MAXON", \
                                        self.plugin.soft_version)
            print Rollit_C4DPlugin + '.....Rollit....'
            os.system('echo f | xcopy /f /y /e "%s" "%s"' % (Rollit_path, Rollit_C4DPlugin))
            print 'rollit...HL...plugin already done!!'
            
        elif plugin.plugin_name == 'unfolder':
            print 'unfolder'
            unfolder_path = plugin_c4d_path
            print unfolder_path  + '===unfolder===='
            unfolder_C4DPlugin = os.path.join(r"C:/Program Files/MAXON", \
                                        self.plugin.soft_version)
            print unfolder_C4DPlugin + '...unfolder...'
            os.system('echo f | xcopy /f /y /e "%s" "%s"' % (unfolder_path, unfolder_C4DPlugin))
            print 'unfolder...HL...plugin already done!!'
        
        elif plugin.plugin_name == 'reeper':
            print 'reeper'
            reeper_path = plugin_c4d_path
            print reeper_path  + '===reeper===='
            reeper_C4DPlugin = os.path.join(r"C:\\Program Files\\MAXON", \
                                        self.plugin.soft_version)
            print reeper_C4DPlugin + '...reeper...'
            #os.system(r'start C:/fcopy/FastCopy.exe /force_close /cmd=sync "B:\plugins\C4D\reeper\reeper_2.02\CINEMA 4D R18\plugins\reeper\" /to="C:\Program Files\MAXON\CINEMA 4D R18\plugins\reeper"')
            #C:/fcopy/FastCopy.exe /force_close "B:\\plugins\\C4D\\reeper\\reeper_2.02\\CINEMA 4D R18\\" /to="C:\\Program Files\\MAXON\\CINEMA 4D R18"
            print (r'start C:/fcopy/FastCopy.exe /force_close "' + reeper_path + '\\" /to="' + reeper_C4DPlugin + '"')
            os.system (r'start C:/fcopy/FastCopy.exe /force_close "' + reeper_path + '\\" /to="' + reeper_C4DPlugin + '"')
            print 'reeper...HL...plugin already done!!'
            
        elif plugin.plugin_name == 'codevonc_depliage':
            print 'codevonc_depliage'
            codevonc_depliage_path = plugin_c4d_path
            print codevonc_depliage_path  + '===codevonc_depliage===='
            codevonc_depliage_C4DPlugin = os.path.join(r"C:\\Program Files\\MAXON", \
                                        self.plugin.soft_version)
            print codevonc_depliage_C4DPlugin + '...codevonc_depliage...'
            #os.system(r'start C:/fcopy/FastCopy.exe /force_close /cmd=sync "B:\plugins\C4D\codevonc_depliage\codevonc_depliage_1.3\CINEMA 4D R18\plugins\codevonc_depliage\" /to="C:\Program Files\MAXON\CINEMA 4D R18\plugins\codevonc_depliage"')
            print (r'start C:/fcopy/FastCopy.exe /force_close "' + codevonc_depliage_path + '\\" /to="' + codevonc_depliage_C4DPlugin + '"')
            os.system (r'start C:/fcopy/FastCopy.exe /force_close "' + codevonc_depliage_path + '\\" /to="' + codevonc_depliage_C4DPlugin + '"')
            print 'codevonc_depliage...HL...plugin already done!!'
            
        elif plugin.plugin_name == 'topcoat_pc':
            print 'topcoat_pc'
            TopCoat_PC_path = plugin_c4d_path + r"\\*.*"
            print TopCoat_PC_path + 'TopCoat_PC_path'
            TopCoat_PC_appdata = 'C:\Users\enfuzion\AppData\Roaming\MAXON\CINEMA 4D R18_62A5E681'
            print TopCoat_PC_appdata + 'TopCoat_PC_appdata'
            os.system('echo f | xcopy /f /y /e "%s" "%s"' % (TopCoat_PC_path, TopCoat_PC_appdata))
            print 'topcoat_pc...HL...plugin already done!!'
        
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
            print 'vray...HL...plugin already done!!'
            
        elif plugin.plugin_name == 'redshift_GPU':
            print 'redshift_GPU...'
            #1.kill lic
            os.system(r'wmic process where name="rlm_redshift.exe" delete')
            #2.copy lic
            #rd_lic_src = r'B:\plugins\C4D\redshift_GPU\redshift_rlm_server_win64'
            rd_lic_src = os.path.join(self.plugin_root, self.plugin.plugin_name, 'redshift_rlm_server_win64')

            rd_lic_dest = "C:/redshift_rlm_server_win64/"
            if os.path.exists(rd_lic_dest):
                try:
                    print "del path %s" % rd_lic_dest
                    shutil.rmtree(rd_lic_dest)
                except Exception as e:  
                    #print( Exception,":",error )
                    print(e)
                    print "dont del path %s" % rd_lic_dest
            
            os.system ('echo f | xcopy /f /y "%s" "%s"' % (rd_lic_src, rd_lic_dest))
            os.system(r'start C:\redshift_rlm_server_win64\rlm_redshift.exe')
            #3.doEnvSetup
            print ("...doEnvSetup...")
            rd_path = ';' + os.path.join(plugin_c4d_path + '\plugins\\') + ';'
            print rd_path + '-------redshift path----------'
            os.environ["C4D_PLUGINS_DIR"] = rd_path
            programData_src = os.path.join(self.plugin_root, \
                                        self.plugin.plugin_name, \
                                        self.plugin.plugin_name + '_' + self.plugin.plugin_version + '\Redshift\\')
            print programData_src + '--------programData_src---------'
            os.environ['PATH']= "$PATH;"+programData_src+"bin"
            os.environ['REDSHIFT_COREDATAPATH']= programData_src
            os.environ['REDSHIFT_LOCALDATAPATH']= programData_src
            os.environ['REDSHIFT_PREFSPATH']= programData_src
            os.environ['REDSHIFT_LICENSEPATH']= "5059@127.0.0.1"
            print("Env done!")
            print 'redshift_GPU...HL...plugin already done!!'
            
        elif plugin.plugin_name == 'octane_GPU':
            myname, myaddr = self.__check_gpu()
            if myname.startswith('GPU'):
                print '001-----------start remove MAXON and OctaneRender-----------'
                appdata_src_path = r'C:/Users/enfuzion/AppData/Roaming'
                if os.path.exists(appdata_src_path + '/MAXON/'):
                    shutil.rmtree(appdata_src_path + '/MAXON/')
                if os.path.exists(appdata_src_path + '/OctaneRender/'):
                    shutil.rmtree(appdata_src_path + '/OctaneRender/')
                    print '666666' + appdata_src_path
                    print '-----------remove done-----------'
                
                print '002-----------start remove RXX\plugins\c4doctane-----------'
                c4doctane_path = 'C:\Program Files\MAXON\CINEMA 4D R18\plugins\c4doctane'
                if os.path.isdir(c4doctane_path):
                    shutil.rmtree(c4doctane_path)
                else:
                    pass
                
                print '003----------start copy MAXON and OctaneRender------------'
                octane_b_path = os.path.join(plugin_c4d_path, myname)
                octane_src_path = octane_b_path
                print '111' + octane_src_path
                octane_dest_path = os.path.join(r'C:/Users/enfuzion/AppData/Roaming/')
                print '222' + octane_src_path, octane_dest_path
                os.system('echo f | xcopy /y /e /f "%s" "%s"' % (octane_src_path, octane_dest_path))
                print '-----------copy done---------------'
                print 'octane_GPU...HL...plugin already done!!'
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
            #w2-r18-CINEMA 4D 64 Bit.exe
            c4d_exe_path = r"B:\plugins\C4D\c4d_R18_exe\CINEMA 4D 64 Bit.exe"
            c4d_exec_dest_path = r'C:\Program Files\MAXON\CINEMA 4D R18\CINEMA 4D 64 Bit.exe'
            print '8888...' + c4d_exe_path, c4d_exec_dest_path
            print('copy "%s" "%s" ' % (c4d_exe_path, c4d_exec_dest_path))
            os.system('copy "%s" "%s" ' % (c4d_exe_path, c4d_exec_dest_path))


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

    plugin_mgr.get_dll(soft_version)
    
    plugin_mgr.set_custom_env(plugin1)

    #plugin2 = C4DPlugin()
    #plugin2.plugin_name      = "gsg_hdri_studio_pack"
    #plugin2.plugin_version   = "2.142"
    #plugin2.soft_version     = "CINEMA 4D R18"
    #plugin2.node             = "ABCDEF"
    #plugin_mgr.set_custom_env(plugin2)
    
    plugin_mgr.copy_R18_exe(soft_version)
    print ('...copy_R18_exe was done...')
    
    c4d_exec_path = '"C:/Program Files/MAXON/%s/CINEMA 4D 64 Bit.exe"' % (plugin1.soft_version)
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
