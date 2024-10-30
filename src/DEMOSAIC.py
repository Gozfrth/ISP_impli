import numpy as np
import math 
import streamlit as st
from scipy.ndimage import convolve

RAW_FILE_PATH = "TestInput_Assignment_1/1920x1280x12bitsxGRBG_2850K_2000Lux.raw"

def Bayer_demosaicing_bilinear(CFA):
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
    R = convolve(CFA * R_mask, H_RB, mode='reflect')
    G = convolve(CFA * G_mask, H_G, mode='reflect')
    B = convolve(CFA * B_mask, H_RB, mode='reflect')

    return np.stack([R, G, B], axis=-1)

def load_raw_image(FILE):
    try:
        with open("TestInput_Assignment_1/" + FILE, 'rb') as f:
            raw_data = f.read()

        width, height = 1920, 1280 

        raw_values = np.frombuffer(raw_data, dtype=np.uint16).reshape((height, width))

        effective_values = raw_values

        return effective_values

    except Exception as e:
        print("Error reading file:", e)
    
def load_raw_image_rgb(FILE):
    try:
        with open("TestInput_Assignment_1/" + FILE, 'rb') as f:
            raw_data = f.read()

        width, height = 1920, 1280 

        raw_values = np.frombuffer(raw_data, dtype=np.uint16).reshape((height, width))

        effective_values = raw_values

        # GRBG 2x2 MATRIX VALS
        g1 = effective_values[0::2, 0::2]
        r = effective_values[0::2, 1::2]
        b = effective_values[1::2, 0::2]
        g2 = effective_values[1::2, 1::2]

        rgb_img = np.zeros((height, width, 3), dtype=np.uint16)

        rgb_img[0::2, 0::2, 1] = g1
        rgb_img[0::2, 1::2, 0] = r
        rgb_img[1::2, 0::2, 2] = b
        rgb_img[1::2, 1::2, 1] = g2

        rgb_img_display = np.zeros((height, width, 3), dtype=np.uint16)

        rgb_img_display = (rgb_img / 4095 * 255).astype(np.uint8)

        print("Raw data loaded successfully")

        return rgb_img_display

    except Exception as e:
        print("Error reading file:", e)

### THIS DOESNT WORK NOW THAT rgb_img_display is defined in the load_raw_image function
# show_image_with_zoom(image_data=rgb_img_display)
