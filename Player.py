from Game import Game
class Player():
    elo = None
    numMoves = 0
    allPossibleMoves= set()
    opponent = None
    isChecked = False

    def __init__(self, team, name,board):
        self.team = team
        self.name = name
        self.pieceMoves = self.calibrate(board)
        self.activePieces = self.getActivePieces()
        self.game = Game()
        self.allPossibleAttacks = self.calculateAllPossibleAttacks()

        
    def calibrate(self,board): #ran in conjunction with reset/creation of a board
        pieceMoves = {}
        if self.team == "white":
            pawnIndex = 1
            while pawnIndex < 9:
                currentPawn = board.board[pawnIndex][2].getPiece()
                pieceMoves[currentPawn] = currentPawn.getPossibleMoves()
                self.allPossibleMoves = self.allPossibleMoves | currentPawn.getPossibleMoves()
                pawnIndex+=1
            #rooks
            rook = board.board[1][1].getPiece()
            pieceMoves[rook] = rook.getPossibleMoves()
            rook = board.board[8][1].getPiece()
            pieceMoves[rook] = rook.getPossibleMoves()
            #knights
            knight = board.board[2][1].getPiece()
            pieceMoves[knight] = knight.getPossibleMoves()
            knight = board.board[7][1].getPiece()
            pieceMoves[knight] = knight.getPossibleMoves()
            #Bishops
            bishop = board.board[3][1].getPiece()
            pieceMoves[bishop] = bishop.getPossibleMoves()
            bishop = board.board[6][1].getPiece()
            pieceMoves[bishop] = bishop.getPossibleMoves()
            #queen
            self.queen = board.board[4][1].getPiece()
            pieceMoves[self.queen] = self.queen.getPossibleMoves()
            #king
            self.king = board.board[5][1].getPiece()
            pieceMoves[self.king] = self.king.getPossibleMoves()
        else: #black pieces
            pawnIndex = 1
            while pawnIndex < 9:
                currentPawn = board.board[pawnIndex][7].getPiece()
                pieceMoves[currentPawn] = currentPawn.getPossibleMoves()
                self.allPossibleMoves = self.allPossibleMoves | currentPawn.getPossibleMoves()
                pawnIndex+=1
            #rooks
            rook = board.board[1][8].getPiece()
            pieceMoves[rook] = rook.getPossibleMoves()
            rook = board.board[8][8].getPiece()
            pieceMoves[rook] = rook.getPossibleMoves()
            #knights
            knight = board.board[2][8].getPiece()
            pieceMoves[knight] = knight.getPossibleMoves()
            knight = board.board[7][8].getPiece()
            pieceMoves[knight] = knight.getPossibleMoves()
            #Bishops
            bishop = board.board[3][8].getPiece()
            pieceMoves[bishop] = bishop.getPossibleMoves()
            bishop = board.board[6][8].getPiece()
            pieceMoves[bishop] = bishop.getPossibleMoves()
            #queen
            self.queen = board.board[4][8].getPiece()
            pieceMoves[self.queen] = self.queen.getPossibleMoves()
            #king
            self.king = board.board[5][8].getPiece()
            pieceMoves[self.king] = self.king.getPossibleMoves()

        return pieceMoves
    def updatePossibleMoves(self,board,piece):
        self.pieceMoves[piece] = piece.getPossibleMoves()
    def setAllPossibleMoves(self, moves):
        self.allPossibleMoves = moves
    def setPieceMoves(self, moves):
        self.pieceMoves = moves
    def getAllPossibleMoves(self): #TODO: remove tiles with self team pieces
        return self.allPossibleMoves
    def getPieceMoves(self): #dict piece --> set of possible moves
        return self.pieceMoves
    def updateAllPieceMoves(self,board):
        #goes through every piece in piece moves and gets their possible moves
        for piece in self.pieceMoves:
            if piece.isAlive() == True:
                self.pieceMoves[piece] = set()
                self.pieceMoves[piece] = piece.getPossibleMoves()
            else:
                del self.pieceMoves[piece]
                #or maybe delete
    def recalculateAllPossibleMoves(self,board):
        #recalcs every pieces move in updateAllPieceMNoves() and compiles into one set
        self.updateAllPieceMoves(board)
        self.allPossibleMoves = set()
        for piece in self.pieceMoves:
            self.allPossibleMoves = self.allPossibleMoves | self.pieceMoves[piece]
    def showPieces(self): #debugging tool prints piece -- > possible tiles it can move to
        for piece in self.pieceMoves:
            print(str(piece), " --> ", self.pieceMoves[piece])
    def getActivePieces(self):
        self.activePieces = set()
        for piece in self.pieceMoves:
            if piece.isAlive():
                self.activePieces.add(piece)
    def calculateAllPossibleAttacks(self):
        allPossibleAttacks = set()
        self.getActivePieces()
        for piece in self.activePieces:
            if piece.getName() == "Pawn":
                allPossibleAttacks = allPossibleAttacks | piece.getPossibleAttacks()
            else:
                allPossibleAttacks = allPossibleAttacks | piece.getPossibleMoves()
        self.allPossibleAttacks = allPossibleAttacks
        return self.allPossibleAttacks

    def turn(self,board):
        finishedMove = self.numMoves+1
        print(self.getTeam(),"'s Turn:")
        while self.numMoves < finishedMove:
            if self.isChecked == True:
                print(self.isCheckmate(board))
                if self.isCheckmate(board) == True:
                    print("Checkmate")

            #Gather inputs##
            start = " "
            end = " "
            #print("Castle Status:", self.king.canLongCastle(self,board), self.king.canShortCastle(self,board))
            while not self.game.checkInput(start) or not self.game.checkInput(end):
                print("Enter The tile of the piece to move")
                start = input()
                print("Enter the tile of where to move the piece")
                end = input()
                if not self.game.checkInput(start) or not self.game.checkInput(end):
                    print("Nonvalid input: try again. (Example input: e4)")
            #could add a really detailed move log later
            move=[start,end]

            tileMap = board.getTileMap()
            startTile = tileMap[start]
            endTile = tileMap[end]
            selectedPiece = startTile.getPiece()


            #IF CHECKED#########
            while self.isChecked == True: #TODO:test (light testing worked)
                #check if the move relieves check
                #print("checking clears check...",selectedPiece,self.clearsCheck([startTile,endTile],selectedPiece,board))
                if self.clearsCheck([startTile,endTile],selectedPiece,board) == True:
                    self.isChecked = False
                else:
                    print("Illegal Move: must resolve check")
                    print("Enter The tile of the piece to move")
                    start = input()
                    print("Enter the tile of where to move the piece")
                    end = input()
                    startTile = tileMap[start]
                    endTile = tileMap[end]
                    selectedPiece = startTile.getPiece()
            ##########################################

            move = [startTile, endTile]
            isPinned = selectedPiece.isPinned(self,move)
            if not isPinned and selectedPiece.move(endTile): #return false on a bad or illegal move
                #TODO:make sure the move made doesnt induce check
                piece = endTile.getPiece()
                self.recalculateAllPossibleMoves(board)
                self.opponent.recalculateAllPossibleMoves(board)
                self.isCheckingMove() 
                self.numMoves +=1
            else:
                if isPinned:
                    print("Illegal move:", selectedPiece, " is pinned.")
    def getName(self):
        return self.name
    def getTeam(self):
        return self.team
    def isChecked(self):
        #return true or false is players king is in check
        return self.isChecked
    def getTeam(self):
        return self.team
    def getKing(self):
        return self.king
    def getQueen(self):
        return self.queen
    def setOpponent(self, opponent):
        self.opponent = opponent
    def getOpponent(self):
        return self.opponent
    def isCheckingMove(self):
        opponentKing = self.getOpponent().getKing()
        kingTile = opponentKing.getTile()
        if kingTile in self.calculateAllPossibleAttacks():
            print(self.opponent.getName(), "is in check!")
            self.opponent.isChecked = True
        else:
            self.opponent.isChecked = False
    def clearsCheck(self,move,selectedPiece,board):
        start = move[0]
        end = move[1]
        king = self.getKing()
        endContents = end.getPiece()
        
        #simluate the move
        selectedPiece.setTile(end)
        start.setPiece(None)
        end.setPiece(selectedPiece)
 
        #recalculate the new possible moves
     
        self.opponent.calculateAllPossibleAttacks()
        opponentPossibleMovesPostMove = self.opponent.allPossibleAttacks


        if king.getTile() not in opponentPossibleMovesPostMove:
            #check resolved
            validMove = True
            selectedPiece.setTile(start)
            start.setPiece(selectedPiece)
            end.setPiece(endContents)
        else:
            #check not resolved
            validMove = False
            selectedPiece.setTile(start)
            start.setPiece(selectedPiece)
            end.setPiece(endContents)
        self.opponent.calculateAllPossibleAttacks()

        return validMove

    
    def isCheckmate(self,board):
        for piece in self.pieceMoves:
            startTile = piece.getTile()
            #need to update moves
            for move in self.pieceMoves[piece]:
                endTile = move
                moveList = [startTile, endTile]
                #print(startTile,endTile,self.clearsCheck(moveList,piece,board))
                if self.clearsCheck(moveList, piece, board) == True:
                    return False
        return True