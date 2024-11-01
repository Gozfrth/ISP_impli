import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import streamlit as st
import numpy as np
import math
from scipy.ndimage import convolve

# GAUSSIAN_KERNEL_5x5 = np.divide(np.array([[ 1,  4,  6,  4,  1],
#  [ 4, 16, 27, 16,  4],
#  [ 6, 27, 44, 27,  6],
#  [ 4, 16, 27, 16,  4],
#  [ 1,  4,  6,  4,  1]]), 273)

# GAUSSIAN_KERNEL_3x3 = np.divide(np.array([[1, 2, 1],
#  [2, 4, 2],
#  [1, 2, 1],]), 16)


def display_interactive_plot(image_data, width=1920, height=1280):
    fig = px.imshow(image_data)
    
    fig.update_layout(
        autosize=True,
        width=width,
        height=height,
        xaxis=dict(scaleanchor="y", scaleratio=1)
    )
    
    st.plotly_chart(fig, use_container_width=True)

def display_subplots_2(image_data_1, image_data_2):
    fig = make_subplots(rows=1, cols=2, subplot_titles=("MEDIAN", "BILATERAL"))

    fig.add_trace(
        go.Image(z=image_data_1),
        row=1, col=1
    )

    fig.add_trace(
        go.Image(z=image_data_2),
        row=1, col=2
    )

    fig.update_layout(
        autosize=True,
        width=1920,
        height=600,
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)


def b16_to_b8(image_data):

    return (image_data / 4095 * 255).astype(np.uint8)

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

    convolved_data_r = apply_gaussian_filter_per_channel(image_data[:,:,0], kernel = kernel)
    convolved_data_g = apply_gaussian_filter_per_channel(image_data[:,:,1], kernel = kernel)
    convolved_data_b = apply_gaussian_filter_per_channel(image_data[:,:,2], kernel = kernel)

    convolved_data = np.stack((convolved_data_r, convolved_data_g, convolved_data_b), axis=-1)

    if ret_kernel:
        return (convolved_data, unnormalized_kernel)

    return convolved_data

def apply_gaussian_filter_per_channel(channel_data, kernel):

    return convolve(channel_data, kernel, mode='reflect')


def load_raw_image(FILE):
    try:
        with open(FILE, 'rb') as f:
            raw_data = f.read()

        width, height = 1920, 1280 

        raw_values = np.frombuffer(raw_data, dtype=np.uint16).reshape((height, width))

        effective_values = raw_values

        return effective_values

    except Exception as e:
        print("Error reading file:", e)
    
def load_raw_image_rgb(FILE):
    try:
        width, height = 1920, 1280 
        effective_values = load_raw_image(FILE)

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
