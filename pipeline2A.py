"""
This pipeline2A.py extract features.
Input:
  1. List of patients in an excel file,
  2. image and mask directories.

Output:
  1. extracted features in an excel file for train set.
  2. extracted features in an excel file for test set.
"""

import os
import pandas as pd
import numpy as np
import SimpleITK as sitk
from BasicIO.nifti import readNifti, saveNifti
from BasicIO.filenameList import getFilterList, getListFromPatientList
from BasicIO.saveFeatures import saveXLSX
from Features.radiomicFeatures import getPyRadiomicFeatures

######################## Input #########################################
databasePath = '/home/willytell/Desktop/LungCTDataBase/Experimentation'
#databasePath = '/home/willytell/Desktop/output/pipeline1B'

# Using ROI image and mask
roi_flag = True
ctPath = 'CTRoi_nii'
ctmaskPath = 'CTRoimask_nii'


# Excel file that contains the list of filenames.
filename = '/home/willytell/Desktop/tcia_diagnosis_25_01_2019.xls'
sheet_name='NoduleMalignancy'

# Params to configure the feature extractor.
paramPath = os.path.join('config', 'Params.yaml')
########################################################################

######################## Output ########################################
outputPath = '/home/willytell/Desktop/output/pipeline2A/Without_Image_Estandardization'
extracted_features_train = os.path.join(outputPath, 'extractedFeatures_Train.xlsx')
extracted_features_test = os.path.join(outputPath, 'extractedFeatures_Test.xlsx')
########################################################################


print("Start.")

# Filter the traning cases
df_train = getFilterList(filename, sheet_name, set_flag=1)

# Filter the testing cases
df_test = getFilterList(filename, sheet_name, set_flag=0)


######################################## TRAIN CASES ##########################################################

mydict = []

for index in range(len(df_train)):
    basename = df_train.iloc[index]['Patient ID']
    noduleID = df_train.iloc[index]['NoduleID']
    noduleDiagnosis = df_train.iloc[index]['Nodule Diagnosis']
    patientDiagnosis = df_train.iloc[index]['Patient Diagnosis']

    imageName = basename + '_GT1_' + noduleID.astype(str) + '.nii.gz'
    maskName = basename + '_GT1_' + noduleID.astype(str) + '_Mask.nii.gz'

    print("imageName, maskName, noduleDiagnosis, patientDiagnosis")
    print(imageName, maskName, noduleDiagnosis, patientDiagnosis)

    imageITK_xyz, image_arr_xyz, image_metadata = readNifti(os.path.join(databasePath, ctPath, imageName))
    maskITK_xyz, mask_arr_xyz, mask_metadata = readNifti(os.path.join(databasePath, ctmaskPath, maskName))

    # Image and mask must have the same volume shape.
    assert image_arr_xyz.shape == mask_arr_xyz.shape, "Error: image and mask shape must match!"

    # # Standardize the image values between [0, 255]
    # standardized_image_arr_xyz = (image_arr_xyz - image_arr_xyz.min()) / (image_arr_xyz.max() - image_arr_xyz.min()) * 255.0
    #
    # # transforming from (x,y,z) to (z,y,x).
    # standardized_image_arr_zyx = np.transpose(standardized_image_arr_xyz, (2, 1, 0))
    # #saveNifti(standardized_image_arr_xyz, image_metadata, os.path.join(outputPath, imageName))   # <-- check here!
    # new_imageITK_xyz = sitk.GetImageFromArray(standardized_image_arr_zyx)
    #
    # # Setting properties
    # new_imageITK_xyz.SetOrigin(image_metadata.origin)
    # new_imageITK_xyz.SetDirection(image_metadata.direction)
    # new_imageITK_xyz.SetSpacing(image_metadata.spacing)

    # As we are working with mask's ROI, the segmentation label always is: 0 (background) or 1 (foreground).
    # For this reason, we are going to compute radiomics from mask ROIs that have only one foreground region.
    segmentation_label = 1

    # Feature extraction.
    od = getPyRadiomicFeatures(imageName, maskName, imageITK_xyz, maskITK_xyz, segmentation_label, noduleDiagnosis, patientDiagnosis, paramPath)
    mydict.append(od)

df_tmp1 = pd.DataFrame.from_dict(mydict)  # pd.DataFrame.from_records(mydict)

# Save the features to an Excel file.
saveXLSX(df_tmp1, extracted_features_train, sheet_name='Sheet1')




######################################## TEST CASES ##########################################################

tmp = os.path.join(outputPath, 'temporary_file.xlsx')
saveXLSX(df_test, tmp, sheet_name='Sheet1')

image_list, mask_list, info_list = getListFromPatientList(databasePath, ctPath, ctmaskPath, tmp, sheet_name='Sheet1')

assert len(image_list)==len(mask_list), "Length of image_list and mask_list must be the same."

mydict = []

for index in range(0, len(mask_list)):
    imageName = os.path.join(databasePath, ctPath, image_list[index])       # full path to the image
    maskName = os.path.join(databasePath, ctmaskPath, mask_list[index])     # full path to the mask
    noduleDiagnosis, patientDiagnosis = info_list[index]

    imageITK_xyz, image_arr_xyz, image_metadata = readNifti(imageName)
    maskITK_xyz, mask_arr_xyz, mask_metadata = readNifti(maskName)

    # Image and mask must have the same volume shape.
    assert image_arr_xyz.shape == mask_arr_xyz.shape, "Error: image and mask shape must match!"

    # # Standardize the image values between [0, 255]
    # standardized_image_arr_xyz = (image_arr_xyz - image_arr_xyz.min()) / (image_arr_xyz.max() - image_arr_xyz.min()) * 255.0
    #
    # # transforming from (x,y,z) to (z,y,x).
    # standardized_image_arr_zyx = np.transpose(standardized_image_arr_xyz, (2, 1, 0))
    # #saveNifti(standardized_image_arr_xyz, image_metadata, os.path.join(outputPath, imageName))   # <-- check here!
    # new_imageITK_xyz = sitk.GetImageFromArray(standardized_image_arr_zyx)
    #
    # # Setting properties
    # new_imageITK_xyz.SetOrigin(image_metadata.origin)
    # new_imageITK_xyz.SetDirection(image_metadata.direction)
    # new_imageITK_xyz.SetSpacing(image_metadata.spacing)

    # As we are working with mask's ROI, the segmentation label always is: 0 (background) or 1 (foreground).
    # For this reason, we are going to compute radiomics from mask ROIs that have only one foreground region.
    segmentation_label = 1

    # Feature extraction.
    od = getPyRadiomicFeatures(imageName.split('/')[-1], maskName.split('/')[-1], imageITK_xyz, maskITK_xyz, segmentation_label, noduleDiagnosis, patientDiagnosis, paramPath)
    mydict.append(od)

df_tmp2 = pd.DataFrame.from_dict(mydict)  # pd.DataFrame.from_records(mydict)

# Save the features to an Excel file.
saveXLSX(df_tmp2, extracted_features_test, sheet_name='Sheet1')

print("\nFinish.")