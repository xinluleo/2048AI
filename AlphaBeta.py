__author__ = 'xin'

import math

directionVectors = (UP_VEC, DOWN_VEC, LEFT_VEC, RIGHT_VEC) = ((-1, 0), (1, 0), (0, -1), (0, 1))
LogTable = {2 : 1, 4 : 2, 8 : 3, 16 : 4, 32 : 5, 64 : 6, 128 : 7, 256 : 8, 512 : 9, 1024 : 10, 2048 : 11, 4096 : 12, 8192 : 13} 
EmptyPenalty = {16 : 1000, 15 : 1000, 14 : 975, 13 : 950, 12: 925, 11 : 900, 10 : 850, 9 : 800, 8 : 700, 7 : 600, 6 : 500, 5 : 350, 4 : 150, 3 : -100, 2 : -400, 1 : -600, 0 : -800}  


def square_sum(grid):
    sum = 0
    for x in grid.map:
        for y in x:
            if y != 0:
                log_y = math.log(y, 2)
                sum += log_y * log_y
    return sum

def findFarthestAdj(grid, (x, y), direction):
    while True:
        new_x, new_y = x + directionVectors[direction][0], y + directionVectors[direction][1]
        new_cell = grid.map[new_x][new_y]
        if new_cell is None:        #cross bound
            break
        x, y = new_x, new_y
        if new_cell != 0:
            break
    #print "return x, y = ", x, " ", y
    return grid.map[x][y]


def smoothness(grid):
    smooth = 0.0
    for x in xrange(grid.size):
        for y in xrange(grid.size):
            if grid.map[x][y] != 0:
                value = LogTable[grid.map[x][y]]
                for direction in (0, 2):
                    #print "x, y = ", x, y, " direction = ", direction
                    adjCellValue = findFarthestAdj(grid, (x, y), direction)
                    #print "type findFarthest Adj= ", type(adjCellValue)
                    if adjCellValue != 0:
                        targetValue = LogTable[adjCellValue]
                        smooth -= math.fabs(value - targetValue)
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
            curCellVal = grid.map[x][current]
            curCellVal = 0 if curCellVal == 0 else LogTable[curCellVal]
            nextCellVal = grid.map[x][next]
            nextCellVal = 0 if nextCellVal == 0 else LogTable[nextCellVal]
            #if curCellVal > nextCellVal:
            #    mono[0] += nextCellVal - curCellVal
            #elif nextCellVal > curCellVal:
            #    mono[1] += curCellVal - nextCellVal
            #mono[0] += 1 if curCellVal > nextCellVal else 0
            #if curCellVal > nextCellVal:
            #    mono[0] += nextCellVal - curCellVal
            mono[0] += curCellVal - nextCellVal
            mono[1] += nextCellVal - curCellVal
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
            curCellVal = grid.map[current][y]
            curCellVal = 0 if curCellVal == 0 else LogTable[curCellVal]
            nextCellVal = grid.map[next][y]
            nextCellVal = 0 if nextCellVal == 0 else LogTable[nextCellVal]
            #if curCellVal > nextCellVal:
            #    mono[2] += nextCellVal - curCellVal
            #elif nextCellVal > curCellVal:
            #    mono[3] += curCellVal - nextCellVal
            #mono[2] += 1 if curCellVal > nextCellVal else 0
            #if curCellVal > nextCellVal:
            #    mono[2] += nextCellVal - curCellVal
            mono[2] += curCellVal - nextCellVal
            mono[3] += nextCellVal - curCellVal
            current = next
            next += 1

    return max(mono[0], mono[1]) + max(mono[2], mono[3])
    #return mono[0] + mono[2]

def emptyness(grid):
    avail_cells_num = len(grid.getAvailableCells())
    #if avail_cells_num == 0:
    #    empty = -100
    #else:
        #log_avail_cells_num = math.log(avail_cells_num) / math.log(2)
    #    empty = avail_cells_num * avail_cells_num * avail_cells_num * 20
    return EmptyPenalty[avail_cells_num]

def evaluate(grid):
    smoothWeight = 6.0  
    monoWeight = 20 
    emptyWeight = 20
    maxWeight = 3.0

    smooth = smoothness(grid) * smoothWeight
    mono = monotonicity(grid) * monoWeight
    avail_cells_num = len(grid.getAvailableCells())
    empty = EmptyPenalty[avail_cells_num]
    #if avail_cells_num == 0:
    #    empty = -100
    #else:
    #    empty = avail_cells_num * avail_cells_num * avail_cells_num * emptyWeight
        #if avail_cells_num < 3:
        #    empty *= 2
        #    smooth *= 0.5
        #    mono *= 0.15
    maxtile = grid.getMaxTile() * maxWeight
    #print "smooth = ", smooth, " mono = ", mono, " empty = ", empty, " maxtile = ", maxtile


    return smooth + mono + empty + maxtile



def maxValue(grid, alpha, beta, depth):
    if not grid.canMove():
        return float('-inf'), None

    if depth == 0:
        return evaluate(grid), None
    depth -= 1
    v = float('-inf')

    # grid_backup = grid.clone()
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
            grid.insertTile(i, tileValue)
            value, __ = maxValue(gridCopy, alpha, beta, depth)
            if value < v:
                bestMove = i
                v = value

            if v <= alpha:
                return v, bestMove

            beta = min(beta, v)
        return v, bestMove
