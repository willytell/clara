import time
import os
from BasicIO.nifti import readNifti
from BasicImageProcessing.slidingwindow import SlidingWindow
from BasicImageProcessing.featureExtractionStrategy import RadiomicParallelClass
from BasicIO.saveFeatures import saveCSV, saveXLSX


################### Start of 'some parameters'
databasePath = '/home/willytell/Desktop'

ctPath = 'LungCTDataBase/LIDC-IDRI/Nii_Vol/CT_nii'
ctmaskPath = 'output/pipeline1A/CTshiftedmask_nii'

image_filename = os.path.join(databasePath, ctPath, "image.nii.gz")       # full path to the image
mask_filename = os.path.join(databasePath, ctmaskPath, "mask.nii.gz")     # full path to the mask

# Replace properly these two values. Here always they are 1,
# but these information should be extracted from the file name.
image_caseID = 1
image_lessionID = 1



winSize = 3     # [3 | 5 | 7 | 9 | 11 | so on ]. For example, 3 means a volume of 3x3x3.
deltaX  = 1     # slide voxel in x direction
deltaY  = 1     # slide voxel in y direction
deltaZ  = 1     # slide voxel in z direction
mode = 'edge'   # ['constant'|'edge'|'mean'| etc.] Look inside np.pad() for all the modes for padding.


nCores = 4      # number of cores to be used in parallel during the feature extraction.
paramPath = "/home/willytell/Documentos/PhD/lc3d/config/Params.yaml"


outputFormat = 'xls'    # ['csv' | 'xls']

################### End of 'some parameters'


# Read image and mask.
imageITK_xyz, image_arr_xyz, image_metadata = readNifti(image_filename)
maskITK_xyz, mask_arr_xyz, mask_metadata = readNifti(mask_filename)


# Image and mask must have the same volume shape.
assert image_arr_xyz.shape == mask_arr_xyz.shape, "Error: image and mask shape must match!"


slidingWindow = SlidingWindow(window_size=winSize, mode=mode)

# adding Pad to the volume
image_arr_xyz_padded = slidingWindow.padding(image_arr_xyz)
print("    The image array has a volume's shape : {}.".format(image_arr_xyz.shape))
print("    The image array has been padded using the method: '{}, now its shape is: {}'.".format(slidingWindow.mode,
                                                                                                 image_arr_xyz_padded.shape))

# little_cubes will contains all the small volumes generated
# after the window have been shifted throughout the volume.
# By the way, little_cubes is a numpy object.
start_time = time.process_time()
little_cubes = slidingWindow.rolling_window(image_arr_xyz_padded)
elapsed_time = time.process_time() - start_time  # it measures in seconds

print("    little_cubes.shape : {}, computed in: {:.2f} seconds.".format(little_cubes.shape, elapsed_time))





myRadiomic = RadiomicParallelClass('ParallelRadiomics', nCores, paramPath, winSize)






if little_cubes is not None:
    # extract features (in parallel) and save them.
    df = myRadiomic.featureExtraction(little_cubes, mask_arr_xyz, image_filename, mask_filename,
                                image_caseID, image_lessionID, image_metadata, mask_metadata)

    if df is not None:
        if outputFormat == 'csv':
            saveCSV(df, file)

