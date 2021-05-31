import tkinter as tk

from model.grid import *

class GridVC(tk.Frame):
    def __init__(self, modelGrid, parent, **options):
        super().__init__(parent, **options)
        self.modelGrid = modelGrid
        self.canvas = tk.Canvas(self)
        self.drawGrid()
        self.canvas.pack(side="left")

        scroll_x = tk.Scrollbar(parent, orient="horizontal", command=self.canvas.xview)
        scroll_x.pack(side="bottom", fill="x")

        scroll_y = tk.Scrollbar(parent, orient="vertical", command=self.canvas.yview)
        scroll_y.pack(side="right", fill="y")

        self.canvas.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        self.canvas.configure(scrollregion = self.canvas.bbox("all"))

    def drawGrid(self):

        w = self.modelGrid.width
        h = self.modelGrid.height
        cellSize = 30
        for y in range(h+1):
            self.canvas.create_line(0, y*cellSize, w*cellSize, y*cellSize, tags="grid")
        for x in range(w+1):
            self.canvas.create_line(x*cellSize, 0, x*cellSize, h*cellSize, tags="grid")
        for y in range(h):
            for x in range(w):
                cell = self.modelGrid.getCell(x, y)

                if(cell.value < 0):
                    if(cell.sumDown <= 0 and cell.sumRight <= 0):
                        self.canvas.create_rectangle(x*cellSize, y*cellSize, (x+1)*cellSize, (y+1)*cellSize, fill="black")
                    else:
                        if(cell.sumDown > 0 and cell.sumRight > 0):
                            self.canvas.create_line(x*cellSize, y*cellSize, (x+1)*cellSize, (y+1)*cellSize)
                        if(cell.sumDown <= 0):
                            self.canvas.create_polygon([(x*cellSize, y*cellSize),
                                (x*cellSize, (y+1)*cellSize),
                                ((x+1)*cellSize, (y+1)*cellSize)], fill="black")
                        else:
                            quarter = cellSize/4
                            self.canvas.create_text(x*cellSize+quarter, (y+1)*cellSize-quarter,
                                text=cell.sumDown, tags=(x, y, "down"))
                        if(cell.sumRight <= 0):
                            self.canvas.create_polygon([(x*cellSize, y*cellSize),
                                ((x+1)*cellSize, y*cellSize),
                                ((x+1)*cellSize, (y+1)*cellSize)], fill="black")
                        else:

                            quarter = cellSize/4
                            self.canvas.create_text((x+1)*cellSize-quarter, y*cellSize+quarter,
                                text=cell.sumRight, tags=(x, y, "right"))
                elif(cell.value != 0):

                    half = cellSize/2
                    self.canvas.create_text(x*cellSize + half, y*cellSize + half,
                        tags=(x, y), text=cell.value, activefill="red")

    def reDrawGrid(self):
        # pour eviter d'interposer les chiffres, on nettoie le canvas et le redessine
        self.canvas.delete("all")
        self.drawGrid()

    def SelectedCell(self, x, y):
        x, y = x//30, y//30
        cell = self.modelGrid.getCell(x, y)
        cellSize = 30
        half = cellSize / 2
        self.canvas.create_rectangle(x*cellSize, y*cellSize, (x+1)*cellSize, (y+1)*cellSize, fill="yellow")

        if cell.value != 0 : self.canvas.create_text(x * cellSize + half, y * cellSize + half,
                         tags=(x, y), text=cell.value, activefill="red")

