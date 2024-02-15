import streamlit as st

st.set_page_config(page_title="movie recommendation system ",layout="wide")

style = '''@import url("https://fonts.googleapis.com/css2?family=Source+Code+Pro:ital,wght@0,200..900;1,200..900&display=swap");
body {
  font-family: "Source Code Pro", monospace !important
  ;
}

body {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100vh;
  margin: 0;
  background-color: #121212;
}

.movie-container {
  text-align: center;
}
.page_description {
  font-size: 25px;
  font-weight: 500;
}

.movie-name {
  font-size: 30px;
  text-transform: uppercase;
  color: red;
}

.movie-image {
  width: 250px;
  height: 350px;
  margin-top: 10px; /* Adjust as needed for spacing between name and image */
  margin-bottom: 10px;
  border-radius: 10px;
  box-shadow: 11px 11px 23px -7px rgba(0, 0, 0, 0.4);
}'''

st.markdown(f'<style>{style}</style>', unsafe_allow_html=True)
    
    
st.title("Movies Recommndation :red[system]")
home_page_description ="""
<p class="page_description">Presenting our movie recommendation system proposal powered by Collaborative filtering technique . Elevate user experience with personalized
recommendations, showcasing our proven success in
algorithmic innovation for dynamic entertainment
needs. </p>
"""
st.markdown(home_page_description,unsafe_allow_html=True)