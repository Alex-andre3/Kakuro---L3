import tkinter as tk

from model.grid import *
from events.event import *

class GridVC(tk.Frame):
    def __init__(self, modelGrid, parent, **options):
        super().__init__(parent, **options)
        self.modelGrid = modelGrid
        self.canvas = tk.Canvas(self)
        self.cellSize = 30
        self.drawGrid()
        self.canvas.pack(side="left")

        scroll_x = tk.Scrollbar(parent, orient="horizontal", command=self.canvas.xview)
        scroll_x.pack(side="bottom", fill="x")

        scroll_y = tk.Scrollbar(parent, orient="vertical", command=self.canvas.yview)
        scroll_y.pack(side="right", fill="y")

        self.canvas.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        self.canvas.configure(scrollregion = self.canvas.bbox("all"))

        self.bind_keys()

    def bind_keys(self):
        self.canvas.bind('<Button-1>', self.saveCoordonate)
        self.canvas.bind('<KeyPress>', self.setNumber)
        #self.winfo_pointerxy()

    def drawGrid(self):

        w = self.modelGrid.width
        h = self.modelGrid.height
        for y in range(h+1):
            self.canvas.create_line(0, y*self.cellSize, w*self.cellSize, y*self.cellSize, tags="grid")
        for x in range(w+1):
            self.canvas.create_line(x*self.cellSize, 0, x*self.cellSize, h*self.cellSize, tags="grid")
        for y in range(h):
            for x in range(w):
                cell = self.modelGrid.getCell(x, y)

                if(cell.value < 0):
                    if(cell.sumDown <= 0 and cell.sumRight <= 0):
                        self.canvas.create_rectangle(x*self.cellSize, y*self.cellSize, (x+1)*self.cellSize, (y+1)*self.cellSize, fill="black")
                    else:
                        if(cell.sumDown > 0 and cell.sumRight > 0):
                            self.canvas.create_line(x*self.cellSize, y*self.cellSize, (x+1)*self.cellSize, (y+1)*self.cellSize)
                        if(cell.sumDown <= 0):
                            self.canvas.create_polygon([(x*self.cellSize, y*self.cellSize),
                                (x*self.cellSize, (y+1)*self.cellSize),
                                ((x+1)*self.cellSize, (y+1)*self.cellSize)], fill="black")
                        else:
                            quarter = self.cellSize/4
                            self.canvas.create_text(x*self.cellSize+quarter, (y+1)*self.cellSize-quarter,
                                text=cell.sumDown, tags=(x, y, "down"))
                        if(cell.sumRight <= 0):
                            self.canvas.create_polygon([(x*self.cellSize, y*self.cellSize),
                                ((x+1)*self.cellSize, y*self.cellSize),
                                ((x+1)*self.cellSize, (y+1)*self.cellSize)], fill="black")
                        else:

                            quarter = self.cellSize/4
                            self.canvas.create_text((x+1)*self.cellSize-quarter, y*self.cellSize+quarter,
                                text=cell.sumRight, tags=(x, y, "right"))
                elif(cell.value != 0):

                    half = self.cellSize/2
                    self.canvas.create_text(x*self.cellSize + half, y*self.cellSize + half,
                        tags=(x, y), text=cell.value, activefill="red")

    def reDrawGrid(self):
        # pour eviter d'interposer les chiffres, on nettoie le canvas et le redessine
        self.canvas.delete("all")
        self.drawGrid()

    def SelectedCell(self, xMouse, yMouse):
        x, y = xMouse//self.cellSize, yMouse//self.cellSize
        cell = self.modelGrid.getCell(x, y)
        half = self.cellSize / 2
        self.canvas.create_rectangle(x*self.cellSize, y*self.cellSize, (x+1)*self.cellSize, (y+1)*self.cellSize, fill="yellow")

        if cell.value != 0 : self.canvas.create_text(x * self.cellSize + half, y * self.cellSize + half,
                         tags=(x, y), text=cell.value, activefill="red")

    def getCellWithCoords(self, x, y):
        try:
            print("Valeur de la case: ", self.modelGrid.getCell((x//self.cellSize), y//self.cellSize).value)
            return self.modelGrid.getCell((x//self.cellSize), y//self.cellSize)

        except IndexError:
            print("Oops! Vous avez appuyé en dehors du plateau de jeu !")
            return None

    def updateCellValue(self, x, y, value):
        self.modelGrid.getCell((x//self.cellSize), y//self.cellSize).setValue(value)

    # --- events callbacks ---

    def saveCoordonate(self, event):
        try:
            # self.grid.getCellWithCoords(event.x, event.y)

            # if event.y // 30 < self.grid.grid.height and event.x // 30 < self.grid.grid.width\
                                                    # and self.grid.getCellWithCoords(event.x, event.y).value != -1:
            if self.getCellWithCoords(event.x, event.y).value != None and self.getCellWithCoords(event.x, event.y).value != -1:

                self.theEvent.set_coord([event.x, event.y])
                x, y = self.theEvent.get_coord()
                self.reDrawGrid()
                self.SelectedCell(x, y)

        except AttributeError:
            pass

    def setNumber(self, event):
        try:
            x, y = self.theEvent.get_coord()
            self.updateCellValue(x, y, int(event.keysym))
            self.reDrawGrid()
            self.SelectedCell(x, y)

        except ValueError:
            print("Erreur, il faut rentrer un chiffre.")
