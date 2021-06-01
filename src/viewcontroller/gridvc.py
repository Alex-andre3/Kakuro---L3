import tkinter as tk
import tkinter.font

from model.grid import *
from events.event import *
from solver.script_dictionary import creer_dictionnaire


class GridVC(tk.Frame):
    def __init__(self, modelGrid, parent, **options):
        super().__init__(parent, **options)
        self.modelGrid = modelGrid
        self.canvas = tk.Canvas(self)
        self.theEvent = Event()
        self.combinationPossible = creer_dictionnaire()
        self.cellSize = 30
        self.drawGrid()
        self.canvas.pack(side="left")

        scroll_x = tk.Scrollbar(parent, orient="horizontal", command=self.canvas.xview)
        scroll_x.pack(side="bottom", fill="x")

        scroll_y = tk.Scrollbar(parent, orient="vertical", command=self.canvas.yview)
        scroll_y.pack(side="right", fill="y")

        self.canvas.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        self.bind_keys()

    def bind_keys(self):
        self.canvas.bind('<Button-1>', lambda event: self.saveCoordonate(event))
        self._root().bind('<KeyPress>', lambda event: self.setNumber(event))
        print("binded")
        # self.winfo_pointerxy()

    def drawGrid(self):

        w = self.modelGrid.width
        h = self.modelGrid.height
        for y in range(h + 1):
            self.canvas.create_line(0, y * self.cellSize, w * self.cellSize, y * self.cellSize, tags="grid")
        for x in range(w + 1):
            self.canvas.create_line(x * self.cellSize, 0, x * self.cellSize, h * self.cellSize, tags="grid")
        for y in range(h):
            for x in range(w):
                cell = self.modelGrid.getCell(x, y)

                if (cell.value < 0):
                    if (cell.sumDown <= 0 and cell.sumRight <= 0):
                        self.canvas.create_rectangle(x * self.cellSize, y * self.cellSize, (x + 1) * self.cellSize,
                                                     (y + 1) * self.cellSize, fill="black")
                    else:
                        if (cell.sumDown > 0 and cell.sumRight > 0):
                            self.canvas.create_line(x * self.cellSize, y * self.cellSize, (x + 1) * self.cellSize,
                                                    (y + 1) * self.cellSize)
                        if (cell.sumDown <= 0):
                            self.canvas.create_polygon([(x * self.cellSize, y * self.cellSize),
                                                        (x * self.cellSize, (y + 1) * self.cellSize),
                                                        ((x + 1) * self.cellSize, (y + 1) * self.cellSize)],
                                                       fill="black")
                        else:
                            quarter = self.cellSize / 4
                            self.canvas.create_text(x * self.cellSize + quarter, (y + 1) * self.cellSize - quarter,
                                                    text=cell.sumDown, tags=(x, y, "down"))
                        if (cell.sumRight <= 0):
                            self.canvas.create_polygon([(x * self.cellSize, y * self.cellSize),
                                                        ((x + 1) * self.cellSize, y * self.cellSize),
                                                        ((x + 1) * self.cellSize, (y + 1) * self.cellSize)],
                                                       fill="black")
                        else:

                            quarter = self.cellSize / 4
                            self.canvas.create_text((x + 1) * self.cellSize - quarter, y * self.cellSize + quarter,
                                                    text=cell.sumRight, tags=(x, y, "right"))
                elif (cell.value != 0):

                    half = self.cellSize / 2
                    self.canvas.create_text(x * self.cellSize + half, y * self.cellSize + half,
                                            tags=(x, y), font=("", 18), text=cell.value, activefill="red")

    def reDrawGrid(self):
        # pour eviter d'interposer les chiffres, on nettoie le canvas et le redessine
        self.canvas.delete("all")
        self.drawGrid()

    def SelectedCell(self, xMouse, yMouse):
        x, y = xMouse // self.cellSize, yMouse // self.cellSize
        cell = self.modelGrid.getCell(x, y)
        half = self.cellSize / 2
        self.canvas.create_rectangle(x * self.cellSize, y * self.cellSize, (x + 1) * self.cellSize,
                                     (y + 1) * self.cellSize, fill="yellow")

        if cell.value != 0: self.canvas.create_text(x * self.cellSize + half, y * self.cellSize + half,
                                                    tags=(x, y), font=("", 18), text=cell.value, activefill="red")

    def getCellWithCoords(self, x, y):
        try:
            print("Valeur value: ", self.modelGrid.getCell((x // self.cellSize), y // self.cellSize).value)
            print("Valeur sumDown: ", self.modelGrid.getCell((x // self.cellSize), y // self.cellSize).sumDown)
            print("Valeur sumRight: ", self.modelGrid.getCell((x // self.cellSize), y // self.cellSize).sumRight)
            # self.test2(x, y)
            return self.modelGrid.getCell((x // self.cellSize), y // self.cellSize)

        except IndexError:
            print("Oops! Vous avez appuyé en dehors du plateau de jeu !")
            return None

    def updateCellValue(self, x, y, value):
        self.modelGrid.getCell((x // self.cellSize), y // self.cellSize).setValue(value)

    # --- events callbacks ---

    def saveCoordonate(self, event):
        xScroll = self.canvas.xview()
        a = xScroll[0]  # seul la position minimal du scroller nous interesse
        dim = self.canvas.bbox("all")
        xValueWithScrollBar = int(dim[2] * a + event.x)

        yScroll = self.canvas.yview()
        b = yScroll[0]
        yValueWithScrollBar = int(dim[3] * b + event.y)

        try:
            if self.getCellWithCoords(xValueWithScrollBar,
                                      yValueWithScrollBar).value is not None and self.getCellWithCoords(
                xValueWithScrollBar,
                yValueWithScrollBar).value != -1:
                self.theEvent.set_coord([xValueWithScrollBar, yValueWithScrollBar])
                x, y = self.theEvent.get_coord()
                self.reDrawGrid()
                self.SelectedCell(x, y)
                self.test(x, y)
            else:
                self.theEvent.set_coord([xValueWithScrollBar, yValueWithScrollBar])
                x, y = self.theEvent.get_coord()
                self.test2(x, y)


        except AttributeError:
            print("error")

    def setNumber(self, event):
        print("set")
        try:
            x, y = self.theEvent.get_coord()
            self.updateCellValue(x, y, int(event.keysym))
            self.reDrawGrid()
            self.SelectedCell(x, y)

        except ValueError:
            print("Erreur, il faut rentrer un chiffre.")

    def test(self, x, y):  # cliquer sur la case vide

        x, y = x // self.cellSize, y // self.cellSize

        cptx = 0  # compteur des cases suivantes horizontaux
        cpty = 0  # compteur des cases suivantes varticaux
        lst = []  # pour sauvgarder les chiffre initiaux

        for i in range(x, -1, -1):
            if self.modelGrid.getCell(i, y).value == -1:
                if self.modelGrid.getCell(i, y).sumRight > 0:
                    lst.append(self.modelGrid.getCell(i, y).sumRight)
                    break
            else:
                cptx += 1

        for i in range(x + 1, self.modelGrid.width):
            if self.modelGrid.getCell(i, y).value == -1:
                break
            else:
                cptx += 1

        for i in range(y, -1, -1):
            if self.modelGrid.getCell(x, i).value == -1:
                if self.modelGrid.getCell(x, i).sumDown is not None:
                    lst.append(self.modelGrid.getCell(x, i).sumDown)
                    break
            else:
                cpty += 1

        for i in range(y + 1, self.modelGrid.height):
            if self.modelGrid.getCell(x, i).value == -1:
                break
            else:
                cpty += 1

        print(cptx, cpty)
        print(lst)
        print("attention roulement de tambour")
        print(lst[0], creer_dictionnaire()[lst[0]][cptx])
        print(lst[1], creer_dictionnaire()[lst[1]][cpty])

        # print(x, "|", y)

    def test2(self, x, y):  # cliquer sur la case avec un ou deux chiffres
        x, y = x // self.cellSize, y // self.cellSize
        cptx = 0  # compteur des cases suivantes horizontaux
        cpty = 0  # compteur des cases suivantes varticaux
        lstr = []  # pour sauvgarder les chiffre initiaux
        lstd = []  # pour sauvgarder les chiffre initiaux

        if self.modelGrid.getCell(x, y).value == -1 and self.modelGrid.getCell(x, y).sumRight > 0:
            lstr.append(self.modelGrid.getCell(x, y).sumRight)
            for i in range(x + 1, self.modelGrid.width):
                if self.modelGrid.getCell(i, y).value == -1:
                    break
                else:
                    cptx += 1

        if self.modelGrid.getCell(x, y).value == -1 and self.modelGrid.getCell(x, y).sumDown > 0:
            lstd.append(self.modelGrid.getCell(x, y).sumDown)
            for i in range(y + 1, self.modelGrid.height):
                if self.modelGrid.getCell(x, i).value == -1:
                    break
                else:
                    cpty += 1

        if not lstr:
            print(lstd[0], creer_dictionnaire()[lstd[0]][cpty])
        elif not lstd:
            print(lstr[0], creer_dictionnaire()[lstr[0]][cptx])
        else:
            print(lstd[0], creer_dictionnaire()[lstd[0]][cpty])
            print(lstr[0], creer_dictionnaire()[lstr[0]][cptx])
