import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import mean_squared_error, mean_absolute_error, precision_score, recall_score, f1_score
import streamlit as st
import numpy as np

# Read user-item matrix
st.set_page_config(
    page_title="Ml training evaluation ",
    initial_sidebar_state='expanded',
    layout='wide'
)
user_item_matrix = pd.read_csv("user_item_matrix.csv", index_col=0)
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def collaborative_filtering_training(user_item_matrix):
    # Display user-item matrix
    st.header("User-Item Matrix:")
    st.dataframe(user_item_matrix.head())

    # Fill missing values and normalize user-item matrix
    user_item_matrix = user_item_matrix.fillna(0)
    user_item_matrix_normalized = user_item_matrix.apply(lambda x: x - x.mean(), axis=1)

    # Calculate item similarity
    item_similarity = cosine_similarity(user_item_matrix_normalized.T)
    item_similarity_df = pd.DataFrame(item_similarity, index=user_item_matrix.columns, columns=user_item_matrix.columns)

    # Save item_similarity_df to CSV
    item_similarity_df.to_csv("Item_similarity_df.csv", index=True, header=True)

    # Display item similarity matrix
    st.header("Item Similarity Matrix:")
    st.dataframe(item_similarity_df.head())

    # Evaluation
    st.header("Model Evaluation")

    # Assuming you have a test set with known user-item interactions
    # Replace this with your actual test set
    test_set = user_item_matrix.copy()

    # Make predictions based on the item similarity matrix
    predicted_ratings = user_item_matrix_normalized.dot(item_similarity)

    # Replace NaN values with zeros using numpy
    predicted_ratings = np.nan_to_num(predicted_ratings)

    # Normalize predicted ratings by dividing each rating by the sum of the corresponding item similarity column
    item_similarity_sums = np.sum(np.abs(item_similarity), axis=0)
    normalized_predicted_ratings = predicted_ratings / item_similarity_sums

    # Display predicted ratings matrix
    st.header("Normalized Predicted Ratings Matrix:")
    st.dataframe(pd.DataFrame(normalized_predicted_ratings, index=user_item_matrix.index, columns=user_item_matrix.columns))

    # Mask to consider only the test set interactions
    mask = test_set.notna()

    # Extract only the values present in both matrices
    test_values = test_set[mask].values.flatten()
    predicted_values = normalized_predicted_ratings[mask].flatten()

    # Calculate MSE, RMSE, MAE for only the observed values
    mse = mean_squared_error(test_values, predicted_values)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(test_values, predicted_values)

    # Calculate additional metrics
    precision = precision_score(test_values > 0, predicted_values > 0)
    recall = recall_score(test_values > 0, predicted_values > 0)
    f1 = f1_score(test_values > 0, predicted_values > 0)

    # Display evaluation metrics
    st.write(f"Mean Squared Error (MSE)",mse)
    st.write(f"Root Mean Squared Error (RMSE):",rmse)
    st.write(f"Mean Absolute Error (MAE):",mae)
    st.write(f"Precision:",precision)
    st.write(f"Recall:",recall)
    st.write(f"F1 Score:",f1)

    # Display training results
    st.header("Collaborative Filtering Training")
    st.write("Training completed. Item Similarity Matrix saved to 'Item_similarity_df.csv'.")

    return item_similarity_df

# Execute collaborative filtering training
item_similarity_matrix = collaborative_filtering_training(user_item_matrix)
