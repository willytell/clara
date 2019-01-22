import os
import glob
import pandas as pd
import numpy as np
from BasicIO.filenameString import getFilenamePair


def checkExistanceOfFiles(imageFilename, maskFilename):
    # Check if there is the image and its corresponding mask.
    if os.path.isfile(os.path.join(imageFilename)) and os.path.isfile(os.path.join(maskFilename)):
        return True

    return False


def getImageMaskFilenamesAndDiagnosis(databasePath, ctPath, ctmaskPath, filename, sheet_name, verbose=True):
    """
    Params
    ------

    databasePath : str
       Path to the database.

    ctPath : str
       Directory name of the CT images or CT ROI images. For e.g. 'CT_nii' or 'CTRoi_nii'.

    ctmaskPath : str
       Directory name of the CT Mask or CT ROI Mask. For e.g. 'CTmask_nii' or CTRoimask_nii'.

    filename : str
       Contains the full path to the .xls file. For e.g. '~/Desktop/tca_diagnosis.xls'.

    """

    df = pd.read_excel(filename, sheet_name=sheet_name)
    if verbose:
        print("Reading the file: {}".format(filename))

    X = []
    y = []

    for idx in range(0, len(df)):
        basename = df.iloc[idx]['Patient ID']   # str
        noduleID = df.iloc[idx]['NoduleID']     # numpy.int64
        diagnosis = df.iloc[idx]['Diagnosis']   # numpy.int64

        imageFilename, maskFilename = getFilenamePair(databasePath, ctPath, ctmaskPath, basename, noduleID.astype(str))

        if checkExistanceOfFiles(imageFilename, maskFilename):
            X.append((imageFilename, maskFilename))
            y.append(diagnosis)
            if verbose:
                print("Included files: {}, {}, {}.".format(idx, imageFilename, maskFilename))

        else:
            if verbose:
                print("Discarded files: {}, {}, {}.".format(idx, imageFilename, maskFilename))


    return X, y



def getFilenameList(path, pattern='*.nii.gz'):
    """ Obtain a list of filenames for a given directory path.

    Params
    ------

    path : str
      Directory path, for e.g. '/home/willytell/Desktop/LungCTDataBase/LIDC-IDRI/Nii_Vol/CTmask_nii

    pattern : str
      Filter filenames using the pattern extension.

    Return
      A filename list, without the path, only the filename is included."""

    filename = [os.path.basename(x) for x in sorted(glob.glob(os.path.join(path, pattern)))]

    return filename



def debug_test():
    databasePath = '/home/willytell/Desktop/LungCTDataBase/LIDC-IDRI/Nii_Vol'
    ctPath = 'CT_nii'
    ctmaskPath = 'CTmask_nii'
    filename = '/home/willytell/Desktop/tcia_diagnosis.xls'
    # X, y = getImageMaskFilenamesAndDiagnosis(databasePath, ctPath, ctmaskPath, filename, sheet_name='NoduleMalignancy')
    #
    # print(X)
    # print("==========")
    # print(y)

    #filename_list = getFilenameList('/home/willytell/Desktop/LungCTDataBase/LIDC-IDRI/Nii_Vol/CTmask_nii')
    filename_list = getFilenameList(os.path.join(databasePath, ctmaskPath))
    for filename in filename_list:
        print(filename)
    #print(filename_list)

if __name__ == '__main__':
    debug_test()
