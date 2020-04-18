from decimal import Decimal
from enum import Enum
from _collections import deque


class Rule(Enum):
    ADDTOBEGIN = 1
    ADDTOEND = 2


class ModRectangle:
    def __init__(self, lowerBound, upperBound):
        self.lowerPoint = lowerBound
        self.upperPoint = upperBound

    def getIterPoint(self, h):
        return list(map(lambda low, up: min(low + h / Decimal(2), up), self.lowerPoint, self.upperPoint))

    def split(self, h, ruleSubList):
        subList = deque()
        for i in range(len(self.lowerPoint)):
            if self.upperPoint[i] - self.lowerPoint[i] > h:
                newLower = self.lowerPoint[:]
                newLower[i] += h
                curIter = i
                newUp = [
                    min(self.lowerPoint[index] + h, self.upperPoint[index]) if index < curIter else self.upperPoint[
                        index] for index, item in enumerate(self.lowerPoint)]
                if ruleSubList == Rule.ADDTOBEGIN:
                    subList.appendleft(ModRectangle(newLower, newUp))
                elif ruleSubList == Rule.ADDTOEND:
                    subList.append(ModRectangle(newLower, newUp))
        return subList


def solve(optimizingFunc, lipzitsFunc, precision, epsilon, lower, upper, ruleSubList, ruleMainList):
    if(isinstance(ruleSubList,int)):
        ruleSubList = Rule(ruleSubList)
    if(isinstance(ruleMainList,int)):
        ruleMainList = Rule(ruleMainList)
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