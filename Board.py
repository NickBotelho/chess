from Tile import Tile
from Pieces import *
class Board:
    tileMap = {} #tile string name (ex 'e4') --> tile object
    board=[None]
    players = {}
    def __init__(self):
        self.stitch()
        self.populatePieces()
        self.activePieces = self.setActivePieces()


    def stitch(self):
        cols = ['a','b','c','d','e','f','g','h']
        rows = [1,2,3,4,5,6,7,8]
        for col in cols:
            current = [None]
            for row in rows:
                tile = Tile(col,row)
                current.append(tile)

                tileName = col + str(row)
                self.tileMap[tileName] = tile

            self.board.append(current)

    def populatePieces(self):
        teams = ["white","black"]
        pawnRowStart = {
            "white":2,
            "black":7
        }
        for team in teams:
            numPawns = 1
            while numPawns <= 8:
                currentTile = self.board[numPawns][pawnRowStart[team]]
                currentTile.setPiece(Pawn(currentTile,team,self))
                numPawns+=1
        mainPieceStartRow = {
            "white":1,
            "black":8
        }
        for team in teams:
            #rooks
            currentTile = self.board[1][mainPieceStartRow[team]]
            currentTile.setPiece(Rook(currentTile,team,self))
            currentTile = self.board[8][mainPieceStartRow[team]]
            currentTile.setPiece(Rook(currentTile,team,self))
            #Knights
            currentTile = self.board[2][mainPieceStartRow[team]]
            currentTile.setPiece(Knight(currentTile,team,self))
            currentTile = self.board[7][mainPieceStartRow[team]]
            currentTile.setPiece(Knight(currentTile,team,self))
            #bishops
            currentTile = self.board[3][mainPieceStartRow[team]]
            currentTile.setPiece(Bishop(currentTile,team,self))
            currentTile = self.board[6][mainPieceStartRow[team]]
            currentTile.setPiece(Bishop(currentTile,team,self))
            #queen
            currentTile = self.board[4][mainPieceStartRow[team]]
            currentTile.setPiece(Queen(currentTile,team,self))
            #king
            currentTile = self.board[5][mainPieceStartRow[team]]
            currentTile.setPiece(King(currentTile,team,self))

    def printBoard(self):
        row = 8
        while row > 0:
            for index in range(1,len(self.board)):
                print(self.board[index][row],end='\t')
            row-=1
            print(" ")
        print("----------------------------------------")


    def printBlackBoard(self):
        row = 1
        while row < 9:
            for index in range(8,0,-1):
                print(self.board[index][row],end='\t')
            row+=1
            print(" ")
        print("----------------------------------------")

    def getTileMap(self):
        return self.tileMap

    def setBoard(self,player1,player2):
        player1.setOpponent(player2)
        player2.setOpponent(player1)
        if player1.getTeam().lower() == player2.getTeam().lower():
            print("Error:  cant have two players on same team")
            return 0
        if player1.getTeam().lower() == "white":
            self.players["white"] = player1
            self.players["black"] = player2
        else:
            self.players["white"] = player2
            self.players["black"] = player1
    def getPlayer(self, team):
        return self.players[team]

    def setActivePieces(self):
        row = 1
        pieces = set()
        while row < 9:
            for col in range(8,0,-1):
                if self.board[col][row].getPiece() != None:
                    pieces.add(self.board[col][row].getPiece())
            row+=1
        self.activePieces = pieces
        return self.activePieces

    def getActivePieces(self):
        return self.activePieces

    def isDraw(self,player):
        opponent = player.getOpponent()
        return len(player.getActivePieces()) == 1 and player.getKing().isAlive() and len(opponent.getActivePieces()) == 1 and opponent.getKing().isAlive()
