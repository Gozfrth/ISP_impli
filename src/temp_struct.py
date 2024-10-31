# TODO:
# WHITE BALANCE
# FORGOT ABOUT DENOISE
# GAMMA CORRECTION (12b to 8b)
# Sharpening Filter

# WHAT PATAMETERS CAN BE CHANGED FOR DEMOSAIC IN THE UI?

import streamlit as st
from UTILS import display_interactive_plot, b16_to_b8
from DEMOSAIC import load_raw_image, load_raw_image_rgb, Bayer_demosaicing_bilinear
from WHITE_BALANCE import apply_white_balance
from DENOISE import denoise
from GAMMA_CORRECTION import gamma_correct_and_reduce_bit_depth
from SHARPENING_FILTER import unsharp_mask
import numpy as np
    
def view_raw_image(FILE):
    st.markdown("""### RAW IMAGE""")    
    raw_image_data_display = load_raw_image_rgb(FILE)
    display_interactive_plot(raw_image_data_display)

def view_demosaic_image(FILE):
    st.markdown("""### DEMOSAICING""")
    raw_image_data = load_raw_image(FILE)
    demosaic_data = Bayer_demosaicing_bilinear(raw_image_data)
    display_interactive_plot(b16_to_b8(demosaic_data))

def view_white_balance_image(FILE):
    st.markdown("""### WHITE BALANCE""")
    raw_image_data = load_raw_image(FILE)
    demosaic_data = Bayer_demosaicing_bilinear(raw_image_data)
    white_balance_data = apply_white_balance(demosaic_data)
    display_interactive_plot(b16_to_b8(white_balance_data))

def view_denoise_image(FILE):
    st.markdown("""### DENOISING (GAUSSIAN FILTER)""")
    sigma = st.slider("Sigma Value", min_value=0.1, max_value=10.0, value=1.0, step=0.1)
    kernel_size = st.slider("Kernel Size", min_value=3, max_value=7, value=5, step=2)
    if kernel_size == 3:
        placeholder_scaling_factor = 16
    elif kernel_size == 5:
        placeholder_scaling_factor = 273
    else:
        placeholder_scaling_factor = 1003
    scaling_factor = st.number_input("Scaling Factor (Preferably dont edit)", value=placeholder_scaling_factor)

    raw_image_data = load_raw_image(FILE)
    demosaic_data = Bayer_demosaicing_bilinear(raw_image_data)
    (denoised_data, gaussian_kernel) = denoise(demosaic_data, kernel_size=kernel_size, sigma=sigma, scaling_factor=scaling_factor, ret_kernel=True)

    display_interactive_plot(b16_to_b8(denoised_data))

    disp_gaussian_kernel_un = st.toggle("Display Gaussian Kernel - unnormalized")
    disp_gaussian_kernel_n = st.toggle("Display Gaussian Kernel - normalized")

    if disp_gaussian_kernel_un:
        st.write("Gaussian Kernel - unnormalized")
        st.write(gaussian_kernel)
    if disp_gaussian_kernel_n:
        st.write("Gaussian Kernel - normalized")
        st.write(np.divide(gaussian_kernel, np.sum(gaussian_kernel)))


def view_gamma_corrected_image(FILE):
    st.markdown("""### GAMMA CORRECTION""")
    gamma = st.slider("Gamma Value", min_value=0.1, max_value=10.0, value=2.2, step=0.1)
    
    raw_image_data = load_raw_image(FILE)
    demosaic_data = Bayer_demosaicing_bilinear(raw_image_data)

    gamma_corrected = gamma_correct_and_reduce_bit_depth(demosaic_data, gamma)
    # print(gamma_corrected)
    display_interactive_plot(gamma_corrected)


def view_sharpening_filter_image(FILE):
    raw_image_data = load_raw_image(FILE)
    demosaic_data = Bayer_demosaicing_bilinear(raw_image_data)
    
    alpha = st.slider("Alpha Value", min_value=0.1, max_value=2.0, value=1.5, step=0.1)
    gamma = st.slider("Gamma Value", min_value=0.1, max_value=10.0, value=2.2, step=0.1)

    gamma_corrected = gamma_correct_and_reduce_bit_depth(demosaic_data, gamma)
    sharpened_image = unsharp_mask(gamma_corrected, alpha=alpha)
    display_interactive_plot(sharpened_image)

def main():
    st.set_page_config(layout="wide")

    add_selectbox = st.sidebar.selectbox(
        "Select Stage of ISP",
        ("RAW", "DEMOSAIC", "WHITE_BALANCE", "DENOISE", "GAMMA_CORRECTION", "SHARPENING_FILTER")
    )

    st.markdown("""## ASSIGNMENT 1""")
    st.markdown("""<hr style="border:3px solid rgb(255,255,255) ">""", unsafe_allow_html=True)

    FILE = st.selectbox(
        "Select file",
        ("1920x1280x12bitsxGRBG_2850K_2000Lux.raw", "1920x1280x12bitsxGRBG_6500K_2000Lux.raw")
    )

    if add_selectbox == "RAW":
        view_raw_image(FILE)
    elif add_selectbox == "DEMOSAIC":
        view_demosaic_image(FILE)
    elif add_selectbox == "WHITE_BALANCE":
        view_white_balance_image(FILE)
    elif add_selectbox == "DENOISE":
        view_denoise_image(FILE)
    elif add_selectbox == "GAMMA_CORRECTION":
        view_gamma_corrected_image(FILE)
    elif add_selectbox == "SHARPENING_FILTER":
        view_sharpening_filter_image(FILE)

if __name__ == "__main__":
    main()