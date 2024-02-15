import streamlit as st

st.set_page_config(page_title="movie recommendation system ",layout="wide")

with open('./style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
    
st.title("Movies Recommndation :red[system]")
home_page_description ="""
<p class="page_description">Presenting our movie recommendation system proposal powered by Collaborative filtering technique . Elevate user experience with personalized
recommendations, showcasing our proven success in
algorithmic innovation for dynamic entertainment
needs. </p>
"""
st.markdown(home_page_description,unsafe_allow_html=True)