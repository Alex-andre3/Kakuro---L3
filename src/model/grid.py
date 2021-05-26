import model.cell

class Grid:
    def __init__(self, grid=[]):
        self.width = len(grid)
        self.length = (len(grid[0]) if (grid != []) else 0)
        self.grid = grid

    def checkCell(self, x, y):
        invertY = len(self.grid) - y - 1
        cell = self.grid[invertY][x]
        if(cell.value < 0):
            return (checkDownSum(x, y) and checkRightSum(x, y))
        else:
            return (cell.value != 0)

    def checkDownSum(self, x, y):
        invertY = len(self.grid) - y - 1
        cell = self.grid[invertY][x]
        if(cell.value < 0):
            sumDown = 0
            numbersDown = []
            i = invertY+1
            while(i < len(self.grid) and self.grid[i][x].value >= 0 and
                not (self.grid[i][x].value in numbersDown)):
                if(self.grid[i][x].value == 0):
                    return False
                else:
                    sumDown += self.grid[i][x].value
                    numbersDown.append(self.grid[i][x].value)
                    i += 1
            return (sumDown == cell.sumDown)

    def checkRightSum(self, x, y):
        invertY = len(self.grid) - y - 1
        cell = self.grid[invertY][x]
        if(cell.value < 0):
            sumRight = 0
            numbersRight = []
            i = x+1
            while(i < len(self.grid[invertY]) and self.grid[invertY][i].value >= 0 and
                not (self.grid[invertY][i].value in numbersRight)):
                if(self.grid[invertY][i].value == 0):
                    return False
                else:
                    sumRight += self.grid[invertY][i].value
                    numbersRight.append(self.grid[invertY][i].value)
                    i += 1
            return (sumRight == cell.sumRight)

    def verifyGrid(self):
        for y in range(len(self.grid)):
            print('\n', y)
            for x in range(len(self.grid[0])):
                print(x, end=' ')
                if(not self.checkCell(x, y)):
                    return False
        return True

    def displayGrid(self):
        for line in self.grid:
            for cell in line:
                print(cell.value, end=" ")
            print("")



