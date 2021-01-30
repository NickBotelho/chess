class Piece: #TODO: add move tracker
    name = None
    currentTile = None
    team = None
    numberOfMoves = 0
    def __init__(self, tile,name,team,board):
        self.name = name
        self.currentTile = tile
        self.team = team
        self.board = board
        self.possibleAttacks = set()
    def setTile(self,tile):
        self.currentTile = tile
    def getTile(self):
        return self.currentTile
    def getName(self):
        return self.name
    def getTeam(self):
        return self.team
    def getRow(self):
        return self.getTile().getRow()
    def getCol(self):#letter
        return self.getTile().getCol()
    def getColNumber(self):#number
        return self.getTile().getColNumber()
    def isPinned(self,player,move):
        tile = self.getTile()
        numChecks = 0
        opponent = player.getOpponent()
        activeOpponentPieces = opponent.getActivePieces()
        startTile = move[0]
        endTile = move[1]
        endTileContent = endTile.getPiece()

        for piece in activeOpponentPieces:
            piece.getPossibleMoves()
            if player.getKing().getTile() in piece.getPossibleAttacks():
                numChecks+=1

        #Simulate effect of moving piece
        tile.setPiece(None)
        endTile.setPiece(self)
        self.setTile(endTile)

        numChecksAfter = 0
        for piece in activeOpponentPieces:
            piece.getPossibleMoves()
            if player.getKing().getTile() in piece.getPossibleAttacks():
                numChecksAfter+=1
        #print("Checks with piece out of place",numChecksAfter)

        #Restore state
        tile.setPiece(self)
        endTile.setPiece(endTileContent)
        self.setTile(tile)
        opponent.recalculateAllPossibleMoves(self.board)
        for piece in activeOpponentPieces:
            piece.getPossibleMoves()
        return numChecksAfter > numChecks
    def isAlive(self):
        
        return self in self.board.getActivePieces()
    def getPossibleAttacks(self): #gets all the tiles that can be attacked have have an enemy on them
        self.getPossibleMoves()
        return self.possibleAttacks
    def executeMove(self,end):
        player = self.board.getPlayer(self.getTeam())
        tile = self.getTile()
        endContents = end.getPiece()
        end.setPiece(self)
        self.setTile(end)
        tile.setPiece(None)
        self.numberOfMoves+=1
        ####if the move is caputring a piece
        if endContents != None:
            #add to player.capturedPIeces
            #recalc enemies active pieces
            self.board.setActivePieces()
            player.getOpponent().getActivePieces()
    def getAbbreviation(self):
        if self.name == "Pawn":
            return ""
        elif self.name == "Rook":
            return "R"
        elif self.name == "Bishop":
            return "B"
        elif self.name == "Knight":
            return "N"
        elif self.name == "Queen":
            return "Q"
        elif self.name == "King":
            return "K"

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
    def __init__(self,tile,team,board):
        super().__init__(tile,self.name,team,board)
    def getPossibleMoves(self):
        possibleMoves = set() #all the possible tiles
        self.possibleAttacks = set() #all the possible tiles that have an enemy on them
        if self.numberOfMoves==0:
            if self.getTeam() =="white":
                y = self.getTile().getRow() + 2
            else:
                y = self.getTile().getRow() - 2
            if self.board.board[self.getTile().getColNumber()][y].getPiece == None:
                possibleMoves.add(self.board.board[self.getTile().getColNumber()][y])
        if self.getTeam() == "white":
            if self.getTile().getRow() < 8:
                front = self.board.board[self.getTile().getColNumber()][self.getTile().getRow()+1]
                if front.getPiece() == None:
                    possibleMoves.add(front)
                if self.getTile().getColNumber() > 1:
                    leftDiagonal = self.board.board[self.getTile().getColNumber()-1][self.getTile().getRow()+1]
                    if leftDiagonal.getPiece() != None and leftDiagonal.getPiece().getTeam()!= self.getTeam():
                        possibleMoves.add(leftDiagonal)
                        self.possibleAttacks.add(leftDiagonal)
                if self.getTile().getColNumber() < 8:
                    rightDiagonal = self.board.board[self.getTile().getColNumber()+1][self.getTile().getRow()+1]
                    if rightDiagonal.getPiece() != None and rightDiagonal.getPiece().getTeam() != self.getTeam():
                        possibleMoves.add(rightDiagonal)
                        self.possibleAttacks.add(rightDiagonal)
        else:
            if self.getTile().getRow() > 1:
                front = self.board.board[self.getTile().getColNumber()][self.getTile().getRow()-1]
                if front.getPiece() == None:
                    possibleMoves.add(front)
                if self.getTile().getColNumber() > 1:
                    leftDiagonal = self.board.board[self.getTile().getColNumber()-1][self.getTile().getRow()-1]
                    if leftDiagonal.getPiece() != None and leftDiagonal.getPiece().getTeam()!= self.getTeam():
                        possibleMoves.add(leftDiagonal)
                        self.possibleAttacks.add(leftDiagonal)
                if self.getTile().getColNumber() < 8:
                    rightDiagonal = self.board.board[self.getTile().getColNumber()+1][self.getTile().getRow()-1]
                    if rightDiagonal.getPiece() != None and rightDiagonal.getPiece().getTeam() != self.getTeam():
                        possibleMoves.add(rightDiagonal)
                        self.possibleAttacks.add(rightDiagonal)
        #TODO:add antpisants LMAO


        #ALSO: possibleAttacks set has been updated
        return possibleMoves
    def move(self,tile): #TODO:, add the first move 2 tile
        start = self.getTile()
        end = tile
        validMove = True
        if self.team == "white":
            if start.getRow() - end.getRow() == -1 and end.isOccupied() == False and start.getCol() == end.getCol(): #valid single move no take
                self.executeMove(end)
            elif start.getRow() - end.getRow() == -1 and end.isOccupied() == True and abs(start.getColNumber() - end.getColNumber()) == 1: #diagonal attack
                self.executeMove(end)
                #trash enemey piece right not its in lingo
            elif start.getRow() - end.getRow() == -2 and end.isOccupied() == False and start.getCol() == end.getCol() and self.numberOfMoves == 0 and start.isStraightClearPath(end,self.board): #first move 2 spaces
                self.executeMove(end)

            else:
                print("illgal move")
                validMove = False
        else:
            if start.getRow() - end.getRow() == 1 and end.isOccupied() == False and start.getCol() == end.getCol(): #valid single move
                self.executeMove(end)
            elif start.getRow() - end.getRow() == 1 and end.isOccupied() == True and abs(start.getColNumber() - end.getColNumber()) == 1: #diagonalAttack
                self.executeMove(end)
                #trash enemey piece right not its in lingo
            elif start.getRow() - end.getRow() == 2 and end.isOccupied() == False and start.getCol() == end.getCol() and self.numberOfMoves == 0 and start.isStraightClearPath(end,self.board): #first move 2 spaces
                self.executeMove(end)

            else:
                print("illgal move")
                validMove = False
        #promotion
        if (self.getTeam() == "white" and self.getTile().getRow() == 8) or (self.getTeam() == "black" and self.getTile().getRow() == 1) and validMove:
            tile = self.getTile()
            promotions = {"queen","rook","bishop","knight"}
            print("promotion available, select 'queen', 'rook', 'bishop', or 'knight'")
            #promotion = input() #for human input
            promotion = "queen"
            while promotion.lower() not in promotions:
                print("invalid input, try again")
                promotion = input()
            if promotion == "queen":     
                tile.setPiece(Queen(tile,self.getTeam(),self.board))
            elif promotion == "rook":
                tile.setPiece(Rook(tile, self.getTeam(),self.board))
            elif promotion == "bishop":
                tile.setPiece(Bishop( tile, self.getTeam(),self.board))
            elif promotion == "knight":
                tile.setPiece(Knight(tile, self.getTeam(),self.board))
            newPiece = tile.getPiece()
            player = self.board.getPlayer(self.getTeam())
            player.addPromotedPiece(newPiece,self.board)
            player.updatePossibleMoves(self.board, newPiece)
            player.recalculateAllPossibleMoves(self.board)
            
            

        return validMove
class Rook(Piece):
    movement = "plus one"
    name = "Rook"
    isShortSide = False
    def __init__(self,tile,team,board):
        super().__init__(tile,self.name,team,board)
        if self.getCol() == 'h':
            self.isShortSide = True
        else:
            self.isShortSide = False
    def getPossibleMoves(self):
        currentTile = self.getTile()
        x = currentTile.getColNumber()
        y = currentTile.getRow()
        possibleMoves = set()
        self.possibleAttacks = set()
        while x > 0 and x < 8 and currentTile.isStraightClearPath(self.board.board[x+1][y],self.board):
            if self.board.board[x+1][y].getPiece()!= None:
                if self.board.board[x+1][y].getPiece().getTeam() != self.getTeam():
                    possibleMoves.add(self.board.board[x+1][y])
                    self.possibleAttacks.add(self.board.board[x+1][y])
            else:
                possibleMoves.add(self.board.board[x+1][y])
            x+=1
        x = currentTile.getColNumber()
        while x > 1 and x < 9 and currentTile.isStraightClearPath(self.board.board[x-1][y],self.board):
            if self.board.board[x-1][y].getPiece()!= None:
                if self.board.board[x-1][y].getPiece().getTeam() != self.getTeam():
                    possibleMoves.add(self.board.board[x-1][y])
                    self.possibleAttacks.add(self.board.board[x-1][y])
            else:
                possibleMoves.add(self.board.board[x-1][y])
            x-=1
        x = currentTile.getColNumber()
        while y > 0 and y < 8 and currentTile.isStraightClearPath(self.board.board[x][y+1],self.board):
            if self.board.board[x][y+1].getPiece()!= None:
                if self.board.board[x][y+1].getPiece().getTeam() != self.getTeam():
                    possibleMoves.add(self.board.board[x][y+1])
                    self.possibleAttacks.add(self.board.board[x][y+1])
            else:
                possibleMoves.add(self.board.board[x][y+1])
            y+=1
        y = currentTile.getRow()
        while y > 1 and y < 9 and currentTile.isStraightClearPath(self.board.board[x][y-1],self.board):
            if self.board.board[x][y-1].getPiece()!= None:
                if self.board.board[x][y-1].getPiece().getTeam() != self.getTeam(): #theres an enemy in the way
                    possibleMoves.add(self.board.board[x][y-1])
                    self.possibleAttacks.add(self.board.board[x][y-1])
            else:
                possibleMoves.add(self.board.board[x][y-1])
            y-=1
        return possibleMoves

    def move(self, tile):
        start = self.getTile()
        end = tile
        enemyPiece = end.getPiece()
        if enemyPiece == None:
            if start.isStraightClearPath(end, self.board):
                self.executeMove(end)
                return True
            else:
                print("illegal move")
                return False
        elif start.isStraightClearPath(end,self.board) and enemyPiece.getTeam() != self.getTeam():
                self.executeMove(end)
                return True
        else:
            print("illegal move")
            return False
class Queen(Piece):
    movement = "plus one"
    name = "Queen"
    def __init__(self,tile,team,board):
        super().__init__(tile,self.name,team,board)
    def getPossibleMoves(self):
        possibleMoves = set()
        self.possibleAttacks = set()
        currentTile = self.getTile()
        def getStraightMoves():
            x = currentTile.getColNumber()
            y = currentTile.getRow()
            while x > 0 and x < 8 and currentTile.isStraightClearPath(self.board.board[x+1][y],self.board):
                if self.board.board[x+1][y].getPiece()!= None:
                    if self.board.board[x+1][y].getPiece().getTeam() != self.getTeam():
                        possibleMoves.add(self.board.board[x+1][y])
                        self.possibleAttacks.add(self.board.board[x+1][y])
                else:
                    possibleMoves.add(self.board.board[x+1][y])
                x+=1
            x = currentTile.getColNumber()
            while x > 1 and x < 9 and currentTile.isStraightClearPath(self.board.board[x-1][y],self.board):
                if self.board.board[x-1][y].getPiece()!= None:
                    if self.board.board[x-1][y].getPiece().getTeam() != self.getTeam():
                        possibleMoves.add(self.board.board[x-1][y])
                        self.possibleAttacks.add(self.board.board[x-1][y])
                else:
                    possibleMoves.add(self.board.board[x-1][y])
                x-=1
            x = currentTile.getColNumber()
            while y > 0 and y < 8 and currentTile.isStraightClearPath(self.board.board[x][y+1],self.board):
                if self.board.board[x][y+1].getPiece()!= None:
                    if self.board.board[x][y+1].getPiece().getTeam() != self.getTeam():
                        possibleMoves.add(self.board.board[x][y+1])
                        self.possibleAttacks.add(self.board.board[x][y+1])
                else:
                    possibleMoves.add(self.board.board[x][y+1])
                y+=1
            y = currentTile.getRow()
            while y > 1 and y < 9 and currentTile.isStraightClearPath(self.board.board[x][y-1],self.board):
                if self.board.board[x][y-1].getPiece()!= None:
                    if self.board.board[x][y-1].getPiece().getTeam() != self.getTeam():
                        possibleMoves.add(self.board.board[x][y-1])
                        self.possibleAttacks.add(self.board.board[x][y-1])
                else:
                    possibleMoves.add(self.board.board[x][y-1])
                y-=1
        def getDiagonalMoves():
            x = currentTile.getColNumber()
            y = currentTile.getRow()
            while x > 0 and x < 8 and y > 0 and y < 8 and currentTile.isDiagonalClearPath(self.board.board[x+1][y+1],self.board):
                if self.board.board[x+1][y+1].getPiece()!= None:
                    if self.board.board[x+1][y+1].getPiece().getTeam() != self.getTeam():
                        possibleMoves.add(self.board.board[x+1][y+1])
                        self.possibleAttacks.add(self.board.board[x+1][y+1])
                else:
                    possibleMoves.add(self.board.board[x+1][y+1])
                x+=1
                y+=1
            x = currentTile.getColNumber()
            y = currentTile.getRow()
            while x > 1 and x < 9 and y > 0 and y < 8 and currentTile.isDiagonalClearPath(self.board.board[x-1][y+1],self.board):
                if self.board.board[x-1][y+1].getPiece()!= None:
                    if self.board.board[x-1][y+1].getPiece().getTeam() != self.getTeam():
                        possibleMoves.add(self.board.board[x-1][y+1])
                        self.possibleAttacks.add(self.board.board[x-1][y+1])
                else:
                    possibleMoves.add(self.board.board[x-1][y+1])
                x-=1
                y+=1
            y = currentTile.getRow()
            x = currentTile.getColNumber()
            while x > 0 and x < 8 and y > 1 and y < 9 and currentTile.isDiagonalClearPath(self.board.board[x+1][y-1],self.board):
                if self.board.board[x+1][y-1].getPiece()!= None:
                    if self.board.board[x+1][y-1].getPiece().getTeam() != self.getTeam():
                        possibleMoves.add(self.board.board[x+1][y-1])
                        self.possibleAttacks.add(self.board.board[x+1][y-1])
                else:
                    possibleMoves.add(self.board.board[x+1][y-1])
                y-=1
                x+=1
            y = currentTile.getRow()
            x = currentTile.getColNumber()
            while x > 1 and x < 9 and y > 1 and y < 9 and currentTile.isDiagonalClearPath(self.board.board[x-1][y-1],self.board):
                if self.board.board[x-1][y-1].getPiece()!= None:
                    if self.board.board[x-1][y-1].getPiece().getTeam() != self.getTeam():
                        possibleMoves.add(self.board.board[x-1][y-1])
                        self.possibleAttacks.add(self.board.board[x-1][y-1])
                else:
                    possibleMoves.add(self.board.board[x-1][y-1])
                y-=1
                x-=1
        getStraightMoves()
        getDiagonalMoves()
        return possibleMoves

    def move(self, tile):
        start = self.getTile()
        end = tile
        enemyPiece = end.getPiece()
        if enemyPiece == None:
            if start.isDiagonalClearPath(end,self.board) or start.isStraightClearPath(end,self.board):
                self.executeMove(end)
                return True
        elif (start.isDiagonalClearPath(end,self.board) or start.isStraightClearPath(end,self.board)) and enemyPiece.getTeam() != self.getTeam():
                self.executeMove(end)
                return True
        elif (start.isDiagonalClearPath(end,self.board) or start.isStraightClearPath(end,self.board)) and enemyPiece.getTeam() == self.getTeam():
            print("Cant take your own piece")
            return False
        else:
            print("illegal move")
            return False
class King(Piece):
    movement = "plus one"
    name = "King"
    def __init__(self,tile,team,board):
        super().__init__(tile,self.name,team,board)
    def getPossibleMoves(self):  #return a set of the possible moves the knight can jump to, regardless of what may be on the tile
        tile = self.getTile()
        self.possibleAttacks = set()
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
                targetTile = self.board.board[x][y]
                if targetTile.getPiece() == None:
                    moves.add(targetTile)
                else:
                    if targetTile.getPiece().getTeam()!= self.getTeam():
                        moves.add(targetTile)
                        self.possibleAttacks.add(targetTile)
        return moves
    def move(self, tile): #TODO: implement system that prevents moves into check
        start = self.getTile()
        end = tile #end and start are tiles
        enemyPiece = end.getPiece()
        kingsTeam = self.getTeam()
        if kingsTeam == "white":
            enemyTeam = "black"
        else:
            enemyTeam = "white"
        enemy = self.board.getPlayer(enemyTeam)
        

        #CASTLEMOVE
        player = self.board.getPlayer(kingsTeam)
        if kingsTeam == "white" and end.getName() == "c1" and self.canLongCastle(player):
            rook = self.board.getTileMap()['a1'].getPiece()
            rookTile = rook.getTile()
            rookTile.setPiece(None)
            self.board.getTileMap()['d1'].setPiece(rook)
            self.getTile().setPiece(None)
            self.board.getTileMap()['c1'].setPiece(self)
            return True
        elif kingsTeam == "white" and end.getName() == "g1" and self.canShortCastle(player):
            rook = self.board.getTileMap()['h1'].getPiece()
            rookTile = rook.getTile()
            rookTile.setPiece(None)
            self.board.getTileMap()['f1'].setPiece(rook)
            self.getTile().setPiece(None)
            self.board.getTileMap()['g1'].setPiece(self)
            return True
        elif kingsTeam == "black" and end.getName() == "c8" and self.canLongCastle(player):
            rook = self.board.getTileMap()['a8'].getPiece()
            rookTile = rook.getTile()
            rookTile.setPiece(None)
            self.board.getTileMap()['d8'].setPiece(rook)
            self.getTile().setPiece(None)
            self.board.getTileMap()['c8'].setPiece(self)
            return True
        elif kingsTeam == "white" and end.getName() == "g8" and self.canShortCastle(player):
            rook = self.board.getTileMap()['h8'].getPiece()
            rookTile = rook.getTile()
            rookTile.setPiece(None)
            self.board.getTileMap()['f8'].setPiece(rook)
            self.getTile().setPiece(None)
            self.board.getTileMap()['g8'].setPiece(self)
            return True

        enemyThreats = enemy.calculateAllPossibleAttacks()   
        safeMoves = set()

        for move in self.getPossibleMoves(): 
             
            cacheContents = move.getPiece()
            move.setPiece(self)
            self.setTile(move)
            start.setPiece(None)
            simulatedThreats = enemy.calculateAllPossibleAttacks()
            if move not in simulatedThreats:
                safeMoves.add(move)
            move.setPiece(cacheContents)
            self.setTile(start)
            start.setPiece(self)
            enemy.calculateAllPossibleAttacks()

        if end not in enemyThreats:
            if enemyPiece == None and end in safeMoves:
                if end in self.getPossibleMoves():
                    self.executeMove(end)
                    return True
                else:
                    print("illegal move")
                    return False
            elif enemyPiece != None and end in self.getPossibleMoves() and enemyPiece.getTeam() != self.getTeam() and end in safeMoves:
                self.executeMove(end)
                return True
            else:
                print("illegalMOve")
                return False
        else:
            print("Illegal move: cant move into check")
            return False
    def canLongCastle(self,player):
        longRook = None
        tileMap = self.board.getTileMap()
        for piece in player.getPieceMoves():
            if piece.name =="Rook":
                if not piece.isShortSide:
                    longRook = piece
        if player.getTeam() == "white":
            b1, c1, d1 = tileMap['b1'],tileMap['c1'],tileMap['d1']
            if b1.getPiece() == None and c1.getPiece() == None and d1.getPiece() == None: 
                if longRook != None and longRook.numberOfMoves == 0 and player.getKing().numberOfMoves == 0:
                    enemyThreats = player.getOpponent().getAllPossibleMoves()
                    if d1 not in enemyThreats and c1 not in enemyThreats:
                        return True
        else:
            b8, c8, d8 = tileMap['b8'],tileMap['c8'],tileMap['d8']
            if b8.getPiece() == None and c8.getPiece() == None and d8.getPiece() == None: 
                if longRook != None and longRook.numberOfMoves == 0 and player.getKing().numberOfMoves == 0:
                    enemyThreats = player.getOpponent().getAllPossibleMoves()
                    if d8 not in enemyThreats and c8 not in enemyThreats:
                        return True
        return False
    def canShortCastle(self,player):
        shortRook = None
        tileMap = self.board.getTileMap()
        for piece in player.getPieceMoves():
            if piece.name =="Rook":
                if piece.isShortSide:
                    shortRook = piece
        if player.getTeam() == "white":
            g1, f1 = tileMap['g1'],tileMap['f1'],
            if g1.getPiece() == None and f1.getPiece() == None: 
                if shortRook != None and shortRook.numberOfMoves == 0 and player.getKing().numberOfMoves == 0:
                    enemyThreats = player.getOpponent().getAllPossibleMoves()
                    if g1 not in enemyThreats and f1 not in enemyThreats:
                        return True
        else:
            g8, f8 = tileMap['g8'],tileMap['f8'],
            if g8.getPiece() == None and f8.getPiece() == None: 
                if shortRook != None and shortRook.numberOfMoves == 0 and player.getKing().numberOfMoves == 0:
                    enemyThreats = player.getOpponent().getAllPossibleMoves()
                    if g8 not in enemyThreats and f8 not in enemyThreats:
                        return True
        return False
class Knight(Piece):
    movement = "plus one"
    name = "Knight"
    def __init__(self,tile,team,board):
        super().__init__(tile,self.name,team,board)
    def getPossibleMoves(self): #return a set of the possible moves the knight can jump to, regardless of what may be on the tile
        tile = self.getTile()
        self.possibleAttacks = set()
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
                targetTile = self.board.board[x][y]
                if targetTile.getPiece() == None:
                    moves.add(targetTile)
                else:
                    if targetTile.getPiece().getTeam()!= self.getTeam():
                        moves.add(targetTile)
                        self.possibleAttacks.add(targetTile)
        return moves
    def move(self, tile):
        start = self.getTile()
        end = tile
        enemyPiece = end.getPiece()
        if enemyPiece == None:
            if end in self.getPossibleMoves():
                self.executeMove(end)
                return True
            else:
                print("illegal move")
                return False
        elif end in self.getPossibleMoves() and enemyPiece.getTeam() != self.getTeam():
            self.executeMove(end)
            return True
        else:
            print("illegalMOve")
            return False
class Bishop(Piece):
    movement = "plus one"
    name = "Bishop"
    def __init__(self,tile,team,board):
        super().__init__(tile,self.name,team,board)
    def getPossibleMoves(self):
        currentTile = self.getTile()
        self.possibleAttacks = set()
        x = currentTile.getColNumber()
        y = currentTile.getRow()
        possibleMoves = set()
        while x > 0 and x < 8 and y > 0 and y < 8 and currentTile.isDiagonalClearPath(self.board.board[x+1][y+1],self.board):
            if self.board.board[x+1][y+1].getPiece()!= None:
                if self.board.board[x+1][y+1].getPiece().getTeam() != self.getTeam():
                    possibleMoves.add(self.board.board[x+1][y+1])
                    self.possibleAttacks.add(self.board.board[x+1][y+1])
            else:
                possibleMoves.add(self.board.board[x+1][y+1])
            x+=1
            y+=1
        x = currentTile.getColNumber()
        y = currentTile.getRow()
        while x > 1 and x < 9 and y > 0 and y < 8 and currentTile.isDiagonalClearPath(self.board.board[x-1][y+1],self.board):
            if self.board.board[x-1][y+1].getPiece()!= None:
                if self.board.board[x-1][y+1].getPiece().getTeam() != self.getTeam():
                    possibleMoves.add(self.board.board[x-1][y+1])
                    self.possibleAttacks.add(self.board.board[x-1][y+1])
            else:
                possibleMoves.add(self.board.board[x-1][y+1])
            x-=1
            y+=1
        y = currentTile.getRow()
        x = currentTile.getColNumber()
        while x > 0 and x < 8 and y > 1 and y < 9 and currentTile.isDiagonalClearPath(self.board.board[x+1][y-1],self.board):
            if self.board.board[x+1][y-1].getPiece()!= None:
                if self.board.board[x+1][y-1].getPiece().getTeam() != self.getTeam():
                    possibleMoves.add(self.board.board[x+1][y-1])
                    self.possibleAttacks.add(self.board.board[x+1][y-1])
            else:
                possibleMoves.add(self.board.board[x+1][y-1])
            x+=1
            y-=1
        y = currentTile.getRow()
        x = currentTile.getColNumber()
        while x > 1 and x < 9 and y > 1 and y < 9 and currentTile.isDiagonalClearPath(self.board.board[x-1][y-1],self.board):
            if self.board.board[x-1][y-1].getPiece()!= None:
                if self.board.board[x-1][y-1].getPiece().getTeam() != self.getTeam():
                    possibleMoves.add(self.board.board[x-1][y-1])
                    self.possibleAttacks.add(self.board.board[x-1][y-1])
            else:
                possibleMoves.add(self.board.board[x-1][y-1])
            x-=1
            y-=1
        return possibleMoves
    def move(self, tile):
        start = self.getTile()
        end = tile
        enemyPiece = end.getPiece()

        if enemyPiece == None:
            if start.isDiagonalClearPath(end,self.board):
                self.executeMove(end)
                return True
            else:
                print("illegal move")
                return False
        elif enemyPiece.getTeam() != self.getTeam() and start.isDiagonalClearPath(end,self.board):
                self.executeMove(end)
                return True
        else:
            print("illegal move")
            return False
                