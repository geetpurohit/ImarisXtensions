#
#
#  SurfacesSplit XTension  
#
#  Copyright Bitplane AG
#
#    <CustomTools>
#      <Menu>
#       <Item name="test" icon="Python3" tooltip="WE are testing">
#         <Command>Python3XT::test(%i)</Command>
#       </Item>
#      </Menu>
#    </CustomTools>

import sys 
import time
import colorama
colorama.init(autoreset=True)
import numpy as np	
import subprocess

sys.path.append("C:\Program Files\Bitplane\Imaris 9.8.0\XT\python3") # unique path to you 
sys.path.append("C:\Program Files\Bitplane\Imaris 9.8.0\Imaris.exe") # unique path to you 

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
		print(ids)
		time.sleep(2)
		sdl = []

		for i in range(len(ids)):
			sdl.append(vSurfaces.GetSurfaceDataLayout(i))

		
		time.sleep(2)
		print("\033[92m Printing Surface Data Layout Array \033[92m")
		print(sdl)
		print("\033[92m Finished Printing Surface Data Layout Array \033[92m")
		time.sleep(2)

		sdlarrfiltered = []
		comarray2 = []
		for i in range(len(ids)):
			if vSurfaces.GetSurfaceDataLayout(i).mSizeX < 2000: #filters out the small spots implement user
				continue
			sdlarrfiltered.append(vSurfaces.GetSurfaceDataLayout(i))
			comarray2.append(vSurfaces.GetCenterOfMass(i))

		print("Printig Comarray2 now:...")
		print(comarray2)		

		comarray = np.array(comarray2).squeeze()
		print("Printig Comarray now:...")
		print(comarray)
		time.sleep(10)
		comarrayleft = []
		comarrayright = []

		for i in range(len(comarray)):
			if comarray[i][0] < 92000:
				comarrayleft.append(comarray[i])
				continue
			comarrayright.append(comarray[i])
		
		print(comarrayright)
		print(comarrayleft)
		print("\033[92m Finished Printing COM array before sorting \033[92m")
		time.sleep(1)

		comarrayright.sort(reverse = False, key = lambda x : x[1])
		comarrayleft.sort(reverse = False, key = lambda x : x[1])

		print(comarrayright)
		print("\033[92m Finished Printing RCOM array after sorting \033[92m")
		print(comarrayleft)
		print("\033[92m Finished Printing LCOM array after sorting \033[92m")
		print(comarrayright[1])
		time.sleep(1)

		shincomarray = []
		for i in range(7):
			shincomarray.append(comarrayleft[i])
			shincomarray.append(comarrayright[i])
			continue

		print("\033[92m Printing SHINCOM array now \033[92m")
		print(shincomarray)
		print("\033[92m Printing filtered array now \033[92m")
		print(sdlarrfiltered)
		
		print("\033[92m Finished Printing Filtered Array! \033[92m")
		time.sleep(1)
		print("\033[92m Size of Filtered Array: \033[92m", len(sdlarrfiltered))

		time.sleep(1)

		#next task to get max x and y array from the new sdlarrfilter
		xsizearray, ysizearray, extendxsizeMaxarray = ([] for i in range(3))
		for i in sdlarrfiltered:
			xsizearray.append(i.mSizeX)
			ysizearray.append(i.mSizeY)
			extendxsizeMaxarray.append(i.mExtendMaxX)

			
		print('here is the xsize array:' , xsizearray)
		print('')
		print('\nhere is the ysize array:' , ysizearray)
		print('')
		print('\nhere is the extendXsizeMaxarray:' , extendxsizeMaxarray)
		print('')
		print('\n The Length of mExtendMaxX array is:L', len(extendxsizeMaxarray)) 
		print('')
		time.sleep(1)


		
		imagedataset = vImaris.GetImage(0)
		print("\033[92m Printing igmdtst now \033[92m")
		print(imagedataset)
		print('hhhhhhhhhhhhh')
		print(imagedataset.GetExtendMinX())
		time.sleep(10)

		maxX = max(xsizearray)
		maxY = max(ysizearray)
		z = len(sdlarrfiltered) #


		data = np.zeros((maxX, maxY, z, imagedataset.GetSizeC(), 1), dtype = np.float32) 

		print('maxX: ',maxX)
		print('maxY: ', maxY)
		print('z: ', z)
		print('',imagedataset.GetSizeC())
		time.sleep(10)

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


		x = int(sdlarrfiltered[0].mExtendMinX)
		y = int(sdlarrfiltered[0].mExtendMinY)
		z = int(sdlarrfiltered[0].mExtendMinZ)
	
		for i,id in enumerate(shincomarray): #use the sorted array and check if the indexes match the slice numbers
			
			vx1min = (id.mExtendMinX - xdatamin)/(vx)
			vy1min = (id.mExtendMinY - ydatamin)/(vy)
			vz1min = (id.mExtendMinZ - zdatamin)/(vz)
			voxel = vx * vy * vz

			print('Working on Surface:', i)
			for channel in range(0, 3):
				print('Working on Channel:', channel)
				data[0:id.mSizeX, 0:id.mSizeY, i, channel] = imagedataset.GetDataSubVolumeFloats(vx1min, vy1min, 0, channel, 0, id.mSizeX, id.mSizeY, 1) #gives data for 1 channel
		
		
		np.save("D:\Abraira Lab Research\Image Analysis\data", data)
		#data = np.load("D:\Abraira Lab Research\Image Analysis\data.npy")
		#data is ok here (don't know if contents are ok but will open in imaris to check after pushing the stack)

	except Exception:
		import traceback
		traceback.print_exc()
		input()
