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
#test

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


	# get the surfaces
	vSurfaces = vFactory.ToSurfaces(vImaris.GetSurpassSelection())

	if vSurfaces is None:
		print('Please select some surfaces in the surpass scene!')
		time.sleep(2)
		return

	# GET IDS SURFACES GET IDS () 
	ids = vSurfaces.GetIds()
	print(ids)
	time.sleep(1)

	#CODE STARRTS FROM HERE

	sdlarr = []
	for i in ids:	
		#print(vSurfaces.GetSurfaceDataLayout(i)) #works fine
		sdlarr.append(vSurfaces.GetSurfaceDataLayout(i))
	
	#print(vSurfaces.GetSurfaceDataLayout(1911))
	#print(vSurfaces.GetSurfaceDataLayout(1912)) #appears to be where this breaks. ???? what. assumption - there are 1912 surfaces in the cropped picture. 
	#new update after unifying surfaces -> pushed back ?? don't forget 2nd instance
	time.sleep(2)
	print("\033[92m Printing Surface Data Layout Array \033[92m")
	print(sdlarr)
	print("\033[92m Finished Printing Surface Data Layout Array \033[92m")
	time.sleep(2)

	sdlarrfiltered = []
	comarray2 = []
	for i in ids:
		if vSurfaces.GetSurfaceDataLayout(i).mSizeX < 2000: #filters out the small spots implement user
			continue
		sdlarrfiltered.append(vSurfaces.GetSurfaceDataLayout(i))
		comarray2.append(vSurfaces.GetCenterOfMass(i))

	comarray = np.array(comarray2).squeeze()
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
	print("\033[92m Size of Filtered Array: \033[92m", len(sdlarrfiltered)) #from 1912 surfaces to 15, thats an improvement !  YAY :3

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

	maxX = max(xsizearray)
	maxY = max(ysizearray)
	z = len(sdlarrfiltered) #


	data = np.zeros((maxX, maxY, z, imagedataset.GetSizeC(), 1), dtype = float) #

	xdatamax = imagedataset.GetExtendMaxX() - 7.17e4
	xdatamin = imagedataset.GetExtendMinX() - 7.17e4
	ydatamin = imagedataset.GetExtendMinY() - 2.73e4
	ydatamax = imagedataset.GetExtendMaxY() - 2.73e4
	zdatamin = imagedataset.GetExtendMinZ() + 1
	zdatamax = imagedataset.GetExtendMaxZ() + 1

	vx = (xdatamax - (xdatamin)) / (imagedataset.GetSizeX()) #for the offset
	vy = (ydatamax - (ydatamin)) / (imagedataset.GetSizeY())
	vz = (zdatamax - (zdatamin)) / (imagedataset.GetSizeZ())

	print(vx)
	print(vy)
	print(vz)
	print('here')
	time.sleep(2)

	tempvx1min = (sdlarrfiltered[0].mExtendMinX - xdatamin)/(vx)
	tempvy1min = (sdlarrfiltered[0].mExtendMinY - xdatamin)/(vy)
	tempvz1min = (sdlarrfiltered[0].mExtendMinZ - xdatamin)/(vz)


	x = int(sdlarrfiltered[0].mExtendMinX)
	y = int(sdlarrfiltered[0].mExtendMinY)
	z = int(sdlarrfiltered[0].mExtendMinZ)

	#print('subvolumefloats\n')
	#print(imagedataset.GetDataSubVolumeFloats(x-7.17e4,y-2.73e4, 0, 2, 0, sdlarrfiltered[0].mSizeX, sdlarrfiltered[0].mSizeY, 1))
	#time.sleep(10)




	for i,id in enumerate(sdlarrfiltered):
		
		vx1min = (id.mExtendMinX - 7.17e4 - xdatamin)/(vx)
		vy1min = (id.mExtendMinY - 2.73e4 - xdatamin)/(vy)
		vz1min = (id.mExtendMinZ + 1 - xdatamin)/(vz)

		voxel = vx * vy * vz
		print('Working on Surface:', i)
		for channel in range(0, imagedataset.GetSizeC()):
			print('Working on Channel:', channel)
			data[0:id.mSizeX, 0:id.mSizeY, i, channel] = imagedataset.GetDataSubVolumeFloats(vx1min, vy1min, 0, channel, 0, id.mSizeX, id.mSizeY, 1) #gives data for 1 channel


	aImarisIdd = aImarisId + 1 #'id101
	subprocess.Popen(["C:\Program Files\Bitplane\Imaris 9.8.0\Imaris.exe",'id' + str(aImarisIdd)]) #works but closes terminal 
	while True:	
		try:
			vImarisApp = vImarisLib.GetApplication(aImarisIdd)
			if(vFactory.IsApplication(vImarisApp)):
				vImarisApp.SetVisible(False)
				break
		except:
			continue
	print('Instance set headless')



	print(data)
	time.sleep(10)

	#horizontally they won't align, so prio will be for vertical. so wanna sort through y first and then x.
	# basic idea is to try to get documentation for surface filter location threshold
