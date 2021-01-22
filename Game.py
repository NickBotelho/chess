class Game():
    def __init__(self):
        self = self
        self.cols = {'a','b','c','d','e','f','g','h'}
        self.rows = {'1','2','3','4','5','6','7','8'}

    def checkInput(self,move):
        return type(move) == str and len(move) == 2 and move[0] in self.cols and move[1] in self.rows
