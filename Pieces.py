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
    def isPinned(self,player, board):
        tile = self.getTile()
        numChecks = 0
        opponent = player.getOpponent()
        opponentPieceMoves = opponent.getPieceMoves()

        for piece in opponentPieceMoves:
            if player.getKing().getTile() in opponentPieceMoves[piece]:
                numChecks+=1
        print("Checks with piece in place:",numChecks)
        #Simulate effect of moving piece
        tile.setPiece(None)
        player.opponent.recalculateAllPossibleMoves(board)
        opponentPossibleMovesPostMove = opponent.getPieceMoves()
        numChecksAfter = 0
        for piece in opponentPossibleMovesPostMove:
            if player.getKing().getTile() in opponentPossibleMovesPostMove[piece]:
                numChecksAfter+=1
        print("Checks with piece out of place",numChecksAfter)

        #Restore state
        tile.setPiece(self)
        player.opponent.recalculateAllPossibleMoves(board)
        return numChecksAfter > numChecks
    def isAlive(self,board):
        row = 1
        while row < 9:
            for col in range(8,0,-1):
                if board.board[col][row].getPiece() == self:
                    return True 
            row+=1
        return False
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
                self.numberOfMoves+=1
            elif start.getRow() - end.getRow() == -1 and end.isOccupied() == True and abs(start.getColNumber() - end.getColNumber()) == 1: #diagonal attack
                end.setPiece(self)
                self.setTile(tile)
                start.setPiece(None)
                self.numberOfMoves+=1
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
                self.numberOfMoves+=1
            elif start.getRow() - end.getRow() == 1 and end.isOccupied() == True and abs(start.getColNumber() - end.getColNumber()) == 1: #diagonalAttack
                end.setPiece(self)
                self.setTile(tile)
                start.setPiece(None)
                self.numberOfMoves+=1
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
    isShortSide = False
    def __init__(self,tile,team):
        super().__init__(tile,self.name,team)
        if self.getCol() == 'h':
            self.isShortSide = True
        else:
            self.isShortSide = False
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
                self.numberOfMoves+=1
                return True
            else:
                print("illegal move")
                return False
        elif start.isStraightClearPath(end,board) and enemyPiece.getTeam() != self.getTeam():
                end.setPiece(self)
                self.setTile(tile)
                start.setPiece(None)
                self.numberOfMoves+=1
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
        end = tile #end and start are tiles
        enemyPiece = end.getPiece()
        kingsTeam = self.getTeam()
        if kingsTeam == "white":
            enemyTeam = "black"
        else:
            enemyTeam = "white"
        enemy = board.getPlayer(enemyTeam)
        enemyThreats = enemy.getAllPossibleMoves()

        #CASTLEMOVE
        player = board.getPlayer(kingsTeam)
        if kingsTeam == "white" and end.getName() == "c1" and self.canLongCastle(player,board):
            rook = board.getTileMap()['a1'].getPiece()
            rookTile = rook.getTile()
            rookTile.setPiece(None)
            board.getTileMap()['d1'].setPiece(rook)
            self.getTile().setPiece(None)
            board.getTileMap()['c1'].setPiece(self)
            return True
        elif kingsTeam == "white" and end.getName() == "g1" and self.canShortCastle(player,board):
            rook = board.getTileMap()['h1'].getPiece()
            rookTile = rook.getTile()
            rookTile.setPiece(None)
            board.getTileMap()['f1'].setPiece(rook)
            self.getTile().setPiece(None)
            board.getTileMap()['g1'].setPiece(self)
            return True
        elif kingsTeam == "black" and end.getName() == "c8" and self.canLongCastle(player,board):
            rook = board.getTileMap()['a8'].getPiece()
            rookTile = rook.getTile()
            rookTile.setPiece(None)
            board.getTileMap()['d8'].setPiece(rook)
            self.getTile().setPiece(None)
            board.getTileMap()['c8'].setPiece(self)
            return True
        elif kingsTeam == "white" and end.getName() == "g8" and self.canShortCastle(player,board):
            rook = board.getTileMap()['h8'].getPiece()
            rookTile = rook.getTile()
            rookTile.setPiece(None)
            board.getTileMap()['f8'].setPiece(rook)
            self.getTile().setPiece(None)
            board.getTileMap()['g8'].setPiece(self)
            return True
            


        if end not in enemyThreats:
            if enemyPiece == None:
                if end in self.getPossibleMoves(board):
                    end.setPiece(self)
                    self.setTile(tile)
                    start.setPiece(None)
                    self.numberOfMoves+=1
                    return True
                else:
                    print("illegal move")
                    return False
            elif end in self.getPossibleMoves(board) and enemyPiece.getTeam() != self.getTeam():
                end.setPiece(self)
                self.setTile(tile)
                start.setPiece(None)
                self.numberOfMoves+=1
                return True
            else:
                print("illegalMOve")
                return False
        else:
            print("Illegal move: cant move into check")
            return False
    def canLongCastle(self,player,board):
        tileMap = board.getTileMap()
        for piece in player.getPieceMoves():
            if piece.name =="Rook":
                if not piece.isShortSide:
                    longRook = piece
        if player.getTeam() == "white":
            b1, c1, d1 = tileMap['b1'],tileMap['c1'],tileMap['d1']
            if b1.getPiece() == None and c1.getPiece() == None and d1.getPiece() == None: 
                if longRook.numberOfMoves == 0 and player.getKing().numberOfMoves == 0:
                    enemyThreats = player.getOpponent().getAllPossibleMoves()
                    if d1 not in enemyThreats and c1 not in enemyThreats:
                        return True
        else:
            b8, c8, d8 = tileMap['b8'],tileMap['c8'],tileMap['d8']
            if b8.getPiece() == None and c8.getPiece() == None and d8.getPiece() == None: 
                if longRook.numberOfMoves == 0 and player.getKing().numberOfMoves == 0:
                    enemyThreats = player.getOpponent().getAllPossibleMoves()
                    if d8 not in enemyThreats and c8 not in enemyThreats:
                        return True
        return False
    def canShortCastle(self,player,board):
        tileMap = board.getTileMap()
        for piece in player.getPieceMoves():
            if piece.name =="Rook":
                if piece.isShortSide:
                    shortRook = piece
        if player.getTeam() == "white":
            g1, f1 = tileMap['g1'],tileMap['f1'],
            if g1.getPiece() == None and f1.getPiece() == None: 
                if shortRook.numberOfMoves == 0 and player.getKing().numberOfMoves == 0:
                    enemyThreats = player.getOpponent().getAllPossibleMoves()
                    if g1 not in enemyThreats and f1 not in enemyThreats:
                        return True
        else:
            g8, f8 = tileMap['g8'],tileMap['f8'],
            if g8.getPiece() == None and f8.getPiece() == None: 
                if shortRook.numberOfMoves == 0 and player.getKing().numberOfMoves == 0:
                    enemyThreats = player.getOpponent().getAllPossibleMoves()
                    if g8 not in enemyThreats and f8 not in enemyThreats:
                        return True
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
                