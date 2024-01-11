import pandas as pd
import pickle

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

    result = resultsinDataFrame[(resultsinDataFrame['Item #1'] == film) | (resultsinDataFrame['Item #2'] == film)] \
        .nlargest(n=count, columns='Support')
    modified_results = result.copy()
    mask = modified_results['Item #2'] == film
    modified_results.loc[mask, 'Item #2'] = modified_results.loc[mask, 'Item #1']
    recommendations = modified_results[["Item #2", "Support"]]
    return recommendations["Item #2"].tolist()

# Define the recommendations_name function
def recommendations_name(film):
    result_ids = recommendations(name_to_id_mapping.get(film))
    result_titles = []
    for film_id in result_ids:
        result_titles.append(id_to_name_mapping.get(film_id))
    return result_titles

# Example usage
<<<<<<< HEAD

=======
film_recommendations = recommendations_name('Titanic')

print(film_recommendations)
>>>>>>> 8a4a808819e7b71daa0767d8ab90b4c2ba03f767

