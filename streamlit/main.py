import image_list
import SessionState

import streamlit as st
import numpy as np
import json
import os
from copy import deepcopy

# TODO : replace test back to test data from train data

@st.cache(allow_output_mutation=True)
def get_json_data():
    with open('../ToolJson/train.json', 'r') as f:
        test_data = json.load(f)

    with open('../ToolJson/train.json', 'r') as f:
        train_data = json.load(f)

    with open('../ToolJson/val.json', 'r') as f:
        train_val_data = json.load(f)
    return test_data,train_data,train_val_data


# Gets current state of app, so that session variables such as counter are preserved after the app restarts

state = SessionState._get_state()
test_data,train_data,train_val_data = get_json_data()


# Filters data based on user selection (Test, Train, Validation)

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


# Filters data based on user selection (CLS,CC,Page Boundary, etc)    

def filter_component(value,data):
    new_data = []

    for i in range(len(data)):
        if data[i]['label'][0] == value:
            new_data.append(data[i])
    return new_data


# Returns image based on current counter value (which stores the current index of image being viewed)

def update_image_info(data):

    if(state.counter > 0 and len(data) > state.counter):
        info = data[state.counter]
        
        image_directory = data[state.counter]['image_url'][0][14:]
        image_directory = image_directory.replace("%20"," ")
        image_path = '../new_jpg_data' + image_directory

    else:
        return 'null', 'null'

    return info, image_path


# Sorts data by iou or hd, showing worst results first

def sort_data(data,inp):
    if inp=='iou':
        data = sorted(data,key=lambda k: k['iou'],reverse=False)
    elif inp=='hd':
        data = sorted(data,key=lambda k: k['hd'],reverse=True)
    
    return data


# Saves current image path, along with IOU and HD values in filenames.txt for later reference

def save_path(image_path,iou,hd,ttv,index):
    with open("saved_paths.txt","a") as f:
        f.write(image_path+"\tiou: "+str(iou)+"\thd: "+str(hd)+"\t"+ttv+"\tindex: "+str(index)+"\n\n")



# MAIN APP LAYOUT

st.title('Layer Visualizer')
image_selector = st.radio('Image Type', ['Train', 'Test', 'Validation'])

component_selector = st.selectbox(
    'Select component type ',
    ('Character Line Segment','Character Component','Page Boundary','Boundary Line','Physical Degradation',
    'Library Marker','Picture / Decorator')
)

json_selected = filter_json(image_selector)

sort_by = st.selectbox(
    'Sort by (iou, hd)',
    ('iou','hd')
)

json_selected = filter_component(component_selector,json_selected)
json_selected = sort_data(json_selected,sort_by)


# Index selection 

sl = st.empty()
state.counter = sl.slider("Select image",1,len(json_selected)-1,state.counter)

c1,c2 = st.beta_columns(2)

p = c1.button('Prev')
n = c2.button('Next')

if p:
    state.counter -= 1

if n:
    state.counter += 1

ind = int(st.text_input("Enter index value here: ",state.counter))
if ind and ind in range(1,len(json_selected)):
    state.counter = ind


# Display image and relevant data based on index selected

info, image_path = update_image_info(json_selected)
# print(image_path)

if(info != 'null'):    
    fig,label,iou,hd = image_list.app(image_path,info)

    st.plotly_chart(fig)

    st.write("IOU: "+str(iou))
    st.write("HD: "+str(hd))

else:
    st.title('Image not found')

if st.button("Save for later"):
    save_path(image_path,iou,hd,image_selector,state.counter)


state.sync()        # Essential to avoid widget rollbacks after page refresh 