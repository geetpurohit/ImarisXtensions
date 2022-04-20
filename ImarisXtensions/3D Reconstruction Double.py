#
#
#  SurfacesSplit XTension  
#
#  Copyright Bitplane AG
#
#    <CustomTools>
#      <Menu>
#       <Item name="3D Reconstruction: Double" icon="Python3" tooltip="3D Reconstruction for bi-columnal spinal cord slices">
#         <Command>Python3XT::test(%i)</Command>
#       </Item>
#      </Menu>
#    </CustomTools>

import sys 
import time
import colorama
colorama.init(autoreset=True)
import numpy as np	

sys.path.append("C:\Program Files\Bitplane\Imaris x64 9.7.2\XT\python3") # unique path to you 
sys.path.append("C:\Program Files\Bitplane\Imaris x64 9.7.2\Imaris.exe") # unique path to you 

import ImarisLib
	
def test(aImarisId):

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
	try: 
			
		# Get the Surfaces (Each Surface has a unique Surface Index and a Surface ID)
		vSurfaces = vFactory.ToSurfaces(vImaris.GetSurpassSelection())

		if vSurfaces is None:
			print('Please select some surfaces in the surpass scene!')
			time.sleep(2)
			return

		# GET IDS SURFACES GET IDS () 
		ids = vSurfaces.GetIds()
		sdl = [] #Surface Data Layout Array

		for i in range(len(ids)):
			sdl.append(vSurfaces.GetSurfaceDataLayout(i))

		print("\033[92m Printing Surface Data Layout Array \033[92m")
		print(sdl)
		print("\033[92m Finished Printing Surface Data Layout Array \033[92m")
		time.sleep(200)

		sdlarrfilteredleft = []
		sdlarrfilteredright = []
		
		#sorting is tricky but we know that vertical hiearchy always follows. So what we do is halve -> sort L+R -> merge
		#it is important to note that this only works for Double Slides, for single Slides you need to modify this
		
		imgmidpoint = (vImaris.GetImage(0).GetExtendMaxX() - vImaris.GetImage(0).GetExtendMinX())/2 + vImaris.GetImage(0).GetExtendMinX()

		for i in range(len(ids)):
			if vSurfaces.GetSurfaceDataLayout(i).mSizeX < (0.1 * vImaris.GetImage(0).GetSizeX()): #we dont want to worry about anything smaller than 2000 microns
				continue

			if vSurfaces.GetSurfaceDataLayout(i).mExtendMaxX < imgmidpoint: #halfway point
				sdlarrfilteredleft.append(vSurfaces.GetSurfaceDataLayout(i))
			
			else:
				sdlarrfilteredright.append(vSurfaces.GetSurfaceDataLayout(i))
			
		
		sdlarrfilteredright.sort(reverse = True, key = lambda x : x.mExtendMaxY)
		sdlarrfilteredleft.sort(reverse = True, key = lambda x : x.mExtendMaxY)



		print(sdlarrfilteredright)
		print('finished printing sdl array right')
		print(sdlarrfilteredleft)
		print('finished printing sdl array left')


		sdl_filtered_sorted = []
		for i in range(len(sdlarrfilteredleft)):
			sdl_filtered_sorted.append(sdlarrfilteredleft[i])
			sdl_filtered_sorted.append(sdlarrfilteredright[i])
		
		print(sdl_filtered_sorted)


		#next task to get max x and y array from the new sdlarrfilter
		xsizearray, ysizearray, extendxsizeMaxarray = ([] for i in range(3))
		for i in sdl_filtered_sorted:
			xsizearray.append(i.mSizeX)
			ysizearray.append(i.mSizeY)
			extendxsizeMaxarray.append(i.mExtendMaxX)

		'''
		print('here is the xsize array:' , xsizearray)
		print('')
		print('\nhere is the ysize array:' , ysizearray)
		print('')
		print('\nhere is the extendXsizeMaxarray:' , extendxsizeMaxarray)
		print('')
		print('\n The Length of mExtendMaxX array is:L', len(extendxsizeMaxarray)) 
		print('')
		time.sleep(1)
		'''

		
		imagedataset = vImaris.GetImage(0)
		print("\033[92m Printing igmdtst now \033[92m")
		print(imagedataset)
		print(imagedataset.GetExtendMinX())
		time.sleep(1)

		maxX = max(xsizearray)
		maxY = max(ysizearray)
		z = len(sdl_filtered_sorted)
		h = len(sdl_filtered_sorted)*vz #height of stack

		data = np.zeros((maxX, maxY, z, imagedataset.GetSizeC(), 1), dtype = np.float32) 

		print('maxX: ',maxX)
		print('maxY: ', maxY)
		print('z: ', z)
		print('',imagedataset.GetSizeC())
		time.sleep(1)

		xdatamin = imagedataset.GetExtendMinX()
		xdatamax = imagedataset.GetExtendMaxX()
		ydatamin = imagedataset.GetExtendMinY()
		ydatamax = imagedataset.GetExtendMaxY()
		zdatamin = imagedataset.GetExtendMinZ()
		zdatamax = imagedataset.GetExtendMaxZ()

		vx = (xdatamax - xdatamin) / (imagedataset.GetSizeX()) 
		vy = (ydatamax - ydatamin) / (imagedataset.GetSizeY())
		vz = (zdatamax - zdatamin) / (imagedataset.GetSizeZ())

		print(vx)
		print(vy)
		print(vz)
		print('here')
		time.sleep(2)


		x = int(sdl_filtered_sorted[0].mExtendMaxX)
		y = int(sdl_filtered_sorted[0].mExtendMaxY)
		z = int(sdl_filtered_sorted[0].mExtendMaxZ)
	
		for i,id in enumerate(sdl_filtered_sorted): #use the sorted array and check if the indexes match the slice numbers
			
			vx1min = (id.mExtendMinX - xdatamin)/(vx)
			vy1min = (id.mExtendMinY - ydatamin)/(vy)
			vz1min = (id.mExtendMinZ - zdatamin)/(vz)
			voxel = vx * vy * vz

			print('Working on Surface:', i)
			for channel in range(0, 3):
				print('Working on Channel:', channel)
				data[0:id.mSizeX, 0:id.mSizeY, i, channel] = imagedataset.GetDataSubVolumeFloats(vx1min, vy1min, vz1min, channel, 0, id.mSizeX, id.mSizeY, 1) #gives data for 1 channel
		
		
		np.save("N:\Geet\data2.npy", data)
		#data = np.load("D:\Abraira Lab Research\Image Analysis\data.npy")

	except Exception:
		import traceback
		traceback.print_exc()
		input()
