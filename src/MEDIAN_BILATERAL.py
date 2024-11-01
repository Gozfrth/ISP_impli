import numpy as np
from scipy.ndimage import convolve
from cv2 import bilateralFilter, medianBlur
from UTILS import b16_to_b8

def median_bilateral(image_data, kernel_size = 5):
    print("________________________________________________________________________________")
    print(image_data.dtype)
    two_median_data = medianBlur(image_data, kernel_size)
    two_bilateral_data = bilateralFilter(b16_to_b8(image_data), kernel_size, 75, 75)
    return two_median_data, two_bilateral_data