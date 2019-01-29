import os
import glob
import pandas as pd
import numpy as np
from BasicIO.filenameString import getFilenamePair


def checkExistanceOfFiles(imageFilename, maskFilename):
    """Check if there is the image and its corresponding mask.

    Parameters
    ----------
    imageFilename : str
        Full path to the image.

    maskFilename : str
        Full path to the mask.

    Returns
    -------
    bool
        True if both files exists, False otherwise.
    """

    if os.path.isfile(imageFilename) and os.path.isfile(maskFilename):
        return True

    return False


def getFilterList(filename, sheet_name, set_flag=1, verbose=True):
    df = pd.read_excel(filename, sheet_name=sheet_name)
    if verbose:
        print("Reading the file: {}".format(filename))

    df = df.loc[df['Training'] == set_flag]    # set_flag=1 filter traint set, otherwise filter test set.

    return df


def getListFromPatientList(databasePath, ctPath, ctmaskPath, filename, sheet_name, verbose=True):

    df = pd.read_excel(filename, sheet_name=sheet_name)
    if verbose:
        print("Reading the file: {}".format(filename))

    image_list = []
    mask_list = []
    info_list = []

    for idx in range(0, len(df)):
        basename = df.iloc[idx]['Patient ID']  # str
        #noduleID = df.iloc[idx]['NoduleID']
        noduleDiagnosis = df.iloc[idx]['Nodule Diagnosis']
        patientDiagnosis = df.iloc[idx]['Patient Diagnosis']

        #imageFilename_list = getFilenameList(os.path.join(databasePath, ctPath), basename + '*')
        maskFilename_list = getFilenameList(os.path.join(databasePath, ctmaskPath), basename + '*')
        maskFilename_list.sort()

        imageFilename_list = []

        for fname in maskFilename_list:
            fname = fname.split('_Mask.nii.gz')[0] + '.nii.gz'
            imageFilename_list.append(fname)

        for idx in range(len(maskFilename_list)):
            if checkExistanceOfFiles(os.path.join(databasePath, ctPath, imageFilename_list[idx]),
                                     os.path.join(databasePath, ctmaskPath, maskFilename_list[idx])):
                mask_list.append(maskFilename_list[idx])
                image_list.append(imageFilename_list[idx])
                info_list.append((noduleDiagnosis, patientDiagnosis))

                if verbose:
                    print("\nFor index: {} including\nfile {}".format(idx, maskFilename_list[idx]))
                else:
                    if verbose:
                        print("\nFor index: {} discarding\nfile {}".format(idx, maskFilename_list[idx]))

    return image_list, mask_list, info_list


def getImageMaskFilenamesAndDiagnosis(databasePath, ctPath, ctmaskPath, filename, sheet_name, roi_flag, verbose=True):
    """
    Parameters
    ----------
    databasePath : str
        Path to the database.

    ctPath : str
        Directory name of the CT images or CT ROI images. For e.g. 'CT_nii' or 'CTRoi_nii'.

    ctmaskPath : str
        Directory name of the CT Mask or CT ROI Mask. For e.g. 'CTmask_nii' or CTRoimask_nii'.

    filename : str
        Full path to the Excel file. For e.g. '/home/willytell/Desktop/tca_diagnosis.xls'.

    sheet_name : str
        Sheet of the Excel file.

    roi_flag : bool
        True if we are working with ROIs images and masks, False otherwise.

    Returns
    -------
    X : :obj:tuple:`list`
        Full path with filename for image and mask in each tuple of the list.

    y : :obj:int:`list`
        It is the diagnosis for a tuple (image and mask) of X. It is the ground truth.

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

        imageFilename, maskFilename = getFilenamePair(databasePath, ctPath, ctmaskPath, basename,
                                                      noduleID.astype(str), roi_flag=roi_flag)

        if checkExistanceOfFiles(imageFilename, maskFilename):
            X.append((imageFilename, maskFilename))
            y.append(diagnosis)
            if verbose:
                print("\nIncluded files for index: {} \n{} \n{}".format(idx, imageFilename, maskFilename))

        else:
            if verbose:
                print("\nDiscarded files for index: {} \n{} \n{}".format(idx, imageFilename, maskFilename))


    return X, y



def getFilenameList(path, pattern='*.nii.gz'):
    """Obtain a list of filenames for a given directory path.

    Parameters
    ----------
    path : str
        Directory path, for e.g. '/home/willytell/Desktop/LungCTDataBase/LIDC-IDRI/Nii_Vol/CTmask_nii

    pattern : str
        Filter filenames using the pattern extension.

    Returns
    -------
    list
        Filenames without the path, only the filename (and extension) is included."""

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
