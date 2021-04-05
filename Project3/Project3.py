"""
EE 381 Project 3 part 1
Shawn Joseph 025671644
"""

import random
p = float(input("Enter probability of success"))
T = int(input("How many trials? "))

for i in range(T):
    r = random.uniform(0, 1)
    if r < p:
        print('1', end=' ')
    else:
        print('0', end=' ')
