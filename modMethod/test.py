from decimal import Decimal
from method import solve
import math
from modRect import Rule


def func(vars):
    power = -math.sqrt(sum(list(map(lambda item: abs(item) / len(vars), vars))))
    return Decimal(math.exp(power)) * Decimal(-10)


def lipFunc(epsilon):
    return Decimal(25) / epsilon


low = [Decimal(-1), Decimal(-1)]

up = [Decimal(1), Decimal(1)]
precision = Decimal(0.01)
epsilon = Decimal(0.001)
result = solve(func, lipFunc, precision, epsilon, low, up, Rule.ADDTOBEGIN, Rule.ADDTOBEGIN)

print("min ={0:.20f} on {1} of {2}".format(result[0], result[1], result[2]))
print("coords x={0:.20f} | y={1:.20f}".format(result[3], result[4]))
