"""
This pipeline3.py uses as input
   1. original image files
   2. shifted and labeled mask files, (preprocessed by pipeline1.py and pipeline2.py respectively).
   3. tcia_diagnosis.xls, which contains the diagnosis of some nodules.

Using 1., 2. and 3. this code calculate the features extraction with the PyRadiomic package and save them
in an excel file.

"""

import os
import numpy as np
import pandas as pd
from BasicIO.nifti import readNifti
from BasicIO.filenameList import getImageMaskFilenamesAndDiagnosis
from BasicIO.saveFeatures import saveXLSX
from Features.radiomicFeatures import getPyRadiomicFeatures

######################## Input #########################################
databasePath = '/home/willytell/Desktop'
ctPath = 'LungCTDataBase/LIDC-IDRI/Nii_Vol/CT_nii'
ctmaskPath = 'output/pipeline2/CTlabeledshiftedmask_nii'
filename = '/home/willytell/Desktop/tcia_diagnosis.xls'
sheet_name = 'NoduleMalignancy'
paramPath = os.path.join('config', 'Params.yaml')
########################################################################

######################## Output ########################################
outputPath = '/home/willytell/Desktop/output/pipeline2'
extracted_features = os.path.join(outputPath, 'features.xlsx')
########################################################################


print("Start.")

X, y = getImageMaskFilenamesAndDiagnosis(databasePath, ctPath, ctmaskPath, filename, sheet_name=sheet_name)

mydict = []  # create an empty list

for index in range(0, len(X)):
    imageName = X[index][0]  # full path to the image
    maskName = X[index][1]  # full path to the mask
    y_label = y[index]  # diagnosis: 0 = benign, 1 = malign

    imageITK, _, _ = readNifti(imageName)
    maskITK, mask_arr_xyz, _ = readNifti(maskName)

    # The mask is already labeled.
    ncomponents = np.max(mask_arr_xyz)

    # MODIFY THIS PART <<<<<<<<<<<< !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    for segmentation_label in range(1, ncomponents):     # We skip the 0, which correspond to the background label.
        od = getPyRadiomicFeatures(imageName, maskName, imageITK, maskITK, segmentation_label, y_label, paramPath)
        mydict.append(od)

df = pd.DataFrame.from_dict(mydict)     # pd.DataFrame.from_records(mydict)

saveXLSX(extracted_features, df)

print("Finish.")