"""
This 'pipeline1A.py' applies a shift operation only for mask file. The shift operation consists in the displacement of
2 pixels of the all values in both axis x an y. Then save the resultant shifted mask in the directory, which is
indicated by the outputPath variable, it preserves the same file name.

Sketch:

"""

import os
from BasicIO.nifti import readNifti, saveNifti
from BasicIO.filenameList import getListFromPatientList
from BasicImageProcessing.shift import shiftXY

######################## Input #########################################
databasePath = '/home/willytell/Desktop/LungCTDataBase/LIDC-IDRI/Nii_Vol'

# Using ROI image and mask
roi_flag = False
ctPath = 'CT_nii'
ctmaskPath = 'CTmask_nii'
#roi_flag = True
# ctPath = 'CTRoi_nii'
# ctmaskPath = 'CTRoimask_nii'

# Excel file that contains the list of filenames.
filename = '/home/willytell/Desktop/tcia_diagnosis_25_01_2019.xls'
sheet_name='NoduleMalignancy'
########################################################################

######################## Output ########################################
outputPath = '/home/willytell/Desktop/output/pipeline1A/CTshiftedmask_nii'
#outputPath = '/home/willytell/Desktop/output/pipeline1A/CTRoishiftedmask_nii'
shift_x = 2     # shift 2 px in axis x.
shift_y = 2     # shift 2 px in axis y.
########################################################################


print("Start.")

#
image_list, mask_list, _ = getListFromPatientList(databasePath, ctPath, ctmaskPath, filename, sheet_name)

print("The length of image_list is {} and mask_list is {}.".format(len(image_list), len(mask_list)))

assert len(image_list)==len(mask_list), "Length of image_list and mask_list must be the same."

for index in range(0, len(mask_list)):
    imageName = os.path.join(databasePath, ctPath, image_list[index])       # full path to the image
    maskName = os.path.join(databasePath, ctmaskPath, mask_list[index])     # full path to the mask

    imageITK, image_arr_xyz, _ = readNifti(imageName)
    maskITK, mask_arr_xyz, mask_metadata = readNifti(maskName)

    # Before the shift operation, the original image and original mask must have the same volume shape.
    assert image_arr_xyz.shape == mask_arr_xyz.shape, "Error: image and mask shape must match!"

    # Shift the mask values.
    shifted_mask_arr_xyz = shiftXY(mask_arr_xyz, shift_x, shift_y)

    # After the shift operation, the original image and the shifted mask must have the same volume shape.
    assert image_arr_xyz.shape == shifted_mask_arr_xyz.shape, "Error: image and mask shape must match!"

    # Save the shifted mask preserving the original mask filename.
    saveNifti(shifted_mask_arr_xyz, mask_metadata, os.path.join(outputPath, maskName.split('/')[-1]))

print("Finish.")