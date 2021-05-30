import tkinter as tk

from model.grid import *

class GridVC(tk.Canvas):
    def __init__(self, grid, parent, **options):
        super().__init__(parent, **options)
        self.grid = grid
        self.drawGrid()

    def drawGrid(self):

        w = self.grid.width
        h = self.grid.height
        cellSize = 30
        for y in range(h+1):
            self.create_line(0, y*cellSize, w*cellSize, y*cellSize, tags="grid")
        for x in range(w+1):
            self.create_line(x*cellSize, 0, x*cellSize, h*cellSize, tags="grid")
        for y in range(h):
            for x in range(w):
                cell = self.grid.getCell(x, y)

                if(cell.value < 0):
                    if(cell.sumDown <= 0 and cell.sumRight <= 0):
                        self.create_rectangle(x*cellSize, y*cellSize, (x+1)*cellSize, (y+1)*cellSize, fill="black")
                    else:
                        if(cell.sumDown > 0 and cell.sumRight > 0):
                            self.create_line(x*cellSize, y*cellSize, (x+1)*cellSize, (y+1)*cellSize)
                        if(cell.sumDown <= 0):
                            self.create_polygon([(x*cellSize, y*cellSize),
                                (x*cellSize, (y+1)*cellSize),
                                ((x+1)*cellSize, (y+1)*cellSize)], fill="black")
                        else:
                            quarter = cellSize/4
                            self.create_text(x*cellSize+quarter, (y+1)*cellSize-quarter,
                                text=cell.sumDown, tags=(x, y, "down"))
                        if(cell.sumRight <= 0):
                            self.create_polygon([(x*cellSize, y*cellSize),
                                ((x+1)*cellSize, y*cellSize),
                                ((x+1)*cellSize, (y+1)*cellSize)], fill="black")
                        else:

                            quarter = cellSize/4
                            self.create_text((x+1)*cellSize-quarter, y*cellSize+quarter,
                                text=cell.sumRight, tags=(x, y, "right"))
                elif(cell.value != 0):

                    half = cellSize/2
                    self.create_text(x*cellSize + half, y*cellSize + half,
                        tags=(x, y), text=cell.value)

    def reDrawGrid(self):
        # pour eviter d'interposer les chiffres, on nettoie le canvas et le redessine
        self.delete("all")
        self.drawGrid()