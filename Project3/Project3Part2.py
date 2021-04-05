"""
EE 381 Project 3 part 2
Shawn Joseph 025671644
"""

import random

RecLoc = []

p_A = float(input("Enter the probability of leaving '0' and going to '1'."))
q_B = float(input("Enter the probability of leaving '1' and going to '0'."))

S = int(input("Enter either a '0' or '1' as a starting state."))
RecLoc.append(S)

for i in range(24):
    r = random.uniform(0, 1)
    if S == 0 and r < p_A:
        S = 1
    elif S == 1 and r < q_B:
        S = 0
    RecLoc.append(S)

for i in RecLoc:
    print(i, end=' ')
