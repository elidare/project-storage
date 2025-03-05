from sklearn.decomposition import TruncatedSVD
from sklearn.model_selection import train_test_split
from sklearn.metrics import root_mean_squared_error, precision_score, recall_score, f1_score
import pandas as pd
import numpy as np


ratings = pd.read_csv('ratings.csv')


def random_split(data):
    train_data, test_data = train_test_split(data, train_size=0.8, random_state=42)
    return train_data, test_data


def temporal_split(data):
    # Convert timestamp to datetime format
    data['timestamp'] = pd.to_datetime(data['timestamp'], unit='s')  # Assuming Unix timestamp
    # Sort data by timestamp
    data = data.sort_values(by='timestamp')
    # Temporal split: 80% training, 20% testing
    split_point = int(len(data) * 0.8)
    train_data = data.iloc[:split_point]  # First 80%
    test_data = data.iloc[split_point:]  # Last 20%
    return train_data, test_data


def apply_SVD(ratings_matrix_filled):
    # Use 10 components for simplicity
    svd = TruncatedSVD(n_components=10)
    np.seterr(divide='ignore', invalid='ignore')
    U = svd.fit_transform(ratings_matrix_filled.values)
    Sigma = svd.singular_values_
    VT = svd.components_
    np.seterr(divide='warn', invalid='warn')

    # Reconstruct the matrix
    reconstructed_matrix = np.dot(np.dot(U, np.diag(Sigma)), VT)
    # Normalize Predicted Ratings:
    min_rating = ratings['rating'].min()  # Should be 0.5 or 1.0
    max_rating = ratings['rating'].max()  # Should be 5.0

    reconstructed_matrix = ((reconstructed_matrix - reconstructed_matrix.min()) / (
            reconstructed_matrix.max() - reconstructed_matrix.min())
                            * (max_rating - min_rating) + min_rating)

    return reconstructed_matrix


def do_training(data, temporal=False):
    train_data, test_data = temporal_split(data) if temporal else random_split(data)

    ratings_matrix = train_data.pivot_table(index='userId', columns='movieId', values='rating')
    ratings_matrix_filled = ratings_matrix.fillna(ratings_matrix.mean())  # Replace nulls with user or movie mean

    # Extract actual ratings from test set
    test_actual = test_data.pivot_table(index='userId', columns='movieId', values='rating')

    reconstructed_matrix = apply_SVD(ratings_matrix_filled)

    predicted_ratings_df = pd.DataFrame(reconstructed_matrix, index=ratings_matrix.index,
                                        columns=ratings_matrix.columns)

    # Get predicted data only if the same rating was in test_data to test
    comparison_df = test_actual.stack().reset_index(name="actual_rating")
    predicted_ratings_df = predicted_ratings_df.stack().reset_index(name="predicted_rating")
    comparison_df = comparison_df.merge(predicted_ratings_df, on=["userId", "movieId"], how="inner")

    y_true_ratings = comparison_df["actual_rating"].values
    y_pred_ratings = comparison_df["predicted_rating"].values

    print('Root mean Square Error:')
    print(root_mean_squared_error(y_true_ratings, y_pred_ratings))

    threshold = 3.5  # Define the relevance threshold

    # Convert actual and predicted ratings into binary values
    y_true = [int(i >= threshold) for i in y_true_ratings]
    y_pred = [int(i >= threshold) for i in y_pred_ratings]

    # Compute Precision, Recall, and F1-Score
    precision = precision_score(y_true, y_pred, zero_division=0)
    recall = recall_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)

    print(f"Precision: {precision}, Recall: {recall}, F1-Score: {f1}")


do_training(ratings)
do_training(ratings, temporal=True)
