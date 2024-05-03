import os
import pandas as pd
from sklearn.linear_model import LogisticRegression
import joblib
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from ML.Featurizers import UrlFeaturizer

#TODO refactor so model is only loaded once
#TODO get rid of warning on prediction
#TODO add more features to improve performance

def train_logistical_regression_model(csv_path):

    # Load the dataset
    df = pd.read_csv(csv_path)

    # Initialize an empty list to store the features
    X = []

    # Initialize the UrlFeaturizer
    featurizer = UrlFeaturizer("")

    # Extract features using the UrlFeaturizer for each URL in the dataset
    for url in df['href']:
        featurizer.url = url
        features = featurizer.run()
        X.append(features)

    # Convert features to a DataFrame
    X = pd.DataFrame(X)

    # Extract labels from the dataset
    y = df['is_exhibition']

    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize and train a Logistic Regression model
    lr_model = LogisticRegression()
    lr_model.fit(X_train, y_train)

    # Predict on the testing set
    y_pred = lr_model.predict(X_test)

    # Evaluate the model
    accuracy = accuracy_score(y_test, y_pred)
    print("Accuracy:", accuracy)
    print("Classification Report:")
    print(classification_report(y_test, y_pred))

    # Save the model and featurizer
    model_dir = 'models'
    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir, 'logistic_regression_model.pkl')
    featurizer_path = os.path.join(model_dir, 'featurizer.pkl')
    joblib.dump(lr_model, model_path)
    joblib.dump(featurizer, featurizer_path)
    print("Model and featurizer saved!")



def predict_url(model, featurizer, url):
    # Initialize the UrlFeaturizer with the new URL
    featurizer.url = url

    # Extract features for the new URL
    features = featurizer.run()

    # Convert the features dictionary into a 2D array
    X = []
    for value in features.values():
        X.append(value)
    X = [X]  # Convert to a list of lists

    # Make prediction using the trained model
    prediction = model.predict(X)

    # Return the predicted class (0 or 1)
    return prediction[0]


def load_model():
    model = joblib.load(r'C:\Users\misza\OneDrive\Documents\Work\Personal Projects\Gallery Scraper\ML\models\logistic_regression_model.pkl')
    featurizer = UrlFeaturizer("")
    print("Model and featurizer loaded successfully!")
    return model, featurizer


# Example usage
def main():
    # Paths
    csv_path = r'C:\Users\misza\OneDrive\Documents\Work\Personal Projects\Gallery Scraper\ML\training_data\exhibition_href_training.csv'

    train_logistical_regression_model(csv_path)

    model, featurizer = load_model()

    url_to_predict = 'https://www.barbican.org.uk/whats-on/2024/event/this-exhibition'
    print(predict_url(model, featurizer, url_to_predict))

    url_to_predict = 'https://www.barbican.org.uk/whats-on/past/event/this-exhibition'
    print(predict_url(model, featurizer, url_to_predict))

    url_to_predict = 'https://www.barbican.org.uk/about'
    print(predict_url(model, featurizer, url_to_predict))


if __name__ == "__main__":
    main()
