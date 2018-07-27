import os,sys,time,re
import argparse
import HoudiniBase


runinfo=''
parser = argparse.ArgumentParser()
parser.add_argument('-project', type=str, required=True, help='.hip file to render')
parser.add_argument('-rop', type=str, required=True, help='rop node to render')
parser.add_argument('-GPU', type=int, required=True, help='the gpu id which to be used to render')
parser.add_argument('-frame', type=str, required=True, help='frames to render')
parser.add_argument('-outdir', type=str, required=True, help='image with dir to render to')
parser.add_argument('-HIP', type=str, required=True, help='HIP path val')
parser.add_argument('-function', type=str, required=True, help='Functions for the job, noly "analysis" and "render"')
parser.add_argument('-cfg', type=str, required=False, help='The json adict for render')

def print_times(info="",file="",type=""):

    time_point=time.strftime("%b_%d_%Y %H:%M:%S", time.localtime())
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

args = parser.parse_args()

def FramesSet():
    all_frames = args.frame
    types = 0
    renderjobs = {}
    ## 5 5 1  /  1,3,6  /  1,2-5,9   /  3,2-10[3],5
    k = 0
    if "," in all_frames:
        frames_list = all_frames.split(",")
        for i in range(len(frames_list)):
            if "-" in frames_list[i]:
                if "[" in frames_list[i]: ## 2-10[3]
                    frame_sp = frames_list[i].split("]")[0].split("[")
                    frame_ah = frame_sp[0].split("-")
                    renderjobs[str(k)] = [frame_ah[0],frame_ah[-1],frame_sp[-1]]
                    k +=1
                else: ## 2-5
                    frame_ah = frames_list[i].split("-")
                    renderjobs[str(k)] = [frame_ah[0],frame_ah[-1],str(1)]
                    k +=1
            else:  ## 1
                renderjobs[str(k)] = [frames_list[i],frames_list[i],str(1)]
                k +=1
    else:
        frames_arr_s=args.frame.split(" ")
        renderjobs[str(k)] = [frames_arr_s[0],frames_arr_s[1],frames_arr_s[2]]

    return renderjobs


def HfsMmain():

    ## --------------------creat a job----------------------------
    hfs_obj = HoudiniBase.hfs_fileBase(args)
    print_times('Load hip file start...')
    try:
        hfs_obj.loadhipfile()
    except :
        print_times('Load hip ignore Errors.')
    print_times('Load hip file end.')

    sys.stdout.flush()
    time.sleep(1)

    ## -----------------------------------------------------------

    ropnode=hou.node(args.rop)
    print_times('Jobs start...')

    if args.function=="analysis":
        print_times('Job type: Analysis job ')
        hfs_obj.Extued()
        
        sys.stdout.flush()
        time.sleep(1)
        
        hfs_obj.analy_info()

    elif args.function=="render":

    ## ----------------------loop render ------------------------
    ## --------------------- loop type --------------------------

        loop_types = ['Redshift_ROP','ifd','arnold']
        if ropnode.type().name() in loop_types:
            frame_adict = FramesSet()
            if len(frame_adict.keys()):
                print_times(str(frame_adict))
                # for key in frame_adict.keys():

                if ropnode.type().name()=='Redshift_ROP':
                    print_times('Job type: Redshift Render job ')
                    # hfs_obj.setframes()
                    hfs_obj.setoutput_RS()
                    hfs_obj.Extued()
                    
                    sys.stdout.flush()
                    time.sleep(1)
                
                    for key in frame_adict.keys():
                        hfs_obj.frame = frame_adict[key]
                        hfs_obj.setframes()
                        hfs_obj.render_RS()

                elif ropnode.type().name()=='ifd':
                    print_times('Job type: Mantra Render job ')
                    # hfs_obj.setframes()
                    hfs_obj.setoutput_Mantra()
                    hfs_obj.Extued()
                    
                    sys.stdout.flush()
                    time.sleep(1)
                    
                    for key in frame_adict.keys():
                        hfs_obj.frame = frame_adict[key]
                        hfs_obj.setframes()
                        hfs_obj.render_Mantra()

                elif ropnode.type().name()=='arnold':
                    print_times('Job type: Arnold Render job ')
                    # hfs_obj.setframes()
                    hfs_obj.setoutput_AR()
                    hfs_obj.Extued()
                    
                    sys.stdout.flush()
                    time.sleep(1)
                    
                    for key in frame_adict.keys():
                        hfs_obj.frame = frame_adict[key]
                        hfs_obj.setframes()
                        hfs_obj.render_AR()

        elif ropnode.type().name()=='rop_geometry':
            print_times('Job type: Simulation job ')
            hfs_obj.setframes()
            hfs_obj.Extued()
            
            sys.stdout.flush()
            time.sleep(1)
            
            hfs_obj.render_sml()
        else:
            print_times('The can\'t find this render: %s '% ropnode.type().name())
            sys.exit(2)
    else:
        print_times('The function only for "analysis" or "render" ')
    print_times('Jobs end.')

if __name__=="__main__":

    print('...')
    print('-'*50)
    print('-'*50)
    print('Creat Houdini base information for running this Job, start Houdini_Files_Function...')
    print('...')    

    HfsMmain()
