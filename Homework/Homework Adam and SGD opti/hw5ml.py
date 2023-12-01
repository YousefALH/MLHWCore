# -*- coding: utf-8 -*-
"""HW5ML.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1VqnxeQnqjsGyRInRlBm1Do4fvUlpgjGA
"""

import torch
import matplotlib.pyplot as plt

"""#Prob 1"""

# Given data
t_u = torch.tensor([35.7, 55.9, 58.2, 81.9, 56.3, 48.9, 33.9, 21.8, 48.4, 60.4, 68.4], dtype=torch.float32)
t_c = torch.tensor([0.5, 14.0, 15.0, 28.0, 11.0, 8.0, 3.0, -4.0, 6.0, 13.0, 21.0], dtype=torch.float32)
t_un = 0.1 * t_u  # Normalize the input data

def model(t_u, params):
    w2, w1, b = params
    return w2 * t_u**2 + w1 * t_u + b

def linear_model(t_u, params):
    w, b = params
    return w * t_u + b

def loss_fn(t_p, t_c):
    """Mean squared error loss function."""
    squared_diffs = (t_p - t_c)**2
    return squared_diffs.mean()

def training_loop(n_epochs, learning_rate, params, t_u, t_c, optimizer, model_fn):
    for epoch in range(1, n_epochs + 1):
        t_p = model_fn(t_u, params)  # Adjusted to pass params as a single argument
        loss = loss_fn(t_p, t_c)

        optimizer.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_value_(params, clip_value=1.0)
        optimizer.step()

        if epoch % 500 == 0 or epoch == 1:
            print(f"Epoch {epoch}, Loss {loss.item()}")

    return params

def initialize_params(model_type='non-linear'):
    """Initializes parameters with default values."""
    if model_type == 'non-linear':
        return (torch.ones((), requires_grad=True),
                torch.ones((), requires_grad=True),
                torch.zeros((), requires_grad=True))
    elif model_type == 'linear':
        return (torch.ones((), requires_grad=True),
                torch.zeros((), requires_grad=True))

# Train non-linear and linear models
learning_rates = [0.1, 0.01, 0.001, 0.0001]
best_loss = float('inf')
best_params, best_lr, best_optimizer = None, None, None

for lr in learning_rates:
    for optimizer_class, model_fn in [(torch.optim.SGD, model), (torch.optim.Adam, model)]:
        optimizer_name = optimizer_class.__name__
        params = initialize_params('non-linear')
        optimizer = optimizer_class(params, lr=lr)
        trained_params = training_loop(5000, lr, params, t_un, t_c, optimizer, model_fn)
        final_loss = loss_fn(model_fn(t_un, trained_params), t_c).item()

        if final_loss < best_loss:
            best_loss, best_params, best_lr, best_optimizer = final_loss, trained_params, lr, optimizer_name

        print(f"Finished training with {optimizer_name} and learning rate {lr}: Final Loss {final_loss}")

# Train linear model with best found learning rate
params_linear = initialize_params('linear')
optimizer_linear = torch.optim.SGD(params_linear, lr=best_lr)
trained_params_linear = training_loop(5000, best_lr, params_linear, t_un, t_c, optimizer_linear, linear_model)
w_linear_value, b_linear_value = trained_params_linear
print(f'Trained linear model parameters: w = {w_linear_value.item()}, b = {b_linear_value.item()}')

# Function to generate predictions using the non-linear model
def non_linear_model_predictions(t_u, params):
    w2, w1, b = params
    return w2 * t_u**2 + w1 * t_u + b

# Function to generate predictions using the linear model
def linear_model_predictions(t_u, params):
    w, b = params
    return w * t_u + b

# Generate predictions
t_un_grid = torch.linspace(min(t_un), max(t_un), 1000)  # A grid of normalized temperature values
non_linear_preds = non_linear_model_predictions(t_un_grid, best_params)
linear_preds = linear_model_predictions(t_un_grid, (w_linear_value, b_linear_value))

# Plotting
plt.figure(figsize=(12, 6))

# Plot for the non-linear model
plt.subplot(1, 2, 1)
plt.title('Non-linear Model')
plt.plot(t_un.numpy(), t_c.numpy(), 'o', label='Actual Data')
plt.plot(t_un_grid.numpy(), non_linear_preds.detach().numpy(), label='Model Prediction')
plt.xlabel('Normalized Temperature (t_un)')
plt.ylabel('Celsius (t_c)')
plt.legend()

# Plot for the linear model
plt.subplot(1, 2, 2)
plt.title('Linear Model')
plt.plot(t_un.numpy(), t_c.numpy(), 'o', label='Actual Data')
plt.plot(t_un_grid.numpy(), linear_preds.detach().numpy(), label='Model Prediction')
plt.xlabel('Normalized Temperature (t_un)')
plt.ylabel('Celsius (t_c)')
plt.legend()

plt.show()

"""# Prob 2

get data
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import SGDRegressor, LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt



#mounting google drive
from google.colab import drive
drive.mount('/content/drive')

file_path = '/content/drive/My Drive/IntroML/content/Housing.csv'
housing_data = pd.read_csv(file_path)
display(housing_data)

# Selecting relevant features and target variable
features = ['area', 'bedrooms', 'bathrooms', 'stories', 'parking']
X = housing_data[features]
y = housing_data['price']

# Splitting the data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=0)

# Training the model using SGD
sgd_regressor = SGDRegressor(max_iter=1000, tol=1e-3, random_state=0)
sgd_regressor.fit(X_train, y_train)

# Predicting and evaluating with SGD
y_pred_sgd = sgd_regressor.predict(X_val)
mse_sgd = mean_squared_error(y_val, y_pred_sgd)

# Training the model using ADAM
adam_regressor = MLPRegressor(solver='adam', max_iter=10000, random_state=0)
adam_regressor.fit(X_train, y_train)

# Predicting and evaluating with ADAM
y_pred_adam = adam_regressor.predict(X_val)
mse_adam = mean_squared_error(y_val, y_pred_adam)

# Output the MSE for both models
print("MSE with SGD:", mse_sgd)
print("MSE with ADAM:", mse_adam)

"""part 2.b"""

# Standardizing the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_val_scaled = scaler.transform(X_val)

# SGD Regressor Training
learning_rates = [0.1, 0.01, 0.001, 0.0001, 0.00001]
sgd_results = {lr: {'training_loss': [], 'validation_loss': []} for lr in learning_rates}

for lr in learning_rates:
    sgd_regressor = SGDRegressor(learning_rate='constant', eta0=lr, max_iter=1, tol=None, random_state=0)
    for epoch in range(5000):
        sgd_regressor.partial_fit(X_train_scaled, y_train)
        if (epoch + 1) % 500 == 0:
            train_loss = mean_squared_error(y_train, sgd_regressor.predict(X_train_scaled))
            val_loss = mean_squared_error(y_val, sgd_regressor.predict(X_val_scaled))
            sgd_results[lr]['training_loss'].append(train_loss)
            sgd_results[lr]['validation_loss'].append(val_loss)

# ADAM Regressor Training (Using MLPRegressor as an approximation)
adam_results = {lr: {'training_loss': [], 'validation_loss': []} for lr in learning_rates}

for lr in learning_rates:
    adam_regressor = MLPRegressor(hidden_layer_sizes=(), solver='adam', learning_rate_init=lr, max_iter=1, random_state=0)
    for epoch in range(5000):
        adam_regressor.partial_fit(X_train_scaled, y_train)
        if (epoch + 1) % 500 == 0:
            train_loss = mean_squared_error(y_train, adam_regressor.predict(X_train_scaled))
            val_loss = mean_squared_error(y_val, adam_regressor.predict(X_val_scaled))
            adam_results[lr]['training_loss'].append(train_loss)
            adam_results[lr]['validation_loss'].append(val_loss)

# Output results
print("SGD Results:", sgd_results)
print("ADAM Results:", adam_results)

# Function to print results vertically
def print_results(title, results):
    print(title)
    for lr, metrics in results.items():
        print(f"\nLearning Rate: {lr}")
        for epoch in range(len(metrics['training_loss'])):
            print(f"Epoch {500 * (epoch + 1)}: "
                  f"Training Loss = {metrics['training_loss'][epoch]}, "
                  f"Validation Loss = {metrics['validation_loss'][epoch]}")

# Output SGD and ADAM results
print_results("SGD Results", sgd_results)
print("\n--------------------------------------\n")
print_results("ADAM Results", adam_results)

# Function to plot the results
def plot_results(title, results):
    plt.figure(figsize=(12, 8))
    for lr, metrics in results.items():
        epochs = range(500, 5001, 500)
        plt.plot(epochs, metrics['training_loss'], marker='o', label=f'Training Loss (LR: {lr})')
        plt.plot(epochs, metrics['validation_loss'], marker='s', label=f'Validation Loss (LR: {lr})')

    plt.title(title)
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()
    plt.grid(True)
    plt.show()

# Plot SGD and ADAM results
plot_results("SGD Results", sgd_results)
plot_results("ADAM Results", adam_results)

"""#prob 3"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import SGDRegressor
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer

from google.colab import drive
drive.mount('/content/drive')

file_path = '/content/drive/My Drive/IntroML/content/Housing.csv'
housing_data = pd.read_csv(file_path)
display(housing_data)

# Selecting target variable
y = housing_data['price'].values

# Preprocessing non-numeric features using OneHotEncoder
numeric_features = housing_data.select_dtypes(include=['int64', 'float64']).columns
categorical_features = housing_data.select_dtypes(include=['object']).columns

# If 'price' is a categorical feature, remove it from the list
if 'price' in categorical_features:
    categorical_features = categorical_features.drop('price')

preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numeric_features),
        ('cat', OneHotEncoder(), categorical_features)
    ])
# Transforming the data
X = preprocessor.fit_transform(housing_data)

# Splitting the data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=0)

# Different learning rates to explore
learning_rates = [0.1, 0.01, 0.001, 0.0001]

# Dictionary to store results
results = {lr: {'training_loss': [], 'validation_accuracy': []} for lr in learning_rates}

# Training models with different learning rates
for lr in learning_rates:
    sgd = SGDRegressor(learning_rate='constant', eta0=lr, max_iter=1, tol=None, random_state=0)
    for epoch in range(1, 5001):
        sgd.partial_fit(X_train, y_train)  # One epoch of training
        if epoch % 500 == 0:
            train_loss = mean_squared_error(y_train, sgd.predict(X_train))
            val_accuracy = mean_squared_error(y_val, sgd.predict(X_val))
            results[lr]['training_loss'].append(train_loss)
            results[lr]['validation_accuracy'].append(val_accuracy)

# Identifying the best learning rate based on validation accuracy
best_lr = min(results, key=lambda lr: min(results[lr]['validation_accuracy']))
best_performance = results[best_lr]

print("Best Learning Rate:", best_lr)
print("Training Loss at every 500 epochs:", best_performance['training_loss'])
print("Validation Accuracy at every 500 epochs:", best_performance['validation_accuracy'])