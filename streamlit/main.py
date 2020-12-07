import image_list
import result

import streamlit as st
import numpy as np
import cv2
import matplotlib.pyplot as pl
import json

with open('/home/bala/Desktop/iiith/visualizer-app/raw/test/combined_test_converted.json', 'r') as f:
    test_data = json.load(f)

with open('/home/bala/Desktop/iiith/visualizer-app/raw/train/combined_train_converted.json', 'r') as f:
    train_data = json.load(f)

with open('/home/bala/Desktop/iiith/visualizer-app/raw/train_val/combined_val_converted.json', 'r') as f:
    train_val_data = json.load(f)

st.write(train_val_data[20]['image_url'][22:])
#st.write(train_val_data[20])

image_path = '/home/bala/Desktop/iiith/visualizer-app/new_jpg_data/Bhoomi_data/images/AAVARNI VYAKHYA/GOML/991/19.jpg'

image = pl.imread(image_path)
st.image(image)

st.sidebar.title('Select Image')
image_selector = st.sidebar.selectbox('Select Images', [1,2,3])

analyze_button = st.sidebar.button('Analyze')

if(analyze_button):
    result.app(image_selector)
else:
    st.write('App')
   # image_list.app()
