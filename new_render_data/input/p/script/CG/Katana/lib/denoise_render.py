# /usr/bin/env python
import sys,os
denoise_com_id=sys.argv[1]
denoise_task_id=sys.argv[2]


denoise_Variance  = sys.argv[3]
denoise_Source = sys.argv[4]
denoise_outdir=sys.argv[5]
plugin_cfg=sys.argv[6]




denoise_root = "/opt/pixar/RenderManProServer-21.0/bin"
#kantan_root = "/home/ladaojeiang/yes"
#denoise --crossframe -v variance D:/td/denoise/Variance/image_variance.%04d.exr D:/td/denoise/Source/SC_KeyLight.%04d.exr --outdir D:/td/Source
#python '/root/Desktop/denoise_render.py'  123 456 '/mnt/projects/super_builder_tv/sequences/Seq03/Seq03_shot100/Comp/publish/elements/CH/MC_AC/CH_Variance/Final/image_variance.*.exr'  '/mnt/projects/super_builder_tv/sequences/Seq03/Seq03_shot100/Comp/publish/elements/CH/MC_AC/CH_KeyLight/Source/CH_KeyLight.*.exr' "/mnt/denoise/test"
print "-t 24"
os.system(r'%s/denoise --crossframe -v variance %s  %s --outdir %s -t 24' % (denoise_root,denoise_Variance,denoise_Source,denoise_outdir))
