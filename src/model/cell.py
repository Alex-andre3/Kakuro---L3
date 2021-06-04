class Cell:

    # value < 0 means the cell is black
    # value = 0 means the cell is empty and must be filled
    # if value > 0, sumDown and sumRight will be ignored
    def __init__(self, value, sumDown=0, sumRight=0):
        self.value = value
        self.sumDown = sumDown
        self.sumRight = sumRight
        self.memoList = [False] * 9 # 9 values for 9 numbers

    def setValue(self, value):
        if(self.value >= 0):
            if(value >= 0):
                self.value = value

    def updateMemoList(self, value):
        if self.value == 0:
            self.memoList[value-1] = not self.memoList[value-1]