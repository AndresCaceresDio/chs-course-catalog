# Program to forecast the next value using the Auto-Integrated Moving Average
# Can only forecast one future vaue, make sure you have a list of y-values
# All three parameters are set to 1, but you can change that for more accurate results

from statsmodels.tsa.arima.model import ARIMA

forecasts = []
for k in range(len(your_y_values)):
  try:
    model = ARIMA(your_y_values[k], order=(1, 1, 1))
    model_fit = model.fit()
    forecast = model_fit.forecast(steps=1)
    forecasts.append(forecast[0])
  except:
    forecasts.append("N/A")

print(forecasts)
