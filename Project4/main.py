import math
import random
import matplotlib.pyplot as plt

n = 100
x = []
y = {}
lmd = 1

for i in range(n):
    r = random.uniform(0, 1)
    x.append(r)
    t = -(1 / lmd) * math.log(1 - r, math.e)
    y.append(t)

b = max(x)
a = min(x)
R = b - a
intervals = int(math.ceil(math.sqrt(n)))
width = R / intervals

plt.subplot(2, 1, 1)
plt.hist(x, intervals, normed=width)
plt.subplot(2, 1, 1)
plt.hist(y, intervals, normed=width)
