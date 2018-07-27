import os,sys,time
import re
import subprocess
import shutil
from HoudiniUtil import HoudiniUtil


class HoudiniPlugin(object):
    """docstring for HoudiniPlugin"""
    def __init__(self, arg):
        super(HoudiniPlugin, self).__init__()
        self.arg = arg

    @classmethod
    def BaseDataSetup(cls,cls_in=''):
        cls_in.LogsCreat("BaseDataSetup start...")
        cls_in.LogsCreat("...")
        cls_in._hip_file = cls_in.G_INPUT_CG_FILE.replace("\\","/") if len(cls_in.G_INPUT_CG_FILE) else ''
        cls_in._output = cls_in.G_WORK_RENDER_TASK_OUTPUT.replace("\\","/")
        cls_in._task_folder = cls_in.G_WORK_RENDER_TASK.replace("\\","/")

        if cls_in._plant=='Linux':
            cls_in._houdini_client_dir = '/opt/plugins/houdini'
            cls_in._houdini_PLuing_dirt = '/B/plugins/houdini' if os.path.exists("/B/plugins/houdini") else "%s/plugins/houdini"%cls_in.G_PLUGIN_PATH.replace("\\","/")
            app_path = "%s/apps/Linux"%cls_in._houdini_PLuing_dirt
        else:
            cls_in._houdini_client_dir = 'D:/plugins/houdini'
            cls_in._houdini_PLuing_dirt = 'B:/plugins/houdini' if os.path.exists("B:/plugins/houdini") else "%s/plugins/houdini"%cls_in.G_PLUGIN_PATH.replace("\\","/")
            app_path = "%s/apps/win"%cls_in._houdini_PLuing_dirt

        cls_in._code_base_path = os.path.join(cls_in.G_NODE_PY,"CG/Houdini").replace("\\","/")         
        cls_in.hfs_save_version = ''
        cls_in._hfs_version = ''
        cls_in._hip_save_val = ''
        cls_in.hip_val = os.path.dirname(cls_in._hip_file)
        cls_in._plugins = cls_in.G_CG_CONFIG_DICT["plugins"]
        ## change to standers
        plugin_temp = {}
        if "HtoA" in cls_in._plugins:
            plugin_temp["Arnold"] = cls_in._plugins["HtoA"].split(" ")[-1] if " " in cls_in._plugins["HtoA"] else cls_in._plugins["HtoA"]
        if "RS_GPU" in cls_in._plugins:
            plugin_temp["Redshift"] = cls_in._plugins["RS_GPU"].split(" ")[-1] if " " in cls_in._plugins["RS_GPU"] else cls_in._plugins["RS_GPU"]
        if len(plugin_temp):cls_in._plugins = plugin_temp

        cls_in.user_id = cls_in.G_USER_ID

        if cls_in.G_ACTION == 'Render' or cls_in.G_ACTION == 'GopRender':
            cls_in._frames = [cls_in.G_CG_START_FRAME,cls_in.G_CG_END_FRAME,cls_in.G_CG_BY_FRAME]
            cls_in._rop_node = cls_in.G_RENDER_OPTIONS['render_rop'] if 'render_rop' in cls_in.G_RENDER_OPTIONS.keys() else ''
            if cls_in._rop_node == '': ## call errors
                cls_in._run_code_result = False
                cls_in._erorr_code = 'RenderHoudini.BaseDataSetup.rop call'
                cls_in._erorr_code_info = 'The rop is not set!.'

        # get imformation from the .hip file
        # version && $HIP
        if os.path.exists(cls_in._hip_file):

            hip_file_info = HoudiniUtil.GetSaveHipInfo(cls_in._hip_file,app_path)
            if len(hip_file_info)==3:
                cls_in.hfs_save_version = hip_file_info[0]
                cls_in._hfs_version = hip_file_info[1]
                cls_in._hip_save_val = hip_file_info[2]
            else:
                cls_in._run_code_result = False
                cls_in._erorr_code = 'HoudiniUtil.GetSaveHipInfo'
                cls_in._erorr_code_info = hip_file_info[0]
        else:
            cls_in._run_code_result = False
            cls_in._erorr_code = 'HoudiniPlugin.BaseDataSetup'
            cls_in._erorr_code_info = 'The .hip file is not exist. File: %s'%cls_in._hip_file

        cls_in.LogsCreat("BaseDataSetup end.")
        cls_in.LogsCreat("")

    @classmethod
    def FramesAnalyse(cls,frames=''):
        all_frames = frames
        types = 0
        renderjobs = {}
        ## 5 5 1  /  1-10[1]  /  1,3,6  /  1,2-5,9   /  3,2-10[3],5
        k = 0
        if "," in all_frames:
            frames_list = all_frames.split(",")
            types = 2
            for i in range(len(frames_list)):
                if "-" in frames_list[i]:
                    if "[" in frames_list[i]: ## 2-10[3]
                        frame_sp = frames_list[i].split("]")[0].split("[")
                        frame_ah = frame_sp[0].split("-")
                        k,renderjobs = cls.createframeadict(k,[frame_ah[0],frame_ah[-1],frame_sp[-1]],renderjobs)
                        
                    else: ## 2-5
                        frame_ah = frames_list[i].split("-")
                        k,renderjobs = cls.createframeadict(k,[i,i,str(1)],renderjobs)
                        
                else:  ## 1
                    k,renderjobs = cls.createframeadict(k,[frames_list[i],frames_list[i],str(1)],renderjobs)
                    
        elif "-" in all_frames and not "," in all_frames: ## 1-10[1]  /  2-5
            types = 1
            if "[" in all_frames: ## 1-10[3]
                frame_sp = all_frames.split("]")[0].split("[")
                frame_ah = frame_sp[0].split("-")
                k,renderjobs = cls.createframeadict(k,[frame_ah[0],frame_ah[-1],frame_sp[-1]],renderjobs)
            else: ## 2-5
                frame_ah = frames_list[i].split("-")
                k,renderjobs = cls.createframeadict(k,[frame_ah[0],frame_ah[-1],str(1)],renderjobs)
                
        else:
            frames_arr_s=all_frames.split(" ")
            k,renderjobs = cls.createframeadict(k,[frames_arr_s[0],frames_arr_s[1],frames_arr_s[2]],renderjobs)

        return renderjobs,types

    @staticmethod
    def createframeadict(idest,list,adict):
        _goon = True
        indest = 0
        adition = 0
        while _goon:
            first_f = int(list[0])
            end_f = int(list[1])
            pas_f = int(list[2])
            if indest == 0:
                adition = first_f
                indest += 1
            else:
                adition += int(pas_f)
            if adition <= end_f:
                adict[idest] = [str(adition),str(adition),"1"]
                idest += 1
            else:
                _goon = False
            
        return idest,adict


    @classmethod
    def setframes(cls,cls_in=''):
        HoudiniUtil.print_times("setframes start...")
        SF = float(cls_in.ropnode.evalParm('f1'))
        EF = float(cls_in.ropnode.evalParm('f2'))
        BF = float(cls_in.ropnode.evalParm('f3'))
        HoudiniUtil.print_times("FRAME RANGE IN THIS FILE's SET: "+str(SF)+"-"+str(EF)+"["+str(BF)+"]")

        if cls_in.ropnode.evalParm("trange")!=1:
            cls_in.ropnode.parm("trange").set(1)

        if cls_in.ropnode.parm('f1').isLocked():
            cls_in.ropnode.parm('f1').lock(False)
        if cls_in.ropnode.parm('f2').isLocked():
            cls_in.ropnode.parm('f2').lock(False)
        if cls_in.ropnode.parm('f3').isLocked():
            cls_in.ropnode.parm('f3').lock(False)
        cls_in.ropnode.parm('f1').deleteAllKeyframes()
        cls_in.ropnode.parm('f2').deleteAllKeyframes()
        cls_in.ropnode.parm('f3').deleteAllKeyframes()

        frames_arr=cls_in.frame
        HoudiniUtil.print_times (frames_arr)
        Fr1=float(frames_arr[0].strip())
        Fr2=float(frames_arr[1].strip())
        Fr3=float(frames_arr[2].strip())
        cls_in.ropnode.parm("f1").set(Fr1)
        cls_in.ropnode.parm("f2").set(Fr2)
        cls_in.ropnode.parm("f3").set(Fr3)

        SF = float(cls_in.ropnode.evalParm('f1'))
        EF = float(cls_in.ropnode.evalParm('f2'))
        BF = float(cls_in.ropnode.evalParm('f3'))
        HoudiniUtil.print_times("NEW FRAME RANGE TO RENDER: "+str(SF)+"-"+str(EF)+"["+str(BF)+"]")
        HoudiniUtil.print_times("setframes end.")

    @classmethod
    def CreateOutput(cls,valparm="",cls_in=''):

        HoudiniUtil.print_times("ROP output parm: %s" % valparm)
        
        outfile_hip_str = cls.node_deep_val(cls_in.ropnode,valparm)[0]
        outfile_hip = cls_in.ropnode.parm(valparm).eval()

        get_out_val = True 
        HoudiniUtil.print_times("Output values: %s" % outfile_hip)
        if outfile_hip=='(not set)' or outfile_hip=='':
            cls_in.outputFiles=os.path.join(cls_in.args.HIP,'out/default.$F4.exr')
            get_out_val = False
        if get_out_val:
            HIP_val_old = cls_in.args.HIP.replace("\\","/")if "\\" in cls_in.args.HIP else cls_in.args.HIP

            if HIP_val_old.endswith('/'): HIP_val_old = HIP_val_old[:-1]
            outfile_hip_dir = os.path.dirname(outfile_hip.replace("\\","/"))  ### $HIP/aa/aa/aa.$F4.exr D:/
            if "//" in outfile_hip_dir:outfile_hip_dir = outfile_hip_dir.replace("//","/")

            if HIP_val_old in outfile_hip_dir:
                outfile_arr_main = outfile_hip_dir.split(HIP_val_old+"/")[-1]   ### aa/aa

            elif cls_in._hip_val in outfile_hip_dir:
                if cls_in._hip_val.endswith('/'): cls_in._hip_val = cls_in._hip_val[:-1]
                outfile_arr_main = outfile_hip_dir.split(cls_in._hip_val+"/")[-1]   ### aa/aa

            elif ":/" in outfile_hip_dir:    ### D:/aa
                outfile_arr_mains=outfile_hip_dir.split("/")   ### aa/aa
                outfile_arr_main = (outfile_arr_mains[-2]+"/"+outfile_arr_mains[-1]) if len(outfile_arr_mains)>2 else outfile_arr_mains[-1]
            
            else:
                outfile_arr_main = outfile_hip_dir
            
            outname = os.path.basename(outfile_hip_str)
            
            # $HIP/aaa/aass
            out_dir=os.path.join(cls_in.args.outdir,outfile_arr_main)
            out_dir=out_dir.replace("\\","/")

            if not os.path.exists(out_dir):
                os.makedirs(out_dir)
            outputFiles=os.path.join(out_dir,outname)
            cls_in.outputFiles=outputFiles.replace("\\","/")
            
        HoudiniUtil.print_times("OutputFiles changed to: %s" % cls_in.outputFiles)
        

    @classmethod
    def SetMantra(cls,cls_in=''):
        HoudiniUtil.print_times("Output_Mantra set start...")
        
        ropTypeName = cls_in.ropnode.type().name()
        HoudiniUtil.print_times("ROP output type %s" % ropTypeName)
        if ropTypeName in ['ifd']:
            cls.CreateOutput("vm_picture",cls_in)
            cls_in.ropnode.parm("vm_picture").set(cls_in.outputFiles)
            HoudiniUtil.print_times("Output check:")
            HoudiniUtil.print_times(cls_in.ropnode.evalParm("vm_picture"))
            
            ### set aov pass
            out_aovs = cls_in.ropnode.parm("vm_numaux").eval()
            if out_aovs > 0:
                HoudiniUtil.print_times("Output_Mantra aov set start...")
                aovs_list = []
                for i in range(out_aovs):
                    parm_k = "vm_disable_plane%d"%(i+1)
                    if not cls_in.ropnode.parm(parm_k).eval():
                        parm_f_use = "vm_usefile_plane%d"%(i+1)
                        if cls_in.ropnode.parm(parm_f_use).eval():
                            parm_f_val = "vm_filename_plane%d"%(i+1)
                            aovs_list.append(parm_f_val)
                if len(aovs_list) > 0:
                    for elm in aovs_list:
                        _outputFiles = cls.CreateOutput(elm,cls_in)
                        cls_in.ropnode.parm(elm).set(_outputFiles)
            ### set deep images
            deep_flag = cls_in.ropnode.parm('vm_deepresolver').unexpandedString()
            if deep_flag in ['camera', 'shadow']:
                vm_deep_pmn = 'vm_dcmfilename'
                if deep_flag == 'shadow':
                    vm_deep_pmn = 'vm_dsmfilename'
                outputDeepFile = cls.CreateOutput(vm_deep_pmn,cls_in)
                try:
                    if cls_in.ropnode.parm(vm_deep_pmn).isLocked():
                        cls_in.ropnode.parm(vm_deep_pmn).lock(False)
                    cls_in.ropnode.parm(vm_deep_pmn).deleteAllKeyframes()
                    cls_in.ropnode.parm(vm_deep_pmn).set(outputDeepFile)
                except:
                    HoudiniUtil.print_times('Failed to delete %s keyframes.' % vm_deep_pmn)
                deep_output_ffn = self.ropnode.parm(vm_deep_pmn).unexpandedString()
                HoudiniUtil.print_times("Final deep output: %s" % deep_output_ffn)

        HoudiniUtil.print_times("Output_Mantra set end.")

    @classmethod
    def render_Mantra(cls,cls_in=''):

        HoudiniUtil.print_times("Render_Mantra start...")
        #root_take = hou.takes.rootTake()
        #curt_take = hou.takes.currentTake()
        _ifd = cls_in.ropnode.parm("soho_outputmode").eval()
        if _ifd:
            cls_in.ropnode.parm("soho_outputmode").set(0)

        # set the Log level to 5 
        _level = cls_in.ropnode.parm("vm_verbose").eval()
        if int(_level) != 5:
            _level = cls_in.ropnode.parm("vm_verbose").set(4)

        cls_in.ropnode.render(verbose=cls_in._verbose_s,quality=cls_in._quality, ignore_inputs=cls_in._ignore_inputs, method=cls_in._method, ignore_bypass_flags=cls_in._ignore_bypass_flags, ignore_lock_flags=False, output_progress=False)
        HoudiniUtil.print_times("Render_Mantra end.")

    @classmethod
    def SetRedshift(cls,cls_in=''):
        HoudiniUtil.print_times("Output_RS set start...")
        
        if cls_in.args.GPU==0:
            hou.hscript("Redshift_setGPU -s 10")
            HoudiniUtil.print_times('Set GPU %d avilable' % cls_in.args.GPU)
        elif cls_in.args.GPU==1:
            #hou.hscript("Redshift_setGPU -s 01")
            HoudiniUtil.print_times('Set GPU avilable' )
            #HoudiniUtil.print_times('Set GPU %d avilable' % cls_in.args.GPU)
        else:
            HoudiniUtil.print_times ("ERROR WITH GPU ID: %d [0 TO 1 FOR RIGHT NOW(17/3/2017)]" % cls_in.args.GPU)
            sys.exit(1)

        ropTypeName = cls_in.ropnode.type().name()
        HoudiniUtil.print_times("ROP output type %s" % ropTypeName)
        if ropTypeName in ['Redshift_ROP']:
            cls.CreateOutput("vm_picture",cls_in)
            if not cls_in.ropnode.evalParm("RS_outputEnable"):
                cls_in.ropnode.parm("RS_outputEnable").set(True)
            cls_in.ropnode.parm("RS_outputFileNamePrefix").set(outputFiles)
            HoudiniUtil.print_times("Output check:")
            HoudiniUtil.print_times(cls_in.ropnode.evalParm("RS_outputFileNamePrefix"))
        
        HoudiniUtil.print_times("Output_RS set end.")

    @classmethod
    def render_RS(cls,cls_in=''):
        HoudiniUtil.print_times("Render_RS start...")
        root_take = hou.takes.rootTake()
        curt_take = hou.takes.currentTake()
        n_parm = cls_in.ropnode.parmTuple("RS_renderToMPlay") if cls_in.ropnode.type().name()=="Redshift_ROP" else ""
        if not n_parm == "":
            if curt_take != root_take:
                if not curt_take.hasParmTuple(n_parm):
                    curt_take.addParmTuple(n_parm)
                    #curt_take.removeParmTuple(n_parm
            if cls_in.ropnode.parm("RS_renderToMPlay").eval()==1:
                cls_in.ropnode.parm("RS_renderToMPlay").set(0)

        cls_in.ropnode.render(verbose=cls_in._verbose_s,quality=cls_in._quality, ignore_inputs=cls_in._ignore_inputs, method=cls_in._method, ignore_bypass_flags=cls_in._ignore_bypass_flags, ignore_lock_flags=False, output_progress=False)
        HoudiniUtil.print_times("Render_RS end.")

    @classmethod
    def SetArnold(cls,cls_in=''):
        HoudiniUtil.print_times("Output_AR set start...")

        ropTypeName = cls_in.ropnode.type().name()
        HoudiniUtil.print_times("ROP output type %s" % ropTypeName)
        if ropTypeName in ['arnold']:
            cls.CreateOutput("vm_picture",cls_in)
            cls_in.ropnode.parm("ar_picture").set(outputFiles)
            HoudiniUtil.print_times("Output check:")
            HoudiniUtil.print_times(cls_in.ropnode.evalParm("ar_picture"))
            
            ### set aov pass
            out_aovs = cls_in.ropnode.parm("ar_aovs").eval()
            if out_aovs > 0:
                HoudiniUtil.print_times("Output_Arnold aov set start...")
                aovs_list = []
                for i in range(out_aovs):
                    parm_k = "ar_enable_aov%d"%(i+1)
                    if cls_in.ropnode.parm(parm_k).eval():
                        parm_f_use = "ar_aov_separate%d"%(i+1)
                        if cls_in.ropnode.parm(parm_f_use).eval():
                            parm_f_val = "ar_aov_separate_file%d"%(i+1)
                            aovs_list.append(parm_f_val)
                if len(aovs_list) > 0:
                    for elm in aovs_list:
                        _outputFiles = cls_in.CreateOutput(elm)
                        cls_in.ropnode.parm(elm).set(_outputFiles)
        
        HoudiniUtil.print_times("Output_AR set end.")

    @classmethod
    def render_AR(cls,cls_in=''):

        HoudiniUtil.print_times("Render_AR start...")
        # root_take = hou.takes.rootTake()
        # curt_take = hou.takes.currentTake()
        cls_in.ropnode.render(verbose=cls_in._verbose_s,quality=cls_in._quality, ignore_inputs=cls_in._ignore_inputs, method=cls_in._method, ignore_bypass_flags=cls_in._ignore_bypass_flags, ignore_lock_flags=False, output_progress=False)
        HoudiniUtil.print_times("Render_AR end.")

    @classmethod
    def RenderSimulate(cls,cls_in=''):
        HoudiniUtil.print_times("Render_sml start...")
        sml_out = cls_in.ropnode.parm("sopoutput").eval()
        HoudiniUtil.print_times("Simulation output: %s" % sml_out)

        cls_in.ropnode.render(verbose=cls_in._verbose_s,quality=cls_in._quality, ignore_inputs=cls_in._ignore_inputs, method=cls_in._method, ignore_bypass_flags=cls_in._ignore_bypass_flags, ignore_lock_flags=False, output_progress=False)
        # print("echo Simulation done>%s/Simulation.txt"%cls_in.args.outdir)
        simulation_pic = "%s/simulation_pic/simulation.jpg"%cls_in.args.plugindir
        os.system("copy /y %s %s"%(os.path.abspath(simulation_pic),os.path.abspath(cls_in.args.outdir)))
        HoudiniUtil.print_times("Render_sml end.")

    @classmethod
    def DataInfo(cls,cls_in=''):
        # --------------------------------------------------------------------------------
        #                           JOB INFORMATION PRINT
        # --------------------------------------------------------------------------------
        cls_in.LogsCreat(" ")
        cls_in.LogsCreat("JOB INFORMATION")
        cls_in.LogsCreat("Function: %s"% (cls_in.G_ACTION if not cls_in.G_ACTION=='' else 'Analyze'))
        cls_in.LogsCreat("File saved with Houdini %s"%cls_in.hfs_save_version)
        cls_in.LogsCreat("File saved with $HIP val %s"%cls_in._hip_save_val)
        cls_in.LogsCreat("...")
        cls_in.LogsCreat("Final Houdini version to run this Job : %s"%cls_in._hfs_version)
        cls_in.LogsCreat("Hip file: %s"%cls_in._hip_file)
        cls_in.LogsCreat("Final $HIP val to run this Job : %s"%cls_in.hip_val)
        cls_in.LogsCreat('...')
        cls_in.LogsCreat("Plugins Info: %s"%(cls_in._plugins if len(cls_in._plugins) else "None"))
        # --------------------------------------------------------------------------------
        # ----------------------------RENDER LOG INFORMATION PRINT------------------------

        cls_in.LogsCreat("Log start...\n"+"-"*150+"\n"+"/"*150+"\n"+"-"*150+"\n",True,False)
        houdini_verser_full = cls_in._hfs_version[:2]+"."+cls_in._hfs_version[2:3]+"."+cls_in._hfs_version[3:]
        cls_in.LogsCreat("Software: Houdini %s\n\n"%houdini_verser_full,True,False)
        if cls_in.G_ACTION == 'Render':
            cls_in.LogsCreat("Frames: %s"%cls_in._frames)
            cls_in.LogsCreat("Frames Types: %s"% ("Normal" if cls_in._render_frame==1 else "MutilFrames"))
            cls_in.LogsCreat("Rop: %s"%cls_in._rop_node)


    @classmethod
    def TipsInfo(cls,cls_in=''):

        ''' tips '''
        HoudiniUtil.print_times("tlspace")
        HoudiniUtil.print_times("="*25 + " Tips Info " + "="*25)

        error_key_adict = cls_in.Error_ids if len(cls_in.Error_ids) else {}
        if "Miss" in cls_in.asset_adict:
            keyword_war = error_key_adict["filemiss"] if "filemiss" in error_key_adict else '50001'   ### just for warnning
            infos_list = []
            # print(cls_in.asset_adict["Miss"])
            if len(cls_in.asset_adict["Miss"]):
                for keys in cls_in.asset_adict["Miss"]:
                    asset_type_adict = cls_in.asset_adict["Miss"][keys]
                    if len(asset_type_adict):
                        for nodes in asset_type_adict:
                            HoudiniUtil.print_times("Nodes: %s"%nodes)
                            HoudiniUtil.print_times("Files: %s"%asset_type_adict[nodes][0])
                            info_temp = "Nodes: %s  miss file: %s "%(nodes,asset_type_adict[nodes][0])
                            if len(asset_type_adict[nodes])>1:
                                if type(asset_type_adict[nodes][1]) == list:
                                    frames_miss = ''
                                    cunt = 0
                                    for elm in asset_type_adict[nodes][1]:
                                        if cunt==0:
                                            frames_miss = str(elm)
                                            cunt +=1
                                        else:
                                            frames_miss += ', '+str(elm)
                                    HoudiniUtil.print_times("Miss frame: %s"%frames_miss)
                                    info_temp += "frame: %s"%frames_miss
                            infos_list.append(info_temp)
                            HoudiniUtil.print_times("-"*60)
            if len(infos_list):
                cls_in.tips_adict[keyword_war] = infos_list

        if "Cam" in cls_in.asset_adict:
            HoudiniUtil.print_times("-"*23 + " Cameras Info " + "-"*23)
            keyword_err = error_key_adict["cmamiss"] if "cmamiss " in error_key_adict else '50002'   ### just for error
            keyword_war = error_key_adict["cmawarning"] if "cmawarning" in error_key_adict else '50003'
            infos_list_err = []
            infos_list_war = []
            if "diff" in cls_in.asset_adict["Cam"]:
                HoudiniUtil.print_times(">> With diffrence values, this error will be try to fix in render process")
                for keys in cls_in.asset_adict["Cam"]["diff"]:
                    asset_cam_adict_temp = cls_in.asset_adict["Cam"]["diff"][keys]
                    asset_cam_adict = asset_cam_adict_temp[0]
                    if len(asset_cam_adict):
                        node_cunt = 1
                        for nodes in asset_cam_adict:
                            if len(asset_cam_adict[nodes])>1:
                                if node_cunt==1:
                                    HoudiniUtil.print_times("Base Nodes: %s  file: %s "%(nodes,asset_cam_adict[nodes][0]))
                                    info_temp = ("Nodes with diffrence file val: %s "%nodes)
                                    node_cunt +=1
                                else:
                                    if len(asset_cam_adict[nodes])==3:
                                        if asset_cam_adict[nodes][1] == 0:
                                            HoudiniUtil.print_times("Nodes with diffrence file val: %s "%nodes)
                                            HoudiniUtil.print_times("File: %s "%asset_cam_adict[nodes][0])
                            else:
                                HoudiniUtil.print_times("Errors...(camera checks) ")
                                HoudiniUtil.print_times("tlspace")
                        infos_list_war.append(info_temp)
                        HoudiniUtil.print_times("-"*60)
                HoudiniUtil.print_times("-"*60)
                if len(infos_list_war):
                    cls_in.tips_adict[keyword_war] = infos_list_war

            if "miss" in cls_in.asset_adict["Cam"]:
                HoudiniUtil.print_times(">> Camera did not exist(the cam path which in the rop node is not exist).")
                for keys in cls_in.asset_adict["Cam"]["miss"]:
                    ## keys eg. '/obj/camera/camera1/cameraShape1'
                    asset_cam_list = cls_in.asset_adict["Cam"]["miss"][keys]
                    ## eg.  {'/obj/cam1': [['None'], '/out/mantra2']}
                    if len(asset_cam_list):
                        if "list" in str(type(asset_cam_list)):
                            asset_cam_list = asset_cam_list[0]
                        for nodes in asset_cam_list:
                            node_temp = asset_cam_list[nodes]
                            if len(node_temp)>1:
                                HoudiniUtil.print_times("Nodes: %s  Miss: %s"%(nodes,node_temp[0]))
                                info_temp = ("Nodes: %s  Miss: %s"%(nodes,node_temp[0]))
                            else:
                                HoudiniUtil.print_times("Nodes: %s  Miss "%nodes)
                                info_temp = ("Nodes: %s  Miss "%nodes)
                        infos_list_err.append(info_temp)
            if "normal" in cls_in.asset_adict["Cam"]:
                if len(cls_in.asset_adict["Cam"]["normal"]):
                    if len(infos_list_err):
                        if len(infos_list_war):
                            cls_in.tips_adict[keyword_war].extend(infos_list_err)
                        else:
                            cls_in.tips_adict[keyword_war] = infos_list_err
                else:
                    if len(infos_list_err):
                        cls_in.tips_adict[keyword_err] = infos_list_err
            else:
                if len(infos_list_war):
                    cls_in.tips_adict[keyword_err] = infos_list_war
                    if len(infos_list_err):
                            cls_in.tips_adict[keyword_err].extend(infos_list_err)
                elif len(infos_list_err):
                        cls_in.tips_adict[keyword_err] = infos_list_err

        HoudiniUtil.print_times("="*60)
        HoudiniUtil.print_times("tlspace")
        HoudiniUtil.print_times("-"*60)
        HoudiniUtil.print_times("Folder adict:")
        HoudiniUtil.print_times(cls_in.foler_adict)
        HoudiniUtil.print_times("-"*60)
        HoudiniUtil.print_times ("Asset adict:")
        HoudiniUtil.print_times(cls_in.asset_adict)
        HoudiniUtil.print_times("-"*60)
        HoudiniUtil.print_times("Check history: %s"%str(cls_in.check_history))
        HoudiniUtil.print_times("-"*60)
        HoudiniUtil.print_times("Tips: %s"%str(cls_in.tips_adict))
        HoudiniUtil.print_times("-"*60)
        HoudiniUtil.print_times("tlspace")


    @classmethod
    def CameraCkeck(cls,cls_in=''):
        HoudiniUtil.print_times("CameraCheck...")
        import hou
        AllNode = hou.node("/").allSubChildren()
        if len(AllNode)>0:
            for elm in AllNode:
                if elm.type().name() in cls_in.render_node_type:
                    rop_path = elm.path()
                    cam_node = elm.parm("camera").eval()
                    if hou.node(cam_node):
                        returns=cls.abc_find(cam_node)
                        if returns[0]=='normal':
                            HoudiniUtil.asset_adict_edit(cls_in.asset_adict,"Cam","normal",cam_node,[returns[1],rop_path])
                        elif returns[0]=='diff':
                            HoudiniUtil.asset_adict_edit(cls_in.asset_adict,"Cam","diff",cam_node,[returns[1],rop_path])
                        elif returns[0]=='miss':
                            HoudiniUtil.asset_adict_edit(cls_in.asset_adict,"Cam","miss",cam_node,[returns[1],rop_path])
                    else:
                        ''' miss '''
                        HoudiniUtil.asset_adict_edit(cls_in.asset_adict,"Cam","miss",cam_node,{cam_node:[rop_path]})
                    if not cam_node in cls_in.check_history:cls_in.check_history[cam_node] = [cam_node]


    @staticmethod
    def abc_find(path=""):
        import hou
        result = True
        return_key = 'normal'
        temp_adict = {}
        if path != "":
            cam_pl = path.split("/")
            if len(cam_pl)>0:
                node_pre = ""
                i=0
                n_types = ["alembicarchive","alembicxform","cam"]
                pathval = {}
                index = 1
                type_abc = False
                first_key = ""          
                for elm in cam_pl:
                    if not elm=="":
                        node_pre += "/"+elm             
                        if hou.node(node_pre).type().name() in n_types:
                            if index==1:
                                if hou.node(node_pre).type().name()=="alembicarchive":
                                    type_abc = True
                                    first_key = node_pre
                            if type_abc==True:                          
                                p_val = hou.node(node_pre).parm("fileName").eval()
                                pathval[node_pre] = p_val                          
                            index+=1
                if len(pathval)>2:
                    vals = pathval[first_key]
                    abc_base = False if not os.path.exists(vals) else True
                    same_p = True
                    keys = None
                    temp_adict = {}
                    return_key = 'normal'
                    for elm in pathval:
                        diff_path = []
                        if not pathval[elm] == vals:
                            if not os.path.exists(pathval[elm]):
                                same_p = False
                                diff_path.append(pathval[elm])
                                diff_path.append(0)
                                diff_path.append("notexist")
                            else:
                                same_p = False
                                diff_path.append(pathval[elm])
                                diff_path.append(0)
                                diff_path.append("exist")
                            temp_adict[elm] = diff_path

                        else:
                            if not os.path.exists(pathval[elm]):
                                diff_path.append(pathval[elm])
                                diff_path.append(1)
                                diff_path.append("notexist")
                            else:
                                diff_path.append(pathval[elm])
                                diff_path.append(1)
                                diff_path.append("exist")
                            temp_adict[elm] = diff_path
                    if abc_base:
                        if same_p:
                            return_key = 'normal'
                        else:
                            return_key = 'diff'
                    else:
                        return_key = 'miss'

        return return_key,temp_adict

    @classmethod
    def FilesCheck(cls,cls_in=''):
        from HoudiniThread import HoudiniThread
        ## All_node_adict={"file":{ },"abcs":{ },"tex":{ }}
        All_node_adict = cls.node_adict_fite()
        function_all = {"file":[cls.file_check,[cls_in,All_node_adict]],"abc":[cls.abc_ckeck,[cls_in,All_node_adict]],
        "tex":[cls.texture_ckeck,[cls_in,All_node_adict]]}
        HoudiniThread.JoinThread(HoudiniThread.StartThread(HoudiniThread.CreatThread(function_all)))

        

    @classmethod
    def file_check(cls,cls_in='',adict_in=''):
        # HoudiniUtil.print_times("FileCheck...")
        import hou
        file_adict = adict_in["file"]
        final_adict = {}
        filte_type = ['filemerge','filecache','cam','ropnet','dopio','output','particlefluidobject']
        for elm in file_adict:
            if cls.node_type_filte(file_adict[elm],filte_type):
                final_adict[elm] = file_adict[elm]
        if len(final_adict):
            print ("All import files: %d"%len(final_adict))
            for nodes in final_adict:
                if not nodes.path() in cls_in.check_history:
                    upnode = os.path.dirname(final_adict[nodes])
                    if hou.node(upnode).type().name()=="cop2net":
                        files_path=nodes.evalParm("filename2")
                        with_out_dot_list = cls.change_dot_val(files_path)
                        old_node_val = cls.node_deep_val(nodes,"filename2")
                    else:
                        files_path=nodes.evalParm("file")
                        with_out_dot_list = cls.change_dot_val(files_path)
                        old_node_val = cls.node_deep_val(nodes,"file")
                    # print(with_out_dot_list)
                    
                    """  old values in this parm  """
                    split_str = HoudiniUtil.getnumber(with_out_dot_list[1])[1] if HoudiniUtil.getnumber(with_out_dot_list[1])[0]else "TLAMPFOREVER"
                    file_name = with_out_dot_list[1].split(split_str)[0]
                    file_folder_temp = os.path.join(with_out_dot_list[0],os.path.basename(old_node_val[0]))
                    if not old_node_val[1] in cls_in.check_history:
                        cls_in.check_history[old_node_val[1]] = [file_folder_temp,file_name]

                        ## dir/name /new_path
                        HoudiniUtil.SequenceCheck(cls_in,with_out_dot_list[0],with_out_dot_list[1],nodes.path())
                    cls_in.check_history[nodes.path()] = [file_folder_temp,file_name]


    @classmethod
    def abc_ckeck(cls,cls_in='',adict_in=''):
        # HoudiniUtil.print_times("AbcCheck...")
        # return
        abc_adict = adict_in["abc"]
        abc_inp_adict = adict_in["abc_ipt"]
        final_adict = {}
        filte_type = ['ropnet']
        for elm in abc_adict:
            if cls.node_type_filte(abc_adict[elm],filte_type):
                final_adict[elm] = abc_adict[elm]
        final_adict=dict(final_adict.items()+abc_inp_adict.items())
        if len(final_adict): 
            print ("All import alembic: %d"%len(final_adict))
            for nodes in final_adict:
                if not nodes.path() in cls_in.check_history:
                    files_path=nodes.evalParm("fileName")
                    with_out_dot_list = cls.change_dot_val(files_path)
                    old_node_val = cls.node_deep_val(nodes,"fileName")
                    
                    """  old values in this parm  """
                    split_str = HoudiniUtil.getnumber(with_out_dot_list[1])[1] if HoudiniUtil.getnumber(with_out_dot_list[1])[0] else "TLAMPFOREVER"
                    file_name = with_out_dot_list[1].split(split_str)[0]
                    file_folder_temp = os.path.join(with_out_dot_list[0],os.path.basename(old_node_val[0]))
                    if not old_node_val[1] in cls_in.check_history:
                        cls_in.check_history[old_node_val[1]] = [file_folder_temp,file_name]

                        ## dir/name /new_path
                        HoudiniUtil.SequenceCheck(cls_in,with_out_dot_list[0],with_out_dot_list[1],nodes.path(),"ABCs")
                    cls_in.check_history[nodes.path()] = [file_folder_temp,file_name]


    @classmethod
    def texture_ckeck(cls,cls_in='',adict_in=''):
        # HoudiniUtil.print_times("TexturCheck...")
        import hou
        tex_adict = adict_in["tex"]
        rs_tex_adict = adict_in["rs_tex"]
        final_adict = {}
        filte_type = ['']
        for elm in tex_adict:
            if cls.node_type_filte(tex_adict[elm],filte_type):
                final_adict[elm] = tex_adict[elm]
        if len(final_adict): 
            print ("All tex file: %d"%len(final_adict))
            for nodes in final_adict:
                if not nodes.path() in cls_in.check_history:
                    files_path=nodes.evalParm("map")
                    with_out_dot_list = cls.change_dot_val(files_path)
                    old_node_val = cls.node_deep_val(nodes,"map")
                    # print(with_out_dot_list)
                    
                    """  old values in this parm  """
                    split_str = HoudiniUtil.getnumber(with_out_dot_list[1])[1] if HoudiniUtil.getnumber(with_out_dot_list[1])[0] else "TLAMPFOREVER"
                    file_name = with_out_dot_list[1].split(split_str)[0]
                    if not old_node_val[1] in cls_in.check_history:
                        cls_in.check_history[old_node_val[1]] = [old_node_val[0],file_name]
                        ## dir/name /new_path
                        HoudiniUtil.SequenceCheck(cls_in,with_out_dot_list[0],with_out_dot_list[1],nodes.path(),"ABCs")
                    cls_in.check_history[nodes.path()] = [old_node_val[0],file_name]

        filte_type = ['']
        for elm in rs_tex_adict:
            if cls.node_type_filte(rs_tex_adict[elm],filte_type):
                final_adict[elm] = rs_tex_adict[elm]
        if len(final_adict): 
            print ("All tex file: %d"%len(final_adict))
            for nodes in final_adict:
                if not nodes.path() in cls_in.check_history:
                    files_path=nodes.evalParm("tex0")
                    with_out_dot_list = cls.change_dot_val(files_path)
                    old_node_val = cls.node_deep_val(nodes,"tex0")
                    # print(with_out_dot_list)

                    """  old values in this parm  """
                    split_str = HoudiniUtil.getnumber(with_out_dot_list[1])[1] if HoudiniUtil.getnumber(with_out_dot_list[1])[0] else "TLAMPFOREVER"
                    file_name = with_out_dot_list[1].split(split_str)[0]
                    file_folder_temp = os.path.join(with_out_dot_list[0],os.path.basename(old_node_val[0]))
                    if not old_node_val[1] in cls_in.check_history:
                        cls_in.check_history[old_node_val[1]] = [file_folder_temp,file_name]
                        ## dir/name /new_path
                        HoudiniUtil.SequenceCheck(cls_in,with_out_dot_list[0],with_out_dot_list[1],nodes.path(),"ABCs")
                    cls_in.check_history[nodes.path()] = [file_folder_temp,file_name]



    @staticmethod
    def node_adict_fite():
        import hou
        type_name = ["file","alembic","alembicarchive","textur::2.0","redshift::TextureSampler"]
        file_adict={}
        abc_adict={}
        abc_ipt_adict={}
        tex_adict={}
        rs_tex_adict={}
        for nodes in hou.node("/").allSubChildren():
            nodePath = nodes.path()
            nodePath = nodePath.replace('\\','/')
            nodename=nodes.type().name()
            if nodename in type_name:
                if nodename=="file":
                    file_adict[nodes]=nodePath
                elif nodename=="alembic":
                    abc_adict[nodes]=nodePath
                elif nodename=="alembicarchive":
                    abc_ipt_adict[nodes]=nodePath
                elif nodename=="textur::2.0":
                    tex_adict[nodes]=nodePath
                elif nodename=="redshift::TextureSampler":
                    rs_tex_adict[nodes]=nodePath
        returns = {"file":file_adict,"abc":abc_adict,"abc_ipt":abc_ipt_adict,
                    "tex":tex_adict,"rs_tex":rs_tex_adict}
        return returns

    @staticmethod
    def change_dot_val(pathin =''):
        path_arr=pathin.split("/")
        arr_elm=[]
        returnpath=''
        file_exit=True
        get_info = ''
        for i in range(0,len(path_arr)):
            if path_arr[i]=="..":
                arr_elm.append(i)
        if len(arr_elm)>0:
            bigen=arr_elm[0]-len(arr_elm)
            end=arr_elm[-1]
            for i in range(0,len(path_arr)):
                if i==0:
                    returnpath=path_arr[i]
                elif i<bigen or i>end:
                    returnpath+="/"+path_arr[i]
            file_folder = os.path.dirname(returnpath)
            file_base_name = os.path.basename(returnpath)
        else:
            file_folder = os.path.dirname(pathin)
            file_base_name = os.path.basename(pathin)

        return file_folder,file_base_name,returnpath

    @classmethod
    def node_deep_val(cls,node=None,parm='file'):
        check_str = ["ch(","chs("]
        val = node.parm(parm).unexpandedString()
        node_deep_path = node.path()
        # print val
        for elm in check_str:
            if elm in val:
                import hou
                this_path = node.path()
                aim_path_list = cls.change_dot_val(this_path+"/"+val.split('"')[1])
                node_deep = hou.node(aim_path_list[0])
                parm=aim_path_list[1]
                val,node_deep_path=cls.node_deep_val(node_deep,parm)
        return val,node_deep_path


    @classmethod
    def node_type_filte(cls,nodepath='',types=[]):
        import hou
        result = True
        F_node = os.path.dirname(nodepath)
        if not F_node == "/":
            # print F_node
            if hou.node(F_node).type().name() in types:
                # print "pass pass pass pass pass pass..."
                passit = False
                if hou.node(F_node).type().name()=="filecache":
                    if hou.node(F_node).parm("loadfromdisk").eval():
                        passit = True
                if not passit:
                    result = False
            else:
                ## remove bypass node
                bypass = False
                if hasattr(hou.node(F_node),'isBypassed'):
                    if hou.node(F_node).isBypassed():
                        bypass = True
                if bypass:
                    result = False
                else:
                    result = cls.node_type_filte(F_node,types)
        return result


    @classmethod
    def TracebackError(cls,list_in='',asset_in={},rop=''):
        
        datapath = "B:\plugins\houdini\data" if str(sys.path[0]).startswith("/",1,3) else "/B/plugins/houdini/data"
        data_file = "%s/data.json"%datapath
        data_adict = eval(open(data_file, 'r').read()) if os.path.exists(os.path.abspath(data_file)) else {}
        error_info  = ''
        error_type = ''
        error_key = ''
        error_find = False
        print(list_in)
        print("-"*80)
        print("TracebackError Infos:")
        if len(data_adict):
            for key in data_adict:
                for elm in list_in:
                    if key in elm:
                        error_info = elm
                        error_type = data_adict[key]
                        error_key = key
                        error_find = True
                        break
        if not error_find:
            for elm in list_in:
                if "Error:       " in elm:
                    error_key = elm.split("Error:       ")[-1]
                    print("Error key word: ",error_key)

        elif not error_info == '':
            if error_type == "Miss files":
                import hou
                this_node_path = error_info.split(error_key)[-1].strip()
                node_find,file_find = cls.inpunodes_miss(hou.node(this_node_path),asset_in["Miss"])
                if not node_find == '':
                    print("MISS: ",node_find,file_find)

            if error_type == "camera_miss":
                print("The render camera is not in the .hip file.")
            if error_type == "camera_diff":
                cls.try_fix_abc_cam(rop,asset_in)


    @classmethod
    def inpunodes_miss(cls,node_in='',miss_asset_in=''):
        filetype = {"file":"","alembic":"","alembicarchive":"","tex":""}
        miss_nodes = miss_asset_in
        node_find = ''
        file_find = ''
        if node_in.type().name() in filetype:
            """  check exists  """
            node_find,file_find = cls.check_asset(node_in.path(),miss_asset_in)
        else:
            input_nodes = node_in.inputs()
            if len(input_nodes):
                for elm in input_nodes:
                    node_find,file_find = cls.inpunodes_miss(elm,miss_asset_in)
        return node_find,file_find

    @classmethod
    def check_asset(cls,node_path='',miss_asset_in=''):
        miss_node = ''
        miss_file = ''
        for key in miss_asset_in:
            if node_path in miss_asset_in[key]:
                miss_file = miss_asset_in[key][node_path][0]
                miss_node = node_path
                break
            else:
                old_node_path = cls.node_deep_val(hou.node(node_path),"file")[1]
                miss_node,miss_file = cls.check_asset(old_node_path,miss_asset_in)

        return miss_node,miss_file

    @classmethod
    def try_fix_abc_cam(cls,rop='',asset_in={}):
        camera_node = rop.parm("camera").eval()
        camera_diff_list = asset_in["Cam"]["diff"][rop.parm("camera").eval()]
        if camera_diff_list[-1] == rop.path(): ## check rop node
            camera_adict = camera_diff_list[0]
            # print str(camera_adict)
            base_elm = ''
            for i in range(len(camera_adict.keys())):
                if i==0:base_elm=camera_adict.keys()[i]
                if len(camera_adict.keys()[i])<len(base_elm):
                    base_elm = camera_adict.keys()[i]
            camera_file = camera_adict[base_elm][0]
            import hou
            for node in camera_adict:
                if not node == base_elm:
                    hou.node(node).parm("fileName").set(camera_file)