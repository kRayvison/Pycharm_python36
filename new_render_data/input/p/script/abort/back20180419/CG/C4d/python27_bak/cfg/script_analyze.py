# "c:\python27\python" "c:\work\render\111\cfg\script_analyze.py" "2017082500021" "0" "frame_analyse_1111352" "11252855482128" "GB116" "0"

#encoding:utf-8
G_CG_NAME='C4d'
G_ACTION='Analyze'
G_USER_ID='100002'
G_TASK_ID='111'
G_SMALL_TASK_ID='666'
G_PHOTON_SMALL_TASK_ID='888'
G_TASK_JSON='//10.60.100.104/new_render_data/input/p/config/100000/100002/111/cfg/task.json'
G_USER_ID_PARENT='100000'
G_SCRIPT_POOL='//10.60.100.104/new_render_data/input/p/script'
G_RENDER_OS='1'
#script_param_mark#
G_JOB_NAME = ' picture_111'
G_JOB_ID = '111281'
G_CG_FRAMES = '10-10[1]'
G_CG_LAYER_NAME = ''
G_CG_OPTION = 'Camera001'
G_CG_TILE = ''
G_CG_TILECOUNT = ''
import os,sys,shutil
print 'copyBasePy...start'
G_NODE_PY=r'c:\script\new_py'
node_py_cg=G_NODE_PY+r'\cg'
if G_RENDER_OS=='0':#linux
    G_NODE_PY=r'/root/rayvision/script/new_py'
    node_py_cg=G_NODE_PY+r'/cg'
else:
    G_SCRIPT_POOL=G_SCRIPT_POOL.replace('/','\\')
    G_TASK_JSON=G_TASK_JSON.replace('/','\\')
if not os.path.exists(node_py_cg):
    os.makedirs(node_py_cg)
def copyFolder(source,target):
    print (source+' ----------> '+target)
    if not os.path.exists(target):
        os.makedirs(target)
    if os.path.exists(source):
        for root, dirs, files in os.walk(source):
            print 'copyBasePy...'
            for dirname in  dirs:
                tdir=os.path.join(root,dirname)
                if not os.path.exists(tdir):
                    os.makedirs(tdir)
            for i in xrange (0, files.__len__()):
                sf = os.path.join(root, files[i])
                folder=target+root[len(source):len(root)]+"/"
                if not os.path.exists(folder):
                    os.makedirs(folder)
                shutil.copy(sf,folder)
script_base=os.path.join(G_SCRIPT_POOL,'Base')
script_cg=os.path.join(G_SCRIPT_POOL,'CG',G_CG_NAME)
script_util=os.path.join(G_SCRIPT_POOL,'Util')
script_node_base=os.path.join(G_NODE_PY,'Base')
script_node_cg=os.path.join(G_NODE_PY,'CG',G_CG_NAME)
script_node_cg_function=os.path.join(script_node_cg,'function')
script_node_cg_process=os.path.join(script_node_cg,'process')
script_node_util=os.path.join(G_NODE_PY,'Util')
print G_SCRIPT_POOL
print script_base
print script_cg
print script_util
print G_NODE_PY
print script_node_base
print script_node_cg
print script_node_util
user_render_py=os.path.join(G_SCRIPT_POOL,'user',G_USER_ID)
try:
    shutil.rmtree(G_NODE_PY)
except Exception, e:
    pass
copyFolder(script_base,script_node_base)
copyFolder(script_cg,script_node_cg)
copyFolder(script_util,script_node_util)
copyFolder(user_render_py,G_NODE_PY)
sys.path.append(G_NODE_PY)
sys.path.append(script_node_base)
sys.path.append(script_node_cg)
sys.path.append(script_node_cg_function)
sys.path.append(script_node_cg_process)
sys.path.append(script_node_util)
print 'copyBasePy...end'
#-----------------------------------------------------
if(__name__=="__main__"):
    paramDict = {}
    paramDict['G_SYS_ARGVS'] = sys.argv
    namespace_list = dir()
    for name in namespace_list:
        if name.startswith('G'):
            paramDict[name] = eval(name)
    print paramDict
    print 'G_CG_NAME=================='+G_CG_NAME
    print 'G_ACTION==================='+G_ACTION
    module_name = G_ACTION+G_CG_NAME
    if G_ACTION == 'RenderPhoton' or G_ACTION == 'MergePic':
        module_name = 'Render'+G_CG_NAME
    if G_ACTION == 'MergePhoton':
        module_name = 'Merge'
    class_name = module_name
    #-----------import cg py model---------------
    from_str = 'from '+module_name+' import *'
    print ('from_str='+from_str)
    print ('class_name='+class_name)
    exec(from_str)
    exec('render='+class_name+'(**paramDict)')
    exec('render.RB_EXECUTE()')
