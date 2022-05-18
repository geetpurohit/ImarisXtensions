3DREC (3 Dimensional Reconstruction) is a Python Xtension to IMARIS to take bi-columnar spinal cord .ims files and stacks the slices to get a 3D reconstruction of the spinal cord.

# Getting Started: Installation

Download and unzip the code. ```setup.py``` will indicate the modules/packages that are about to be installed, in case they are not present. It should be enough to write: ```$ pip install .``` 

# Getting Started: Prerequisites

There are some pre-requisites before getting started. Note that some of the system requirements are the bare minimum, since any system specifications below the listed ones is not guaranteed to support this implementation:

1. Oxford Imaris (x64 9.7.2)
2. 2 ```.ims``` files (bi-columnar, separated) for each reconstruction, visualized below 
3. Python Editor of your choice (I use VSCode)
4. Processor: Intel(R) Xeon(R) W-2235 3.80GHz
5. RAM: 32.0 GB
6. Storage: Atleast 1TB, preferably on SSD for faster execution

# 3D Reconstruction: Overview

The purpose of this implementation is to visualize lesion sites in 3 Dimensions, to infer biological and neurological effects from different lab procedures. We start off with having two .ims files: 

![explorer](https://user-images.githubusercontent.com/68968629/168905811-db79815e-010b-48c9-a7b0-04318f96898a.JPG)

An .ims files looks something like this:


![sample ims file](https://user-images.githubusercontent.com/68968629/168905842-e0040874-4636-4b08-8370-27fab98a6459.JPG)


Then we proceed to use the Python code to:

* convert the .ims files into numpy arrays, preserving all the channels 
* combine both the arrays into one, keeping in mind the original Z heights
* push the data into a new IMARIS instance (stacking it as a rigid body).

# 3D Reconstruction: Result

Having two .ims images for the spinal cord, we can expect the final output to be something like this:

![res](https://user-images.githubusercontent.com/68968629/168905856-8c28a495-1fdd-4b86-932d-1d4827e38875.gif)


*Note that this result is exagerated for demonstration purposes (thickness, color, etc).*

# Notes

* This implementation can take ~1-2 hours depending on dataset size
* Make sure to have a combined npy file before running this script
* Make sure to have your npy file and save path on the 'local' drive and not on a cloud share, since that will increase the execution time by a lot
* If any script crashes instantly on execution in IMARIS, check if you did not rename the script, the name should be an invariant throughout the script (including the script name).
* You can change your transformation from RIGID to AFFINE or BILINEAR to get the best looking result
* The result is variant, subject to initial conditions such as .ims file accuracy, python methods of ```VolumeFloats``` versus ```SetDataSliceFloats```, etc.


