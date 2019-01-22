import numpy as np

def shiftXY(mask_xyz, shift_x, shift_y):

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

    for row in range(0, shift_x):
        # Delete the last row in axis X.
        tmp_xyz = np.delete(tmp_xyz, tmp_xyz.shape[0]-1, axis=0)

    for column in range(0, shift_y):
        # Delete the last column in axis Y.
        tmp_xyz = np.delete(tmp_xyz, tmp_xyz.shape[1]-1, axis=1)


    return tmp_xyz



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
