#!/usr/bin/python  
# -*- coding=utf-8 -*-
# Author: kaname
# QQ: 1394041054
#Update:2018-07-23

import os,sys,subprocess,shutil,time,socket

class C4dPlugin(object): 
    #初始化对象, 读取json来得出这些参数
    def __init__(self):
        if not os.path.exists("c:/c4d"):
            os.mkdir("c:/c4d")
        sys.stdout = open('c:/c4d/@KANADA-C4dPluginManager.log', 'w')
        self.plugin_name    = ''
        self.plugin_version = ''
        self.soft_version   = ''
        self.node           = 'ABCDEF'

class C4dPluginMgr(object):
    def __init__(self, user_id, plugin_path):
        sys.stdout.flush()
        self.user_id     = user_id
        self.plugin_root = plugin_path
        self.plugin      = C4dPlugin()
        self.plugin_full_path = ''
        self.maxon_data_path = r'C:\users\enfuzion\AppData\Roaming\MAXON\CINEMA 4D %s\plugins'
        self.c4d_pyp_config = {
            'CINEMA 4D R13' : 'R13_05DFD2A0',
            'CINEMA 4D R14' : 'R14_4A9E4467',
            'CINEMA 4D R15' : 'R15_53857526',
            'CINEMA 4D R16' : 'R16_14AF56B1',
            'CINEMA 4D R17' : 'R17_8DE13DAD',
            'CINEMA 4D R18' : 'R18_62A5E681',
            'CINEMA 4D R19' : 'R19_BFE04C39'
        }
        
    def set_custom_envs(self, plugin_list):
        pass

    def get_dll(self,soft_version):
        print ('[-----------start libmmd.dll---------------]')
        dll_src = r'B:\\plugins\\C4D\\libmmd\\'
        soft_src = os.path.join(r"C:\\Program Files\\MAXON\\", soft_version)
        print (r'C:/fcopy/FastCopy.exe /force_close "' + dll_src + '" /to="' + soft_src + '"')
        os.system (r'C:/fcopy/FastCopy.exe /force_close "' + dll_src + '" /to="' + soft_src + '"')
        print ('[--copy libmmd.dll done--]')
        # This is different bewteen GPU platform....
        if soft_version == 'CINEMA 4D R19':
            print('[-----------CINEMA 4D R19.053 start copy-----------]')
            r19053 = r'B:\\plugins\\C4D\\MAXON\\CINEMA 4D R19.053\\'
            c_soft = r'C:\Program Files\MAXON\CINEMA 4D R19'
            print (r'C:/fcopy/FastCopy.exe /force_start /estimate /cmd=sync /force_close "' + r19053 + '" /to="' + c_soft + '"')
            os.system (r'C:/fcopy/FastCopy.exe /force_start /estimate /cmd=sync /force_close "' + r19053 + '" /to="' + c_soft + '"')
            print ('[--CINEMA 4D R19.053 copy done--]')
        
        
    def set_custom_env(self, plugin):
        self.plugin = plugin
        plugin_c4d_path = self.__get_c4d_path()
        c4d_library_path = self.__get_c4d_library_path()
        print(plugin_c4d_path, c4d_library_path)
        appdata_path =  self.maxon_data_path % (self.c4d_pyp_config.get(self.plugin.soft_version))
        
        ### C4D_PLUGINS_DIR
        old_plugin_env = ''
        
        if os.environ.get('C4D_PLUGINS_DIR') is not None:
            old_plugin_env = os.environ["C4D_PLUGINS_DIR"] 
        
        self.plugin_full_path = self.__get_plugin_path()
        print('[@KANADA.self.plugin_full_path: ]'+ self.plugin_full_path)
        self.maxon_install = os.path.join(self.__maxon_install_path() + '\plugins')
        print('[@KANADA.self.maxon_install: ]'+ self.maxon_install)
        
        #20180710update
        #renderer_plugin = ['c4dtoa','vray','redshift','octane']
        os.environ["C4D_PLUGINS_DIR"] = old_plugin_env + ';' + self.plugin_full_path + ';'
        print(os.environ["C4D_PLUGINS_DIR"])
        
        if plugin.plugin_name == 'c4dtoa': # if c4dtoa, set env to C_pan
            os.environ["C4D_PLUGINS_DIR"] = old_plugin_env + ';' + self.maxon_install + ';'
            print('C4D_PLUGINS_DIR: ' + os.environ["C4D_PLUGINS_DIR"])
        else:
            os.environ["C4D_PLUGINS_DIR"] = old_plugin_env + ';' + self.plugin_full_path + ';' 
            print('C4D_PLUGINS_DIR: ' + os.environ["C4D_PLUGINS_DIR"])
        
        # =======================================================================================================
        ### C4D_BROWSERLIBS
        old_library_env = ''
        if os.environ.get('C4D_BROWSERLIBS') is not None:
            old_library_env = os.environ["C4D_BROWSERLIBS"]
            print ('old_library_env: ' + old_library_env)
        library_path = self.__get_c4d_library_path()
        c_pan_library_path = self.__get_new_library_path()
        print ('c_pan_library_path: ' + c_pan_library_path)
        os.environ["C4D_BROWSERLIBS"] = old_library_env + ';' + library_path + ';'
        print('C4D_BROWSERLIBS: ' + os.environ["C4D_BROWSERLIBS"])
        
        if plugin.plugin_name == 'c4dtoa': # if c4dtoa, set env to C_pan
            os.environ["C4D_BROWSERLIBS"] = old_library_env + ';' + c_pan_library_path + ';'
            print(os.environ["C4D_BROWSERLIBS"])
        else:
            os.environ["C4D_BROWSERLIBS"] = old_library_env + ';' + library_path + ';'
            print(os.environ["C4D_BROWSERLIBS"])

        
        
        '''#ai.dll 破解版
        # if plugin.plugin_name == 'c4dtoa':
        #     os.environ["C4D_BROWSERLIBS"] = old_library_env + ';' + c_pan_library_path + ';' 
        #     print(os.environ["C4D_BROWSERLIBS"])
        # else:
        #     os.environ["C4D_BROWSERLIBS"] = old_library_env + ';' + library_path + ';' 
        #     print(os.environ["C4D_BROWSERLIBS"])
        
        #sys.stdout.flush()

        #plugin_name = plugin.plugin_name.lower()
        #print plugin_name
        
        # About special plugin set env start
        # including(16): 1-5(c4dtoa, vray,redshift,octane,gsg_hdri_studio_pack,)
        #            6-10(trypogen,realflow,rollit,unfolder,reeper,codevonc_depliage,)
        #            11-15(Light_kit_infinite_free,cv_vrcam,meshboolean,transform,topcoat_pc,)
        
        #ai.dll 破解版
        # if plugin.plugin_name == 'c4dtoa':
        #     #if plugin.plugin_version == 'c4dtoa_2.2.2.1':
        #     #if self.plugin.soft_version == "CINEMA 4D R19":
        #     print( '!!! C4dtoa2.2 later is special set !!! \n')
        #     software_root = os.path.join(r'C:/Program Files/MAXON/' + self.plugin.soft_version)
        #     print (software_root)
        #     if os.path.exists(software_root):
        #         c4dtoa = r'C:/Program Files/MAXON/' + self.plugin.soft_version + '/plugins/C4DtoA'
        #         print (c4dtoa + '@KANADA_remove c4dtoa done')
        #         if os.path.exists(c4dtoa):
        #             shutil.rmtree(c4dtoa)
        #             time.sleep(10)
        #         #B:\plugins\C4D\c4dtoa\c4dtoa_2.1.2\CINEMA 4D R18
        #         c4dtoa_src = os.path.join(self.plugin_root, \
        #                                    r'plugins\C4D', \
        #                                 self.plugin.plugin_name, \
        #                                 self.plugin.plugin_name + '_' + self.plugin.plugin_version + '/' + self.plugin.soft_version + '/plugins/C4DtoA/')
        #         print (c4dtoa_src + '@KANADA-c4dtoa_src')
        #         #c4dtoa_dest = r"C:\Program Files\MAXON\CINEMA 4D R19\\"
        #         c4dtoa_dest = r"C:\Program Files\MAXON/" + self.plugin.soft_version + '\\plugins\\C4DtoA'
        #         print (c4dtoa_dest + '@KANADA-c4dtoa_dest')
        #         print (r'C:/fcopy/FastCopy.exe /force_close "' + c4dtoa_src + '" /to="' + c4dtoa_dest + '"')
        #         os.system (r'C:/fcopy/FastCopy.exe /force_close "' + c4dtoa_src + '" /to="' + c4dtoa_dest + '"')
        #         print ('[...copy c4dtoa for R19..]')

        #     # copy ai.dll&solidangle.lic
        #     c4d_installed_path = os.path.join(r"C:/Program Files/MAXON", \
        #                                     self.plugin.soft_version)
            
        #     ai_path  = plugin_c4d_path + r"\\ai.dll"
        #     lic_path = os.path.join(plugin_c4d_path, r"solidangle.lic")
        #     arnold_lic = os.path.join(plugin_c4d_path, r"arnold.lic")
            
        #     os.system('echo f | xcopy /f /y "%s" "%s"' % (ai_path, c4d_installed_path))
        #     os.system('echo f | xcopy /f /y "%s" "%s"' % (lic_path, c4d_installed_path))
        #     os.system('echo f | xcopy /f /y "%s" "%s"' % (arnold_lic, c4d_installed_path))
        #     print ('[c4dtoa...plugin already done!!]')'''
        

        # rlm.exe 服务型版本
        if plugin.plugin_name == 'c4dtoa':
            print ('c4dtoa config...')
            #1.kill lic
            os.system(r'wmic process where name="rlm.exe" delete')
            os.system(r'wmic process where name="rlm_c4dtoa.exe" delete')
            
            #2.copy lic
            #rd_lic_src = r'B:\plugins\C4D\c4dtoa\AMPED' to 'c:\AMPED'
            rlm_src = os.path.join(self.plugin_root, r'plugins\C4D', self.plugin.plugin_name, 'AMPED')
            print (rlm_src + ' @KANADA_amped_src')
            rlm_dest = r"C:\\"
            if os.path.exists(rlm_dest):
                print ('888888')
                try:
                    print ("del path %s" % rlm_dest)
                    shutil.rmtree(rlm_dest)
                except Exception as e:  
                    #print( Exception,":",error )
                    print (e)
                    print ("dont del path %s" % rlm_dest)
            print (r'C:/fcopy/FastCopy.exe /speed=full /force_close /force_start "' + rlm_src + '" /to="' + rlm_dest + '"')
            os.system (r'C:/fcopy/FastCopy.exe /speed=full /force_close /force_start "' + rlm_src + '" /to="' + rlm_dest + '"')
            print ('[rlm copy done...]')
            
            #3.doEnvSetup(new) B pan to C pan
            print( '!!! C4dtoa is using officially now !!! \n')
            # delte old
            software_root = os.path.join(r'C:/Program Files/MAXON/' + self.plugin.soft_version)
            print (software_root)
            if os.path.exists(software_root):
                c4dtoa = r'C:/Program Files/MAXON/' + self.plugin.soft_version + '/plugins/C4DtoA'
                print (c4dtoa + ' @KANADA_remove c4dtoa done')
                if os.path.exists(c4dtoa):
                    try:
                        os.system('rmdir /s /q "%s"' % c4dtoa)
                        print(3333333)
                        os.mkdir(c4dtoa)
                    except:
                        pass
                else:
                    os.mkdir(c4dtoa)
                    time.sleep(10)
                # copy new  B to C #B:\plugins\C4D\c4dtoa\2.2.0\CINEMA 4D R18
                c4dtoa_src = os.path.join(self.plugin_root, \
                                        r'plugins\C4D', \
                                        self.plugin.plugin_name, \
                                        self.plugin.plugin_version + '/' + self.plugin.soft_version + '/plugins/C4DtoA/')
                print ('c4dtoa_src: ' + c4dtoa_src)
                c4dtoa_dest = "C:\\Program Files\\MAXON\\" + self.plugin.soft_version + '\\plugins\\C4DtoA'
                print ('c4dtoa_dest: ' + c4dtoa_dest)
                if not os.path.exists(c4dtoa_src):
                    print('This version is not exists!!! \n')
                    return False
                else:
                    print (r'C:/fcopy/FastCopy.exe /speed=full /force_close /no_confirm_stop /force_start "' + c4dtoa_src + '" /to="' + c4dtoa_dest + '"')
                    os.system (r'C:/fcopy/FastCopy.exe /speed=full /force_close /no_confirm_stop /force_start "' + c4dtoa_src + '" /to="' + c4dtoa_dest + '"')
                    print('c4dtoa to c copy done.....')
                # run rlm
                os.environ['solidangle_LICENSE'] = r"5059@localhost"
                #os.environ['PATH'] = '$PATH;'+c4dtoa_dest+r'/arnold/bin'
                os.system(r'start C:\AMPED\rlm.exe')
                print("@KANADA Arnold Env done!")

        elif plugin.plugin_name == 'vray':
            # del Old_vray
            print( '!!! del Old_vray !!! \n')
            software_root = os.path.join(r'C:/Program Files/MAXON/' + self.plugin.soft_version)
            print (software_root)
            if os.path.exists(software_root):
                vray = r'C:/Program Files/MAXON/' + self.plugin.soft_version + '/plugins/VrayBridge'
                print (vray + '@KANADA_remove vray done')
                if os.path.exists(vray):
                    shutil.rmtree(vray)
                    time.sleep(10)
            # copy VrayBridge.key
            vray_installed_path = os.path.join(r"C:/Program Files/MAXON", \
                                            self.plugin.soft_version) 
                                            
            # 这里判断node 匹配出key，例如：VrayBridge.key.ABCDEFGHJ  w2一个镜像无需匹配，w5现在只用ABCDEF即可
             
            vray_key_path = os.path.join(plugin_c4d_path, r'vray_key', self.plugin.node, r"VrayBridge.key")
            print (vray_key_path)
            vray_key_dest_path = os.path.join(vray_installed_path, r"VrayBridge.key")
            print (vray_key_dest_path)
            os.system('echo f | xcopy /f /y "%s" "%s"' % (vray_key_path,  vray_key_dest_path))
            print ('vray...plugin already done!!')
            
        elif plugin.plugin_name == 'redshift':
            print ('redshift...')
            #1.kill lic
            os.system(r'wmic process where name="rlm_redshift.exe" delete')
            #2.copy lic
            #rd_lic_src = r'B:\plugins\C4D\redshift\redshift_rlm_server_win64'
            rd_lic_src = os.path.join(self.plugin_root, 'plugins\C4D', self.plugin.plugin_name, 'redshift_rlm_server_win64')
            print('rd_lic_src: ' + rd_lic_src)
            rd_lic_dest = "C:/redshift_rlm_server_win64/"
            if os.path.exists(rd_lic_dest):
                try:
                    print ("del path %s" % rd_lic_dest)
                    shutil.rmtree(rd_lic_dest)
                except Exception as e:  
                    #print( Exception,":",error )
                    print (e)
                    print ("dont del path %s" % rd_lic_dest)
            
            os.system ('echo f | xcopy /f /y "%s" "%s"' % (rd_lic_src, rd_lic_dest))
            os.system(r'start C:\redshift_rlm_server_win64\rlm_redshift.exe')
            #3.doEnvSetup
            print ("[...doEnvSetup...]")
            rd_path = ';' + os.path.join(plugin_c4d_path + '\plugins\\') + ';'
            print (rd_path + '-------redshift path----------')
            os.environ["C4D_PLUGINS_DIR"] = rd_path
            programData_src = os.path.join(self.plugin_root, \
                                           'plugins\C4D', \
                                        self.plugin.plugin_name, \
                                        self.plugin.plugin_name + '_' + self.plugin.plugin_version + '\Redshift\\')
            print (programData_src + '--------programData_src---------')
            REDSHIFT_LOCALDATAPATH = r'D:/temp/REDSHIFT_C4D/CACHE'
            if not os.path.exists(REDSHIFT_LOCALDATAPATH):
                os.makedirs(REDSHIFT_LOCALDATAPATH)
                
            os.environ['REDSHIFT_LOCALDATAPATH']= REDSHIFT_LOCALDATAPATH
            os.environ['LOCALAPPDATA'] = REDSHIFT_LOCALDATAPATH
            os.environ['PATH']= "$PATH;"+programData_src+"bin"
            os.environ['REDSHIFT_COREDATAPATH']= programData_src
            
            os.environ['REDSHIFT_PREFSPATH']= programData_src
            os.environ['REDSHIFT_LICENSEPATH']= "C:/redshift_rlm_server_win64/redshift-core2.lic"
            os.environ['REDSHIFT_LICENSE']= "5059@127.0.0.1"
            print("[Env done!]")
            print ('[redshift...plugin already done!!]')

        elif plugin.plugin_name == 'octane':
            myname, myaddr = self.__check_gpu()
            if myname.startswith('GPU'):
                print ('001-----------start remove MAXON and OctaneRender-----------')
                appdata_src_path = r'C:/Users/enfuzion/AppData/Roaming'
                if os.path.exists(appdata_src_path + '/MAXON/'):
                    shutil.rmtree(appdata_src_path + '/MAXON/')
                if os.path.exists(appdata_src_path + '/OctaneRender/'):
                    shutil.rmtree(appdata_src_path + '/OctaneRender/')
                    print('666666' + appdata_src_path)
                    print ('-----------remove done-----------')
                
                print ('002-----------start remove RXX\plugins\c4doctane-----------')
                c4doctane_path = r'C:/Program Files/MAXON/CINEMA 4D R18/plugins/c4doctane'
                if os.path.isdir(c4doctane_path):
                    shutil.rmtree(c4doctane_path)
                else:
                    pass
                
                print ('003----------start copy MAXON and OctaneRender------------')
                octane_b_path = os.path.join(plugin_c4d_path, myname)
                octane_src_path = octane_b_path
                print('111' + octane_src_path)
                octane_dest_path = os.path.join(r'C:/Users/enfuzion/AppData/Roaming/')
                print('222' + octane_src_path, octane_dest_path)
                os.system('echo f | xcopy /y /e /f "%s" "%s"' % (octane_src_path, octane_dest_path))
                print ('-----------copy done---------------')
                print ('octane...plugin already done!!')
        
        elif plugin.plugin_name == 'trypogen':
            print ('[trypogen ]') # .pypv
            appdata_path =  self.maxon_data_path % (self.c4d_pyp_config.get(self.plugin.soft_version))
            print(appdata_path + ' aaaaaaaaaaaa')
            if os.path.exists(appdata_path):
                try:
                    os.system('rmdir /s /q "%s"' % appdata_path)
                    os.mkdir(appdata_path)
                except:
                    pass
            else:
                os.mkdir(appdata_path)
            trypogen_Studio = plugin_c4d_path + r"/plugins/*.*"
            c4d_appdata = appdata_path + '\\'
            print ('echo f | xcopy /f /y /e "%s" "%s"' % (trypogen_Studio, c4d_appdata))
            os.system('echo f | xcopy /f /y /e "%s" "%s"' % (trypogen_Studio, c4d_appdata))
            print ('[trypogen...plugin already done!!]')

        #20180712update
        elif plugin.plugin_name == 'realflow':
            print('realflow....')
            b_rf_lic = os.path.join(self.plugin_root, \
                                        r'\plugins\C4D', \
                                        self.plugin.plugin_name, \
                                        self.plugin.plugin_name + '_' + self.plugin.plugin_version + '/realflow_cinema4d')
            print (b_rf_lic + ' @KANADA-b_rf_lic')
            dest_rf_lic = r'C:\\Users\\enfuzion\\Documents\\'
            dest_lic = r'C:\\Users\\enfuzion\\Documents\\realflow_cinema4d\\'
            if os.path.exists(dest_lic):
                shutil.rmtree(dest_lic)
                time.sleep(5)
            print (r'C:/fcopy/FastCopy.exe /force_close "' + b_rf_lic + '" /to="' + dest_rf_lic + '"')
            os.system (r'C:/fcopy/FastCopy.exe /force_close "' + b_rf_lic + '" /to="' + dest_rf_lic + '"')
            print ('[realflow...plugin already done!!]')
            
        #20180530——update
        elif plugin.plugin_name == 'gsg_hdri_studio_pack':
            print ('[gsg_hdri_studio_pack]')
            # install here “Preferences/MAXON/CINEMA 4D/plugins/“
            # 判断下软件版本，同一个插件板本存在一份packs，拷贝到不同软件版本下

            # 1.delete “Preferences/MAXON/CINEMA 4D/plugins/“
            # 2.需拷贝的
            appdata_path =  self.maxon_data_path % (self.c4d_pyp_config.get(self.plugin.soft_version))
            appdata_hdri_browser = self.maxon_data_path % (self.c4d_pyp_config.get(self.plugin.soft_version)) + '\\HDRI Browser'
            appdata_hdri_studio = self.maxon_data_path % (self.c4d_pyp_config.get(self.plugin.soft_version)) + '\\HDRI Studio Rig'
            print(appdata_path + ' aaaaaaaaaaaa')
            
            if os.path.exists(appdata_path):
                #shutil.rmtree(appdata_path)
                try:
                    os.system('rmdir /s /q "%s"' % appdata_path)
                    os.mkdir(appdata_path)
                except:
                    pass
            else:
                os.mkdir(appdata_path)

            HDRI_Studio = plugin_c4d_path + r"/plugins/*.*"
            HDRI_C4DPlugin = os.path.join(r"C:/Program Files/MAXON", \
                                        self.plugin.soft_version)

            #c4d_appdata = os.path.join(r'C:/Users/enfuzion/AppData/Roaming/MAXON/CINEMA 4D R19_BFE04C39/plugins')
            c4d_appdata = appdata_path + '\\'
            #os.system('echo f | xcopy /f /y /e "%s" "%s"' % (HDRI_Studio, HDRI_C4DPlugin))
            print ('echo f | xcopy /f /y /e "%s" "%s"' % (HDRI_Studio, c4d_appdata))
            os.system('echo f | xcopy /f /y /e "%s" "%s"' % (HDRI_Studio, c4d_appdata))
            print ('[gsg_hdri_studio_pack...plugin already done!!]')
            
        elif plugin.plugin_name == 'rollit':
            print ('Rollit')
            Rollit_path = plugin_c4d_path + r"\\*.*"
            print (Rollit_path  + '====Rollit===')
            Rollit_C4DPlugin = os.path.join(r"C:/Program Files/MAXON", \
                                        self.plugin.soft_version)
            print (Rollit_C4DPlugin + '.....Rollit....')
            os.system('echo f | xcopy /f /y /e "%s" "%s"' % (Rollit_path, Rollit_C4DPlugin))
            print ('rollit...plugin already done!!')
            
        elif plugin.plugin_name == 'unfolder':
            print ('unfolder')
            unfolder_path = plugin_c4d_path
            print (unfolder_path  + '===unfolder====')
            unfolder_C4DPlugin = os.path.join(r"C:/Program Files/MAXON", \
                                        self.plugin.soft_version)
            print (unfolder_C4DPlugin + '...unfolder...')
            os.system('echo f | xcopy /f /y /e "%s" "%s"' % (unfolder_path, unfolder_C4DPlugin))
            print ('unfolder...plugin already done!!')
        
        elif plugin.plugin_name == 'reeper':
            print ('reeper')
            reeper_path = plugin_c4d_path
            print (reeper_path  + '===reeper====')
            reeper_C4DPlugin = os.path.join(r"C:\\Program Files\\MAXON", \
                                        self.plugin.soft_version)
            print(reeper_C4DPlugin + '...reeper...')
            #os.system(r'start C:/fcopy/FastCopy.exe /force_close /cmd=sync "B:\plugins\C4D\reeper\reeper_2.02\CINEMA 4D R18\plugins\reeper\" /to="C:\Program Files\MAXON\CINEMA 4D R18\plugins\reeper"')
            #C:/fcopy/FastCopy.exe /force_close "B:\\plugins\\C4D\\reeper\\reeper_2.02\\CINEMA 4D R18\\" /to="C:\\Program Files\\MAXON\\CINEMA 4D R18"
            print(r'start C:/fcopy/FastCopy.exe /force_close "' + reeper_path + '\\" /to="' + reeper_C4DPlugin + '"')
            os.system (r'start C:/fcopy/FastCopy.exe /force_close "' + reeper_path + '\\" /to="' + reeper_C4DPlugin + '"')
            print ('reeper...plugin already done!!')
            
        elif plugin.plugin_name == 'codevonc_depliage':
            print ('codevonc_depliage')
            codevonc_depliage_path = plugin_c4d_path
            print (codevonc_depliage_path  + '===codevonc_depliage====')
            codevonc_depliage_C4DPlugin = os.path.join(r"C:\\Program Files\\MAXON", \
                                        self.plugin.soft_version)
            print (codevonc_depliage_C4DPlugin + '...codevonc_depliage...')
            #os.system(r'start C:/fcopy/FastCopy.exe /force_close /cmd=sync "B:\plugins\C4D\codevonc_depliage\codevonc_depliage_1.3\CINEMA 4D R18\plugins\codevonc_depliage\" /to="C:\Program Files\MAXON\CINEMA 4D R18\plugins\codevonc_depliage"')
            print (r'start C:/fcopy/FastCopy.exe /force_close "' + codevonc_depliage_path + '\\" /to="' + codevonc_depliage_C4DPlugin + '"')
            os.system (r'start C:/fcopy/FastCopy.exe /force_close "' + codevonc_depliage_path + '\\" /to="' + codevonc_depliage_C4DPlugin + '"')
            print ('codevonc_depliage...plugin already done!!')
            
        elif plugin.plugin_name == 'cv_vrcam':
            print ('cv_vrcam')
            codevonc_depliage_path = plugin_c4d_path
            print (codevonc_depliage_path  + '===cv_vrcam====')
            codevonc_depliage_C4DPlugin = os.path.join(r"C:\\Program Files\\MAXON", \
                                        self.plugin.soft_version)
            print (codevonc_depliage_C4DPlugin + '...cv_vrcam...')
            print (r'start C:/fcopy/FastCopy.exe /force_close "' + codevonc_depliage_path + '\\" /to="' + codevonc_depliage_C4DPlugin + '"')
            os.system (r'start C:/fcopy/FastCopy.exe /force_close "' + codevonc_depliage_path + '\\" /to="' + codevonc_depliage_C4DPlugin + '"')
            print ('[cv_vrcam...plugin already done!!]')
        
        elif plugin.plugin_name == 'meshboolean':
            print ('meshboolean')
            meshboolean_path = plugin_c4d_path
            print (meshboolean_path  + '===meshboolean====')
            print (r'start C:/fcopy/FastCopy.exe /force_close "' + meshboolean_path + '\\" /to="' + appdata_path + '"')
            os.system (r'start C:/fcopy/FastCopy.exe /force_close "' + meshboolean_path + '\\" /to="' + appdata_path + '"')
            print ('[meshboolean...plugin already done!!]')
            
        elif plugin.plugin_name == 'transform':
            print ('transform')
            codevonc_depliage_path = plugin_c4d_path
            print (codevonc_depliage_path  + '===transform====')
            codevonc_depliage_C4DPlugin = os.path.join(r"C:\\Program Files\\MAXON", \
                                        self.plugin.soft_version)
            print (codevonc_depliage_C4DPlugin + '...transform...')
            print (r'start C:/fcopy/FastCopy.exe /force_close "' + codevonc_depliage_path + '\\" /to="' + codevonc_depliage_C4DPlugin + '"')
            os.system (r'start C:/fcopy/FastCopy.exe /force_close "' + codevonc_depliage_path + '\\" /to="' + codevonc_depliage_C4DPlugin + '"')
            print ('[transform...plugin already done!!]')
            
        elif plugin.plugin_name == 'topcoat_pc':
            print ('topcoat_pc')
            TopCoat_PC_path = plugin_c4d_path + r"\\*.*"
            print (TopCoat_PC_path + 'TopCoat_PC_path')
            TopCoat_PC_appdata = r'C:\Users\enfuzion\AppData\Roaming\MAXON\CINEMA 4D R18_62A5E681'
            print (TopCoat_PC_appdata + 'TopCoat_PC_appdata')
            os.system('echo f | xcopy /f /y /e "%s" "%s"' % (TopCoat_PC_path, TopCoat_PC_appdata))
            print ('topcoat_pc...plugin already done!!')
            
        elif plugin.plugin_name =="Light_kit_infinite_free":
            print("Light_kit_infinite_free")
            codevonc_depliage_path = plugin_c4d_path
            codevonc_depliage_C4DPlugin = os.path.join(r"C:\\Program Files\\MAXON", \
                                        self.plugin.soft_version)
            print(55555555555555555555555555555555555555555555555555555555555555555555)
            print (r'start robocopy "' + codevonc_depliage_path + '\\" /to="' + codevonc_depliage_C4DPlugin + '"')
            cmds = 'start C:/fcopy/FastCopy.exe /force_close "%s" /to="%s"'%(codevonc_depliage_path,codevonc_depliage_C4DPlugin)
            os.system(cmds)
        
        else:
            pass
    
        return True

    
    def __get_plugin_path(self):
        # B:\plugins\C4D\c4dtoa\c4dtoa_2.2.0\CINEMA 4D R18\plugins
        plugin_full_path =  os.path.join(self.plugin_root, \
                                        r'plugins\C4D', \
                                        self.plugin.plugin_name, \
                                        self.plugin.plugin_name + '_' + self.plugin.plugin_version, \
                                        self.plugin.soft_version, 'plugins')
        return plugin_full_path
        
    def __get_c4d_path(self):
        plugin_c4d_path =  os.path.join(self.plugin_root, \
                                        r'plugins\C4D', \
                                        self.plugin.plugin_name, \
                                        self.plugin.plugin_name + '_' + self.plugin.plugin_version, \
                                        self.plugin.soft_version)
        return plugin_c4d_path
        
    def __get_c4d_library_path(self):
        c4d_library_path =  os.path.join(self.__get_c4d_path(),r"library\browser")
        return c4d_library_path
        
    # 20180710
    def __get_new_plugin(self):
        # B:\plugins\C4D\c4dtoa\2.2.0\CINEMA 4D R18\plugins
        plugin_new_path =  os.path.join(self.plugin_root, \
                                        r'plugins\C4D', \
                                        self.plugin.plugin_name, \
                                        self.plugin.plugin_version, \
                                        self.plugin.soft_version, 'plugins')
        return plugin_new_path
        
    def __maxon_install_path(self):
        # C:\Program Files\MAXON\CINEMA 4D R17\plugins
        maxon_install_path = os.path.join(r"C:\Program Files\MAXON", self.plugin.soft_version)
        return maxon_install_path
        
    def __get_new_library_path(self):
        # C:\Program Files\MAXON\CINEMA 4D R17\library\browser
        c_pan_library_path =  os.path.join(self.__maxon_install_path(),r"library\browser")
        return c_pan_library_path
        
    def __check_gpu(self):
        myname = socket.getfqdn(socket.gethostname(  ))
        myaddr = socket.gethostbyname(myname)
        return myname, myaddr
    ''' 
    def check_exe_version(self, soft_version):
        exe_file = os.path.join(r'C:\Program Files\MAXON\\' + self.soft_version + '.exe')
        print ('exeeeeeeeeeee' + exe_file)
        ##注：exe的属性有st_mode，st_size，st_ino ......
        print (“- size:”, size, “bytes”)
        print (“- owner:”, uid, gid)
        print (“- created:”, time.ctime(ctime))
        print (“- last accessed:”, time.ctime(atime))
        print (“- last modified:”, time.ctime(mtime))
        print (“- mode:”, oct(mode))
        print (“- inode/dev:”, ino, dev)
        # get stats for a filename
        st = os.stat(exe_file)
        print (“station”, exe_file)
        check_exe_version(soft_version)
        print (st)
        sys.stdout.flush()

    def copy_R18_exe(self,soft_version):
            #w2-r18-CINEMA 4D.exe
            c4d_exe_path = r"B:\plugins\C4D\c4d_R18_exe\CINEMA 4D.exe"
            c4d_exec_dest_path = r'C:\Program Files\MAXON\CINEMA 4D R18\CINEMA 4D.exe'
            print ('8888' + c4d_exe_path, c4d_exec_dest_path)
            print('copy "%s" "%s" ' % (c4d_exe_path, c4d_exec_dest_path))
            os.system('copy "%s" "%s" ' % (c4d_exe_path, c4d_exec_dest_path))
    '''
if __name__ == "__main__":
    plugin_name    = sys.argv[1]
    plugin_version = sys.argv[2]
    soft_version   = sys.argv[3]
    node           = sys.argv[4]
    
    print (plugin_name, plugin_version, soft_version, node)

    plugin_mgr = C4dPluginMgr('100000',r'\\10.90.96.51\td1')
    
    plugin1 = C4dPlugin()
    plugin1.plugin_name      = plugin_name
    plugin1.plugin_version   = plugin_version
    plugin1.soft_version     = soft_version
    plugin1.node             = node


    plugin_mgr.get_dll(soft_version)
    
    result = plugin_mgr.set_custom_env(plugin1)

    #plugin2 = C4dPlugin()
    #plugin2.plugin_name      = "c4dtoa"
    #plugin2.plugin_version   = "2.2.0"
    #plugin2.soft_version     = "CINEMA 4D R18"
    #plugin2.node             = "ABCDEF"
    #plugin_mgr.set_custom_env(plugin2)
    
    #plugin_mgr.copy_R18_exe(soft_version)
    #print ('...copy_R18_exe was done...')
    
    if result:
        c4d_exec_path = r'"C:\Program Files\MAXON\%s\CINEMA 4D.exe"' % (plugin1.soft_version)
        print ('@KANADA.9999' + c4d_exec_path)
        os.system (os.path.normpath(c4d_exec_path))
        print ('[everything are perfect!!!]')
        print ('[@KANADA.done!!!]')
    else:
        print ('[@KANADA.done, plugin config failed!!!]')



"""
TEST:    
C:\Python27\python.exe "\\10.60.100.104\new_render_data\input\p\script\CG\C4d\function\C4DPluginManager.py" "vray" "3.4" "CINEMA 4D R18" "ABCDEF"

#C4D_PLUGINS_DIR
#B:\plugins\C4D\vray\vray_1.9\CINEMA 4D R17\plugins;B:\plugins\C4D\c4dtoa\c4dtoa_1.6.2.0\CINEMA 4D R17\plugins;B:\plugins\C4D\realflow\realflow_2015\CINEMA 4D R17\plugins;

#C4D_BROWSERLIBS
#B:\plugins\C4D\gsg_hdri_studio_pack\gsg_hdri_studio_pack_2.0\CINEMA 4D R17\library\browser;B:\plugins\C4D\c4dtoa\c4dtoa_1.4.0.0\CINEMA 4D R17\library\browser;

#B:\plugins\C4D\vray\vray_1.9\CINEMA 4D R17\VrayBridge.key 
#B:\plugins\C4D\c4dtoa\c4dtoa_1.0.14.1\CINEMA 4D R17\ai.dll
#B:\plugins\C4D\c4dtoa\c4dtoa_1.0.14.1\CINEMA 4D R17\solidangle.lic

"""
