from radiomics import featureextractor
from collections import OrderedDict

def getPyRadiomicFeatures(imageName, maskName, imageITK, maskITK, segmentation_label, noduleDiagnosis, patientDiagnosis, paramPath, verbose=True):
    """ Extract features using pyradiomic.

    Params
    ------

    imageName : str
      Full path to the file image name.

    maskName : str
      Full path to the file mask name.

    imageITK : SimpleITK
      Image in xyz coordinate system.

    maskITK : SimpleITK
      Mask in xyz coordinate system.

    segmentation_label : int
      Label number of the segmentation which belong to the mask.

    y_label : int
      Classification label is the diagnose obtained from the biopsy, it is the ground truth (gold standard).

    paramPath : str
      File with the parameter to be used by the extractor of pyradiomics.

    Return
      List of features extracted.


    """

    extractor = featureextractor.RadiomicsFeaturesExtractor(paramPath)

    if verbose:
        print("\nExtracting features:")
        print("   Segmentation label: {}".format(segmentation_label))
        print("   Image file: {}".format(imageName))
        print("   Mask file: {}".format(maskName))

    print(imageITK.GetSize())
    print(maskITK.GetSize())

    featureVector = extractor.execute(imageITK, maskITK) #, label=segmentation_label)

    new_row = {}
    for featureName in featureVector.keys():  # Note that featureVectors is a 'disordered dictionary'
        # print('Computed %s: %s' % (featureName, featureVector[featureName]))
        # print(featureVector[featureName])
        if ('firstorder' in featureName) or ('glszm' in featureName) or \
                ('glcm' in featureName) or ('glrlm' in featureName) or \
                ('gldm' in featureName) or ('shape' in featureName):
            new_row.update({featureName: featureVector[featureName]})

    lst = sorted(new_row.items())  # Ordering the new_row dictionary.

    # Adding some columns
    lst.insert(0, ('patient_diagnosis', patientDiagnosis))
    lst.insert(0, ('nodule_diagnosis', noduleDiagnosis))
    lst.insert(0, ('segmentation_label', segmentation_label))
    lst.insert(0, ('mask_filename', maskName))
    lst.insert(0, ('image_filename', imageName))

    od = OrderedDict(lst)
    return (od)