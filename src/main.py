from model.gridfactory import GridFactory

gridmaker = GridFactory()
grid = gridmaker.loadGrid("templates/test1")
grid.displayGrid()
