import random

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
        if cell.value > 0:
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
        else:
            return True

    def checkRightSum(self, x, y):
        cell = self.getCell(x, y)
        if cell.value > 0:
            sumRight = 0
            numbersRight = []
            i = x+1
            while(i < self.width and self.getCell(i, y).value >= 0 and
                not (self.getCell(i, y).value in numbersRight)):
                if(self.getCell(i, y).value == 0):
                    return False
                else:
                    sumRight += self.getCell(i, y).value
                    numbersRight.append(self.getCell(i, y).value)
                    i += 1
            return sumRight == cell.sumRight
        else:
            return True

    def verifyGrid(self):
        for y in range(self.height):
            print('\n', y)
            for x in range(self.width):
                print(x, end=' ')
                if(not self.checkCell(x, y)):
                    return False
        return True

    def getCell(self, x, y):
        return self.grid[y][x]

    def addOneValueFromSolution(self, grid_solution):
        if grid_solution is None:
            return None
        if self.height != grid_solution.height or self.width != grid_solution.width:
            return None
        list_cells_to_change = []
        for x in range(self.width):
            for y in range(self.height):
                cell1 = self.getCell(x, y)
                cell2 = grid_solution.getCell(x, y)
                if cell2.value > 0:
                    if cell1.value > 0:
                        if cell1.value != cell2.value:
                            cell1.setValue(cell2.value)
                            return False
                    elif cell1.value == 0:
                        list_cells_to_change.append([cell1, cell2])
        if list_cells_to_change:
            one_pair = random.choice(list_cells_to_change)
            one_pair[0].setValue(one_pair[1].value)
        return True

    # --- debugging ---
    # def displayGrid(self):
    #     for line in self.grid:
    #         for cell in line:
    #             print(cell.value, end=" ")
    #         print("")

