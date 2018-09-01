#!/usr/bin/env python
#encoding:utf-8
# -*- coding: utf-8 -*-
'''
C:\Python27\python.exe C:\script\maya\check_all.py --cgsw "Maya" --ui 119768 --ti 5334090 --sfp "C:/Program Files/Autodesk/maya2014/bin/maya.exe" --proj "" --cgfile "G:/test_2014.mb" --cg_info_file "C:/WORK/helper/60156/analyse_net.txt" --pt 1005
'''
import os
import sys
import re
import subprocess
import json
if sys.version_info[:2] == (2, 6):
    if sys.platform.startswith("win"):
        sys.path.append(r"\\10.60.100.101\o5\py\model\tim\py26")
    elif sys.platform.startswith("linux"):
        sys.path.append(r"/mnt_rayvision/o5/py/model/tim/")

import argparse

if "maya" in sys.executable.lower():
    if "mayapy" in sys.executable.lower() or \
            "python-bin" in sys.executable.lower():
        import maya.standalone as standalone
        standalone.initialize()
    import maya.cmds as cmds
    import maya.mel as mel
    import pymel.core as pm

    
    
def RBcmd(cmdStr, continueOnErr = False, myShell = False):
    print cmdStr
    an_task_id = options['cg_info_file'].split('/')[3]
    user_id = options['user_id']

    if user_id in [11]:
        G_JOB_NAME=os.environ.get('G_JOB_NAME')
        print an_task_id,user_id,G_JOB_NAME
        render_log = "d:/log/helper/%s/%s.log" % (an_task_id,G_JOB_NAME)
        with open(render_log,"wb") as l:
            l.write('render cmd info: \n')
            l.write(cmdStr)
            l.flush()
            cmdp = subprocess.Popen(cmdStr,stdin = subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.STDOUT, shell = myShell)
            cmdp.stdin.write('3/n')
            cmdp.stdin.write('4/n')
            exitcode = 0
            
            while cmdp.poll() is None:
                resultLine = cmdp.stdout.readline().strip()
                
                if resultLine != '':            
                    l.write(resultLine+'\n')
                    l.flush()
                    print resultLine
                if resultLine =="write cg_info_file":
                    cmdp.kill()
                        
            resultStr = cmdp.stdout.read()
            resultCode = cmdp.returncode
    else:
        cmdp = subprocess.Popen(cmdStr,stdin = subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.STDOUT, shell = myShell)
        cmdp.stdin.write('3/n')
        cmdp.stdin.write('4/n')
        exitcode = 0
        while cmdp.poll() is None:
            resultLine = cmdp.stdout.readline().strip()
            
            if resultLine != '':
                print resultLine
            if resultLine =="write cg_info_file":
                cmdp.kill()
                    
        resultStr = cmdp.stdout.read()
        resultCode = cmdp.returncode

    
    
    if exitcode == -1:
        sys.exit(-1)

    if not continueOnErr:
        if resultCode != 0:
            sys.exit(resultCode)
    return resultStr


class Analyze(dict):

    def __init__(self, options):

        for i in options:
            self[i] = options[i]

    def run(self):
        ''

    def write_info_file(self):
        info_file_path=os.path.dirname(self["cg_info_file"])
        if not os.path.exists(info_file_path):
            os.makedirs(info_file_path)
        # try:
            # inof_json_path=  os.path.splitext(self["cg_info_file"])[0]+".json"
            # print inof_json_path
            # with open(inof_json_path, 'w') as f:
                # f.write(json.dumps(self))
                # f.close()
        # except Exception as err:
            # print  err
            # pass
            
            
        with open(self["cg_info_file"], "w") as f:
            #f.write("Start::%s\n" % (self["Start"]))
            f.flush()
            #f.write("End::%s\n" % (self["End"]))
            f.flush()            
            if "userRenderer" in self:
                f.write("userRenderer::%s\n" % (self["userRenderer"]))
                f.flush()                
            if "imageFilePrefix" in self:
                f.write("imageFilePrefix::%s\n" % (self["imageFilePrefix"]))
                f.flush()                
            if "Ext" in self:
                f.write("Ext::%s\n" % (self["Ext"]))
                f.flush()
            if "dynMemLimit" in self:
                f.write("dynMemLimit::%s\n" % (self["dynMemLimit"]))
                f.flush()          
            
            if "camera" in self:
                f.write("camera::%s\n" % (self["camera"]))
                f.flush()
            if "render_camera" in self:
                f.write("render_camera::%s\n" % (self["render_camera"]))
                f.flush()               

            # if "render_layer" in self:
                # f.write("render_layer::%s\n" % (self["render_layer"]))
                # f.flush()
            # if "renderable_layer" in self:
                # f.write("renderable_layer::%s\n" % (self["renderable_layer"]))
                # f.flush()

            # if "width" in self:
                # f.write("width::%s\n" % (self["width"]))
                # f.flush()
            # if "height" in self:
                # f.write("height::%s\n" % (self["height"]))
                # f.flush()

            if "preMel" in self:
                f.write("preMel::%s\n" % (self["preMel"]))
                f.flush()
            if "postMel" in self:
                f.write("postMel::%s\n" % (self["postMel"]))
                f.flush()

            if "preRenderLayerMel" in self:
                f.write("preRenderLayerMel::%s\n" % (self["preRenderLayerMel"]))
                f.flush()
            if "postRenderLayerMel" in self:
                f.write("postRenderLayerMel::%s\n" % (self["postRenderLayerMel"]))
                f.flush()

            if "preRenderMel" in self:
                f.write("preRenderMel::%s\n" % (self["preRenderMel"]))
                f.flush()
            if "postRenderMel" in self:
                f.write("postRenderMel::%s\n" % (self["postRenderMel"]))
                f.flush()                
            for key in self:
                print key
                if "layer_name_num" in key:
                    Layer_str ="%s::%s::%s::%s::%s::%s::%s::%s \n" % (key.replace(key,"Layer"),self[key]["layer_name"],self[key]["Start"],self[key]["End"],self[key]["Step"],self[key]["Width"],self[key]["Height"],self[key]["able"])
                    print Layer_str
                    f.write(Layer_str)
                    f.flush() 
            
            
            
            
            f.flush()
            print "write cg_info_file"            
            cmds.quit(force=True)
        cmds.quit(force=True)
    # def write_dict_info(self):
        # print "write_dict_info is start "
        # info_file_path=os.path.dirname(self["cg_info_file"])
        # if not os.path.exists(info_file_path):
            # os.makedirs(info_file_path)
        # with open(self["cg_info_file"], "w") as f:
            # for key in self:
                # str_w = '%s::%s' % (key, self[key])
                # f.write(str_w)
                # f.write('\n')
                # f.flush()
            # print "write cg_info_file"
            # cmds.quit(force=True)
        # cmds.quit(force=True)
        
    def write_dict_info(self):
        print "write_dict_info is start "
        for i in self.analyze_list:
            if i == ' ':
                self.analyze_list.remove(' ')           
        info_file_path=os.path.dirname(self["cg_info_file"])
        if not os.path.exists(info_file_path):
            os.makedirs(info_file_path)
        with open(self["cg_info_file"], "w") as f:
            for key in self.analyze_list:
                if self.has_key(key):                    
                    str_w = '%s::%s' % (key, self[key])
                    f.write(str_w)
                    f.write('\n')
                    f.flush()
                else:
                    continue
            f.write('Texture&Cache:')
            f.write('\n')
            f.flush()                    
            # for i in self['texture&cache']:                
                # f.write(i)
                # f.write('\n')
                # f.flush()
            # f.flush()            
            print "write cg_info_file"            
            cmds.quit(force=True)
        cmds.quit(force=True)       

    def write_file(self,file_content,my_file,my_code='UTF-8',my_mode='w'):
        
        if isinstance(file_content,(str,unicode)):
            file_content_u = self.str_to_unicode(file_content)
            fl=codecs.open(my_file, my_mode, my_code)
            fl.write(file_content_u)
            fl.close()
            return True
        elif isinstance(file_content,(list,tuple)):
            fl=codecs.open(my_file, my_mode, my_code)
            for line in file_content:
                fl.write(line+'\r\n')
            fl.close()
            return True
        else:
            return False 

            
class MayaAnalyze(Analyze):

    def __init__(self, options):
        super(MayaAnalyze, self).__init__(options)
    def get_info(self):
        if self["user_id"]:
          
            if int(str(self["user_id"])[-3:]) >= 500:
                fileId = str(self["user_id"] - int(str(self["user_id"])[-3:]) + 500)
            else:
                fileId = str(self["user_id"] - int(str(self["user_id"])[-3:]))
        else:
            print "don't find user_id"
        currentPath = os.path.split(os.path.realpath(__file__))[0].replace('\\', '/')
        info_json = eval(open(currentPath + '\\info.json').read())
        self["platform"] = str(self["platform"])
        if self["platform"] in info_json:
            cfg_path = info_json[self['platform']]['cfg_path']
            json_path = info_json[self['platform']]['json_path']
            custom_config = info_json[self['platform']]['custom_config']
            py_path = info_json[self['platform']]['py_path']
            bat_path = info_json[self['platform']]['bat_path']
            auto_plugins = info_json[self['platform']]['auto_plugins']
            #print cfg_path, json_path, custom_config, py_path, bat_path, auto_plugins
        else:
            raise Exception("Can not find  Current platform info form info.json")
        plugin_config = r"%s/%s/%s/%s/plugins.json" % (json_path,fileId, self["user_id"], self["task_id"])

        self["model"] = py_path
        self["process"] = py_path + "/process"
        self["plugin_config"] = plugin_config
        self["custom_config"] = custom_config
        maya_batch = os.path.split(self["cg_software_path"])[0]+"\mayabatch.exe"
        self["cg_software_path"] =maya_batch
        

        print "*"*30
        if  self['user_id'] in [1868564]:
            self['cmdStr'] = "\"%(cg_software_path)s\" -command \"python \\\"options={'cg_file':  '%(cg_file)s' , 'cg_info_file': '%(cg_info_file)s', 'cg_software': 'Maya','cg_project':'%(cg_project)s'};import sys;sys.path.insert(0, '%(process)s');from check_all import *;analyze = eval(options['cg_software']+'Analyze(options)');analyze.run();analyze.write_info_file();\\\"\"" % ( self)
        else:
            self['cmdStr'] = "\"%(cg_software_path)s\" -command \"python \\\"options={'cg_file':  '%(cg_file)s' , 'cg_info_file': '%(cg_info_file)s', 'cg_software': 'Maya','cg_project':'%(cg_project)s'};import sys;sys.path.insert(0, '%(model)s');from check_all import *;analyze = eval(options['cg_software']+'Analyze(options)');analyze.run();analyze.write_info_file();\\\"\"" % (self)
        print "+"*30
        return self
    def load_plugins(self):
        plugin_path = os.path.join(self["model"],"function")
        sys.path.append(plugin_path)
        import RayvisionPluginsLoader
        custom_file = self["custom_config"] + "/" + str(self["user_id"]) + "/RayvisionCustomConfig.py"
        print self["plugin_config"]
        plginLd = RayvisionPluginsLoader.RayvisionPluginsLoader()
        plginLd.RayvisionPluginsLoader(self["plugin_config"], [custom_file])

        with open(self["plugin_config"], 'r') as file:
            file_str = file.read()
            plugis_dict = dict(eval(file_str))
            
            if plugis_dict:
                renderSoftware = plugis_dict['renderSoftware']
                softwareVer = plugis_dict['softwareVer']
                plugis_list_dict = plugis_dict['plugins']
                print plugis_list_dict
    
    def run(self):
        self.analyze_list = ["Start","End",'userRenderer','imageFilePrefix',"Ext","dynMemLimit",\
                                'camera','render_camera',"render_layer",'renderable_layer','width',\
                                'height','preMel','postMel','preRenderLayerMel','postRenderLayerMel','preRenderMel','postRenderMel']   
         
        self.texture_node_list = {'file':'fileTextureName','aiImage':'filename','alTriplanar':'texture'} 
        
        
        self.cache_node_list = {'file':'fileTextureName','aiImage':'filename','alTriplanar':'texture',\
                                'AlembicNode':'abc_File','pgYetiMaya':'cacheFileName','aiStandIn':'dso',\
                                'RMSGeoLightBlocker':'Map','VRayMesh':'fileName','VRayLightIESShape':'iesFile',\
                                'diskCache':'cacheName','RealflowMesh':'Path','mip_binaryproxy':'object_filename',\
                                'mentalrayLightProfile':'fileName','aiPhotometricLight':'ai_filename',\
                                'cacheFile':'cachePath','VRayVolumeGrid':'inFile','aiPhotometricLight':'ai_filename'}

        print "[Rayvision]: open maya file " + self["cg_file"]
        
        if self["cg_project"]:
            if os.path.exists(self["cg_project"]):
                workspacemel = os.path.join(self["cg_project"],
                                            "workspace.mel")
                if not os.path.exists(workspacemel):
                    try:
                        with open(workspacemel, "w"):
                            ''
                    except:
                        pass
                        # raise Exception("Can't create empty workspace.mel file "
                        #                 "in project folder")

                if os.path.exists(workspacemel):
                    pm.mel.eval('setProject "%s"' % (self["cg_project"]))       

        
        try:
            cmds.file(self["cg_file"], o=1, force=1, ignoreVersion=1, prompt=0)
        except:
            pass
        print "[Rayvision]: open maya ok."

        
            
        
        #self['userRenderer'] =  cmds.getAttr("defaultRenderGlobals.currentRenderer")
        
        self['camera'] = ",".join(cmds.ls(type="camera"))
        self['render_camera'] = ",".join([i.name() for i in pm.ls(type="camera") if i.renderable.get()]) 
        self["render_layer"] = [ i for i in cmds.listConnections("renderLayerManager.renderLayerId")]        
        print self["render_layer"]
        
        #if user_id not in [1865943]:
        #    if "defaultRenderLayer" not in self["render_layer"]:
        #        print ("Can't find defaultRenderLayer in scene.")
        #        sys.exit(555)
            # raise Exception("Can't find defaultRenderLayer in scene.")
            
        render_node = pm.PyNode("defaultRenderGlobals")
        resolution_settings = pm.PyNode("defaultResolution")
        layer_num = 0
        for render_layer in  self["render_layer"]:
            print render_layer
            try:
                pm.PyNode(render_layer).setCurrent()
                print "switch renderlayer"
                rd_path = pm.PyNode("defaultRenderGlobals").imageFilePrefix.get()
                self["Ext"] = self.GetOutputExt()
                
                render_name = render_node.currentRenderer.get()
                self['userRenderer'] = render_name
                if render_name == "vray":
                    vraySettings_node = pm.PyNode("vraySettings")
                    rd_path = vraySettings_node.fnprx.get()
                    self["dynMemLimit"]  = int(vraySettings_node.sys_rayc_dynMemLimit.get())
                    if vraySettings_node.hasAttr("animType"):
                        if vraySettings_node.animType.get() == 2:
                            raise AssertionError("the renderer is vray , the animType Specific Frames is dont support")                    
                self['imageFilePrefix'] =  rd_path

                #self["layer_name_num%s" % layer_num]={}
                layer_name_num = "layer_name_num%s" % layer_num 
                print layer_name_num
                #self.setdefault(layer_name_num)
                self[layer_name_num]={}
                print self[layer_name_num] 
                self[layer_name_num]["layer_name"] = render_layer
                print self[layer_name_num]["layer_name"]
                self[layer_name_num]["able"]=0
                if pm.PyNode(render_layer).renderable.get():
                    self[layer_name_num]["able"]= 1
                
                self[layer_name_num]["Start"]= int(render_node.startFrame.get())
                self[layer_name_num]["End"]= int(render_node.endFrame.get())
                self[layer_name_num]["Step"]= int(render_node.byFrameStep.get())
                
                self[layer_name_num]["Width"]= resolution_settings.width.get()
                self[layer_name_num]["Height"]= resolution_settings.height.get()

                self['preMel'] = self.unicode_to_str(self.get_pre()[0])
                self['postMel'] = self.unicode_to_str(self.get_pre()[1])
                self['preRenderLayerMel'] = self.unicode_to_str(self.get_pre()[2])
                self['postRenderLayerMel'] = self.unicode_to_str(self.get_pre()[3])
                self['preRenderMel'] = self.unicode_to_str(self.get_pre()[4])
                self['postRenderMel'] = self.unicode_to_str(self.get_pre()[5])
                layer_num += 1
            except Exception as err:
                print  err
                #raise Exception("Can't switch renderlayer " + render_layer)

        # self['texture&cache'] = self.get_cache(self.cache_node_list)
        # self['cache'] = self.get_cache(self.cache_node_list)
        print self
        print '+'*30
        # print self['cache']
        
    def encode_str(self,my_str):
        if my_str:        
            my_str=my_str.encode('unicode-escape').decode('string_escape')
        else:
            my_str = str(None)
        print my_str
        return my_str
        
    def unicode_to_str(self,str1,str_encode = 'system'):
        if isinstance(str1,unicode):
            try:
                if str_encode.lower() == 'system':
                    str1=str1.encode(sys.getfilesystemencoding())
                elif str_encode.lower() == 'utf-8':
                    str1 = str1.encode('utf-8')
                elif str_encode.lower() == 'gbk':
                    str1 = str1.encode('gbk')
                else:
                    str1 = str1.encode(str_encode)
            except Exception as e:
                print '[err]unicode_to_str:encode %s to %s failed' % (str1,str_encode)
                print e
        else:
            print '%s is not unicode ' % (str1)
        return str1
        
    def get_texture_path(self):
        all_image_path = {}
        str_list = []
        if pm.ls(type="file"):
            for i in pm.ls(type="file"):
                j = i.fileTextureName.get()                
                # print  i,j
                file_name = 'file:' + i
                wr_str1 = file_name + '=' + j
                str_list.append(wr_str1)        
        if cmds.ls(exactType ="aiImage"): 
            for a in cmds.ls(exactType ="aiImage"):
                b = cmds.getAttr(a+".filename")
                # print a,b 
                aiImage_name = 'aiImage:' + a
                wr_str = aiImage_name + '=' + b
                str_list.append(wr_str)                 

        return str_list
            # task_json_str = json.dumps(self['Texture'],ensure_ascii=False)


        
    def get_cache(self,node_list_dict):
        str_list = []
        node_type_list = node_list_dict.keys()
        for node_type in node_type_list:
            attr_name = node_list_dict.get(node_type)     
            # node_type='ExocortexAlembicXform'
            # attr_name='fileName'
            all_node = pm.ls(type=node_type)
            if all_node:
                print all_node            
                for node in all_node:                
                    file_path = cmds.getAttr(node + "."+attr_name)
                    if file_path == None:
                        file_path = " "
                    # node.attr(attr_name).set(l=0)
                    # file_path = node.attr(attr_name).get()
                    node_str = node_type + '::' + node 
                    wr_str = node_str + '=' + file_path
                    str_list.append(wr_str)                
                    # print wr_str 
        print '+'*40            
        print str_list             
        return str_list
            
           

    def GetStrippedSceneFileName(self):        
        fileName=str(pm.pm.cmds.file(q=1, sceneName=1))
        fileName=str(pm.mel.basename(fileName, ".mb"))
        fileName=str(pm.mel.basename(fileName, ".ma"))
        return fileName     
        
    def write_result(self,str):  
        writeresult=file(r'D:\eclipse4.4.1 script\my_selenium\model\test_result.log','a+')  
        str1=writeresult.write(str+'\n')  
        writeresult.close()  
        return str         
            
        
    def get_pre(self):
        render_node = pm.PyNode("defaultRenderGlobals")
        preMel = render_node.preMel.get()
        postMel = render_node.postMel.get()
        preRenderLayerMel = render_node.preRenderLayerMel.get()
        postRenderLayerMel = render_node.postRenderLayerMel.get()
        preRenderMel = render_node.preRenderMel.get()
        postRenderMel = render_node.postRenderMel.get()
        return preMel,postMel,preRenderLayerMel,postRenderLayerMel,preRenderMel,postRenderMel

    def GetCurrentRenderer(self):
        """Returns the current renderer."""       
        renderer=str(pm.mel.currentRenderer())
        if renderer == "_3delight":
            renderer="3delight"
            
        return renderer

        
    def GetOutputExt(self):

        renderer = str(self.GetCurrentRenderer())
        if renderer == "vray":
            pm.melGlobals.initVar('string[]', 'g_vrayImgExt')
            # Need to special case vray, because they like to do things differently.
            ext = ""
            if pm.optionMenuGrp('vrayImageFormatMenu', exists=1):
                ext = str(pm.optionMenuGrp('vrayImageFormatMenu', q=1, v=1))


            else:
                ext = str(pm.getAttr('vraySettings.imageFormatStr'))

            if ext == "":
                ext = "png"
                # for some reason this happens if you have not changed the format
                # VRay can append this to the end of the render settings display, but we don't want it in the file name.

            isMultichannelExr = int(False)
            multichannel = " (multichannel)"
            if ext.endswith(multichannel):
                ext = ext[0:-len(multichannel)]
                isMultichannelExr = int(True)

        else:

            if renderer == "renderMan" or renderer == "renderManRIS":
                pat = str(pm.mel.rmanGetImagenamePattern(1))
                # $prefixString = `rmanGetImageName 1`;
                ext = str(pm.mel.rmanGetImageExt(""))

            elif renderer == "mentalRay":
                ext = str(cmds.getAttr("defaultRenderGlobals.imfkey"))

            else:
                ext = str(cmds.getAttr("defaultRenderGlobals.imageFormat"))

        return ext
            
            

class LightWaveAnalyze(Analyze):

    def __init__(self, options):
        super(LightWaveAnalyze, self).__init__(options)

    def run(self):
        start_re = re.compile(r'FirstFrame +(\d+)', re.I)
        end_re = re.compile(r'LastFrame +(\d+)', re.I)

        output_re_list = [re.compile(r'SaveAnimationName +(.+)\\.+?\.avi$', re.I),
                          re.compile(r'SaveRGBImagesPrefix +(.+)[/\\][\w ]+$', re.I),
                          re.compile(r'SaveAlphaImagesPrefix +(.+)[/\\][\w ]+$', re.I)]

        ok_file = os.path.splitext(self["cg_file"])[0] + "_rayvision.lws"
        output = r"c:\work\render\%s\output" % (self["task_id"])

        with open(self["cg_file"]) as f:
            with open(ok_file, "w") as f_ok:
                for line in f:
                    if line and line.strip():
                        if start_re.findall(line):
                            self["start"] = start_re.findall(line)[0]
                        elif end_re.findall(line):
                            self["end"] = end_re.findall(line)[0]

                    for i_re in output_re_list:
                        if i_re.findall(line):
                            print "Old: " + line
                            sys.stdout.flush()
                            line = line.replace(i_re.findall(line)[0], output)
                            print "New: " + line
                            sys.stdout.flush()
                            break
                    f_ok.write(line)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'rayvision web submit check python')
    parser.add_argument("--cgsw", dest="cg_software", type=str)
    parser.add_argument("--ui", dest="user_id", type=int)
    parser.add_argument("--ti", dest="task_id", type=int)
    parser.add_argument("--sfp", dest="cg_software_path", type=str)
    parser.add_argument("--proj", dest="cg_project", type=str)
    parser.add_argument("--cgfile", dest="cg_file", type=str)
    parser.add_argument("--cg_info_file", dest="cg_info_file", type=str)
    parser.add_argument("--pt", dest="platform", type=int)
    
    options = parser.parse_args().__dict__
    print "*"*30
    print options['user_id']
    print "*"*30
    analyze = eval(options["cg_software"]+"Analyze(options)")
    if options["cg_software"] == "Maya":
        opt= analyze.get_info()
        analyze.load_plugins() 
        RBcmd(opt['cmdStr'],False,False)    
    else:
        analyze.run()
        analyze.write_info_file()
