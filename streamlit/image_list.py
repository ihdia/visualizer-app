import streamlit as st
import cv2 as cv
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

    fig = go.Figure(go.Image(z=image))
    fig.update_xaxes(showticklabels=False)
    fig.update_yaxes(showticklabels=False)

    fig.add_trace(go.Scatter(x=np.take(pts,0,axis=1),y=np.take(pts,1,axis=1),line_color='blue',name="GT-pts",visible='legendonly'))    
    fig.add_trace(go.Scatter(x=np.take(pts,0,axis=1),y=np.take(pts,1,axis=1),fill="toself",mode='none',name="GT-mask",fillcolor='rgba(128,0,128,0.3)',visible='legendonly'))
    fig.add_trace(go.Scatter(x=np.take(encoder_pts,0,axis=1),y=np.take(encoder_pts,1,axis=1),line_color='green',name='encoder output',visible='legendonly'))
    fig.add_trace(go.Scatter(x=np.take(encoder_pts,0,axis=1),y=np.take(encoder_pts,1,axis=1),fill="toself",mode='none',name="MCNN-mask",fillcolor='rgba(255,255,0,0.3)',visible='legendonly'))
    fig.add_trace(go.Scatter(x=np.take(gcn_pts,0,axis=1),y=np.take(gcn_pts,1,axis=1),line_color='red',name='GCN output',visible='legendonly'))
    
    
    return fig,label,iou,hd
