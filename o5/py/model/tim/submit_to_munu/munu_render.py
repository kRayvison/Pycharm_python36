# #! /usr/bin/env python
# #coding=utf-8
# #written by liuqiang qq: 386936142

import subprocess
import os

if not os.path.exists(cg_output):
    os.makedirs(cg_output)

cmd = "\"%s\" -s %s -e %s -b %s -rd \"%s\"" % (
    cg_exe, start, end, byframe, cg_output)

if cg_render_layer:
    cmd += " -rl %s" % (cg_render_layer)

cmd += " \"%s\"" % (cg_file)

print "start Rayvision render: " + cmd
subprocess.call(cmd)
print "finished Rayvision render."
