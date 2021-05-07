import image_list
import PlotImage
import SessionState
import streamlit as st
import boundaryNetApp
import ocrApp
import fullyAutomaticApp

pages = {
    "Boundary Net":boundaryNetApp,
    "OCR":ocrApp,
    "Fully Automatic":fullyAutomaticApp
}

st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to", list(pages.keys()))
page = pages[selection]
page.app()

# state.sync()