import streamlit as st
import cv2

def assignment_2_current_parameters():
    pass

def view_median_bilateral():
    st.markdown("""### MEDIAN AND BILATERAL DENOISING""")

def view_ai_denoise():
    st.markdown("""### AI_DENOISE""")

def view_snr():
    st.markdown("""### SNR""")

def view_laplacian_filter():
    st.markdown("""### LAPLACIAN FILTER""")

def view_edge_strength():
    st.markdown("""### EDGE STRENGTH""")

def assignment_2():    
    radio_select = "MEDIAN AND BILATERAL"
    
    with st.sidebar:
        st.title("EMMITRA ASSIGNMENTS")
        
        with st.expander("ASSIGNMENT-1", True):
            rad_select = st.radio("DENOISE", options=["MEDIAN AND BILATERAL", "AI DENOISE", "SNR", "LAPLACIAN FILTER", "EDGE STRENGTH"])
            radio_select = rad_select
        # with st.expander("ASSIGNMENT-2", True):
        #     rad_select = st.radio("DENOISE AND SHARPNESS", options=["MEDIAL, BILATERAL", "AI DENOISING", "SPATIAL SNR", "LAPLACIAN", "SHARPENING_FILTER"])
        #     radio_select = rad_select
    
    st.markdown("""## ASSIGNMENT 1""")
    st.markdown("""<hr style="border:3px solid rgb(255,255,255) ">""", unsafe_allow_html=True)

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