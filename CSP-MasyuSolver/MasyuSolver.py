from constraint import *
from problems import *
from math import *
from copy import *


def isBlank(v):
    if v == '╬':
        return True
    return False


def isFilled(v):
    if v == '┼':
        return True
    return False


def ignoreOptions(activeList, ignored):
    for i in ignored:
        if i in activeList:
            activeList.remove(i)


"""CONSTRAINTS"""


def filledCellConstraint(own, top, right, bottom, left):
    if own == "BL" and (bottom != "TB" or left != "LR"):
        return False
    elif own == "BR" and (bottom != "TB" or right != "LR"):
        return False
    elif own == "TL" and (top != "TB" or left != "LR"):
        return False
    elif own == "TR" and (top != "TB" or right != "LR"):
        return False

    return True

def blankCellConstraint(own, top, right, bottom, left):
    if own == "LR" and left == "LR" and right == "LR":
        return False
    elif own == "TB" and top == "TB" and bottom == "TB":
        return False
    return True

"""bana bakan yoksa empty degilsam false"""


def allCellConstraint(own, top, right, bottom, left):
    # ["TB", "LR", "BL", "BR", "TL",
    #  "TR", "CC"]
    if own == 'CC':
        return True
    else:

        # if own[1] == 'R' and "L" not in right:
        #     return False
        # el
        #
        if "T" in own and "B" not in top:
            return False
        elif "B" in own and "T" not in bottom:
            return False
        elif "R" in own and "L" not in right:
            return False
        elif "L" in own and "R" not in left:
            return False

            # elif own[1] == 'R' and "L" not in right:
        #     return False


    return True
"""CONSTRAINTS"""

def singleCircleConstraint(*args):
    size = int(sqrt(len(args)))
    visitedList = []
    start = -1
    for i in range(len(args)):
        if args[i] != 'CC':
            start = i
        else:
            break

    if start == -1:
        return False

    current = start

    while(True):
        visitedList.append(current)
        if args[current] == 'TB':
            current = current + size
        elif args[current] == 'LR':
            current = current + 1
        elif args[current] == 'BL':
            current = current - 1
        elif args[current] == 'BR':
            current = current + 1
        elif args[current] == 'TL':
            current = current - 1
        elif args[current] == 'TR':
            current = current + 1

    for i in range(len(args)):
        if args[i] != 'CC' and i not in visitedList:
            return False

    return True

def getArea(c, p, size):
    i = c
    j = p
    res = []
    res.append((i, j))

    # uste git
    i = i - 1
    if i < 0 or j < 0 or j > size - 1 or i > size - 1:
        res.append((-1,-1))
    else:
        res.append((i, j))

    # ustten saga git
    i = i + 1
    j = j + 1
    if i < 0 or j < 0 or j > size - 1 or i > size - 1:
        res.append((-1,-1))
    else:
        res.append((i, j))

    # sagdan alta git
    i = i + 1
    j = j - 1
    if i < 0 or j < 0 or j > size - 1 or i > size - 1:
        res.append((-1,-1))
    else:
        res.append((i, j))

    # ustten saga git
    i = i - 1
    j = j - 1
    if i < 0 or j < 0 or j > size - 1 or i > size - 1:
        res.append((-1,-1))
    else:
        res.append((i, j))

    return res


def getAllCells(size, size2):
    res = []
    for i in range(size):
        for j in range(size2):
            res.append((i,j))

    return res

def solveMasyu(state):
    problem = Problem()
    size = len(state)
    filleds = []
    blanks = []

    problem.addVariable((-1,-1), [None])

    for i in range(size):
        for j in range(size):
            tup = (i, j)
            Available = ["TB", "LR", "BL", "BR", "TL",
                         "TR", "CC"]

            if state[i][j] != '.' or True:

                try:
                    if isBlank(state[i][j]):
                        blanks.append(tup)
                        ignoreOptions(Available, ["CC", "BL", "BR", "TL", "TR"])

                    elif isFilled(state[i][j]):
                        filleds.append(tup)
                        ignoreOptions(Available, ["CC", "TB", "LR"])

                    if i == 0 or i == size - 1:
                        ignoreOptions(Available, ["TB"])
                        if i == 0:
                            ignoreOptions(Available, ["TL", "TR"])
                        elif i == size - 1:
                            ignoreOptions(Available, ["BL", "BR"])

                    if j == 0 or j == size - 1:
                        ignoreOptions(Available, ["LR"])
                        if j == 0:
                            ignoreOptions(Available, ["BL", "TL"])
                        elif j == size - 1:
                            ignoreOptions(Available, ["BR", "TR"])
                except ValueError:
                    pass

                problem.addVariable(tup, Available)
                print(tup, Available)

        for i in range(size):
            for j in range(size):
                tup = (i, j)
                problem.addConstraint(FunctionConstraint(allCellConstraint), getArea(i, j, size))
                if isBlank(state[i][j]):
                    problem.addConstraint(FunctionConstraint(blankCellConstraint), getArea(i, j, size))
                elif isFilled(state[i][j]):
                    problem.addConstraint(FunctionConstraint(filledCellConstraint), getArea(i, j, size))

    problem.addConstraint(FunctionConstraint(singleCircleConstraint), getAllCells(size,size))
    deneme = problem.getSolution()
    showSolution(state, deneme, size)
    isSolutionSingleLoop(deneme,state,size)
    # showSolutions(deneme, size)


def showSolutions(deneme, size):
    for i in deneme:
        showSolution(i, size)
        print("--------------")
    print(str(len(deneme)) + " solution found")

def getFirstCell(state, size):
    for i in range(size):
        for j in range(size):
            if state[i][j] == '╬' or state[i][j] == '┼':
                return (i, j)


def isSolutionSingleLoop(solution, state, size):
    startCell = getFirstCell(state, size)


def showSolution(state, solution, size):
    mode = 1
    dictMap = {
        "LR": '─',
        "TB": '│',
        "CC": '.',
        "BL": '┐',
        "BR": '┌',
        "TL": '┘',
        "TR": '└'
    }
    for i in range(size):
        for j in range(size):
            if mode == 0:
                if state[i][j] == '╬':
                    print("╬", end="")
                elif state[i][j] == '┼':
                    print("┼", end="")
                else:
                    print(dictMap[solution[(i, j)]], end="")
            else:
                print(dictMap[solution[(i, j)]], end="")
        print()
