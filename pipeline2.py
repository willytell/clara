import os
from BasicIO.nifti import readNifti, saveNifti
from BasicIO.filenameList import getImageMaskFilenamesAndDiagnosis
from BasicImageProcessing.shift import labeling

######################## Input #########################################
databasePath = '/home/willytell/Desktop'
ctPath = 'LungCTDataBase/LIDC-IDRI/Nii_Vol/CT_nii'
ctmaskPath = 'output/pipeline1/CTshiftedmask_nii'
filename = '/home/willytell/Desktop/tcia_diagnosis.xls'
sheet_name='NoduleMalignancy'
paramPath = os.path.join('config', 'Params.yaml')
########################################################################

######################## Output ########################################
outputPath = '/home/willytell/Desktop/output/pipeline2/CTlabeledshiftedmask_nii'
########################################################################


print("Start.")

X, y = getImageMaskFilenamesAndDiagnosis(databasePath, ctPath, ctmaskPath, filename, sheet_name=sheet_name)

mydict = []   # Create an empty list.

for index in range(0, len(X)):
    imageName = X[index][0]     # Full path to the image
    maskName = X[index][1]      # Full path to the mask
    y_label = y[index]          # Diagnosis: 0 = benign, 1 = malign

    imageITK, image_arr_xyz, _ = readNifti(imageName)
    maskITK, mask_arr_xyz, mask_metadata = readNifti(maskName)

    assert image_arr_xyz.shape != mask_arr_xyz, "Error: image and mask shape must match!"

    # Label the mask to find all the connected components.
    labeled_mask_xyz, ncomponents = labeling(mask_arr_xyz, (3, 3, 3))

    # Save the labeled mask, it preserves the same name.
    saveNifti(labeled_mask_xyz, mask_metadata, os.path.join(outputPath, maskName.split('/')[-1]))


print("Finish.")