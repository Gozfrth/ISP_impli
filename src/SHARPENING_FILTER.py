# sharpened image = original image – blurred image

import numpy as np
from scipy.ndimage import convolve
from UTILS import derive_kernel_unnormalized, apply_gaussian_filter_whole, display_interactive_plot

def temp_unsharp_mask(image_data, alpha=1.5):
    blurred_image_data = apply_gaussian_filter_whole(image_data, kernel_size=7, sigma=3, scaling_factor = 273, ret_kernel = False)
    print("IM_________________________________________")
    print(image_data[0,0])
    print("BL_________________________________________")
    print(blurred_image_data[0,0])

    mask = np.subtract(image_data, blurred_image_data)
    print("MA_________________________________________")
    print(mask[0,0])
    sharpened_image_data = image_data + alpha * mask
    print("SH_________________________________________")
    print(sharpened_image_data[0,0])

    sharpened_image_data = np.clip(sharpened_image_data, 0, 255)

    return sharpened_image_data

def unsharp_mask(image_data, alpha=1.5, kernel_size=5, sigma=1):
    # Convert to float for accurate calculations
    image_data_float = image_data.astype(np.float32)

    # Apply Gaussian blur to the image
    blurred_image_data = apply_gaussian_filter_whole(image_data_float, kernel_size=kernel_size, sigma=sigma, scaling_factor=273, ret_kernel=False)
    
    # Calculate the mask
    mask = np.subtract(image_data_float, blurred_image_data)

    # Clamp negative values in the mask to 0
    mask = np.clip(mask, 0, None)  # or mask[mask < 0] = 0

    # Calculate sharpened image
    sharpened_image_data = image_data_float + alpha * mask

    # Clip the sharpened image to [0, 255]
    sharpened_image_data = np.clip(sharpened_image_data, 0, 255)

    return sharpened_image_data.astype(np.uint8)  