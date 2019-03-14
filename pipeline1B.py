# -*- coding: utf-8 -*-
"""
This 'pipeline1B.py' compute the labels from the masks and obtain a list of ROIs. Then use these ROIs to save
the image and the mask.

Input:
  1. list of patient in an excel file.
  2. masks directory which already are shifted from pipeline1A.py,
  3. images directory.

Output:
  1. save image's ROIS,
  2. save mask's ROI.
"""

import os
import numpy as np
from BasicIO.nifti import readNifti, saveNifti
from BasicIO.filenameList import getListFromPatientList
from BasicImageProcessing.shift import labeling, getROIList

######################## Input #########################################
databasePath = '/home/willytell/Desktop'

# Using ROI image and mask
roi_flag = False
ctPath = 'LungCTDataBase/LIDC-IDRI/Nii_Vol/CT_nii'
ctmaskPath = 'output/pipeline1A/CTshiftedmask_nii'

# roi_flag = True
# ctPath = 'LungCTDataBase/LIDC-IDRI/Nii_Vol/CTRoi_nii'
# ctmaskPath = 'output/pipeline1A/CTRoishiftedmask_nii'


# Excel file that contains the list of filenames.
filename = '/home/willytell/Desktop/tcia_diagnosis_25_01_2019.xls'
sheet_name='NoduleMalignancy'
########################################################################

######################## Output ########################################
output_ctPath = '/home/willytell/Desktop/output/pipeline1B/CTRoi_nii'
output_ctmaskPath = '/home/willytell/Desktop/output/pipeline1B/CTRoimask_nii'
########################################################################


print("Start.")

# Obtain the list of names of the images and masks.
image_list, mask_list, _ = getListFromPatientList(databasePath, ctPath, ctmaskPath, filename, sheet_name)

print("The length of image_list is {} and mask_list is {}.".format(len(image_list), len(mask_list)))

assert len(image_list)==len(mask_list), "Length of image_list and mask_list must be the same."

for index in range(0, len(mask_list)):
    imageName = os.path.join(databasePath, ctPath, image_list[index])       # full path to the image
    maskName = os.path.join(databasePath, ctmaskPath, mask_list[index])     # full path to the mask

    # Read image and mask.
    imageITK_xyz, image_arr_xyz, image_metadata = readNifti(imageName)
    maskITK_xyz, mask_arr_xyz, mask_metadata = readNifti(maskName)

    # Before the shift operation, the original image and original mask must have the same volume shape.
    assert image_arr_xyz.shape == mask_arr_xyz.shape, "Error: image and mask shape must match!"

    # Find the labels in the volume.
    labeled_mask_arr_xyz, ncomponents = labeling(mask_arr_xyz, structural_element_shape=(3,3,3))
    print("In the mask {} there is(are) {} label(s).".format(maskName, ncomponents))

    # Find each ROI in the volume.
    roi_list = getROIList(labeled_mask_arr_xyz, ncomponents)
    print("{} ROIs were found.".format(len(roi_list)))

    assert ncomponents == len(roi_list), "Error, ncomponents and roi_list's length mus be the same."

    # Considering the label number, save each image and mask according to its ROI.
    for num_label, one_roi in enumerate(roi_list, start=1):  # 0 corresponds to background

        # LIDC-IDRI-0124_GT1.nii.gz  -> LIDC-IDRI-0124_GT1_1.nii.gz
        # LIDC-IDRI-0124_GT1_Mask.nii.gz -> LIDC-IDRI-0124_GT1_1_Mask.nii.gz

        image_fname = image_list[index].split('_')[0] + '_GT1_' + str(num_label) + '.nii.gz'
        mask_fname = mask_list[index].split('_')[0] + '_GT1_' + str(num_label) + '_Mask.nii.gz'

        roi_image_xyz = np.copy(image_arr_xyz[one_roi[0]:one_roi[1] + 1,
                                              one_roi[2]:one_roi[3] + 1,
                                              one_roi[4]:one_roi[5] + 1])

        roi_mask_xyz = np.copy(mask_arr_xyz[one_roi[0]:one_roi[1] + 1,
                                            one_roi[2]:one_roi[3] + 1,
                                            one_roi[4]:one_roi[5] + 1])

        # save the image
        saveNifti(roi_image_xyz, image_metadata, os.path.join(output_ctPath, image_fname))

        # save the mask
        saveNifti(roi_mask_xyz, mask_metadata, os.path.join(output_ctmaskPath, mask_fname))

print("Finish.")