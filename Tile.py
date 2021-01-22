#color, row, col, occupiedBy 
class Tile:
    color = None
    occupiedBy = None
    darkCols = {'a','c','e','g'}
    def __init__(self,column,row):
        self.col = column
        self.row = row #int
        self.setColor()
        self.setTerritory()

    def setColor(self):
        if self.col in self.darkCols:
            if self.row % 2 != 0:
                self.color = "dark"
            else:
                self.color = "white"
        else:
            if self.row % 2 == 0:
                self.color = "dark"
            else:
                self.color = "white"

    def setPiece(self, piece):
        self.occupiedBy = piece
    
    def getPiece(self):
        return self.occupiedBy

    def isOccupied(self):
        return self.occupiedBy != None

    def setTerritory(self):
        if self.row <=4:
            self.territory= "white"
        else:
            self.territory= "black"
    def getTerritory(self):
        return self.territory
    def getCoordinates(self):
        x = self.getColNumber()
        y = self.getRow()
       
        return tuple([x,y])
    def getName(self):
        return self.col+str(self.row)
    def getRow(self): #getX
        return self.row
    def getCol(self): 
        return self.col
    def getColNumber(self):#getY
        colConvert={
            'a':1,
            'b':2,
            'c':3,
            'd':4,
            'e':5,
            'f':6,
            'g':7,
            'h':8 
        }
        return colConvert[self.getCol()]

    def isStraightClearPath(self,tile,board):
        colDifference = abs(self.getColNumber() - tile.getColNumber())
        rowDifference = abs(self.getRow() - tile.getRow())

        if colDifference == 0: #same row / different col
            col = self.getColNumber()
            if self.getRow() < tile.getRow():
                bottomTile = self
                topTile = tile
            else:
                bottomTile = tile
                topTile = self
            for row in range(bottomTile.getRow()+1, topTile.getRow()):
                currentTile = board.board[col][row]
                #print(currentTile)
                if currentTile.isOccupied():
                    return False
            return True
        elif rowDifference == 0: #same col different row
            row= self.getRow()
            if self.getColNumber() < tile.getColNumber():
                leftTile = self
                rightTile = tile
            else:
                leftTile = tile
                rightTile = self
            for col in range(leftTile.getColNumber()+1, rightTile.getColNumber()):
                currentTile = board.board[col][row]
                if currentTile.isOccupied():
                    return False
            return True
        elif colDifference == 0 and rowDifference == 0:
            print("error, same tile")
            return None
        else:
            print("illegal input", "colDifference= ", colDifference, "rowDifference = ", rowDifference)
            return None

    def isDiagonalClearPath(self,tile,board):
        x1 = self.getRow()
        y1 = self.getColNumber()
        x2 = tile.getRow()
        y2 = tile.getColNumber()
        if abs(x1-x2) == abs(y1-y2): #check to be diagonal
            while x1 != x2 and y1 != y2:
                if x1 < x2:
                    x1+=1
                else:
                    x1-=1
                if y1 < y2:
                    y1+=1
                else:
                    y1-=1

                currentTile = board.board[y1][x1]
                #print(currentTile)
                if currentTile == tile:
                    return True
                if currentTile.isOccupied():
                    return False
            return True
        else:
            #print("not a diagonal")
            return False
        

    def __str__(self):
        return self.col + str(self.row) + "|:" + str(self.occupiedBy) + "|"
        #e4 |occupied by:piece

    


