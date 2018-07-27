#!/usr/bin/env python
#encoding:utf-8
# -*- coding: utf-8 -*-
r'''
    Usage:    c:\python34\python.exe "c:\script\py\Util\RunCmd.py" "[CMD(unicode)]"
'''
import sys
import os

print(sys.argv[0])
print('-------------------------start---------------------------')
cmd = sys.argv[1]
cmd = cmd.encode(sys.getfilesystemencoding()).decode('utf-8')
print(cmd)
ret = os.system(cmd)
if ret != 0:
    sys.exit(ret)
print('-------------------------end---------------------------')