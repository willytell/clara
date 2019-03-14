from abc import ABC, abstractmethod
import SimpleITK as sitk
import numpy as np
import pandas as pd
import time
import multiprocessing as mp

import os
from collections import OrderedDict
import six
import radiomics
from radiomics import featureextractor  # This module is used for interaction with pyradiomics




############################ PARALLEL COMPUTING ######################################################

results = []

def collect_result(result):
    global results
    results.append(result)

def do_it(i, x, y, z, flattened_index, winSize, paramPath, volume, label_value, image_filename, mask_filename, caseID, lessionID, image_metadata, mask_metadata):

    #print("Process {} working in index: {}".format(os.getpid(), flattened_index))

    mask_trick = np.ones((winSize, winSize, winSize), dtype=np.int)
    maskITK = sitk.GetImageFromArray(mask_trick)
    maskITK.origin = image_metadata.origin
    maskITK.spacing = image_metadata.spacing
    maskITK.direction = image_metadata.direction

    extractor = featureextractor.RadiomicsFeaturesExtractor(paramPath)

    imageITK = sitk.GetImageFromArray(volume)
    imageITK.origin = mask_metadata.origin
    imageITK.spacing = mask_metadata.spacing
    imageITK.direction = mask_metadata.direction

    new_row = {}

    featureVector = extractor.execute(imageITK, maskITK)  # allways is used the same mask
    # print("Result type: {} and length: {}".format(type(featureVector), len(featureVector)))  # result is returned in a Python ordered dictionary)
    # print('')
    # print('Calculated features')
    for featureName in featureVector.keys():  # Note that featureVectors is a 'disordered dictionary'
        # print('Computed %s: %s' % (featureName, featureVector[featureName]))
        # print(featureVector[featureName])
        if ('firstorder' in featureName) or ('glszm' in featureName) or \
            ('glcm' in featureName) or ('glrlm' in featureName) or \
            ('gldm' in featureName):
            new_row.update({featureName: featureVector[featureName]})

    lst = sorted(new_row.items())  # Ordering the new_row dictionary

    # Adding some columns and values at the front of the list
    # label_value = mask[z, x, y]
    lst.insert(0, ('label', label_value))
    lst.insert(0, ('axisZ', z))
    lst.insert(0, ('axisY', y))
    lst.insert(0, ('axisX', x))
    # flattened_index = np.ravel_multi_index([[z], [y], [x]], (3, 3, 3), order='F')
    #                 np.ravel_multi_index([[2],[1],[0]],rw.shape[:3])
    # [flattened_index] = np.ravel_multi_index([[x], [y], [z]], (max_x, max_y, max_z))  # order='C'
    lst.insert(0, ('flattened_index', int(flattened_index)))
    lst.insert(0, ('lessionID', lessionID))
    lst.insert(0, ('caseID', caseID))
    lst.insert(0, ('mask_filename', mask_filename))
    lst.insert(0, ('image_filename', image_filename))

    od = OrderedDict(lst)
    # for name in od.keys():
    #     print('Computed %s: %s' % (name, od[name]))

    #print("Process {} done processing index: {}".format(os.getpid(), flattened_index))

    return (i, od)

############################ PARALLEL COMPUTING ######################################################


class RadiomicParallelClass():
    def __init__(self, name, ncores):
        self.name = name
        self.radiomicNCores = ncores

    def featureExtraction(self, array, mask, image_filename, mask_filename, caseID, lessionID, image_metadata, mask_metadata, winSize, paramPath):
        print("      Using Parallel Radiomics to extract features...")

        assert type(array).__module__ == np.__name__, "Error, expected a numpy object."
        assert array.ndim == 6, "Error, the array's dimension must be equal to 6."

        max_z, max_x, max_y = array.shape[:3]

        print("         max_z: {}, max_x: {}, max_y: {}".format(max_z, max_x, max_y))
        print("         Extracting new {} rows of features.".format(max_z * max_x * max_y))

        start_time = time.process_time()

        global results
        results = []

        # Set the number of cores to be used in parallel.
        pool = mp.Pool(self.radiomicNCores)    # pool = mp.Pool(mp.cpu_count()-1)

        for x in range(max_x):  # x: row
            for y in range(max_y):  # y: column
                for z in range(max_z):  # z: deep

                    volume = array[z, x, y]     # get a cube from the array (little cubes).
                    label_value = mask[z, x, y] # label value of the mask in the position [z,x,y]
                    [flattened_index] = np.ravel_multi_index([[x], [y], [z]], (max_x, max_y, max_z))  # order='C'

                    i = flattened_index # used to get back an ordered list.

                    pool.apply_async(do_it, args=(i, x, y, z, flattened_index, winSize, paramPath, volume, label_value,
                                    image_filename, mask_filename, caseID, lessionID, image_metadata, mask_metadata), callback=collect_result)

        pool.close()
        pool.join()

        results.sort(key=lambda x: x[0])
        results_final = [r for i, r in results]

        df = pd.DataFrame.from_dict(results_final)

        elapsed_time = time.process_time() - start_time  # it measures in seconds
        print("      Elapsed time for Radiomic to extract features: {:.2f} seconds.".format(elapsed_time))

        return df





def debug_test():
    vol = np.arange(216).reshape(6, 6, 6)
    mr = RadiomicParallelClass('RadiomicParallel', 4)
    #mr.featureExtraction(rw)


if __name__ == '__main__':
    debug_test()
    #test()