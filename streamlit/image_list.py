import streamlit as st
import matplotlib.pyplot as pl

def app():
    image = pl.imread('https://matplotlib.org/2.1.1/_images/sphx_glr_image_clip_path_thumb.png')


    st.title('Image list')
    with st.beta_container():
        st.write('Image 1')
        st.image(image)
        st.write('Image 2')
        st.image(image)
        st.write('Image 3')
        st.image(image)
