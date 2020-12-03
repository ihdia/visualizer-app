import image_list
import result

import streamlit as st
import numpy as np
import cv2
import pandas as pd


st.sidebar.title('Select Image')
image_selector = st.sidebar.selectbox('Select Images', [1,2,3])

analyze_button = st.sidebar.button('Analyze')

if(analyze_button):
    result.app(image_selector)
else:
    image_list.app()
