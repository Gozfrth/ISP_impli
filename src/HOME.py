# TODO:
# WHITE BALANCE
# GAMMA CORRECTION (12b to 8b)
# Sharpening Filter

# WHAT PATAMETERS CAN BE CHANGED FOR DEMOSAIC IN THE UI?

import streamlit as st
import pandas as pd
from DEMOSAIC import load_raw_image, load_raw_image_rgb, Bayer_demosaicing_bilinear
from UTILS import display_interactive_plot
    
def view_raw_image():
    image_data, image_data_display = load_raw_image_rgb()
    display_interactive_plot(image_data)
    print(image_data.shape)

def view_demosaic_image():
    raw_image_data = load_raw_image()
    demosaic_data = Bayer_demosaicing_bilinear(raw_image_data)
    display_interactive_plot(demosaic_data)

def main():
    st.set_page_config(layout="wide")

    add_selectbox = st.sidebar.selectbox(
        "Select Stage of ISP",
        ("DEMOSAIC", "SOMETHNG", "SOMETHING")
    )

    st.markdown("""<hr style="border:3px solid rgb(255,255,255) ">""", unsafe_allow_html=True)
    st.markdown("""# ASSIGNMENT 1""")
    st.markdown("""<hr style="border:3px solid rgb(255,255,255) ">""", unsafe_allow_html=True)


    if add_selectbox == "DEMOSAIC":
        view_raw = st.checkbox("View Raw?", value=False)

        if view_raw:
            view_raw_image()
        
        view_demosaiced = st.checkbox("view_demosaiced?", value=False)

        if view_demosaiced:
            view_demosaic_image()

if __name__ == "__main__":
    main()