
# /usr/bin/env python
import sys,os

katana_com_id=sys.argv[1]
kantan_task_is=sys.argv[2]
plugin_cfg  = sys.argv[3]
katana_scene  = sys.argv[4]
katana_ana_txt=sys.argv[5]

def set_plug():
    if sys.platform.startswith("win"):
        os_type = "win"
        katana_soft_path = r"B:/plugins/katana/win"
        katana_exe = 'katanaBin.exe'
    elif sys.platform.startswith("linux"):
        os_type = "linux"
        katana_soft_path = r"/munt/plugins"
        katana_exe = "katana"

    plugins_dict = eval(open(plugin_cfg).read())
    katana_n = plugins_dict['renderSoftware']
    katana_v = plugins_dict['softwareVer']
    plugins = plugins_dict['plugins']
    os.environ['foundry_LICENSE'] = "4101@127.0.0.1;4101@10.60.5.248"
    katana_root = "%s/%s%s" % (katana_soft_path ,katana_n,katana_v)
    katana_path = "%s/bin/%s" % (katana_root,katana_exe)
    _PATH_env = os.environ.get('PATH')
    os.environ['PATH'] = (_PATH_env if _PATH_env else "") + r";" + katana_root + r"\bin;"
    
    for plugin in plugins:
        plg_name = plugin
        plg_v = plugins[plg_name]
        plg_root = "%s/%s-%s-%s%s" % (katana_soft_path,plg_name, plg_v,katana_n,katana_v.split('v')[0])
        plg_config = plg_root+"/Config.py"
        if os.path.exists(plg_config):
            sys.path.append(plg_root)
            try:
                cfg = __import__('Config')
                reload(cfg)
                cfg.doConfigSetup(plugins)
                print ('=== the plugin %s %s load  Success for katana' % (plg_name,plg_v))
            except Exception as err:
                print ('=== Error occur import/execute "%s"! ===\n=== Error Msg : %s ===' % (plg_config, err))
            try:
                while True:
                    sys.path.remove(plg_root)
            except:
                pass
        else:
            print ('plugin file "%s" is not exists!' % (plg_config))
    return katana_path
currentPath = os.path.split(os.path.realpath(__file__))[0]        
katana_script = currentPath+"/katana_script_bak.py"
def kanana_analyse_sys(kantan_root,katana_script,katana_scene,katana_ana_txt):
    os.system(r'%s --script %s %s  %s' % (kantan_root,katana_script,katana_scene,katana_ana_txt))
    if  os.path.exists(katana_ana_txt):
        return 1
    else:
        return 0

kantan_root = set_plug()
kanana_analyse_sys(kantan_root,katana_script,katana_scene,katana_ana_txt)


