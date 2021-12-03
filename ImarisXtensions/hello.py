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

import sys, time


sys.path.append("C:\Program Files\Bitplane\Imaris 9.8.0\XT\python3") # unique path to you 
sys.path.append("C:\Program Files\Bitplane\Imaris 9.8.0\Imaris.exe") # unique path to you


import ImarisLib

def hello(aImarisId):
    vImarisLib = ImarisLib.ImarisLib()
    vImaris = vImarisLib.GetApplication(aImarisId)
    imagedataset = vImaris.GetImage(0)
    print(imagedataset)
    x = imagedataset.GetSizeC()
    print(x)

    
    '''
    print(imagedataset.GetExtendMaxX())
    print(imagedataset.GetExtendMinY())
    print(imagedataset.GetExtendMaxY())	
    print(imagedataset.GetExtendMinZ())
    print(imagedataset.GetExtendMaxZ())
    '''
    time.sleep(15)

    return