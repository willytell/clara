"""
This pipeline2.py takes as input:
  1. the ROI image files, and
  2. the ROI shifted mask files (preprocessed by pipeline1.py),
  3. excel file with the list of image, mask, and diagnosis.

Using 1., 2., and 3., this code perform the features extraction for each pair of image and mask. The features are
extracted with PyRadiomic and saved in an excel file.

Sketch:
  https://drive.google.com/open?id=1UGpoQyLhae2KpVrn2mkni-gRBBzYJNZA
"""

import os
import pandas as pd
from BasicIO.nifti import readNifti
from BasicIO.filenameList import getImageMaskFilenamesAndDiagnosis
from BasicIO.saveFeatures import saveXLSX
from Features.radiomicFeatures import getPyRadiomicFeatures

######################## Input #########################################
databasePath = '/home/willytell/Desktop'

# Using ROI image and mask
roi_flag = True
ctPath = 'LungCTDataBase/LIDC-IDRI/Nii_Vol/CTRoi_nii'
ctmaskPath = 'output/pipeline1/CTRoishiftedmask_nii'

# Excel file that contains the list of filenames.
filename = '/home/willytell/Desktop/tcia_diagnosis.xls'
sheet_name='NoduleMalignancy'

# Params to configure the feature extractor.
paramPath = os.path.join('config', 'Params.yaml')
########################################################################

######################## Output ########################################
outputPath = '/home/willytell/Desktop/output/pipeline2'
extracted_features = os.path.join(outputPath, 'extractedFeatures.xlsx')
########################################################################


print("Start.")

# Get the list of tuple: (image and mask) in X, and the diagnosis (0=benign, 1=malign) in y.
X, y = getImageMaskFilenamesAndDiagnosis(databasePath, ctPath, ctmaskPath, filename, sheet_name, roi_flag)

mydict = []   # Create an empty list.

for index in range(0, len(X)):
    imageName = X[index][0]     # Full path to the image.
    maskName = X[index][1]      # Full path to the mask.
    y_label = y[index]          # Diagnosis: 0=benign, 1=malign.

    imageITK, image_arr_xyz, _ = readNifti(imageName)
    maskITK, mask_arr_xyz, mask_metadata = readNifti(maskName)

    # Image and mask must have the same volume shape.
    assert image_arr_xyz.shape == mask_arr_xyz.shape, "Error: image and mask shape must match!"

    # As we are working with mask's ROI, the segmentation label always is: 0 (background) or 1 (foreground).
    # For this reason, we are going to compute radiomics from mask ROIs that have only one foreground region.
    segmentation_label = 1

    # Feature extraction.
    od = getPyRadiomicFeatures(imageName, maskName, imageITK, maskITK, segmentation_label, y_label, paramPath)
    mydict.append(od)


df = pd.DataFrame.from_dict(mydict)  # pd.DataFrame.from_records(mydict)

# Save the features to an Excel file.
saveXLSX(df, extracted_features, sheet_name='Sheet1')

print("\nFinish.")