# Project description can be found at: https://cs50.harvard.edu/x/2023/psets/6/cash/

from cs50 import get_float

change_owed = -1
while change_owed < 0:
    change_owed = get_float("Change owed: ")
change_owed *= 100
def quarters(n):
    a = 0
    for i in range(int(n)):
        a += 1
        n -= 25
        if n < 0:
            a -= 1
            break
    return a

def dimes(n):
    b = 0
    for i in range(int(n)):
        b += 1
        n -= 10
        if n < 0:
            b -= 1
            break
    return b

def nickels(n):
    c = 0
    for i in range(int(n)):
        c += 1
        n -= 5
        if n < 0:
            c -= 1
            break
    return c

def pennies(n):
    d = 0
    for i in range(int(n)):
        d += 1
        n -= 1
        if n < 0:
            d -= 1
            break
    return d

quarters = quarters(change_owed)
change_owed = change_owed - quarters * 25

dimes = dimes(change_owed)
change_owed = change_owed - dimes * 10

nickels = nickels(change_owed)
change_owed = change_owed - nickels * 5

pennies = pennies(change_owed)
change_owed = change_owed - pennies * 1

coins = quarters + dimes + nickels + pennies
print(coins)
