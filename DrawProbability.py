# code: UTF-8
import math
import re
import string
import numpy as np
import datetime
import time
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(8, 6), dpi=84, facecolor="white")
x1 = np.arange(0.0, 2, 0.0001)
y1 = np.sqrt(x1)


ax = plt.gca()
ax.set_xticks(np.linspace(x1[0], x1[-1], 5))
#ax.set_xticklabels( (Time[0][0:8], Time[interval][0:8], Time[2*interval][0:8], Time[3*interval][0:8], Time[-1][0:8]))
ax.set_yticks(np.linspace(y1[0], y1[-1], 5))

l = [x1[0], 2 * x1[-1], min(y1), 2 * max(y1)]
plt.axis(l)
ax.plot(x1, y1, color='black')

ax.set_xticks(np.linspace(x1[-1], 2 * x1[-1], 5))
ax.set_yticks(np.linspace(y1[-1], 2 * y1[-1], 5))

x2 = np.arange(2, 4, 0.0001)
y2 = y1[-1] + np.sqrt(x2 - x1[-1])
y3 = y1[-1] - np.sqrt(x2 - x1[-1])
y4 = y1[-1] + 0.2 * np.sqrt(x2 - x1[-1])
y5 = y1[-1] - 0.2 * np.sqrt(x2 - x1[-1])
ax.plot(x2, y2, x2, y3, color='black')

plt.axis(l)
# ax.fill_betweenx(y2, y3, 4, where=x2 >= x1[-1],  facecolor="orange", color="white")
# ax.fill_between(x2, y1, y2, where=y2 <= y1, facecolor='red', interpolate=True)
ax.fill_between(x2, y2, y3, facecolor="orange", color="white" )
ax.fill_between(x2, y4, y5, facecolor="red", color="white" )
ax.set_title('fill between where')

plt.show()