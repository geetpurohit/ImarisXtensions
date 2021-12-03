#
#
#  SurfacesSplit XTension  
#
#  Copyright Bitplane AG
#
#    <CustomTools>
#      <Menu>
#       <Item name="Sup!" icon="Python3" tooltip="WE are testing">
#         <Command>Python3XT::hello(%i)</Command>
#       </Item>
#      </Menu>
#    </CustomTools>

import sys 
import time
import numpy
import subprocess

sys.path.append("C:\Program Files\Bitplane\Imaris 9.8.0\XT\python3") # unique path to you 
sys.path.append("C:\Program Files\Bitplane\Imaris 9.8.0\Imaris.exe") # unique path to you 

import ImarisLib


def GetSercer

def hello(aImarisId):
	# Create an ImarisLib object
	vImarisLib = ImarisLib.ImarisLib()

	# Get an imaris object with id aImarisId
	vImaris = vImarisLib.GetApplication(aImarisId)

	# Check if the object is valid
	if vImaris is None:
		print('Could not connect to Imaris!')
		# Sleep 2 seconds to give the user a chance to see the printed message
		time.sleep(2)
		return

	# Get the factory
	vFactory = vImaris.GetFactory()

	# Get the surpass scene
	vSurpassScene = vImaris.GetSurpassScene()

	# This XTension requires a loaded dataset
	if vSurpassScene is None:
		print('Please create some Surfaces in the Surpass scene!')
		time.sleep(2)
		return

	# get the surfaces
	vSurfaces = vFactory.ToSurfaces(vImaris.GetSurpassSelection())

	if vSurfaces is None:
		print('Please select some surfaces in the surpass scene!')
		time.sleep(2)
		return
		
# GET IDS SURFACES GET IDS () 
	ids = vSurfaces.GetIds()
	# build up dictionary to get out bases to sort from left to right and top to bottom 
	# 1 > rectangle 
	tempdict = {id:vSurfaces.GetSurfaceLayout(id) for id in vSurfaces.GetIds()}
	print(tempdict)
	time.sleep(5)

	# sort left right top to bot 
	max_sizex = max([v.mSizeX for v in tempdict.values()])
	max_sizey = max([v.mSizeY for v in tempdict.values()])

	
	imagedataset = vImaris.GetImage(0)
	type = imagedataset.GetType()

	numpy.zeros([max_sizex, max_sizey, len(ids), imagedataset.GetSizeC()], dtype=convert_etype_numtype(type))
	# GetDataSubSliceBytes()


def convert_etype_numtype(type):
	if type is vImarisLib.tType.eTypeUInt8:
		return numpy.uint8

	if type is vImarisLib.tType.eTypeUInt16:
		return numpy.uint16

	if type is vImarisLib.tType.eTypeUIntFloat:
		return numpy.float32