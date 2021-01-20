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



gameRunning = True
while gameRunning:
    # m = wQueen.getPossibleMoves(board)
    # for i in m:
    #     print(i)
    board.printBoard()
    p1.turn(board)
    #p2.showPieces()
    # m = bQueen.getPossibleMoves(board)
    # for i in m:
    #     print(i)
    board.printBlackBoard()
    p2.turn(board)
    

