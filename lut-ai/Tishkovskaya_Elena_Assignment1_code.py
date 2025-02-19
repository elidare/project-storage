from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report
import pandas as pd
import numpy as np
import fasttext
import time


start_time = time.time()  # Measuring time resources

train_data = pd.read_csv('.\kagglehub\datasets\columbine\imdb-dataset-sentiment-analysis-in-csv-format\\versions\\1\Train.csv')
valid_data = pd.read_csv('.\kagglehub\datasets\columbine\imdb-dataset-sentiment-analysis-in-csv-format\\versions\\1\Valid.csv')
test_data = pd.read_csv('.\kagglehub\datasets\columbine\imdb-dataset-sentiment-analysis-in-csv-format\\versions\\1\Test.csv')

# Choose Naive Bayes as a classification
nb = MultinomialNB()


def train(X_train, y_train):
    start = 0
    chunk_size = 5000

    # nb.fit() was causing ArrayMemoryError
    while start < len(train_data):
        print('Start ', start, len(train_data))
        x_chunk = X_train[start:start + chunk_size]
        y_chunk = y_train[start:start + chunk_size]
        nb.partial_fit(x_chunk.toarray(), y_chunk, classes=np.unique(y_train))
        print('Chunk ', start, ' ready out of', len(train_data))
        start += chunk_size

    print('Time spent:', time.strftime('%H:%M:%S', time.gmtime(time.time() - start_time)))


def validate(X_valid, y_valid):
    # Predict and Evaluate on validation set
    preds_valid = nb.predict(X_valid.toarray())
    print('Validation Accuracy:', accuracy_score(y_valid, preds_valid))
    print(classification_report(y_valid, preds_valid))
    print('Time spent:', time.strftime('%H:%M:%S', time.gmtime(time.time() - start_time)))


def test(X_test, y_test):
    # Predict and Evaluate on test set
    preds_test = nb.predict(X_test.toarray())
    print('Test Accuracy:', accuracy_score(y_test, preds_test))
    print(classification_report(y_test, preds_test))
    print('Time spent:', time.strftime('%H:%M:%S', time.gmtime(time.time() - start_time)))


def get_results(filter=False):
    # Vectorize
    vectorizer = TfidfVectorizer(stop_words="english") if filter else TfidfVectorizer()

    # Fit and transform the whole document set
    X_train = vectorizer.fit_transform(train_data['text'])
    y_train = train_data['label']
    X_valid = vectorizer.transform(valid_data['text'])
    y_valid = valid_data['label']
    X_test = vectorizer.transform(test_data['text'])
    y_test = test_data['label']
    # Train, validate, and test
    train(X_train, y_train)
    validate(X_valid, y_valid)
    test(X_test, y_test)


def get_results_fasttext():
    # Function to predict sentiment for a DataFrame column
    def predict_sentiment(text):
        label, _ = model.predict(text)  # FastText returns a tuple (label, confidence)
        return int(label[0].replace('__label__', ''))  # Extract and clean the label

    y_valid = valid_data['label']
    y_test = test_data['label']

    # Convert labels to FastText format
    train_data['label'] = train_data['label'].apply(lambda x: "__label__" + str(x))
    valid_data['label'] = valid_data['label'].apply(lambda x: "__label__" + str(x))
    test_data['label'] = test_data['label'].apply(lambda x: '__label__' + str(x))

    # Save in FastText format
    train_data[['label', 'text']].to_csv('fasttext_data/train_data.txt', sep=' ', index=False, header=False)
    valid_data[['label', 'text']].to_csv('fasttext_data/valid_data.txt', sep=' ', index=False, header=False)
    test_data[['label', 'text']].to_csv('fasttext_data/test_data.txt', sep=' ', index=False, header=False)

    # Train model with hyperparameters
    print('Start training')
    model = fasttext.train_supervised(input='fasttext_data/train_data.txt', epoch=25, wordNgrams=2)

    # Evaluate on validation data
    valid_data['predicted_label'] = valid_data['text'].apply(predict_sentiment)
    print('Test Accuracy:', accuracy_score(y_valid, valid_data['predicted_label']))
    print(classification_report(y_valid, valid_data['predicted_label']))
    print('Time spent:', time.strftime('%H:%M:%S', time.gmtime(time.time() - start_time)))

    # Evaluate on test data
    test_data['predicted_label'] = test_data['text'].apply(predict_sentiment)
    print('Test Accuracy:', accuracy_score(y_test, test_data['predicted_label']))
    print(classification_report(y_test, test_data['predicted_label']))
    print('Time spent:', time.strftime('%H:%M:%S', time.gmtime(time.time() - start_time)))


# get_results()
# get_results(filter=True)
get_results_fasttext()
