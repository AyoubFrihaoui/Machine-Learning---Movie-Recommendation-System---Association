import streamlit as st
import pandas as pd
import numpy as np
from joblib import Parallel, delayed
import seaborn as sns
import matplotlib.pyplot as plt
import warnings


st.set_page_config(
    page_title="Data preprocessing",
    layout='wide'
)
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Load the dataset
movies = pd.read_csv('ml-latest-small/movies.csv')
ratings = pd.read_csv('ml-latest-small/ratings.csv')

# Function to fix movie titles
def fix_movie_title(title):
    # Remove leading "The" or "A"
    if title.endswith(", The"):
        title = "The " + title[:-5]
    elif title.endswith(", A"):
        title = "A " + title[:-3]
    return title



# # Basic Statistics
# st.sidebar.header("Navigation")
# page = st.sidebar.radio("Go to", ("Preprocessing", "Training", "Slides"))

# if page == "Preprocessing":
#     st.sidebar.subheader("Preprocessing")
#     # Display preprocessing content
#     st.write("This is the preprocessing page.")
#     # Add your preprocessing content here.

# elif page == "Training":
#     st.sidebar.subheader("Training")
#     # Display training content
#     st.write("This is the training page.")
#     # Add your training content here.

# elif page == "Slides":
#     st.sidebar.subheader("Slides")
#     # Display slides content
#     st.write("This is the slides page.")
#     # Add your slides content here.


# Function for data preprocessing and EDA
def preprocess_and_eda(movies, ratings):
    # Merging movies and ratings
    df = pd.merge(ratings, movies, on='movieId', how='left')

    # EDA Steps
    st.title("Exploratory Data Analysis (EDA)")

    # Basic Statistics
    st.header("Basic Statistics")
    movies_count = df['movieId'].nunique()
    users_count = df['userId'].nunique()
    num_rows = df.shape[0]
    avg_ratings_per_user = num_rows / users_count

    st.write("Number of movies:", movies_count)
    st.write("Number of users:", users_count)
    st.write("Number of ratings:", num_rows)
    st.write("Average ratings per user:", avg_ratings_per_user)

    # Plot histogram of ratings per user
    st.subheader("Number of Ratings per User")
    ratings_per_user = df.groupby('userId')['movieId'].count()
    bins = [20, 30, 40, 50, 100, 200, 500, 1000, 2000, ratings_per_user.max()]
    hist, bins, _ = plt.hist(ratings_per_user, bins=bins, color='skyblue', edgecolor='black')
    plt.xscale('log')
    plt.xticks(rotation=45, ha='right')
    st.pyplot(plt)

    # Plot countplot to visualize the distribution of ratings
    st.subheader("Distribution of Ratings")
    with warnings.catch_warnings():
        warnings.simplefilter(action='ignore', category=FutureWarning)
        plt.figure(figsize=(12, 6))
        sns.countplot(x='rating', data=df, palette='viridis')
        plt.annotate(f'Total Ratings: {num_rows}', (0.5, 1), xycoords='axes fraction', ha='center', va='center')
        st.pyplot(plt)

    # Plot histogram of ratings per movie
    st.subheader("Distribution of Ratings per Movie")
    ratings_per_movie = df.groupby('movieId')['userId'].count()
    per_movie_ratings_count = ratings_per_movie.tolist()
    num_bins = 20
    custom_ranges = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 30, 40, 50, 100]
    plt.figure(figsize=(10, 6))
    plt.hist(per_movie_ratings_count, bins=custom_ranges, color='blue', edgecolor='black')
    plt.xlabel('Number of Ratings')
    plt.ylabel('Number of Movies')
    st.pyplot(plt)

    # Additional preprocessing steps
    st.header("Additional Preprocessing Steps")

    # Count movies above threshold
    num_movies_above_threshold = sum(count > 25 for count in per_movie_ratings_count)
    st.write("Number of movies with more than 25 ratings:", num_movies_above_threshold)

    # Identify and remove movies under the threshold
    movies_under_threshold = ratings_per_movie[ratings_per_movie < 25].index.tolist()
    len_movies_under_threshold = len(movies_under_threshold)
    st.write("Number of movies under the threshold (less than 25 ratings):", len_movies_under_threshold)

    movies = movies[~movies["movieId"].isin(movies_under_threshold)]
    df = pd.merge(ratings, movies, on='movieId', how='left')
    df = df[~df["movieId"].isin(movies_under_threshold)]

    # Calculate average rating per movie
    average_rating_per_movie = df.groupby('movieId')['rating'].mean()

    # Create bins for rating ranges
    bins = [i * 0.5 for i in range(11)]
    with warnings.catch_warnings():
        warnings.simplefilter(action='ignore', category=FutureWarning)
        # Bin the average ratings into ranges and count the number of movies in each range
        rating_ranges = pd.cut(average_rating_per_movie, bins, right=False)
        count_per_range = rating_ranges.value_counts().sort_index()

        # Plot the count of movies in each rating range
        st.subheader("Number of Movies in Average Rating Ranges")
        plt.figure(figsize=(12, 6))
        sns.barplot(x=count_per_range.index.astype(str), y=count_per_range.values, palette='viridis')
        plt.title('Number of Movies in Average Rating Ranges')
        plt.xlabel('Rating Range')
        plt.ylabel('Number of Movies')
        plt.xticks(rotation=45, ha='right')
        st.pyplot(plt)

    # Remove year from movie titles
    movies['title'] = movies['title'].str.replace(r'\s*\(\d{4}\)\s*$', '', regex=True)
    df = pd.merge(ratings, movies, on='movieId', how='left')
    # Fix movie titles
    st.subheader("Fixing Movie Titles")
    movies['title'] = movies['title'].apply(fix_movie_title)
    df = pd.merge(ratings, movies, on='movieId', how='left')
    # Drop unnecessary columns
    st.subheader("Dropping Unnecessary Columns")
    df.drop(['genres', 'timestamp'], axis=1, inplace=True)


    # st.sidebar.subheader("User-Item Matrix and Standardization")
    user_item_matrix = df.pivot_table(index="userId", columns="title", values="rating")
    user_means = user_item_matrix.mean(axis=1, skipna=True)
    standardized_user_item_matrix = user_item_matrix.sub(user_means, axis=0)

   

    return user_item_matrix , standardized_user_item_matrix , df

# Streamlit UI for data preprocessing and EDA
def data_preprocessing():
    # Call the preprocessing function
    user_item_matrix , standardized_user_item_matrix , processed_data = preprocess_and_eda(movies, ratings)

    # Display the processed data
    st.header("Processed Data")
    st.write(processed_data.head())
     # Display User-Item Matrix
    st.subheader("User-Item Matrix")
    st.write(user_item_matrix.head())

    # Display Standardized User-Item Matrix
    st.subheader("Standardized User-Item Matrix")
    st.write(standardized_user_item_matrix.head())
    standardized_user_item_matrix.to_csv("user_item_matrix.csv" , index=True)
# Run the Streamlit app
if __name__ == "__main__":
    data_preprocessing()
