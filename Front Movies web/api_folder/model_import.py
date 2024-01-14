import pandas as pd
import pickle


links = pd.read_csv('links.csv')
# Import the mappings using pickle
with open('movie_mappings.pkl', 'rb') as f:
    id_to_name_mapping, name_to_id_mapping = pickle.load(f)

# Now you can use id_to_name_mapping and name_to_id_mapping in your code

# Load the association rules model
try:
    resultsinDataFrame = pd.read_csv('association_rules.csv')  # Adjust the filename and path as needed
except FileNotFoundError:
    print("Association rules model not found. Please generate the rules first.")
    # Optionally, you can include code here to generate the rules if not found

# Define the recommendations function
def recommendations(film, count=20):
    if 'resultsinDataFrame' not in globals():
        print("Association rules model not loaded. Please load the model first.")
        return []
    if not (film  in links['tmdbId'].values):
        print('this film is not in our dataset')
        return []
    #map tmdbId to our movieId
    row = links.loc[links['tmdbId'] == film, 'movieId'].iloc[0]
    #print(row)
    movieId = row
    result = resultsinDataFrame[(resultsinDataFrame['Item #1'] == movieId) | (resultsinDataFrame['Item #2'] == movieId)] \
        .nlargest(n=count, columns='Support')
    modified_results = result.copy()
    mask = modified_results['Item #2'] == movieId
    modified_results.loc[mask, 'Item #2'] = modified_results.loc[mask, 'Item #1']
    recommendations = modified_results[["Item #2", "Support"]]
    return recommendations["Item #2"].tolist()

# Define the recommendations_name function
def recommendations_tmdbIds(film):
    #result_ids = recommendations(name_to_id_mapping.get(film))
    result_ids = recommendations(film)
    result_tmdbIds = list(map(int, links.loc[links['movieId'].isin(result_ids), 'tmdbId'].tolist()))
    #result_titles = []
    #for film_id in result_ids:
    #    result_titles.append(id_to_name_mapping.get(film_id))
    return result_tmdbIds

# Example usage
film_recommendations = recommendations_tmdbIds(863)

print(film_recommendations)

