import os.path

from model.cell import *
from model.grid import *

class GridFactory:
    def __init__(self):
        pass

    def loadGrid(self, gridName):
        if not os.path.isfile(gridName):
            print('No such grid, empty grid created instead')
        else:
            cellsArray = []
            try:
                with open(gridName, "r") as f:
                    for line in f.read().splitlines():
                        cellsArray.append([])
                        for cell in line.split('_'):
                            if('/' in cell):
                                sums = cell.split('/')
                                cellsArray[-1].append(Cell(-1, sums[0], sums[1]))
                            else:
                                cellsArray[-1].append(Cell(int(cell)))
                return Grid(cellsArray)
            except OSError:
                print('Cannot read the grid, empty grid created instead')
        return Grid([])
