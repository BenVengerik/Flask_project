import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

resistance_values = np.array([332776, 96481, 32566, 12486, 10000, 5331, 2490, 1071, 678.1, 387.3])  
temperature_values = np.array([-40, -20, 0, 20, 25, 40, 60, 85, 100, 120])  


def log_fit(R, A, B):
    return A + B * np.log(R)

params, _ = curve_fit(log_fit, resistance_values, temperature_values)
A_fit, B_fit = params

resistance_range = np.linspace(min(resistance_values), max(resistance_values), 100)
fitted_temperatures = log_fit(resistance_range, A_fit, B_fit)

plt.figure(figsize=(8, 5))
plt.scatter(resistance_values, temperature_values, color='red', label="Given Data", zorder=2)
plt.plot(resistance_range, fitted_temperatures, label="Log Fit: T = {:.2f} + {:.2f} ln(R)".format(A_fit, B_fit), color='blue', zorder=1)
plt.xscale("log")
plt.xlabel("Resistance (Ohms, Log Scale)")
plt.ylabel("Temperature (°C)")
plt.legend()
plt.title("Linear Interpolation Log Fit")

# Show plot
plt.show()

# Return fitted parameters for reference
A_fit, B_fit

# Not a bad fit, but a nonlinear model might be more appropriate for this data. It's fine for now. 