import numpy as np
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(8, 6), dpi=84, facecolor="white")
n = 3
X = np.linspace(0.0, 1, n)
Y = np.random.normal(0, 0.3, n)
X1 = np.random.rand(0, 1, n)
Z = np.sin(30*X)
Y1 = np.linspace(0, 1, n)
T = 1 - abs(np.arctan2(Y, X))**5

plt.axes([0.025, 0.025, 0.95, 0.95])
plt.scatter(X, Y1, s=100, c=[2,1,3], alpha=.5)

plt.xlim(-1.5, 1.5), plt.xticks([])
plt.ylim(-1.5, 1.5), plt.yticks([])
# savefig('../figures/scatter_ex.png',dpi=48)
plt.show()