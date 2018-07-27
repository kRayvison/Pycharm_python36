#script_param_mark#


import os,sys,shutil


print 'copyBasePy...start'
G_NODE_PY=r'c:\script\new_py'
node_py_cg=G_NODE_PY+r'\CG'
if G_RENDEROS=='0':#linux
    G_NODE_PY=r'/root/rayvision/script/new_py'
    node_py_cg=G_NODE_PY+r'/CG'
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


import AnalyzeAction


if(__name__=="__main__"):
    paramDict = {'G_JOB_ID':G_JOB_ID,'G_USER_ID':G_USER_ID,'G_USER_ID_PARENT':G_USER_ID_PARENT,'G_TASK_ID':G_TASK_ID,'G_CG_NAME':G_CG_NAME,'G_NODE_PY':G_NODE_PY,'G_SYS_ARGVS':sys.argv,'G_SCRIPT_POOL':G_SCRIPT_POOL,'G_RENDER_OS':G_RENDER_OS,'G_TASK_JSON':G_TASK_JSON,'G_ACTION':G_ACTION}
    AnalyzeAction.main(**paramDict)
