#encoding:utf-8
#script_param_mark#
import os,sys,shutil
from distutils.sysconfig import get_python_lib
print('copyBasePy...start')
G_NODE_PY=r'c:\script\new_py'
node_py_cg=G_NODE_PY+r'\cg'
if G_ACTION == 'PreRender':
    G_ACTION = 'Render'
if G_RENDER_OS=='0':#linux
    G_NODE_PY=r'/root/rayvision/script/new_py'
    node_py_cg=G_NODE_PY+r'/cg'
else:
    G_SCRIPT_POOL=G_SCRIPT_POOL.replace('/','\\')
    G_TASK_JSON=G_TASK_JSON.replace('/','\\')
if not os.path.exists(node_py_cg):
    os.makedirs(node_py_cg)
def copy_folder(source,target):
    print(source+' ----------> '+target)
    if not os.path.exists(target):
        os.makedirs(target)
    if os.path.exists(source):
        for root, dirs, files in os.walk(source):
            print('copyBasePy...')
            for dirname in  dirs:
                tdir=os.path.join(root,dirname)
                if not os.path.exists(tdir):
                    os.makedirs(tdir)
            for i in range(0, files.__len__()):
                sf = os.path.join(root, files[i])
                folder=target+root[len(source):len(root)]+"/"
                if not os.path.exists(folder):
                    os.makedirs(folder)
                shutil.copy(sf,folder)
def copy_py_site_package():
    lib_path=get_python_lib()
    print('lib_path='+lib_path)
    script_site_package=os.path.join(G_SCRIPT_POOL,'SitePackage')
    script_cg_site_package=os.path.join(G_SCRIPT_POOL,'CG',G_CG_NAME,'SitePackage')
    user_site_packageos=os.path.join(G_SCRIPT_POOL,'user',G_USER_ID,'SitePackage')
    print('script_site_package='+script_site_package)
    print('script_cg_site_package='+script_cg_site_package)
    print('user_site_packageos='+user_site_packageos)
    copy_folder(script_site_package,lib_path)
    copy_folder(script_cg_site_package,lib_path)
    copy_folder(user_site_packageos,lib_path)
script_base=os.path.join(G_SCRIPT_POOL,'Base')
script_cg=os.path.join(G_SCRIPT_POOL,'CG',G_CG_NAME)
script_util=os.path.join(G_SCRIPT_POOL,'Util')
script_node_base=os.path.join(G_NODE_PY,'Base')
script_node_cg=os.path.join(G_NODE_PY,'CG',G_CG_NAME)
script_node_cg_function=os.path.join(script_node_cg,'function')
script_node_cg_process=os.path.join(script_node_cg,'process')
script_node_util=os.path.join(G_NODE_PY,'Util')
user_render_py=os.path.join(G_SCRIPT_POOL,'user',G_USER_ID)
print('G_SCRIPT_POOL='+G_SCRIPT_POOL)
print('script_base='+script_base)
print('script_cg='+script_cg)
print('script_util='+script_util)
print('G_NODE_PY='+G_NODE_PY)
print('script_node_base='+script_node_base)
print('script_node_cg='+script_node_cg)
print('script_node_util='+script_node_util)
print('user_render_py='+user_render_py)
try:
    shutil.rmtree(G_NODE_PY)
except Exception as e:
    pass
copy_folder(script_base,script_node_base)
copy_folder(script_cg,script_node_cg)
copy_folder(script_util,script_node_util)
copy_folder(user_render_py,G_NODE_PY)
copy_py_site_package()
sys.path.append(G_NODE_PY)
sys.path.append(script_node_base)
sys.path.append(script_node_cg)
sys.path.append(script_node_cg_function)
sys.path.append(script_node_cg_process)
sys.path.append(script_node_util)
print('copyBasePy...end')
#-----------------------------------------------------
if(__name__=="__main__"):
    paramDict = {}
    paramDict['G_SYS_ARGVS'] = sys.argv
    namespace_list = dir()
    for name in namespace_list:
        if name.startswith('G'):
            paramDict[name] = eval(name)
    #print(paramDict)
    print('G_CG_NAME=================='+G_CG_NAME)
    print('G_ACTION==================='+G_ACTION)
    module_name = G_ACTION+G_CG_NAME
    if G_ACTION == 'RenderPhoton' or G_ACTION == 'MergePic' or G_ACTION == 'GopRender':
        module_name = 'Render'+G_CG_NAME
    if G_ACTION == 'MergePhoton':
        module_name = 'Merge'+G_CG_NAME
    class_name = module_name
    #-----------import cg py model---------------
    from_str = 'from '+module_name+' import *'
    print('from_str='+from_str)
    print('class_name='+class_name)
    exec(from_str)
    exec('render='+class_name+'(**paramDict)')
    exec('render.RB_EXECUTE()')
