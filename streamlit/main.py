import image_list
import result
import SessionState

import streamlit as st
import numpy as np
import json
import os

# Loading jsons, directories need to be replaced aptly
with open('../ToolJson/test.json', 'r') as f:
    test_data = json.load(f)

with open('../ToolJson/train.json', 'r') as f:
    train_data = json.load(f)

with open('../ToolJson/val.json', 'r') as f:
    train_val_data = json.load(f)

session_state = SessionState.get(name='', counter=None)


def filter_json(value, session_state):
    if(value == 'Train'):
        data = train_data
    elif(value == 'Test'):
        data = test_data
    elif(value == 'Validation'):
        data = train_val_data
    else:
        session_state.counter = 1
        return 'null'

    return data

def filter_component(value,data,session_state):
    new_data = []

    # print(data[0].keys())

    for i in range(len(data)):
        if data[i]['label'][0] == value:
            new_data.append(data[i])
    print(new_data)
    return new_data



def update_image_info(data):

    counter = session_state.counter


    if(counter > 0 and len(data) > counter):
        info = data[counter]
        
        # Picking a random image from data, extracting location
        image_directory = data[counter]['image_url'][0][14:]
        image_directory = image_directory.replace("%20"," ")

        # Finding image path. To be replaced with server directiory
        image_path = '../new_jpg_data' + image_directory
        print(image_path)
    else:
        return 'null', 'null'


    return info, image_path



# Sidebar elements
st.sidebar.title('Select Image')
image_selector = st.sidebar.radio('Image Type', ['None', 'Train', 'Test', 'Validation'])
component_selector = st.sidebar.selectbox(
    'Select component type ',
    ('Character Component','Page Boundary','Character Line Segment','Boundary Line','Physical Degradation',
    'Library Marker','Picture / Decorator')
)


# if st.sidebar.button('Prev'):
#     session_state.counter -= 1
# if st.sidebar.button('Next'):
#     session_state.counter += 1

c1,c2 = st.sidebar.beta_columns(2)
p = c1.button('Prev')
n = c2.button('Next')

if p:
    session_state.counter -= 1
if n:
    session_state.counter += 1

json_selected = filter_json(image_selector, session_state)

if json_selected == 'null':
    st.title('Select an option')

else:
    json_selected = filter_component(component_selector,json_selected,session_state)

    info, image_path = update_image_info(json_selected)

    print(info)
    print(image_path)


    if(info != 'null'):
        # st.title('Image list')
        # c1,c2 = st.beta_columns(2)
        
        st.sidebar.write('\nSelect outputs to show')
        gt_pts = st.sidebar.checkbox("GT-points")
        gt_mask = st.sidebar.checkbox("GT-mask")

        fig,label = image_list.app(image_path,info,gt_pts,gt_mask)
        
        st.write(label[0])
        st.plotly_chart(fig)

    else:
        st.title('Image not found')


    # if(info == 'null'):
    #     st.title('Select an option')
