#!/usr/bin/env python
# -*- coding=utf-8 -*-
# Author: kaname
# QQ: 1394041054

import c4d, sys, re, os, json
import codecs
from c4d import documents, gui    

class C4dParser():
    def __init__(self, *args):
        sys.stdout = open('c:/c4d_analyse.log', 'w') 
        self.missings = {}
        self.tex_missings = []
        self.video_format = []

        self.task_json_dict = {}
        self.scene_common_dict = {}
        self.asset_json_dict = {}
        self.tips_json_dict = {}
        self.cg_file  = args[0]
        self.task_json = args[1]
        self.asset_json = args[2]
        self.tips_json = args[3]

    def __del__(self):
        sys.stdout.flush();
        sys.path.append(r'C:\script\new_py\CG\C4d\function')
        #import C4dKiller
        """ kill all c4d process """
        kill_command = r'C:\script\new_py\CG\C4d\function\taskkill.exe /F /IM "CINEMA 4D.exe"'
        os.system(kill_command)
     
    def init(self):
        if not os.path.exists(self.task_json):
            return False
        with open(self.task_json, 'r') as json_file:
            self.task_json_dict = json.load(json_file)
            task_scene_info = self.task_json_dict['scene_info']
            if 'common' not in task_scene_info:
                task_scene_info['common'] = {}

            self.scene_common_dict = task_scene_info['common']

        return True                        

    def analyze(self, *args):
        doc = c4d.documents.GetActiveDocument()
        """
        image size
        """    
        rd = doc.GetActiveRenderData()
        size_x = int(rd[c4d.RDATA_XRES_VIRTUAL]) 
        size_y = int(rd[c4d.RDATA_YRES_VIRTUAL]) 
        _size = {}
        _size['width'] = size_x
        _size['height'] = size_y
        self.scene_common_dict['image_size'] = _size 
      
        """
        render frame
        """
        rd = doc.GetActiveRenderData()
        fps = doc.GetFps()
        frame_rate = int(rd[c4d.RDATA_FRAMERATE])
        start_frame = (rd[c4d.RDATA_FRAMEFROM]).GetFrame(fps)
        end_frame = (rd[c4d.RDATA_FRAMETO]).GetFrame(fps)
        _frame_data = {}
        _frame_data['fps'] = fps
        _frame_data['start_frame'] = start_frame
        _frame_data['end_frame'] = end_frame
        _frame_data['frame_rate'] = frame_rate
        self.scene_common_dict['render_frame'] = _frame_data 

        """
        render format
        """
        rd = doc.GetActiveRenderData()
        RI_Format = {1035823:'Arnold-Dummy',1102:'BMP',1109:'BodyPaint 3D(B3D)',1023737:'DPX',1103:'IFF',1104:'JPEG',1016606:'OpenEXR',1106:'Photoshop(PSD)',
                    1111:'Photoshop Large Document(PSB)',1105:'PICT',1023671:'PNG',1001379:'Radiance(HDR)',1107:'RLA',1108:'RPF',
                    1101:'TARGA',1110:'TIFF(B3D Layers)',1100:'TIFF(PSD Layers)',1122:'AVI Movie',1125:'QuickTime Movie',
                    1150:'QuickTime VR Panorama',1151:'QuickTime VR Object'}
        print RI_Format[int(rd[c4d.RDATA_FORMAT])]

        MP_Format = {1035823:'Arnold-Dummy',1102:'BMP',1109:'BodyPaint 3D(B3D)',1023737:'DPX',1103:'IFF',1104:'JPEG',1016606:'OpenEXR',1106:'Photoshop(PSD)',
                    1111:'Photoshop Large Document(PSB)',1105:'PICT',1023671:'PNG',1001379:'Radiance(HDR)',1107:'RLA',1108:'RPF',
                    1101:'TARGA',1110:'TIFF(B3D Layers)',1100:'TIFF(PSD Layers)',1122:'AVI Movie',1125:'QuickTime Movie'}
        print MP_Format[int(rd[c4d.RDATA_MULTIPASS_SAVEFORMAT])]

        _render_format = {}
        _render_format['ri_format'] = RI_Format[int(rd[c4d.RDATA_FORMAT])]
        _render_format['mp_format'] = MP_Format[int(rd[c4d.RDATA_MULTIPASS_SAVEFORMAT])]
        self.scene_common_dict['render_format'] = _render_format 

        """
        multipass
        """
        _multipass = self.get_multipass(doc)
        self.scene_common_dict['multi_pass'] = _multipass
        
        """
        cameras
        """
        _cameras = self.get_cameras(doc)
        self.scene_common_dict['all_camera'] = _cameras
        
        """
        textures
        """
        _texts = [] 
        texs = doc.GetAllTextures()
        for tex in texs:
            _texts.append(tex[1])
        self.asset_json_dict['texture'] = _texts

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

        self.parse_analyze_result()

        self.dump()
                
    def get_multipass(self, doc):
        _multipass_dict = {}
        doc = c4d.documents.GetActiveDocument()
        rd = doc.GetActiveRenderData()
       
        single_savepath = rd[c4d.RDATA_PATH]
        multi_savepath = rd[c4d.RDATA_MULTIPASS_FILENAME]
        print single_savepath
        print multi_savepath
        print os.path.basename(multi_savepath)

        mp = rd.GetFirstMultipass()
        while mp:
            # object_buffer_arr = []
            # object_bufferID_arr = []
            # if mp.GetTypeName() == "Object Buffer":
            #     object_buffer_arr.append (mp.GetName())
            #     object_bufferID_arr.append (mp[c4d.MULTIPASSOBJECT_OBJECTBUFFER])

            mp_name = mp.GetName()

            _multipass_dict[mp_name] = []

            mp = mp.GetNext()

        return _multipass_dict
    
    def get_cameras(self, doc):
            _camera = []
            c4d.CallCommand(12112) # Select All
            c4d.CallCommand(16388) # Select Children
            cameras = doc.GetActiveObjectsFilter(True, type = 5103, instanceof = True)
            for camera in cameras:
                _camera.append(camera.GetName())
                
            c4d.CallCommand(12113) # Deselect All
            return _camera    

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
                print rf_mesh_path
        c4d.CallCommand(12113) # Deselect All
        return _realflow_mesh

    def get_realflow_particle(self, doc):
        _realflow_particle=[]
        c4d.CallCommand(12112) # Select All
        c4d.CallCommand(16388) # Select Children
        objs = doc.GetObjects()
        for obj in objs:
            if not obj: return
            if obj.GetTypeName() == ('RealFlow Particle Importer' and '粒子导入RealFlow Particle Importer'):
                rf_particle_path = obj[c4d.P_IMP_FILE_PATH]
                _realflow_particle.append(rf_particle_path)
                print rf_particle_path
        c4d.CallCommand(12113) # Deselect All
        return _realflow_particle

    def parse_analyze_result(self):
        self.parse_texture(self.asset_json_dict['texture'])
        # parse_mesh
        # ...
 
    def parse_texture(self, textures):
        for texture in textures:
            texture = os.path.normpath(texture)

            # 绝对路径检查
            if texture.find(':\\') > -1:
                if not os.path.exists(texture):
                    self.tex_missings.append(texture)            
            # 仅有贴图名检查
            else:
                # 到tex文件夹下面查找贴图
                root_dir = os.path.dirname(self.cg_file)
                tex_dir = os.path.join(root_dir, 'tex')  
                tex_file = os.path.join(tex_dir, texture)
                #tex_file = tex_file.replace('\\', '/')
                print 'tex = ' + tex_file
                # abs_file_path = ''.join(x.decode('utf-8') for x in tex_file.split())
                abs_file_path = tex_file
                if not os.path.exists(abs_file_path):
                    self.tex_missings.append(texture)
                    
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
        
    def dump(self):
        self.task_json_dict['scene_info']['common'] = self.scene_common_dict
        # write task.json
        with open(self.task_json, 'w') as outfile:
            json.dump(self.task_json_dict, outfile, indent=4, ensure_ascii=False)
        # write asset.json
        with open(self.asset_json, 'w') as outfile:
            json.dump(self.asset_json_dict, outfile, indent=4, ensure_ascii=False)
        #write missings
        print self.tips_json
        with open(self.tips_json, 'w') as outfile:
            json.dump(self.missings, outfile, indent=4, ensure_ascii=False) 

def PluginMessage(id, data):
    print 'PluginMessage in------'
    
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
        
        print 'load c4d file ' + cg_file

        if os.path.exists(cg_file):
            c4d.documents.LoadFile(cg_file)
            c4d_parser = C4dParser(cg_file, task_json, asset_json, tips_json)
            c4d_parser.init()
            c4d_parser.analyze()
        else:
            print 'load c4d file failed'

        return True

    return False