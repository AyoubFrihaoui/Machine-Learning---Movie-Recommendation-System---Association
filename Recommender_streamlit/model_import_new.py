import pandas as pd
import pickle


try:
    item_similarity_df = pd.read_csv('Item_similarity_df.csv', index_col=0)  # Adjust the filename and path as needed
except FileNotFoundError:
    print("Collaborative filtering model not found. Please generate the model first.")
    # Optionally, you can include code here to generate the rules if not found



def get_movie_recommendations(movie_name, item_similarity_df):
    similar_scores = item_similarity_df[movie_name]
    similar_movies = similar_scores.sort_values(ascending=False).index
    
    recommended_movies = [movie for movie in similar_movies if movie != movie_name]
    return recommended_movies[0:21]








