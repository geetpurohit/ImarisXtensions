#
#
#  SurfacesSplit XTension  
#
#  Copyright Bitplane AG
#
#    <CustomTools>
#      <Menu>
#       <Item name="Hello" icon="Python3" tooltip="Hello.">
#         <Command>Python3XT::hello(%i)</Command>
#       </Item>
#      </Menu>
#    </CustomTools>

import sys, time, subprocess

import numpy as np
from numpy.core.numeric import moveaxis
from pystackreg import StackReg


sys.path.append("C:\Program Files\Bitplane\Imaris 9.8.0\XT\python3") # unique path to you 
sys.path.append("C:\Program Files\Bitplane\Imaris 9.8.0\Imaris.exe") # unique path to you


import ImarisLib
import Imaris

def hello(aImarisId):
    try:
        vImarisLib =  ImarisLib.ImarisLib()
        vImaris = vImarisLib.GetApplication(aImarisId)
    	
        vFactory = vImaris.GetFactory()
        aImarisIdd = aImarisId + 1 #'id101
        subprocess.Popen(["C:\Program Files\Bitplane\Imaris 9.8.0\Imaris.exe",'id' + str(aImarisIdd)])
        time.sleep(5)
        while True:	
            try:
                vImarisApp = vImarisLib.GetApplication(aImarisIdd)
                if(vFactory.IsApplication(vImarisApp)):
                    vImarisApp.SetVisible(True)
                    break
            except:
                continue



        
        print('set visible True') #i do this to set it not headless for now
        time.sleep(1)
        dataimage = np.load("D:\Abraira Lab Research\Image Analysis\data.npy") #i saved the computed data so i dont have to compute it every time
        
        sr = StackReg(StackReg.RIGID_BODY)
        temparray = np.moveaxis(dataimage,2,0) #z*y*x
        print(temparray.shape)
    
        tmats = sr.register_stack(temparray[:,:,:,0,0], reference = 'previous')

        for c in range(temparray.shape[3]):
            temparray[:,:,:,c,0] = sr.transform_stack(temparray[:,:,:,c,0], tmats = tmats)
        

        temparray = np.moveaxis(temparray, 0, 2) #switch z and x back


        print('dataset loaded')
        time.sleep(1)
        vDataSet = vImarisApp.GetFactory().CreateDataSet()  
        vDataSet.Create(Imaris.tType.eTypeUInt16,7583,2771,14,3,1)
        print('passed create')
        for c in range(3):
            for z in range(14):
                vDataSet.SetDataSliceFloats(temparray[:,:,z,c,0], z, c, 0) #should give an xy slice at given z at given c
        print('setdata pasassed')
        vImarisApp.SetDataSet(vDataSet)
        print('passed setdataset')
        vImarisApp.SetImage(0, vDataSet)
        print('passed setimage')
        print(vImarisApp.GetImage(0))
        time.sleep(2)
        vImarisApp.FileSave("D:\Abraira Lab Research\Image Analysis\result_allchannel_16bit.ims", "")
        print('done')
        time.sleep(5)

    except:
        import traceback
        traceback.print_exc()
        input()

    '''
    print(imagedataset.GetExtendMaxX())
    print(imagedataset.GetExtendMinY())
    print(imagedataset.GetExtendMaxY())	
    print(imagedataset.GetExtendMinZ())
    print(imagedataset.GetExtendMaxZ())
    '''
    time.sleep(15)

    return