import sys,os,subprocess,string,re,time,shutil
import json
import time

from itertools import islice


_PATH_ORG = os.environ.get('PATH')
os.environ['PATH'] = (_PATH_ORG if _PATH_ORG else "") + r";C:\Windows\system32"

def _RV_retrieveUniqueUserRoot(userid, fullfilename):
    root = _RV_getUserRootFromFileName(userid, fullfilename)
    return root

def _RV_getUserRootFromFileName(userid, filename):
    root = None
    filedir = os.path.dirname(filename)
    buff = filedir.split(userid)
    if len(buff)>1:
        root = buff[0] + userid
    return root

def _RV_filePath_Dir_Match_Counts(src_dir, tar_dir):
    # file path dir match count
    # be aware that file path dir order is not taken into consideration
    i = 0
    src_dir = src_dir.replace("\\","/")
    src_dirs = src_dir.split("/")
    tar_dir = tar_dir.replace("\\","/")
    tar_dirs = tar_dir.split("/")
    
    for d in src_dirs:
        if d in tar_dirs:
            i += 1
    
    return i

def _RV_fileName_Dir_Match_Counts(pmv_bn_no_ext, pmv_ext, pmv_dir, this_ffileName):
    # file base has to be the same
    # if yes, check file path dir match count
    # be aware that file path dir order is not taken into consideration
    # case ignore
    
    i = -1
    f_dir = os.path.dirname(this_ffileName)
    f_dir = f_dir.replace("\\","/")
    f_dirs = f_dir.split("/")
    pmv_dir = pmv_dir.replace("\\","/")
    pmv_dirs = pmv_dir.split("/")
    f_bn_ext = os.path.basename(this_ffileName)
    f_bn_no_ext = os.path.splitext(os.path.basename(this_ffileName))[0]
    f_ext = os.path.splitext(os.path.basename(this_ffileName))[1]
    if f_bn_no_ext == pmv_bn_no_ext and f_ext == pmv_ext:
        i = 0
        for d in f_dirs:
            if d in pmv_dirs:
                i += 1
    return i

def _RV_App_Nuke_Env_Setup(runpath, pyvd, pyvnd):
    os.environ['HFS'] = runpath
    _PATH_ORG = os.environ.get('PATH')
    os.environ['PATH'] = (_PATH_ORG if _PATH_ORG else "") + r";" + runpath
    libpath = "%slib" % (runpath)
    _PATH_New = os.environ.get('PATH')
    print "_PATH_New = " + _PATH_New
    sitepath = "%s/lib/site-packages" % (runpath)
    if libpath not in sys.path:
        sys.path.append(libpath)
    if sitepath not in sys.path:
        sys.path.append(sitepath)
        
        

    
def _RV_App_Nuke_new_Setup(_SERVER_Plugins, vers, skip_flag):
    vers = "Nuke9.0v9"
    print "_RV_App_Hou_Setup running, _SERVER_Plugins:%s, vers:%s, skip_flag:%s" % (_SERVER_Plugins, vers, str(skip_flag))
    fromdir = _SERVER_Plugins + r"/plugins/nuke/apps/7z"
    vname = vers + ".7z"
    todir = r"D:/plugins/nuke"
    if not os.path.exists(todir):
        #import rebult
        #rebult.main(todir)
        # os.rmdir(todir)
        # print("Do a removed of nuke folder")
        os.makedirs(todir)
    # print("makes folders for nuke")
    runpath = todir + r"/" + vers
    z7 = "D:/plugins/tools/7z/7z.exe"

    if skip_flag is not None:
        os.system ("robocopy /S /NDL /NFL %s %s %s" % (fromdir, todir, vname))
        cmd_un7z = z7 + " x -y -aos " + todir + r"/" + vname + " -o" + runpath
        subprocess.check_output(cmd_un7z, shell=True)
        #os.system("\"" + cmd_un7z + "\"")
        os.remove(todir + r"/" + vname)
    return runpath
    
def _RV_App_Nuke_Setup(_CID,_CGV):
    # if _CGV == '9.0v1':
        # if os.path.exists(r'C:/Program Files/Nuke9.0v1/'):
            # nuke_folder = r'C:/Program Files/Nuke9.0v1/'
        # else:
            # nuke_folder = None
    
    # if _CGV == '10.0v4':
        # if os.path.exists(r'C:/Program Files/Nuke10.0v4/'):
            # nuke_folder = r'C:/Program Files/Nuke10.0v4/'
        # else:
            # nuke_folder = None            
    # if _CGV == '10.5v1':
        # if os.path.exists(r'C:/Program Files/Nuke10.5v1/'):
            # nuke_folder = r'C:/Program Files/Nuke10.5v1/'
        # else:
            # nuke_folder = None
            
    if os.path.exists(r'C:/Program Files/Nuke9.0v1/'):
        nuke_folder = r'C:/Program Files/Nuke9.0v1/'
    else:
        nuke_folder = None 

    if nuke_folder == None:
        return None
        
    else:
        print nuke_folder
        
    runpath = nuke_folder

    # fromdir = _SERVER_IP_ROOT + r"/plugins/nuke/apps/7z"
    # vname = vers + ".7z"
    # todir = r"D:/plugins/nuke"
    # runpath = todir + r"/" + vers
    # z7 = "D:/nuke/tools/7z/7z.exe"
    #
    # if skip_flag is not None:
    #     os.system ("robocopy /S /NDL /NFL %s %s %s" % (fromdir, todir, vname))
    #     cmd_un7z = z7 + " x -y -aos " + todir + r"/" + vname + " -o" + runpath
    #     subprocess.check_output(cmd_un7z, shell=True)
    #     #os.system("\"" + cmd_un7z + "\"")
    #     os.remove(todir + r"/" + vname)
    return runpath

def _RV_Tool_7z_Setup(_SERVER_Plugins):
    localpath = r"D:/plugins/tools/7z"
    z7 = "D:/plugins/tools/7z/7z.exe"
    fromdir = _SERVER_Plugins + r"/tools/7-Zip"
    runpath = fromdir
    os.system ("robocopy /S /NDL /NFL %s %s %s" % (fromdir, localpath, "*"))
    runpath = localpath
    _PATH_ORG = os.environ.get('PATH')
    os.environ['PATH'] = (_PATH_ORG if _PATH_ORG else "") + r";" + runpath
    return runpath





def _RV_getNUKESaveVersion(NK_file):

    _HV = 0
    with open(NK_file, 'rb') as src:

        newline = []
        for line in src.readlines():
            if re.match(r'^version \d{1,2}.\d{1} v\d{1}\r$', line):
                print "NK Save line: %s" % line
                line = line.replace(' ','')
                _HV = line[7:-1]
                _HV = _HV.split('.')
                _HV = _HV[0] + _HV[1][0] + _HV[1][-1]

    return _HV
def _RV_getBestFitNUKEVersionFromNK(_SERVER_IP_ROOT, NK_file):

    ver = 0
    ver_str = r"NULL"
    ver = _RV_getNUKESaveVersion(NK_file)
    print "NK_SAVEVERSION: "+str(ver)
    #print ver

    ver_str = str(ver)

    print "ver_str _____"
    return ver_str

def _RV_changeNUKEVersion(NK_file,_CGV):
    

    with open(NK_file,"r") as f:
        lines = f.readlines()
    with open(NK_file,"w") as f_w:
        print lines[0]
        if lines[0].split('/')[1] == 'Applications':
            lines[0] = '#! C:/Program Files/Nuke10.0v4/nuke-10.0.4.dll -nx\n'
            for i,value in enumerate(lines):
                if re.match(r'^version \d{1,2}.\d{1} v\d{1}$', value):
                    print "NK Save line: %s" % value
                    print i
                    lines[i] = 'version 10.0 v4\n'
        elif _CGV == '9.0v1':
            lines[0] = '#! C:/Program Files/Nuke9.0v9/nuke-9.0.9.dll -nx\n'
            for i,value in enumerate(lines):
                if re.match(r'^version \d{1,2}.\d{1} v\d{1}$', value):
                    print "NK Save line: %s" % value
                    print i
                    lines[i] = 'version 9.0 v9\n'
            print lines[0]
            
        f_w.writelines(lines)
        
        
def HasExtension( path ):
    filename = os.path.basename( path )

    return filename.rfind( "." ) > -1

# Checks if path is local (c, d, or e drive).
def IsPathLocal( path ):
    lowerPath = path.lower()
    if lowerPath.startswith( "c:" ) or lowerPath.startswith( "d:" ):
        return True
    return False

def IsPathNetIp( path ):
    lowerPath = path.lower()
    if lowerPath.startswith( "//" ):
        return True
    return False





# Checks if the given filename ends with a movie extension
def IsMovie( path ):
    lowerPath = path.lower()
    if lowerPath.endswith( ".mov" ):
        return True
    return False

# Checks if the filename is padded (ie: \\output\path\filename_%04.tga).
def IsPadded( path ):
    #Check for padding in the file
    paddingRe = re.compile( "%([0-9]+)d", re.IGNORECASE )
    if paddingRe.search( path ) != None:
        return True
    elif path.find( "#" ) > -1:
        return True
    return False




def RightReplace(s, old, new, occurrence):
    li = s.rsplit(old, occurrence)
    return new.join(li)



def GetPaddedPath( path ):
    # paddingRe = re.compile( "%([0-9]+)d", re.IGNORECASE )

    # paddingMatch = paddingRe.search( path )
    # if paddingMatch != None:
        # paddingSize = int(paddingMatch.lastgroup)

        # padding = ""
        # while len(padding) < paddingSize:
            # padding = padding + "#"

        # path = paddingRe.sub( padding, path, 1 )

    paddingRe = re.compile( "([0-9]+)", re.IGNORECASE )

    paddingMatches = paddingRe.findall( path )
    if paddingMatches != None and len( paddingMatches ) > 0:
        paddingString = paddingMatches[ len( paddingMatches ) - 1 ]
        paddingSize = len(paddingString)

        padding = ""
        while len(padding) < paddingSize:
            padding = padding + "#"

        path = RightReplace( path, paddingString, padding, 1 )

    return path


def store(INF,data):
    with open(INF, 'w') as json_file:
        json_file.write(json.dumps(data))

def load(INF):
    with open(INF) as json_file:
        data = json.load(json_file)
        return data



# if __name__ == "__main__":
#
#     data = {}
#     data["last"]=time.strftime("%Y%m%d")
#     store(data)
#
#     data = load()
#     print data["last"]