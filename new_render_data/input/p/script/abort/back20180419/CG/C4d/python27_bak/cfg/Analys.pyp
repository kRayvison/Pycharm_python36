#!/usr/bin/env python
#coding=utf-8

#.A ---- customer cannot assign folder
#.B ---- customer can assign folder
#.d ---- the item is a folder
#.f ---- the item is a file
#.C4D_Analys-'Lion''QQ:58701328'
###-modify by 'kanada'
import c4d, sys, re, os, json
import codecs;
from c4d import documents, gui    

class C4Dparser():
    def __init__(self, *args):
        sys.stdout = open('c:/c4d_analyse.log', 'w') 
        self.texture_tag              = "------------texture-----------------"
        self.image_size_tag           = "------------Image Size-----------------"
        self.render_frame_tag         = "------------Render Frame-----------------"
        self.render_format_tag        = "------------Render Format-----------------"
        self.multi_pass_tag           = "------------Multi-Pass-----------------"
        self.camera_tag               = "------------camera-----------------"
        self.rfmesh_name_path_tag     = "------------RFMesh_name_path-----------------"
        self.rfparticle_name_path_tag = "------------RFParticle_name_path-----------------"
        self.missings = {}
        self.tex_missings = []
        self.video_format = []
        self.cgFileStr  = args[0]
        self.txtFileStr = args[1]
        #self.taskIdStr = args[1]
       
    def __del__(self):
        sys.stdout.flush();
        sys.path.append(r'B:\plugins\C4D\script')
        import kill
        os.remove('C:\users\enfuzion\AppData\Roaming\MAXON\CINEMA 4D R13_05DFD2A0\plugins\Analys.pyp')
        os.remove('C:\users\enfuzion\AppData\Roaming\MAXON\CINEMA 4D R14_4A9E4467\plugins\Analys.pyp')
        os.remove('C:\users\enfuzion\AppData\Roaming\MAXON\CINEMA 4D R15_53857526\plugins\Analys.pyp')
        os.remove('C:\users\enfuzion\AppData\Roaming\MAXON\CINEMA 4D R16_14AF56B1\plugins\Analys.pyp')
        os.remove('C:\users\enfuzion\AppData\Roaming\MAXON\CINEMA 4D R17_8DE13DAD\plugins\Analys.pyp')
        os.remove('C:\users\enfuzion\AppData\Roaming\MAXON\CINEMA 4D R18_62A5E681\plugins\Analys.pyp')
       
    def getAllCams(self,doc):
        cameraStr=''
        doc = c4d.documents.GetActiveDocument()
        c4d.CallCommand(12112) # Select All
        c4d.CallCommand(16388) # Select Children
        Cameras = doc.GetActiveObjectsFilter(True, type=5103, instanceof=True)
        for C in (Cameras):
            if C.GetTypeName() == "Camera":
                obj = str(C)
                print obj+'\n'
                for C in obj.split():
                    if "/" in C:
                        keyword = C
                        break
                word = keyword.replace("'","")
                wordSplit = word.split("/")
                if wordSplit:
                    wordHead = wordSplit[0]
                    print "CameaName:"+wordHead + '\n'
                    cameraStr=cameraStr+("cameraName:"+str(wordHead)+"\n")
            else:
                continue
        c4d.CallCommand(12113) # Deselect All
        return cameraStr

    def MultiPass(self, doc):
        MPnameStr=''
        rd = doc.GetActiveRenderData()
        rd_long = doc.GetActiveRenderData()
        vp = rd.GetFirstMultipass()
        single_path = rd[c4d.RDATA_PATH]
        multi_path = rd[c4d.RDATA_MULTIPASS_FILENAME]
        multi_path_arr = multi_path.split("\\")
        i = 0
        arr_len = len (multi_path_arr)
        arr_len = arr_len - 1
        object_buffer_arr = []
        object_bufferID_arr = []
        pfadarr = []
        file_type_arr = []
        file_name =  multi_path_arr[arr_len]
        i = 0
        j = 0
        k = 0
        while vp:
            if vp.GetTypeName() == "Object Buffer":
                object_buffer_arr.append (vp.GetName())
                object_bufferID_arr.append (vp[c4d.MULTIPASSOBJECT_OBJECTBUFFER])
                j = j + 1
            mp_name = vp.GetName()
            print mp_name + '\n'
            MPnameStr=MPnameStr+("MultiPassName:"+str(mp_name)+"\n\n")
           
            multipass_type = ""
            if mp_name == "RGBA Image":
                multipass_type = "rgb"
            elif mp_name == "Ambient":
                multipass_type = "ambient"
            elif mp_name == "Ambient Occlusion":
                multipass_type = "ao"
            elif mp_name == "Atmosphere":
                multipass_type = "atmos"        
            elif mp_name == "Atmosphere (Multiply)":
                multipass_type = "atmosmul"
            elif mp_name == "Caustics":
                multipass_type = "caustics"
            elif mp_name == "Depth":
                multipass_type = "depth"
            elif mp_name == "Diffuse":
                multipass_type = "diffuse"
            elif mp_name == "Global Illumination":
                multipass_type = "gi"
            elif mp_name == "Illumination":
                multipass_type = "illum"
            elif mp_name == "Material Color":
                multipass_type = "matcolor"
            elif mp_name == "Material Diffusion":
                multipass_type = "matdif"            
            elif mp_name == "Material Environment":
                multipass_type = "matenv"            
            elif mp_name == "Material Luminance":
                multipass_type = "matlum"
            elif mp_name == "Material Reflection":
                multipass_type = "matrefl"            
            elif mp_name == "Material Refraction":
                multipass_type = "matrefr"            
            elif mp_name == "Material Specular":
                multipass_type = "matspec"            
            elif mp_name == "Material Specular Color":
                multipass_type = "matspeccol"  
            elif mp_name == "Material Transparency":
                multipass_type = "mattrans"            
            elif mp_name == "Motion Vector":
                multipass_type = "motion"            
            elif mp_name == "Material Normal":
                multipass_type = "normal"            
            elif mp_name == "Specular":
                multipass_type = "specular"            
            elif mp_name == "Shadow":
                multipass_type = "shadow"            
            elif mp_name == "Material UVW":
                multipass_type = "uv"              
            elif mp_name == "Reflection":
                multipass_type = "refl"            
            elif mp_name == "Refraction":
                multipass_type = "refr"              
            elif mp_name == "Post Effects":
                multipass_type = "post"
            vp = vp.GetNext()
        else:
            print "multipass is Null"
        return MPnameStr
    
    def getRFMesh(self, doc):
        RFMeshStr=''
        doc = c4d.documents.GetActiveDocument()
        c4d.CallCommand(12112) # Select All
        c4d.CallCommand(16388) # Select Children
        obj = doc.GetObjects()
        for i in (obj):
            if not obj: return
            if i.GetTypeName() == ('RealFlow Mesh Importer' and '网格导入RealFlow Mesh Importer'):
                RFMesh_path = i[c4d.M_IMP_FILE_PATH]
                obj = str(i)
                for i in obj.split():
                    if "/" in i:
                        keyword1 = i
                        break
                word = keyword1.replace("'","")
                wordSplit = word.split("/")
                if wordSplit:
                    wordHead1 = wordSplit[0]
                    print "RFMesh_Name:"+wordHead1 + '\n'
                print 'RFMesh_path' + ':' + RFMesh_path
                RFMeshStr=RFMeshStr+("RFMesh_Name:"+str(wordHead1)+"\n\n"+'RFMesh_path'+':'+ str(RFMesh_path)+"\n\n")
            else:
                continue
        c4d.CallCommand(12113) # Deselect All
        return RFMeshStr

    def getRFParticle(self, doc):
        RFParticleStr=''
        doc = c4d.documents.GetActiveDocument()
        c4d.CallCommand(12112) # Select All
        c4d.CallCommand(16388) # Select Children
        obj = doc.GetObjects()
        for i in (obj):
            if not obj: return
            if i.GetTypeName() == ('RealFlow Particle Importer' and '粒子导入RealFlow Particle Importer'):
                RFParticle_path = i[c4d.P_IMP_FILE_PATH]
                obj = str(i)
                for i in obj.split():
                    if "/" in i:
                        keyword1 = i
                        break
                word = keyword1.replace("'","")
                wordSplit = word.split("/")
                if wordSplit:
                    wordHead1 = wordSplit[0]
                    print "RFParticle_Name:"+wordHead1 + '\n'
                print 'RFParticle_path' + ':' + RFParticle_path
                RFParticleStr=RFParticleStr+("RFParticle_Name:"+str(wordHead1)+"\n\n"+'RFParticle_path'+':'+ str(RFParticle_path)+"\n\n")
            else:
                continue
        c4d.CallCommand(12113) # Deselect All
        return RFParticleStr
    
    def Analyze(self, *args):
        analystxt = '%s' % (self.txtFileStr)
        print analystxt
        with open(analystxt,'w+') as f:
            f.write("\n------------texture-----------------\n")
            doc = documents.GetActiveDocument()
            texs = doc.GetAllTextures()
            for item in texs:
                print item[1]
                f.write(item[1] + "\n")
            
            f.write("\n------------Image Size-----------------\n")
            rd = doc.GetActiveRenderData()
            sizeX = int(rd[c4d.RDATA_XRES_VIRTUAL]) 
            sizeY = int(rd[c4d.RDATA_YRES_VIRTUAL]) 
            print "Width:"+str(sizeX)
            print "Height:"+str(sizeY)
            f.write("Width:"+str(sizeX)+"\n")
            f.write("Height:"+str(sizeY)+"\n")
          
            f.write("------------Render Frame-----------------"+"\n\n")
            doc = documents.GetActiveDocument()
            rd = doc.GetActiveRenderData()
            fps = doc.GetFps()
            Render_Settings_fps = int(rd[c4d.RDATA_FRAMERATE])
            sf = (rd[c4d.RDATA_FRAMEFROM]).GetFrame(fps)
            ef = (rd[c4d.RDATA_FRAMETO]).GetFrame(fps)
            print "Start frame:"+str(sf)+"\n"
            print "End frame:"+str(ef)+"\n"
            print "Project_fps:"+str(fps)+"\n"
            print "Render_Settings_fps"+str(Render_Settings_fps)+"\n"
            f.write("Start frame:"+str(sf)+"\n\n")
            f.write("End frame:"+str(ef)+"\n\n")
            f.write("Project_fps:"+str(fps)+"\n\n")
            f.write("Render_Settings_fps:"+str(Render_Settings_fps)+"\n\n")
            
            f.write("\n------------Render Format-----------------\n")
            doc = documents.GetActiveDocument()
            rd = doc.GetActiveRenderData()
            RI_Format = {1035823:'Arnold-Dummy',1102:'BMP',1109:'BodyPaint 3D(B3D)',1023737:'DPX',1103:'IFF',1104:'JPEG',1016606:'OpenEXR',1106:'Photoshop(PSD)',
                        1111:'Photoshop Large Document(PSB)',1105:'PICT',1023671:'PNG',1001379:'Radiance(HDR)',1107:'RLA',1108:'RPF',
                        1101:'TARGA',1110:'TIFF(B3D Layers)',1100:'TIFF(PSD Layers)',1122:'AVI Movie',1125:'QuickTime Movie',
                        1150:'QuickTime VR Panorama',1151:'QuickTime VR Object'}
            print RI_Format[int(rd[c4d.RDATA_FORMAT])]
            f.write("RI_Format:"+RI_Format[int(rd[c4d.RDATA_FORMAT])]+"\n")
            MP_Format = {1035823:'Arnold-Dummy',1102:'BMP',1109:'BodyPaint 3D(B3D)',1023737:'DPX',1103:'IFF',1104:'JPEG',1016606:'OpenEXR',1106:'Photoshop(PSD)',
                        1111:'Photoshop Large Document(PSB)',1105:'PICT',1023671:'PNG',1001379:'Radiance(HDR)',1107:'RLA',1108:'RPF',
                        1101:'TARGA',1110:'TIFF(B3D Layers)',1100:'TIFF(PSD Layers)',1122:'AVI Movie',1125:'QuickTime Movie'}
            print MP_Format[int(rd[c4d.RDATA_MULTIPASS_SAVEFORMAT])]
            f.write("MP_Format:"+MP_Format[int(rd[c4d.RDATA_MULTIPASS_SAVEFORMAT])]+"\n")
            
            f.write("\n------------Multi-Pass-----------------\n") 
            MPnameStr=self.MultiPass(doc)
            f.write(MPnameStr)
            
            f.write("\n------------camera-----------------\n")
            cameraStr=self.getAllCams(doc)
            f.write(cameraStr)
            
            f.write("\n------------RFMesh_name_path-----------------\n")
            RFMeshStr=self.getRFMesh(doc)
            f.write(RFMeshStr)
            
            f.write("\n------------RFParticle_name_path-----------------\n")             
            RFParticleStr=self.getRFParticle(doc)
            f.write(RFParticleStr)
          
            f.close()
        self.parse_analyze_result()
            
    ## TODO:lynne
    
    def parse_analyze_result(self):
        with open(self.txtFileStr, 'r') as infle:
            content = infle.read()
            tex_start_pos = content.find(self.texture_tag) + len(self.texture_tag)
            tex_end_pos = content.find(self.image_size_tag)
            
            if tex_start_pos != -1 and tex_end_pos != -1:
                self.parse_texture(content[tex_start_pos:tex_end_pos])
        
        self.write_missings()
 
    def parse_texture(self, textures):
        items = [item for item in textures.split('\n') if item]
        self.extract_texture(items)

    def extract_texture(self, items):
        for item in items:
            texture = os.path.normpath(item)

            # 绝对路径检查
            if texture.find(':\\') > -1:
                if not os.path.exists(texture):
                    self.tex_missings.append(texture)            
            # 仅有贴图名检查
            else:
                # 到tex文件夹下面查找贴图
                root_dir = os.path.dirname(self.cgFileStr)
                tex_dir = os.path.join(root_dir, 'tex')  
                tex_file = os.path.join(tex_dir, texture)
                #tex_file = tex_file.replace('\\', '/')
                print 'tex = ' + tex_file
                abs_file_path = ''.join(x.decode('utf-8') for x in tex_file.split())
                '''if not os.path.exists(abs_file_path):
                    self.tex_missings.append(texture)'''
                    
            # 视频格式检查
            if texture.endswith('.mov'):
                if not os.path.exists(texture):
                    self.video_format.append(texture)         
            elif texture.endswith('.mp4'):
                if not os.path.exists(texture):
                    self.video_format.append(texture)
            else: 
                pass
        
        #'35000':missing tex
        #'35001':video format
        self.missings['35000'] = self.tex_missings
        self.missings['35001'] = self.video_format

        sys.stdout.flush()
        
    def write_missings(self):
        root_dir = os.path.dirname(self.txtFileStr)
        missing_file = os.path.join(root_dir, 'tips.json')
        with open(missing_file, 'w') as outfile:
            json.dump(self.missings, outfile, indent=4, ensure_ascii=False)
    
    

def PluginMessage(id, data):
    print 'plugin------'
    
    if id==c4d.C4DPL_COMMANDLINEARGS:
        cgFileStr=''
        txtFileStr=''
        print sys.argv #print arguments
        for arg in sys.argv:
            print arg
            if arg.startswith('-cgFile'):
                cgFileStr=arg.replace('-cgFile:', '')
                print cgFileStr
            elif arg.startswith('-txtPath'):
                txtFileStr=arg.replace('-txtPath:', '')
                print txtFileStr
            else:
                print 'no info'
        RFile = str(cgFileStr)
        c4d.documents.LoadFile(RFile)

        mainFunc = C4Dparser(cgFileStr, txtFileStr)
        mainFunc.Analyze()
        return True

    return False