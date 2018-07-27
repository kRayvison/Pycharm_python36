import os,sys,time
import argparse
import json
import re
# import traceback
import lux
from multiprocessing import cpu_count

base_keyshot = os.path.dirname(sys.path[0])
sys.path.append("%s/function"%base_keyshot)
from KeyshotUtil import KeyshotUtil
from KeyshotPlugin import KeyshotPlugin

parser = argparse.ArgumentParser()
parser.add_argument('-project', type=str, required=True, help='.bip file to render')
parser.add_argument('-frame', type=str, required=True, help='frames to render')
parser.add_argument('-outdir', type=str, required=True, help='image with dir to render to')
parser.add_argument('-taskbase', type=str, required=True, help='The render task path ')
parser.add_argument('-plugindir', type=str, required=True, help='The plugin dirt ')
parser.add_argument('-custid', type=str, required=True, help='The user id  ')

args = parser.parse_args()

class ks_fileBase():
    
    def __init__(self,args=""):
        KeyshotUtil.print_times('Start ks base...')
        self.render_node_type = []
        self.args = args
        self.frame = ''
        self.basedir = os.path.abspath(self.args.project)
        self.basedir = self.basedir.replace("\\","/")
        self._hip_val = os.path.dirname(self.args.project).replace("\\","/")
        self._reset_val = False
        self.DataSet()

    def loadbipfile(self):

        self.bip_file=self.args.project
        if os.path.exists(self.bip_file):
            KeyshotUtil.print_times ("Loading bip file: %s" % self.bip_file)
            try:
                lux.openFile(self.bip_file)
                lux.pause()
                KeyshotUtil.print_times ("Loading bip file success")

            except (IOError ,ZeroDivisionError) as e:
                KeyshotUtil.print_times (e)
        else:
            KeyshotUtil.print_times ("ERROR: the bip file is not exist!")
            sys.exit(1)

    def RenderPicBaseSet(self):
        self._opts = lux.getRenderOptions()
        self._computer_thread = cpu_count()
        # just for this setting the render option, and use full threads in rendering 
        self._opts.setThreads(self._computer_thread-3) 

        # print(str(self.Json_adict["scene_info"]))

        self._out_name = self.Json_adict["scene_info"]["outputname"]
        self._width = int(self.Json_adict["scene_info"]["width"])
        self._height = int(self.Json_adict["scene_info"]["height"])
        self._format = self.Json_adict["scene_info"]["format"].lower()
        self._render_cameras = self.Json_adict["scene_info"]["renderable_cameras"]
        KeyshotUtil.print_times("This Jobs information:")
        KeyshotUtil.print_times("Output name: %s "%self._out_name)
        KeyshotUtil.print_times("Width: %d "%self._width)
        KeyshotUtil.print_times("Height: %d "%self._height)
        KeyshotUtil.print_times("Format: %s "%self._format)
        KeyshotUtil.print_times("Camreas: %s "%self._render_cameras)
        ##---------------------------------------
        if self.Json_adict["scene_info"]["sample_type"] == "maxsample":
            self._opts.setMaxSamplesRendering(int(float(self.Json_adict["scene_info"]["maxsample"])))
            KeyshotUtil.print_times("Render sample type: maxsample. ")
        if self.Json_adict["scene_info"]["sample_type"] == "maxtime":
            self._opts.setMaxTimeRendering(float(self.Json_adict["scene_info"]["maxtime"])*60)
            KeyshotUtil.print_times("Render sample type: maxtime. ")
        if self.Json_adict["scene_info"]["sample_type"] == "advanced":
            KeyshotUtil.print_times("Render sample type: advanced. ")
        ##---------------------------------------

    def RenderVrBaseSet(self):
        _vr_modes = {"turntable":1,"spherical":2,"hemispherical":3,"tumble":4,"custom":5}
        _vr_rotation_centers = {"enviroment":1,"object":2,"camera":4,"camera_pivot":5}
        # print(str(self.Json_adict["vr_info"]))

        self._vr_mode = _vr_modes[self.Json_adict["vr_info"]["vr_type"].lower()]
        self._vr_center = _vr_rotation_centers[self.Json_adict["vr_info"]["vr_center"].lower()]
        self._hframes = int(self.Json_adict["vr_info"]["vr_smooth_h"])
        self._vframes = int(self.Json_adict["vr_info"]["vr_smooth_v"])
        self._vr_smooth = True if float(self._hframes)>0 or float(self._hframes)>0 else False
        self._vr_view = []

    def Custmset(self):
        KeyshotUtil.print_times("Custom Setup start...")
        
        _files_name = []
        _config_patn = "%s/custom/Bhand"%self.args.plugindir
        from custom import Bhand
        _function_all = dir(Bhand)
        for (dirpath, dirnames, filenames) in os.walk(_config_patn):
            _files_name.extend(filenames)
        for scr in _files_name:
            _py_list = scr.split(".py")
            if _py_list[-1]=='' and _py_list[0] in _function_all:
                cmds = "Bhand.%s.main(self)" % _py_list[0]
                ## print(cmds)
                try:
                    exec(cmds)
                except Exception as e:
                    KeyshotUtil.print_times(e)
        KeyshotUtil.print_times("Custom Setup end.")

    def DataSet(self):
        KeyshotUtil.print_times("DataSet Setup start...")
        cfg_path = '%s/cfg'%self.args.taskbase.replace("\\","/")
        out_dir = '%s/output'%self.args.taskbase.replace("\\","/")
        self._cfg_task = '%s/task.json'%cfg_path
        cfg_asset = '%s/asset.json'%cfg_path

        self.Json_adict = eval(open(self._cfg_task, 'r').read()) if os.path.exists(self._cfg_task) else {}
        self.Asset_adict = eval(open(cfg_asset, 'r').read()) if os.path.exists(cfg_asset) else {}
        if len(self.Asset_adict) == 0:KeyshotUtil.print_times("Asset_adict is empty.")
        KeyshotUtil.print_times("DataSet Setup end.")


    def configs(self):
        KeyshotUtil.print_times("Config Setup start...")
        ## All the code in configs folder will run one time 
        _files_name = []
        _config_patn = "%s/configs/Bhand"%self.args.plugindir
        from configs import Bhand
        _function_all = dir(Bhand)
        for (dirpath, dirnames, filenames) in os.walk(_config_patn):
            _files_name.extend(filenames)
        for scr in _files_name:
            _py_list = scr.split(".py")
            if _py_list[-1]=='' and _py_list[0] in _function_all:
                cmds = "Bhand.%s.main(self)" % _py_list[0]
                try:
                    exec(cmds)
                except Exception as e:
                    KeyshotUtil.print_times(e)
        KeyshotUtil.print_times("Config Setup end.")


    def RenderPic(self,this_frame):
        if len(self._render_cameras) == 0:
            _render_camera = lux.getCamera()
            if _render_camera=="active":
                _render_camera="default"
            KeyshotUtil.print_times("Without any camera give,use the current scene camera. ")
            lux.setCamera(_render_camera)
            _Save_File = "%s_%s.%s"%(self._out_name,"%04d" % this_frame,self._format)
            self._outputfile = "%s/%s"%(self.args.outdir,_Save_File)
            self.renderpic()
        elif len(self._render_cameras)==1:
            _render_camera = self._render_cameras[0]
            lux.setCamera(_render_camera)
            _resub_cam=re.sub(r'\W+',"_",_render_camera)
            _Save_File = "%s_%s_%s.%s"%(self._out_name,_resub_cam,"%04d" % this_frame,self._format)
            self._outputfile = "%s/%s"%(self.args.outdir,_Save_File)
            self.renderpic()
        elif len(self._render_cameras)>1:
            for cam in self._render_cameras:
                KeyshotUtil.print_times ("Render camera: %s."%cam)
                lux.setCamera(cam)
                _resub_cam=re.sub(r'\W+',"_",_render_camera)
                _Save_File = "%s_%s_%s.%s"%(self._out_name,_resub_cam,"%04d" % this_frame,self._format)
                self._outputfile = "%s/%s"%(self.args.outdir,_Save_File)
                self.renderpic()


    def renderpic(self):
        KeyshotUtil.print_times ("Render pic start.")
        KeyshotUtil.print_times ("Render pic will saved in: %s."%self._outputfile)
        ## -------------------------------------------------------------------------------------
        ## make caches evry frame
        this_time = time.time()
        lux.unpause()
        if self.Json_adict["scene_info"]["sample_type"] == "maxtime":
            self._opts.setMaxTimeRendering(3.0)
            lux.renderImage(path = self._outputfile, width = 3, height = 3, opts = self._opts)
            self._opts.setMaxTimeRendering(float(self.Json_adict["scene_info"]["maxtime"]))
        elif self.Json_adict["scene_info"]["sample_type"] == "maxsample":
            lux.renderImage(path = self._outputfile, width = 3, height = 3, opts = self._opts)
        self._opts.setThreads(self._computer_thread)
        ##-------------------------------------------------------------------------------------
        lux.renderImage(path = self._outputfile, width = self._width, height = self._height,
                         opts = self._opts)

        KeyshotUtil.print_times ("Render pic end.")
        KeyshotUtil.print_times ("Render times: %d s." % int(time.time()-this_time))

    def rendervr(self):
        if not len(self._vr_view)==0:
            if self._vr_mode==5:
                if self._vr_smooth:
                    lux.renderVR(folder=self.args.outdir,name=self._out_name,type=self._vr_mode,center=self._vr_center,
                                width=self._width,height=self._height,hframes=self._hframes,vframes=self._vframes,
                                hbegin=self._vr_view[0],hend=self._vr_view[1],vbegin=self._vr_view[2],vend=self._vr_view[3])
                else:
                    lux.renderVR(folder=self.args.outdir,name=self._out_name,type=self._vr_mode,center=self._vr_center,
                                width=self._width,height=self._render_size[1],hbegin=self._vr_view[0],
                                hend=self._vr_view[1],vbegin=self._vr_view[2],vend=self._vr_view[3])
        else:
            if self._vr_smooth:
                lux.renderVR(folder=self.args.outdir,name=self._out_name,type=self._vr_mode,center=self._vr_center,
                            width=self._width,height=self._height,
                            hframes=self._hframes,vframes=self._vframes)
            else:
                lux.renderVR(folder=self.args.outdir,name=self._out_name,type=self._vr_mode,center=self._vr_center,
                            width=self._width,height=self._height)


    def Extued(self):
        pass
        # self.configs()
        # self.Custmset()


def KStMmain():

    ## --------------------creat a job----------------------------
    ks_obj = ks_fileBase(args)
    KeyshotUtil.print_times('Load bip file start...')
    try:
        ks_obj.loadbipfile()
    except :
        KeyshotUtil.print_times('Load hip ignore Errors.')
    KeyshotUtil.print_times('Load hip file end.')

    sys.stdout.flush()
    time.sleep(1)

    ## -----------------------------------------------------------

    KeyshotUtil.print_times('Jobs start...')

    ## ----------------------loop render ------------------------
    ## --------------------- loop type --------------------------

    if ks_obj.Json_adict["scene_info"]["rendertypes"] == "picture":
        frame_adict,types = KeyshotPlugin.FramesAnalyse(args.frame)
        ## if types != 0 will start multiframe render
        if len(frame_adict.keys()):
            KeyshotUtil.print_times(str(frame_adict))
            try_times = 3
            run_times = 0
            run_result = True
            while run_times<try_times:
                try:
                    KeyshotUtil.print_times('Job type: Picture Render job ')
                    ks_obj.Extued()
                    ks_obj.RenderPicBaseSet()
                    
                    sys.stdout.flush()
                    time.sleep(1)
                
                    aim_names = []
                    for key in frame_adict.keys():
                        frames = frame_adict[key]
                        KeyshotUtil.print_times('Render frames: %s'%frames)
                        ## do render here
                        ## keyshot start from 0,so set frame 0 will render frame 1
                        lux.setAnimationFrame((int(frames[0])-1)if int(frames[0])>0 else 1)
                        ks_obj.RenderPic(int(frames[0]))
                        if types != 0:
                            aim_names = KeyshotPlugin.copyfiles(args.outdir,frames[0],aim_names)
                            print("[_____render end_____][%s]"%str(frames[0]))

                    run_times = try_times
                    run_result = True
                except :
                    run_times +=1
                    info = sys.exc_info()
                    # for file, lineno, function, text in traceback.extract_tb(info[2]):
                    #     print file, "line:", lineno, "in", function
                    #     print text
                    """ get the node which call Errors """
                    tx = "** %s: %s" % info[:2]
                    list_tx = tx.split("\n") if "\n" in tx else [tx]
                    print("="*80)
                    print(list_tx)
                    run_times = try_times
                    # KeyshotPlugin.TracebackError(list_tx,hfs_obj.Asset_adict,ropnode)

                    # if hfs_obj._reset_val:
                    #     """  reset the node value  """
                    #     pass
                    # else:
                    #     run_times = try_times
                        
                    run_result = False
                    if run_times<=try_times:
                        print("Render rease errors ",run_times)
                        print("="*80)
            if not run_result:
                sys.exit(8860)
    elif ks_obj.Json_adict["scene_info"]["rendertypes"] == "vr":
        KeyshotUtil.print_times('Job type: Vr Render job ')
        ks_obj.RenderPicBaseSet()
        ks_obj.RenderVrBaseSet()
        ks_obj.rendervr()
    else:
        KeyshotUtil.print_times('Job only for picture render or vr renders.')
        sys.exit(8861)


    KeyshotUtil.print_times('Jobs end.')
    try:
        for elm in ["keyshot.exe"]:
            os.system(r'wmic process where name="%s" delete'%elm)
        # KeyshotUtil.KillApps(["keyshot.exe"])
    except:
        print("Cant kill the keyhsot.exe or others")
    sys.exit(0)

if __name__=="__main__":

    print('...')
    print('-'*50)
    print('-'*50)
    print('Creat Keyshot base information for running this Job, start Keyshot_Files_Function...')
    print('...')    
    print(args)
    KStMmain()
    
