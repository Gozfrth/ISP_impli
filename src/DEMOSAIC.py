import numpy as np
import math
from scipy.ndimage import convolve

RAW_FILE_PATH = "TestInput_Assignment_1/1920x1280x12bitsxGRBG_2850K_2000Lux.raw"

def Bayer_demosaicing_bilinear(CFA, r_gain = 1, g_gain = 1, b_gain = 1):
    """
    REFERENCED THE FOLLOWING A LOT: 
    https://github.com/colour-science/colour-demosaicing/blob/develop/colour_demosaicing/bayer/demosaicing/bilinear.py
    """
    height, width = CFA.shape

    # MASKS

    R_mask = np.zeros((height, width))
    G_mask = np.zeros((height, width))
    B_mask = np.zeros((height, width))

    R_mask[0::2, 1::2] = 1
    G_mask[0::2, 0::2] = 1
    G_mask[1::2, 1::2] = 1 
    B_mask[1::2, 0::2] = 1 

    # Kernels
    H_G = np.array([[0, 1, 0],
                    [1, 4, 1],
                    [0, 1, 0]]) / 4

    H_RB = np.array([[1, 2, 1],
                     [2, 4, 2],
                     [1, 2, 1]]) / 4

    # {‘reflect’, ‘constant’, ‘nearest’, ‘mirror’, ‘wrap’} modes
    R = convolve(CFA * R_mask, H_RB, mode='mirror') * r_gain
    G = convolve(CFA * G_mask, H_G, mode='mirror') * g_gain
    B = convolve(CFA * B_mask, H_RB, mode='mirror') * b_gain

    return np.stack([R, G, B], axis=-1)
