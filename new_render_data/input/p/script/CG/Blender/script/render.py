#.A ---- customer cannot assign folder
#.B ---- customer can assign folder
#.d ---- the item is a folder
#.f ---- the item is a file
#.Blender_render-'Lion''QQ:58701328'

import bpy, sys, re, json

wfile = open('RB_blender_debug.txt','w+')
wfile.write("------------debug-----------------")

def blend(filepath):
    with open(filepath, 'r') as json_file:
        print("123")
        task_json_dict = json.load(json_file)
        w = task_json_dict['scene_info']['common']['width']
        h = task_json_dict['scene_info']['common']['height']
        bpy.data.scenes[0].render.resolution_x = int(w)
        bpy.data.scenes[0].render.resolution_y = int(h)
        
        #output texture path
    bpy.data.scenes[0].render.resolution_percentage = 100
    bpy.context.scene.render.threads_mode = 'AUTO'
    bpy.context.scene.render.tile_x = 16
    bpy.context.scene.render.tile_y = 16
    bpy.context.user_preferences.system.use_scripts_auto_execute = True

#sys.stdout.write("write-------------.." +sys.argv[15])
print("print-------------.." +sys.argv[0]+sys.argv[15])
wfile.write("\n==------"+sys.argv[15]+"----------\n")
wfile.close()
blend(sys.argv[15])
