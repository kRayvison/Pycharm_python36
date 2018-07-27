""" C4d killer """
#!/usr/bin/python
# -*- coding=utf-8 -*-
# Author: kaname
# QQ: 1394041054

import os

""" kill all c4d process """
kill_command = r'C:\script\new_py\CG\C4d\function\taskkill.exe /F /IM "CINEMA 4D.exe"'
os.system(kill_command)