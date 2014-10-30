#!/usr/bin/env python
# coding:utf-8

from random import randint
from BaseAI import BaseAI
from AlphaBeta import minValue

class ComputerAI(BaseAI):
    def getMove(self, grid):
        depth = 8
        cells = grid.getAvailableCells()
        return cells[randint(0, len(cells) - 1)] if cells else None
        #bestPlace = minValue(grid, float('-inf'), float('inf'), depth)[1]
        #print "best place = ", bestPlace
        #return bestPlace if cells else None