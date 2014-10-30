__author__ = 'xin'

import math

directionVectors = (UP_VEC, DOWN_VEC, LEFT_VEC, RIGHT_VEC) = ((-1, 0), (1, 0), (0, -1), (0, 1))
LogTable = {0: 0, 2: 1, 4: 2, 8: 3, 16: 4, 32: 5, 64: 6, 128: 7, 256: 8, 512: 9, 1024: 10, 2048: 11, 4096: 12, 8192: 13}
EmptyPenalty = {16: 1000, 15: 1000, 14: 950, 13: 900, 12: 850, 11: 800, 10: 700, 9: 600, 8: 500, 7: 350, 6: 200, 5: 50,
                4: -200, 3: -500, 2: - 800, 1: -1200, 0: -1800}
GridRecord = {}  # {GridKey : [smoothness, monotonicity]}

edge_bonus = 1.5


def findFarthestAdj(grid, (x, y), direction):
    while True:
        new_x, new_y = x + directionVectors[direction][0], y + directionVectors[direction][1]
        if grid.crossBound((new_x, new_y)):
            break
        new_cell = grid.map[new_x][new_y]
        x, y = new_x, new_y
        if new_cell != 0:
            break
    return grid.map[x][y]


def smooth_row(grid, x):
    diff = 0.0
    for y in xrange(grid.size):
        if grid.map[x][y] != 0:
            value = LogTable[grid.map[x][y]]
            adjCellValue = findFarthestAdj(grid, (x, y), 3)
            if adjCellValue != 0:
                targetValue = LogTable[adjCellValue]
                diff += math.fabs(value - targetValue)
    return diff


def smooth_col(grid, y):
    diff = 0.0
    for x in xrange(grid.size):
        if grid.map[x][y] != 0:
            value = LogTable[grid.map[x][y]]
            adjCellValue = findFarthestAdj(grid, (x, y), 1)
            if adjCellValue != 0:
                targetValue = LogTable[adjCellValue]
                diff += math.fabs(value - targetValue)
    return diff


def smoothness(grid, rows, cols):
    smooth = 0.0

    row_diff = 0.0
    for x in xrange(grid.size):
        if rows[x] in GridRecord:
            if not GridRecord[rows[x]][0] is None:
                row_diff = GridRecord[rows[x]][0]
                #print "HIT !!! row_diff = ", row_diff, type(row_diff)
            else:
                row_diff = smooth_row(grid, x)
                GridRecord[rows[x]][0] = row_diff
                GridRecord[rows[x + grid.size]][0] = row_diff
        else:
            row_diff = smooth_row(grid, x)
            GridRecord[rows[x]] = [row_diff, None]
            GridRecord[rows[x + grid.size]] = [row_diff, None]
        if x == 0 or x == grid.size:
            row_diff *= edge_bonus
        smooth -= row_diff

    col_diff = 0.0
    for y in xrange(grid.size):
        if cols[y] in GridRecord:
            if not GridRecord[cols[y]][0] is None:
                col_diff = GridRecord[cols[y]][0]
                #print "HIT !!!"
            else:
                col_diff = smooth_col(grid, y)
                GridRecord[cols[y]][0] = col_diff
                GridRecord[cols[y + grid.size]][0] = col_diff
        else:
            col_diff = smooth_col(grid, y)
            GridRecord[cols[y]] = [col_diff, None]
            GridRecord[cols[y + grid.size]] = [col_diff, None]
        if y == 0 or y == grid.size:
            col_diff *= edge_bonus
        smooth -= col_diff

    return smooth


def mono_row(grid, x):
    current = 0
    next = current + 1
    diff = 0.0
    while next < grid.size:
        #find the first non-empty cell in row x next to current
        while next < grid.size and grid.map[x][next] == 0:
            next += 1
        if next == grid.size:
            break
        curCellVal = LogTable[grid.map[x][current]]
        nextCellVal = LogTable[grid.map[x][next]]
        diff += curCellVal - nextCellVal
        current = next
        next += 1

    return diff


def mono_col(grid, y):
    current = 0
    next = current + 1
    diff = 0.0
    while next < grid.size:
        while next < grid.size and grid.map[next][y] == 0:
            next += 1
        if next == grid.size:
            break
        curCellVal = LogTable[grid.map[current][y]]
        nextCellVal = LogTable[grid.map[next][y]]
        diff += curCellVal - nextCellVal
        current = next
        next += 1

    return diff


def monotonicity(grid, rows, cols):
    # monotonicity for left, right, up, down direction
    mono = [0, 0, 0, 0]

    # left/right direction
    row_diff = 0.0
    for x in xrange(grid.size):
        if rows[x] in GridRecord:
            if not GridRecord[rows[x]][1] is None:
                row_diff = GridRecord[rows[x]][1]
            else:
                row_diff = mono_row(grid, x)
                GridRecord[rows[x]][1] = row_diff
        else:
            row_diff = mono_row(grid, x)
            GridRecord[rows[x]] = [None, row_diff]
        if x == 0 or x == grid.size:
            row_diff *= edge_bonus
        mono[0] += row_diff
        mono[1] -= row_diff

    #up/down direction
    col_diff = 0.0
    for y in xrange(grid.size):
        if cols[y] in GridRecord:
            if not GridRecord[cols[y]][1] is None:
                col_diff = GridRecord[cols[y]][1]
            else:
                col_diff = mono_col(grid, y)
                GridRecord[cols[y]][1] = col_diff
        else:
            col_diff = mono_col(grid, y)
            GridRecord[cols[y]] = [None, col_diff]
        if y == 0 or y == grid.size:
            col_diff *= edge_bonus
        mono[2] += col_diff
        mono[3] -= col_diff

    return max(mono[0], mono[1]) + max(mono[2], mono[3])
    #return mono[0] + mono[2]


def emptyness(grid):
    avail_cells_num = len(grid.getAvailableCells())
    return EmptyPenalty[avail_cells_num]


def evaluate(grid):
    smoothWeight = 6.5
    monoWeight = 16
    maxWeight = 5.5

    rows = []
    cols = []
    for i in xrange(2 * grid.size):
        rows.append(0)
        cols.append(0)

    for x in xrange(grid.size):
        base_right = 0x1000
        base_left = 0x0001
        for y in xrange(grid.size):
            rows[x] += LogTable[grid.map[x][y]] * base_right
            rows[x + grid.size] += LogTable[grid.map[x][y]] * base_left
            base_right >>= 4
            base_left <<= 4

    for y in xrange(grid.size):
        base_down = 0x1000
        base_up = 0x0001
        for x in xrange(grid.size):
            cols[y] += LogTable[grid.map[x][y]] * base_down
            cols[y + grid.size] += LogTable[grid.map[x][y]] * base_up
            base_down >>= 4
            base_up <<= 4

    smooth = smoothness(grid, rows, cols) * smoothWeight
    mono = monotonicity(grid, rows, cols) * monoWeight

    avail_cells_num = len(grid.getAvailableCells())
    empty = EmptyPenalty[avail_cells_num] * 0.3
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
