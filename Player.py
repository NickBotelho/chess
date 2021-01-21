import copy
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

        
    def calibrate(self,board): #ran in conjunction with reset/creation of a board
        pieceMoves = {}
        if self.team == "white":
            pawnIndex = 1
            while pawnIndex < 9:
                currentPawn = board.board[pawnIndex][2].getPiece()
                pieceMoves[currentPawn] = currentPawn.getPossibleMoves(board)
                self.allPossibleMoves = self.allPossibleMoves | currentPawn.getPossibleMoves(board)
                pawnIndex+=1
            #rooks
            rook = board.board[1][1].getPiece()
            pieceMoves[rook] = rook.getPossibleMoves(board)
            rook = board.board[8][1].getPiece()
            pieceMoves[rook] = rook.getPossibleMoves(board)
            #knights
            knight = board.board[2][1].getPiece()
            pieceMoves[knight] = knight.getPossibleMoves(board)
            knight = board.board[7][1].getPiece()
            pieceMoves[knight] = knight.getPossibleMoves(board)
            #Bishops
            bishop = board.board[3][1].getPiece()
            pieceMoves[bishop] = bishop.getPossibleMoves(board)
            bishop = board.board[6][1].getPiece()
            pieceMoves[bishop] = bishop.getPossibleMoves(board)
            #queen
            queen = board.board[4][1].getPiece()
            pieceMoves[queen] = queen.getPossibleMoves(board)
            #king
            self.king = board.board[5][1].getPiece()
            pieceMoves[self.king] = self.king.getPossibleMoves(board)
        else: #black pieces
            pawnIndex = 1
            while pawnIndex < 9:
                currentPawn = board.board[pawnIndex][7].getPiece()
                pieceMoves[currentPawn] = currentPawn.getPossibleMoves(board)
                self.allPossibleMoves = self.allPossibleMoves | currentPawn.getPossibleMoves(board)
                pawnIndex+=1
            #rooks
            rook = board.board[1][8].getPiece()
            pieceMoves[rook] = rook.getPossibleMoves(board)
            rook = board.board[8][8].getPiece()
            pieceMoves[rook] = rook.getPossibleMoves(board)
            #knights
            knight = board.board[2][8].getPiece()
            pieceMoves[knight] = knight.getPossibleMoves(board)
            knight = board.board[7][8].getPiece()
            pieceMoves[knight] = knight.getPossibleMoves(board)
            #Bishops
            bishop = board.board[3][8].getPiece()
            pieceMoves[bishop] = bishop.getPossibleMoves(board)
            bishop = board.board[6][8].getPiece()
            pieceMoves[bishop] = bishop.getPossibleMoves(board)
            #queen
            self.queen = board.board[4][8].getPiece()
            pieceMoves[self.queen] = self.queen.getPossibleMoves(board)
            #king
            self.king = board.board[5][8].getPiece()
            pieceMoves[self.king] = self.king.getPossibleMoves(board)

        return pieceMoves
    def updatePossibleMoves(self,board,piece):
        self.pieceMoves[piece] = piece.getPossibleMoves(board)

    def getAllPossibleMoves(self): #TODO: remove tiles with self team pieces
        res = set()
        for piece in self.pieceMoves:
            res = res | self.pieceMoves[piece]
        return res
    def getPieceMoves(self): #dict piece --> set of possible moves
        return self.pieceMoves
    def showPieces(self): #debugging tool prints piece -- > possible tiles it can move to
        for piece in self.pieceMoves:
            print(str(piece), " --> ", self.pieceMoves[piece])

    def turn(self,board):
        finishedMove = self.numMoves+1
        while self.numMoves < finishedMove:
            if self.isChecked == True:
                print(self.isCheckmate(board))
                if self.isCheckmate(board) == True:
                    print("Checkmate")
            print("Enter The tile of the piece to move")
            start = input()
            print("Enter the tile of where to move the piece")
            end = input()
            #could add a really detailed move log later
            move=[start,end]
            tileMap = board.getTileMap()
            startTile = tileMap[start]
            endTile = tileMap[end]
            selectedPiece = startTile.getPiece()


            while self.isChecked == True: #TODO:test (light testing worked)
                #check if the move relieves check
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
            if selectedPiece.move(endTile,board): #return false on a bad or illegal move
                #TODO:make sure the move made doesnt induce check
                piece = endTile.getPiece()
                self.updatePossibleMoves(board,piece)
                self.isCheckingMove() 
                self.numMoves +=1
    def getName(self):
        return self.name
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
        if kingTile in self.getAllPossibleMoves():
            print(self.opponent.getName(), "is in check!")
            self.opponent.isChecked = True
        else:
            self.opponent.isChecked = False
    def clearsCheck(self,move,selectedPiece,board):
        start = move[0]
        end = move[1]
        originalRow = selectedPiece.getRow()
        originalCol = selectedPiece.getColNumber()
        #simluate the move
        selectedPiece.setTile(end)
        start.setPiece(None)
        end.setPiece(selectedPiece)
        opponentPossibleMovesPostMove = self.opponent.recalculateAllPossibleMoves(board)       
        # print("king tile", self.king.getTile(), "|", self.king.getTile() in opponentPossibleMovesPostMove)
        # for i in opponentPossibleMovesPostMove:#the set hold references to the tiles. so changing tile changes content of set
        #     print("updated possible moves", i)

        if self.king.getTile() not in opponentPossibleMovesPostMove:
            #check resolved
            validMove = True
            selectedPiece.setTile(start)
            start.setPiece(selectedPiece)
            end.setPiece(None)

        else:
            #check not resolved
            validMove = False
            selectedPiece.setTile(start)
            start.setPiece(selectedPiece)
            end.setPiece(None)
        return validMove

    def recalculateAllPossibleMoves(self,board):
        allMoves = set()
        for piece in self.pieceMoves:
            allMoves = allMoves | piece.getPossibleMoves(board)
        return allMoves
    def isCheckmate(self,board):
        for piece in self.pieceMoves:
            startTile = piece.getTile()
            for move in self.pieceMoves[piece]:
                endTile = move
                moveList = [startTile, endTile]
                print(startTile,endTile,piece,self.clearsCheck(moveList,piece,board))
                if self.clearsCheck(moveList, piece, board) == True:
                    return False
        return True