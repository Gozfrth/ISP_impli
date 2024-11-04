import streamlit as st
import cv2
import numpy as np

# HDR

from UTILS import display_interactive_plot, display_subplots_2, display_crf

def assignment_3_current_parameters():
    pass

def hdr(img_list, exposure_times):
    ## DEBEVEC
    merge_debevec = cv2.createMergeDebevec()
    hdr_debevec = merge_debevec.process(img_list, times=exposure_times.copy())

    tonemap1 = cv2.createTonemap(gamma=2.2)
    res_debevec = tonemap1.process(hdr_debevec.copy())
    cal_debevec = cv2.createCalibrateDebevec()
    crf_debevec = cal_debevec.process(img_list, times=exposure_times)
    
    ## ROBERTSON
    merge_robertson = cv2.createMergeRobertson()
    hdr_robertson = merge_robertson.process(img_list, times=exposure_times.copy())
    
    # SHOULD YOU TONE MAP ROBERTSON? idk
    tonemap1 = cv2.createTonemap(gamma=2.2)
    res_robertson = tonemap1.process(hdr_robertson.copy())

    ## MERTENS (doesnt need exposure times)
    merge_mertens = cv2.createMergeMertens()
    res_mertens = merge_mertens.process(img_list)
    
    res_debevec_8bit = np.clip(res_debevec*255, 0, 255).astype('uint8')
    res_robertson_8bit = np.clip(res_robertson*255, 0, 255).astype('uint8')
    res_mertens_8bit = np.clip(res_mertens*255, 0, 255).astype('uint8')

    display_interactive_plot(res_debevec_8bit, title="DEBEVEC")
    display_interactive_plot(res_robertson_8bit, title="ROBERTSON")
    display_interactive_plot(res_mertens_8bit, title="METRENS")

    display_crf(crf_debevec)

def assignment_3():
    st.markdown("""## ASSIGNMENT 3""")
    st.markdown("""<hr style="border:3px solid rgb(255,255,255) ">""", unsafe_allow_html=True)
    
    img_fn = []

    exp1 = 0.0
    exp2 = 0.0
    exp3 = 0.0
    run_exp = False
    run_files = False

    if "one_place_holder" not in st.session_state:
        st.session_state.one_place_holder = "1"
        st.session_state.two_place_holder = "2"
        st.session_state.three_place_holder = "3"

    with st.sidebar:
        path = st.file_uploader("Upload 3 images", accept_multiple_files=True)
        for uploaded_file in path:
            img_fn.append(uploaded_file)
        exp1 = st.number_input("Exposure time " + st.session_state.one_place_holder, value=0.0)
        exp2 = st.number_input("Exposure time " + st.session_state.two_place_holder, value=0.0)
        exp3 = st.number_input("Exposure time " + st.session_state.three_place_holder, value=0.0)
    
    if(len(img_fn) >= 1):
        st.session_state.one_place_holder = img_fn[0].name
    if(len(img_fn) >= 2):
        st.session_state.two_place_holder = img_fn[1].name
    if(len(img_fn) == 3):
        st.session_state.three_place_holder = img_fn[2].name

    # print([file.name for file in img_fn])

    exp_times = [0.0, 0.0, 0.0]

    for uploaded_file in img_fn:
        match uploaded_file.name:
            case "1-10.jpg":
                exp_times[0] = 0.1
            case "1.jpg":
                exp_times[1] = 1.0
            case "4.jpg":
                exp_times[2] = 4.0
            
    if exp1 != 0.0 and exp2 != 0.0 and exp3 != 0.0:
        exp_times = [exp1, exp2, exp3]
        run_exp = True

    img_list = []
    for uploaded_file in img_fn:
        image_bytes = uploaded_file.read()
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_list.append(img_rgb)
        
    exposure_times = np.array(exp_times, dtype=np.float32)
    if(len(img_list) == 3):
        run_files = True
    if (run_files and run_exp):
        hdr(img_list, exposure_times)
    
    
    # with st.sidebar:
    #     with st.expander("ASSIGNMENT-2", True):
    #         rad_select = st.radio("A-2", options=["MEDIAN AND BILATERAL", "AI DENOISE", "SNR", "LAPLACIAN FILTER", "EDGE STRENGTH"])
    #         radio_select = rad_select

    # match radio_select:
    #     case "MEDIAN AND BILATERAL":
    #         view_median_bilateral()
    #     case "AI DENOISE":
    #         view_ai_denoise()
    #     case "SNR":
    #         view_snr()
    #     case "LAPLACIAN FILTER":
    #         view_laplacian_filter()
    #     case "EDGE STRENGTH":
    #         view_edge_strength()

    assignment_3_current_parameters()