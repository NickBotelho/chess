from Board import Board
from Pieces import Pawn
from Player import Player

board = Board()
tileMap = board.getTileMap()

p1 = Player("white", "Player 1",board)
p2 = Player("black", "Player 2",board)
board.setBoard(p1,p2)

wQueen = tileMap['d1'].getPiece()
bQueen = tileMap['d8'].getPiece()
bQueen = tileMap['d8']


turns = 1
gameRunning = True
while gameRunning:
    print("Turn:",turns)
    print("p1 active pieces",p1.getStringListOfActivePieces())
    board.printBoard()
    p1.computerTurn(board)
    
    print("p2 active pieces",p2.getStringListOfActivePieces())
    board.printBoard()
    p2.computerTurn(board)
    turns+=1


