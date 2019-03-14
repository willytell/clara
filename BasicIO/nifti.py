import SimpleITK as sitk
import numpy as np


class Metadata():
    def __init__(self, origin=None, spacing=None, direction=None):
        self.origin = origin
        self.spacing = spacing
        self.direction = direction



def readNifti(filename, verbose=True):

    image_xyz = sitk.ReadImage(filename)

    metadata = Metadata(image_xyz.GetOrigin(), image_xyz.GetSpacing(), image_xyz.GetDirection())

    # Converting from SimpleITK image to Numpy array.
    # During the type transformation the coordinate system is changed from: (x,y,z) -> (z,y,x).
    array_zyx = sitk.GetArrayFromImage(image_xyz)

    # back to the initial xyz coordinate system.
    array_xyz = np.transpose(array_zyx, (2, 1, 0))

    if verbose:
        print("\nReading nifti format from file: {}".format(filename))
        print("Image size: {}".format(image_xyz.GetSize()))
        print("Volume shape: {}".format(array_xyz.shape))
        print("Minimum value: {}".format(np.min(array_xyz)))
        print("Maximum value: {}".format(np.max(array_xyz)))

    return image_xyz, array_xyz, metadata


def saveNifti(array_xyz, metadata, filename, verbose=True):

    # transforming from (x,y,z) to (z,y,x).
    array_zyx = np.transpose(array_xyz, (2, 1, 0))

    # Converting from Numpy array to SimpleITK image.
    image_xyz = sitk.GetImageFromArray(array_zyx)

    # Setting properties
    if metadata is not None:
        image_xyz.SetOrigin(metadata.origen)
        image_xyz.SetSpacing(metadata.spacing)
        image_xyz.SetDirection(metadata.direction)

    # saving the file
    sitk.WriteImage(image_xyz, filename)

    if verbose:
        print("\nSaving the filename: {}.".format(filename))
        print("Image size: {}".format(image_xyz.GetSize()))
        print("Volume shape: {}".format(array_xyz.shape))
        print("Minimum value: {}".format(np.min(array_xyz)))
        print("Maximum value: {}".format(np.max(array_xyz)))
