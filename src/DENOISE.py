import numpy as np
import math
from scipy.ndimage import convolve

GAUSSIAN_KERNEL_5x5 = np.divide(np.array([[ 1,  4,  6,  4,  1],
 [ 4, 16, 27, 16,  4],
 [ 6, 27, 44, 27,  6],
 [ 4, 16, 27, 16,  4],
 [ 1,  4,  6,  4,  1]]), 273)

GAUSSIAN_KERNEL_3x3 = np.divide(np.array([[1, 2, 1],
 [2, 4, 2],
 [1, 2, 1],]), 16)

def Gauss(x, y, sigma):
    return (1/2*math.pi) * np.exp(-((x**2 + y**2) / (2 * (sigma**2))))

def derive_kernel_unnormalized(kernel_size=5, sigma=1, scaling_factor=273):
    gaussian_matrix = np.zeros((kernel_size, kernel_size))

    k_center = kernel_size // 2

    # FLOAT
    for i in range(kernel_size):
        for j in range(kernel_size):
            gaussian_matrix[i, j] = Gauss(i - k_center, j-k_center, sigma)

    # INTIGER APPROXIMATION
    gaussian_matrix /= np.sum(gaussian_matrix)

    scaled_matrix = gaussian_matrix * scaling_factor
    gaussian_matrix_int = np.round(scaled_matrix).astype(int)
    gaussian_matrix_int[k_center, k_center] += scaling_factor - np.sum(gaussian_matrix_int)
    
    return gaussian_matrix_int

def apply_gaussian_filter_whole(image_data, kernel_size=5, sigma=1, scaling_factor = 273, ret_kernel = False):
    unnormalized_kernel = derive_kernel_unnormalized(kernel_size = kernel_size, sigma = sigma, scaling_factor = scaling_factor)
    kernel = np.zeros((kernel_size, kernel_size, 3), dtype=np.float32)
    kernel = np.divide(unnormalized_kernel, np.sum(unnormalized_kernel))

    denoised_data_r = apply_gaussian_filter_per_channel(image_data[:,:,0], kernel = kernel)
    denoised_data_g = apply_gaussian_filter_per_channel(image_data[:,:,1], kernel = kernel)
    denoised_data_b = apply_gaussian_filter_per_channel(image_data[:,:,2], kernel = kernel)

    denoised_data = np.stack((denoised_data_r, denoised_data_g, denoised_data_b), axis=-1)

    if ret_kernel:
        return (denoised_data, unnormalized_kernel)

    return denoised_data

def apply_gaussian_filter_per_channel(channel_data, kernel):

    return convolve(channel_data, kernel, mode='reflect')

# def Gauss(x, y, sigma):
#     return (1/2*math.pi) * np.exp(-((x**2 + y**2) / (2 * (sigma**2))))



# def Gauss5x5(sigma):
#     gaussian_matrix = np.zeros((5, 5))

#     for i in range(5):
#         for j in range(5):
#             gaussian_matrix[i, j] = Gauss(i-2, j-2, 1)
#     # print(gaussian_matrix)
#     # array([[0.02877014, 0.12893881, 0.21258417, 0.12893881, 0.02877014],
#     #        [0.12893881, 0.57786367, 0.95273613, 0.57786367, 0.12893881],
#     #        [0.21258417, 0.95273613, 1.57079633, 0.95273613, 0.21258417],
#     #        [0.12893881, 0.57786367, 0.95273613, 0.57786367, 0.12893881],
#     #        [0.02877014, 0.12893881, 0.21258417, 0.12893881, 0.02877014]])
#     gaussian_matrix /= np.sum(gaussian_matrix)

#     scaled_matrix = gaussian_matrix * 273
#     gaussian_matrix_int = np.round(scaled_matrix).astype(int)

#     #     print(gaussian_matrix_int)
#     # print("Sum:", np.sum(gaussian_matrix_int))

#     # SUM != 273, subtract 3 from middle element (44 to 41) to make sum 273...
#     # Seems unreliable to calculate on the fly so better to store the matrices instead of computing.

#     # [[ 1  4  6  4  1]
#     #  [ 4 16 27 16  4]
#     #  [ 6 27 44 27  6]
#     #  [ 4 16 27 16  4]
#     #  [ 1  4  6  4  1]]
#     # Sum: 276