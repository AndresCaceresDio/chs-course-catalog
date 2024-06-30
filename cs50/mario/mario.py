# Project description can be found at: https://cs50.harvard.edu/x/2023/psets/6/mario/less/

from cs50 import get_int

height = 0
while int(height) > 8 or int(height) < 1:
    height = get_int("Height: ")
x = height - 1
y = 1
for i in range(height):
    for i in range(x):
        print(" ", end="")
    for i in range(y):
        print("#", end="")
    x -= 1
    y += 1
    print("")
