import os,sys,time
import argparse
import json
import traceback

base_houdini = os.path.dirname(sys.path[0])
sys.path.append("%s/function"%base_houdini)
from HoudiniUtil import HoudiniUtil
from HoudiniPlugin import HoudiniPlugin

parser = argparse.ArgumentParser()
parser.add_argument('-project', type=str, required=True, help='.hip file to render')
parser.add_argument('-rop', type=str, required=True, help='rop node to render')
parser.add_argument('-GPU', type=int, required=True, help='the gpu id which to be used to render')
parser.add_argument('-frame', type=str, required=True, help='frames to render')
parser.add_argument('-outdir', type=str, required=True, help='image with dir to render to')
parser.add_argument('-HIP', type=str, required=True, help='HIP path val')
parser.add_argument('-taskbase', type=str, required=True, help='The render task path ')
parser.add_argument('-plugindir', type=str, required=True, help='The plugin dirt ')
parser.add_argument('-custid', type=str, required=True, help='The user id  ')

args = parser.parse_args()

class hfs_fileBase():
    
    def __init__(self,args=""):
        HoudiniUtil.print_times('Start hfs base...')
        self.render_node_type = ['Redshift_ROP','ifd','arnold']
        self.args = args
        self.frame = ''
        self.basedir = os.path.abspath(self.args.project)
        self.basedir = self.basedir.replace("\\","/")
        self._hip_val = os.path.dirname(self.args.project).replace("\\","/")
        self._reset_val = False
        self.CreatRenderMethod()

    def CreatRenderMethod(self):
        ## 
        HoudiniUtil.print_times('CreatRenderMethod start...')
        self._res = []
        self._quality = 2
        self._ignore_inputs = True
        self._verbose_s = True
        self._method = hou.renderMethod.RopByRop
        # self._method = hou.renderMethod.FrameByFrame
        self._ignore_bypass_flags = True
        self._ignore_lock_flags = False
        self._verbose = False
        self._output_progress = False

        HoudiniUtil.print_times('CreatRenderMethod end.')

    def loadhipfile(self):

        self.hip_file=self.args.project
        if os.path.exists(self.hip_file):
            HoudiniUtil.print_times ("Loading hip file: %s" % self.hip_file)
            try:
                hou.hipFile.load(self.hip_file)
                HoudiniUtil.print_times ("Loading hip file success")
        ## -----------------------------------------------------------
        ## ----------if it is render job , get the rop node ----------

                # update $HIP once file loaded
                _hip_var = os.path.dirname(self.hip_file)
                hou.hscript("setenv HIP=" + str(_hip_var))
                hou.hscript("varchange")
                
            except (IOError ,ZeroDivisionError),e:
                HoudiniUtil.print_times (e)
        else:
            HoudiniUtil.print_times ("ERROR: the hip file is not exist!")
            sys.exit(1)

    def Custmset(self):
        HoudiniUtil.print_times("Custom Setup start...")
        
        _files_name = []
        _config_patn = "%s/custom/Bhand"%self.args.plugindir
        from custom import Bhand
        _function_all = dir(Bhand)
        for (dirpath, dirnames, filenames) in os.walk(_config_patn):
            _files_name.extend(filenames)
        for scr in _files_name:
            _py_list = scr.split(".py")
            if _py_list[1]=='' and _py_list[0] in _function_all:
                cmds = "Bhand.%s.main(self)" % _py_list[0]
                ## print(cmds)
                try:
                    exec cmds
                except Exception as e:
                    HoudiniUtil.print_times(e)
        HoudiniUtil.print_times("Custom Setup end.")

    def DataSet(self):
        HoudiniUtil.print_times("DataSet Setup start...")
        cfg_path = '%s/cfg'%self.args.taskbase.replace("\\","/")
        out_dir = '%s/output'%self.args.taskbase.replace("\\","/")
        self._cfg_task = '%s/task.json'%cfg_path
        cfg_asset = '%s/asset.json'%cfg_path

        self.Json_adict = eval(open(self._cfg_task, 'r').read()) if os.path.exists(self._cfg_task) else {}
        self.Asset_adict = eval(open(cfg_asset, 'r').read()) if os.path.exists(cfg_asset) else {}
        if len(self.Asset_adict) == 0:HoudiniUtil.print_times("Asset_adict is empty.")
        HoudiniUtil.print_times("DataSet Setup end.")

    def File_fix(self):
        """ camera abc file """
        cam_node =  self.ropnode.parm("camera").eval()
        cam_diff_adict = self.Asset_adict["Cam"]["diff"]
        if cam_node in cam_diff_adict:
            HoudiniPlugin.try_fix_abc_cam(self.ropnode,self.Asset_adict)

    def configs(self):
        HoudiniUtil.print_times("Config Setup start...")
        ## All the code in configs folder will run one time 
        _files_name = []
        _config_patn = "%s/configs/Bhand"%self.args.plugindir
        from configs import Bhand
        _function_all = dir(Bhand)
        for (dirpath, dirnames, filenames) in os.walk(_config_patn):
            _files_name.extend(filenames)
        for scr in _files_name:
            _py_list = scr.split(".py")
            if _py_list[1]=='' and _py_list[0] in _function_all:
                cmds = "Bhand.%s.main(self)" % _py_list[0]
                try:
                    exec cmds
                except Exception as e:
                    HoudiniUtil.print_times(e)
        HoudiniUtil.print_times("Config Setup end.")

    def Extued(self):
        
        self.DataSet()
        # self.configs()
        # self.Custmset()
        self.File_fix()

def HfsMmain():

    ## --------------------creat a job----------------------------
    hfs_obj = hfs_fileBase(args)
    HoudiniUtil.print_times('Load hip file start...')
    try:
        hfs_obj.loadhipfile()
    except :
        HoudiniUtil.print_times('Load hip ignore Errors.')
    HoudiniUtil.print_times('Load hip file end.')

    sys.stdout.flush()
    time.sleep(1)

    ## -----------------------------------------------------------

    hfs_obj.ropnode=ropnode=hou.node(args.rop)
    HoudiniUtil.print_times('Jobs start...')

    ## ----------------------loop render ------------------------
    ## --------------------- loop type --------------------------

    if ropnode.type().name() in hfs_obj.render_node_type:
        frame_adict = HoudiniPlugin.FramesAnalyse(args.frame)
        if len(frame_adict.keys()):
            HoudiniUtil.print_times(str(frame_adict))
            try_times = 3
            run_times = 0
            run_result = True
            while run_times<try_times:
                try:
                    if ropnode.type().name()=='Redshift_ROP':
                        HoudiniUtil.print_times('Job type: Redshift Render job ')
                        HoudiniUtil.setoutput_RS(hfs_obj)
                        hfs_obj.Extued()
                        
                        sys.stdout.flush()
                        time.sleep(1)
                    
                        for key in frame_adict.keys():
                            hfs_obj.frame = frame_adict[key]
                            HoudiniPlugin.setframes(hfs_obj)
                            hfs_obj.render_RS()

                    elif ropnode.type().name()=='ifd':
                        HoudiniUtil.print_times('Job type: Mantra Render job ')
                        HoudiniPlugin.SetMantra(hfs_obj)
                        hfs_obj.Extued()
                        
                        sys.stdout.flush()
                        time.sleep(1)
                        
                        for key in frame_adict.keys():
                            hfs_obj.frame = frame_adict[key]
                            HoudiniPlugin.setframes(hfs_obj)
                            HoudiniPlugin.render_Mantra(hfs_obj)

                    elif ropnode.type().name()=='arnold':
                        HoudiniUtil.print_times('Job type: Arnold Render job ')
                        HoudiniPlugin.SetArnold(hfs_obj)
                        hfs_obj.Extued()
                        
                        sys.stdout.flush()
                        time.sleep(1)
                        
                        for key in frame_adict.keys():
                            hfs_obj.frame = frame_adict[key]
                            HoudiniPlugin.setframes(hfs_obj)
                            HoudiniPlugin.render_AR(hfs_obj)
                            
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
                    HoudiniPlugin.TracebackError(list_tx,hfs_obj.Asset_adict,ropnode)

                    if hfs_obj._reset_val:
                        """  reset the node value  """
                        pass
                    else:
                        run_times = try_times
                        
                    run_result = False
                    if run_times<=try_times:
                        print("Render rease errors ",run_times)
                        print("="*80)
            if not run_result:
                sys.exit(8860)
    elif ropnode.type().name()=='rop_geometry':
        HoudiniUtil.print_times('Job type: Simulation job ')
        # HoudiniPlugin.setframes(hfs_obj)
        hfs_obj.Extued()
        
        sys.stdout.flush()
        time.sleep(1)
        
        HoudiniPlugin.RenderSimulate(hfs_obj)
        # hfs_obj.render_sml()
    else:
        HoudiniUtil.print_times('The can\'t find this render: %s '% ropnode.type().name())
        sys.exit(2)

    HoudiniUtil.print_times('Jobs end.')

if __name__=="__main__":

    print('...')
    print('-'*50)
    print('-'*50)
    print('Creat Houdini base information for running this Job, start Houdini_Files_Function...')
    print('...')    

    HfsMmain()
