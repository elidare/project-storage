import pandas as pd
import numpy as np
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, classification_report
from sklearn.feature_extraction.text import TfidfVectorizer

train_data = pd.read_csv('.\kagglehub\datasets\columbine\imdb-dataset-sentiment-analysis-in-csv-format\\versions\\1\Train.csv')
valid_data = pd.read_csv('.\kagglehub\datasets\columbine\imdb-dataset-sentiment-analysis-in-csv-format\\versions\\1\Valid.csv')
test_data = pd.read_csv('.\kagglehub\datasets\columbine\imdb-dataset-sentiment-analysis-in-csv-format\\versions\\1\Test.csv')

# Choosing Naive Bayes as a classification
nb = GaussianNB()

# Vectorizing
vectorizer = TfidfVectorizer()

# Fit and transform the whole document set
X_train = vectorizer.fit_transform(train_data['text'])
y_train = train_data['label']
X_valid = vectorizer.transform(valid_data['text'])
y_valid = valid_data['label']
X_test = vectorizer.transform(test_data['text'])
y_test = test_data['label']

start = 0
chunk_size = 5000

while start < len(train_data):
    print('Start ', start, len(train_data))
    X_chunk = X_train[start:start + chunk_size]
    y_chunk = y_train[start:start + chunk_size]
    nb.partial_fit(X_chunk.toarray(), y_chunk, classes=np.unique(y_train))
    print('Chunk ', start, ' ready out of', len(train_data))
    start += chunk_size

# Predict and Evaluate on validation set
preds_valid = nb.predict(X_valid.toarray())
print("Validation Accuracy:", accuracy_score(y_valid, preds_valid))
print(classification_report(y_valid, preds_valid))

# Predict and Evaluate on test set
preds_test = nb.predict(X_test.toarray())
print("Test Accuracy:", accuracy_score(y_test, preds_test))
print(classification_report(y_test, preds_test))
