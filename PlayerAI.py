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
        #mono = monotonicity(grid) * 16
        #smooth = smoothness(grid) * 6.5
        #empty = emptyness(grid) * 1.8
        #maxtile = grid.getMaxTile() * 5.5
        #print "player best move = ", bestmove, " monotonicity = ", mono, " smoothness = ", smooth, " empty = ", empty, " maxtile = ", maxtile, " edge = " , edge
        return bestmove
