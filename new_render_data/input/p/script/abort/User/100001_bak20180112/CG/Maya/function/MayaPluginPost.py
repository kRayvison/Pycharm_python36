#!/usr/bin/env python
#encoding:utf-8
# -*- coding: utf-8 -*-


import sys
import os
import shutil

def doConfigSetup(*args):
    #print 'testplugin config args', args
    print args[0]
    clientInfo = args[0]
    pluginList = clientInfo.plgins()
    print "pass"