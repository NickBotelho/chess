class Piece: #TODO: add move tracker
    name = None
    currentTile = None
    team = None
    numberOfMoves = 0
    def __init__(self, tile,name,team):
        self.name = name
        self.currentTile = tile
        self.team = team
    def setTile(self,tile):
        self.currentTile = tile
    def getTile(self):
        return self.currentTile
    def getTeam(self):
        return self.team
    def getRow(self):
        return self.getTile().getRow()
    def getCol(self):#letter
        return self.getTile().getCol()
    def getColNumber(self):#number
        return self.getTile().getColNumber()
    def __str__(self):
        teams={
            "white":"w",
            "black":"b"
        }
        return "("+teams[self.team] + ") " + self.name 
        #+ " is on " + str(self.currentTile)
    
    

class Pawn(Piece):
    movement = "plus one"
    name = "Pawn"
    def __init__(self,tile,team):
        super().__init__(tile,self.name,team)
    def getPossibleMoves(self,board):
        possibleMoves = set()
        if self.numberOfMoves==0:
            if self.getTeam() =="white":
                y = self.getTile().getRow() + 2
            else:
                y = self.getTile().getRow() - 2
            possibleMoves.add(board.board[self.getTile().getColNumber()][y])
        if self.getTeam() == "white":
            if self.getTile().getRow() < 8:
                front = board.board[self.getTile().getColNumber()][self.getTile().getRow()+1]
                if front.getPiece() == None:
                    possibleMoves.add(front)
                if self.getTile().getColNumber() > 1:
                    leftDiagonal = board.board[self.getTile().getColNumber()-1][self.getTile().getRow()+1]
                    if leftDiagonal.getPiece() != None and leftDiagonal.getPiece().getTeam()!= self.getTeam():
                        possibleMoves.add(leftDiagonal)
                if self.getTile().getColNumber() < 8:
                    rightDiagonal = board.board[self.getTile().getColNumber()+1][self.getTile().getRow()+1]
                    if rightDiagonal.getPiece() != None and rightDiagonal.getPiece().getTeam() != self.getTeam():
                        possibleMoves.add(rightDiagonal)
        else:
            if self.getTile().getRow() > 1:
                front = board.board[self.getTile().getColNumber()][self.getTile().getRow()-1]
                if front.getPiece() == None:
                    possibleMoves.add(front)
                if self.getTile().getColNumber() > 1:
                    leftDiagonal = board.board[self.getTile().getColNumber()-1][self.getTile().getRow()-1]
                    if leftDiagonal.getPiece() != None and leftDiagonal.getPiece().getTeam()!= self.getTeam():
                        possibleMoves.add(leftDiagonal)
                if self.getTile().getColNumber() < 8:
                    rightDiagonal = board.board[self.getTile().getColNumber()+1][self.getTile().getRow()-1]
                    if rightDiagonal.getPiece() != None and rightDiagonal.getPiece().getTeam() != self.getTeam():
                        possibleMoves.add(rightDiagonal)
        #TODO:add antpisants LMAO
        return possibleMoves
    def move(self,tile,board): #TODO:, add the first move 2 tile
        start = self.getTile()
        end = tile
        validMove = True
        if self.team == "white":
            if start.getRow() - end.getRow() == -1 and end.isOccupied() == False and start.getCol() == end.getCol(): #valid single move no take
                end.setPiece(self)
                self.setTile(tile)
                start.setPiece(None)
            elif start.getRow() - end.getRow() == -1 and end.isOccupied() == True and abs(start.getColNumber() - end.getColNumber()) == 1: #diagonal attack
                end.setPiece(self)
                self.setTile(tile)
                start.setPiece(None)
                #trash enemey piece right not its in lingo
            elif start.getRow() - end.getRow() == -2 and end.isOccupied() == False and start.getCol() == end.getCol() and self.numberOfMoves == 0: #first move 2 spaces
                end.setPiece(self)
                self.setTile(tile)
                start.setPiece(None)
                self.numberOfMoves+=1

            else:
                print("illgal move")
                validMove = False
        else:
            if start.getRow() - end.getRow() == 1 and end.isOccupied() == False and start.getCol() == end.getCol(): #valid single move
                end.setPiece(self)
                self.setTile(tile)
                start.setPiece(None)
            elif start.getRow() - end.getRow() == 1 and end.isOccupied() == True and abs(start.getColNumber() - end.getColNumber()) == 1: #diagonalAttack
                end.setPiece(self)
                self.setTile(tile)
                start.setPiece(None)
                #trash enemey piece right not its in lingo
            elif start.getRow() - end.getRow() == 2 and end.isOccupied() == False and start.getCol() == end.getCol() and self.numberOfMoves == 0: #first move 2 spaces
                end.setPiece(self)
                self.setTile(tile)
                start.setPiece(None)
                self.numberOfMoves+=1

            else:
                print("illgal move")
                validMove = False
        #promotion
        if (self.getTeam() == "white" and self.getTile().getRow() == 8) or (self.getTeam() == "black" and self.getTile().getRow() == 1) and validMove:
            tile = self.getTile()
            print("promotion available, select 'queen', 'rook', 'bishop', or 'knight'")
            promotion = input()
            if promotion == "queen":     
                tile.setPiece(Queen(tile,self.getTeam()))
            elif promotion == "rook":
                tile.setPiece(Rook(tile, self.getTeam()))
            elif promotion == "bishop":
                tile.setPiece(Bishop( tile, self.getTeam()))
            elif promotion == "knight":
                tile.setPiece(Knight(tile, self.getTeam()))

        return validMove


class Rook(Piece):
    movement = "plus one"
    name = "Rook"
    def __init__(self,tile,team):
        super().__init__(tile,self.name,team)
    def getPossibleMoves(self,board):
        currentTile = self.getTile()
        x = currentTile.getColNumber()
        y = currentTile.getRow()
        possibleMoves = set()
        while x > 0 and x < 8 and currentTile.isStraightClearPath(board.board[x+1][y],board):
            if board.board[x+1][y].getPiece()!= None:
                if board.board[x+1][y].getPiece().getTeam() != self.getTeam():
                    possibleMoves.add(board.board[x+1][y])
            else:
                possibleMoves.add(board.board[x+1][y])
            x+=1
        x = currentTile.getColNumber()
        while x > 1 and x < 9 and currentTile.isStraightClearPath(board.board[x-1][y],board):
            if board.board[x-1][y].getPiece()!= None:
                if board.board[x-1][y].getPiece().getTeam() != self.getTeam():
                    possibleMoves.add(board.board[x-1][y])
            else:
                possibleMoves.add(board.board[x-1][y])
            x-=1
        x = currentTile.getColNumber()
        while y > 0 and y < 8 and currentTile.isStraightClearPath(board.board[x][y+1],board):
            if board.board[x][y+1].getPiece()!= None:
                if board.board[x][y+1].getPiece().getTeam() != self.getTeam():
                    possibleMoves.add(board.board[x][y+1])
            else:
                possibleMoves.add(board.board[x][y+1])
            y+=1
        y = currentTile.getRow()
        while y > 1 and y < 9 and currentTile.isStraightClearPath(board.board[x][y-1],board):
            if board.board[x][y-1].getPiece()!= None:
                if board.board[x][y-1].getPiece().getTeam() != self.getTeam():
                    possibleMoves.add(board.board[x][y-1])
            else:
                possibleMoves.add(board.board[x][y-1])
            y-=1
        return possibleMoves

    def move(self, tile,board):
        start = self.getTile()
        end = tile
        enemyPiece = end.getPiece()
        if enemyPiece == None:
            if start.isStraightClearPath(end, board):
                end.setPiece(self)
                self.setTile(tile)
                start.setPiece(None)
                return True
            else:
                print("illegal move")
                return False
        elif start.isStraightClearPath(end,board) and enemyPiece.getTeam() != self.getTeam():
                end.setPiece(self)
                self.setTile(tile)
                start.setPiece(None)
                return True
        else:
            print("illegal move")
            return False
        

class Queen(Piece):
    movement = "plus one"
    name = "Queen"
    def __init__(self,tile,team):
        super().__init__(tile,self.name,team)
    def getPossibleMoves(self,board):
        possibleMoves = set()
        currentTile = self.getTile()
        def getStraightMoves():
            x = currentTile.getColNumber()
            y = currentTile.getRow()
            while x > 0 and x < 8 and currentTile.isStraightClearPath(board.board[x+1][y],board):
                if board.board[x+1][y].getPiece()!= None:
                    if board.board[x+1][y].getPiece().getTeam() != self.getTeam():
                        possibleMoves.add(board.board[x+1][y])
                else:
                    possibleMoves.add(board.board[x+1][y])
                x+=1
            x = currentTile.getColNumber()
            while x > 1 and x < 9 and currentTile.isStraightClearPath(board.board[x-1][y],board):
                if board.board[x-1][y].getPiece()!= None:
                    if board.board[x-1][y].getPiece().getTeam() != self.getTeam():
                        possibleMoves.add(board.board[x-1][y])
                else:
                    possibleMoves.add(board.board[x-1][y])
                x-=1
            x = currentTile.getColNumber()
            while y > 0 and y < 8 and currentTile.isStraightClearPath(board.board[x][y+1],board):
                if board.board[x][y+1].getPiece()!= None:
                    if board.board[x][y+1].getPiece().getTeam() != self.getTeam():
                        possibleMoves.add(board.board[x][y+1])
                else:
                    possibleMoves.add(board.board[x][y+1])
                y+=1
            y = currentTile.getRow()
            while y > 1 and y < 9 and currentTile.isStraightClearPath(board.board[x][y-1],board):
                if board.board[x][y-1].getPiece()!= None:
                    if board.board[x][y-1].getPiece().getTeam() != self.getTeam():
                        possibleMoves.add(board.board[x][y-1])
                else:
                    possibleMoves.add(board.board[x][y-1])
                y-=1
        def getDiagonalMoves():
            x = currentTile.getColNumber()
            y = currentTile.getRow()
            while x > 0 and x < 8 and y > 0 and y < 8 and currentTile.isDiagonalClearPath(board.board[x+1][y+1],board):
                if board.board[x+1][y+1].getPiece()!= None:
                    if board.board[x+1][y+1].getPiece().getTeam() != self.getTeam():
                        possibleMoves.add(board.board[x+1][y+1])
                else:
                    possibleMoves.add(board.board[x+1][y+1])
                x+=1
                y+=1
            x = currentTile.getColNumber()
            y = currentTile.getRow()
            while x > 1 and x < 9 and y > 0 and y < 8 and currentTile.isDiagonalClearPath(board.board[x-1][y+1],board):
                if board.board[x-1][y+1].getPiece()!= None:
                    if board.board[x-1][y+1].getPiece().getTeam() != self.getTeam():
                        possibleMoves.add(board.board[x-1][y+1])
                else:
                    possibleMoves.add(board.board[x-1][y+1])
                x-=1
                y+=1
            y = currentTile.getRow()
            x = currentTile.getColNumber()
            while x > 0 and x < 8 and y > 1 and y < 9 and currentTile.isDiagonalClearPath(board.board[x+1][y-1],board):
                if board.board[x+1][y-1].getPiece()!= None:
                    if board.board[x+1][y-1].getPiece().getTeam() != self.getTeam():
                        possibleMoves.add(board.board[x+1][y-1])
                else:
                    possibleMoves.add(board.board[x+1][y-1])
                y-=1
                x+=1
            y = currentTile.getRow()
            x = currentTile.getColNumber()
            while x > 1 and x < 9 and y > 1 and y < 9 and currentTile.isDiagonalClearPath(board.board[x-1][y-1],board):
                if board.board[x-1][y-1].getPiece()!= None:
                    if board.board[x-1][y-1].getPiece().getTeam() != self.getTeam():
                        possibleMoves.add(board.board[x-1][y-1])
                else:
                    possibleMoves.add(board.board[x-1][y-1])
                y-=1
                x-=1
        getStraightMoves()
        getDiagonalMoves()
        return possibleMoves

    def move(self, tile, board):
        start = self.getTile()
        end = tile
        enemyPiece = end.getPiece()
        if enemyPiece == None:
            if start.isDiagonalClearPath(end,board) or start.isStraightClearPath(end,board):
                end.setPiece(self)
                self.setTile(tile)
                start.setPiece(None)
                return True
        elif (start.isDiagonalClearPath(end,board) or start.isStraightClearPath(end,board)) and enemyPiece.getTeam() != self.getTeam():
                end.setPiece(self)
                self.setTile(tile)
                start.setPiece(None)
                return True
        elif (start.isDiagonalClearPath(end,board) or start.isStraightClearPath(end,board)) and enemyPiece.getTeam() == self.getTeam():
            print("Cant take your own piece")
            return False
        else:
            print("illegal move")
            return False

class King(Piece):
    movement = "plus one"
    name = "King"
    def __init__(self,tile,team):
        super().__init__(tile,self.name,team)
    def getPossibleMoves(self,board):  #return a set of the possible moves the knight can jump to, regardless of what may be on the tile
        tile = self.getTile()
        x = tile.getColNumber()
        y = tile.getRow()
        moveList = []
        moveList.append([x-1,y+1])
        moveList.append([x,y+1])
        moveList.append([x+1,y+1])
        moveList.append([x+1,y])
        moveList.append([x+1,y-1])
        moveList.append([x,y-1])
        moveList.append([x-1,y-1])
        moveList.append([x-1,y])
        moves = set()
        for move in moveList: #TODO: implement removing checked tiles
            x = move[0]
            y = move[1]
            if x > 0 and x < 9 and y > 0 and y < 9:
                targetTile = board.board[x][y]
                if targetTile.getPiece() == None:
                    moves.add(targetTile)
                else:
                    if targetTile.getPiece().getTeam()!= self.getTeam():
                        moves.add(targetTile)
        return moves
    def move(self, tile, board): #TODO: implement system that prevents moves into check
        start = self.getTile()
        end = tile
        enemyPiece = end.getPiece()
        kingsTeam = self.getTeam()
        if kingsTeam == "white":
            enemyTeam = "black"
        else:
            enemyTeam = "white"
        enemy = board.getPlayer(enemyTeam)
        enemyThreats = enemy.getAllPossibleMoves()

        if end in enemyThreats: print("hi")
        if end not in enemyThreats:
            if enemyPiece == None:
                if end in self.getPossibleMoves(board):
                    end.setPiece(self)
                    self.setTile(tile)
                    start.setPiece(None)
                    return True
                else:
                    print("illegal move")
                    return False
            elif end in self.getPossibleMoves(board) and enemyPiece.getTeam() != self.getTeam():
                end.setPiece(self)
                self.setTile(tile)
                start.setPiece(None)
                return True
            else:
                print("illegalMOve")
                return False
        else:
            print("Illegal move: cant move into check")
            return False

class Knight(Piece):
    movement = "plus one"
    name = "Knight"
    def __init__(self,tile,team):
        super().__init__(tile,self.name,team)
    def getPossibleMoves(self,board): #return a set of the possible moves the knight can jump to, regardless of what may be on the tile
        tile = self.getTile()
        x = tile.getColNumber()
        y = tile.getRow()
        moveList = []
        moveList.append([x+2,y+1])
        moveList.append([x+2,y-1])
        moveList.append([x-2,y+1])
        moveList.append([x-2,y-1])
        moveList.append([x+1,y+2])
        moveList.append([x+1,y-2])
        moveList.append([x-1,y+2])
        moveList.append([x-1,y-2])
      
        moves = set()
        for move in moveList:
            x = move[0]
            y = move[1]
            if x > 0 and x < 9 and y > 0 and y < 9:
                targetTile = board.board[x][y]
                if targetTile.getPiece() == None:
                    moves.add(targetTile)
                else:
                    if targetTile.getPiece().getTeam()!= self.getTeam():
                        moves.add(targetTile)
        return moves
    def move(self, tile, board):
        start = self.getTile()
        end = tile
        enemyPiece = end.getPiece()
        if enemyPiece == None:
            if end in self.getPossibleMoves(board):
                end.setPiece(self)
                self.setTile(tile)
                start.setPiece(None)
                return True
            else:
                print("illegal move")
                return False
        elif end in self.getPossibleMoves(board) and enemyPiece.getTeam() != self.getTeam():
            end.setPiece(self)
            self.setTile(tile)
            start.setPiece(None)
            return True
        else:
            print("illegalMOve")
            return False
class Bishop(Piece):
    movement = "plus one"
    name = "Bishop"
    def __init__(self,tile,team):
        super().__init__(tile,self.name,team)
    def getPossibleMoves(self,board):
        currentTile = self.getTile()
        x = currentTile.getColNumber()
        y = currentTile.getRow()
        possibleMoves = set()
        while x > 0 and x < 8 and y > 0 and y < 8 and currentTile.isDiagonalClearPath(board.board[x+1][y+1],board):
            if board.board[x+1][y+1].getPiece()!= None:
                if board.board[x+1][y+1].getPiece().getTeam() != self.getTeam():
                    possibleMoves.add(board.board[x+1][y+1])
            else:
                possibleMoves.add(board.board[x+1][y+1])
            x+=1
            y+=1
        x = currentTile.getColNumber()
        y = currentTile.getRow()
        while x > 1 and x < 9 and y > 0 and y < 8 and currentTile.isDiagonalClearPath(board.board[x-1][y+1],board):
            if board.board[x-1][y+1].getPiece()!= None:
                if board.board[x-1][y+1].getPiece().getTeam() != self.getTeam():
                    possibleMoves.add(board.board[x-1][y+1])
            else:
                possibleMoves.add(board.board[x-1][y+1])
            x-=1
            y+=1
        y = currentTile.getRow()
        x = currentTile.getColNumber()
        while x > 0 and x < 8 and y > 1 and y < 9 and currentTile.isDiagonalClearPath(board.board[x+1][y-1],board):
            if board.board[x+1][y-1].getPiece()!= None:
                if board.board[x+1][y-1].getPiece().getTeam() != self.getTeam():
                    possibleMoves.add(board.board[x+1][y-1])
            else:
                possibleMoves.add(board.board[x+1][y-1])
            x+=1
            y-=1
        y = currentTile.getRow()
        x = currentTile.getColNumber()
        while x > 1 and x < 9 and y > 1 and y < 9 and currentTile.isDiagonalClearPath(board.board[x-1][y-1],board):
            if board.board[x-1][y-1].getPiece()!= None:
                if board.board[x-1][y-1].getPiece().getTeam() != self.getTeam():
                    possibleMoves.add(board.board[x-1][y-1])
            else:
                possibleMoves.add(board.board[x-1][y-1])
            x-=1
            y-=1
        return possibleMoves
    def move(self, tile, board):
        start = self.getTile()
        end = tile
        enemyPiece = end.getPiece()

        if enemyPiece == None:
            if start.isDiagonalClearPath(end,board):
                end.setPiece(self)
                self.setTile(end)
                start.setPiece(None)
                return True
            else:
                print("illegal move")
                return False
        elif enemyPiece.getTeam() != self.getTeam() and start.isDiagonalClearPath(end,board):
                end.setPiece(self)
                self.setTile(end)
                start.setPiece(None)
                return True
        else:
            print("illegal move")
            return False
        


        