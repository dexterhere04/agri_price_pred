# -*- coding: utf-8 -*-
"""PREDICTIONRGK.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/13oSysqKhoJ-crSHo_hv5y0G2oIZDtEdh
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, KFold
from sklearn.metrics import mean_squared_error, r2_score, f1_score
import matplotlib.pyplot as plt
import os
from django.conf import settings
# Load the data
pickle_file_path=os.path.join(settings.BASE_DIR,'home','trained_model','retailavg.csv')
df = pd.read_csv(pickle_file_path)
# Convert 'Date' column to datetime format and extract features
df['Date'] = pd.to_datetime(df['Date'], format="%d/%m/%Y")
df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.month
df['Day'] = df['Date'].dt.day
df.drop('Date', axis=1, inplace=True)

# Define features (X) and target (y)
X = df[['Year', 'Month', 'Day']].values
y = df[['Rice', 'Wheat', 'Atta (Wheat)', 'Gram Dal', 'Tur/Arhar Dal',
         'Urad Dal', 'Moong Dal', 'Masoor Dal', 'Sugar', 'Milk @',
         'Groundnut Oil (Packed)', 'Mustard Oil (Packed)', 'Vanaspati (Packed)',
         'Soya Oil (Packed)', 'Sunflower Oil (Packed)', 'Palm Oil (Packed)',
         'Gur', 'Tea Loose', 'Salt Pack (Iodised)', 'Potato', 'Onion', 'Tomato']].values

# Scale features
scaler = StandardScaler()
X = scaler.fit_transform(X)

# Scale target variables
y_scaler = StandardScaler()
y = y_scaler.fit_transform(y)

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define the ELM model
class ELM:
    def __init__(self, input_dim, hidden_dim, regularization=0.0):
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.regularization = regularization
        self.W = None
        self.b = None
        self.beta = None

    def fit(self, X, y):
        self.W = np.random.randn(self.hidden_dim, self.input_dim)
        self.b = np.random.randn(self.hidden_dim, 1)

        H = self._hidden_layer_output(X)
        I = np.eye(H.shape[1])
        self.beta = np.linalg.pinv(H.T @ H + self.regularization * I) @ H.T @ y

    def _hidden_layer_output(self, X):
        return 1 / (1 + np.exp(- (X @ self.W.T + self.b.T)))

    def predict(self, X):
        H = self._hidden_layer_output(X)
        return H @ self.beta
    def _getstate_(self):
        """This is called when pickling the object."""
        state = self._dict_.copy()
        # Return only the state that can be pickled
        return state

    def _setstate_(self, state):
        """This is called when unpickling the object."""
        self._dict_.update(state)
# Define the Firefly Algorithm for optimization
class FireflyAlgorithm:
    def __init__(self, n_fireflies, n_iterations, input_dim, hidden_dim, X, y, reg_param=0.01):
        self.n_fireflies = n_fireflies
        self.n_iterations = n_iterations
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.X = X
        self.y = y
        self.reg_param = reg_param
        self.best_firefly = None
        self.best_score = float('inf')
        self.best_model = None

    def optimize(self):
        fireflies = np.random.uniform(-1, 1, (self.n_fireflies, self.input_dim * self.hidden_dim + self.hidden_dim))
        scores = np.zeros(self.n_fireflies)

        for iteration in range(self.n_iterations):
            for i in range(self.n_fireflies):
                W, b = self.decode_firefly(fireflies[i])
                elm = ELM(self.input_dim, self.hidden_dim, self.reg_param)
                elm.W = W
                elm.b = b
                elm.fit(self.X, self.y)
                predictions = elm.predict(self.X)

                score = np.mean((predictions - self.y) ** 2)
                scores[i] = score

                if score < self.best_score:
                    self.best_score = score
                    self.best_firefly = fireflies[i]
                    self.best_model = elm

            fireflies = self.move_fireflies(fireflies, scores)

        return self.best_model

    def decode_firefly(self, firefly):
        W = firefly[:self.hidden_dim * self.input_dim].reshape((self.hidden_dim, self.input_dim))
        b = firefly[self.hidden_dim * self.input_dim:].reshape((self.hidden_dim, 1))
        return W, b

    def move_fireflies(self, fireflies, scores):
        attractiveness = np.exp(-np.array(scores))
        for i in range(self.n_fireflies):
            for j in range(self.n_fireflies):
                if scores[i] < scores[j]:
                    distance = np.linalg.norm(fireflies[i] - fireflies[j])
                    attractiveness_i = attractiveness[j] / (1 + distance)
                    fireflies[i] += attractiveness_i * np.random.rand() * (fireflies[j] - fireflies[i])
        return fireflies

# Train the model using the Firefly Algorithm
input_dim = X_train.shape[1]
hidden_dim = 70
n_fireflies = 40
n_iterations = 200

fa = FireflyAlgorithm(n_fireflies, n_iterations, input_dim, hidden_dim, X_train, y_train)
best_model = fa.optimize()

# Make predictions on the test set
predictions = best_model.predict(X_test)

# Function to predict prices based on user input date range
def predict_prices(start_date, end_date):
    # Convert input dates to datetime
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    # Create a date range
    date_range = pd.date_range(start=start_date, end=end_date)

    # Prepare features for prediction
    features = np.array([[date.year, date.month, date.day] for date in date_range])
    features_scaled = scaler.transform(features)

    # Make predictions using the trained model
    predicted_prices_scaled = best_model.predict(features_scaled)

    # Inverse transform the predictions to get original scale
    predicted_prices = y_scaler.inverse_transform(predicted_prices_scaled)

    # Create a DataFrame for the results
    results_df = pd.DataFrame(predicted_prices, columns=['Rice', 'Wheat', 'Atta (Wheat)', 'Gram Dal',
                                                          'Tur/Arhar Dal', 'Urad Dal', 'Moong Dal',
                                                          'Masoor Dal', 'Sugar', 'Milk @',
                                                          'Groundnut Oil (Packed)', 'Mustard Oil (Packed)',
                                                          'Vanaspati (Packed)', 'Soya Oil (Packed)',
                                                          'Sunflower Oil (Packed)', 'Palm Oil (Packed)',
                                                          'Gur', 'Tea Loose', 'Salt Pack (Iodised)',
                                                          'Potato', 'Onion', 'Tomato'])
    results_df['Date'] = date_range

    return results_df[['Date'] + list(results_df.columns[:-1])]

# # Example usage: Get user input for date range
# start_date = input("Enter the start date (DD/MM/YYYY): ")
# end_date = input("Enter the end date (DD/MM/YYYY): ")

# predicted_prices_df = predict_prices("12/12/2012","12/1/2013")
# print("\nPredicted prices from","to")
# print(predicted_prices_df)