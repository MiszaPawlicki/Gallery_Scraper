import os
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
import joblib
from UrlFeaturizer import UrlFeaturizer


def train_logistic_regression_model(csv_path):
    # Read data from CSV
    df = pd.read_csv(csv_path)

    # Feature extraction
    X = df['href']
    y = df['is_exhibition']

    # Feature extraction and transformation
    vectorizer = CountVectorizer()
    X_transformed = vectorizer.fit_transform(X)

    # Train the logistic regression model
    model = LogisticRegression()
    model.fit(X_transformed, y)

    # Save the model and vectorizer
    model_dir = 'models'
    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir, 'logistic_regression_model.pkl')
    vectorizer_path = os.path.join(model_dir, 'count_vectorizer.pkl')
    joblib.dump(model, model_path)
    joblib.dump(vectorizer, vectorizer_path)
    print("Model and vectorizer saved successfully!")

    return model, vectorizer


def predict_url(model, vectorizer, url):
    # Transform the URL using the same vectorizer used during training
    url_transformed = vectorizer.transform([url])

    # Predict using the trained model
    prediction = model.predict(url_transformed)

    return prediction[0]  # Assuming only one prediction is made


def load_model():
    model = joblib.load(r'C:\Users\misza\OneDrive\Documents\Work\Personal Projects\Gallery Scraper\ML\models\logistic_regression_model.pkl')
    vectorizer = joblib.load(r'C:\Users\misza\OneDrive\Documents\Work\Personal Projects\Gallery Scraper\ML\models\count_vectorizer.pkl')
    print("Model and vectorizer loaded successfully!")
    return model, vectorizer


# Example usage
def main():

    foobar = UrlFeaturizer('https://www.southbankcentre.co.uk/whats-on/art-exhibitions/when-forms-come-alive?eventId=967958')
    print(foobar.run())

    # Paths
    csv_path = r'C:\Users\misza\OneDrive\Documents\Work\Personal Projects\Gallery Scraper\ML\training_data\exhibition_href_training.csv'

    # Train the model and save
    model, vectorizer = train_logistic_regression_model(csv_path)

    # Load the model
    loaded_model, loaded_vectorizer = load_model()

    # URL to predict
    url_to_predict = "https://www.southbankcentre.co.uk/whats-on/art-exhibitions/when-forms-come-alive?eventId=973233"

    # Predict
    prediction = predict_url(loaded_model, loaded_vectorizer, url_to_predict)

    if prediction:
        print("The URL is predicted to be that of an exhibition.")
    else:
        print("The URL is predicted not to be that of an exhibition.")


if __name__ == "__main__":
    main()
