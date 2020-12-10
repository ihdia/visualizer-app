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




def update_image_info(value):

    if(value == 'Train'):
        data = train_data
    elif(value == 'Test'):
        data = test_data
    elif(value == 'Validation'):
        data = train_val_data
    else:
        return 'null', 'null'


    info = data[20]
    
    # Picking a random image from data, extracting location
    image_directory = data[20]['image_url'][22:]
    image_directory = image_directory.replace("%20"," ")
    
    
    # Finding image path. To be replaced with server directiory
    image_path = '../new_jpg_data' + image_directory

    return info, image_path


# Sidebar elements
st.sidebar.title('Select Image')
image_selector = st.sidebar.radio('Image Type', ['None', 'Train', 'Test', 'Validation'])

info, image_path = update_image_info(image_selector)


if(info != 'null'):
    st.title('Image list')
    print('INFO IS ', info)
    c1,c2 = st.beta_columns(2)
    
    gt_pts = c1.checkbox("GT-points")
    gt_mask = c1.checkbox("GT-mask")
    
    fig,label = image_list.app(image_path,info,gt_pts,gt_mask)
    
    c2.write(label)
    c2.plotly_chart(fig)
if(info == 'null'):
    st.title('Select an option')
