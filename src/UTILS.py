import plotly.express as px
import streamlit as st

def display_interactive_plot(image_data):
    fig = px.imshow(image_data)
    
    fig.update_layout(
        width=1920,  # Adjust width as needed
        height=1280  # Adjust height as needed
    )
    
    st.plotly_chart(fig)