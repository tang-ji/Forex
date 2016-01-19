__author__ = 'Jojo'
import numpy as np

from Hurst import *
a = [1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2]
a = np.tile(a, 10)
print Hurst(a)