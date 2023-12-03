import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn import metrics
import joblib  # Corrected import statement

# Load the data from the Excel file
df = pd.read_excel('training_dat.xlsx')

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(df['Title'], df['Rating'], test_size=0.2, random_state=42)

# Build a classifier using a simple pipeline (you can use other classifiers as well)
model = make_pipeline(CountVectorizer(), MultinomialNB())

# Train the model
model.fit(X_train, y_train)

# Make predictions on the test set
predictions = model.predict(X_test)

# Print classification report and accuracy
print(metrics.classification_report(y_test, predictions))
print(f'Accuracy: {metrics.accuracy_score(y_test, predictions)}')

# Save the model for future use
joblib.dump(model, 'weather_classifier_model.joblib')
