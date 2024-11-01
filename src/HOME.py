# TODO:
# REDUCE SESSION STATE JEEZ

# WHAT PATAMETERS CAN BE CHANGED FOR WHITE BALANCE IN THE UI?
# MAYBE TEMPERATURE?

import streamlit as st
from UTILS import display_interactive_plot, b16_to_b8, load_raw_image, load_raw_image_rgb
from DEMOSAIC import Bayer_demosaicing_bilinear
from WHITE_BALANCE import apply_white_balance
from DENOISE import denoise
from GAMMA_CORRECTION import gamma_correct_and_reduce_bit_depth
from SHARPENING_FILTER import unsharp_mask
from ASSIGNMENT_2 import assignment_2
import numpy as np
    
st.set_page_config(layout="wide")

# DEMOSAIC PARAMS
if "r_gain" not in st.session_state:
    st.session_state.r_gain = 1.0
    st.session_state.g_gain = 1.0
    st.session_state.b_gain = 1.0

# WHITE_BALANCE PARAMS (empty rn)

# DENOISE PARAMS
if "sigma" not in st.session_state:
    st.session_state.sigma = 1
    st.session_state.kernel_size = 5
    st.session_state.scaling_factor = 273

if "gamma" not in st.session_state:
    st.session_state.gamma = 2.2

if "alpha" not in st.session_state:
    st.session_state.alpha = 1.5

if "file" not in st.session_state:
    st.session_state.file = "1920x1280x12bitsxGRBG_2850K_2000Lux.raw"

if "previous_file" not in st.session_state:
    st.session_state.previous_file = st.session_state.file

st.session_state.file = st.sidebar.selectbox(
    "Select file",
    ("TestInput_Assignment_1/1920x1280x12bitsxGRBG_2850K_2000Lux.raw", "TestInput_Assignment_1/1920x1280x12bitsxGRBG_6500K_2000Lux.raw", "TestInput_Assignment_2/eSFR_1920x1280_12b_GRGB_6500K_60Lux.raw")
)

if "raw_image_data" not in st.session_state:
    st.session_state.raw_image_data = load_raw_image(st.session_state.file)
    
if "raw_image_data_display" not in st.session_state:
    st.session_state.raw_image_data_display = load_raw_image_rgb(st.session_state.file)

if "demosaic_data" not in st.session_state:
    st.session_state.demosaic_data = Bayer_demosaicing_bilinear(st.session_state.raw_image_data, st.session_state.r_gain, st.session_state.g_gain, st.session_state.b_gain)

if "white_balance_data" not in st.session_state:
    st.session_state.white_balance_data = apply_white_balance(st.session_state.demosaic_data)

if "denoised_data" not in st.session_state:
    st.session_state.denoised_data = denoise(st.session_state.white_balance_data, kernel_size=st.session_state.kernel_size, sigma=st.session_state.sigma, scaling_factor=st.session_state.scaling_factor)

if "gamma_corrected" not in st.session_state:
    st.session_state.gamma_corrected = gamma_correct_and_reduce_bit_depth(st.session_state.denoised_data, st.session_state.gamma)

if "sharpened_image" not in st.session_state:
    st.session_state.sharpened_image = unsharp_mask(st.session_state.gamma_corrected, alpha=st.session_state.alpha)


# KINDA STUPID APPROACH BUT IT WORKS 
if st.session_state.file != st.session_state.previous_file:
    st.session_state.raw_image_data = load_raw_image(st.session_state.file)
    st.session_state.raw_image_data_display = load_raw_image_rgb(st.session_state.file)
    st.session_state.demosaic_data = Bayer_demosaicing_bilinear(st.session_state.raw_image_data, st.session_state.r_gain, st.session_state.g_gain, st.session_state.b_gain)
    st.session_state.white_balance_data = apply_white_balance(st.session_state.demosaic_data)
    st.session_state.denoised_data = denoise(st.session_state.white_balance_data, kernel_size=st.session_state.kernel_size, sigma=st.session_state.sigma, scaling_factor=st.session_state.scaling_factor)
    st.session_state.gamma_corrected = gamma_correct_and_reduce_bit_depth(st.session_state.denoised_data, st.session_state.gamma)
    st.session_state.sharpened_image = unsharp_mask(st.session_state.gamma_corrected, alpha=st.session_state.alpha)

    st.session_state.previous_file = st.session_state.file


def assignment_1_current_parameters():
    demosaic_params = {"red_gain": st.session_state.r_gain, "green_gain": st.session_state.g_gain, "blue_gain": st.session_state.b_gain}
    white_balance_params = {}
    denoise_params = {"Sigma": st.session_state.sigma, "Kernel Size": st.session_state.kernel_size, "Scaling Factor": st.session_state.scaling_factor}
    gamma_params = {"Gamma": st.session_state.gamma}
    sharpening_params = {"Alpha": st.session_state.alpha}

    all_params ={
        "Demosaic": demosaic_params,
        "White Balance": white_balance_params,
        "Denoise": denoise_params,
        "Gamma Correction": gamma_params,
        "Sharpening Filter": sharpening_params
    }
    st.write("Current Parameters:")
    st.write(all_params)
    pass


def view_raw_image():
    st.markdown("""### RAW IMAGE""")
    display_interactive_plot(st.session_state.raw_image_data_display)

def view_demosaic_image():
    st.session_state.r_gain = st.slider("r_gain", min_value=0.1, max_value=4.0, value=st.session_state.r_gain, step=0.1)
    st.session_state.g_gain = st.slider("g_gain", min_value=0.1, max_value=4.0, value=st.session_state.g_gain, step=0.1)
    st.session_state.b_gain = st.slider("b_gain", min_value=0.1, max_value=4.0, value=st.session_state.b_gain, step=0.1)
    1.0

    st.markdown("""### DEMOSAICING""")
    st.session_state.demosaic_data = Bayer_demosaicing_bilinear(st.session_state.raw_image_data, st.session_state.r_gain, st.session_state.g_gain, st.session_state.b_gain)
    display_interactive_plot(b16_to_b8(st.session_state.demosaic_data))

def view_white_balance_image():
    st.markdown("""### WHITE BALANCE""")
    st.session_state.white_balance_data = apply_white_balance(st.session_state.demosaic_data)
    display_interactive_plot(b16_to_b8(st.session_state.white_balance_data))

def view_denoise_image():
    st.markdown("""### DENOISING (GAUSSIAN FILTER)""")

    st.session_state.sigma = st.slider("Sigma Value", min_value=0.1, max_value=10.0, value=1.0, step=0.1)
    1.0
    st.session_state.kernel_size = st.slider("Kernel Size", min_value=3, max_value=7, value=5, step=2)
    5

    if st.session_state.kernel_size == 3:
        placeholder_scaling_factor = 16
    elif st.session_state.kernel_size == 5:
        placeholder_scaling_factor = 273
    else:
        placeholder_scaling_factor = 1003
    
    st.session_state.scaling_factor = st.number_input("Scaling Factor (Preferably dont edit)", value=placeholder_scaling_factor)

    (st.session_state.denoised_data, gaussian_kernel) = denoise(st.session_state.white_balance_data, kernel_size=st.session_state.kernel_size, sigma=st.session_state.sigma, scaling_factor=st.session_state.scaling_factor, ret_kernel=True)

    display_interactive_plot(b16_to_b8(st.session_state.denoised_data))

    disp_gaussian_kernel_un = st.toggle("Display Gaussian Kernel - unnormalized")
    disp_gaussian_kernel_n = st.toggle("Display Gaussian Kernel - normalized")

    if disp_gaussian_kernel_un:
        st.write("Gaussian Kernel - unnormalized")
        st.write(gaussian_kernel)
    if disp_gaussian_kernel_n:
        st.write("Gaussian Kernel - normalized")
        st.write(np.divide(gaussian_kernel, np.sum(gaussian_kernel)))


def view_gamma_corrected_image():
    st.markdown("""### GAMMA CORRECTION""")
    st.session_state.gamma = st.slider("Gamma Value", min_value=0.1, max_value=10.0, value=1.6, step=0.1)
    1.6

    st.session_state.gamma_corrected = gamma_correct_and_reduce_bit_depth(st.session_state.denoised_data, st.session_state.gamma)
    # print(gamma_corrected)
    display_interactive_plot(st.session_state.gamma_corrected)


def view_sharpening_filter_image():    
    st.session_state.alpha = st.slider("Alpha Value", min_value=0.1, max_value=2.0, value=1.5, step=0.1)
    1.5

    st.session_state.sharpened_image = unsharp_mask(st.session_state.gamma_corrected, alpha=st.session_state.alpha)
    display_interactive_plot(st.session_state.sharpened_image)

def assignment_1():    
    radio_select = "RAW"

    with st.sidebar:
        st.title("EMMITRA ASSIGNMENTS")
        
        with st.expander("ASSIGNMENT-1", True):
            rad_select = st.radio("ISP", options=["RAW", "DEMOSAIC", "WHITE_BALANCE", "DENOISE", "GAMMA_CORRECTION", "SHARPENING_FILTER"])
            radio_select = rad_select
        # with st.expander("ASSIGNMENT-2", True):
        #     rad_select = st.radio("DENOISE AND SHARPNESS", options=["MEDIAL, BILATERAL", "AI DENOISING", "SPATIAL SNR", "LAPLACIAN", "SHARPENING_FILTER"])
        #     radio_select = rad_select
    
    st.markdown("""## ASSIGNMENT 1""")
    st.markdown("""<hr style="border:3px solid rgb(255,255,255) ">""", unsafe_allow_html=True)

    match radio_select:
        case "RAW":
            view_raw_image()
        case "DEMOSAIC":
            view_demosaic_image()
        case "WHITE_BALANCE":
            view_white_balance_image()
        case "DENOISE":
            view_denoise_image()
        case "GAMMA_CORRECTION":
            view_gamma_corrected_image()
        case "SHARPENING_FILTER":
            view_sharpening_filter_image()

    assignment_1_current_parameters()

def main():
    st.session_state.page = st.sidebar.selectbox(
        "SELECT ASSIGNMENT",
        ("ASSIGNMENT_1", "ASSIGNMENT_2")
    )

    match st.session_state.page:
        case "ASSIGNMENT_1":
            assignment_1()
        case "ASSIGNMENT_2":
            assignment_2()
        case _:
            pass

if __name__ == "__main__":
    main()