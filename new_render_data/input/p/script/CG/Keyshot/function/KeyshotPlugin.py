import os,sys,time
import re
import subprocess
import shutil
from KeyshotUtil import KeyshotUtil


class KeyshotPlugin(object):
    """docstring for HoudiniPlugin"""
    def __init__(self, arg):
        super(KeyshotPlugin, self).__init__()
        self.arg = arg

    @classmethod
    def BaseDataSetup(cls,cls_in=''):
        cls_in.LogsCreat("BaseDataSetup start...")
        cls_in.LogsCreat("...")
        cls_in._bip_file = cls_in.G_INPUT_CG_FILE.replace("\\","/") if len(cls_in.G_INPUT_CG_FILE) else ''
        cls_in._output = cls_in.G_WORK_RENDER_TASK_OUTPUT.replace("\\","/")
        cls_in._task_folder = cls_in.G_WORK_RENDER_TASK.replace("\\","/")

        if cls_in._plant=='Linux':
            cls_in._keyshot_client_dir = ''
            cls_in._keyshot_PLuing_dirt = ''
            app_path = ""
        else:
            cls_in._keyshot_client_dir = 'C:/Program Files'
            cls_in._keyshot_PLuing_dirt = 'B:/plugins/KeyShot' ##if os.path.exists("B:/plugins/KeyShot") else "%s/plugins/keyshot"%cls_in.G_PLUGIN_PATH.replace("\\","/")

        cls_in._code_base_path = os.path.join(cls_in.G_NODE_PY,"CG/Keyshot").replace("\\","/")
        cls_in._keyshot_version = cls_in.G_CG_CONFIG_DICT["cg_version"]
        cls_in._plugins = cls_in.G_CG_CONFIG_DICT["plugins"]
        cls_in.user_id = cls_in.G_USER_ID

        if cls_in.G_ACTION == 'Render':
            cls_in._frames = [cls_in.G_CG_START_FRAME,cls_in.G_CG_END_FRAME,cls_in.G_CG_BY_FRAME]
            # cls_in._camers = "1111"#cls_in.G_RENDER_OPTIONS['render_rop']if 'render_rop' in cls_in.G_RENDER_OPTIONS.keys()else ''
            # if cls_in._camers == '': ## call errors
            #     cls_in._run_code_result = False
            #     cls_in._erorr_code = 'RenderHoudini.BaseDataSetup.rop call'
            #     cls_in._erorr_code_info = 'The rop is not set!.'

        cls_in.LogsCreat("BaseDataSetup end.")
        cls_in.LogsCreat("")

    @classmethod
    def DataInfo(cls,cls_in=''):
        # --------------------------------------------------------------------------------
        #                           JOB INFORMATION PRINT
        # --------------------------------------------------------------------------------
        cls_in.LogsCreat(" ")
        cls_in.LogsCreat("JOB INFORMATION")
        cls_in.LogsCreat("Software: Keyshot %s"%cls_in._keyshot_version)
        cls_in.LogsCreat("Function: %s"% (cls_in.G_ACTION if not cls_in.G_ACTION=='' else 'Analyze'))
        cls_in.LogsCreat("...")
        cls_in.LogsCreat("Bip file: %s"%cls_in._bip_file)
        cls_in.LogsCreat("Plugins Info: %s"%(cls_in._plugins if len(cls_in._plugins) else "None"))
        # --------------------------------------------------------------------------------
        # ----------------------------RENDER LOG INFORMATION PRINT------------------------

        cls_in.LogsCreat("Log start...\n"+"-"*150+"\n"+"/"*150+"\n"+"-"*150+"\n",True,False)
        cls_in.LogsCreat("Software: Keyshot %s\n\n"%cls_in._keyshot_version,True,False)
        if cls_in.G_ACTION == 'Render':
            cls_in.LogsCreat("Frames: %s"%cls_in._frames)
            # cls_in.LogsCreat("Cameras: %s"%cls_in._camers)


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


    @staticmethod
    def copyfiles(pathin,frame,aim_name):
        source_path = os.path.abspath(pathin)
        frame_folder = str(frame).zfill(4)

        for dirpath,dirnames,filenames in os.walk(source_path):
            if dirpath == source_path:
                #print(dirpath)
                #print(dirnames)
                #print(filenames)
                if len(dirnames):
                    for fd in dirnames:
                        if fd not in aim_name:
                            path_new = os.path.join(dirpath,fd)
                            path_aim = os.path.join(dirpath,frame_folder,fd)
                            print(path_new,path_aim)
                            os.system ("robocopy /e /ns /nc /nfl /ndl /np /move %s %s" % (path_new, path_aim))
                if len(filenames):
                    for pic in filenames:
                        path_new = os.path.join(dirpath,pic)
                        path_aim = os.path.join(dirpath,frame_folder,pic)
                        if not os.path.exists(os.path.join(dirpath,frame_folder)):os.makedirs(os.path.join(dirpath,frame_folder))
                        print(path_new,path_aim)
                        os.system ('copy /y  "%s" "%s"' % (path_new, path_aim))
                        os.remove(path_new)
        aim_name.append(frame_folder)
        return aim_name