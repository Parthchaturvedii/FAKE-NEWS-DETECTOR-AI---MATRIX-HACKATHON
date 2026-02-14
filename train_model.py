import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import PassiveAggressiveClassifier
import joblib

# Sample data - Replace with a real dataset path
data = {'text': ["The moon is cheese", "The sun is hot"], 'label': ['FAKE', 'REAL']}
df = pd.DataFrame(data)

tfidf = TfidfVectorizer(stop_words='english', max_df=0.7)
tfidf_matrix = tfidf.fit_transform(df['text'])

model = PassiveAggressiveClassifier(max_iter=50)
model.fit(tfidf_matrix, df['label'])

# Save artifacts for the API
joblib.dump(model, 'model.joblib')
joblib.dump(tfidf, 'tfidf.joblib')
print("Model artifacts saved.")