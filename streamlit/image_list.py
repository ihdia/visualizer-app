import streamlit as st
import matplotlib.pyplot as pl

def app(image_path):
    image = pl.imread(image_path)


    st.title('Image list')
    with st.beta_container():
        st.write('Image 1')
        st.image(image)
