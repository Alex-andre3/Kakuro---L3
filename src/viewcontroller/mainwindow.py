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
        if(self.grid != None):
            if(messagebox.askokcancel("Confirmation", "Delete your current game ? (\"ok\")", parent=self)):
                self.grid.destroy()
            else:
                return
        gridName = filedialog.askopenfilename(parent=self)
        if(gridName != None):
            print(gridName)
            self.grid = GridVC(self.gridLoader.loadGrid(gridName), self, confine=False) # creating the view of the returned grid
            self.grid.pack(side="bottom")

    # def loadGrid(self):
    #     pass
