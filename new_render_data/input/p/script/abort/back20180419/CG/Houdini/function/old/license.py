#!/usr/bin/env python
#encoding:utf-8
# -*- coding: utf-8 -*-
import os,sys,time,re
import subprocess
from HoudiniUtil import HoudiniUtil
from HoudiniThread import HoudiniThread
def aaa():
    try:
        HoudiniUtil.SetServer("16","10.60.96.203")
    except Exception, e:
        print e

    
def vvv():
    print ("vvvvvvvvvv")
def bbb():
    print("bbbbbbbbbbbbbbbb")
ff = {"aaa":[aaa,""],"vvv":[vvv,""],"bbb":[bbb,""]}
HoudiniThread.JoinThread(HoudiniThread.StartThread(HoudiniThread.CreatThread(ff)))