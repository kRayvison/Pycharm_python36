#.A ---- customer cannot assign folder
#.B ---- customer can assign folder
#.d ---- the item is a folder
#.f ---- the item is a file
#.Blender_render-'Lion''QQ:58701328'

import bpy, os, sys, time, json
import codecs,time

class BlenderParser():
    def __init__(self, *args):
        print (time.strftime('%y/%m/%d/%H/%M/%S'))
        self.task_json_dict = {}
        self.scene_common_dict = {}
        self.scene_renderer_dict = {}
        self.asset_json_dict = {}
        self.tips_json_dict = {}
        self.cg_file  = args[0]
        self.task_json = args[1]
        self.asset_json = args[2]
        self.tips_json = args[3]
        
    def __del__(self):
        self.exit()
    
    def init(self):
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
            
        return True
        
    def analyze(self, *args):
        #output start and end frame
        start_frame = bpy.context.scene.frame_start
        print(str(start_frame))
        end_frame = bpy.context.scene.frame_end
        print(str(end_frame))
        frame_step = bpy.context.scene.frame_step
        print(str(frame_step))
        self.scene_common_dict["frames"] = "%s-%s[%s]"%(start_frame,end_frame,frame_step)
        #output width and height
        width = bpy.context.scene.render.resolution_x
        print("Width::" + str(width) + "\n")
        self.scene_common_dict['width'] = str(width)
        
        height = bpy.context.scene.render.resolution_y
        print("Height::" + str(height) + "\n")
        self.scene_common_dict['height'] = str(height)
        
        Format = bpy.data.scenes[0].render.image_settings.file_format
        print("Render_format::" + str(Format) + "\n")
        self.scene_common_dict['Format'] = str(Format)
            
    def dump(self):
        print ('[.@Lion_dump]')
        # dicts= sorted(self.scene_common_dict.items(), key=lambda d:d[1], reverse = True)
        print(self.scene_common_dict)
        self.task_json_dict['scene_info']['common'] = self.scene_common_dict
        self.task_json_dict['scene_info']['renderer'] = self.scene_renderer_dict
        
        print(str(self.task_json_dict['software_config'])+ '777777777')
        
        # write task.json
        with open(self.task_json, 'w') as outfile:
            json.dump(self.task_json_dict, outfile, indent=4, ensure_ascii=False)
        # write asset.json
        with open(self.asset_json, 'w') as outfile:
            json.dump(self.asset_json_dict, outfile, indent=4, ensure_ascii=False)
        #write missings
        with open(self.tips_json, 'w') as outfile:
            json.dump(self.missings, outfile, indent=4, ensure_ascii=False) 
