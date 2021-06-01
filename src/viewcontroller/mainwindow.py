import tkinter
import tkinter as tk
from tkinter import filedialog, messagebox

from model.gridfactory import *
from viewcontroller.gridvc import *

class MainWindow(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.gridLoader = GridFactory()
        self.grid = None
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


        # checkValue = tkinter.BooleanVar()
        # self.CheckButton1 = tk.Checkbutton(self, variable=checkValue, text="Activate possible combinations", command=self.isChecked(checkValue))
        # self.CheckButton1.pack(side="right")

        # self.CheckButton2 = tk.Checkbutton(self, text="Activate Heatmap")
        # self.CheckButton2.pack(side="right")

    def loadCustomGrid(self):
        if(self.grid != None):
            if(messagebox.askokcancel("Confirmation", "Delete your current game ? (\"ok\")", parent=self)):
                self.grid.destroy()
            else:
                return
        gridName = filedialog.askopenfilename(parent=self)
        if(gridName != None):
            print(gridName)
            self.grid = GridVC(self.gridLoader.loadGrid(gridName), self) # creating the view of the returned grid
            self.grid.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=tk.YES)


    # def reloadGrid(self):

    #     self.grid.reDrawGrid()
    #     self.grid.pack(side="bottom")

    # def ColorSelectedCell(self, x, y):

    #     self.grid.SelectedCell(x, y)
    # def loadGrid(self):
    #     pass
