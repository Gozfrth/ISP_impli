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


def display_interactive_plot(image_data, width=1920, height=1280, title=""):
    fig = px.imshow(image_data)
    
    fig.update_layout(
        autosize=True,
        width=width,
        height=height,
        xaxis=dict(scaleanchor="y", scaleratio=1),
        title=title,
        title_x=0.5,
    )
    
    st.plotly_chart(fig, use_container_width=True)

def display_subplots_2(image_data_1, image_data_2, subplot_titles):
    fig = make_subplots(rows=1, cols=2, subplot_titles=subplot_titles)

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

def display_crf(crf_debevec):
    # Assume crf_debevec is a 1D array with the CRF values
    # We need to create an array for input intensity values (usually 0 to 255)
    intensity_values = np.arange(0, 256, 1)  # Input intensity values from 0 to 255
    output_values = crf_debevec.flatten()  # Flatten in case it's a 2D array

    # Create a Plotly graph
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=intensity_values, y=output_values, mode='lines', name='CRF'))
    
    # Update layout
    fig.update_layout(
        title='Camera Response Function (CRF)',
        xaxis_title='Input Intensity',
        yaxis_title='Output Intensity',
        showlegend=True,
        width=700,
        height=500
    )
    
    # Display the figure in Streamlit
    st.plotly_chart(fig)

def display_color_checker():
    color_checker_srgb = [
        ['#735244', '#c29682', '#627a9d', '#576c43', '#8580b1', '#67bdaa'],
        ['#d68d8f', '#d4b86e', '#505ba6', '#c15a63', '#5e3c6c', '#9dbc40'],
        ['#e0a32e', '#383d96', '#469449', '#af363c', '#e5c78d', '#9a9a9d'],
        ['#e1d8eb', '#363636', '#808080', '#c8c8c8', '#ffffff', '#000000']
    ]

    fig = go.Figure()

    # Adjust layout to have enough space for the entire grid
    fig.update_layout(
        height=400,
        width=600,
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis=dict(range=[0, 6], showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(range=[-4, 0], showgrid=False, zeroline=False, showticklabels=False)
    )

    # Add rectangles for each color block
    for row_index, row in enumerate(color_checker_srgb):
        for col_index, color in enumerate(row):
            fig.add_shape(
                type="rect",
                x0=col_index, x1=col_index + 1,
                y0=-row_index, y1=-row_index - 1,
                fillcolor=color,
                line=dict(color=color)  # Use same color for the border
            )

    # Hide axes and set the background color
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    fig.update_layout(showlegend=False, plot_bgcolor='black')

    # Display in Streamlit
    st.title("Color Checker Visualization")
    st.plotly_chart(fig)


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

        return rgb_img_display

    except Exception as e:
        print("Error reading file:", e)

### THIS DOESNT WORK NOW THAT rgb_img_display is defined in the load_raw_image function
# show_image_with_zoom(image_data=rgb_img_display)
