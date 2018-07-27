#!/usr/bin/env python
# -*- coding=utf-8 -*-
# Author: kaname
# QQ: 1394041054
# Update:20180626

# Run in here: %appdata%\MAXON\%cgv%_62A5E681/plugins
# from C4dLoader.py to do it.


import c4d, sys, re, os, json
import codecs,time
import logging
from c4d import documents, gui
from c4d import storage as st, gui

if not os.path.exists("c:/c4d"):
    os.mkdir("c:/c4d")

logging.basicConfig(level=logging.DEBUG,
    format='%(asctime)s %(filename)s %(levelname)s %(message)s',
    datefmt='%a, %d %b %Y %H:%M:%S',
    filename='c:/c4d/@KANADA-C4dRBAnalyzer.log',
    filemode='w')


class C4dParser():
    def __init__(self, *args):
        logging.info (time.strftime('%y/%m/%d/%H/%M/%S'))
        
        self.missings = {}
        self.tex_missings = []
        self.tex_video_format = []
        self.FPS_check = []
        self.output_avi_movie = []
        self.physical_sampler_mode = []
        self.octane_render_passes = []

        self.task_json_dict = {}
        self.scene_common_dict = {}
        self.scene_renderer_dict = {}
        self.asset_json_dict = {}
        self.tips_json_dict = {}
        self.cg_file  = args[0]
        self.task_json = args[1]
        self.asset_json = args[2]
        self.tips_json = args[3]
        #1 :未激活参数面板，自动提交
        #2：激活参数面板，手动提交
        self.auto_commit = True if args[4] == '1' else False

        # 打印用下面这个，不需要ylogging.info
        logging.info('C4dParser inited...')

    def __del__(self):
        self.exit()
     
    def parse(self):
        if self.init():
            if self.check_verison():
                self.analyze()
            else:
                logging.error('C4dParser check_verison failed...')
     
    def init(self):
        logging.info('init inited...')

        if not os.path.exists(self.task_json):
            return False
        with open(self.task_json, 'rb') as json_file:
            self.task_json_dict = json.load(json_file)
 
            # if not self.task_json_dict.has_key('scene_info'):
            self.task_json_dict['scene_info']  = {}
                
            if 'common' not in self.task_json_dict['scene_info']:
                self.task_json_dict['scene_info']['common']  = {}
                
            if 'renderer' not in self.task_json_dict['scene_info']:
                self.task_json_dict['scene_info']['renderer'] = {}

            self.scene_common_dict = self.task_json_dict['scene_info']['common']
            self.scene_renderer_dict = self.task_json_dict['scene_info']['renderer']
            
        #logging.info str(self.task_json_dict['software_config'])+ '555555555555555'
        return True
        
    def exit(self):
        logging.info('[.@KANADA.kill_c4d]')

        sys.path.append(r'C:\script/new_py/CG/C4d/function')
        #import C4dKiller
        """ kill all c4d process """
        kill_command = r'C:\script/new_py/CG/C4d/function/taskkill.exe /F /IM "CINEMA 4D 64 Bit.exe"'
        os.system(kill_command)
          
    def kanada_get_document_data(self, doc):
        # ps:不同版本的sdk写法不一致在这里写
        
        _data = {}
        """
        try:
            _data = doc.GetData([c4d.DOCUMENTSETTINGS_DOCUMENT])
        except:
            _data = doc.GetDocumentData(c4d.DOCUMENTSETTINGS_DOCUMENT)
        return _data

        """
        softversion = int(c4d.GetC4DVersion())
        # if R19 using this
        if softversion >= 19000 and softversion <= 20000:
            _data = doc.GetDocumentData(c4d.DOCUMENTSETTINGS_DOCUMENT)
        else:
            _data = doc.GetData(c4d.DOCUMENTSETTINGS_DOCUMENT)
            
        return _data


    def check_verison(self):
        logging.info ('[.@KANADA_check_verison]')
        # cg file version != cg version,error, otherwise go on
        doc = documents.GetActiveDocument()
        data = self.kanada_get_document_data(doc)
        saved_ver = data[c4d.DOCUMENT_INFO_PRGWRITER_NAME]
        logging.info('saved_ver:' + saved_ver)
        """
        saved_ver:
        MAXON CINEMA 4D Studio 13.061
        MAXON CINEMA 4D Studio 14.041
        MAXON CINEMA 4D Studio 15.064 
        MAXON CINEMA 4D Studio (R16) 16.011
        MAXON CINEMA 4D Studio (R17) 17.055
        MAXON CINEMA 4D Studio (RC - R18) 18.011
        MAXON CINEMA 4D Studio (RC - R19) 19.024
        """
        pattern = re.compile(r'\d{2}\.\d{3}\w*')

        # 文件本身版本,'17' , 
        #int_saved_ver = int(saved_ver.split()[-2].replace('(', '').replace(')', '').replace('R', ''))
        all_saved_ver = pattern.findall(saved_ver)
        logging.info('all_saved_ver:' + str(all_saved_ver)) #['15.064']
        hi_saved_ver = all_saved_ver[0] #15.064
        logging.info('hi_saved_ver:' + hi_saved_ver)
        int_saved_ver = int(float(hi_saved_ver)) #15
        logging.info('int_saved_ver:' + str(int_saved_ver))
        

        software_config = self.task_json_dict['software_config']
        cg_verison = software_config['cg_name'] + ' ' + software_config['cg_version']
        logging.info('cg_verison:' + str(cg_verison))

        # 提交配置的版本CINEMA 4D R17,  '17', 
        int_cg_ver = int(cg_verison.split()[-1].replace('R', ''))
        logging.info('int_cg_ver:' + str(int_cg_ver))

        if int_cg_ver < int_saved_ver:
            #write missings
            with open(self.tips_json, 'w') as outfile:
                ver_arr = []
                ver_arr.append('cg_verison: %s' % cg_verison)
                ver_arr.append('saved_ver: %s' % saved_ver)
                self.missings['35007'] = ver_arr

                json.dump(self.missings, outfile, indent=4, ensure_ascii=False)
                logging.info('tips_json dump....')
            return False

        return True

    def analyze(self, *args):
        logging.info('C4dParser inited...')
        logging.info ('[.@KANADA_analyze is starting] \n')

        doc = c4d.documents.GetActiveDocument()
        rd = doc.GetActiveRenderData()

        logging.info ('///1. scene_renderer_dict/// \n')
        # 1. a scene of renderer set in here [scene_info][renderer]
        """
        Renderer
        """
        _renderer = self.get_renderer(doc)
        self.scene_renderer_dict['name'] = _renderer

        # logging.info ('------------------------------------------------------------------------------')
        """
        Render_Settings_Physical_Sampler
        """
        _physical_sampler = self.get_rs_phys_sampler(doc)
        self.scene_renderer_dict['physical_sampler'] = _physical_sampler

        # logging.info ('------------------------------------------------------------------------------')
        """
        Render_Settings_Physical_Sampler_Mode
        """
        _physical_sampler_mode = self.get_rs_phys_sampler_mode(doc)
        self.scene_renderer_dict['physical_sampler_mode'] = _physical_sampler_mode
        
        
        logging.info ('///2. scene_common_dict/// \n')
        # 2. All of the scene's set are in task.json which in here [scene_info][common]

        """
        image size
        """    
        size_x = int(rd[c4d.RDATA_XRES_VIRTUAL]) 
        logging.info (size_x)
        size_y = int(rd[c4d.RDATA_YRES_VIRTUAL])
        logging.info (size_y)
        #_size = {}
        #_size['width'] = size_x
        #_size['height'] = size_y
        #self.scene_common_dict['size'] = _size
        self.scene_common_dict['width'] = str(size_x)
        self.scene_common_dict['height'] = str(size_y)

        # logging.info ('------------------------------------------------------------------------------')

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
        _frame_data['fps'] = str(fps)
        _frame_data['frame_rate'] = str(frame_rate)
        _frame_data['render_region'] = str(render_region)
        self.scene_common_dict["frames"] = "%s-%s[%s]" % (start_frame, end_frame, frame_step)
        self.scene_common_dict["fps"] = str(fps)
        self.scene_common_dict["frame_rate"] = str(frame_rate)
        
        
        # logging.info ('------------------------------------------------------------------------------')
        
        """
        Regular image save options
        """
        regular_image_save_enabled = int(rd[c4d.RDATA_SAVEIMAGE])
        regular_image_save_path = rd[c4d.RDATA_PATH]
        regular_image_save_path.decode('gbk','ignore').encode('utf-8')
        print(regular_image_save_enabled, regular_image_save_path)
        self.scene_common_dict['regular_image_save_enabled'] = str(regular_image_save_enabled)
        #self.scene_common_dict['regular_image_saveimage_path'] = str(regular_image_save_path.replace('\\', '/'))
        file_name = os.path.basename(self.cg_file) # R16_test.c4d
        self.scene_common_dict['regular_image_saveimage_path'] = os.path.splitext(file_name)[0] # R16_test

        # logging.info ('------------------------------------------------------------------------------')

        """
        Multi-Pass save options
        """
        multipass_save_enabled = int(rd[c4d.RDATA_MULTIPASS_SAVEIMAGE])
        multipass_save_path = rd[c4d.RDATA_MULTIPASS_FILENAME]
        MP_saveonefile = rd[c4d.RDATA_MULTIPASS_SAVEONEFILE]
        # MP_options = rd[c4d.RDATA_MULTIPASS_SAVEOPTIONS]
        multipass_save_path.decode('gbk', 'ignore').encode('utf-8')
        print(multipass_save_enabled, multipass_save_path, MP_saveonefile)
        #_save_data = {}
        #_save_data['multipass_save_enabled'] = multipass_save_enabled
        #_save_data['multipass_saveimage_path'] = multipass_save_path
        # _save_data['MP_saveonefile'] = MP_saveonefile
        # _save_data['MP_options'] = MP_options
        self.scene_common_dict['multipass_save_enabled'] = str(multipass_save_enabled)
        self.scene_common_dict['multipass_saveimage_path'] = str(multipass_save_path.replace('\\', '/'))
        self.scene_common_dict['multipass_saveonefile'] = str(MP_saveonefile)
        

        # logging.info ('------------------------------------------------------------------------------')

        """
        render format
        """

        # 20180604update 不同版本的出图格式 c4d_version, ex:R19_NEW

        #列出软件内所有的输出格式,主图与通道一致
        
        format_all = []
        softversion = int(c4d.GetC4DVersion())
        # if R19 using this
        if softversion >= 19000 and softversion <= 20000:
            R19_new_RI_Format = {1102:'BMP',1109:'B3D',1073775603:'DDS',1023737:'DPX',1001379:'HDR',1103:'IFF',1104:'JPG',1016606:'EXR',
                            1105:'PICT',1023671:'PNG',1111:'PSB',1106:'PSD',1107:'RLA',1108:'RPF',1101:'TGA',1100:'TIFF',1073794140:'3GP',
                            1073773172:'ASF',1122:'AVI',1125:'MP4',1073794144:'WMV'}
            logging.info(R19_new_RI_Format[int(rd[c4d.RDATA_FORMAT])])
            
            R19_new_MP_Format = {1102:'BMP',1109:'B3D',1073775603:'DDS',1023737:'DPX',1001379:'HDR',1103:'IFF',1104:'JPG',1016606:'EXR',
                                1105:'PICT',1023671:'PNG',1111:'PSB',1106:'PSD',1107:'RLA',1108:'RPF',1101:'TGA',1100:'TIFF',1073794140:'3GP',
                                1073773172:'ASF',1122:'AVI',1125:'MP4',1073794144:'WMV'}
            logging.info(R19_new_MP_Format[int(rd[c4d.RDATA_MULTIPASS_SAVEFORMAT])])
        
            self.scene_common_dict['regular_image_format'] = R19_new_MP_Format[int(rd[c4d.RDATA_FORMAT])]
            self.scene_common_dict['multi_pass_format'] = R19_new_MP_Format[int(rd[c4d.RDATA_MULTIPASS_SAVEFORMAT])]
        
            # find all regular image format for display, multipass not need.
            for format_key in R19_new_MP_Format.keys():
                format_all.append(R19_new_MP_Format[format_key])
        # R13-R18 using this one
        else:
            R13_18_RI_Format = {1035823:'Arnold-Dummy',1102:'BMP',1109:'B3D',1023737:'DPX',1103:'IFF',1104:'JPG',1016606:'EXR',1106:'PSD',
                    1111:'PSB',1105:'PICT',1023671:'PNG',1001379:'HDR',1107:'RLA',1108:'RPF',
                    1101:'TGA',1110:'TIFF(B3D Layers)',1100:'TIFF',1122:'AVI Movie',1125:'QuickTime Movie',
                    1150:'QuickTime VR Panorama',1151:'QuickTime VR Object',}
            logging.info(R13_18_RI_Format[int(rd[c4d.RDATA_FORMAT])])

            R13_18_MP_Format = {1035823:'Arnold-Dummy',1102:'BMP',1109:'B3D',1023737:'DPX',1103:'IFF',1104:'JPG',1016606:'EXR',1106:'PSD',
                        1111:'PSB',1105:'PICT',1023671:'PNG',1001379:'HDR',1107:'RLA',1108:'RPF',
                        1101:'TGA',1110:'TIFF(B3D Layers)',1100:'TIFF',1122:'AVI Movie',1125:'QuickTime Movie'}
            logging.info(R13_18_MP_Format[int(rd[c4d.RDATA_MULTIPASS_SAVEFORMAT])])
            
            self.scene_common_dict['regular_image_format'] = R13_18_RI_Format[int(rd[c4d.RDATA_FORMAT])]
            self.scene_common_dict['multi_pass_format'] = R13_18_MP_Format[int(rd[c4d.RDATA_MULTIPASS_SAVEFORMAT])]
            
            for format_key in R13_18_RI_Format.keys():
                format_all.append(R13_18_RI_Format[format_key])
            
        self.scene_common_dict['all_format'] = format_all


        # logging.info ('------------------------------------------------------------------------------')
        """
        multipass
        """
        _multipass = self.get_multipass(doc)
        self.scene_common_dict['multi_pass'] = _multipass

        # logging.info ('------------------------------------------------------------------------------')
        """
        cameras
        """
        _cameras = self.get_cameras(doc)
        self.scene_common_dict['all_camera'] = _cameras
        
        # logging.info ('------------------------------------------------------------------------------')
        """
        C4D_Version
        #BaseDocument.GetData([type]) : <--R16 before
        #BaseDocument.GetDocumentData(): New in version R16.021-->
        """
        '''
        B盘用一个json来把不同版本不同写法弄成一个外部文件；
        每次有新的东西就不需要改这个脚本了，在那个外部文件修改即可。
        '''
        
        doc = documents.GetActiveDocument()
        
        #20180523-update 不同版本的sdk写法不一致
        data = self.kanada_get_document_data(doc)
        print(data)
        
        created_ver = data[c4d.DOCUMENT_INFO_PRGCREATOR_NAME]
        #file_version_dict['created_version'] = created_ver
        saved_ver = data[c4d.DOCUMENT_INFO_PRGWRITER_NAME]
        #file_version_dict['saved_version'] = saved_ver
        #file_ver = data[c4d.DOCUMENT_INFO_FILEVERSION] # 20180622update
        c4d_version = c4d.GetC4DVersion()
        #_version_dict = self.get_c4d_version(doc)
        self.scene_common_dict['created_version'] = created_ver
        self.scene_common_dict['saved_version'] = saved_ver
        #self.scene_common_dict['file_version'] = str(file_ver)
        self.scene_common_dict['c4d_software_version'] = c4d_version

        
        # ====sepreate line====
        # logging.info ('------------------------------------------------------------------------------')
        logging.info('///3. asset_json_dict/// \n')
        # All of the asset that scene used are in asset.json

        """
        textures
        """
        _texts = [] 
        texs = doc.GetAllTextures()
        for tex in texs:
            _texts.append(tex[1])
        self.asset_json_dict['textures'] = _texts

        # logging.info ('------------------------------------------------------------------------------')

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


        # logging.info ('------------------------------------------------------------------------------')

        
        self.parse_analyze_result()

        self.dump()
        #先分析完，dump后，做最后的检查
        #检查physical的sampler模式为Infinite下报错退出
        logging.info('hhhhhhhh')
        if self.sampler_mode == "Progressive":
            if self.progressive_mode == "Infinite":
                logging.info ('@KANADA physical Infinite mode is not supported..')
                self.exit()
               

    def get_multipass(self, doc):
        _multipass_dict = {}
        doc = c4d.documents.GetActiveDocument()
        rd = doc.GetActiveRenderData()
       
        single_savepath = rd[c4d.RDATA_PATH]
        multi_savepath = rd[c4d.RDATA_MULTIPASS_FILENAME]
        logging.info(single_savepath)
        logging.info(multi_savepath)
        logging.info(os.path.basename(multi_savepath))

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
        MyRenderSetting = doc.GetActiveRenderData()
        rd = doc.GetActiveRenderData()
        #engine = rd[c4d.RDATA_RENDERENGINE] # 1023342
        Renderer_ID = {0:'Standard',1:'Software_OpenGL',1023342:'Physical',1016630:'CineMan',1019782:'V_Ray',1029988:'Arnold(c4dtoa)',1029525:'OctaneRender',1036219:'Redshift'}
        Renderer = Renderer_ID[MyRenderSetting[c4d.RDATA_RENDERENGINE]]

        return Renderer

    def get_rs_phys_sampler(self, doc):
        """
        note
        :param str doc:
        :return:
        :rtype: str
        """
        Renderer = self.get_renderer(doc)
        _physical_sampler = ''
        
        if Renderer == "Physical":
            rd = doc.GetActiveRenderData()
            vp = rd.GetFirstVideoPost()
            Phy_S = {0:'Fixed',1:'Adaptive',2:'Progressive'}
            en_ch = ''
            if en_ch == Phy_S:
                _physical_sampler = Phy_S[int(vp[c4d.VP_XMB_RAYTRACING_SAMPLER])]
                logging.info('This is English Physical: ' + _physical_sampler)
            else:
                _physical_sampler = Phy_S[foo(vp[c4d.VP_XMB_RAYTRACING_SAMPLER])] # 如果是中文版的软件，这里会卡住
                logging.info('This is Chinese Physical: ' + _physical_sampler)

        return _physical_sampler

    def get_rs_phys_sampler_mode(self, doc):
        Renderer = self.get_renderer(doc)
        _physical_sampler_mode = ''

        if Renderer == "Physical":
            rd = doc.GetActiveRenderData()
            vp = rd.GetFirstVideoPost()
            
            Phy_S_Pro_Mode = {0:'Infinite',1:'Pass Count',2:'Time Limit'}
            _physical_sampler_mode = Phy_S_Pro_Mode[int(vp[c4d.VP_XMB_RAYTRACING_INTERACTIVE_MODE])]

        return _physical_sampler_mode


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
                logging.info('rf_mesh_path = ' + rf_mesh_path)
        c4d.CallCommand(12113) # Unselect All
        return _realflow_mesh

    def parse_realflow(self):
        logging.info ('[.@KANADA_parse_realflow]')
        #1.场景内的缓存路径
        if os.path.exists(self.asset_json_dict(_realflow_mesh)):
            logging.info('@KANADArrrrrr' + _realflow_mesh)
        #2.工程目录的路径
        #get_cg_file = os.path.basename(self.cg_file)

        cg_project_path = os.path.basename(self.G_INPUT_PROJECT_PATH)
        logging.info (cg_project_path)
        cg_file = self.G_INPUT_CG_FILE[len(self.G_INPUT_PROJECT_PATH):]
        logging.info(cg_file + '@KANADA88888888888')

        get_cg_file = cg_project_path + ':' + cg_file
        logging.info(get_cg_file + '@KANADA9999999999')


        if os.path.exists(get_cg_file):
            logging.info('@KANADAcccccccccc' + get_cg_file)

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
                logging.info('rf_particle_path = ' + rf_particle_path)
        c4d.CallCommand(12113) # Unselect All
        return _realflow_particle

    def parse_analyze_result(self):
        self.parse_error(self.asset_json_dict['textures'])
        # parse_mesh
        # ...
 
    def parse_error(self, textures):
        doc = documents.GetActiveDocument()
        rd = doc.GetActiveRenderData()
        vp = rd.GetFirstVideoPost()

        for texture in textures:
            texture = os.path.normpath(texture)
            """
            35000 贴图检查
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
                logging.info('root_dir = ' + root_dir)
                tex_dir = os.path.join(root_dir, 'tex')  
                tex_file = os.path.join(tex_dir, texture)
                #tex_file = tex_file.replace('\\', '/')
                logging.info('tex = ' + tex_file)
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
            elif texture.endswith('.3gp'):
                if not os.path.exists(texture):
                    self.tex_video_format.append(texture)
            elif texture.endswith('.avi'):
                if not os.path.exists(texture):
                    self.tex_video_format.append(texture)
            elif texture.endswith('.wmv'):
                if not os.path.exists(texture):
                    self.tex_video_format.append(texture)
            elif texture.endswith('.asf'):
                if not os.path.exists(texture):
                    self.tex_video_format.append(texture)
            else: 
                pass

        """
            35002 FPS_check检查
        """
        fps = doc.GetFps()
        logging.info (str(fps))
        Render_Settings_fps = int(rd[c4d.RDATA_FRAMERATE])
        logging.info(str(Render_Settings_fps))

        if str(fps) != str(Render_Settings_fps):
            self.FPS_check.append('%s:%s' % ('fps', fps))
            self.FPS_check.append('%s:%s' % ('Render_Settings_fps', Render_Settings_fps))
        else:
            pass

        """
            35003 output_avi_movie检查 20180605update
        """
        self.common_format = self.task_json_dict['scene_info']['common']
        self.ri_format = self.common_format['regular_image_format']
        self.mp_format = self.common_format['multi_pass_format']
        #ri_img_format = self.common_format.keys('regular_image_format')
        #mp_img_format = self.common_format.keys('multi_pass_format')
        #logging.info(ri_img_format, mp_img_format)
        logging.info('iiiiii')
        logging.info (type(self.ri_format)),(type(self.mp_format))

        softversion = int(c4d.GetC4DVersion())
        logging.info('1')
        if softversion >= 19000 and softversion <= 20000:
            for avi_format in self.ri_format:
                if 'AVI' in self.ri_format:
                    if '%s: %s' % ('regular_image_format', "AVI") not in self.output_avi_movie:
                        self.output_avi_movie.append('%s:%s' % ('regular_image_format', "AVI"))
                        break
            for avi_format in self.mp_format:
                if 'AVI' in self.mp_format:
                    if '%s: %s' % ('multi_pass_format', "AVI") not in self.output_avi_movie:
                        self.output_avi_movie.append('%s:%s' % ('multi_pass_format', "AVI"))
                        break
        else:
            logging.info('2')
            for avi_format in self.ri_format:
                if 'AVI Movie' in self.ri_format:
                    if '%s: %s' % ('regular_image_format', "AVI Movie") not in self.output_avi_movie:
                        self.output_avi_movie.append('%s:%s' % ('regular_image_format', "AVI Movie"))
                        break
            for avi_format in self.mp_format:
                if 'AVI Movie' in self.mp_format:
                    if '%s: %s' % ('multi_pass_format', "AVI Movie") not in self.output_avi_movie:
                        self.output_avi_movie.append('%s:%s' % ('multi_pass_format', "AVI Movie"))
                        break
        logging.info('3')

        
        """
            35004 physical_sampler_mode检查
        """
       
        # self.get_rs_phys_sampler,get_rs_phys_sampler_mode 2个都是返回是str
        
        self.sampler_mode = self.get_rs_phys_sampler(doc)
        self.progressive_mode = self.get_rs_phys_sampler_mode(doc)

        if self.sampler_mode == "Progressive":
            if self.progressive_mode == "Infinite":
                logging.info ('@KANADA physical Infinite checking...')
                
                sampler_str = 'sampler: %s' % self.sampler_mode
                progressive_str = 'progressive: %s' % self.progressive_mode
                #str.append(字符串组合)
                logging.info ('@KANADA 4...')
                self.physical_sampler_mode.append(sampler_str)
                self.physical_sampler_mode.append(progressive_str)
                logging.info ('@KANADA 5...')
        

        
        """
            35005 octane_render_passes 20160606update
        
        # 如果是用octane passes的话渲染设置下的通道输出必须勾选以及输出路径
        if Renderer=="OctaneRenderer":
            oc_enable = int(vp[c4d.SET_PASSES_ENABLED])
            logging.info (oc_enable)
            if oc_enable == '1':
                multipass_save_enabled = int(rd[c4d.RDATA_MULTIPASS_SAVEIMAGE])
                multipass_save_path = rd[c4d.RDATA_MULTIPASS_FILENAME]
                logging.info(' %s either enable and %s: ' % multipass_save_enabled, multipass_save_path)
                if multipass_save_enabled == '0':
                    self.octane_render_passes.append('%s:%s' % oc_enable)
                logging.info("your octane render passes enabled, please enable your multipass and set the path of output!!!")
        """

        logging.info ('==============================================')
        """
        '35000':missing tex,丢失贴图检查
        '35001':the texture is video format，贴图存在视频格式检查
        '35002':FPS unified，帧速率是否一致检查
        
        若C4D的主图或者通道输出格式为视频格式(RI or MP output format is AVI movie)：
        Error:   35003(启用参数修改), 
        warning: 30000(不启用参数修改)
        
        '35004':physical_sampler_mode，渲染器physical为Infinite检查
        '35005':octane render passes，渲染器是octane勾选passes检查保存路径
        '35006':C4D文件用了第三方渲染器，在提交任務時未配置對應渲染器和版本，將導致渲染失敗,not yet
        '35007':文件版本与配置版本不匹配
        """

        # if tips.json 不出现错误码的时候写, 空的时候不去写

        if len(self.tex_missings) > 0:
            self.missings['35000'] = self.tex_missings
        if len(self.tex_video_format) > 0:          
            self.missings['35001'] = self.tex_video_format
        if len(self.FPS_check) > 0:
            self.missings['35002'] = self.FPS_check
        if len(self.output_avi_movie) > 0: 
            logging.info('aa:%s'%self.output_avi_movie)
            if self.auto_commit is False: #auto_commit=2,手动提交
                logging.info('bb:%s'%self.auto_commit)
                self.missings['35003'] = self.output_avi_movie #35003 error
                logging.info('35003:%s'%self.output_avi_movie)
            else:                        #auto_commit=1,自动提交
                logging.info('bb:%s'%self.auto_commit)
                logging.info('30000:%s'%self.output_avi_movie)
                self.missings['30000'] = self.output_avi_movie #30000 warning

        if len(self.physical_sampler_mode) > 0:            
            self.missings['35004'] = self.physical_sampler_mode

        #self.missings['35005'] = self.octane_render_passes

        #sys.stdout.flush()
        

    def dump(self):
        logging.info ('[.@KANADA_dump]')
        # dicts= sorted(self.scene_common_dict.items(), key=lambda d:d[1], reverse = True)
        logging.info(self.scene_common_dict)
        self.task_json_dict['scene_info']['common'] = self.scene_common_dict
        self.task_json_dict['scene_info']['renderer'] = self.scene_renderer_dict
        
        logging.info(str(self.task_json_dict['software_config'])+ '777777777')
        
        # write task.json
        with open(self.task_json, 'w') as outfile:
            json.dump(self.task_json_dict, outfile, indent=4, ensure_ascii=False)
            logging.info('task_json dump....')
        # write asset.json
        with open(self.asset_json, 'w') as outfile:
            json.dump(self.asset_json_dict, outfile, indent=4, ensure_ascii=False)
            logging.info('asset_json dump....')
        #write missings
        with open(self.tips_json, 'w') as outfile:
            json.dump(self.missings, outfile, indent=4, ensure_ascii=False)
            logging.info('tips_json dump....')

def PluginMessage(id, data):
    logging.info ('.[@KANADA PluginMessage in---------]')
    
    if id == c4d.C4DPL_COMMANDLINEARGS:
        cg_file = ''
        task_json = ''
        asset_json = ''
        tips_json = ''
        auto_commit = '1'

        for arg in sys.argv:
            #arg = arg.decode('gbk').encode('utf-8')
            logging.info ('load c4d version...' + arg)
            if arg.startswith('-cg_file'):
                cg_file = arg.replace('-cg_file=', '').strip('"')
            elif arg.startswith('-task_json'):
                task_json = arg.replace('-task_json=', '').strip('"')
            elif arg.startswith('-asset_json'):
                asset_json = arg.replace('-asset_json=', '').strip('"')
            elif arg.startswith('-tips_json'):
                tips_json = arg.replace('-tips_json=', '').strip('"') 
            elif arg.startswith('-auto_commit'):
                auto_commit = arg.replace('-auto_commit=', '').strip('"') 

        logging.info('load c4d file... ' + cg_file)
        
        if os.path.exists(cg_file):
            c4d.documents.LoadFile(cg_file)
            c4d_parser = C4dParser(cg_file, task_json, asset_json, tips_json, auto_commit)
            c4d_parser.parse()
        else:
            logging.info ('load c4d file is not exists or damaged...')
            

        return True

    return False