import tkinter as tk
import tkinter.font

from model.grid import *
from events.event import *
from solver.script_dictionary import creer_dictionnaire

heatColors = ["#BF0000", "#9E3900", "#9B7200", "#899900", "#519900",
            "#199900", "#00998E", "#006B99", "#003399"]

class GridVC(tk.Frame):
    def __init__(self, modelGrid, parent, **options):
        super().__init__(parent, **options)
        self.modelGrid = modelGrid
        self.canvas = tk.Canvas(self)
        self.theEvent = Event()
        self.combinationPossible = creer_dictionnaire()
        self.cellSize = 30
        self.helpCombination = False
        self.heatmap = False
        self.helpResultFrame1 = parent.helpResultFrame1
        self.helpResultFrame2 = parent.helpResultFrame2
        self.drawGrid()
        self.canvas.pack(side="left")

        scroll_x = tk.Scrollbar(parent, orient="horizontal", command=self.canvas.xview)
        scroll_x.pack(side="bottom", fill="x")

        scroll_y = tk.Scrollbar(parent, orient="vertical", command=self.canvas.yview)
        scroll_y.pack(side="right", fill="y")

        self.canvas.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        self.bind_keys()

        self.varChiffre1 = tk.StringVar()
        self.varChiffre2 = tk.StringVar()
        self.varAddition1 = tk.StringVar()
        self.varAddition2 = tk.StringVar()
        self.text_conseil_Chiffre1 = tk.Label(self.helpResultFrame1, textvariable=self.varChiffre1)
        self.text_conseil_Chiffre2 = tk.Label(self.helpResultFrame2, textvariable=self.varChiffre2)
        self.text_conseil_Addition1 = tk.Label(self.helpResultFrame1, textvariable=self.varAddition1)
        self.text_conseil_Addition2 = tk.Label(self.helpResultFrame2, textvariable=self.varAddition2)
        self.text_conseil_Chiffre1.pack(side="top")
        self.text_conseil_Chiffre2.pack(side="bottom")
        self.text_conseil_Addition1.pack(side="top")
        self.text_conseil_Addition2.pack(side="bottom")

    def bind_keys(self):
        self.canvas.bind('<Button-1>', lambda event: self.saveCoordonate(event))
        self._root().bind('<KeyPress>', lambda event: self.setNumber(event))
        # print("binded")
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
                else:
                    if(cell.value != 0):
                        half = self.cellSize / 2
                        self.canvas.create_text(x * self.cellSize + half, y * self.cellSize + half,
                                                tags=(x, y), font=("", 18), text=cell.value, activefill="red")
                    else:
                        if(self.heatmap):
                            self.canvas.create_rectangle(x * self.cellSize, y * self.cellSize, (x + 1) * self.cellSize,
                                                    (y + 1) * self.cellSize, fill=heatColors[self.getCellHeat(x, y)-1])

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
            # print("Valeur value: ", self.modelGrid.getCell((x // self.cellSize), y // self.cellSize).value)
            # print("Valeur sumDown: ", self.modelGrid.getCell((x // self.cellSize), y // self.cellSize).sumDown)
            # print("Valeur sumRight: ", self.modelGrid.getCell((x // self.cellSize), y // self.cellSize).sumRight)
            self.test2(x, y)
            return self.modelGrid.getCell((x // self.cellSize), y // self.cellSize)

        except IndexError:
            # print("Oops! Vous avez appuyé en dehors du plateau de jeu !")
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
            #else:
                #self.theEvent.set_coord2([xValueWithScrollBar, yValueWithScrollBar])
                #x, y = self.theEvent.get_coord2()
                #self.test2(x, y)


        except AttributeError:
            print("error")

    def setNumber(self, event):
        # print("set")
        try:
            x, y = self.theEvent.get_coord()
            self.updateCellValue(x, y, int(event.keysym))
            self.reDrawGrid()
            self.SelectedCell(x, y)

        except ValueError:
            pass
            # print("Erreur, il faut rentrer un chiffre.")

    def test(self, x, y):  # cliquer sur la case vide


        x, y = x // self.cellSize, y // self.cellSize

        cptx = 0  # compteur des cases suivantes horizontaux
        cpty = 0  # compteur des cases suivantes varticaux
        lst = []  # pour sauvgarder les chiffre initiaux

        for i in range(x, -1, -1):  # pour détecter les cases vides à droite
            if self.modelGrid.getCell(i, y).value == -1:
                if self.modelGrid.getCell(i, y).sumRight > 0:
                    lst.append(self.modelGrid.getCell(i, y).sumRight)
                    break
            else:
                cptx += 1

        for i in range(x + 1, self.modelGrid.width):  # pour détecter les cases vides à gauche
            if self.modelGrid.getCell(i, y).value == -1:
                break
            else:
                cptx += 1

        for i in range(y, -1, -1):  # pour détecter les cases vides en haut
            if self.modelGrid.getCell(x, i).value == -1:
                if self.modelGrid.getCell(x, i).sumDown is not None:
                    lst.append(self.modelGrid.getCell(x, i).sumDown)
                    break
            else:
                cpty += 1

        for i in range(y + 1, self.modelGrid.height):  # pour détecter les cases vides en bas
            if self.modelGrid.getCell(x, i).value == -1:
                break
            else:
                cpty += 1

        if self.helpCombination == True:
            self.varChiffre1.set(lst[0])
            self.varChiffre2.set(lst[1])
            self.varAddition1.set(creer_dictionnaire()[lst[0]][cptx])
            self.varAddition2.set(creer_dictionnaire()[lst[1]][cpty])

        else:
            self.varChiffre1.set("")
            self.varChiffre2.set("")
            self.varAddition1.set("")
            self.varAddition2.set("")


        # print(x, "|", y)

    def test2(self, x, y):  # cliquer sur la case avec un ou deux chiffres

        if self.helpCombination == True:

            x, y = x // self.cellSize, y // self.cellSize
            cptx = 0  # compteur des cases suivantes horizontales
            cpty = 0  # compteur des cases suivantes varticales
            lstr = []  # pour sauvgarder les chiffres initiaux
            lstd = []  # pour sauvgarder les chiffres initiaux

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

            if not lstr and not lstd:
                print("case invalide")
            elif not lstd:
                print(lstr[0], creer_dictionnaire()[lstr[0]][cptx])
                self.varChiffre1.set(lstr[0])
                self.varAddition1.set(creer_dictionnaire()[lstr[0]][cptx])
                self.varChiffre2.set(0)
                self.varAddition2.set(0)
            elif not lstr:
                print(lstd[0], creer_dictionnaire()[lstd[0]][cpty])
                self.varChiffre2.set(lstd[0])
                self.varAddition2.set(creer_dictionnaire()[lstd[0]][cpty])
                self.varChiffre1.set(0)
                self.varAddition1.set(0)
            else:
                print(lstd[0], creer_dictionnaire()[lstd[0]][cpty])
                print(lstr[0], creer_dictionnaire()[lstr[0]][cptx])
                self.varChiffre1.set(lstr[0])
                self.varAddition1.set(creer_dictionnaire()[lstr[0]][cptx])
                self.varChiffre2.set(lstd[0])
                self.varAddition2.set(creer_dictionnaire()[lstd[0]][cpty])

        else:
            self.varChiffre1.set("")
            self.varChiffre2.set("")
            self.varAddition1.set("")
            self.varAddition2.set("")

    def switchHeatMap(self):
        self.heatmap = not self.heatmap
        self.reDrawGrid()

    def getCellHeat(self, x, y):
        downLength = rightLength = 1
        rightNbFilledCells = downNbFilledCells = 0
        i = x-1
        while(self.modelGrid.getCell(i, y).value >= 0):
            rightLength += 1
            if(self.modelGrid.getCell(i, y).value != 0):
                rightNbFilledCells += 1
            i -= 1
        i = x+1
        while(i < self.modelGrid.width and self.modelGrid.getCell(i, y).value >= 0):
            rightLength += 1
            if(self.modelGrid.getCell(i, y).value != 0):
                rightNbFilledCells += 1
            i += 1
        i = y-1
        while(self.modelGrid.getCell(x, i).value >= 0):
            downLength += 1
            if(self.modelGrid.getCell(x, i).value != 0):
                downNbFilledCells += 1
            i -= 1
        i = y+1
        while(i < self.modelGrid.height and self.modelGrid.getCell(x, i).value >= 0):
            downLength += 1
            if(self.modelGrid.getCell(x, i).value != 0):
                downNbFilledCells += 1
            i += 1
        return min(rightLength-rightNbFilledCells, downLength-downNbFilledCells)

    def getSumDownCellFrom(self, x, y):
        i = y-1
        while(self.modelGrid.getCell(x, i).value >= 0):
            i -= 1
        return self.modelGrid.getCell(x, i)

    def getSumRightCellFrom(self, x, y):
        i = x-1
        while(self.modelGrid.getCell(i, y).value >= 0):
            i -= 1
        return self.modelGrid.getCell(i, y)
