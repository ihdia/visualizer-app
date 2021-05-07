import streamlit as st
import SessionState

def app():
    state = SessionState._get_state()

    if state.a is None:
        state.a = 0

    a = st.slider("test",0,100)
    st.write(str(a))

    state.sync()
