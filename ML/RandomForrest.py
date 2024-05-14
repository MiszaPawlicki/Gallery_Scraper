import os
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.tree import plot_tree
from ML.UrlFeaturizer import UrlFeaturizer
import joblib

# TODO refactor so loads only occur once

def train_random_forest_model(csv_path):
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

    # Extract labels from the dataset
    y = df['is_exhibition']

    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Initialize and train a Random Forest model
    rf_model = RandomForestClassifier()
    rf_model.fit(X_train, y_train)

    # Predict on the testing set
    y_pred = rf_model.predict(X_test)

    # Evaluate the model
    accuracy = accuracy_score(y_test, y_pred)
    print("Accuracy:", accuracy)
    print("Classification Report:")
    print(classification_report(y_test, y_pred))

    # Save the model and featurizer along with feature names
    model_dir = 'models'
    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir, 'random_forest_model.pkl')
    featurizer_path = os.path.join(model_dir, 'featurizer.pkl')
    joblib.dump(rf_model, model_path)
    feature_names = X.columns.tolist()
    with open(featurizer_path, 'wb') as f:
        joblib.dump((featurizer, feature_names), f)  # Store feature names from DataFrame columns

    # Print feature importance
    print("Feature Importance:")
    for i, importance in enumerate(rf_model.feature_importances_):
        print(f"{feature_names[i]}: {importance}")

        # Visualize the first tree
    plt.figure(figsize=(20, 10))
    plot_tree(rf_model.estimators_[0], filled=True, feature_names=feature_names,
              class_names=['not exhibition', 'exhibition'])
    plt.show()


def predict_url(url):
    # Load the model and featurizer with feature names
    model_path = r'C:\Users\misza\OneDrive\Documents\Work\Personal Projects\Gallery Scraper\ML\models\random_forest_model.pkl'
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

    # Load the model
    model = joblib.load(model_path)

    # Make prediction using the trained model
    prediction = model.predict(X)

    # Return the predicted class (0 or 1)
    return prediction[0]


# Example usage
def main():
    # Paths
    csv_path = r'C:\Users\misza\OneDrive\Documents\Work\Personal Projects\Gallery Scraper\ML\training_data\exhibition_href_training.csv'

    # Train the model
    train_random_forest_model(csv_path)

    url_to_predict = 'https://www.barbican.org.uk/whats-on/2024/event/this-exhibition'
    print(predict_url(url_to_predict))

    url_to_predict = 'https://www.barbican.org.uk/whats-on/past/event/this-exhibition'
    print(predict_url(url_to_predict))

    url_to_predict = 'https://www.barbican.org.uk/about'
    print(predict_url(url_to_predict))

    url_to_predict = 'https://www.lissongallery.com/exhibitions/otobong-nkanga'
    print(predict_url(url_to_predict))


if __name__ == "__main__":
    main()
