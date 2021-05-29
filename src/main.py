import tkinter as tk

from viewcontroller.mainwindow import *
from events.event import Event

def saveCoordonate(event):
    try:
        app.grid.grid.getCellWithCoords(event.x, event.y)
        theEvent.set_coord([event.x, event.y])

    except AttributeError:
        pass

def setNumber(event):
    try:
        x, y = theEvent.get_coord()
        app.grid.grid.updateCellValue(x, y, int(event.keysym))
        app.reloadGrid()

    except ValueError:
        print("Erreur, il faut rentrer un chiffre.")


theEvent = Event()

root = tk.Tk()
app = MainWindow(master=root)

root.bind('<Button-1>', saveCoordonate)
root.bind('<KeyPress>', setNumber)
#root.winfo_pointerxy()

app.mainloop()

