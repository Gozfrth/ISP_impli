# TODO:
# REDUCE SESSION STATE JEEZ

# WHAT PATAMETERS CAN BE CHANGED FOR WHITE BALANCE IN THE UI?
# MAYBE TEMPERATURE?

import streamlit as st
import numpy as np
from ASSIGNMENT_3 import assignment_3
from ASSIGNMENT_2 import assignment_2
from ASSIGNMENT_1 import assignment_1

def main():
    print("------------------------------------------------------------------------------------------------------------")
    st.set_page_config(layout="wide")
    st.session_state.page = st.sidebar.selectbox(
        "SELECT ASSIGNMENT",
        ("ASSIGNMENT_1", "ASSIGNMENT_2", "ASSIGNMENT_3")
    )

    match st.session_state.page:
        case "ASSIGNMENT_1":
            assignment_1()
        case "ASSIGNMENT_2":
            assignment_2()
        case "ASSIGNMENT_3":
            assignment_3()
        case _:
            pass

if __name__ == "__main__":
    main()