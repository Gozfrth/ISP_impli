# TODO:
# After adding AMAT in csv, provide option to plot any of the 3 (hit, miss, AMAT) against each other, instead of the hit v misscount right now

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plot_cache_data
from DEMOSAIC import load_raw_image, display_interactive_plot
import plotly.express as px

def plot_cache_data(csv_file, output_png, field):
    data = pd.read_csv(csv_file)

    # 'MissCount', 'HitCount', 'AMAT', 'MissRatio'
    plt.figure(figsize=(15, 9))
    plt.plot(data['Step'], data[field], label=field)
    plt.xlabel('Step')
    plt.ylabel('Count')
    plt.title(f'{field} Over Time')
    plt.legend()
    plt.grid(True)

    st.pyplot(plt)

def run_cache(execution, max_size, k, block_size, step_size, display, iterations):
    subprocess.call(["g++", f"{execution}.cpp"])
    req_output = subprocess.run(["./a.out", "--max_size", str(max_size), "--k", str(k), "--block_size", str(block_size), "--step_size", str(step_size), "--display", str(display), "--iterations", str(iterations)], capture_output = True, text = True)
    return req_output.stdout

    
def view_raw_image():
    image_data, image_data_display = load_raw_image()
    display_interactive_plot(image_data)
    print(image_data.shape)

def main():
    st.set_page_config(layout="wide")

    add_selectbox = st.sidebar.selectbox(
        "Select Stage of ISP",
        ("DEMOSAIC", "SOMETHNG", "SOMETHING")
    )

    st.markdown("""<hr style="border:3px solid rgb(255,255,255) ">""", unsafe_allow_html=True)
    st.markdown("""# ASSIGNMENT 1""")
    st.markdown("""<hr style="border:3px solid rgb(255,255,255) ">""", unsafe_allow_html=True)

    # MAXSIZE_input = st.number_input("Enter MAX SIZE of cache (bytes)", value=512)
    # K_input = st.number_input("Enter the value of K", value=4)
    # BLOCKSIZE_input = st.number_input("Enter the block size (bytes)", value=32)
    # STEP_input = st.number_input("Enter the step size ", value=10)
    # ITERATIONS_input = st.number_input("Enter the number of iterations", value = 250)

    if add_selectbox == "DEMOSAIC":
        view_raw = st.checkbox("View Raw?", value=False)

        if view_raw:
            view_raw_image()


    # options = st.multiselect("Select fields", ['MissCount', 'HitCount', 'AMAT', 'MissRatio'], ['MissRatio', 'AMAT'])

    # st.write("You selected:", options)


    # if(not (is_power_of_two(K_input))):
    #     st.error(f"{K_input} is not a power of 2")

    # if st.button(label="SIMULATE"):
    #     if(execution == None):
    #         st.error("Enter an execution method")
    #         return

    #     st.markdown("""<hr style="border:3px solid rgb(255,255,255) ">""", unsafe_allow_html=True)
    #     output = run_cache(execution=execution, max_size=MAXSIZE_input, k=K_input, block_size=BLOCKSIZE_input, step_size=STEP_input, display = display_input and (MAXSIZE_input <= 128), iterations = ITERATIONS_input)

    #     for field in options:
    #         st.markdown(f"""### {field}:""")
    #         plot_cache_data(f"{execution}.csv", f"{execution}", field) 
    #     # remove {execution.csv} here
        
    #     st.markdown("""<hr style="border:3px solid rgb(255,255,255) ">""", unsafe_allow_html=True)
    #     st.markdown("""### TERMINAL OUTPUT:""")
    #     st.text(output)

if __name__ == "__main__":
    main()