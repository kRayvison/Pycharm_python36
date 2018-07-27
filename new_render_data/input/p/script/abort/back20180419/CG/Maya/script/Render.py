#!/usr/bin/env python
#encoding:utf-8
# -*- coding: utf-8 -*-

import pymel.core as pm
import maya.cmds as cmds
import maya.mel as mel
import os,sys,re
import logging


    
  


class PreRender(object):
    
    def __init__(self, mylog=None):     

        self.errReturn = 0
        self.log = mylog
        self.customprerender=os.path.join(self.G_NODE_PY,'CG',self.G_CG_NAME,'script','CustomPrerender.py')
        #-----------------------------------------log-----------------------------------------------
        self.G_DEBUG_LOG=logging.getLogger('debug_log')
        self.G_RENDER_LOG=logging.getLogger('render_log')
        
        #-------------global vars-------------
        self.MAYA_PROJ_PATH = cmds.workspace(q=True, fullName=True)
        self.SOURCE_PATH = "%s/sourceimages" % (self.MAYA_PROJ_PATH)
        self.SCENES_PATH = "%s/scenes" % (self.MAYA_PROJ_PATH)
        
        self.RENDER_NODE = pm.PyNode("defaultRenderGlobals")
        self.RENDER_ARNOLD_DRIVER_NODE = pm.PyNode("defaultArnoldDriver")
        
        yeti_load = cmds.pluginInfo("pgYetiMaya", query=True, loaded=True )
        yeti_vray_load = cmds.pluginInfo("pgYetiVRayMaya", query=True, loaded=True )
        shave_load = cmds.pluginInfo("shaveNode", query=True, loaded=True )

        rep_path = ""
        search = ""
        dicts = {}         
        #-----------unlock   node------
        pm.lockNode( 'defaultRenderGlobals', lock=False )
        
        
    def mylog(self,message,extr="PreRender"):
        if self.log:
            self.log.info("[%s] %s"%(extr,str(message)))         
        else:        
            if str(message).strip() != "":
                print("[%s] %s"%(extr,str(message)))
            
            

            
    def doCustomPrerender(self):     
        # Check is the config file exists ----------------------------------
        if os.path.exists(self.customprerender):
            self.mylog('custom prerender  \'s config path : %s' % self.customprerender)
            
            cfgFileDir = os.path.dirname(self.customprerender)
            cfgFileName = os.path.splitext(os.path.split(self.customprerender)[-1])[0]
            print cfgFileName
            sys.path.append(cfgFileDir)          
            
            try:
                cfg = __import__('CustomPrerender')
                reload(cfg)
                cfg.main()                            
            except Exception as err:
                self.mylog('=== Error occur import/execute "%s"! ===\n=== Error Msg : %s ===' % (self.customprerender, err))
            try:
                while True:
                    sys.path.remove(cfgFileDir)
                    
            except:
                pass

        else:
            self.mylog('Config file %s is not exists!' %self.customprerender )


            
    def GetCurrentRenderer(self):
        """Returns the current renderer."""
        

        renderer=str(pm.mel.currentRenderer())
        if renderer == "_3delight":
            renderer="3delight"
            
        return renderer




    def GetOutputPrefix(self,replaceFrameNumber, newFrameNumber, layerName, cameraName, renderElement):
        """Returns the output prefix as is shown in the Render Globals, except that the frame
        number is replaced with '?' padding.
        lobal proc string GetOutputPrefix( int $replaceFrameNumber, int $newFrameNumber )"""
        

        outputPrefix=""
        paddingString=""
        renderer=str(self.GetCurrentRenderer())
        renderableCameras= ",".join([i.name() for i in pm.ls(type="camera") if i.renderable.get()]) 
        multipleRenderableCams=(len(renderableCameras)>1)
        if renderer == "vray":
            pm.melGlobals.initVar('string[]', 'g_vrayImgExt')
            # Need to special case vray, because they like to do things differently.
            ext=""
            if pm.optionMenuGrp('vrayImageFormatMenu', exists=1):
                ext=str(pm.optionMenuGrp('vrayImageFormatMenu', q=1, v=1))
                
            
            else:
                ext=str(pm.getAttr('vraySettings.imageFormatStr'))
                
            if ext == "":
                ext="png"
                #for some reason this happens if you have not changed the format
                # VRay can append this to the end of the render settings display, but we don't want it in the file name.
                
            isMultichannelExr=int(False)
            multichannel=" (multichannel)"
            if ext.endswith(multichannel):
                ext=ext[0:-len(multichannel)]
                isMultichannelExr=int(True)
                
            versionString=str(pm.mel.vray('version'))
            version=2
            minorVersion=0
            if versionString != "":
                buffer = []
                buffer=versionString.split(".")
                version=int(int(buffer[0]))
                minorVersion=int(int(buffer[1]))
                
            prefix=str(pm.getAttr('vraySettings.fileNamePrefix'))
            # We need to use eval because the definition of vrayTransformFilename is different for
            # different versions of vray, and this is the only way to get around the "incorrect
            # number of arguments" error.
            separateFolders=int(pm.getAttr("vraySettings.relements_separateFolders"))
            separateRGBA=0
            if not pm.catch(lambda: pm.getAttr("vraySettings.relements_separateRGBA")):
                separateRGBA=int(pm.getAttr("vraySettings.relements_separateRGBA"))
                
            if prefix == "":
                prefix=str(pm.mel.GetStrippedSceneFileName())
                '''
                if( IsOldVray() )
                    $prefix = eval( "vrayTransformFilename( \"" + $prefix + "\", \"\" )" );
                else
                    $prefix = eval( "vrayTransformFilename( \"" + $prefix + "\", \"\", \"\" )" );
                '''
                
            if renderElement != "" and separateFolders:
                tempPrefix=str(pm.mel.dirname(prefix))
                if tempPrefix != "":
                    tempPrefix=tempPrefix + "/"
                    
                prefix=tempPrefix + renderElement + "/" + str(pm.mel.basename(prefix, ""))
                
            
            elif renderElement == "" and separateFolders and separateRGBA:
                tempPrefix=str(pm.mel.dirname(prefix))
                if tempPrefix != "":
                    tempPrefix=tempPrefix + "/"
                    
                prefix=tempPrefix + "rgba/" + str(pm.mel.basename(prefix, ""))
                
            if multipleRenderableCams and (pm.mel.match("<Camera>", prefix) == "") and (pm.mel.match("<camera>", prefix) == "") and (pm.mel.match("%c", prefix) == ""):
                prefix="<Camera>/" + prefix
                
            if pm.mel.IsRenderLayersOn() and (pm.mel.match("<Layer>", prefix) == "") and (pm.mel.match("<layer>", prefix) == "") and (pm.mel.match("%l", prefix) == ""):
                prefix="<Layer>/" + prefix
                
            if prefix != "":
                if not pm.catch(lambda: pm.mel.eval("vrayTransformFilename( \"\", \"\", \"\", 0, 0 )")):
                    sceneName=str(pm.mel.GetStrippedSceneFileName())
                    # Don't transform if the prefix is blank, so we can just default to the scene file name.
                    # Vray strips off all extensions in the scene name when replacing the <Scene> tag.
                    if version<3 or (version == 3 and minorVersion == 0):
                        sceneName=str(pm.mel.basenameEx(sceneName))
                        
                    prefix=str(pm.mel.eval("vrayTransformFilename( \"" + prefix + "\", \"" + cameraName + "\", \"" + sceneName + "\", 0, 0 )"))
                    
                
                elif not pm.catch(lambda: pm.mel.eval("vrayTransformFilename( \"\", \"\", \"\", 0 )")):
                    sceneName=str(pm.mel.GetStrippedSceneFileName())
                    # Vray strips off all extensions in the scene name when replacing the <Scene> tag.
                    if version<3 or (version == 3 and minorVersion == 0):
                        sceneName=str(pm.mel.basenameEx(sceneName))
                        
                    prefix=str(pm.mel.eval("vrayTransformFilename( \"" + prefix + "\", \"" + cameraName + "\", \"" + sceneName + "\", 0 )"))
                    
                
                elif not pm.catch(lambda: pm.mel.eval("vrayTransformFilename( \"\", \"\", \"\" )")):
                    prefix=str(pm.mel.eval("vrayTransformFilename( \"" + prefix + "\", \"\", \"\" )"))
                    
                
                elif not pm.catch(lambda: pm.mel.eval("vrayTransformFilename( \"\", \"\" )")):
                    prefix=str(pm.mel.eval("vrayTransformFilename( \"" + prefix + "\", \"\" )"))
                    
                
                else:
                    print "Could not evaluate output path using vrayTransformFilename, please contact Deadline support and include the version of vray you are using\n"
                    
                
            if renderElement != "" and isMultichannelExr == 0:
                prefix=prefix + str((pm.getAttr("vraySettings.fileNameRenderElementSeparator"))) + renderElement
                #if( catchQuiet( eval( "vrayTransformFilename( \"" + $prefix + "\", \"\", \"\" )" ) ) )
                #{
                #	if( catchQuiet( eval( "vrayTransformFilename( \"" + $prefix + "\", \"\" )" ) ) )
                #		$prefix = `getAttr vraySettings.fileNamePrefix`;
                #}
                #if( $prefix == "" )
                #	$prefix = GetStrippedSceneFileName();
                
            
            elif renderElement == "" and separateFolders and separateRGBA and isMultichannelExr == 0:
                prefix=prefix + str((pm.getAttr("vraySettings.fileNameRenderElementSeparator"))) + "rgba"
                
            if pm.mel.IsAnimatedOn():
                padding=4
                # Seems to be a bug where no matter what, VRay will use 4 digits for padding.
                # If ever fixed, try using the value from the vray settings.
                #int $padding = `getAttr vraySettings.fileNamePadding`;
                if version>=3:
                    padding=int(pm.getAttr('vraySettings.fileNamePadding'))
                    
                for i in range(0,padding):
                    paddingString=paddingString + "#"
                    # When rendering to a non-raw format, vray places a period before the padding, even though it
                    # doesn't show up in the render globals filename.
                    
                if ext == "vrimg" or (isMultichannelExr and version<3):
                    outputPrefix=prefix + paddingString + "." + ext
                    
                
                else:
                    outputPrefix=prefix + "." + paddingString + "." + ext
                    
                
            
            elif ext == "vrimg" or (isMultichannelExr and version<3):
                outputPrefix=prefix + "." + ext
                # When rendering to a non-raw format, vray places a period before the padding, even though it
                # doesn't show up in the render globals filename.
                
            
            else:
                outputPrefix=prefix + "." + ext
                
            
        
        else:
            paddingFound=0
            # Get the first output prefix.
            prefixString=""
            if renderer == "renderMan" or renderer == "renderManRIS":
                if cameraName == "":
                    pat=str(pm.mel.rmanGetImagenamePattern(1))
                    #$prefixString = `rmanGetImageName 1`;
                    ftext=str(pm.mel.rmanGetImageExt(""))
                    prefixString=str(pm.mel.rman("assetref", "-cls", "Final", "-assetnmpat", pat, "-ref", "$ASSETNAME", "-LAYER", layerName, "-EXT", ftext, "-DSPYID", "", "-DSPYCHAN", ""))
                    
                
                else:
                    cameraRelatives=pm.listRelatives(cameraName, s=1)
                    camera=cameraRelatives[0]
                    pat=str(pm.mel.rmanGetImagenamePattern(1))
                    ftext=str(pm.mel.rmanGetImageExt(""))
                    prefixString=str(pm.mel.rman("assetref", "-cls", "Final", "-assetnmpat", pat, "-ref", "$ASSETNAME", "-LAYER", layerName, "-CAMERA", camera, "-EXT", ftext, "-DSPYID", "", "-DSPYCHAN", ""))
                    
                
            
            elif renderer == "MayaKrakatoa":
                prefixes=pm.renderSettings(fin=1, cam=cameraName, lyr=layerName)
                #string $prefixes[] = `renderSettings -fin`;
                prefixString=prefixes[0]
                forceEXROutput=int(pm.getAttr("MayaKrakatoaRenderSettings.forceEXROutput"))
                if forceEXROutput == 1:
                    tokens = []
                    tokens=prefixString.split(".")
                    result=""
                    i = 0
                    for i in range(0,len(tokens) - 1):
                        result+=tokens[i] + "."
                        
                    prefixString=result + "exr"
                    
                
            
            else:
                currentPrefix=str(pm.getAttr('defaultRenderGlobals.imageFilePrefix'))
                newPrefix=currentPrefix
                if newPrefix == "":
                    newPrefix=str(pm.mel.GetStrippedSceneFileName())
                    
                if renderer == "arnold" and pm.mel.match("<RenderPass>", newPrefix) == "":
                    elements=pm.mel.getArnoldElementNames()
                    if elements[0] != "":
                        newPrefix="<RenderPass>/" + newPrefix
                        
                    
                if renderer == "mentalRay" and pm.mel.match("<RenderPass>", newPrefix) == "":
                    elements=pm.mel.getMentalRayElementNames(layerName)
                    if elements[0] != "":
                        newPrefix="<RenderPass>/" + newPrefix
                        
                    
                if multipleRenderableCams and (pm.mel.match("<Camera>", newPrefix) == "") and (pm.mel.match("%c", newPrefix) == ""):
                    newPrefix="<Camera>/" + newPrefix
                    
                if pm.mel.IsRenderLayersOn() and (pm.mel.match("<RenderLayer>", newPrefix) == "") and (pm.mel.match("<Layer>", newPrefix) == "") and (pm.mel.match("%l", newPrefix) == ""):
                    newPrefix="<RenderLayer>/" + newPrefix
                    
                pm.setAttr("defaultRenderGlobals.imageFilePrefix", newPrefix, type="string")
                #string $prefixes[] = `renderSettings -fin`;
                prefixes=pm.renderSettings(fin=1, cam=cameraName, lyr=layerName, cts=("RenderPass=" + renderElement))
                prefixString=prefixes[0]
                pm.setAttr("defaultRenderGlobals.imageFilePrefix", currentPrefix, type="string")
                
            prefixWithColons=""
            # Go through each letter of the prefix and create a new prefix with each letter
            # separated by colons, ie: f:i:l:e:n:a:m:e:.:e:x:t:
            for i in range(1,len(prefixString)+1):
                prefixWithColons+=prefixString[i-1:i] + ":"
                # Now split up the new prefix into an array, which removes all the colons and
                # places one letter in each index. Then count backwards and replace the first
                # group of numbers with the padding characters.
                
            prefix=prefixWithColons.split(":")
            if pm.mel.IsAnimatedOn():
                for i in range(len(prefix),0,-1):
                    if pm.mel.match("[0-9]", prefix[i]) != "":
                        prefix[i]="#"
                        paddingString=paddingString + "#"
                        paddingFound=1
                        
                    
                    elif paddingFound:
                        if prefix[i] == "-":
                            prefix[i]="#"
                            paddingString=paddingString + "#"
                            
                        break
                        
                    
                
            outputPrefix="".join(prefix)
            # Finally, convert the prefix array back to a string.
            if renderer == "maxwell" and renderElement != "":
                prefixParts=outputPrefix.split(".")
                numParts=len(prefixParts)
                mainPart=numParts - 2
                if pm.mel.IsAnimatedOn():
                    mainPart-=1
                    
                prefixParts[mainPart]=prefixParts[mainPart] + "_" + renderElement
                extNumber=0
                if renderElement == "zbuffer":
                    extNumber=int(pm.getAttr('maxwellRenderOptions.depthChannelFormat'))
                    
                
                elif renderElement == "object":
                    extNumber=int(pm.getAttr('maxwellRenderOptions.objIDChannelFormat'))
                    
                
                elif renderElement == "material":
                    extNumber=int(pm.getAttr('maxwellRenderOptions.matIDChannelFormat'))
                    
                
                elif renderElement == "motion":
                    extNumber=int(pm.getAttr('maxwellRenderOptions.motionVectorChannelFormat'))
                    
                
                elif renderElement.startswith("customAlpha_"):
                    extNumber=int(pm.getAttr('maxwellRenderOptions.customAlphaChannelFormat'))
                    
                
                else:
                    extNumber=int(pm.getAttr("maxwellRenderOptions." + renderElement + "ChannelFormat"))
                    
                prefixParts[numParts - 1]=str(pm.mel.getMaxwellChannelExtension(extNumber, True))
                outputPrefix=".".join(prefixParts)
                
            
            elif renderer == "maxwell":
                format=int(pm.getAttr('defaultRenderGlobals.imageFormat'))
                outputPrefix=outputPrefix[0:-3]
                outputPrefix=outputPrefix + str(pm.mel.getMaxwellChannelExtension(format, False))
                
            
        if pm.mel.IsAnimatedOn() and replaceFrameNumber:
            paddedFrame="" + str(newFrameNumber)
            while len(paddedFrame)<len(paddingString):
                paddedFrame="0" + paddedFrame
                
            
            outputPrefix=str(pm.mel.substituteAllString(outputPrefix, paddingString, paddedFrame))
            
        return outputPrefix
        

    def IsRenderLayersOn():
        """Returns if render layers is on."""
        

        renderLayers=pm.ls(exactType="renderLayer")
        referenceLayers=pm.ls(exactType="renderLayer", rn=1)
        return ((len(renderLayers) - len(referenceLayers))>1)
        


    def getRenderableRenderLayers(onlyReferenced):
        
        renderLayerList=pm.ls(exactType="renderLayer")
        # Loop through the render layer if the checkbox is on
        renderableLayers=[]
        for layer in renderLayerList:
            renderable=int(pm.getAttr(str(layer) + ".renderable"))
            # Only get output if the renderable attribute is on
            if renderable:
                isReferenceLayer=int(pm.referenceQuery(layer, inr=1))
                if isReferenceLayer and onlyReferenced:
                    renderableLayers.insert(0,layer)
                    
                
                elif not isReferenceLayer and not onlyReferenced:
                    renderableLayers.insert(0,layer)
                    
                
            
        return renderableLayers
        
        
    def CheckSlashes(filename):
        """Ensures that all slashes are consistent throughout the filename."""
        

        result=filename
        #string $result = substituteAllString( $filename, "\\", "/" ); // switch from '\' to '/'
        #$result = substituteAllString( $result, "//", "/" ); // replace double '/' where paths may have been combined
        #if( startsWith( $result, "/" ) )
        #	$result = "/" + $result;
        #return $result;
        newResult = ""
        newResult=result.replace("\\\\","/")
        while newResult != result:
            result=newResult
            newResult=result.replace("\\\\","/")
            
        
        result=newResult
        newResult=result.replace("//","/")
        while newResult != result:
            result=newResult
            newResult=result.replace("//","/")
            
        
        if pm.about(ntOS=1):
            if newResult.startswith("/"):
                newResult="/" + newResult
                
            
        return newResult        
        
    def GetStrippedSceneFileName():
        
        fileName=str(pm.pm.cmds.file(q=1, sceneName=1))
        fileName=str(pm.mel.basename(fileName, ".mb"))
        fileName=str(pm.mel.basename(fileName, ".ma"))
        return fileName        


        
    def ConductMel(): 
        print '++++++++++++++++++pre_layer_mel +++++++++++++++++++++++++++++'
        # if "pgYetiMaya" in plugins and "vrayformaya" in plugins:
            # cmds.loadPlugin( "vrayformaya")
            # cmds.loadPlugin( "pgYetiVRayMaya")   
        render_node=pm.PyNode("defaultRenderGlobals")
        render_name = render_node.currentRenderer.get()
        yeti_load=cmds.pluginInfo("pgYetiMaya", query=True, loaded=True )
        print "the yeti load is %s " % yeti_load
        yeti_vray_load=cmds.pluginInfo("pgYetiVRayMaya", query=True, loaded=True )
        print "the yeti_vray_load load is %s " % yeti_vray_load
        shave_load=cmds.pluginInfo("shaveNode", query=True, loaded=True )
        print "the shave_load load is %s " % shave_load
        

        render_node.postMel.set(l=0)
        render_node.preRenderLayerMel.set(l=0)
        render_node.postRenderLayerMel.set(l=0)
        render_node.preRenderMel.set(l=0)
        render_node.postRenderMel.set(l=0)
        

        preMel = render_node.preMel.get()
        postMel = render_node.postMel.get()
        preRenderLayerMel = render_node.preRenderLayerMel.get()
        postRenderLayerMel = render_node.postRenderLayerMel.get()
        preRenderMel = render_node.preRenderMel.get()
        postRenderMel = render_node.postRenderMel.get()

        

 
        
        if render_name=="vray":

            print "++++++++++++++++ the renderer is vray+++++++++++++++++++++"
            if yeti_load and  yeti_vray_load and shave_load==False:
                mel.eval('pgYetiVRayPreRender;')
                print render_node.postMel.get()
            if shave_load and yeti_load==False :
                mel.eval('shaveVrayPreRender;')
            if yeti_load and  yeti_vray_load and shave_load:
                mel.eval('shaveVrayPreRender;pgYetiVRayPreRender;')
            else:
                render_node.postMel.set("")
                render_node.preRenderLayerMel.set("")
                render_node.postRenderLayerMel.set("")
                render_node.preRenderMel.set("")
                render_node.postRenderMel.set("")
                
        elif render_name=="mentalRay":
            print "++++++++++++++++ the renderer is mentalRay++++++++++++++++++"
            if shave_load:
                #render_name = render_node.currentRenderer.get()
                
                render_node.preRenderMel.set("shave_MRFrameStart;")
                render_node.postRenderMel.set("shave_MRFrameEnd;")
                #mel.eval('shave_MRFrameStart')

                #render_node.preRenderLayerMel.set('python \"mel.eval(\\"pgYetiVRayPreRender\\")\"')
            else:
                render_node.preRenderMel.set("")
                render_node.postRenderMel.set("")
        else:
            print "++++++++++++++++ the renderer isnot vray mentalRay+++++++++++++++++++++++++"
            render_node.postMel.set("")
            render_node.preRenderLayerMel.set("")
            render_node.postRenderLayerMel.set("")
            render_node.preRenderMel.set("")
            render_node.postRenderMel.set("")
            
        
        if preMel:
            print preMel
            pmel = preMel
            pmel_list = pmel.split(';')
            for mels in pmel_list:
                if not mels == ''
                
                    try:                    
                        mel.eval(mels)

                    except Exception as err:

                        self.mylog('=== Error occur execute "%s"! ===\n=== Error Msg : %s ===' % (mels, err))
                        self.G_DEBUG_LOG(mels)

    
    
    def resetup():
        #------set Frame/Animation ext: name.#.ext---
        mel.eval("setMayaSoftwareFrameExt(3,0);")
        #-------Renumber frames   is off-----
        self.RENDER_NODE.modifyExtension.set(0)
        #--------Append   off ------
        self.RENDER_ARNOLD_DRIVER_NODE.append.set(0)
        #---------Merge AOVs --------
        
        if self.RENDER_ARNOLD_DRIVER_NODE.mergeAOVs.get() == 0:
            pass
            
        else:
            pass
            
            
            
            
        
        
    def arnoldsetup(self):
        pass
        
        
    def vraysetup(self):
        pass
    
        



        
def rd_path():
    
    rd_path = pm.PyNode("defaultRenderGlobals").imageFilePrefix.get()
    render_node=pm.PyNode("defaultRenderGlobals")
    render_name = render_node.currentRenderer.get()
    if render_name == "vray":
        rd_path = pm.PyNode("vraySettings").fnprx.get()
    print rd_path
    if rd_path is not None:
        print "change output path"
        rd_path=rd_path.replace('\\','/').replace('//','/')
        p1=re.compile(r"^\w:/?")
        p2=re.compile(r"^/*")
        
        p3=re.compile(r"[^\w///<>.% :]")
        p4=re.compile(r"//*")
        #print re.findall(p,rd_path)
        #p=re.compile("[.~!@#$%\^\+\*&/ \? \|:\.{}()<>';=\\"]")
        #print p.search(rd_path).group()
        #m=p.match(rd_path)
        rd_path=re.sub(p4,"/",rd_path)
        print rd_path
        rd_path = re.sub(p1,"",rd_path)
        print rd_path
        rd_path = re.sub(p2,"",rd_path)
        print rd_path
        rd_path = re.sub(p3,"",rd_path)
        rd_path = re.sub(" ","_",rd_path)
        print rd_path
        sceneName = os.path.splitext(os.path.basename(pm.system.sceneName()))[0].strip()
        if '<Scene>' in rd_path:
            rd_path = rd_path.replace('<Scene>', sceneName)
        if '%s' in rd_path:
            rd_path = rd_path.replace('%s', sceneName)
        print "the output is %s " % rd_path
        pm.PyNode("defaultRenderGlobals").imageFilePrefix.set(rd_path)
        if render_name == "vray":
            rd_path = pm.PyNode("vraySettings").fnprx.set(rd_path)
    else:
        pass

def change_path(node_type, attr_name, mapping, rep_path,dicts):
    print "the  node type  is %s" % (node_type)    
    maya_proj_paht = cmds.workspace(q=True, fullName=True)
    source_path = "%s/sourceimages" % (maya_proj_paht)
    scenes_path = "%s/scenes" % (maya_proj_paht)
    data_path = "%s/data" % (maya_proj_paht)
    all_node = pm.ls(type=node_type)
    if len(all_node) != 0:
        for node in all_node:
            if node.hasAttr(attr_name):
                #file_path = cmds.getAttr(node + "."+attr_name)
                refcheck = pm.referenceQuery(node, inr = True)
                #print "refcheck %s " % (refcheck)
                if (refcheck == False):
                    try:              
                        node.attr(attr_name).set(l=0)
                    except Exception,error:
                        print Exception,":",error
                        pass
                file_path = node.attr(attr_name).get()
                if file_path != None and file_path.strip() !="" :
                    file_path = file_path.replace('\\', '/')
                    file_path = file_path.replace('<udim>', '1001')
                    file_path = file_path.replace('<UDIM>', '1001')
                    if os.path.exists(file_path) == 0:                        
                        asset_name = os.path.split(file_path)[1]
                        file_path_new = file_path
                        if rep_path:
                            file_path_new = "%s/%s" % (rep_path, asset_name)
                        if os.path.exists(file_path_new) == 0 and mapping:
                            for repath in mapping:
                                if mapping[repath] != repath:
                                    if file_path.find(repath) >= 0:
                                        file_path_new = file_path.replace(repath, mapping[repath])
                        
                        if os.path.exists(file_path_new) == 0:
                            file_path_new = "%s/%s" % (source_path, asset_name)
                        if os.path.exists(file_path_new) == 0:
                            file_path_new = "%s/%s" % (scenes_path, asset_name)
                        if os.path.exists(file_path_new) == 0 and dicts :
                            if asset_name in dicts:
                                file_path_new = dicts[asset_name]
                        
                        if os.path.exists(file_path_new) == 0:
                            print "the %s node %s  %s is not find ::: %s " % (node_type,node,attr_name,file_path)
                        else:
                            cmds.setAttr((node + "." + attr_name), file_path_new, type="string")
def change_path_mapping(node_type, attr_name, mapping):
    print "the  node type  is %s" % (node_type)    
    maya_proj_paht = cmds.workspace(q=True, fullName=True)
    source_path = "%s/sourceimages" % (maya_proj_paht)
    scenes_path = "%s/scenes" % (maya_proj_paht)
    data_path = "%s/data" % (maya_proj_paht)
    all_node = pm.ls(type=node_type)
    if len(all_node) != 0:
        for node in all_node:
            if node.hasAttr(attr_name):
                #file_path = cmds.getAttr(node + "."+attr_name)
                refcheck = pm.referenceQuery(node, inr = True)
                
                if (refcheck == False):
                    try:              
                        node.attr(attr_name).set(l=0)
                    except Exception,error:
                        print Exception,":",error
                        pass
                file_path = node.attr(attr_name).get()
                if file_path != None and file_path.strip() !="" :
                    file_path = file_path.replace('\\', '/')
                    if os.path.exists(file_path) == 0:                        
                        asset_name = os.path.split(file_path)[1]
                        file_path_new = file_path
                        print file_path_new
                        if os.path.exists(file_path_new) == 0 and mapping:
                            for repath in mapping:
                                if mapping[repath] != repath:
                                    if file_path.find(repath) >= 0:
                                        file_path_new = file_path.replace(repath, mapping[repath])
                                        print file_path_new                        
                                        cmds.setAttr((node + "." + attr_name), file_path_new, type="string")
def replace_path(node_type, attr_name,rep_path,repath_new):
    maya_proj_paht = cmds.workspace(q=True, fullName=True)
    source_path = "%s/sourceimages" % (maya_proj_paht)
    scenes_path = "%s/scenes" % (maya_proj_paht)
    data_path = "%s/data" % (maya_proj_paht)
    all_node = pm.ls(type=node_type)
    if all_node:
        for node in all_node:
            #file_path = cmds.getAttr(node + "."+attr_name)
            refcheck = pm.referenceQuery(node, inr = True)
            if (refcheck == False):                
                node.attr(attr_name).set(l=0)
            file_path = node.attr(attr_name).get()
            print file_path
            if file_path != None and file_path.strip() !="" :
                file_path_new = file_path.replace(rep_path, repath_new)
                print file_path_new
                cmds.setAttr((node + "." + attr_name), file_path_new, type="string")
                print "%s %s %s " % (node,attr_name,file_path_new)
                


   
    

def set_cam_render(cams):
    print "multiple cams to cmd"
    cams_list = cams.split(',')
    
    cams_all = pm.ls(type='camera')
    for cam in cams_all:
        mel.eval('removeRenderLayerAdjustmentAndUnlock("%s.renderable")' % cam)
        if cam not in cams_list:
            cmds.setAttr(cam + ".renderable", 0)
        else:
            cmds.setAttr(cam + ".renderable", 1)

def del_cam(cams):
    print "multiple cams to cmd"
    cams_all = pm.ls(type='camera')
    if cams:
        cams_list = cams.split(',')    
    
        for cam in cams_all:
            mel.eval('removeRenderLayerAdjustmentAndUnlock("%s.renderable")' % cam)
            if cam not in cams_list:
                try:                    
                    del_node(cam)
                    
                except:
                    print "the %s dont del " % (cam) 
                    pass 
            else:
                print "the cam %s is render" % (cam)
    else:
        for cam in cams_all:
            mel.eval('removeRenderLayerAdjustmentAndUnlock("%s.renderable")' % cam)
            if cmds.getAttr(cam + ".renderable")==0:
                try:
                    del_node(cam)
                    
                except:
                    print "the %s dont del " % (cam) 
                    pass 
            else:
                print "the cam %s is render" % (cam)
def set_layer_render(layers):
    print "multiple render layer to cmd"
    layers_list = layers.split(',')
    
    layers_all = cmds.listConnections("renderLayerManager.renderLayerId")
    for layer in layers_all:
        mel.eval('removeRenderLayerAdjustmentAndUnlock("%s.renderable")' % layer)
        if layer not in layers_list:
            cmds.setAttr(layer + ".renderable", 0)
        else:
            cmds.setAttr(layer + ".renderable", 1)
          
pre_layer_mel()
if rendersetting:
    if 'renderableLayer' in rendersetting :
        if "," in rendersetting['renderableLayer']:
            set_layer_render(rendersetting['renderableLayer'])


            
            
    def main():
    
        self.doCustomPrerender()
            
            

if __name__ == '__main__':
    print '\n\n-------------------------------------------------------[MayaPlugin]start----------------------------------------------------------\n\n'
    beginTime = datetime.datetime.now()
    
    doPre = PreRender()
    doPre.main()    
    
    
    endTime = datetime.datetime.now()
    timeOut = endTime - beginTime
    print "[Prerender time]----%s".format(str(timeOut))
    print '\n\n-------------------------------------------------------[MayaPlugin]end----------------------------------------------------------\n\n')   


