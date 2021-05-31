import model.cell

class Grid:
    def __init__(self, grid=[]):
        self.height = len(grid)
        self.width = (len(grid[0]) if (grid != []) else 0)
        self.grid = grid

    def checkCell(self, x, y):
        cell = self.getCell(x, y)
        if cell.value < 0 :
            return (self.checkDownSum(x, y) and self.checkRightSum(x, y))
        else:
            return cell.value != 0

    def checkDownSum(self, x, y):
        cell = self.getCell(x, y)
        if cell.value < 0:
            sumDown = 0
            numbersDown = []
            i = y+1
            while(i < self.height and self.getCell(x, i).value >= 0 and
                not (self.getCell(x, i).value in numbersDown)):
                if(self.getCell(x, i).value == 0):
                    return False
                else:
                    sumDown += self.getCell(x, i).value
                    numbersDown.append(self.getCell(x, i).value)
                    i += 1
            return sumDown == cell.sumDown

    def checkRightSum(self, x, y):
        cell = self.getCell(x, y)
        if cell.value < 0:
            sumRight = 0
            numbersRight = []
            i = x+1
            while(i < self.width and self.getCell(i, invertY).value >= 0 and
                not (self.getCell(i, invertY).value in numbersRight)):
                if(self.getCell(i, invertY).value == 0):
                    return False
                else:
                    sumRight += self.getCell(i, invertY).value
                    numbersRight.append(self.getCell(i, invertY).value)
                    i += 1
            return sumRight == cell.sumRight

    def verifyGrid(self):
        for y in range(self.height):
            print('\n', y)
            for x in range(self.width):
                print(x, end=' ')
                if(not self.checkCell(x, y)):
                    return False
        return True

    def displayGrid(self):
        for line in self.grid:
            for cell in line:
                print(cell.value, end=" ")
            print("")

    def getCell(self, x, y):
        return self.grid[y][x]

    def getCellWithCoords(self, x, y):
        try:
            print("Valeur de la case: ", self.getCell((x//30), y//30).value)
            return self.getCell((x//30), y//30)

        except IndexError:
            print("Oops! Vous avez appuyé en dehors du plateau de jeu !")

    def updateCellValue(self, x, y, value):
        self.getCell((x//30), y//30).setValue(value)

