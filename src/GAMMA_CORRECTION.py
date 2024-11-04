import numpy as np
import math 

def gamma_correct_and_reduce_bit_depth(image_12bit, gamma=2.2):

    image_normalized = (image_12bit) / 4095.0

    image_gamma_corrected = np.power(image_normalized, 1/gamma)

    image_8bit = np.zeros((image_12bit.shape[0], image_12bit.shape[1], 3), dtype=np.uint8)
    image_8bit = np.round(image_gamma_corrected * 255).astype(np.uint8)
    
    return image_8bit
