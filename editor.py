import ast
import numpy as np

lister = []

# Open the text file containing the dictionaries
with open('editor.txt', 'r') as file:
    for line in file:
        lister.append(ast.literal_eval(line.strip()))

new_list = []
for i in range(len(lister)):
    new_list.append(list(lister[i].values()))

log = []
for i in range(len(lister)):
    log.append(list(lister[i].keys()))

# means = []
# medians = []
# modes = []
# std_devs = []
# rs = []
# equations = []
# for k in range(len(new_list)):
#     mean = np.mean(new_list[k])
#     means.append(mean)

#     median = np.median(new_list[k])
#     medians.append(median)

#     mode = log[k][0] + new_list[k].index(max(new_list[k]))
#     modes.append(mode)

#     std_dev = np.std(new_list[k], ddof=1)
#     std_devs.append(std_dev)

#     x_values = log[k]
#     x_mean = np.mean(x_values)
#     y_mean = mean
#     x_std = np.std(x_values, ddof=1)
#     y_std = std_dev
#     cov_xy = np.cov(x_values, new_list[k])[0][1]
#     rs.append(cov_xy / (x_std * y_std))
#     slope, intercept = np.polyfit(x_values, new_list[k], 1)
#     equations.append(slope)


from scipy.optimize import curve_fit
from scipy.stats import pearsonr

point = []
rsq = []
x_values = np.array(log[1])
y_values = np.array(new_list[1])

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

# with open("new.txt", "w") as file:
#     for i in range(len(rsq)):
#         file.write(str(rsq[i]) + "\n")


# from statsmodels.tsa.arima.model import ARIMA

# d = []
# for k in range(len(new_list)):
#     try:
#         model = ARIMA(new_list[k], order=(1, 1, 1))
#         model_fit = model.fit()
#         forecast = model_fit.forecast(steps=1)
#         d.append(forecast[0])
#     except:
#         d.append("N/A")
