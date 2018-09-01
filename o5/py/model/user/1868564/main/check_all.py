#!/usr/bin/env python
#encoding:utf-8
# -*- coding: utf-8 -*-
import os
import sys
import re
import subprocess
import json
import platform
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

class Maya(object):
    def __init__(self):
        currentPath = os.path.split(os.path.realpath(__file__))[0].replace('\\', '/')
        currentPath = currentPath.lower()
        if "user" in currentPath:
            process_path = os.path.join(currentPath.split('user')[0], "process")
            function_path = os.path.join(currentPath.split('user')[0], "function")
            script_path = os.path.join(currentPath.split('user')[0], "script")

        else:
            process_path = currentPath
            function_path = currentPath.replace("process", "function")
            script_path = currentPath.replace("process", "script")
        self.info_json = os.path.join(process_path, 'info.json')
        print "json_path : %s" % self.info_json

    def convertStr2Unicode(self,str):
        if not isinstance(str, unicode):
            str=str.decode(sys.getfilesystemencoding())
        return str

    def convertUnicode2Str(self,uStr):
        print type(uStr)
        CURRENT_OS = platform.system()
        if isinstance(uStr, unicode):
            if CURRENT_OS == 'Linux':
                uStr=uStr.encode('utf-8')
            else:
                uStr=uStr.encode(sys.getfilesystemencoding())
            print type(uStr)
            return uStr
        else:
            return uStr

    def get_platfom(self, platform):
        platform = str(platform)
        info_dict = {}
        with open(self.info_json, 'r') as fn:
            fn_dict = json.load(fn)
            info_dict = fn_dict[platform]
        info_dict["auto_plugins"] = info_dict["auto_plugins"].replace("/", "\\")
        return info_dict


    def print_info(self, info):
        print (info)

    def print_info_err(self, info):
        info = self.convertUnicode2Str(info)
        print ("[Analyze Error]%s" % (self.unicode_to_str(info)))


    def unicode_to_str(self, str1, str_encode='system'):
        if str1 == None or str1 == "" or str1 == 'Null' or str1 == 'null':
            str1 = ""
            return str1
        elif isinstance(str1, unicode):
            try:
                if str_encode.lower() == 'system':
                    str1 = str1.encode(sys.getfilesystemencoding())
                elif str_encode.lower() == 'utf-8':
                    str1 = str1.encode('utf-8')
                elif str_encode.lower() == 'gbk':
                    str1 = str1.encode('gbk')
                else:
                    str1 = str1.encode(str_encode)
            except Exception as e:
                print ('[err]unicode_to_str:encode %s to %s failed' % (str1, str_encode))
                print (e)
        elif isinstance(str1, str):
            return str1
        else:
            print ('%s is not unicode ' % (str1))
        return str(str1)

    
    def RBcmd(self,cmdStr, continueOnErr = False, myShell = False):
        print ('cmd...' + cmdStr)
        cmdp = subprocess.Popen(cmdStr,stdin = subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.STDOUT, shell = myShell)
        cmdp.stdin.write('3/n')
        cmdp.stdin.write('4/n')
        exitcode = 0
        while cmdp.poll() is None:
            resultLine = cmdp.stdout.readline().strip()
            
            if resultLine != '':
                print resultLine
            if "fatal flex scanner internal error--end of buffer missed" in resultLine:
                self.print_info_err("Please Check that the file is uploaded intact")

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

    def get_encode(self, encode_str):
        for code in ["utf-8", sys.getfilesystemencoding(), "gb18030", "ascii", "gbk", "gb2312"]:
            try:
                encode_str.decode(code)
                return code
            except:
                pass

    def to_gbk(self, encode_str):
        if isinstance(encode_str, str):
            return encode_str
        else:
            code = self.get_encode(encode_str)
            return encode_str.decode(code).encode('GBK')
  
class MayaAnalyze(dict,Maya):

    def __init__(self, options):
        dict.__init__(self)
        Maya.__init__(self)
        for i in options:
            self[i] = options[i]

   
    def get_info(self):
        fileId = str(self["user_id"] - self["user_id"]%500)
        self["platform"] = str(self["platform"])
        info_json = self.get_platfom(self["platform"])
        cfg_path = info_json['cfg_path']
        json_path = info_json['json_path']
        custom_config = info_json['custom_config']
        py_path = info_json['py_path']
        bat_path = info_json['bat_path']
        auto_plugins = info_json['auto_plugins']
        plugin_config = r"%s/%s/%s/%s/plugins.json" % (json_path,fileId, self["user_id"], self["task_id"])
        self["model"] = py_path
        self["process"] = os.path.split(os.path.realpath(__file__))[0].replace('\\', '/')
        self["plugin_config"] = plugin_config
        self["custom_config"] = custom_config
        maya_batch = os.path.split(self["cg_software_path"])[0]+"/mayabatch.exe"
        self["cg_software_path"] =maya_batch
        self['cmdStr'] = "\"%(cg_software_path)s\" -command \"python \\\"options={'cg_file':  '%(cg_file)s' , 'cg_info_file': '%(cg_info_file)s', 'cg_software': 'Maya','cg_project':'%(cg_project)s'};import sys;sys.path.insert(0, '%(process)s');from check_all import *;analyze = eval(options['cg_software']+'Analyze(options)');analyze.run();analyze.write_info_file();\\\"\"" % ( self)
        self.analyse_cmd = "\"%(cg_software_path)s\" -command \"python \\\"options={'cg_file':  '%(cg_file)s' , 'cg_info_file': '%(cg_info_file)s', 'cg_software': 'Maya','cg_project':'%(cg_project)s'};import sys;sys.path.insert(0, '%(process)s');from check_all import *;analyze = MayaAnalyze(options);analyze.config();\\\"\"" % (self)


    def check_maya_file_intact(self):
        #检查maya渲染文件是否上传完整
        maya_file = self["cg_file"]
        last_line_temp_ma = "// End of %s" % os.path.basename(maya_file)
        if os.path.exists(self["cg_file"]):
            if maya_file.endswith(".ma"):
                maya_file_last_line = self.get_file_last_line(maya_file)
                if last_line_temp_ma not in maya_file_last_line:
                    self.print_info_err("MA file`s last line is %s" % maya_file_last_line)
                    self.print_info_err("%s  might be incomplete and corrupt."%maya_file)
                    self.print_info_err("文件没有上传完整，请重新上传")
                    sys.exit(555)

            elif maya_file.endswith(".mb"):
                pass

    def get_file_last_line(self,inputfile):
        filesize = os.path.getsize(inputfile)
        blocksize = 1024
        with open(inputfile, 'rb') as f:
            last_line = ""
            if filesize > blocksize:
                maxseekpoint = (filesize // blocksize)
                f.seek((maxseekpoint - 1) * blocksize)
            elif filesize:
                f.seek(0, 0)
            lines = f.readlines()
            if lines:
                lineno = 1
                while last_line == "":
                    last_line = lines[-lineno].strip()
                    lineno += 1
            return last_line


    def load_plugins(self):
        plugin_path = os.path.join(self["model"], "function")
        sys.path.append(plugin_path)
        from MayaPlugin import MayaPlugin
        with open(self["plugin_config"], 'r') as file:
            file_str = file.read()
            plugis_dict = dict(eval(file_str))
            
            if plugis_dict:
                renderSoftware = plugis_dict['renderSoftware']
                softwareVer = plugis_dict['softwareVer']
                plugis_list_dict = plugis_dict['plugins']
                print plugis_list_dict
           
        print "--------------------Set Plugins start---------------------------"

        print self["plugin_config"]
        if self["plugin_config"]:
            if "gpu_card_no" in os.environ:
                print "gpu_card_no: " + os.environ["gpu_card_no"]
            else:
                print "gpu_card_no variable is not exists."

            custom_file = self["custom_config"] + "/" + str(self["user_id"]) + "/RayvisionCustomConfig.py"
            if os.path.exists(custom_file):
                print "[Custom_config] is: " + custom_file
            else:
                print ("Can`t find %s" % custom_file)
            print "[Plugin path]:"
            print self["plugin_config"]
            maya_plugin = MayaPlugin(self["plugin_config"], [custom_file], self["user_id"],
                                     self["task_id"])
            maya_plugin.config()
            sys.stdout.flush()
            if "MAYA_SCRIPT_PATH" in os.environ:
                print "MAYA_SCRIPT_PATH: " + os.environ["MAYA_SCRIPT_PATH"]
            sys.stdout.flush()
        print "--------------------Set Plugins  end---------------------------"
    
    def config(self):
        self.start_open_maya()
        self.analyze_render_setting()
        self.write_info_file()
    
    def main(self):
        '''
        :return:
        '''
        self.get_info()
        self.check_maya_file_intact()
        self.load_plugins()
        analyze_result =  self.RBcmd(self.analyse_cmd,False,False)
        print analyze_result
    
    def start_open_maya(self):
        self.print_info("start open maya file: " + self["cg_file"])
        self["cg_project"] = os.path.normpath(self["cg_project"]).replace('\\', '/')
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
                if os.path.exists(workspacemel):
                    pm.mel.eval('setProject "%s"' % (self["cg_project"]))
        # ignore some open maya errors.
        if os.path.exists(self["cg_file"]) and os.path.isfile(self["cg_file"]):
            try:
                # pm.openFile(options["cg_file"], force=1, ignoreVersion=1, prompt=0, loadReferenceDepth="all")
                cmds.file(self["cg_file"], o=1, force=1, ignoreVersion=1, prompt=0)
                # pm.openFile(self["cg_file"], force=1, ignoreVersion=1, prompt=0)
                self.print_info("open maya file ok.")
            except:
                pass
        else:
            raise Exception("Dont Found the maya files error.")

    def analyze_render_setting(self):

        #self['userRenderer'] =  cmds.getAttr("defaultRenderGlobals.currentRenderer")
        
        self['camera'] = ",".join(cmds.ls(type="camera"))
        self['render_camera'] = ",".join([i.name() for i in pm.ls(type="camera") if i.renderable.get()]) 
        self["render_layer"] = [ i for i in cmds.listConnections("renderLayerManager.renderLayerId")]        
        print self["render_layer"]

        all_render_layer = cmds.listConnections("renderLayerManager.renderLayerId")
        if "defaultRenderLayer" not in all_render_layer:
            self.print_info(all_render_layer)
            self.print_info_err("Can't find defaultRenderLayer in scene.")
            sys.exit(555)
            
        render_node = pm.PyNode("defaultRenderGlobals")
        resolution_settings = pm.PyNode("defaultResolution")
        layer_num = 0
        for render_layer in  self["render_layer"]:
            print ("[Analyze]>> %s " % render_layer)
            try:
                pm.PyNode(render_layer).setCurrent()
                print "switch renderlayer"
                rd_path = pm.PyNode("defaultRenderGlobals").imageFilePrefix.get()
                self["Ext"] = self.get_image_format()
                render_name = render_node.currentRenderer.get()
                self['userRenderer'] = render_name
                if render_name == "vray":
                    vraySettings_node = pm.PyNode("vraySettings")
                    rd_path = vraySettings_node.fnprx.get()
                    self["dynMemLimit"]  = int(vraySettings_node.sys_rayc_dynMemLimit.get())
                    if vraySettings_node.hasAttr("animType"):
                        if vraySettings_node.animType.get() == 2:
                            raise AssertionError("the renderer is vray , the animType Specific Frames is dont support")

                    if vraySettings_node.hasAttr("productionEngine"):
                        productionEngine_dict = {0: "CPU", 1: "OpenCL", 2: "CUDA"}
                        productionEngine = vraySettings_node.productionEngine.get()
                        if productionEngine != 0 and self["platform"] != "1016":
                            print ("Current Platform is CPU ,Vray  productionEngine is %s" % productionEngine_dict[productionEngine])
                            sys.exit(555)
                        
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
                self.print_info_err(err)
                sys.exit(555)
                #raise Exception("Can't switch renderlayer " + render_layer)

        print '+'*30
 
    def encode_str(self,my_str):
        if my_str:        
            my_str=my_str.encode('unicode-escape').decode('string_escape')
        else:
            my_str = str(None)
        print my_str
        return my_str

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

    def get_image_format(self):
        render_engine = str(self.GetCurrentRenderer())
        if render_engine == 'arnold':
            return cmds.getAttr('defaultArnoldDriver.aiTranslator')
        if render_engine == 'redshift':
            redshift_format_number = cmds.getAttr('redshiftOptions.imageFormat')
            redshift_Image_format = {
                0: 'iff',
                1: 'exr',
                2: 'png',
                3: 'tga',
                4: 'jpg',
                5: 'tif'}
            return redshift_Image_format.get(redshift_format_number)
        if render_engine == 'vray':
            vray_format = pm.getAttr('vraySettings.imageFormatStr')
            if vray_format == None:
                return 'png'
            return vray_format
        if render_engine == 'mentalRay' or render_engine == 'mayaSoftware' or render_engine == 'mayaHardware' or render_engine == 'mayaHardware2' or render_engine == 'turtle':
            Image_format_number = cmds.getAttr("defaultRenderGlobals.imageFormat")
            Image_Format = {
                0: 'gif',
                1: 'pic',
                2: 'rla',
                3: 'tif',
                4: 'tif16',
                5: 'sgi',
                6: 'als',
                7: 'iff',
                8: 'jpg',
                9: 'eps',
                10: 'iff16',
                11: 'cin',
                12: 'yuv',
                13: 'sgi16',
                16: 'sgi16',
                19: 'tga',
                20: 'bmp',
                23: 'avi',
                31: 'psd',
                32: 'png',
                35: 'dds',
                36: 'Layered(psd)',
                51: 'exr'}
            return Image_Format.get(Image_format_number)
        if render_engine == 'renderManRIS' or render_engine == 'renderMan':
            Image_format_number = cmds.getAttr("rmanFinalOutputGlobals0.rman__riopt__Display_type")
            return Image_format_number

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

    def write_info_file(self):
        info_file_path = os.path.dirname(self["cg_info_file"])
        if not os.path.exists(info_file_path):
            os.makedirs(info_file_path)
    
        with open(self["cg_info_file"], "w") as f:
            # f.write("Start::%s\n" % (self["Start"]))
            f.flush()
            # f.write("End::%s\n" % (self["End"]))
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
                    Layer_str = "%s::%s::%s::%s::%s::%s::%s::%s \n" % (
                    key.replace(key, "Layer"), self[key]["layer_name"], self[key]["Start"], self[key]["End"],
                    self[key]["Step"], self[key]["Width"], self[key]["Height"], self[key]["able"])
                    print Layer_str
                    f.write(Layer_str)
                    f.flush()
            f.flush()
            print "write cg_info_file"
            cmds.quit(force=True)
        cmds.quit(force=True)


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
    analyze = MayaAnalyze(options)
    analyze.main()
    print "check_all end....................."