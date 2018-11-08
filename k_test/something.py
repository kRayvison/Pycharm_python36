import os
aaa='2017'
cmd_str = r"D:\Autodesk\Maya%s\bin\maya.exe" % (aaa)
print (cmd_str)
#os.system('"' + cmd_str + '"')
os.startfile('"' + cmd_str + '"')
print ('ahaha')