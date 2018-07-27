#!/usr/bin/env python
# -*- coding=utf-8 -*-
#.A ---- customer cannot assign folder
#.B ---- customer can assign folder
#.d ---- the item is a folder
#.f ---- the item is a file
#.Blender_render-'Lion''QQ:58701328'

import bpy, os, sys, json

def abc(filepath,tips_json,asset_json):
    if not os.path.exists(filepath):
        return False
        
    #output start and end frame
    for scene in bpy.data.scenes:
        start = bpy.context.scene.frame_start
        print(str(start))
        end = bpy.context.scene.frame_end
        print(str(end))
        frame_step = bpy.context.scene.frame_step
        print(str(frame_step))
        width = bpy.context.scene.render.resolution_x
        height = bpy.context.scene.render.resolution_y
        Format = bpy.data.scenes[0].render.image_settings.file_format
        common_dict={}
        common_dict['frames']=str(start)+'-'+str(end)+'['+str(frame_step)+']'
        common_dict['width']=str(width)
        common_dict['height']=str(height)
        common_dict['Render_Format']=str(Format)

    with open(filepath, 'r') as json_file:
        print("123")
        #if 'common' not in task_json_dict['scene_info']:
            #task_json_dict['scene_info']['common']  = {}
        task_json_dict = json.load(json_file)
        if 'scene_info' not in task_json_dict:
            task_json_dict['scene_info']  = {}
            
        if 'common' not in task_json_dict['scene_info']:
            task_json_dict['scene_info']['common']  = {}
            
        task_json_dict['scene_info']['common']  = common_dict
    with open(filepath, 'w') as json_file:
        json.dump(task_json_dict, json_file, indent=4, ensure_ascii=False)
    with open(tips_json, 'w') as tips_json_temp:
        tips_json_dict={}
        json.dump(tips_json_dict, tips_json_temp, indent=4, ensure_ascii=False)
    with open(asset_json, 'w') as asset_json_temp:
        asset_json_dict={}
        json.dump(asset_json_dict, asset_json_temp, indent=4, ensure_ascii=False)
        
        #file_set_error
        if str(Format) == ('AVI_JPEG' or 'AVI Raw' or 'Frame Server' or 'FFmpeg video'):
            with open(tips_json, 'w') as tips_json_temp:
                if 'error_info' not in tips_json_dict:
                    error_dict = {}
                    tips_json_dict['36000']  =[]
                    json.dump(tips_json_dict, tips_json_temp, indent=4, ensure_ascii=False)
        #file_set_warning
        if str(frame_step) != ('1'):
            with open(tips_json, 'w') as tips_json_temp:
                if 'error_info' not in tips_json_dict:
                    error_dict = {}
                    tips_json_dict['36001']  =[]
                    json.dump(tips_json_dict, tips_json_temp, indent=4, ensure_ascii=False)
            
print("-------------.." +sys.argv[6])
print("-------------.." +sys.argv[7])
print("-------------.." +sys.argv[8])
abc(sys.argv[6],sys.argv[7],sys.argv[8])
