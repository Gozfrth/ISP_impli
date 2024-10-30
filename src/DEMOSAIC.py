import numpy as np
import math 
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st

RAW_FILE_PATH = "TestInput_Assignment_1/1920x1280x12bitsxGRBG_2850K_2000Lux.raw"

scale = 1.0
window_name = "Zoomable Image"

def load_raw_image():
    try:
        with open(RAW_FILE_PATH, 'rb') as f:
            raw_data = f.read()

        width, height = 1920, 1280 

        raw_values = np.frombuffer(raw_data, dtype=np.uint16).reshape((height, width))

        effective_values = raw_values << 4

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

        rgb_img_display = (rgb_img / 4095 * 255).astype(np.uint8)

        print("Raw data loaded successfully")

        return (rgb_img, rgb_img_display)

    except Exception as e:
        print("Error reading file:", e)

def display_interactive_plot(image_data):
    fig = px.imshow(image_data)
    
    fig.update_layout(
        width=1920,  # Adjust width as needed
        height=1280  # Adjust height as needed
    )
    
    st.plotly_chart(fig)




### THIS DOESNT WORK NOW THAT rgb_img_display is defined in the load_raw_image function
# show_image_with_zoom(image_data=rgb_img_display)
