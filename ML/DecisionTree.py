import os
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from ML.UrlFeaturizer import UrlFeaturizer
import joblib

def train_and_test_decision_tree_model(csv_path):
    # Load the dataset
    df = pd.read_csv(csv_path)

    # Initialize an empty list to store the features
    X = []

    # Extract features using the UrlFeaturizer for each URL in the dataset
    for url in df['href']:
        featurizer = UrlFeaturizer(url)
        features = featurizer.run()
        X.append(features)

    # Convert features to a DataFrame
    X = pd.DataFrame(X)

    # Ensure baseUrlID is included in features
    assert 'baseUrlID' in X.columns, "baseUrlID is missing from the features."

    # Extract labels from the dataset
    y = df['is_exhibition']

    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Initialize dictionary to store trees and their performance
    trees = {}
    performances = {}

    # Create a directory to store the tree visualizations
    tree_visualization_dir = 'decision_tree_visualizations'
    os.makedirs(tree_visualization_dir, exist_ok=True)

    # Split the training data based on baseUrlID and train separate trees
    for baseUrlID in X_train['baseUrlID'].unique():
        # Filter the training data
        train_mask = X_train['baseUrlID'] == baseUrlID
        X_train_filtered = X_train[train_mask].drop(columns=['baseUrlID'])
        y_train_filtered = y_train[train_mask]

        # Filter the testing data
        test_mask = X_test['baseUrlID'] == baseUrlID
        X_test_filtered = X_test[test_mask].drop(columns=['baseUrlID'])
        y_test_filtered = y_test[test_mask]

        # Skip training if there is not enough data for a particular baseUrlID
        if len(X_train_filtered) < 2 or len(X_test_filtered) < 1:
            print(f"Not enough data for baseUrlID {baseUrlID}, skipping...")
            continue

        # Initialize and train a Decision Tree model
        dt_model = DecisionTreeClassifier(
            criterion='entropy',  # Use 'entropy' or 'gini'
            max_depth=None,       # No maximum depth
            min_samples_split=2,  # Minimum number of samples to split a node
            min_samples_leaf=1,   # Minimum number of samples at a leaf node
            max_features=None,    # Consider all features
            random_state=42
        )
        dt_model.fit(X_train_filtered, y_train_filtered)
        trees[baseUrlID] = dt_model

        # Predict on the filtered testing set
        y_pred_filtered = dt_model.predict(X_test_filtered)

        # Evaluate and store the performance
        accuracy = accuracy_score(y_test_filtered, y_pred_filtered)
        performances[baseUrlID] = accuracy

        print(f"baseUrlID {baseUrlID} -> Accuracy: {accuracy:.2f}")

        # Save the tree visualization
        plt.figure(figsize=(20, 10))
        plot_tree(dt_model, filled=True, feature_names=X_train_filtered.columns, class_names=['not exhibition', 'exhibition'])
        plt.title(f'Decision Tree for baseUrlID = {baseUrlID}')
        tree_path = os.path.join(tree_visualization_dir, f'decision_tree_baseUrlID_{baseUrlID}.png')
        plt.savefig(tree_path)
        plt.close()

    # Save the models and featurizer along with feature names
    model_dir = 'models'
    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir, 'decision_tree_models.pkl')
    featurizer_path = os.path.join(model_dir, 'featurizer.pkl')
    joblib.dump(trees, model_path)
    feature_names = X_train.columns.tolist()
    with open(featurizer_path, 'wb') as f:
        joblib.dump((featurizer, feature_names), f)  # Store feature names from DataFrame columns

    return trees, performances

def predict_url(url):
    # Load the model and featurizer with feature names
    model_path = r'C:\Users\misza\OneDrive\Documents\Work\Personal Projects\Gallery Scraper\ML\models\decision_tree_models.pkl'
    featurizer_path = r'C:\Users\misza\OneDrive\Documents\Work\Personal Projects\Gallery Scraper\ML\models\featurizer.pkl'
    with open(featurizer_path, 'rb') as f:
        featurizer, feature_names = joblib.load(f)

    # Initialize the UrlFeaturizer with the new URL
    featurizer.path = url

    # Extract features for the new URL
    features = featurizer.run()

    # Convert features to a DataFrame
    features_df = pd.DataFrame([features])

    # Select features based on their names
    X = features_df[feature_names]

    # Load the models
    trees = joblib.load(model_path)

    # Select the appropriate model based on baseUrlID
    baseUrlID = features['baseUrlID']
    model = trees.get(baseUrlID)

    if model is None:
        print(f"No model found for baseUrlID {baseUrlID}")
        return None

    # Make prediction using the selected model
    prediction = model.predict(X.drop(columns=['baseUrlID']))

    return prediction[0]

# Example usage
def main():
    # Paths
    csv_path = r'C:\Users\misza\OneDrive\Documents\Work\Personal Projects\Gallery Scraper\ML\training_data\exhibition_href_training.csv'

    # Train the model
    trees, performances = train_and_test_decision_tree_model(csv_path)

    # Print overall performance
    print("\nOverall Performance by baseUrlID:")
    for baseUrlID, accuracy in performances.items():
        print(f"baseUrlID {baseUrlID}: Accuracy = {accuracy:.2f}")

    # Example URL predictions
    exhibition_urls = [
        'https://www.barbican.org.uk/whats-on/2024/event/this-exhibition',
        'https://www.lissongallery.com/exhibitions/otobong-nkanga',
        'https://www.southbankcentre.co.uk/whats-on/art-exhibitions/secondary-schools-morning-tavares-strachan?eventId=985129'
    ]

    non_exhibition_urls = [
        'https://www.barbican.org.uk/whats-on/past/event/this-exhibition',
        'https://www.barbican.org.uk/about',
        'https://www.southbankcentre.co.uk/',
        'https://www.southbankcentre.co.uk/whats-on'
    ]

    print('\nExhibition URLs:')
    for url in exhibition_urls:
        result = predict_url(url)
        print(f"{url} -> {'Exhibition' if result else 'Not Exhibition'}")

    print('\nNon-Exhibition URLs:')
    for url in non_exhibition_urls:
        result = predict_url(url)
        print(f"{url} -> {'Exhibition' if result else 'Not Exhibition'}")

if __name__ == "__main__":
    main()
