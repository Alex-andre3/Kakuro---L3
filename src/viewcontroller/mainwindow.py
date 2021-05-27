import tkinter as tk
from tkinter import filedialog

from model.gridfactory import *

class MainWindow(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.gridLoader = GridFactory()
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.loadCustomGridButton = tk.Button(self, text="Load a custom grid",
                                        command=self.loadCustomGrid)
        self.loadCustomGridButton.pack(side="top")

        # self.loadGridButton = tk.Button(self, text="Load a grid",
        #                                 command=self.loadGrid)
        # self.loadGridButton.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red", 
                                        command=self.master.destroy)
        self.quit.pack(side="bottom")

    def loadCustomGrid(self):
        gridName = filedialog.askopenfilename(parent=self)
        if(gridName != None):
            print(gridName)
            self.grid = Grid(GridFactory.loadGrid(gridName), parent=self) # creating the view of the returned grid

    # def loadGrid(self):
    #     pass
