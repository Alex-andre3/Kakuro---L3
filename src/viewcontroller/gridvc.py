import time
import datetime
import tkinter as tk

from model.grid import *
from events.event import *
from solver.script_dictionary import creer_dictionnaire
from .timer import Timer


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
        self.helpValue = False
        self.helpHeatmap = False
        self.helpMemo = False
        self.helpResultFrame1 = parent.helpResultFrame1
        self.helpResultFrame2 = parent.helpResultFrame2
        self.currentSelectedCell = None
        self.drawGrid()

        self.scroll_x = tk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)
        self.scroll_x.pack(side="bottom", fill="x")

        self.canvas.pack(side="left")

        self.scroll_y = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scroll_y.pack(side="right", fill="y")

        self.canvas.configure(yscrollcommand=self.scroll_y.set, xscrollcommand=self.scroll_x.set)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        self.bind_keys()

        self.varChiffre1 = tk.StringVar()
        self.varChiffre2 = tk.StringVar()
        self.varAddition1 = tk.StringVar()
        self.varAddition2 = tk.StringVar()
        self.varPossible1 = tk.StringVar()
        self.varPossible2 = tk.StringVar()
        self.text_conseil_Chiffre1 = tk.Label(self.helpResultFrame1, textvariable=self.varChiffre1)
        self.text_conseil_Chiffre2 = tk.Label(self.helpResultFrame2, textvariable=self.varChiffre2)
        self.text_conseil_Addition1 = tk.Label(self.helpResultFrame1, textvariable=self.varAddition1)
        self.text_conseil_Addition2 = tk.Label(self.helpResultFrame2, textvariable=self.varAddition2)
        self.text_conseil_Possible1 = tk.Label(self.helpResultFrame1, textvariable=self.varPossible1)
        self.text_conseil_Possible2 = tk.Label(self.helpResultFrame2, textvariable=self.varPossible2)
        self.text_conseil_Chiffre1.pack(side="top")
        self.text_conseil_Chiffre2.pack(side="bottom")
        self.text_conseil_Addition1.pack(side="top")
        self.text_conseil_Addition2.pack(side="bottom")
        self.text_conseil_Possible1.pack(side="top")
        self.text_conseil_Possible2.pack(side="bottom")

        self.timer = Timer(self)
        self.gridName = parent.gridName

        # en attendant d'avoir fait la fonction qui vérifie si une partie à été remporté
        self.setGameToLog()

    def setGameToLog(self):
        date = datetime.datetime.today().strftime('%Y-%m-%d')
        heure = datetime.datetime.today().strftime('%H:%M:%S')
        log_file = open("logs/log.txt", "a")
        log_file.write("\nPartie jouée sur : {} en {} secondes le {} à {} ".format(self.splitGridName(self.gridName), self.timer.seconds, date, heure))
        log_file.close()

    def splitGridName(self, gridName):
        tab = gridName.split("/")
        return tab[-1]


    #Fonctions gérant l'affichage et l'interactivité de l'interface de jeu

    def bind_keys(self):
        self.canvas.bind('<Button-1>', lambda event: self.saveCoordonate(event))
        self._root().bind('<KeyPress>', lambda event: self.setNumber(event))

    def unbind_keys(self):
        self.canvas.unbind('<Button-1>')
        self._root().unbind('<KeyPress>') #dangerous, destroys every other binding

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

                if cell.value < 0:
                    if cell.sumDown <= 0 and cell.sumRight <= 0:
                        self.canvas.create_rectangle(x * self.cellSize, y * self.cellSize, (x + 1) * self.cellSize,
                                                     (y + 1) * self.cellSize, fill="black")
                    else:
                        if cell.sumDown > 0 and cell.sumRight > 0:
                            self.canvas.create_line(x * self.cellSize, y * self.cellSize, (x + 1) * self.cellSize,
                                                    (y + 1) * self.cellSize)
                        if cell.sumDown <= 0:
                            self.canvas.create_polygon([(x * self.cellSize, y * self.cellSize),
                                                        (x * self.cellSize, (y + 1) * self.cellSize),
                                                        ((x + 1) * self.cellSize, (y + 1) * self.cellSize)],
                                                       fill="black")
                        else:
                            quarter = self.cellSize / 4
                            self.canvas.create_text(x * self.cellSize + quarter, (y + 1) * self.cellSize - quarter,
                                                    text=cell.sumDown, tags=(x, y, "down"))
                        if cell.sumRight <= 0:
                            self.canvas.create_polygon([(x * self.cellSize, y * self.cellSize),
                                                        ((x + 1) * self.cellSize, y * self.cellSize),
                                                        ((x + 1) * self.cellSize, (y + 1) * self.cellSize)],
                                                       fill="black")
                        else:

                            quarter = self.cellSize / 4
                            self.canvas.create_text((x + 1) * self.cellSize - quarter, y * self.cellSize + quarter,
                                                    text=cell.sumRight, tags=(x, y, "right"))
                else:
                    if cell.value != 0:
                        if self.currentSelectedCell is cell:
                            self.canvas.create_rectangle(x * self.cellSize, y * self.cellSize, (x + 1) * self.cellSize,
                                                         (y + 1) * self.cellSize, fill="yellow")
                            self.currentSelectedCell = None

                        half = self.cellSize / 2
                        self.canvas.create_text(x * self.cellSize + half, y * self.cellSize + half,
                                                tags=(x, y), font=("", 18), text=cell.value, activefill="red")
                    else:
                        if self.helpHeatmap:
                            self.canvas.create_rectangle(x * self.cellSize, y * self.cellSize, (x + 1) * self.cellSize,
                                                    (y + 1) * self.cellSize, fill=heatColors[self.getCellHeat(x, y)-1])

                        if self.currentSelectedCell is cell:
                            self.canvas.create_rectangle(x * self.cellSize, y * self.cellSize, (x + 1) * self.cellSize,
                                                         (y + 1) * self.cellSize, fill="yellow")
                            self.currentSelectedCell = None

                        if self.helpMemo:
                            third = self.cellSize / 3
                            number = 1
                            for booleanValue in cell.memoList:
                                if booleanValue:
                                    self.canvas.create_text(x * self.cellSize + third * ((number-1) % 3 + 0.5),
                                                            y * self.cellSize + third * ((number-1) // 3 + 0.5),
                                                            text=number, fill="gray")
                                number += 1

    def reDrawGrid(self):
        # pour eviter d'interposer les chiffres, on nettoie le canvas et le redessine
        self.canvas.delete("all")
        self.drawGrid()

    def SelectedCell(self, xMouse, yMouse):
        x, y = xMouse // self.cellSize, yMouse // self.cellSize
        cell = self.modelGrid.getCell(x, y)
        self.currentSelectedCell = cell

    def getCellWithCoords(self, x, y):
        try:
            # print("Valeur value: ", self.modelGrid.getCell((x // self.cellSize), y // self.cellSize).value)
            # print("Valeur sumDown: ", self.modelGrid.getCell((x // self.cellSize), y // self.cellSize).sumDown)
            # print("Valeur sumRight: ", self.modelGrid.getCell((x // self.cellSize), y // self.cellSize).sumRight)
            self.algoHelperCominaison2(x, y)
            return self.modelGrid.getCell((x // self.cellSize), y // self.cellSize)

        except IndexError:
            # print("Oops! Vous avez appuyé en dehors du plateau de jeu !")
            return None

    def updateCellValue(self, x, y, value):
        cell = self.modelGrid.getCell((x // self.cellSize), y // self.cellSize)
        if self.helpMemo:
            cell.updateMemoList(value)
        else:
            cell.setValue(value)

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
            if self.getCellWithCoords(xValueWithScrollBar, yValueWithScrollBar).value is not None \
                    and self.getCellWithCoords(xValueWithScrollBar, yValueWithScrollBar).value != -1:
                self.theEvent.set_coord([xValueWithScrollBar, yValueWithScrollBar])
                x, y = self.theEvent.get_coord()
                self.SelectedCell(x, y)
                self.reDrawGrid()
                self.algoHelperCominaison(x, y)

        except AttributeError:
            print("error")

    def setNumber(self, event):
        # print("set")
        try:
            x, y = self.theEvent.get_coord()
            self.updateCellValue(x, y, int(event.keysym))
            self.SelectedCell(x, y)
            self.reDrawGrid()

        except ValueError:
            pass
            # print("Erreur, il faut rentrer un chiffre.")

    #Fonctions gérant l'aide à la résolution grâce aux combinaisons possibles de chaque cases

    def formattingResultsHelpCombination(self, liste):
        chn = ""
        for x in liste:
            for i in x:
                chn += str(i) + " "
            chn += "\n"
        chn += "\n"
        return chn

    def algoHelperCominaison(self, x, y):  # cliquer sur la case vide
        x, y = x // self.cellSize, y // self.cellSize

        cptx = 0  # compteur des cases suivantes horizontales
        cpty = 0  # compteur des cases suivantes varticales
        lst = []  # pour sauvgarder les chiffres initiaux
        sommeh = 0  # pour sauvgarder la somme des chiffres des cases dans la même ligne
        cptsh = 0  # pour sauvgarder le nombre des cases déjà remplies dans la même ligne
        sommev = 0  # pour sauvgarder la somme des chiffres des cases dans la même colonne
        cptsv = 0  # pour sauvgarder le nombre des cases déjà remplies dans la même colonne
        registeredx = []  # pour sauvgarder le chiffre déjà saisi dans la case blanche
        registeredy = []  # pour sauvgarder le chiffre déjà saisi dans la case blanche
        listex = []
        listey = []
        listefinale1 = []
        listefinale2 = []

        for i in range(x, -1, -1):  # pour détecter les cases vides à gauche
            if self.modelGrid.getCell(i, y).value == -1:
                if self.modelGrid.getCell(i, y).sumRight > 0:
                    lst.append(self.modelGrid.getCell(i, y).sumRight)
                    break
            else:
                cptx += 1
                if self.modelGrid.getCell(i, y).value > 0:
                    sommeh = sommeh + self.modelGrid.getCell(i, y).value
                    registeredx.append(self.modelGrid.getCell(i, y).value)
                    cptsh = cptsh + 1

        for i in range(x + 1, self.modelGrid.width):  # pour détecter les cases vides à droite
            if self.modelGrid.getCell(i, y).value == -1:
                break
            else:
                cptx += 1
                if self.modelGrid.getCell(i, y).value > 0:
                    sommeh = sommeh + self.modelGrid.getCell(i, y).value
                    registeredx.append(self.modelGrid.getCell(i, y).value)
                    cptsh = cptsh + 1

        for i in range(y, -1, -1):  # pour détecter les cases vides en haut
            if self.modelGrid.getCell(x, i).value == -1:
                if self.modelGrid.getCell(x, i).sumDown is not None:
                    lst.append(self.modelGrid.getCell(x, i).sumDown)
                    break
            else:
                cpty += 1
                if self.modelGrid.getCell(x, i).value > 0:
                    sommev = sommev + self.modelGrid.getCell(x, i).value
                    registeredy.append(self.modelGrid.getCell(x, i).value)
                    cptsv = cptsv + 1

        for i in range(y + 1, self.modelGrid.height):  # pour détecter les cases vides en bas
            if self.modelGrid.getCell(x, i).value == -1:
                break
            else:
                cpty += 1
                if self.modelGrid.getCell(x, i).value > 0:
                    sommev = sommev + self.modelGrid.getCell(x, i).value
                    registeredy.append(self.modelGrid.getCell(x, i).value)
                    cptsv = cptsv + 1



        if self.helpCombination == True:
            self.varChiffre1.set("Possibilities for : {}".format(lst[0]))
            self.varChiffre2.set("Possibilities for : {}".format(lst[1]))
            self.varAddition1.set(self.formattingResultsHelpCombination(creer_dictionnaire()[lst[0]][cptx]))
            self.varAddition2.set(self.formattingResultsHelpCombination(creer_dictionnaire()[lst[1]][cpty]))


        else:
            self.varChiffre1.set("")
            self.varChiffre2.set("")
            self.varAddition1.set("")
            self.varAddition2.set("")


        if self.helpValue == True:
            if lst[0] - sommeh != 0 and lst[1] - sommev != 0 and self.modelGrid.getCell(x, y).value == 0:
                try:
                    if not registeredx:
                        print("horizontal")
                        print(creer_dictionnaire()[lst[0] - sommeh][cptx - cptsh])
                        self.varPossible1.set("Possible values for this empty cell in this line : {} {}"
                                              .format("\n", self.formattingResultsHelpCombination(
                            creer_dictionnaire()[lst[0] - sommeh][cptx - cptsh])))

                    else:

                        listetest=creer_dictionnaire()[lst[0] - sommeh][cptx - cptsh]
                        listetesttest = creer_dictionnaire()[lst[0] - sommeh][cptx - cptsh]
                        print("-----")
                        print(registeredx)
                        print(listetesttest)
                        print("-----")
                        for i in range(0, len(registeredx)):
                            for j in range(0, len(listetest)):
                                if registeredx[i] in listetest[j]:
                                    listex.append(listetest[j])

                        print("-----")
                        print(listetest)
                        print(listex)
                        print("-----")

                        for x in range(0, len(listetest)):
                            if listetest[x] not in listex:
                                listefinale1.append(listetest[x])


                        self.varPossible1.set("Possible values for this empty cell in this line : {} {}"
                                              .format("\n", self.formattingResultsHelpCombination(listefinale1)))

                except Exception as e:
                    print('str(e):\t\t', str(e))
                    print("il y a des erreurs dans cette ligne")
                    self.varPossible1.set("il y a des erreurs dans cette ligne")
                try:
                    if not registeredy:
                        print("vertical")
                        print(creer_dictionnaire()[lst[1] - sommev][cpty - cptsv])
                        self.varPossible2.set("Possible values for this empty cell in this column : {} {}"
                                              .format("\n", self.formattingResultsHelpCombination(
                            creer_dictionnaire()[lst[1] - sommev][cpty - cptsv])))
                    else:
                        listetest2 = creer_dictionnaire()[lst[1] - sommev][cpty - cptsv]
                        listetesttest2 = creer_dictionnaire()[lst[1] - sommev][cpty - cptsv]
                        print("-----")
                        print(registeredy)
                        print(listetesttest2)
                        print("-----")
                        for i in range(0, len(registeredy)):
                            for j in range(0, len(listetest2)):
                                if registeredy[i] in listetest2[j]:
                                    listey.append(listetest2[j])

                        for x in range(0, len(listetest2)):
                            if listetest2[x] not in listey:
                                listefinale2.append(listetest2[x])


                        self.varPossible2.set("Possible values for this empty cell in this column : {} {}"
                                              .format("\n", self.formattingResultsHelpCombination(listefinale2)))



                except Exception as e:
                    print('str(e):\t\t', str(e))
                    print("il y a des erreurs dans cette colonne")
                    self.varPossible2.set("il y a des erreurs dans cette colonne")
        else:
            self.varPossible1.set("")
            self.varPossible2.set("")



    def algoHelperCominaison2(self, x, y):  # cliquer sur la case avec un ou deux chiffres

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
                self.varChiffre1.set("Possibilities for : {}".format(lstr[0]))
                self.varAddition1.set(self.formattingResultsHelpCombination(creer_dictionnaire()[lstr[0]][cptx]))
                self.varChiffre2.set(0)
                self.varAddition2.set(0)

            elif not lstr:
                self.varChiffre2.set("Possibilities for : {}".format(lstd[0]))
                self.varAddition2.set(self.formattingResultsHelpCombination(creer_dictionnaire()[lstd[0]][cpty]))
                self.varChiffre1.set(0)
                self.varAddition1.set(0)
            else:
                self.varChiffre1.set("Possibilities for : {}".format(lstr[0]))
                self.varAddition1.set(self.formattingResultsHelpCombination(creer_dictionnaire()[lstr[0]][cptx]))
                self.varChiffre2.set("Possibilities for : {}".format(lstd[0]))
                self.varAddition2.set(self.formattingResultsHelpCombination(creer_dictionnaire()[lstd[0]][cpty]))

        else:
            self.varChiffre1.set("")
            self.varChiffre2.set("")
            self.varAddition1.set("")
            self.varAddition2.set("")





    #Fonctions gérant l'aide à la résolution grâce à la heatmap

    def switchHeatMap(self):
        self.helpHeatmap = not self.helpHeatmap
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
