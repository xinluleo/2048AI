#!/usr/bin/env python
# coding:utf-8

from random import randint
from BaseAI import BaseAI
from AlphaBeta import * 

import math

class PlayerAI(BaseAI):
    def getMove(self, grid):
        depth = 9 
        bestmove = maxValue(grid, float('-inf'), float('inf'), depth)[1]
        #mono = monotonicity(grid) * 15
        #smooth = smoothness(grid) * 6.0
        #empty = emptyness(grid)  
        #maxtile = grid.getMaxTile() * 5.0
        #print "player best move = ", bestmove, " monotonicity = ", mono, " smoothness = ", smooth, " empty = ", empty, " maxtile = ", maxtile, " edge = " , edge
        return bestmove
