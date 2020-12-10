import image_list
import result

import streamlit as st
import numpy as np
import json

# Loading jsons, directories need to be replaced aptly
with open('../raw/test/combined_test_converted.json', 'r') as f:
    test_data = json.load(f)

with open('../raw/train/combined_train_converted.json', 'r') as f:
    train_data = json.load(f)

with open('../raw/train_val/combined_val_converted.json', 'r') as f:
    train_val_data = json.load(f)

info = train_data[20]

# Picking a random image from train val, extracting location
image_directory = train_val_data[20]['image_url'][22:]
image_directory = image_directory.replace("%20"," ")

#st.write(image_directory)

# Finding image path. To be replaced with server directiory
image_path = '../new_jpg_data/' + image_directory

# Sidebar elements
st.sidebar.title('Select Image')
image_selector = st.sidebar.radio('Image Type', ['Train', 'Test', 'Validation'])

# analyze_button = st.sidebar.button('Analyze')

# if(analyze_button):
#     result.app(image_selector)
# else:
#     #st.write('App')





st.title('Image list')
    # st.image(image)

c1,c2 = st.beta_columns(2)

gt_pts = c1.checkbox("GT-points")
gt_mask = c1.checkbox("GT-mask")

fig,label = image_list.app(image_path,info,gt_pts,gt_mask)

c2.write(label)
c2.plotly_chart(fig)
