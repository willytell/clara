import os
from BasicIO.nifti import readNifti, saveNifti
from BasicIO.filenameList import getFilenameList
from BasicImageProcessing.shift import shiftXY

######################## Input #########################################
databasePath = '/home/willytell/Desktop/LungCTDataBase/LIDC-IDRI/Nii_Vol'
ctPath = 'CT_nii'
ctmaskPath = 'CTmask_nii'
########################################################################

######################## Output ########################################
outputPath = '/home/willytell/Desktop/output/pipeline1/CTshiftedmask_nii'
shift_x = 2     # shift 2 px in axis x.
shift_y = 2     # shift 2 px in axis y.
########################################################################

print("Start.")

filename_list = getFilenameList(os.path.join(databasePath, ctmaskPath))

for filename in filename_list:
    _, mask_arr_xyz, metadata = readNifti(os.path.join(databasePath, ctmaskPath, filename))
    shifted_mask_arr_xyz = shiftXY(mask_arr_xyz, shift_x, shift_y)
    saveNifti(shifted_mask_arr_xyz, metadata, os.path.join(outputPath, filename))

print("Finish.")