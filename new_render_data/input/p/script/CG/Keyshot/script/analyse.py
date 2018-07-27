import os,sys,time
import argparse
import json
import lux

base_keyshot = os.path.dirname(sys.path[0])
sys.path.append("%s/function"%base_keyshot)
from KeyshotUtil import KeyshotUtil
from KeyshotPlugin import KeyshotPlugin

parser = argparse.ArgumentParser()
parser.add_argument('-project', type=str, required=True, help='.bip file to render')
parser.add_argument('-outdir', type=str, required=True, help='image with dir to render to')
parser.add_argument('-plugindir', type=str, required=True, help='The plugin path in B disk')
parser.add_argument('-custid', type=str, required=True, help='The user id  ')

args = parser.parse_args()

class ks_fileBase():
    
    def __init__(self,args=""):
        KeyshotUtil.print_times('Start keyshot base.__init__')

        self.args = args
        self.frame = ''

        self.asset_adict = {} ### for asset.json 
        self.foler_adict = {} ### the asset in folders
        self.tips_adict = {}
        self.check_history = {}


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

    def DataSet(self):
        KeyshotUtil.print_times("DataSet Setup start...")

        sys.path.append(self.args.plugindir)
        cfg_path = '%s/cfg'%self.args.outdir.replace("\\","/")
        self._cfg_task = '%s/task.json'%cfg_path
        self._cfg_asset = '%s/asset.json'%cfg_path
        self._cfg_tips = '%s/tips.json'%cfg_path
        self._cfg_folder = '%s/folder_asset.json'%cfg_path

        datapath = "B:\plugins\houdini\data"
        data_file = "%s/error_id.json"%datapath

        self.Json_adict = eval(open(self._cfg_task, 'r').read()) if os.path.exists(self._cfg_task) else {}
        # self.Error_ids = eval(open(data_file, 'r').read()) if os.path.exists(data_file) else {}

        KeyshotUtil.print_times("DataSet Setup end.")

    def configs(self):
        KeyshotUtil.print_times("Config Setup start...")
        ## All the code in configs folder will run one time 
        _files_name = []
        # _config_patn = "%s/configs/Bhand"%self.args.plugindir
        # from configs import Bhand
        # _function_all = dir(Bhand)
        # for (dirpath, dirnames, filenames) in os.walk(_config_patn):
        #     _files_name.extend(filenames)
        # for scr in _files_name:
        #     _py_list = scr.split(".py")
        #     if _py_list[1]=='' and _py_list[0] in _function_all:
        #         cmds = "Bhand.%s.main(self)" % _py_list[0]
        #         try:
        #             exec cmds
        #         except Exception as e:
        #             KeyshotUtil.print_times(e)
        KeyshotUtil.print_times("Config Setup end.")

    def GetAsses(self):
        KeyshotUtil.print_times('')
        KeyshotUtil.print_times("GetAsses start...")
        pass
        ##Informations 
        # HoudiniPlugin.TipsInfo(self)
        KeyshotUtil.WriteFile(self.asset_adict,self._cfg_asset,'json')
        # KeyshotUtil.WriteFile(self.foler_adict,self._cfg_folder,'json')
        KeyshotUtil.WriteFile(self.tips_adict,self._cfg_tips,'json')

    def analy_info(self):
        KeyshotUtil.print_times("Analysis informations start...")

        if not self.args.outdir== '':
            self.file_info = self.args.outdir
        else:
            self.file_info = "D:/houdini/RS/Analysis_info.txt"
            if not os.path.exists("D:/houdini/RS"):
                os.makedirs("D:/houdini/RS")
            KeyshotUtil.print_times("The function is not used as analysis,write the infomation to default file")

        scene_info = {}
        _Animat = lux.getAnimationInfo()

        scene_info["frames"] = "1-%d[1]"%(_Animat['frames'] if _Animat['frames']>0 else 1)
        scene_info["times"] = "%.2f" % _Animat['duration']
        
        _Scene_ifo = lux.getSceneInfo()
        scene_info["name"] = _Scene_ifo['name']
        scene_info["width"] = str(_Scene_ifo['width'])
        scene_info["height"] = str(_Scene_ifo['height'])
        _Scene_camera = lux.getCameras()
        _curent_camera= lux.getCamera()
        if _curent_camera=="active":
            _curent_camera="default"
        if _curent_camera in _Scene_camera:
            _Scene_camera.remove(_curent_camera)
        _Scene_camera.insert(0,_curent_camera)
        scene_info["cameras"] = _Scene_camera
        
        _opts = lux.getRenderOptions()
        _opts_adict = _opts.getDict()
        # print(_opts_adict)
        scene_info["maxsample"] = "64"
        scene_info["maxtime"] = "3"

        _sample_type="maxtime"
        _values = 0
        if _opts_adict['progressive_max_time']==0.0 and _opts_adict['advanced_samples']==0:
            _sample_type="maxsample"
            _values = _opts_adict['progressive_max_samples']
            scene_info["maxsample"] = "64"
        elif _opts_adict['progressive_max_time']==0.0 and _opts_adict['progressive_max_samples']==0:
            _sample_type="advanced"
            _values = _opts_adict['advanced_samples']
        else:
            _values = _opts_adict['progressive_max_time']
            scene_info["maxtime"] = str(_values)
        scene_info["sample_type"] = _sample_type
        print(_sample_type,_values)
        print(scene_info)

        ## defualt values
        scene_info["renderable_cameras"] = []
        scene_info["outputname"] = "untitled"
        scene_info["format"] = "JPEG"
        scene_info["rendertypes"] = "picture"

        ## common
        common_adict = {}
        common_adict["rendertype_list"] = [ "picture","vr"]
        common_adict["format_list"] = ["jpeg","png","exr","tif","tiff"]
        scene_info["common"] = common_adict

        ## vr adict
        vr_info_adict = {
                            "vr_type":"spherical",
                            "vr_center":"object",
                            "vr_crop_distance":"3000",
                            "vr_crop_angle":"-50",
                            "vr_crop_oblique":"15",
                            "vr_crop_Perspective":"35",
                            "vr_smooth_h":"18",
                            "vr_smooth_v":"9"   }

        scene_info["vr_info"] = vr_info_adict
        self.Json_adict["scene_info"] = scene_info
        # self.Json_adict["vr_info"] = vr_info_adict
        KeyshotUtil.WriteFile(self.Json_adict,self._cfg_task,'json')
        KeyshotUtil.print_times("Analysis & file end.")


    def Extued(self):
        
        self.DataSet()
        # self.configs()
        self.GetAsses()

def KStMmain():

    ## --------------------creat a job----------------------------
    ks_obj = ks_fileBase(args)
    KeyshotUtil.print_times('Load bip file start...')
    try:
        ks_obj.loadbipfile()
    except :
        KeyshotUtil.print_times('Load bip ignore Errors.')
    KeyshotUtil.print_times('Load bip file end.')

    sys.stdout.flush()
    time.sleep(1)

    ## -----------------------------------------------------------

    KeyshotUtil.print_times('Jobs start...')
    KeyshotUtil.print_times('Job type: Analysis job ')
    ks_obj.Extued()
    
    sys.stdout.flush()
    time.sleep(1)
    
    ks_obj.analy_info()
        
    sys.stdout.flush()
    time.sleep(1)

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
    print('-'*60)
    print('-'*60)
    print('Creat Keyshot base information for running this Job, start Keyshot_Files_Function...')
    print('...')    
    print(args)
    KStMmain()
