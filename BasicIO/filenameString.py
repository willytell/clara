# -*- coding: utf-8 -*-

import os

def getMaskFilename(imageFilename):
    """ Using the original image filename, it returns the corresponding original mask filename.
    original-image-filename -> original-mask-filename.
    Case 1:
        LIDC-IDRI-0003_GT1.nii.gz -> LIDC-IDRI-0003_GT1_Mask.nii.gz
    Case 2:
        LIDC-IDRI-0003_GT1_2.nii.gz -> LIDC-IDRI-0003_GT1_2_Mask.nii.gz

    In both cases, we must add '_Mask'. """


    return imageFilename.split('.')[0] + '_Mask.nii.gz'


def getImageFilename(maskFilename):
    """ Using the original mask filename, it returns the corresponding original image filename.
    original-mask-filename -> original-image-filename.
    Case 1:
        LIDC-IDRI-0003_GT1_Mask.nii.gz -> LIDC-IDRI-0003_GT1.nii.gz
    Case 2:
        LIDC-IDRI-0003_GT1_2_Mask.nii.gz -> LIDC-IDRI-0003_GT1_2.nii.gz """

    return maskFilename.split('.')[0].replace('_Mask', '') + '.nii.gz'


def getFilenamePair(databasePath, ctPath, ctmaskPath, basename, noduleID, roi_flag=False):
    """ Form the full path for the image and the mask.

    Parameters
    ----------

    databasePath : str
        Indicate the path to the databe, for e.g. '/home/willytell/Desktop/LungCTDataBase/Nii_Vol'.

    ctPath : str
        Image directory, for e.g. 'CT_nii' or 'CTRoi_nii'.


    ctmaskPath : str
        Mast directory, for e.g. 'CTmask_nii' or 'CTRoimask_nii'.

    basename : str
        Same part of the filename for image and mask, for e.g. 'LIDC-IDRI-0246'

    nodeID : str
        Number of nodule, for e.g. '1' or '2'.

    roi_flag : bool
        Indicates if the noduleID is used to conform the filename of the image and mask. When we are working with
        ROIs image and mask, this must be True.

    Returns
    -------
    str, str
        Full path with filename for image and mask.
    """


    if roi_flag:
        tmp = basename + '_GT1_'  + noduleID
    else:
        tmp = basename + '_GT1'  # + noduleID

    imageFilename = os.path.join(databasePath, ctPath, tmp + '.nii.gz')
    maskFilename = os.path.join(databasePath, ctmaskPath, tmp + '_Mask.nii.gz')

    return imageFilename, maskFilename
