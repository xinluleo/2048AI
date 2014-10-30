__author__ = 'xin'

import math

directionVectors = (UP_VEC, DOWN_VEC, LEFT_VEC, RIGHT_VEC) = ((-1, 0), (1, 0), (0, -1), (0, 1))
LogTable = {0: 0, 2 : 1, 4 : 2, 8 : 3, 16 : 4, 32 : 5, 64 : 6, 128 : 7, 256 : 8, 512 : 9, 1024 : 10, 2048 : 11, 4096 : 12, 8192 : 13} 
EmptyPenalty = {16 : 1000, 15 : 1000, 14 : 950, 13 : 900, 12: 850, 11 : 800, 10 : 700, 9 : 600, 8 : 500, 7 : 350, 6 : 200, 5 :   50, 4 : -200, 3 : -500, 2 : - 800, 1 : -1200, 0 : -1800}  

edge_bonus = 1.5

def findFarthestAdj(grid, (x, y), direction):
    while True:
        new_x, new_y = x + directionVectors[direction][0], y + directionVectors[direction][1]
        if new_x < 0 or new_x >= grid.size or new_y < 0 or new_y >= grid.size:
            break
        new_cell = grid.map[new_x][new_y]
        x, y = new_x, new_y
        if new_cell != 0:
            break
    return grid.map[x][y]


def smoothness(grid):
    smooth = 0.0
    for x in xrange(grid.size):
        for y in xrange(grid.size):
            if grid.map[x][y] != 0:
                value = LogTable[grid.map[x][y]]
                for direction in (1, 3):
                    adjCellValue = findFarthestAdj(grid, (x, y), direction)
                    if adjCellValue != 0:
                        targetValue = LogTable[adjCellValue]
                        diff = math.fabs(value - targetValue)
                        if x == 0 or x == grid.size or y == 0 or y == grid.size:
                            diff *= edge_bonus
                        smooth -= diff
    return smooth


def monotonicity(grid):
    #monotonicity for left, right, up, down direction
    mono = [0, 0, 0, 0]
    
    #left/right direction
    for x in xrange(grid.size):
        current = 0
        next = current + 1
        while next < grid.size:
            #find the first non-empty cell in row x next to current
            while next < grid.size and grid.map[x][next] == 0:
                next += 1
            if next == grid.size:
                break
            curCellVal = LogTable[grid.map[x][current]]
            nextCellVal = LogTable[grid.map[x][next]]
            diff = curCellVal - nextCellVal
            if x == 0 or x == grid.size:
                diff *= edge_bonus
            mono[0] += diff
            mono[1] -= diff
            current = next
            next += 1

    #up/down direction
    for y in xrange(grid.size):
        current = 0
        next = current + 1
        while next < grid.size:
            #find the first non-empty cell in column y below current
            while next < grid.size and grid.map[next][y] == 0:
                next += 1
            if next == grid.size:
                break
            curCellVal = LogTable[grid.map[current][y]]
            nextCellVal = LogTable[grid.map[next][y]]
            diff = curCellVal - nextCellVal
            if y == 0 or y == grid.size:
                diff *= edge_bonus
            mono[2] += diff
            mono[3] -= diff
            current = next
            next += 1

    return max(mono[0], mono[1]) + max(mono[2], mono[3])
    #return mono[0] + mono[2]

def emptyness(grid):
    avail_cells_num = len(grid.getAvailableCells())
    return EmptyPenalty[avail_cells_num]

def evaluate(grid):
    smoothWeight = 6.5
    monoWeight = 16
    maxWeight = 5.5

    smooth = smoothness(grid) * smoothWeight
    mono = monotonicity(grid) * monoWeight
    avail_cells_num = len(grid.getAvailableCells())
    empty = EmptyPenalty[avail_cells_num]
    maxtile = grid.getMaxTile() * maxWeight * 0.2
    #print "smooth = ", smooth, " mono = ", mono, " empty = ", empty, " maxtile = ", maxtile

    return smooth + mono + empty + maxtile


def maxValue(grid, alpha, beta, depth):
    if not grid.canMove():
        return float('-inf'), None

    if depth == 0:
        return evaluate(grid), None
    depth -= 1
    v = float('-inf')

    bestMove = None
    for i in grid.getAvailableMoves():
        if bestMove is None:
            bestMove = i
        gridCopy = grid.clone()
        gridCopy.move(i)
        value, __ = minValue(gridCopy, alpha, beta, depth)
        if value > v:
            bestMove = i
            v = value
        if v >= beta:
            return v, bestMove
        alpha = max(alpha, v)
    return v, bestMove


def minValue(grid, alpha, beta, depth):
    if not grid.canMove():
        return float('-inf'), None

    if depth == 0:
        return evaluate(grid), None
    depth -= 1
    v = float('inf')

    bestMove = None
    for i in grid.getAvailableCells():
        for tileValue in (2, 4):
            gridCopy = grid.clone()
            gridCopy.insertTile(i, tileValue)
            value, __ = maxValue(gridCopy, alpha, beta, depth)
            if value < v:
                bestMove = i
                v = value

            if v <= alpha:
                return v, bestMove

            beta = min(beta, v)
        return v, bestMove
