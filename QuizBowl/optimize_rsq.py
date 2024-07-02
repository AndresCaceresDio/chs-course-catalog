# Program that finds the function that yields the largest R-Squared value
# It fits linear, exponential, logarithmic, and sine models
# Data includes a NumPy array of x-values and a NumPy array of y-values

from scipy.optimize import curve_fit
from scipy.stats import pearsonr
import ast
import numpy as np

point = []
rsq = []
x_values = np.array(your_x_values)
y_values = np.array(your_y_values)

# Define different types of functions to fit to the data
def linear_func(x, a, b):
    return a * x + b

def exponential_func(x, a, b, c, d):
    return a + b*np.exp(c*x) + d

def logarithmic_func(x, a, b, c):
    return a * np.log(x) + b * x + c

def sine_func(x, A, B, C, D):
    return A * np.sin(B * x + C) + D

# List of models to try with initial guesses and model names
models = [
    (linear_func, "Linear", [0, 1]),
    (exponential_func, "Exponential", [1, 0.1, 1]),
    (logarithmic_func, "Logarithmic", [1, 1, 1]),
    (sine_func, "Sine", [1, 2 * np.pi / max(x_values), 0, np.mean(y_values)])
]

# Dictionary to hold R-squared values
r_squared_values = {}

# Fit each model to the data and calculate R-squared
for model, name, initial_guess in models:
    try:
        # Increase maxfev to give the algorithm more iterations to converge
        params, _ = curve_fit(model, x_values, y_values, p0=initial_guess, maxfev=5000)
        fitted_values = model(x_values, *params)
        # Compute correlation coefficient and square it to get R-squared
        r_squared = pearsonr(y_values, fitted_values)[0] ** 2
        r_squared_values[name] = r_squared
    except Exception as e:
        print(f"Could not fit {name} model: {e}")
        r_squared_values[name] = None  # Use None to indicate failure to fit

# Identify the best model (ignoring None values)
best_model_name = max((model for model in r_squared_values if r_squared_values[model] is not None),
                    key=lambda model: r_squared_values[model], default=None)
best_r_squared = r_squared_values["Exponential"] if best_model_name else None
print(best_r_squared)
