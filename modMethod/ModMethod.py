from modRect import Rule
from modRect import ModRectangle
from _collections import deque
from decimal import Decimal


def solve(optimizingFunc, lipzitsFunc, precision, epsilon, lower, upper, ruleSubList, ruleMainList):
    lipzitsConst = lipzitsFunc(epsilon)
    rectanglePool = deque()
    firstRectangle = ModRectangle(lower, upper)
    rectanglePool.append(firstRectangle)
    counter = 1
    optimal = 1
    x_opt = 0
    y_opt = 0
    currentMin = Decimal(optimizingFunc(lower))
    step = Decimal(2 * (precision - epsilon) / lipzitsConst)
    while len(rectanglePool) != 0:
        currentRectangle = rectanglePool.popleft()
        iterPoint = currentRectangle.getIterPoint(step)
        funcVal = optimizingFunc(iterPoint)
        if funcVal > currentMin:
            step += Decimal((funcVal - currentMin) / lipzitsConst)
        else:
            currentMin = funcVal
            optimal = counter
            x_opt = iterPoint[0]
            y_opt = iterPoint[1]
        newRects = currentRectangle.split(step, ruleSubList)
        if ruleMainList == Rule.ADDTOBEGIN:
            rectanglePool.extendleft(newRects)
        elif ruleMainList == Rule.ADDTOEND:
            rectanglePool.extend(newRects)
        counter += 1
    return [currentMin, optimal, counter, x_opt, y_opt]
