import streamlit as st
import cv2 as cv
from PIL import Image
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

class BNetImage:

    def __init__(self,path,info):
        self.path = path
        self.image = []
        self.info = info
        self.label = ""
        self.bbox = []
        self.pts = []
        self.encoder_pts = []
        self.gcn_pts = []
        self.iou = 0
        self.hd = float('inf')
    
    def ProcessInfo(self):
        self.image = cv.imread(self.path)
        self.label = self.info['label']
        self.bbox = self.info['bbox'][0]
        self.info['poly'][0].append(self.info['poly'][0][0])
        self.pts = np.array(self.info['poly'][0],dtype='int32')
        self.encoder_pts = np.array(self.info['encoder_output'],dtype='int32')
        self.gcn_pts = np.array(self.info['gcn_output'])
        self.iou = round(self.info['iou'],4)
        self.hd = round(self.info['hd'],4)
    
    def RenderImage(self):
        self.ProcessInfo()
        
        x0 = max(int(self.bbox[0]),0)
        y0 = max(int(self.bbox[1]),0)
        w = max(int(self.bbox[2]),0)
        h = max(int(self.bbox[3]),0)

        if x0 - 6 > 0 and y0-2 > 0:    
            self.image = self.image[y0-2:y0+h+2,x0-6:x0+w+6]
            self.pts[:,0] += 6
            self.pts[:,1] +=  2
            self.encoder_pts[:,0] += 6
            self.encoder_pts[:,1] += 2
            self.bbox[2] += 12
            self.bbox[3] += 4
            w += 12
            h += 4
            
        else:
            self.image = self.image[y0:y0+h,x0:x0+w]

        self.pts[:,0] -= x0
        self.pts[:,1] -= y0

        # simplified_pts = simplify_coords(pts,1.0)

        self.image = cv.cvtColor(self.image,cv.COLOR_RGB2BGR)
        pil_image = Image.fromarray(self.image)

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

        self.fig = go.Figure()
        actual_height, actual_width, _ = self.image.shape
        
        if(self.label[0] == "Boundary Line"):
            img_width = actual_width
            img_height = actual_height
            scale_factor = 3
        
        elif(actual_width / actual_height < 15 and not self.label[0] == "Character Line Segment"):
            img_width = 1600
            img_height = 900
            scale_factor = 0.5
            
        # else:
        elif self.label[0] == "Character Line Segment":

            # Special zoom
            img_width = 1300
            img_height = 200
            scale_factor = 1

        # print(np.take(pts,0,axis=1) * img_width * scale_factor / actual_width)
        x_zoom = (np.take(self.pts,0,axis=1) * img_width * scale_factor / actual_width)
        y_zoom = img_height * scale_factor - (np.take(self.pts,1,axis=1) * img_height * scale_factor / actual_height)
        
        x_zoom_encoder = np.take(self.encoder_pts,0,axis=1) * img_width * scale_factor / actual_width
        y_zoom_encoder = img_height * scale_factor - (np.take(self.encoder_pts,1,axis=1) * img_height * scale_factor / actual_height)

        x_zoom_gcn = np.take(self.gcn_pts,0,axis=1) * img_width * scale_factor / actual_width
        y_zoom_gcn = img_height * scale_factor - (np.take(self.gcn_pts,1,axis=1) * img_height * scale_factor / actual_height)

        x_axis_range = img_width * scale_factor
        y_axis_range = img_height * scale_factor

        self.fig.add_trace(go.Scatter(x = x_zoom,y = y_zoom,line_color='blue',name="GT-line",visible='legendonly'))
        self.fig.add_trace(go.Scatter(x = x_zoom,y = y_zoom,name="GT-pts",visible='legendonly',mode='markers',marker_color='rgb(0,180,255)'))    
        self.fig.add_trace(go.Scatter(x = x_zoom,y = y_zoom,fill="toself",mode='none',name="GT-mask",fillcolor='rgba(128,0,128,0.3)',visible='legendonly'))
        self.fig.add_trace(go.Scatter(x= x_zoom_encoder,y=y_zoom_encoder,line_color='green',name='encoder output',visible='legendonly'))
        self.fig.add_trace(go.Scatter(x= x_zoom_encoder,y=y_zoom_encoder,name='encoder pts',visible='legendonly',mode='markers',marker_color='rgba(0,255,0,1)'))
        self.fig.add_trace(go.Scatter(x= x_zoom_encoder,y=y_zoom_encoder,fill="toself",mode='none',name="MCNN-mask",fillcolor='rgba(255,255,0,0.3)',visible='legendonly'))
        self.fig.add_trace(go.Scatter(x= x_zoom_gcn,y=y_zoom_gcn,line_color='red',name='GCN lines',visible='legendonly'))
        self.fig.add_trace(go.Scatter(x= x_zoom_gcn,y=y_zoom_gcn,name='GCN pts',visible='legendonly',mode='markers',marker_color='rgba(255,128,0,1)'))


        # Configure axes
        self.fig.update_xaxes(
            visible=False,
            range=[0, x_axis_range]
        )
        
        self.fig.update_yaxes(
            visible=False,
            range=[0, y_axis_range],
            # the scaleanchor attribute ensures that the aspect ratio stays constant
            scaleanchor="x"
        )

        # Add image
        self.fig.add_layout_image(
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
        self.fig.update_layout(
            width=img_width * scale_factor,
            height=img_height * scale_factor,
            margin={"l": 0, "r": 0, "t": 0, "b": 0},
        )

        # fig.update_layout(legend_x = 0,legend_y=0)
        self.fig.update_layout(legend=dict(
            orientation="h",
            # xanchor="center",
            yanchor="top",
            y=-0.1, 
            x=0   
        ))

        
        return self.fig,self.label,self.iou,self.hd




    


