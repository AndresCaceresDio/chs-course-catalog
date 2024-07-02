# Program to conduct basic statistical analysis of the QuizBowl dataset
# Make sure you have a list of x values and y values
# Here, your_y_values is a list of lists of y values, same with your_x_values

means = []
medians = []
modes = []
std_devs = []
correlation_coefficients = []
equations = []
for k in range(len(your_y_values)):
    mean = np.mean(your_y_values[k])
    means.append(mean)

    median = np.median(your_y_values[k])
    medians.append(median)

    mode = your_x_values[k][0] + your_y_values[k].index(max(your_y_values[k]))
    modes.append(mode)

    std_dev = np.std(your_y_values[k], ddof=1)
    std_devs.append(std_dev)

    x_values = your_x_values[k]
    x_mean = np.mean(x_values)
    y_mean = mean
    x_std = np.std(x_values, ddof=1)
    y_std = std_dev
    cov_xy = np.cov(x_values, your_y_values[k])[0][1]
    correlation_coefficients.append(cov_xy / (x_std * y_std))
    slope, intercept = np.polyfit(x_values, your_y_values[k], 1)
    equations.append(slope)

print(means)
print(medians)
print(modes)
print(std_devs)
print(correlation_coefficients)
print(equations)
