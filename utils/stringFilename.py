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


def getFilenamePair(databasePath, ctPath, ctmaskPath, basename, noduleID):
    """
    databasePath = '/home/willytell/Desktop/LungCTDataBase/Nii_Vol'
    ctPath = 'CT_nii' or 'CTRoi_nii'
    ctmaskPath = 'CTmask_nii' or 'CTRoimask_nii'
    basename = 'LIDC-IDRI-0246'
    nodeID = '1' or '2'
    """

    tmp = basename + '_GT1_' + noduleID

    imageFilename = os.path.join(databasePath, ctPath, tmp + '.nii.gz')
    maskFilename = os.path.join(databasePath, ctmaskPath, tmp + '_Mask.nii.gz')

    return imageFilename, maskFilename
