import logging
import os
import sys
import subprocess
import string
import logging
import time
import shutil
from RenderBase import RenderBase 
from RenderMax import *
from RenderMaya import *
from RenderHoudini import *
from RenderC4D import *
from Merge import *
from Preprocess import *
from RenderLightWave import *
from RenderSoftImage import *
from RenderBlender import *
from RenderVray import *
from RenderMrstand import *
from RenderSketchUp import *
from RenderVue import *
from RenderClarisse import *
from RenderKeyShot import *
from RenderOctaneRender import *
from MayaPre import *

class RenderAction():
	def __init__(self,**paramDict):
		cgName=paramDict['G_CG_NAME']
		print 'cgName=================='+cgName
		exec('RenderAction.__bases__=('+cgName+',)')
		exec(cgName+'.__init__(self,**paramDict)')
	'''
	def RBrender(self):#Render command
		print 'RenderAction..max...render....'
	'''
#-----------------------main-------------------------------
def main(**paramDict):
	render=RenderAction(**paramDict)
	print 'G_POOL_NAME___'+render.G_POOL
	render.RBexecute()