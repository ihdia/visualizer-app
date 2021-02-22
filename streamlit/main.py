import image_list
import result
import SessionState

import streamlit as st
import numpy as np
import json
import os
from copy import deepcopy

# Loading jsons, directories need to be replaced aptly.
# replace test with train after.

@st.cache(allow_output_mutation=True)
def get_json_data():
    with open('../ToolJson/train.json', 'r') as f:
        test_data = json.load(f)

    with open('../ToolJson/train.json', 'r') as f:
        train_data = json.load(f)

    with open('../ToolJson/val.json', 'r') as f:
        train_val_data = json.load(f)
    return test_data,train_data,train_val_data

state = SessionState._get_state()
test_data,train_data,train_val_data = get_json_data()

def filter_json(value):
    if(value == 'Train'):
        data = train_data
    elif(value == 'Test'):
        data = test_data
    elif(value == 'Validation'):
        data = train_val_data
    else:
        return 'null'

    return data

def filter_component(value,data):
    new_data = []

    for i in range(len(data)):
        if data[i]['label'][0] == value:
            new_data.append(data[i])
    return new_data



def update_image_info(data):

    if(state.counter > 0 and len(data) > state.counter):
        info = data[state.counter]
        
        image_directory = data[state.counter]['image_url'][0][14:]
        image_directory = image_directory.replace("%20"," ")
        image_path = '../new_jpg_data' + image_directory

    else:
        return 'null', 'null'


    return info, image_path

def sort_data(data,inp):
    if inp=='iou':
        data = sorted(data,key=lambda k: k['iou'],reverse=False)
    elif inp=='hd':
        data = sorted(data,key=lambda k: k['hd'],reverse=True)
    
    return data

st.title('Layer Visualizer')
image_selector = st.radio('Image Type', ['Train', 'Test', 'Validation'])
component_selector = st.selectbox(
    'Select component type ',
    ('Character Line Segment','Character Component','Page Boundary','Boundary Line','Physical Degradation',
    'Library Marker','Picture / Decorator')
)

json_selected = filter_json(image_selector)

# if json_selected == 'null':
#     st.title('Select an option')

# else:
sort_by = st.selectbox(
    'Sort by (iou, hd)',
    ('iou','hd')
)

json_selected = filter_component(component_selector,json_selected)
json_selected = sort_data(json_selected,sort_by)


sl = st.empty()
state.counter = sl.slider("Select image",1,len(json_selected)-1,state.counter)


info, image_path = update_image_info(json_selected)
print(image_path)



if(info != 'null'):    
    fig,label,iou,hd = image_list.app(image_path,info)

    st.plotly_chart(fig)

    st.write("IOU: "+str(iou))
    st.write("HD: "+str(hd))

else:
    st.title('Image not found')


c1,c2 = st.beta_columns(2)

p = c1.button('Prev')
n = c2.button('Next')

if p:
    state.counter -= 1

if n:
    state.counter += 1

state.sync()