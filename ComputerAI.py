#!/usr/bin/env python
# coding:utf-8

from random import randint
from BaseAI import BaseAI


class ComputerAI(BaseAI):
    def getMove(self, grid):
        # I’m too simple, please change me!
        cells = grid.getAvailableCells()
        return cells[randint(0, len(cells) - 1)] if cells else None