#Shawn Joseph E E 381 Project 2 Part 3
import random

false = False
true = True

random.seed(a=None, version=2)
outcomes = []
trial_num = 10000000
for i in range(trial_num):
    heads = false
    j = 0
    while heads == false:
        j += 1
        print("Coin flipped " + str(j) + " times")
        heads = random.uniform(0, 1) > 0.5
    outcomes.append(j % 2)
    print("Trial " + str(i) + " was " + str(j % 2 == 0))
print(sum(outcomes) / len(outcomes))
