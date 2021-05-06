# Poisson
import matplotlib.pyplot as plt
import math


L = float(input("Enter the value of the Poisson parameter."))
N = 25

P = math.exp(-L)
X = [0]
Y = [P]

for i in range(N):
    if i > 0:
        P = P * (L / i)
        X.append(i)
        Y.append(P)
    print(i, P)


plt.plot(X, Y, 'r+')
plt.show()
