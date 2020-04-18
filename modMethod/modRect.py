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
