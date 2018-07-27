import os,sys,subprocess,string,logging,time,shutil
import logging

sys.path.append('C:/script/py/Base')
sys.path.append('/root/rayvision/script/py/Base')
from AnalysisBase import *



class AnalyseAction():
    def __init__(self,**paramDict):
        cgName=paramDict['G_CG_NAME']
        nodePyDir=paramDict['G_NODE_PY']
        print 'cgName=================='+cgName+'========='
        print 'nodePyDir=================='+nodePyDir
        
        #-----------apeend cg py path---------------
        
        cgPyPath=nodePyDir+'/'+cgName
        print ('cgPyPath='+cgPyPath)
        if os.path.exists(cgPyPath):
            print 'append path-------'
            sys.path.append(cgPyPath)
        if os.path.exists(nodePyDir+'/Util'):
            sys.path.append(nodePyDir+'/Util')
            
        #-----------import cg py model---------------
        fromStr='from Analysis'+cgName+' import *'
        print ('fromStr='+fromStr)
        if cgName=='Preprocess':
            fromStr='from '+cgName+' import *'
        exec(fromStr)
        
        exec('AnalyseAction.__bases__=('+cgName+',)')
        exec(cgName+'.__init__(self,**paramDict)')
        
    '''
    def RBrender(self):#Render command
        print 'AnalyseAction..max...render....'
    '''
#-----------------------main-------------------------------
def main(**paramDict):
    analyse=AnalyseAction(**paramDict)
    print 'G_POOL_NAME___'+analyse.G_POOL
    analyse.RBexecute()