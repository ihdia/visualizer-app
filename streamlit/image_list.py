import streamlit as st
import cv2 as cv
from PIL import Image

import numpy as np
import plotly.graph_objects as go
import plotly.express as px

def app(image_path,info):
    image = cv.imread(image_path)

    
    label = info['label']
    # comp = info['components'][0]
    bbox = info['bbox'][0]
    pts = np.array(info['poly'][0],dtype='int32')
    encoder_pts = np.array(info['encoder_output'],dtype='int32')
    gcn_pts = np.array(info['gcn_output'])
    iou = round(info['iou'],4)
    hd = round(info['hd'],4)

    x0 = max(int(bbox[0]),0)
    y0 = max(int(bbox[1]),0)
    w = max(int(bbox[2]),0)
    h = max(int(bbox[3]),0)
    
    if x0 - 6 > 0 and y0-2 > 0:    
        image = image[y0-2:y0+h+2,x0-6:x0+w+6]
        pts[:,0] = pts[:,0] + 6
        pts[:,1] = pts[:,1] + 2
        # encoder_pts[:,0] += 6
        # encoder_pts[:,1] += 2
        bbox[2] = bbox[2] + 12
        bbox[3] = bbox[3] + 4
        w = w + 12
        h = h + 4
    else:
        image = image[y0:y0+h,x0:x0+w]

    pts[:,0] -= x0
    pts[:,1] -= y0

    image = cv.cvtColor(image,cv.COLOR_RGB2BGR)
    pil_image = Image.fromarray(image)

    layout = go.Layout(
        autosize=False,
        width=1000,
        height=1000,
    
        xaxis= go.layout.XAxis(linecolor = 'black',
                              linewidth = 1,
                              mirror = True),
    
        yaxis= go.layout.YAxis(linecolor = 'black',
                              linewidth = 1,
                              mirror = True),
    
        margin=go.layout.Margin(
            l=50,
            r=50,
            b=100,
            t=100,
            pad = 4
        )
    )


    # Constants
    img_width = 1600
    img_height = 900
    scale_factor = 0.5

    fig = go.Figure()


    actual_height, actual_width, _ = image.shape
    x_zoom = (np.take(pts,0,axis=1) * img_width * scale_factor / actual_width)
    y_zoom = img_height * scale_factor - (np.take(pts,1,axis=1) * img_height * scale_factor / actual_height)

    print(x_zoom, y_zoom)


    fig.add_trace(go.Scatter(x=np.take(pts,0,axis=1) * img_width * scale_factor / actual_width,y=np.take(pts,1,axis=1) * img_height * scale_factor / actual_height,line_color='blue',name="GT-pts",visible='legendonly'))    
    fig.add_trace(go.Scatter(x = x_zoom,y = y_zoom,fill="toself",mode='none',name="GT-mask",fillcolor='rgba(128,0,128,0.3)',visible='legendonly'))
    fig.add_trace(go.Scatter(x=np.take(encoder_pts,0,axis=1),y=np.take(encoder_pts,1,axis=1),line_color='green',name='encoder output',visible='legendonly'))
    fig.add_trace(go.Scatter(x=np.take(encoder_pts,0,axis=1),y=np.take(encoder_pts,1,axis=1),fill="toself",mode='none',name="MCNN-mask",fillcolor='rgba(255,255,0,0.3)',visible='legendonly'))
    fig.add_trace(go.Scatter(x=np.take(gcn_pts,0,axis=1),y=np.take(gcn_pts,1,axis=1),line_color='red',name='GCN output',visible='legendonly'))


    # Configure axes
    fig.update_xaxes(
        visible=False,
        range=[0, img_width * scale_factor]
    )
    
    fig.update_yaxes(
        visible=False,
        range=[0, img_height * scale_factor],
        # the scaleanchor attribute ensures that the aspect ratio stays constant
        scaleanchor="x"
    )

    # Add image
    fig.add_layout_image(
        dict(
            x=0,
            sizex=img_width * scale_factor,
            y=img_height * scale_factor,
            sizey=img_height * scale_factor,
            xref="x",
            yref="y",
            opacity=1.0,
            layer="below",
            sizing="stretch",
            source=pil_image)
    )
    # Configure other layout
    fig.update_layout(
        width=img_width * scale_factor,
        height=img_height * scale_factor,
        margin={"l": 0, "r": 0, "t": 0, "b": 0},
    )



 
    
    return fig,label,iou,hd
