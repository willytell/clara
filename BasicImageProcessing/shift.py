import numpy as np
from scipy.ndimage.measurements import label

def shiftXY(mask_xyz, shift_x, shift_y, verbose=True):

    if verbose:
        print("\nShift operation:")
        print("   The input volume's shape is: {}.".format(mask_xyz.shape))

    i, j, k = mask_xyz.nonzero()

    shape_x, shape_y, shape_z = mask_xyz.shape

    # numpy works with a coordinate order: zxy
    new_shape_zxy = (shape_z, shape_x + shift_x, shape_y + shift_y)

    # create a new numpy array following its coodenate order: zxy
    tmp_zxy = np.zeros(new_shape_zxy, dtype=mask_xyz.dtype)

    # zxy -> xyz
    tmp_xyz = np.transpose(tmp_zxy, (1, 2, 0))

    # shifting the values
    tmp_xyz[i + shift_x, j + shift_y, k] = 1
    if verbose:
        print("   Shifting the values in x and y axis: {} px and {} px, respectively.".format(shift_x, shift_y))

    for row in range(0, shift_x):
        # Delete the last row in axis X.
        tmp_xyz = np.delete(tmp_xyz, tmp_xyz.shape[0]-1, axis=0)

    for column in range(0, shift_y):
        # Delete the last column in axis Y.
        tmp_xyz = np.delete(tmp_xyz, tmp_xyz.shape[1]-1, axis=1)

    if verbose:
        print("   The resultant shifted volume's shape is: {}.".format(tmp_xyz.shape))

    return tmp_xyz


def labeling(mask_arr, structural_element_shape):
    """ Assign a label to the connected components of the mask.

    Params
    ------

    mask_arr : Numpy array
      Volume with the mask.

    structural_element_shape : tuple
      For e.g. (3,3,3).

    Return
      A mask labeled and the found number of components."""
    
    # build the 'structure element'
    se = np.ones(structural_element_shape, dtype=np.int8)

    # label the mask
    labeled_mask_arr, ncomponents = label(mask_arr, se)

    return labeled_mask_arr, ncomponents



def getROIList(labeled_mask_arr, ncomponents):

    ROI_List = []

    #####################################################################################
    # Input:  volume (is a mask) where 0 means background and 1 means groundtruth
    # Output: Volume Bounding Box for the volumen: xmin, xma, ymin, ymax, zmin, zmax
    def bbox_3D(volume):
        r = np.any(volume, axis=(1, 2))
        c = np.any(volume, axis=(0, 2))
        z = np.any(volume, axis=(0, 1))

        rmin, rmax = np.where(r)[0][[0, -1]]
        cmin, cmax = np.where(c)[0][[0, -1]]
        zmin, zmax = np.where(z)[0][[0, -1]]

        return [rmin, rmax, cmin, cmax, zmin, zmax]
    #####################################################################################


    for num_label in range(1, ncomponents+1):
        mask = np.zeros(labeled_mask_arr.shape, dtype=np.int)
        mask[np.where(labeled_mask_arr == num_label)] = 1

        # Find the exact position for the volume bounding box
        one_ROI = bbox_3D(mask)

        ROI_List.append(one_ROI)


    return ROI_List



def debug_test():
    mask_zxy = np.zeros((5,5,5), dtype=np.int8)
    mask_zxy[:,4,:]=1
    mask_zxy[:,:,4]=1
    mask_zxy[0,0,0]=1
    print(mask_zxy)
    print("===================")

    mask_xyz = np.transpose(mask_zxy, (1, 2, 0))

    result_xyz = shiftXY(mask_xyz, 2, 2)
    result_zxy = np.transpose(result_xyz, (2, 0, 1))
    print(result_zxy)

if __name__ == '__main__':
    debug_test()
