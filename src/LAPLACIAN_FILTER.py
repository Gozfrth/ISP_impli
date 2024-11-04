import cv2
import numpy as np

def apply_laplacian_filter(denoised_data, kernel_size=5, enhancement_factor=1.0):
    ddepth = cv2.CV_16S  
    print("Input shape:", denoised_data.shape)
    print("Input dtype:", denoised_data.dtype)
    
    if denoised_data.ndim == 3 and denoised_data.shape[2] == 3:
        gray_image = cv2.cvtColor(denoised_data, cv2.COLOR_RGB2GRAY)
    else:
        gray_image = denoised_data

    laplacian_filtered = cv2.Laplacian(gray_image, ddepth=ddepth, ksize=kernel_size)
    
    print("Laplacian shape:", laplacian_filtered.shape)
    print("Laplacian dtype:", laplacian_filtered.dtype)
    
    laplacian_abs = cv2.convertScaleAbs(laplacian_filtered)

    enhanced_image = np.zeros_like(denoised_data)

    
    for i in range(3):
        enhanced_image[:, :, i] = cv2.addWeighted(denoised_data[:, :, i], 1.0, laplacian_abs, enhancement_factor, 0)

    print("Enhanced shape:", enhanced_image.shape)
    print("Enhanced dtype:", enhanced_image.dtype)
    return enhanced_image
