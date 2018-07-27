#!/usr/bin/env python
# -*- coding=utf-8 -*-
# Author: kaname
# QQ: 1394041054


# Run in here: %appdata%\MAXON\%cgv%_62A5E681\plugins
# from C4dLoader.py to do it.


import c4d, sys, re, os, json
import codecs,time
from c4d import documents, gui


class C4dParser():
    def __init__(self, *args):
        print (time.strftime('%y/%m/%d/%H/%M/%S'))
        sys.stdout = open('c:/@KANADA-C4dRBAnalyzer.log', 'w') 
        self.missings = {}
        self.tex_missings = []
        self.tex_video_format = []
        self.FPS_check = []
        self.output_avi_movie = []
        self.PhySampler_Mode = []

        self.task_json_dict = {}
        self.scene_common_dict = {}
        self.asset_json_dict = {}
        self.tips_json_dict = {}
        self.cg_file  = args[0]
        self.task_json = args[1]
        self.asset_json = args[2]
        self.tips_json = args[3]

    def __del__(self):
        print ('[.@KANADA.kill_c4d]')
        sys.stdout.flush();
        sys.path.append(r'C:\script\new_py\CG\C4d\function')
        #import C4dKiller
        """ kill all c4d process """
        kill_command = r'C:\script\new_py\CG\C4d\function\taskkill.exe /F /IM "CINEMA 4D 64 Bit.exe"'
        os.system(kill_command)
     
    def init(self):
        if not os.path.exists(self.task_json):
            return False
        with open(self.task_json, 'r') as json_file:
            self.task_json_dict = json.load(json_file)
            # if not self.task_json_dict.has_key('scene_info'):
            self.task_json_dict['scene_info']  = {}

            if 'common' not in self.task_json_dict['scene_info']:
                self.task_json_dict['scene_info']['common']  = {}

            self.scene_common_dict = self.task_json_dict['scene_info']['common'] 

        return True                        

    def analyze(self, *args):
        print ('[.@KANADA_analyze] \n')
        doc = c4d.documents.GetActiveDocument()
        rd = doc.GetActiveRenderData()


        print ('///scene_common_dict/// \n')
        # All of the scene's set are in task.json which in here [scene_info][common]

        """
        image size
        """    
        size_x = int(rd[c4d.RDATA_XRES_VIRTUAL]) 
        size_y = int(rd[c4d.RDATA_YRES_VIRTUAL]) 
        _size = {}
        _size['width'] = size_x
        _size['height'] = size_y
        self.scene_common_dict['image_size'] = _size

        # print ('------------------------------------------------------------------------------')

        """
        render frame
        """
        fps = doc.GetFps()
        start_frame = (rd[c4d.RDATA_FRAMEFROM]).GetFrame(fps)
        end_frame = (rd[c4d.RDATA_FRAMETO]).GetFrame(fps)
        frame_rate = int(rd[c4d.RDATA_FRAMERATE])
        frame_step = int(rd[c4d.RDATA_FRAMESTEP])
        render_region = int(rd[c4d.RDATA_RENDERREGION])
        _frame_data = {}
        _frame_data['fps'] = fps
        _frame_data['start_frame'] = start_frame
        _frame_data['end_frame'] = end_frame
        _frame_data['frame_rate'] = frame_rate
        _frame_data['frame_step'] = frame_step
        _frame_data['render_region'] = render_region
        self.scene_common_dict['render_frame'] = _frame_data

        # print ('------------------------------------------------------------------------------')

        """
        Regular save options
        """
        RI_save_click = int(rd[c4d.RDATA_SAVEIMAGE])
        RI_saveimage_path = rd[c4d.RDATA_PATH]
        RI_saveimage_path.decode('gbk','ignore').encode('utf-8')
        print(RI_save_click, RI_saveimage_path)
        _save_data = {}
        _save_data['RI_save_click'] = RI_save_click
        _save_data['RI_saveimage_path'] = RI_saveimage_path
        self.scene_common_dict['RI_save_options'] = _save_data

        # print ('------------------------------------------------------------------------------')

        """
        Multi-Pass save options
        """
        MP_save_click = int(rd[c4d.RDATA_MULTIPASS_SAVEIMAGE])
        MP_saveimage_path = rd[c4d.RDATA_MULTIPASS_FILENAME]
        # MP_saveonefile = rd[c4d.RDATA_MULTIPASS_SAVEONEFILE]
        # MP_options = rd[c4d.RDATA_MULTIPASS_SAVEOPTIONS]
        MP_saveimage_path.decode('gbk','ignore').encode('utf-8')
        print(MP_save_click, MP_saveimage_path)
        _save_data = {}
        _save_data['MP_save_click'] = MP_save_click
        _save_data['MP_saveimage_path'] = MP_saveimage_path
        # _save_data['MP_saveonefile'] = MP_saveonefile
        # _save_data['MP_options'] = MP_options
        self.scene_common_dict['MP_save_options'] = _save_data

        # print ('------------------------------------------------------------------------------')

        """
        render format
        """

        RI_Format = {1035823:'Arnold-Dummy',1102:'BMP',1109:'BodyPaint 3D(B3D)',1023737:'DPX',1103:'IFF',1104:'JPEG',1016606:'OpenEXR',1106:'Photoshop(PSD)',
                    1111:'Photoshop Large Document(PSB)',1105:'PICT',1023671:'PNG',1001379:'Radiance(HDR)',1107:'RLA',1108:'RPF',
                    1101:'TARGA',1110:'TIFF(B3D Layers)',1100:'TIFF(PSD Layers)',1122:'AVI Movie',1125:'QuickTime Movie',
                    1150:'QuickTime VR Panorama',1151:'QuickTime VR Object'}
        print(RI_Format[int(rd[c4d.RDATA_FORMAT])])

        MP_Format = {1035823:'Arnold-Dummy',1102:'BMP',1109:'BodyPaint 3D(B3D)',1023737:'DPX',1103:'IFF',1104:'JPEG',1016606:'OpenEXR',1106:'Photoshop(PSD)',
                    1111:'Photoshop Large Document(PSB)',1105:'PICT',1023671:'PNG',1001379:'Radiance(HDR)',1107:'RLA',1108:'RPF',
                    1101:'TARGA',1110:'TIFF(B3D Layers)',1100:'TIFF(PSD Layers)',1122:'AVI Movie',1125:'QuickTime Movie'}
        print(MP_Format[int(rd[c4d.RDATA_MULTIPASS_SAVEFORMAT])])

        _render_format = {}
        _render_format['regular_image_format'] = RI_Format[int(rd[c4d.RDATA_FORMAT])]

        _render_format['multi-pass_format'] = MP_Format[int(rd[c4d.RDATA_MULTIPASS_SAVEFORMAT])]
        self.scene_common_dict['render_format'] = _render_format 

        # print ('------------------------------------------------------------------------------')
        """
        multipass
        """
        _multipass = self.get_multipass(doc)
        self.scene_common_dict['multi_pass'] = _multipass

        # print ('------------------------------------------------------------------------------')
        """
        cameras
        """
        _cameras = self.get_cameras(doc)
        self.scene_common_dict['all_camera'] = _cameras

        # print ('------------------------------------------------------------------------------')
        """
        Renderer
        """
        _renderer = self.get_renderer(doc)
        self.scene_common_dict['Renderer'] = _renderer

        # print ('------------------------------------------------------------------------------')
        """
        Render_Settings_Physical_Sampler
        """
        _physical_sampler = self.get_rs_phys_sampler(doc)
        self.scene_common_dict['R_Physical_Sampler'] = _physical_sampler

        # print ('------------------------------------------------------------------------------')
        """
        Render_Settings_Physical_Sampler_Mode
        """
        _physical_sampler_mode = self.get_rs_phys_sampler_mode(doc)
        self.scene_common_dict['R_Physical_Sampler_Mode'] = _physical_sampler_mode
        
        # print ('------------------------------------------------------------------------------')
        """
        C4D_File_Version
        """
        _c4d_file_version = self.get_c4d_file_version(doc)
        self.scene_common_dict['C4D_File_Version'] = _c4d_file_version


        # ====分割线====
        # print ('------------------------------------------------------------------------------')
        print('///asset_json_dict/// \n')
        # All of the asset that scene used are in asset.json

        """
        textures
        """
        _texts = [] 
        texs = doc.GetAllTextures()
        for tex in texs:
            _texts.append(tex[1])
        self.asset_json_dict['textures'] = _texts

        # print ('------------------------------------------------------------------------------')

        """
        realflow mesh
        """
        _realflow_mesh = self.get_realflow_mesh(doc)
        self.asset_json_dict['realflow_mesh'] = _realflow_mesh


        """
        realflow particle
        """
        _realflow_particle = self.get_realflow_particle(doc)
        self.asset_json_dict['realflow_particle'] = _realflow_particle


        # print ('------------------------------------------------------------------------------')


        self.parse_analyze_result()

        self.dump()
                
    def get_multipass(self, doc):
        _multipass_dict = {}
        doc = c4d.documents.GetActiveDocument()
        rd = doc.GetActiveRenderData()
       
        single_savepath = rd[c4d.RDATA_PATH]
        multi_savepath = rd[c4d.RDATA_MULTIPASS_FILENAME]
        print(single_savepath)
        print(multi_savepath)
        print(os.path.basename(multi_savepath))

        mp = rd.GetFirstMultipass()
        while mp:
            object_buffer_arr = []
            object_bufferID_arr = []
            if mp.GetTypeName() == "Object Buffer":
                object_buffer_arr.append (mp.GetName())
                object_bufferID_arr.append (mp[c4d.MULTIPASSOBJECT_OBJECTBUFFER])

            mp_name = mp.GetName()
            _multipass_dict[mp_name] = []
            mp_name.decode('gbk','ignore').encode('utf-8')
            mp = mp.GetNext()

        return _multipass_dict
    
    def get_cameras(self, doc):
            _camera = []
            c4d.CallCommand(12112) # Select All
            c4d.CallCommand(16388) # Select Children
            cameras = doc.GetActiveObjectsFilter(True, type = 5103, instanceof = True)
            for camera in cameras:
                _camera.append(camera.GetName())
                camera.GetName().decode('gbk','ignore').encode('utf-8')
                
            c4d.CallCommand(12113) # Unselect All
            return _camera    

    def get_renderer(self, doc):
        _my_renderer = []
        doc = documents.GetActiveDocument()
        MyRenderSetting = doc.GetActiveRenderData()
        Renderer_ID = {0:'Standard',1023342:'Physical',1:'Software_OpenGL',1016630:'CineMan',1019782:'V_Ray',1029988:'Arnold(c4dtoa)',1029525:'Octane_GPURender',1036219:'Redshift_GPURender'}
        Renderer = Renderer_ID[MyRenderSetting[c4d.RDATA_RENDERENGINE]]
        _my_renderer.append(Renderer)

        return _my_renderer

    def get_rs_phys_sampler(self, doc):
        doc = documents.GetActiveDocument()
        MyRenderSetting = doc.GetActiveRenderData()
        Renderer_ID = {0:'Standard',1023342:'Physical',1:'Software_OpenGL',1016630:'CineMan',1019782:'V_Ray',1029988:'Arnold(c4dtoa)',1029525:'Octane_GPURender',1036219:'Redshift_GPURender'}
        Renderer = Renderer_ID[MyRenderSetting[c4d.RDATA_RENDERENGINE]]

        _physical_sampler = []
        
        if Renderer == "Physical":
            doc = documents.GetActiveDocument()
            rd = doc.GetActiveRenderData()
            vp = rd.GetFirstVideoPost()
            Phy_S = {0:'Fixed',1:'Adaptive',2:'Progressive'}
            _physical_sampler.append(Phy_S[int(vp[c4d.VP_XMB_RAYTRACING_SAMPLER])])

        return _physical_sampler

    def get_rs_phys_sampler_mode(self, doc):
        doc = documents.GetActiveDocument()
        MyRenderSetting = doc.GetActiveRenderData()
        Renderer_ID = {0:'Standard',1023342:'Physical',1:'Software_OpenGL',1016630:'CineMan',1019782:'V_Ray',1029988:'Arnold Renderer',1029525:'Octane_GPURender',1036219:'Redshift_GPURender',1037639:'ProRender'}
        Renderer = Renderer_ID[MyRenderSetting[c4d.RDATA_RENDERENGINE]]

        _physical_sampler_mode = []

        if Renderer == "Physical":
            doc = documents.GetActiveDocument()
            rd = doc.GetActiveRenderData()
            vp = rd.GetFirstVideoPost()
            
            Phy_S_Pro_Mode = {0:'Infinite',1:'Pass Count',2:'Time Limit'}
            _physical_sampler_mode.append(Phy_S_Pro_Mode[int(vp[c4d.VP_XMB_RAYTRACING_INTERACTIVE_MODE])])

        return _physical_sampler_mode

    def get_c4d_file_version(self, doc):
        _c4d_file_version = []
        doc = documents.GetActiveDocument()
        #BaseDocument.GetData([type]) : <--R16 before
        #BaseDocument.GetDocumentData(): New in version R16.021-->
        data = doc.GetDocumentData(c4d.DOCUMENTSETTINGS_DOCUMENT)
        created_ver = data[c4d.DOCUMENT_INFO_PRGCREATOR_NAME]
        saved_ver = data[c4d.DOCUMENT_INFO_PRGWRITER_NAME]
        return _c4d_file_version


    def get_realflow_mesh(self, doc):
        _realflow_mesh = []
        c4d.CallCommand(12112) # Select All
        c4d.CallCommand(16388) # Select Children
        objs = doc.GetObjects()
        for obj in objs:
            if not obj: return
            if obj.GetTypeName() == ('RealFlow Mesh Importer' and '网格导入RealFlow Mesh Importer'):
                rf_mesh_path = obj[c4d.M_IMP_FILE_PATH]
                _realflow_mesh.append(rf_mesh_path)
                print('rf_mesh_path = ' + rf_mesh_path)
        c4d.CallCommand(12113) # Unselect All
        return _realflow_mesh

    def parse_realflow(self):
        print ('[.@KANADA_parse_realflow]')
        #1.场景内的缓存路径
        if os.path.exists(self.asset_json_dict(_realflow_mesh)):
            print('@KANADArrrrrr' + _realflow_mesh)
        #2.工程目录的路径
        #get_cg_file = os.path.basename(self.cg_file)

        cg_project_path = os.path.basename(self.G_INPUT_PROJECT_PATH)
        print (cg_project_path)
        cg_file = self.G_INPUT_CG_FILE[len(self.G_INPUT_PROJECT_PATH):]
        print(cg_file + '@KANADA88888888888')

        get_cg_file = cg_project_path + ':' + cg_file
        print(get_cg_file + '@KANADA9999999999')


        if os.path.exists(get_cg_file):
            print('@KANADAcccccccccc' + get_cg_file)

    def get_realflow_particle(self, doc):
        _realflow_particle = []
        c4d.CallCommand(12112) # Select All
        c4d.CallCommand(16388) # Select Children
        objs = doc.GetObjects()
        for obj in objs:
            if not obj: return
            if obj.GetTypeName() == ('RealFlow Particle Importer' and '粒子导入RealFlow Particle Importer'):
                rf_particle_path = obj[c4d.P_IMP_FILE_PATH]
                _realflow_particle.append(rf_particle_path)
                print('rf_particle_path = ' + rf_particle_path)
        c4d.CallCommand(12113) # Unselect All
        return _realflow_particle

    def parse_analyze_result(self):
        self.parse_error(self.asset_json_dict['textures'])
        # parse_mesh
        # ...
 
    def parse_error(self, textures):
        doc = documents.GetActiveDocument()
        rd = doc.GetActiveRenderData()

        for texture in textures:
            texture = os.path.normpath(texture)
            """
                35001 贴图检查
            """
            texture.decode('gbk','ignore').encode('utf-8')
            # 绝对路径检查
            if texture.find(':\\') > -1:
                if not os.path.exists(texture):
                    self.tex_missings.append(texture)            
            # 仅有贴图名检查
            else:
                # 到tex文件夹下面查找贴图
                root_dir = os.path.dirname(self.cg_file)
                print('root_dir = ' + root_dir)
                tex_dir = os.path.join(root_dir, 'tex')  
                tex_file = os.path.join(tex_dir, texture)
                #tex_file = tex_file.replace('\\', '/')
                print('tex = ' + tex_file)
                abs_file_path = ''.join(x.decode('utf-8') for x in tex_file.split())
                #abs_file_path = tex_file
                if not os.path.exists(abs_file_path):
                    self.tex_missings.append(texture)

            """
                35001 贴图为视频格式检查判断
            """
            if texture.endswith('.mov'):
                if not os.path.exists(texture):
                    self.tex_video_format.append(texture)         
            elif texture.endswith('.mp4'):
                if not os.path.exists(texture):
                    self.tex_video_format.append(texture)
            elif texture.endswith('.mp3'):
                if not os.path.exists(texture):
                    self.tex_video_format.append(texture)
            elif texture.endswith('.gif'):
                if not os.path.exists(texture):
                    self.tex_video_format.append(texture)
            else: 
                pass

        """
            35002 FPS_check检查
        """
        fps = doc.GetFps()
        print (str(fps))
        Render_Settings_fps = int(rd[c4d.RDATA_FRAMERATE])
        print(str(Render_Settings_fps))


        if str(fps) != str(Render_Settings_fps):
            self.FPS_check.append('%s:%s' % ('fps', fps))
            self.FPS_check.append('%s:%s' % ('Render_Settings_fps', Render_Settings_fps))
        else:
            pass

        """
            35003 output_avi_movie检查
        """
        self.render_format = self.task_json_dict['scene_info']['common']['render_format']
        for avi in self.render_format:
            if 'AVI Movie' in self.render_format[avi]:
                if '%s:%s' % (avi, "AVI Movie") not in self.output_avi_movie:
                    self.output_avi_movie.append('%s:%s' % (avi, "AVI Movie"))
        else:
            pass

        """
            35004 PhySampler_Mode检查
        """
        doc = documents.GetActiveDocument()
        MyRenderSetting = doc.GetActiveRenderData()
        Renderer_ID = {0:'Standard',1023342:'Physical',1:'Software',1016630:'CineMan',1019782:'VrayBridge',1029988:'c4dtoa',1029525:'Octane Renderer',1036219:'Redshift'}
        Renderer = Renderer_ID[MyRenderSetting[c4d.RDATA_RENDERENGINE]]

        if Renderer == "Physical":
            doc = documents.GetActiveDocument()
            rd = doc.GetActiveRenderData()
            vp = rd.GetFirstVideoPost()
            Phy = {0:'Fixed',1:'Adaptive',2:'Progressive'}
            Phy_S = Phy[int(vp[c4d.VP_XMB_RAYTRACING_SAMPLER])]
            Phy_Mode = {0:'Infinite',1:'Pass Count',2:'Time Limit'}
            Phy_S_Pro_Mode = Phy_Mode[int(vp[c4d.VP_XMB_RAYTRACING_INTERACTIVE_MODE])]
            if Phy_S == "Progressive":
                if Phy_S_Pro_Mode == "Infinite":
                    self.PhySampler_Mode.append('%s:%s' % (Phy_S, Phy_S_Pro_Mode))
            else:
                pass


        print ('==============================================')
        #'35000':missing tex
        #'35001':the texture is video format
        #'35002':FPS unified
        #'35003':RI or MP output format is AVI movie
        #'35004':PhySampler_Mode
        self.missings['35000'] = self.tex_missings
        self.missings['35001'] = self.tex_video_format
        self.missings['35002'] = self.FPS_check
        self.missings['35003'] = self.output_avi_movie
        self.missings['35004'] = self.PhySampler_Mode
        sys.stdout.flush()


    def dump(self):
        print ('[.@KANADA_dump]')
        # dicts= sorted(self.scene_common_dict.items(), key=lambda d:d[1], reverse = True)
        self.task_json_dict['scene_info']['common'] = self.scene_common_dict
        # write task.json
        with open(self.task_json, 'w') as outfile:
            json.dump(self.task_json_dict, outfile, indent=4, ensure_ascii=False)
        # write asset.json
        with open(self.asset_json, 'w') as outfile:
            json.dump(self.asset_json_dict, outfile, indent=4, ensure_ascii=False)
        #write missings
        print(self.tips_json)
        with open(self.tips_json, 'w') as outfile:
            json.dump(self.missings, outfile, indent=4, ensure_ascii=False) 

def PluginMessage(id, data):
    print ('@KANADA \n PluginMessage in---------')
    
    if id == c4d.C4DPL_COMMANDLINEARGS:
        cg_file = ''
        task_json = ''
        asset_json = ''
        tips_json = ''

        for arg in sys.argv:
            #arg = arg.decode('gbk').encode('utf-8')
            if arg.startswith('-cg_file'):
                cg_file = arg.replace('-cg_file=', '').strip('"')
            elif arg.startswith('-task_json'):
                task_json = arg.replace('-task_json=', '').strip('"')
            elif arg.startswith('-asset_json'):
                asset_json = arg.replace('-asset_json=', '').strip('"')
            elif arg.startswith('-tips_json'):
                tips_json = arg.replace('-tips_json=', '').strip('"') 

            print('load c4d file... ' + cg_file)

        if os.path.exists(cg_file):
            c4d.documents.LoadFile(cg_file)
            c4d_parser = C4dParser(cg_file, task_json, asset_json, tips_json)
            c4d_parser.init()
            c4d_parser.analyze()
        else:
            print ('load c4d file failed...')

        return True

    return False