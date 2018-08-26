import os,sys,stat
a=r'\\10.60.100.101'
#=r'E:\Dot'

#b=os.chmod(a,7)
b=os.path.exists(a)  #判断路径是否为链接
print (b)