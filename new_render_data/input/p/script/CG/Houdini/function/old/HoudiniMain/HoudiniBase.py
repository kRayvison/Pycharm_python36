import os,sys,time,re
import json
#import argparse
#from RS_Lib import ExtInfo
import hou

py_folder = sys.path[0]
base_folder = os.path.dirname(os.path.abspath(os.sys.path[0]))
sys.path.append(base_folder)

runinfo=''

def print_times(info="",file="",type=""):

    time_point=time.strftime("%b_%d_%Y %H:%M:%S", time.localtime())
    # infos = "["+str(time_point) + "] " + str(info)
    addpoint = "HTS"
    infos = "["+str(addpoint) + "] " + str(info)
    print (infos)

    if type=="w":
        if not os.path.exists(file):
            if not os.path.exists(os.path.dirname(file)):
                os.makedirs(os.path.dirname(file))
            with open(file,"w") as f:
                f.close()
        else:
            with open(file,"a") as f:
                f.write(infos)
                f.close()


class hfs_fileBase():
    
    def __init__(self,args=""):
        print_times('Start hfs base...')
        self.args = args
        self.frame = ''
        self.basedir = os.path.abspath(self.args.project)
        self.basedir = self.basedir.replace("\\","/")
        self._hip_val = os.path.dirname(self.args.project).replace("\\","/")
        self.CreatRenderMethod()

    def CreatRenderMethod(self):
        ## 
        print_times('CreatRenderMethod start...')
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
        print_times('CreatRenderMethod end.')

    def loadhipfile(self):

        self.hip_file=self.args.project
        if os.path.exists(self.hip_file):
            print_times ("Loading hip file: %s" % self.hip_file)
            try:
                hou.hipFile.load(self.hip_file)
                print_times ("Loading hip file success")
        ## -----------------------------------------------------------
        ## ----------if it is render job , get the rop node ----------
                if self.args.function=="render":
                    self.ropnode=hou.node(self.args.rop)
                
                # update $HIP once file loaded
                _hip_var = os.path.dirname(self.hip_file)
                hou.hscript("setenv HIP=" + str(_hip_var))
                hou.hscript("varchange")
                
            except (IOError ,ZeroDivisionError),e:
                print_times (e)
        else:
            print_times ("ERROR: the hip file is not exist!")
            sys.exit(1)

    def Custmset(self):
        print_times("Custom Setup start...")
        
        _files_name = []
        _config_patn = "%s/custom/Bhand"%base_folder
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
                    print_times(e)
        print_times("Custom Setup end.")

    def DataSet(self):
        print_times("DataSet Setup start...")

        cfg_path = '%s/cfg'%self.args.cfg.replace("\\","/")
        out_dir = '%s/output'%self.args.cfg.replace("\\","/")
        self._cfg_task = '%s/task.json'%cfg_path
        cfg_asset = '%s/asset.json'%cfg_path

        self.Json_adict = eval(open(self._cfg_task, 'r').read()) if os.path.exists(self._cfg_task) else {}
        self.Asset_adict = eval(open(cfg_asset, 'r').read()) if os.path.exists(cfg_asset) else {}


        print_times("DataSet Setup end.")

    def configs(self):
        print_times("Config Setup start...")
        ## All the code in configs folder will run one time 
        _files_name = []
        _config_patn = "%s/configs/Bhand"%base_folder
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
                    print_times(e)
        print_times("Config Setup end.")

    def writeinfo(self,info="",file="",types='txt'):
        if types == 'txt':
            with open(file,"w") as f:
                f.write(info)
                f.close()
        elif types == 'json':
            with open(file,"w")as f:
                json.dump(info,f)
                f.close()
        print_times("Infomations write to %s" %file)


    def analy_info(self):
        print_times("Analysis & file start...")
    
        rop_node = {}
        geo_node = {}

        if self.args.function == "analysis":
            self.file_info = self.args.outdir
        else:
            self.file_info = "D:/houdini/RS/Analysis_info.txt"
            if not os.path.exists("D:/houdini/RS"):
                os.makedirs("D:/houdini/RS")
            print_times("The function is not used as analysis,write the infomation to default file")
        info = ''
        i = 0
        print_times("Searching Geometrry Rops...")
        simu_cunt = 0
        for obj in hou.node('/').allSubChildren():
            nodes = {} ## {"node":"","frames":"","option":""}
            objPath = obj.path()
            objPath = objPath.replace('\\','/')
            objTypeName = obj.type().name()
            if objTypeName in ['geometry','rop_geometry']:
                render_rop_Node = hou.node(objPath)
                if render_rop_Node.parm("execute"):
                    print_times("\t\tGeometry ROP: %s" % render_rop_Node)
                    if i>0: info += '\n'
                    info += objPath
                    nodes["node"] = objPath

                    info += '|' + str(obj.evalParm('f1'))

                    info += '|' + str(obj.evalParm('f2'))

                    info += '|' + str(obj.evalParm('f3'))
                    nodes["frames"] = [str(obj.evalParm('f1')), str(obj.evalParm('f2')), str(obj.evalParm('f3'))]

                    info += '|' + '0'
                    nodes["option"] = '0'

                    geo_node[simu_cunt] = nodes
                    i+=1
                    simu_cunt += 1
        print_times("Total Render Nodes: %s" % simu_cunt)

        print_times("Searching Render ROPS ...")
        rop_cunt=0
        for obj in hou.node('/').allSubChildren():
            nodes={}
            objPath = obj.path()
            objPath = objPath.replace('\\','/')
            objTypeName = obj.type().name()

            if objTypeName in ['ifd', 'arnold','Redshift_ROP']:
                render_rop_Node = hou.node(objPath)
                print_times("\t\tRender ROP: %s" % render_rop_Node)
                if i>0: info += '\n'
                info += objPath
                info += '|' + str(obj.evalParm('f1'))
                info += '|' + str(obj.evalParm('f2'))
                info += '|' + str(obj.evalParm('f3'))
                info += '|' + '-1'

                nodes["node"] = objPath
                nodes["frames"] = [str(obj.evalParm('f1')),str(obj.evalParm('f2')),str(obj.evalParm('f3'))]
                nodes["option"] = '-1'
                rop_node[rop_cunt] = nodes
                i+=1
                rop_cunt+=1
        print_times("Total Render ROPs: %s" % rop_cunt)

        scene_info = {"geo_node":geo_node,"rop_node":rop_node}
        print_times("...")
        print_times("Result:\n[HTS] %s"%str(scene_info))
        print_times(".")

        self.Json_adict["scene_info"] = scene_info
        # self.writeinfo(info,self.file_info)
        self.writeinfo(self.Json_adict,self._cfg_task,'json')
        print_times("Analysis & file end.")


    def setframes(self):
        print_times("setframes start...")
        
        SF = float(self.ropnode.evalParm('f1'))
        EF = float(self.ropnode.evalParm('f2'))
        BF = float(self.ropnode.evalParm('f3'))
        print_times("FRAME RANGE IN THIS FILE's SET: "+str(SF)+"-"+str(EF)+"["+str(BF)+"]")

        if self.ropnode.evalParm("trange")!=1:
            self.ropnode.parm("trange").set(1)

        if self.ropnode.parm('f1').isLocked():
            self.ropnode.parm('f1').lock(False)
        if self.ropnode.parm('f2').isLocked():
            self.ropnode.parm('f2').lock(False)
        if self.ropnode.parm('f3').isLocked():
            self.ropnode.parm('f3').lock(False)
        self.ropnode.parm('f1').deleteAllKeyframes()
        self.ropnode.parm('f2').deleteAllKeyframes()
        self.ropnode.parm('f3').deleteAllKeyframes()

        frames_arr=self.frame
        print_times (frames_arr)
        Fr1=float(frames_arr[0].strip())
        Fr2=float(frames_arr[1].strip())
        Fr3=float(frames_arr[2].strip())
        self.ropnode.parm("f1").set(Fr1)
        self.ropnode.parm("f2").set(Fr2)
        self.ropnode.parm("f3").set(Fr3)

        SF = float(self.ropnode.evalParm('f1'))
        EF = float(self.ropnode.evalParm('f2'))
        BF = float(self.ropnode.evalParm('f3'))
        print_times("NEW FRAME RANGE TO RENDER: "+str(SF)+"-"+str(EF)+"["+str(BF)+"]")

        print_times("setframes end.")

    def CreatOutput(self,valparm=""):

        print_times("ROP output parm: %s" % valparm)
        
        self.outfile_hip=self.ropnode.evalParm(valparm)
        print_times("Output values: %s" % self.outfile_hip)
        if self.outfile_hip=='(not set)' or self.outfile_hip=='':
            self.outfile_hip=os.path.join(self.args.HIP,'out/default.0001.exr')

        HIP_val = ''
        HIP_val = self.args.HIP.replace("\\","/")if "\\" in self.args.HIP else self.args.HIP
        if HIP_val.endswith('/'): HIP_val = HIP_val[:-1]
        # print_times("$Hip_Save_Val: %s" % HIP_val)
        
        outfile_hip=self.outfile_hip.replace("\\","/")   ### $HIP/aa/aa/aa.$F4.exr
        if HIP_val in outfile_hip:
            outfile_arr_main=outfile_hip.split(HIP_val+"/")[-1]   ### aa/aa/aa.$F4.exr  aa.$F4.exr
        elif self._hip_val in outfile_hip:
            outfile_arr_main=outfile_hip.split(self._hip_val+"/")[-1]   ### aa/aa/aa.$F4.exr  aa.$F4.exr
        elif ":/" in outfile_hip:
            outfile_arr_mains=outfile_hip.split("/")   ### aa/aa/aa.$F4.exr  aa.$F4.exr
            outfile_arr_main = (outfile_arr_mains[-2]+"/"+outfile_arr_mains[-1]) if len(outfile_arr_mains)>2 else outfile_arr_mains[-1]
        else:
            outfile_arr_main = outfile_hip
        
        outfile_arr=outfile_arr_main.split("/") if "/" in outfile_arr_main else [outfile_arr_main]

        FFs=re.findall(r"\d+",outfile_arr[-1])
        FF = FFs[-1] if len(FFs) else '001'
        dotF="$F%d" % len(FF)
        namepart=outfile_arr[-1].split(".")
        name_s = ''
        if len(namepart)>2:
            for i in range(len(namepart)):
                if i == len(namepart)-2:
                    break
                name_s += namepart[i] + "."
        else:
            name_s = namepart[0]
        outname = name_s+dotF+"."+namepart[-1]  ### aa.$F4.exr
        outfile_M=outfile_arr_main.split("/"+outfile_arr[-1])[0] if "/" in outfile_arr_main else ''

        # $HIP/aaa/aass/aaa.$F3.exr
        out_dir=os.path.join(self.args.outdir,outfile_M)
        out_dir=out_dir.replace("\\","/")
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        outputFiles=os.path.join(self.args.outdir,outfile_M,outname)
        outputFiles=outputFiles.replace("\\","/")
        # print_times("outputFiles .../%s/%s" % (outfile_M,outname))
        print_times("OutputFiles changed to: %s" % outputFiles)
        
        return outputFiles


    def setoutput_RS(self):
        print_times("Output_RS set start...")
        
        if self.args.GPU==0:
            hou.hscript("Redshift_setGPU -s 10")
            print_times('Set GPU %d avilable' % self.args.GPU)
        elif self.args.GPU==1:
            #hou.hscript("Redshift_setGPU -s 01")
            print_times('Set GPU avilable' )
            #print_times('Set GPU %d avilable' % self.args.GPU)
        else:
            print_times ("ERROR WITH GPU ID: %d [0 TO 1 FOR RIGHT NOW(17/3/2017)]" % self.args.GPU)
            sys.exit(1)

        ropTypeName = self.ropnode.type().name()
        print_times("ROP output type %s" % ropTypeName)
        if ropTypeName in ['Redshift_ROP']:
            outputFiles = self.CreatOutput("RS_outputFileNamePrefix")
            if not self.ropnode.evalParm("RS_outputEnable"):
                self.ropnode.parm("RS_outputEnable").set(True)
            self.ropnode.parm("RS_outputFileNamePrefix").set(outputFiles)
            print_times("Output check:")
            print_times(self.ropnode.evalParm("RS_outputFileNamePrefix"))
        
        print_times("Output_RS set end.")

    def render_RS(self):
        print_times("Render_RS start...")
        root_take = hou.takes.rootTake()
        curt_take = hou.takes.currentTake()
        n_parm = self.ropnode.parmTuple("RS_renderToMPlay") if self.ropnode.type().name()=="Redshift_ROP" else ""
        if not n_parm == "":
            if curt_take != root_take:
                if not curt_take.hasParmTuple(n_parm):
                    curt_take.addParmTuple(n_parm)
                    #curt_take.removeParmTuple(n_parm
            if self.ropnode.parm("RS_renderToMPlay").eval()==1:
                self.ropnode.parm("RS_renderToMPlay").set(0)

        self.ropnode.render(verbose=self._verbose_s,quality=self._quality, ignore_inputs=self._ignore_inputs, method=self._method, ignore_bypass_flags=self._ignore_bypass_flags, ignore_lock_flags=False, output_progress=False)
        print_times("Render_RS end.")

    def setoutput_Mantra(self):
        print_times("Output_Mantra set start...")
        
        ropTypeName = self.ropnode.type().name()
        print_times("ROP output type %s" % ropTypeName)
        if ropTypeName in ['ifd']:
            outputFiles = self.CreatOutput("vm_picture")
            self.ropnode.parm("vm_picture").set(outputFiles)
            print_times("Output check:")
            print_times(self.ropnode.evalParm("vm_picture"))
            
            ### set aov pass
            out_aovs = self.ropnode.parm("vm_numaux").eval()
            if out_aovs > 0:
                print_times("Output_Mantra aov set start...")
                aovs_list = []
                for i in range(out_aovs):
                    parm_k = "vm_disable_plane%d"%(i+1)
                    if not self.ropnode.parm(parm_k).eval():
                        parm_f_use = "vm_usefile_plane%d"%(i+1)
                        if self.ropnode.parm(parm_f_use).eval():
                            parm_f_val = "vm_filename_plane%d"%(i+1)
                            aovs_list.append(parm_f_val)
                if len(aovs_list) > 0:
                    for elm in aovs_list:
                        _outputFiles = self.CreatOutput(elm)
                        self.ropnode.parm(elm).set(_outputFiles)

        print_times("Output_Mantra set end.")

    def render_Mantra(self):

        print_times("Render_Mantra start...")
        #root_take = hou.takes.rootTake()
        #curt_take = hou.takes.currentTake()
        _ifd = self.ropnode.parm("soho_outputmode").eval()
        if _ifd:
            self.ropnode.parm("soho_outputmode").set(0)

        # set the Log level to 5 
        _level = self.ropnode.parm("vm_verbose").eval()
        if int(_level) != 5:
            _level = self.ropnode.parm("vm_verbose").set(5)

        self.ropnode.render(verbose=self._verbose_s,quality=self._quality, ignore_inputs=self._ignore_inputs, method=self._method, ignore_bypass_flags=self._ignore_bypass_flags, ignore_lock_flags=False, output_progress=False)
        print_times("Render_Mantra end.")

    def setoutput_AR(self):
        print_times("Output_AR set start...")

        ropTypeName = self.ropnode.type().name()
        print_times("ROP output type %s" % ropTypeName)
        if ropTypeName in ['arnold']:
            outputFiles = self.CreatOutput("ar_picture")
            self.ropnode.parm("ar_picture").set(outputFiles)
            print_times("Output check:")
            print_times(self.ropnode.evalParm("ar_picture"))
            
            ### set aov pass
            out_aovs = self.ropnode.parm("ar_aovs").eval()
            if out_aovs > 0:
                print_times("Output_Arnold aov set start...")
                aovs_list = []
                for i in range(out_aovs):
                    parm_k = "ar_enable_aov%d"%(i+1)
                    if self.ropnode.parm(parm_k).eval():
                        parm_f_use = "ar_aov_separate%d"%(i+1)
                        if self.ropnode.parm(parm_f_use).eval():
                            parm_f_val = "ar_aov_separate_file%d"%(i+1)
                            aovs_list.append(parm_f_val)
                if len(aovs_list) > 0:
                    for elm in aovs_list:
                        _outputFiles = self.CreatOutput(elm)
                        self.ropnode.parm(elm).set(_outputFiles)
        
        print_times("Output_AR set end.")

    def render_AR(self):

        print_times("Render_AR start...")
        # root_take = hou.takes.rootTake()
        # curt_take = hou.takes.currentTake()
        self.ropnode.render(verbose=self._verbose_s,quality=self._quality, ignore_inputs=self._ignore_inputs, method=self._method, ignore_bypass_flags=self._ignore_bypass_flags, ignore_lock_flags=False, output_progress=False)
        print_times("Render_AR end.")

    def render_sml(self):
        ## function for simulation
        print_times("Render_sml start...")
        self.sml_out = self.ropnode.parm("sopoutput").eval()
        print_times("Simulation output: %s" % self.sml_out)

        self.ropnode.render(verbose=self._verbose_s,quality=self._quality, ignore_inputs=self._ignore_inputs, method=self._method, ignore_bypass_flags=self._ignore_bypass_flags, ignore_lock_flags=False, output_progress=False)
        print_times("Render_sml end.")

    def Extued(self):
        
        self.DataSet()
        # self.configs()
        # self.Custmset()

        # ---------------------------------------------------
        # depends=r' -s True'
        # renderscript="render "+args.rop+depends
        # hou.hscript(renderscript)