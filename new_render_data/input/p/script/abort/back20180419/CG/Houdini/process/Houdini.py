#!/usr/bin/env python
#encoding:utf-8
# -*- coding: utf-8 -*-
import os,sys
from RenderBase import RenderBase
from CommonUtil import RBCommon as CLASS_COMMON_UTIL

reload(sys)
sys.setdefaultencoding('utf-8')
class Houdini(RenderBase):
    def __init__(self,**paramDict):
        print("Houdini class")
        RenderBase.__init__(self,**paramDict)
        self.format_log('Houdini.init','start')
        self.G_RENDER_OPTIONS = {"render_rop":self.G_CG_OPTION} if self.G_CG_OPTION !=''else {} 

        dir_list=[]
        CLASS_COMMON_UTIL.make_dirs(dir_list)
        self.format_log('done','end')


    def LogsCreat(self,info='',render=False,debug=True):
        if render and debug:
            self.G_RENDER_LOG.info(str(info))
            self.G_DEBUG_LOG.info(str(info))
        elif render and not debug:
            self.G_RENDER_LOG.info(str(info))
        else:
            self.G_DEBUG_LOG.info(str(info))

    def Updata(self):
        pass