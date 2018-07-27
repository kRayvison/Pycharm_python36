#.A ---- customer cannot assign folder
#.B ---- customer can assign folder
#.d ---- the item is a folder
#.f ---- the item is a file
#.Blender_render-'Lion''QQ:58701328'

import bpy, os, sys, json
import os,sys,time
import subprocess,threading,shutil

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

def abc(filepath):
    file = open(filepath, 'w')
    print("1111111111")
    
    #output start and end frame
    
    for scene in bpy.data.scenes:
        start = bpy.context.scene.frame_start
        end = bpy.context.scene.frame_end
        frame_step = bpy.context.scene.frame_step
        self.scene_common_dict['scene_info']['common']["frames"] = "%s-%s[%s]"%(str(start),str(end),str(frame_step))
        width = bpy.context.scene.render.resolution_x
        height = bpy.context.scene.render.resolution_y
        Format = bpy.data.scenes[0].render.image_settings.file_format
          
    file.close()

print("-------------.." +sys.argv[6])
abc(sys.argv[6])