import tkinter
import os
from tkinter import filedialog, messagebox

from model.gridfactory import *
from viewcontroller.gridvc import *


class MainWindow(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.gridLoader = GridFactory()
        self.gridSolution = None
        self.gridVC = None
        self.gridName = None
        self.winState = False
        self.textWin = tk.StringVar()
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        buttons = tk.Frame(self)

        self.loadCustomGridButton = tk.Button(buttons, text="Load a custom grid", command=self.loadCustomGrid)
        self.loadCustomGridButton.pack(side="left")

        self.quit = tk.Button(buttons, text="QUIT", fg="red", command=self.master.destroy)
        self.quit.pack(side="right")

        buttons.pack(side="top")

        # Boutons en haut

        gameOption = tk.Frame(self)

        self.helpHint = tk.Button(gameOption, text="Get a hint", command=self.helpHint)
        self.helpHint.pack(side="left")

        self.checkGrid = tk.Button(gameOption, text="Check grid", fg="green",
                                   command=self.checkGrid)
        self.checkGrid.pack(side="right")

        gameOption.pack(side="top")

        # Boutons en bas : aide à la résolution

        helpFrame = tk.Frame(self, bg="#b8b2a7", bd=5)

        HelpFrameLeft = tk.Frame(helpFrame, bg="#b8b2a7")
        HelpFrameRight = tk.Frame(helpFrame, bg="#b8b2a7")

        self.text = tk.Message(helpFrame, text="To Help you", width=300, bg="#b8b2a7").pack(side="top")

        self.state = tkinter.BooleanVar()
        self.CheckButton1 = tk.Checkbutton(HelpFrameLeft, variable=self.state, onvalue=True, offvalue=False,
                                           relief="ridge", text="Activate possible combinations",
                                           command=self.helpToCombinationPossibilities)
        self.CheckButton1.pack(side="top")

        self.state2 = tkinter.BooleanVar()
        self.CheckButton2 = tk.Checkbutton(HelpFrameLeft, variable=self.state2, onvalue=True, offvalue=False,
                                           relief="ridge", text="Activate Heatmap", command=self.HelpHeatmap)
        self.CheckButton2.pack(side="bottom")

        self.state3 = tkinter.BooleanVar()
        self.CheckButton3 = tk.Checkbutton(HelpFrameRight, variable=self.state3, onvalue=True, offvalue=False,
                                           relief="ridge", text="Activate Memo", command=self.HelpMemo)
        self.CheckButton3.pack(side="bottom")

        self.state4 = tkinter.BooleanVar()
        self.CheckButton4 = tk.Checkbutton(HelpFrameRight, variable=self.state4, onvalue=True, offvalue=False,
                                           relief="ridge", text="Activate possible values",
                                           command=self.helpToValuesPossibilities)
        self.CheckButton4.pack(side="top")

        HelpFrameLeft.pack(side="left")
        HelpFrameRight.pack(side="right")
        helpFrame.pack(side="bottom")

        # est utile pour GridVC

        self.helpResultFrame = tk.Frame(self, bd=2)
        self.helpResultFrame.pack(side="right")

        self.helpResultFrame1 = tk.Frame(self.helpResultFrame, bd=5)
        self.helpResultFrame1.pack(side="top")

        self.helpResultFrame2 = tk.Frame(self.helpResultFrame, bd=5)
        self.helpResultFrame2.pack(side="bottom")

        self.helpResultFrame3 = tk.Frame(self.helpResultFrame, bd=5)
        self.helpResultFrame3.pack(side="bottom")

        # bouton pour le message de victoire
        self.labelWin = tk.Label(self, textvariable=self.textWin, font="Arial 10", fg="green", width=10)
        self.labelWin.pack()

    #  Fonctions liées aux boutons

    def helpToCombinationPossibilities(self):
        if self.gridVC is not None and self.winState is False:
            self.gridVC.helpCombination = self.state.get()

    def helpToValuesPossibilities(self):
        if self.gridVC is not None and self.winState is False:
            self.gridVC.helpValue = self.state4.get()

    def HelpHeatmap(self):
        if self.gridVC is not None and self.winState is False:
            self.gridVC.helpHeatmap = self.state2.get()
            self.gridVC.reDrawGrid()

    def switchHeatMap(self):
        if self.gridVC is not None:
            self.gridVC.switchHeatMap()

    def HelpMemo(self):
        if self.gridVC is not None and self.winState is False:
            self.gridVC.helpMemo = self.state3.get()
            self.gridVC.reDrawGrid()

    def helpHint(self):
        if self.gridVC is not None and self.winState is False:
            if self.gridSolution is not None:
                grid = self.gridVC.modelGrid
                result = grid.addOneValueFromSolution(self.gridSolution)
                if result is None:
                    print("Pas de fichier de solution présent.")
                self.gridVC.reDrawGrid()
            else:
                print("Pas de fichier de solution présent.")

    def checkGrid(self):
        if self.gridVC is not None and self.winState is False:
            if self.gridVC.modelGrid.verifyGrid():
                self.gridVC.setGameToLog(self.gridName)
                self.gridVC.winState = True
                self.winState = True
                self.textWin.set("You won!")

    def clearHelpResultFrame1(self):
        for widget in self.helpResultFrame1.winfo_children():
            widget.destroy()
        for widget in self.helpResultFrame2.winfo_children():
            widget.destroy()

    def loadCustomGrid(self):
        if (self.gridVC != None):
            if (messagebox.askokcancel("Confirmation", "Delete your current game ? (\"ok\")", parent=self)):
                self.clearHelpResultFrame1()
                self.gridVC.destroy()
            else:
                return
        gridName = filedialog.askopenfilename(parent=self)
        if (gridName != None):
            print("gridname =", gridName)
            self.gridName = gridName
            self.gridVC = GridVC(self.gridLoader.loadGrid(self.gridName),
                                 self)  # creating the view of the returned grid
            self.gridVC.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=tk.YES)
            sName = gridName.replace("grids", "solutions")
            if os.path.exists(sName):
                self.gridSolution = GridFactory().loadGrid(sName)
            self.winState = False
            self.textWin.set("")
