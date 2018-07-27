#.A ---- customer cannot assign folder
#.B ---- customer can assign folder
#.d ---- the item is a folder
#.f ---- the item is a file
#.Blender_render-'Lion''QQ:58701328'

import bpy, sys, re

wfile = open('RB_blender_debug.txt','w+')
wfile.write("------------debug-----------------")

def blend(rfile_name):
    rHandle = open(rfile_name,'r')
        #output texture path
    bpy.data.scenes[0].render.resolution_percentage = 100
    bpy.context.scene.render.threads_mode = 'AUTO'
    bpy.context.scene.render.tile_x = 16
    bpy.context.scene.render.tile_y = 16
    bpy.context.user_preferences.system.use_scripts_auto_execute = True

    while True:
        eachLine = rHandle.readline()
        if not eachLine:
            break
        bpy.ops.file.make_paths_absolute()
        
        #print("....."+eachLine) 
        if eachLine.split('::')[0] == "Width":
            w = eachLine.split('::')[1]
            print("w___"+w)
            bpy.data.scenes[0].render.resolution_x = int(w)
        if eachLine.split('::')[0] == "Height":
            h = eachLine.split('::')[1]
            print("h___"+h)
            bpy.data.scenes[0].render.resolution_y = int(h)
    rHandle.close


#sys.stdout.write("write-------------.." +sys.argv[10])
print("print-------------.." +sys.argv[0]+sys.argv[10])
wfile.write("\n==------"+sys.argv[10]+"----------\n")
wfile.close()
blend(sys.argv[10])
