import streamlit as st
import cv2
import numpy as np

# ISP

from UTILS import display_interactive_plot, display_subplots_2, b16_to_b8, load_raw_image, load_raw_image_rgb
from DEMOSAIC import Bayer_demosaicing_bilinear
from WHITE_BALANCE import apply_white_balance
from DENOISE import denoise
from GAMMA_CORRECTION import gamma_correct_and_reduce_bit_depth
from SHARPENING_FILTER import unsharp_mask

from MEDIAN_BILATERAL import median_bilateral
from LAPLACIAN_FILTER import apply_laplacian_filter
from SNR import calculate_snr

def assignment_2_current_parameters():
    pass

def view_median_bilateral():
    ## SHOW MEDIAN, BILATERAL and standard_gaussian_DENOISED(st.session_state.two_denoised_data)
    st.markdown("""### MEDIAN AND BILATERAL DENOISING""")

    st.session_state.two_kernel_size = st.slider("Kernel Size", min_value=3, max_value=7, value=st.session_state.two_kernel_size, step=2)

    st.session_state.two_median_data, st.session_state.two_bilateral_data = median_bilateral(st.session_state.two_white_balance_data, kernel_size=st.session_state.two_kernel_size)
    
    ## st.session_state.two_bilateral_data --- IS 8 BIT!!!
    ## CV2 BILATERAL DOESNT SUPPORT 16 BIT IMAGES, SO CONVERTING TO 8 BIT. big sad

    display_subplots_2(b16_to_b8(st.session_state.two_median_data), st.session_state.two_bilateral_data, subplot_titles=["Median", "Bilateral"])
    
    match st.session_state.two_kernel_size:
        case 3:
            st.session_state.two_scaling_factor = 16
        case 5:
            st.session_state.two_scaling_factor = 273
        case 7:
            st.session_state.two_scaling_factor = 1003

    display_interactive_plot(b16_to_b8(denoise(st.session_state.two_white_balance_data, kernel_size=st.session_state.two_kernel_size, sigma=st.session_state.two_sigma, scaling_factor=st.session_state.two_scaling_factor)), width=980, height=640)

def view_ai_denoise():
    st.markdown("""### AI_DENOISE""")

def view_snr():
    ROIS = [
    (791, 365, 1042, 459), 
    (677, 557, 763, 646),  
    (794, 746, 1036, 835)
]
    st.markdown("### Signal-to-Noise Ratio (SNR)")
    denoised_image = st.session_state.two_median_data
    denoised_image_8bit = b16_to_b8(denoised_image)

    
    for i, roi in enumerate(ROIS, start=1):
        x1, y1, x2, y2 = roi
        cv2.rectangle(denoised_image_8bit, (x1, y1), (x2, y2), (255, 0, 0), 2)
    
    display_interactive_plot(denoised_image_8bit, width=800, height=600)

    st.markdown("#### SNR Values for ROIs")
    for i, roi in enumerate(ROIS, start=1):
        snr_value = calculate_snr(denoised_image, roi)
        st.write(f"ROI {i} SNR: {snr_value:.2f}")

def view_laplacian_filter():
    st.markdown("""### LAPLACIAN FILTER""")
    st.session_state.two_laplace_kernel_size = st.slider("Laplacian Filter", min_value=3, max_value=7, value=5, step=2)
    st.session_state.two_enhancement_factor = st.slider("Enhancement Factor", min_value=0.1, max_value=2.0, value=1.0, step=0.05)
    st.session_state.denoise_data1, st.session_state.denoise_data2 = median_bilateral(st.session_state.two_white_balance_data, kernel_size=st.session_state.two_kernel_size)
    st.session_state.filtered_data=apply_laplacian_filter(st.session_state.denoise_data2,kernel_size=st.session_state.two_laplace_kernel_size, enhancement_factor=st.session_state.two_enhancement_factor)
    display_interactive_plot(st.session_state.filtered_data)

def view_edge_strength():
    st.markdown("""### EDGE STRENGTH""")

    st.session_state.threshold1 = st.slider("threshold1", min_value=50, max_value=150, value=100, step=5)
    st.session_state.threshold2 = st.slider("threshold2", min_value=150, max_value=300, value=200, step=5)

    st.session_state.denoised_data = denoise(st.session_state.two_white_balance_data, kernel_size=st.session_state.two_kernel_size, sigma=st.session_state.two_sigma, scaling_factor=st.session_state.two_scaling_factor)

    denoised_image_8bit = b16_to_b8(st.session_state.denoised_data)
    
    st.session_state.edge_data = cv2.Canny(denoised_image_8bit, threshold1=st.session_state.threshold1, threshold2=st.session_state.threshold2)
    
    edge_strength = np.sum(st.session_state.edge_data > 0) / (st.session_state.edge_data.size) * 100
    st.markdown(f"Edge Strength: {edge_strength:.2f}%")
    
    display_interactive_plot(st.session_state.edge_data)

def init_state():
    # DEMOSAIC PARAMS
    if "two_r_gain" not in st.session_state:
        st.session_state.two_r_gain = 1.0
        st.session_state.two_g_gain = 1.0
        st.session_state.two_b_gain = 1.0

    # WHITE_BALANCE PARAMS (empty rn)

    # DENOISE PARAMS
    if "two_sigma" not in st.session_state:
        st.session_state.two_sigma = 1
        st.session_state.two_kernel_size = 5
        st.session_state.two_scaling_factor = 273

    if "two_gamma" not in st.session_state:
        st.session_state.two_gamma = 2.2

    if "two_alpha" not in st.session_state:
        st.session_state.two_alpha = 1.5
    
    # Laplacian Filter
    if "two_laplace_kernel_size" not in st.session_state:
        st.session_state.two_enhancement_factor = 1.0
        st.session_state.two_laplace_kernel_size = 5
    
    if "threshold1" not in st.session_state:
        st.session_state.threshold1 = 100
        st.session_state.threshold2 = 200

    FILE = "TestInput_Assignment_2/eSFR_1920x1280_12b_GRGB_6500K_60Lux.raw"

    if "two_raw_image_data" not in st.session_state:
        st.session_state.two_raw_image_data = load_raw_image(FILE)
        
    if "two_raw_image_data_display" not in st.session_state:
        st.session_state.two_raw_image_data_display = load_raw_image_rgb(FILE)

    if "two_demosaic_data" not in st.session_state:
        st.session_state.two_demosaic_data = Bayer_demosaicing_bilinear(st.session_state.two_raw_image_data, st.session_state.two_r_gain, st.session_state.two_g_gain, st.session_state.two_b_gain)

    if "two_white_balance_data" not in st.session_state:
        st.session_state.two_white_balance_data = apply_white_balance(st.session_state.two_demosaic_data)

    if "two_denoised_data" not in st.session_state:
        st.session_state.two_denoised_data = denoise(st.session_state.two_white_balance_data, kernel_size=st.session_state.two_kernel_size, sigma=st.session_state.two_sigma, scaling_factor=st.session_state.two_scaling_factor)

    if "two_gamma_corrected" not in st.session_state:
        st.session_state.two_gamma_corrected = gamma_correct_and_reduce_bit_depth(st.session_state.two_denoised_data, st.session_state.two_gamma)

    if "two_sharpened_data" not in st.session_state:
        st.session_state.two_sharpened_data = unsharp_mask(st.session_state.two_gamma_corrected, alpha=st.session_state.two_alpha)
    
    if "two_median_data" not in st.session_state:
        st.session_state.two_median_data, st.session_state.two_bilateral_data = median_bilateral(st.session_state.two_white_balance_data)

radio_select = "MEDIAN AND BILATERAL"

def assignment_2():
    init_state() 
    st.markdown("""## ASSIGNMENT 2""")
    st.markdown("""<hr style="border:3px solid rgb(255,255,255) ">""", unsafe_allow_html=True)
    
    with st.sidebar:
        with st.expander("ASSIGNMENT-2", True):
            rad_select = st.radio("A-2", options=["MEDIAN AND BILATERAL", "AI DENOISE", "SNR", "LAPLACIAN FILTER", "EDGE STRENGTH"])
            radio_select = rad_select

    match radio_select:
        case "MEDIAN AND BILATERAL":
            view_median_bilateral()
        case "AI DENOISE":
            view_ai_denoise()
        case "SNR":
            view_snr()
        case "LAPLACIAN FILTER":
            view_laplacian_filter()
        case "EDGE STRENGTH":
            view_edge_strength()

    assignment_2_current_parameters()