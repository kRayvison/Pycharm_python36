#!/usr/bin/env python
#encoding:utf-8
# -*- coding: utf-8 -*-


__author__ = 'miaoyuanxi'


import sys,os,string,re
import nuke
import RVLIB
import json
import subprocess
import _subprocess
import threading
import multiprocessing
import time
import codecs
import random
import datetime
import logging
from multiprocessing import Pool

_PATH_ORG = os.environ.get('PATH')
os.environ['PATH'] = (_PATH_ORG if _PATH_ORG else "") + r";C:\Windows\system32"



def RecursiveFindNodes( nodeClass ,startNode ):
    nodeList = []

    if startNode != None:
        if startNode.Class() == nodeClass:
            nodeList = [startNode]
        elif isinstance(startNode, nuke.Group):
            for child in startNode.nodes():
                nodeList.extend( RecursiveFindNodes(nodeClass, child) )

    return nodeList


def _RV_write_Frame_Info(INF, _NK_BASENAME):
    info = {}
    framerange = {}
    i = 0
    print "\nSEARCHING WRITE....................."

    writeNodes = RecursiveFindNodes( "Write", nuke.Root())

    # deepWriteNodes = RecursiveFindNodes( "DeepWrite", nuke.Root() )
    # writeGeoNodes = RecursiveFindNodes( "WriteGeo", nuke.Root() )
    #
    # writeNodes.extend(deepWriteNodes)
    # writeNodes.extend(writeGeoNodes)


    for node in writeNodes:
        filename = nuke.filename(node)
        filename = filename.replace('\\','/')
        Mnode = node.fullName()

        print "    RENDERING NODE : %s" % node.fullName()
        framerange['firstframe'] = node.firstFrame()
        framerange['lastframe'] = node.lastFrame()
        framerange['byframe'] = 1

        info[Mnode] = framerange
        print '"    RENDERING NODE : %s---%s-%s"' % (node.fullName(),node.firstFrame(),node.lastFrame())

    print "\nSEARCHING RENDER WRITES......."



    if info is not None:

        # Mjsonfile = RVLIB.store(INF,info)
        #
        # data = RVLIB.load(INF)
        # print data
        print "before write to txt \n%s" %(info)
        with open(INF, 'w') as analysefile:
            analysefile.write(str(info))


        with open(INF, 'r') as rfile:
            lines = rfile.readlines()
            for line in lines:
                print line
            print "write success!_____________________________________________"
    else:
        print("Warning: there is not any write in this file!..............")




def _RV_loadNKFile(NK_file, error_logger = None):


    NK_file = NK_file.replace("\\", "/")

    try:
        nuke.scriptOpen(NK_file)
        #nuke.load(NK_file)



    except:
        print "except "
        pass


def _RV_renderSetup(_WRI, _SFM, _EFM, _BFM, _IN, _OUT, _NK_BASENAME):
    #if filename is C:/ or D:/ or //
    #netmap = _INPUTpath

    print '\nRENDER SETUP ...'
    _write_Node = None
    output_new = None
    fileinputValue = ''
    T_Nodes = []
    readNodes = []
    writeNodes = []
    warningMessages = ''
    warningMessages_out = ''
    readNodes = RecursiveFindNodes( "Read", nuke.Root())
    readgeoNodes = RecursiveFindNodes( "ReadGeo2", nuke.Root())
    readNodes.extend(readgeoNodes)


    writeNodes = RecursiveFindNodes( "Write", nuke.Root())

    # deepWriteNodes = RecursiveFindNodes( "DeepWrite", nuke.Root() )
    # writeGeoNodes = RecursiveFindNodes( "WriteGeo", nuke.Root() )
    #
    # writeNodes.extend(deepWriteNodes)
    # writeNodes.extend(writeGeoNodes)


    #change readnodes path  D:/M_Nuke_test/sources/timg.jpg    or   //10.50.242.6/d/inputdata/100000/100001/yanrk_test/upload/engine_checker/zlib1.dll

    for nodes in readNodes:
        fileinputValue = nuke.filename( nodes )


        if fileinputValue != '':

            if os.path.exists(fileinputValue):
                print nodes.name() + ":" + fileinputValue


                if RVLIB.IsPathLocal(fileinputValue):
                    warningMessages = "Input path for read node '" + nodes.name() + "' is local:\n" + fileinputValue + "\n\n"
                    print warningMessages
                    newinputpath = fileinputValue.replace(fileinputValue.split("/")[0],_IN,1)
                    nodes['file'].setValue(newinputpath)
                    finalinputValue = nuke.filename( nodes )
                    print  finalinputValue



                if RVLIB.IsPathNetIp(fileinputValue):
                    warningMessages =  "Input path for read node '" + nodes.name() + "' is net:\n" + fileinputValue + "\n\n"
                    print warningMessages
                    newinputpath = fileinputValue.replace(fileinputValue.split("/")[0:3],_IN,1)
                    nodes['file'].setValue(newinputpath)
                    finalinputValue = nuke.filename( nodes )
                    print  finalinputValue

                # print "New path" + ":" + finalinputValue
            else:
                print nodes.name() +":" + fileinputValue + r"  is not exist!!!!!!"


# change  writenodes path  D:/M_Nuke_test/sources/timg.jpg    or   //10.50.242.6/d/inputdata/100000/100001/yanrk_test/upload/engine_checker/zlib1.dll

    # for node in writeNodes:

        # fileoutValue = nuke.filename( node )
        # if fileoutValue != '':
            # print node.name() + ":" + fileoutValue

            # if fileoutValue.split("/")[1] != _OUT.split("/")[1]:
                # warningMessages_out = "Output path for read node '" + node.name() + "' is local:\n" + fileoutValue + "\n\n"
                # print warningMessages_out
                # newoutputpath = fileoutValue.replace(fileoutValue.split("/")[0],_OUT,1)
                                # #OUTput
                # if os.path.dirname(newoutputpath) == False:
                    # os.makedirs(os.path.dirname(newoutputpath))

                # node['file'].setValue(newoutputpath)
                # finaloutputValue = nuke.filename( node )
                # print  "New path:" + finaloutputValue

                
            # elif fileoutValue.split("/")[1] == _OUT.split("/")[1] and fileoutValue.split("/")[9] != _OUT.split("/")[9]:
                # warningMessages_out = "Output path for read node '" + node.name() + "' is local:\n" + fileoutValue + "\n\n"
                # print warningMessages_out
                # mlist = fileoutValue.split("/")[10:]

                # newoutputpath = _OUT + "/".join(mlist)
                                # #OUTput
                # if os.path.dirname(newoutputpath) == False:
                    # os.makedirs(os.path.dirname(newoutputpath))

                # node['file'].setValue(newoutputpath)
                # finaloutputValue = nuke.filename( node )
                # print  "New path:" + finaloutputValue
    # If the Nuke script has been modified, then save it to preserve SG settings.
    #root = nuke.Root()
    #nuke.scriptSave( root.name() )


    _write_Node = _WRI


    return _write_Node





def getFrameList(frameIn, frameOut, interval, fileName, multiRenderNum = 4):
    video_list = ["mov", "mp4"]
    max_threads_number = int(multiprocessing.cpu_count())
    n = max_threads_number / int(multiRenderNum)
    print "cpu_count: %s" % n
    
    n = 4
    
    if max_threads_number % int(multiRenderNum) > 0:
        if (n + 1) * int(multiRenderNum) - max_threads_number <= max_threads_number / 2:
            n = n + 1
    inout = [str(i) for i in range(int(frameIn), int(frameOut) + 1, int(interval))]
    filePath = os.path.split(fileName)[0]
    if os.path.exists(filePath) == False:
        os.makedirs(filePath)
    if fileName.split(".")[-1] in video_list:
        n = 1
    print inout
    print "frames: %s" % len(inout)
    framesEach = len(inout) / n
    if len(inout) % n > 0:
        framesEach = framesEach + 1
    print "renders: %s" % n
    print "framesEach: %s" % framesEach

    frameList = [[] for i in range(n + 1)]
    for i in range(1, n):
        frameList[i] = inout[((i - 1) * framesEach):(i * framesEach)]
    frameList[n] = inout[((n - 1) * framesEach):]
    frameStr = ["" for i in range(n + 1)]
    for i in range(1, n + 1):
        tempList = []
        if frameList[i] != []:
            tempList.append(frameList[i][0])
            tempList.append(frameList[i][-1])
            frameStr[i] = ",".join(tempList)
    return frameStr



def createCMDList(nukeExecutePath, renderThreads, write, nkPath, _SFM, _EFM, _BFM, fileName):


    print _SFM
    print _EFM
    print _BFM
    print fileName
    frameList = getFrameList(_SFM, _EFM, _BFM, fileName)
    print  frameList
    cmdList = []
    for frames in frameList:
        if frames != "":
            # cmd = nuke.execute(write ,_SFM,_EFM,_BFM)
            if nukeExecutePath.find("/") != -1:
                cmd = '"%s" -x -m %s -X %s -F %s,%s %s' % (nukeExecutePath, renderThreads, write, frames, _BFM, nkPath)
            else:
                cmd = '%s -x -m %s -X %s -F %s,%s %s' % (nukeExecutePath, renderThreads, write, frames, _BFM, nkPath)
            # # print cmd
            cmdList.append(cmd)
    print cmdList
    return cmdList





def long_time_task(name):
    print('Run task %s (%s)...' % (name, os.getpid()))
    start = time.time()
    name.daemon = True
    name.start()
    time.sleep(random.random() * 3)
    end = time.time()
    print('Task %s runs %0.2f seconds.' % (name, (end - start)))

def execCmd(cmd):
     try:
        print "cmd %s start %s" % (cmd,datetime.datetime.now())
        os.system(cmd)
        print "cmd %s end %s" % (cmd,datetime.datetime.now())
     except Exception, e:
        print '%s\t failed, cause of failure\r\n%s' % (cmd,e)

'''
    调用子进程运行cmd命令
'''
def runCmd(self,cmd):
    print 'cmd='+cmd
    cmdp=subprocess.Popen(cmd,shell = True,stdout = subprocess.PIPE, stderr = subprocess.STDOUT)        
    while True:
        buff = cmdp.stdout.readline()
        if buff == '' and cmdp.poll() != None:
            break       
        print buff
        # self.G_RENDERCMD_LOGGER.info(buff)
        # self.G_PROCESS_LOGGER.info(buff)          
    resultCode = cmdp.returncode
    print 'resultCode='+str(resultCode) 
def RBcmd(cmdStr,continueOnErr=False,myShell=False):#continueOnErr=true-->not exit ; continueOnErr=false--> exit 
    print str(continueOnErr)+'--->>>'+str(myShell)
    G_PROCESS_LOG_M=logging.getLogger('processlog')
    G_PROCESS_LOG_M.info('cmd...'+cmdStr)
    cmdp=subprocess.Popen(cmdStr,stdin = subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.STDOUT, shell = myShell)
    cmdp.stdin.write('3/n')
    cmdp.stdin.write('4/n')
    while cmdp.poll()==None:
        resultLine = cmdp.stdout.readline().strip()
        if resultLine!='':
            G_PROCESS_LOG_M.info(resultLine)
        
    resultStr = cmdp.stdout.read()
    resultCode = cmdp.returncode
    
    G_PROCESS_LOG_M.info('resultStr...'+resultStr)
    G_PROCESS_LOG_M.info('resultCode...'+str(resultCode))
    
    if not continueOnErr:
        if resultCode!=0:
            sys.exit(resultCode)
    return resultStr
    
def RBTry3cmd(cmdStr,continueOnErr=False,myShell=False):#continueOnErr=true-->not exit ; continueOnErr=false--> exit 
    print str(continueOnErr)+'--->>>'+str(myShell)
    G_PROCESS_LOG=logging.getLogger('processlog')
    G_PROCESS_LOG.info('cmd...'+cmdStr)
    #self.G_PROCESS_LOG.info('try3...')
    l=0
    resultStr=''
    resultCode=0
    while l < 3:
        l=l+1;
        cmdp=subprocess.Popen(cmdStr,stdin = subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.STDOUT, shell = myShell)
        cmdp.stdin.write('3/n')
        cmdp.stdin.write('4/n')
        while cmdp.poll()==None:
            resultLine = cmdp.stdout.readline().strip()
            if resultLine!='':
                G_PROCESS_LOG.info(resultLine)
            
        resultStr = cmdp.stdout.read()
        resultCode = cmdp.returncode
        if resultCode==0:
            break
        else:
            time.sleep(1)
    
    G_PROCESS_LOG.info('resultStr...'+resultStr)
    G_PROCESS_LOG.info('resultCode...'+str(resultCode))
    
    if not continueOnErr:
        if resultCode!=0:
            sys.exit(resultCode)
    return resultStr
    
def checkResult(root,finalpath):
    G_PROCESS_LOG.info( '================[checkResult]===============')
    serverOutput=finalpath.encode(sys.getfilesystemencoding())
    nodeOutput=root.replace('\\','/')
    G_PROCESS_LOG.info('')
    G_PROCESS_LOG.info(nodeOutput)
    G_PROCESS_LOG.info(serverOutput)
    G_PROCESS_LOG.info('')
    nodeImgDict={}
    serverImgDict={}
    for root, dirs, files in os.walk(nodeOutput) : 
        for name in files:
            #------------node output file----------------
            nodeImgFile =os.path.join(root, name).replace('\\','/')
            imgFile=nodeImgFile.replace(nodeOutput,'')
            
            imgFileStat=os.stat(nodeImgFile)
            imgFileSize=str(os.path.getsize(nodeImgFile))
            nodeImgDict[imgFile]=imgFileSize
            date = datetime.datetime.fromtimestamp(imgFileStat.st_ctime)  
            imgFileCtime= date.strftime('%Y%m%d%H%M%S')  
            #imgFileCtime=str(imgFileStat.st_ctime)
            imgFileInfo='[node]'+imgFile+' ['+imgFileSize+'] ['+imgFileCtime+']'
            
            G_PROCESS_LOG.info(imgFileInfo)
            #------------server output file----------------
            serverImgFile=(serverOutput+imgFile).replace('/','\\')
            serverImgFileInfo=''
            if os.path.exists(serverImgFile):
                imgFileStat=os.stat(serverImgFile)
                imgFileSize=str(os.path.getsize(serverImgFile))
                
                date = datetime.datetime.fromtimestamp(imgFileStat.st_ctime)  
                imgFileCtime= date.strftime('%Y%m%d%H%M%S')
                serverImgFileInfo='[server]'+imgFile+' ['+imgFileSize+'] ['+imgFileCtime+']'
                serverImgDict[imgFile]=imgFileSize
            else:
                serverImgFileInfo='[server]'+imgFile+' [missing]'
            
            G_PROCESS_LOG.info(serverImgFileInfo)
            G_PROCESS_LOG.info('')
            
    G_PROCESS_LOG.info('')    
    
def _RV_renderWrite(write,_NK, _SFM,_EFM,_BFM,_IN,_OUT,_CGV,_NUKE_RUN_PATH):
    _SERVER_Plugins = r"B:"
    print '---------------------------------------'
    print 'write = ', write
    print 'first|last|byframe = %d-%d-%d'%(_SFM,_EFM,_BFM)

    print '---------------------------------------\n'

###############################################################################
    print _CGV

    # if _CGV == '9.0v1':
        # if os.path.exists(r'C:/Program Files/Nuke9.0v1/'):
            # nuke_path = r'C:/Program Files/Nuke9.0v1/Nuke9.0.exe'
        # else:
            # nuke_path = None
    
    # if _CGV == '10.0v4':
        # if os.path.exists(r'C:/Program Files/Nuke10.0v4/'):
            # nuke_path = r'C:/Program Files/Nuke10.0v4/Nuke10.0.exe'
        # else:
            # nuke_path = None            
    # if _CGV == '10.5v1':
        # if os.path.exists(r'C:/Program Files/Nuke10.5v1/'):
            # nuke_path = r'C:/Program Files/Nuke10.5v1/Nuke10.5.exe'
        # else:
            # nuke_path = None
            
    # if os.path.exists(r'C:/Program Files/Nuke9.0v9/'):
        # nuke_path = r'C:/Program Files/Nuke9.0v9/Nuke9.0.exe'
    # else:
        # nuke_path = None  

    # if nuke_path == None:
        # return None
        
    # else:
        # print nuke_path
        

    nuke_path = _NUKE_RUN_PATH + "/" + "Nuke9.0.exe"
    print "_NUKE_RUN_PATH= " + nuke_path
    
    
    nukeExecutePath = nuke_path
    # nukeExecutePath = nuke.env["ExecutablePath"]
    max_threads_number = int(multiprocessing.cpu_count())

    # nuke.scriptOpen(_NK)
    nuke.load(_NK)
    renderwrite = nuke.toNode(write)
    print type(write)
    print type(renderwrite)

    fileName = nuke.filename(renderwrite)


    cmdList = createCMDList(nukeExecutePath, max_threads_number, write, _NK, _SFM, _EFM, _BFM, fileName)

    threads = []
    print r"--------------------rendering  start---------------------- "
    print r"cmd starting %s" % datetime.datetime.now()

    for cmd in cmdList:
        th = threading.Thread(target=RBcmd, args=(cmd,))
        th.start()
        threads.append(th)

    for th in threads:
        th.join()

    print r"cmd ending %s" % datetime.datetime.now()
    
    print r"--------------------rendering  end---------------------- "   
    
    #newinputpath = _IN + fileName.split("/")[0][0] + "/" + "/".join(fileName.split("/")[1:])
    newinputpath = fileName
    
    newoutputpath = fileName.replace(fileName.split("/")[0],_OUT,1)                    
    if not os.path.exists(os.path.dirname(newoutputpath)):
        os.makedirs(os.path.dirname(newoutputpath))
        
    finalpath = os.path.dirname(newoutputpath)
    
    root = os.path.dirname(newinputpath)

    root.replace("/", "\\")
    finalpath.replace("/", "\\")
    

    print "User output path : %s"  %root.replace('/','\\')
    print "Platform output path : %s"  %finalpath.replace('/','\\')
    
    cmd1='c:\\fcopy\\FastCopy.exe  /speed=full /force_close  /no_confirm_stop /force_start "' + root.replace('/','\\') +'" /to="'+finalpath.replace('/','\\')+'"'
    RBTry3cmd(cmd1)
    # try:
        # checkResult(root,finalpath)
    # except Exception, e:
        # print '[checkResult.err]'
        # print e
    # a = os.walk(root)
    # for x in a:
        # pre=os.path.basename(x[0])
        # for j in x[-1]:
            # os.rename(x[0]+'/'+j, finalpath +'/'+j)

    print("RENDERING FINISHED WITH EXECUTE PARM!")





    
    
def _RV_getOutputPath(writenode):
    """Returns an empty string if it cannot be determined."""
    if writenode is None:
        return None
    output_parm = nuke.filename(writenode)

    if output_parm is not None:
        output_path = output_parm.getReferencedParm().unexpandedString()
    else:
        output_path = ""

    return output_path





def addenvpath(_CGV):
    userpath = os.environ["userprofile"]
    usernukepath = userpath + r"/.nuke"

    if os.path.exists(usernukepath) == False:
        os.makedirs(usernukepath)

    initfile = usernukepath + "/init.py"


    with open(initfile, 'w') as f:

        addpath  =r"B:/plugins/nuke/plugins/NukePackages"

        inf = "import nuke\nnuke.pluginAddPath('%s')" % addpath

        f.write(inf)

            
            
            
            
