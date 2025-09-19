import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import simpson
from numpy import trapezoid
x = np.arange(0.0, 10, 0.1)
y = np.abs(np.sin(x*np.exp(np.cos(x))))
plt.grid()
plt.plot(x, y, c = "r")
plt.fill_between(x, y)

area = trapezoid(y)
print(area)