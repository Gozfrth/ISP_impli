# TODO:
# WHITE BALANCE
# FORGOT ABOUT DENOISE
# GAMMA CORRECTION (12b to 8b)
# Sharpening Filter

# WHAT PATAMETERS CAN BE CHANGED FOR DEMOSAIC IN THE UI?

import streamlit as st
from DEMOSAIC import load_raw_image, load_raw_image_rgb, Bayer_demosaicing_bilinear
from UTILS import display_interactive_plot, b16_to_b8
from GAMMA_CORRECTION import gamma_correct_and_reduce_bit_depth
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

def view_denoise_image(FILE):
    st.markdown("""### DENOISING (GAUSSIAN FILTER)""")

def view_gamma_corrected_image(FILE):
    st.markdown("""### GAMMA CORRECTION""")
    gamma = st.slider("Gamma Value", min_value=0.1, max_value=10.0, value=2.2, step=0.1)
    
    raw_image_data = load_raw_image(FILE)
    demosaic_data = Bayer_demosaicing_bilinear(raw_image_data)

    gamma_corrected = gamma_correct_and_reduce_bit_depth(demosaic_data, gamma)
    # print(gamma_corrected)
    display_interactive_plot(gamma_corrected)

def main():
    st.set_page_config(layout="wide")

    add_selectbox = st.sidebar.selectbox(
        "Select Stage of ISP",
        ("RAW", "DEMOSAIC", "DENOISE", "WHITE_BALANCE", "GAMMA_CORRECTION")
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
    elif add_selectbox == "GAMMA_CORRECTION":
        view_gamma_corrected_image(FILE)
    else:
        view_denoise_image(FILE)

if __name__ == "__main__":
    main()