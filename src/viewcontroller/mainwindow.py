import tkinter
import tkinter as tk
from tkinter import filedialog, messagebox

from model.gridfactory import *
from viewcontroller.gridvc import *

class MainWindow(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.gridLoader = GridFactory()
        self.gridVC = None
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        buttons = tk.Frame(self)

        self.loadCustomGridButton = tk.Button(buttons, text="Load a custom grid",
                                        command=self.loadCustomGrid)
        self.loadCustomGridButton.pack(side="left")

        # self.loadGridButton = tk.Button(self, text="Load a grid",
        #                                 command=self.loadGrid)
        # self.loadGridButton.pack(side="top")

        self.quit = tk.Button(buttons, text="QUIT", fg="red", 
                                        command=self.master.destroy)
        self.quit.pack(side="right")

        buttons.pack(side="top")

        self.helpFrame = tk.Frame(self, bg="#b8b2a7", bd=5)
        self.helpFrame.pack(side="bottom")

        self.text = tk.Message(self.helpFrame, text="To Help you", width=200, bg="#b8b2a7").pack(side="top")

        self.state = tkinter.BooleanVar()
        self.CheckButton1 = tk.Checkbutton(self.helpFrame, variable=self.state, onvalue=True, offvalue=False, relief="ridge", text="Activate possible combinations", command=self.helpToCombinationPossibilities)
        self.CheckButton1.pack(side="left")

        self.state4 = tkinter.BooleanVar()
        self.CheckButton4 = tk.Checkbutton(self.helpFrame, variable=self.state4, onvalue=True, offvalue=False,
                                           relief="ridge", text="Activate possible values",
                                           command=self.helpToValuesPossibilities)
        self.CheckButton4.pack(side="left")

        self.state2 = tkinter.BooleanVar()
        self.CheckButton2 = tk.Checkbutton(self.helpFrame, variable=self.state2, onvalue=True, offvalue=False, relief="ridge", text="Activate Heatmap", command=self.HelpHeatmap)
        self.CheckButton2.pack(side="right")

        self.state3 = tkinter.BooleanVar()
        self.CheckButton3 = tk.Checkbutton(self.helpFrame, variable=self.state3, onvalue=True, offvalue=False,
                                           relief="ridge", text="Activate Memo", command=self.HelpMemo)
        self.CheckButton3.pack(side="right")

        self.helpResultFrame = tk.Frame(self, bd=2)
        #self.helpResultFrame.grid_propagate(0)
        self.helpResultFrame.pack(side="right")

        self.helpResultFrame1 = tk.Frame(self.helpResultFrame, bd=5)
        #self.helpResultFrame1.grid_propagate(0)
        self.helpResultFrame1.pack(side="top")

        self.helpResultFrame2 = tk.Frame(self.helpResultFrame, bd=5)
        #self.helpResultFrame2.grid_propagate(0)
        self.helpResultFrame2.pack(side="bottom")

        self.helpResultFrame3 = tk.Frame(self.helpResultFrame, bd=5)
        # self.helpResultFrame2.grid_propagate(0)
        self.helpResultFrame3.pack(side="bottom")



    def helpToCombinationPossibilities(self):
        if(self.gridVC != None):
            self.gridVC.helpCombination = self.state.get()

    def helpToValuesPossibilities(self):
        if(self.gridVC != None):
            self.gridVC.helpValue = self.state4.get()

    def HelpHeatmap(self):
        if(self.gridVC != None):
            self.gridVC.helpHeatmap = self.state2.get()
            self.gridVC.reDrawGrid()

    def HelpMemo(self):
        if(self.gridVC != None):
            self.gridVC.helpMemo = self.state3.get()
            self.gridVC.reDrawGrid()

    def clearHelpResultFrame1(self):
        for widget in self.helpResultFrame1.winfo_children():
            widget.destroy()
        for widget in self.helpResultFrame2.winfo_children():
            widget.destroy()

    def loadCustomGrid(self):
        if(self.gridVC != None):
            if(messagebox.askokcancel("Confirmation", "Delete your current game ? (\"ok\")", parent=self)):
                self.clearHelpResultFrame1()
                self.gridVC.destroy()
            else:
                return
        gridName = filedialog.askopenfilename(parent=self)
        if(gridName != None):
            print(gridName)
            self.gridVC = GridVC(self.gridLoader.loadGrid(gridName), self) # creating the view of the returned grid
            self.gridVC.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=tk.YES)

    def switchHeatMap(self):
        if(self.gridVC != None):
            self.gridVC.switchHeatMap()


    # def reloadGrid(self):

    #     self.gridVC.reDrawGrid()
    #     self.gridVC.pack(side="bottom")

    # def ColorSelectedCell(self, x, y):

    #     self.gridVC.SelectedCell(x, y)
    # def loadGrid(self):
    #     pass
