import os,sys,subprocess,string,logging,time,shutil
import logging

sys.path.append('C:/script/new_py/Base')
sys.path.append('/root/rayvision/script/new_py/Base')
from AnalyzeBase import *



class AnalyzeAction():
    def __init__(self,**paramDict):
        cg_name=paramDict['G_CG_NAME']
        node_py=paramDict['G_NODE_PY']
        action=paramDict['G_ACTION']
        print 'cg_name=================='+cg_name+'========='
        print 'node_py=================='+node_py
        print 'action=================='+action
        
        #-----------append cg py path---------------
        
        cg_py_path=os.path.join(node_py,'CG',cg_name)
        print ('cg_py_path='+cg_py_path)
        if os.path.exists(cg_py_path):
            print 'append path-------'
            sys.path.append(cg_py_path)
        if os.path.exists(node_py+'/Util'):
            sys.path.append(node_py+'/Util')
            
        #-----------import cg py model---------------
        from_str='from '+action+cg_name+' import *'
        print ('from_str='+from_str)
        exec(from_str)
        
        exec('AnalyzeAction.__bases__=('+cg_name+',)')
        exec(cg_name+'.__init__(self,**paramDict)')
        
    '''
    def RBrender(self):#Render command
        print 'AnalyseAction..max...render....'
    '''
#-----------------------main-------------------------------
def main(**paramDict):
    analyze=AnalyzeAction(**paramDict)
    analyze.RB_EXECUTE()