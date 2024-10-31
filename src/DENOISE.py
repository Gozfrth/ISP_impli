import numpy as np
import math
from UTILS import derive_kernel_unnormalized, apply_gaussian_filter_whole

# COULD JUST BE IN UTILS NO?

def denoise(image_data, kernel_size=5, sigma=1, scaling_factor = 273, ret_kernel = False):
    return apply_gaussian_filter_whole(image_data, kernel_size=kernel_size, sigma=sigma, scaling_factor=scaling_factor, ret_kernel=ret_kernel)

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
# WHY NO WORK ;-;
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