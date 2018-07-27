#!/usr/bin/python
# -*- coding=utf-8 -*-
# Author: kaname
# QQ: 1394041054
# Update:20180626

""" C4d loader """
# loading RBAnalzer.pyp to do it.


import os,sys,time
import subprocess,threading,shutil
from RenderBase import *
from CommonUtil import RBCommon as CLASS_COMMON_UTIL

#print ('..........This is custom by user 10000001............')

G_NODE_PY = 'c:\\script\\new_py\\'
pyp_rel_path = os.path.join(G_NODE_PY, 'CG\\C4d\\function\\RBAnalyzer.pyp')
maxon_ver = 'C:\\users\\enfuzion\\AppData\\Roaming\\MAXON\\CINEMA 4D %s\\' # %appdata%MAXON/CINEMA 4D R18
maxon_data_path = maxon_ver + 'plugins\\' # %appdata%MAXON/plugins/
print('maxon_ver: %s' % maxon_ver)
print('maxon_data_path: %s' % maxon_data_path)

c4d_pyp_config = {
    'CINEMA 4D R13' : 'R13_05DFD2A0',
    'CINEMA 4D R14' : 'R14_4A9E4467',
    'CINEMA 4D R15' : 'R15_53857526',
    'CINEMA 4D R16' : 'R16_14AF56B1',
    'CINEMA 4D R17' : 'R17_8DE13DAD',
    'CINEMA 4D R18' : 'R18_62A5E681',
    'CINEMA 4D R19' : 'R19_BFE04C39'
}


class C4dLoader(object):
    """ C4d loader class """
    def __init__(self, cgv, taskid, cgfile, taskjson, assetjson, tipsjson, autocommit):
        self.cgver = cgv
        self.taskid = taskid
        self.cgfile = cgfile
        self.taskjson = taskjson
        self.assetjson = assetjson
        self.tipsjson = tipsjson
        self.autocommit = autocommit

    def execute(self):#4
        #>>> 01.检测参数之cgfile是否存在 20180523update
        #input_cgfile = os.path.normpath(self.G_INPUT_CG_FILE)
        print (self.cgfile + ' ccccccccccc')
        if not os.path.exists(self.cgfile):
            print('Error: the input cg_file is not exists or damaged!!!!')
            #sys.stdout.flush()
            time.sleep(5)
            #cgfile不存在就杀进程
            """ kill all c4d process """
            node_py_cg = r'C:\script\new_py\CG\C4d\function'
            kill_command = node_py_cg + r'\taskkill.exe /F /IM "CINEMA 4D 64 Bit.exe"'
            print (kill_command)
            #os.system(kill_command)
            print('CINEMA 4D 64 Bit.exe ended!!!')
            return
        else:
            print('loading input cgfile success~~~')


        #01.remove RBAnalyzer.pyp
        C4dLoader.remove_pyp_script(self.cgver)
        #02. update pyp & run c4d.exe
        self.__update_pyp_script()

        #03.run c4d
        c4d_cmdline = r'"C:\Program Files\MAXON\%s\CINEMA 4D 64 Bit.exe" -task_id=%s -cg_file="%s" -task_json="%s" -asset_json="%s" -tips_json="%s" -auto_commit="%s"' \
            % (self.cgver, self.taskid, self.cgfile, self.taskjson, self.assetjson, self.tipsjson, self.autocommit)
        print ('Cmds: ' + c4d_cmdline)
        try:
            #prog = subprocess.Popen(c4d_cmdline, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
            prog = CLASS_COMMON_UTIL.cmd(c4d_cmdline)
            #out, err = prog.communicate()
            #print(out, err)
            print ('AAAAAAAAAAAAA')
        except:
            print ('subprocess CINEMA 4D 64 Bit.exe failed...')

    def __update_pyp_script(self):#2
        print ('update pyp.........')
        src = pyp_rel_path
        print (src + '3333')
        dst = maxon_data_path % (c4d_pyp_config.get(self.cgver))
        time.sleep(3)
        print ('dst: %s' % dst)
        try:
            self.__copy_file(src, dst)
            print ('RBAnalyzer.pyp was updated now!!!')
        except:
            pass


    @classmethod
    def remove_pyp_script(self, cgv):#1
        '''
        if %appdata% is not exists, then copy  20180709
        '''
        maxon_sour = r'B:\\plugins\\C4D\\appdata_file\\MAXON' # %appdata%MAXON
        maxon_dest = "%appdata%/"
        print (r'C:/fcopy/FastCopy.exe /speed=full /force_close /no_confirm_stop /force_start "' + maxon_sour + '" /to="' + maxon_dest + '"')
        os.system(r'C:/fcopy/FastCopy.exe /speed=full /force_close /no_confirm_stop /force_start "' + maxon_sour + '" /to="' + maxon_dest + '"')


        print ('del pyp......')
        dst_dir = maxon_data_path % (c4d_pyp_config.get(cgv))
        print (cgv)
        print ('dst_dir: %s' % dst_dir)
        
        for pyp in os.listdir(dst_dir):
            pyp_file = os.path.join(dst_dir, pyp)
            print (pyp_file+'111111')
            if pyp_file.endswith('.pyp'):
                os.remove(pyp_file)
            else:
                pass


    def __copy_file(self, src, dst): #3
        print (r'C:/fcopy/FastCopy.exe /speed=full /force_close /no_confirm_stop /force_start "' + src + '" /to="' + dst + '"')
        os.system(r'C:/fcopy/FastCopy.exe /speed=full /force_close /no_confirm_stop /force_start "' + src + '" /to="' + dst + '"')

if __name__ == '__main__':
    args = sys.argv

    cg_ver = args[1]
    task_id = args[2]
    cg_file = args[3]
    task_json = args[4]
    asset_json = args[5]
    tips_json = args[6]
    auto_commit = args[7]

    c4d_loader = C4dLoader(cg_ver, task_id, cg_file, task_json, asset_json, tips_json, auto_commit)
    c4d_loader.execute()
