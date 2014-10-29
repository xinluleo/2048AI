#!/usr/bin/env python
# coding:utf-8

from random import randint
from BaseAI import BaseAI
from AlphaBeta import maxValue
from AlphaBeta import monotonicity
from AlphaBeta import smoothness
from AlphaBeta import emptyness

import math

defaultPossibility = 0.7
possibleNewTileValue = [2, 4]

class PlayerAI(BaseAI):

    def getNewTileValue(self):
        if randint(0, 99) < 100 * defaultPossibility:
            return possibleNewTileValue[0]
        else:
            return possibleNewTileValue[1]

    def result(self, moveDirect, grid):
        newGrid = grid.clone()
        newGrid.move(moveDirect)
        return newGrid

    def getMove(self, grid):
        # I'm too naive, please change me!
        depth = 9 
        bestmove = maxValue(grid, float('-inf'), float('inf'), depth)[1]
        #mono = monotonicity(grid) * 15
        #smooth = smoothness(grid) * 6.0
        #empty = emptyness(grid)  
        #sqr_sum = square_sum(grid) * 0.1
        #maxtile = grid.getMaxTile() * 5.0
        #edge = edgeBonus(grid) * 0.1 
        #if len(grid.getAvailableCells()) < 4:
        #    smooth *= 0.15
        #    mono *= 0.15
        #print "player best move = ", bestmove, " monotonicity = ", mono, " smoothness = ", smooth, " empty = ", empty, " maxtile = ", maxtile, " edge = " , edge
        return bestmove
