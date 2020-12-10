import streamlit as st
import cv2 as cv
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

def app(image_path,info,gt_pts,gt_mask):
    image = cv.imread(image_path)
    
    label = info['label']
    comp = info['components'][0]
    bbox = comp['bbox']
    pts = np.array(comp['poly'],dtype='int32')

    x0 = max(int(bbox[0]),0)
    y0 = max(int(bbox[1]),0)
    w = max(int(bbox[2]),0)
    h = max(int(bbox[3]),0)
    
    if x0 - 6 > 0 and y0-2 > 0:    
        image = image[y0-2:y0+h+2,x0-6:x0+w+6]
        pts[:,0] = pts[:,0] + 6
        pts[:,1] = pts[:,1] + 2
        bbox[2] = bbox[2] + 12
        bbox[3] = bbox[3] + 4
        w = w + 12
        h = h + 4
    else:
        image = image[y0:y0+h,x0:x0+w]

    pts[:,0] -= x0
    pts[:,1] -= y0

    # image = image[y0:y0+h,x0:x0+w,:]
    # print(image.shape)
    
    if(gt_pts):
        image = cv.polylines(image,[pts],True,(0, 0, 255),1)

    if(gt_mask):
        overlay = image.copy()
        overlay = cv.fillPoly(overlay,[pts],color=(255,0,0))

        alpha = 0.3
        image = cv.addWeighted(overlay,alpha,image,1-alpha,0)

        

    image = cv.cvtColor(image,cv.COLOR_RGB2BGR)

    # fig = px.imshow(image,width=image.shape[1],height=image.shape[0])
    fig = go.Figure(go.Image(z=image))
    fig.update_xaxes(showticklabels=False)
    fig.update_yaxes(showticklabels=False)

    

    return fig,label

# image = cv2.imread(i_url)
# w_image, h_image = image.shape[1], image.shape[0]

# image1 = imread(i_url)
        
# label = instance['label']
# bbox = component['bbox']
# x0 = max(int(bbox[0]),0)
# y0 = max(int(bbox[1]),0)
# w = max(int(bbox[2]),0)
# h = max(int(bbox[3]),0)
# pts = component["pts"]
# pts2 = component["pts"]

# bbox1 = bbox

# pts = np.asarray(pts)

# if x0 - 6 >= 0 and y0-2 >=0:    
#     image = image[y0-2:y0+h+2,x0-6:x0+w+6]
#     image1 = image1[y0-2:y0+h+2,x0-6:x0+w+6]
#     pts[:,0] = pts[:,0] + 6
#     pts[:,1] = pts[:,1] + 2
#     bbox[2] = bbox[2] + 12
#     bbox[3] = bbox[3] + 4
#     w = w + 12
#     h = h + 4
# else:
#     image = image[y0:y0+h,x0:x0+w]
#     image1 = image1[y0:y0+h,x0:x0+w]


# pts = np.array(pts).astype(np.float)
# pts2 = np.array(pts2).astype(np.float)

# old_pts = copy.deepcopy(pts)

# pts[:,0] = pts[:,0] - x0
# pts[:,1] = pts[:,1] - y0

# if x0 - 6 >= 0 and y0-2 >=0:
#     x0 = x0 - 6
#     y0 = y0 - 2

# actual_gt_pts11 = pts.tolist()
# actual_gt_pts11 = np.array(actual_gt_pts11)

# pts4 = pts
