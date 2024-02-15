import streamlit as st
import requests
from model_import_new import get_movie_recommendations
import pandas as pd 



# Set Streamlit page configuration
st.set_page_config(
    page_title="Movies recommendation app",
    page_icon=':movie_camera:',
    initial_sidebar_state='expanded',
    layout='wide'
)
headers =  {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJlNjRlMjY2MjZlNWVjMzYwOGZhYTFhNmYyZmVhM2I5NSIsInN1YiI6IjY1YzBmMGY1YmE0ODAyMDE4MjZlYzEzMSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.-domdvJv_wqvrMytNl2hnpbPo9BTA9nNmCtzskY1tvA"
             }
item_similarity_df = pd.read_csv('Item_similarity_df.csv', index_col=0)

def tmdb_movie(movie_name):
     split_string = movie_name.split("a.k.a.")

# Get the name after "a.k.a."
     if len(split_string) > 1:
       return split_string[1][:-1].strip()
     else:
        return movie_name
    

# Load external CSS style
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Page title and introduction
st.title('Movie:red[Magnet]')
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<p style='font-size: 22px;'>Hi, welcome to <span style='color: red;'>MovieMagnet!</span> This free movie recommendation engine suggests films based on your interest with MovieMagnet.</p>", unsafe_allow_html=True)

# Dropdown for selecting a movie
selected_movie = st.text_input('Pick a Movie :')





# Button to recommend movies
if st.button('Recommend'):
    try:
        selected_movie=selected_movie.replace(selected_movie[0],selected_movie[0].upper(),1)
       
        selected_movie_request = requests.get(f"https://api.themoviedb.org/3/search/movie?api_key=e64e26626e5ec3608faa1a6f2fea3b95&query={tmdb_movie(selected_movie)}",headers=headers)
        selected_movie_request=selected_movie_request.json()
        selected_movie_request_list=selected_movie_request["results"]

        mainmovie=f""" 
    <body>
        <div class="movie-container">
            <h1 class="movie-name">{selected_movie_request_list[0]["title"]}</h1>
            <img class="movie-image" src="https://image.tmdb.org/t/p/w500/{selected_movie_request_list[0]["poster_path"]}" alt="Movie Image">
             <h5><span style='font-size: 18px;color: red' >Rating: </span>{round(selected_movie_request_list[0]['vote_average'], 1)}</h1>
        </div>
    </body>
"""
        
     
        st.markdown(mainmovie, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
       

        # Send API request
       
        list=get_movie_recommendations(selected_movie,item_similarity_df)
        
       
        

        
        movie_list=[]
        for i in list :  
            response = requests.get(f"https://api.themoviedb.org/3/search/movie?api_key=e64e26626e5ec3608faa1a6f2fea3b95&query={tmdb_movie(i)}",headers=headers)
            response=response.json()
            response_list=response["results"]
            movie=response_list[0]
            movie_list.append({"movie_name":movie["title"],
                               "movie_image":"https://image.tmdb.org/t/p/w500/"+movie["poster_path"],
                               "movie_rating":round(movie['vote_average'], 1)}
                               )



        

        # Sample list of movies
      

        # Streamlit app title
        st.subheader("Here are few Recommendations..")

        # Number of movies per row
        movies_per_row = 6

        # Calculate the number of rows
        num_rows = len(movie_list) // movies_per_row + (len(movie_list) % movies_per_row > 0)
        

        # Create a grid layout
        for i in range(num_rows):
            # Create columns for each movie in the current row
            cols = st.columns(movies_per_row)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            for j in range(movies_per_row):
                # Calculate the movie index in the list
                index = i * movies_per_row + j
                

                # Check if the index is within the movie list range
                if index < len(movie_list):
                    

                   
                    # Display movie information in each column
                    cols[j].image(movie_list[index]['movie_image'], use_column_width=True)
                    cols[j].markdown(f"<span style='font-size: 18px;color: red' > Name : </span>{movie_list[index]['movie_name']}", unsafe_allow_html=True)
                    cols[j].markdown(f"<span style='font-size: 18px;color: red' >Rating: </span> {movie_list[index]['movie_rating']}", unsafe_allow_html=True)
            
       


    except Exception as e:
        st.error(f"Error: {str(e)}")
