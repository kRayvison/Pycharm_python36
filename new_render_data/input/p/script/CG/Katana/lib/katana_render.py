# /usr/bin/env python
import socket,os,shutil,sys
katana_com_id=sys.argv[1]
katana_task_is=sys.argv[2]
katana_scene  = sys.argv[3]
katana_render_node = sys.argv[4]
katana_farm_start=sys.argv[5]
katana_farm_end=sys.argv[6]
plugin_cfg=sys.argv[7]

katana_root = "/opt/foundry/katana"
#katana_root = "/home/ladaojeiang/yes"
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
    os.environ['foundry_LICENSE'] = "4101@127.0.0.1"
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
katana_root = set_plug()
def kanana_render(katana_root,katana_scene,katana_render_node,katana_farm_start,katana_farm_end):
        print "______--------start render___________---------------"
        os.system(r'%s --batch --katana-file=%s --render-node=%s  --t=%s-%s' % (katana_root,katana_scene,katana_render_node,katana_farm_start,katana_farm_end))
kanana_render(katana_root,katana_scene,katana_render_node,katana_farm_start,katana_farm_end)