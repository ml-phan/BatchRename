import math

import numpy as np
import time


a = np.random.rand(1000000)
b = np.random.rand(1000000)

# start = time.perf_counter()
start = time.time()
c = np.dot(a, b)
finish = time.time()
# finish = time.perf_counter()
print(c)
print("Vectorized", 1000*(finish - start),  "ms")

start = time.time()
d = 0
for i in range(1000000):
     d += a[i]*b[i]
finish = time.time()
print(d)
print("For Loop", 1000*(finish - start),  "ms")

