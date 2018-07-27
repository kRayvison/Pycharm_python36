#!/usr/bin/python
# -*- coding=utf-8 -*-
# Author: kaname
# QQ: 1394041054

""" C4d loader """

import os
import sys
import subprocess
from RenderBase import *
from CommonUtil import RBCommon as CLASS_COMMON_UTIL

G_NODE_PY = 'c:/script/new_py/'
pyp_rel_path = os.path.join(G_NODE_PY, 'CG/C4d/function/RBAnalyzer.pyp')
maxon_data_path = 'C:/users/enfuzion/AppData/Roaming/MAXON/CINEMA 4D %s/plugins/'

c4d_pyp_config = {
    'CINEMA 4D R13' : 'R13_05DFD2A0',
    'CINEMA 4D R14' : 'R14_4A9E4467',
    'CINEMA 4D R15' : 'R15_53857526',
    'CINEMA 4D R16' : 'R16_14AF56B1',
    'CINEMA 4D R17' : 'R17_8DE13DAD',
    'CINEMA 4D R18' : 'R18_62A5E681',
}


# def soft_version(self):
#     print 'config software...'
#     self.G_LOCAL_MAXON='C:/Program Files/MAXON'
#     self.G_CG_VERSION =self.G_CG_CONFIG_DICT['cg_name'] + ' ' + self.G_CG_CONFIG_DICT['cg_version']


class C4dLoader(object):
    """ C4d loader class """
    def __init__(self, cgv, taskid, cgfile, taskjson, assetjson, tipsjson):
        self.cgver = cgv
        self.taskid = taskid
        self.cgfile = cgfile
        self.taskjson = taskjson
        self.assetjson = assetjson
        self.tipsjson = tipsjson

    def execute(self):
        #01.remove RBAnalyzer.pyp
        self.__remove_pyp_script()
        #02. update pyp & run c4d.exe
        self.__update_pyp_script()

        #03.run c4d
        c4d_cmdline = '"C:/Program Files/MAXON/%s/CINEMA 4D.exe" -task_id=%s -cg_file="%s" -task_json="%s" -asset_json="%s" -tips_json="%s"' \
            % (self.cgver, self.taskid, self.cgfile, self.taskjson, self.assetjson, self.tipsjson)
        print 'Cmd: ' + c4d_cmdline
        try:
            #prog = subprocess.Popen(c4d_cmdline, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
            prog = CLASS_COMMON_UTIL.cmd(c4d_cmdline)
            #out, err = prog.communicate()
            #print(out, err)
        except:
            print 'subprocess CINEMA 4D.exe failed...'             

    def __update_pyp_script(self):#2
        print 'update pyp.........'
        src = pyp_rel_path
        print src + '3333'
        dst = maxon_data_path % (c4d_pyp_config.get(self.cgver))
        print dst + '2222'
        try:
            self.__copy_file(src, dst)
        except:
            pass

    def __remove_pyp_script(self):#1
        print 'del pyp......'
        dst_dir = maxon_data_path % (c4d_pyp_config.get(self.cgver))
        print dst_dir + '000000'
        dst_pyp_file = os.path.join(dst_dir, 'RBAnalyzer.pyp')
        print dst_pyp_file + '11111'
        try:
            os.remove(dst_pyp_file)
        except:
            pass

    def __copy_file(self, src, dst):
        os.system('xcopy /f /y /e "%s" "%s"' % (src, dst))

if __name__ == '__main__':
    args = sys.argv

    cg_ver = args[1]
    task_id = args[2]
    cg_file = args[3]
    task_json = args[4]
    asset_json = args[5]
    tips_json = args[6]

    c4d_loader = C4dLoader(cg_ver, task_id, cg_file, task_json, asset_json, tips_json)
    c4d_loader.execute()
