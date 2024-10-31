import plotly.express as px
import streamlit as st
import numpy as np

def display_interactive_plot(image_data):
    fig = px.imshow(image_data)
    
    fig.update_layout(
        autosize=True,
        width=None,  # Adjust width as needed
        height=None,  # Adjust height as needed
        xaxis=dict(scaleanchor="y", scaleratio=1)
    )
    
    st.plotly_chart(fig, use_container_width=True)

def b16_to_b8(image_data):
    return (image_data / 4095 * 255).astype(np.uint8)