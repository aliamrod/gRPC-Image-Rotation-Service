"""
Image Processing Functions.
Author : Alia Mahama-Rodriguez
"""

# Importing the required package(s).
from PIL import Image, ImageFilter
import numpy as np

from scipy import signal
import io

#  Global variables
MAX_WIDTH = 1000 
MAX_HEIGHT = 1000

def convert_to_jpg(file):
    """
    Convert a files (e.g., .png) to .jpg.
    Arguments:
        - file (str) :          file to convert to .jpg
    Returns:
        - file (str) :          file of the converted .jpg
    """

# Open image.
"""extension = file[-4:]
if extension not in ['.jpg', 'jpeg']:
    print("Converting input image from .png to .jpg format...")
    img = Image.open(file)
    # The image object is used to save the image in .jpg format.
    modified_file = file[:-3]+"jpg"
    img.save(modified_img)
    return modified_file
else: 
    return file
"""
def rotate_image(input_image, angle):
    """
    Read image (PIL import Image) and consequently, rotate an image in accordance to designated degree.
    Arguments:
        - rotation(string)      : angle of rotation (multiple of 90), positive motion moving CCW
        - image(NLImage)        : NLImage object containing data (bytes data) and other intrinsic attributes
    Returns:
        - img(NLImage)
    """

    rotated_image = im.rotate(angle*90, expand = True)
    return rotated_image

# Applying Mean Filter.
"""
Objective: Replace each pixel value in the image with the mean ('average') value of its neighbors, including itself.
This has the effect of eliminating pixel values which are non-representative of their environment. Like other convolutions,
it is based around a kernel, which represents the shape and size of the neighborhood to be sampled when calculating this mean value.
"""
# First, apply function to count number of neighboring pixels. 
def count_neighbors(in_array):
    kernel = np.ones((3,3))
    ones_ = np.oness((in_array.shape))
    count_n = signal.convolve2d(ones_, kernel, mode = 'same')
    return count_n

# Function applying mean filter of input image.
def mean_filter(input_image, rgb):
    kernel = np.ones((3,3))
    if not rgb:
        conv_output = signal.convolve2d(input_image, kernel, mode =  'same')
        count_n = count_neighbors(input_image)
        mean_filter_output = np.divide(conv_output, count_n)
    else:
        num_channels = np.arange(3)
        mean_filter_output = np.zeros(input_image.shape)
        count_n = count_neighbors(input_image[:, :, 0])
        for channel in num_channels:
            conv_output = signal.convolve2d(input_image[:, :, channel], kernel, mode = 'same')
            mean_filter_out[:, :, channel] = np.divide(conv_out, count_ngb)
        return mean_filter_output 
