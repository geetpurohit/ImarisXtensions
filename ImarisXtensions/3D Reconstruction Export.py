#
#
#  SurfacesSplit XTension  
#
#  Copyright Bitplane AG
#
#    <CustomTools>
#      <Menu>
#       <Item name="3D Reconstruction: Export" icon="Python3" tooltip="Load the data into a new IMARIS instance and export as an .ims file">
#         <Command>Python3XT::hello(%i)</Command>
#       </Item>
#      </Menu>
#    </CustomTools>

import sys, time, subprocess

import numpy as np
from numpy.core.numeric import moveaxis
from pystackreg import StackReg


sys.path.append("C:\Program Files\Bitplane\Imaris x64 9.7.2\XT\python3") # unique path to you 
sys.path.append("C:\Program Files\Bitplane\Imaris x64 9.7.2\Imaris.exe") # unique path to you


import ImarisLib
import Imaris

def hello(aImarisId):
    try:
        vImarisLib =  ImarisLib.ImarisLib()
        vImaris = vImarisLib.GetApplication(aImarisId)
    	
        vFactory = vImaris.GetFactory()
        aImarisIdd = aImarisId + 1 #'id101
        subprocess.Popen(["C:\Program Files\Bitplane\Imaris x64 9.7.2\Imaris.exe",'id' + str(aImarisIdd)])
        time.sleep(5)
        while True:	
            try:
                vImarisApp = vImarisLib.GetApplication(aImarisIdd)
                if(vFactory.IsApplication(vImarisApp)):
                    vImarisApp.SetVisible(False)
                    break
            except:
                continue

        
        print('set visible False') #headless
        dataimage = np.load("D:\Geet\datasingleslice.npy") #load the saved data
        sr = StackReg(StackReg.RIGID_BODY)
        temparray = np.moveaxis(dataimage,2,0) #z*y*x
        tmats = sr.register_stack(temparray[:,:,:,0,0], reference = 'previous')


        for c in range(temparray.shape[3]):
            temparray[:,:,:,c,0] = sr.transform_stack(temparray[:,:,:,c,0], tmats = tmats)
        

        temparray = np.moveaxis(temparray, 0, 2) #switch z and x back => x*y*z
        
        print("The shape of the original array was: ", np.shape(temparray))
        y = np.pad(temparray, ((1000,1000),(500,500),(0,0),(0,0),(0,0))) #don't forget to generalize this
        print("The shape of the padded array is: ", np.shape(y)) #welness check
        shapearray = [z for z in np.shape(y)]

        print('dataset loaded') #wait until Python supports .wav sounds in codebase, then add gun reload sound at this execution
        vDataSet = vImarisApp.GetFactory().CreateDataSet()  
        vDataSet.Create(Imaris.tType.eTypeFloat,shapearray[0],shapearray[1],shapearray[2],shapearray[3],shapearray[4]) #use nparray shape to generalize it
        #use SetExtendMin and Max from imagedata(0)
        #use vxsz for EDL STATS
        print('passed create')
        for c in range(3):
            for z in range(7):                                                                  
                vDataSet.SetDataSliceFloats(y[:,:,z,c,0], z, c, 0) #should give an xy slice at given z at given c
        print('setdata passed')        
        vImarisApp.SetDataSet(vDataSet)
        print('passed setdataset')
        vImarisApp.SetImage(0, vDataSet)
        print('passed setimage')
        vImarisApp.GetDataSet().SetExtendMaxZ(28)
        print(vImarisApp.GetImage(0))
        vImarisApp.FileSave("N:\Geet\KeckCenterSingle50PercentPaddingextent.ims", "")
        print('done')
        time.sleep(5)

    except:
        import traceback
        traceback.print_exc()
        input()

    return