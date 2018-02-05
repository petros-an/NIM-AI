class move:
    def __init__(self, row, start, end):
        self.row = row
        self.start = start
        self. end = end
    def prnt(self):
        print(self.row, self.start, self.end)
class Board:
    def __init__(self, rowsN):
        self.rows = [];
        self.size = rowsN
        for i in range(0,rowsN):
            self.rows.append([1 for k in range(0,i+1)])
    def erase(self, move):
        if not self.legalMove(move):
            return False
        for i in range(move.start,move.end+1):
            self.rows[move.row][i] = 0
    def makeState(self,move):
        import copy
        stateBoard = copy.deepcopy(self)
        stateBoard.erase(move)
        return stateBoard
    def gameOver(self):
        for i in range(0,self.size):
            for j in range(0, i+1):
                if self.rows[i][j] == 1:
                    return False
        return True
    def legalMove(self, move):
        r = move.row
        s = move.start
        e = move.end
        if s < 0 or e > r or r > self.size:
            return False
        for i in range(s,e+1):
            if self.rows[r][i] == 0:
                return False
        return True
    def getAvailableMoves(self):
        moves = []
        for row in range(0,self.size):
            for start in range(0,row+1):
                for end in range(start,row+1):
                    moves.append(move(row,start,end))
        return moves
    def getLegalMoves(self):
        availableMoves = self.getAvailableMoves()
        return [m for m in availableMoves if self.legalMove(m)]
    def prnt(self):
        for i in range(0,self.size):
            print([k for k in self.rows[i]])
    def hashable(self, player):
        s = ""
        for i in range(0,self.size):
            for j in range(0,i+1):
                s = s + str(self.rows[i][j])
        s = s + str(player)
        return s

def correctInpFormat():
    return True


def askForMode():
    print("Type 1 to play against a human, 2 for AI, 0 to exit")
    while True:
        inp = input()
        print(inp)
        if inp in [1, 2, 0]:
            break
        else:
            print("input not understood")
    return inp

class Game:
    def __init__(self, mode):
        self.mode = mode
        self.currentPlayer = 0
        print("Enter size")
        size = input()
        self.board = Board(size)
    def play(self):

        while(True):
            print("Player: " + str(self.currentPlayer))
            self.board.prnt()
            mv = self.readMove()
            self.board.erase(mv)
            if (self.board.gameOver()):
                self.end()
                break;
            self.currentPlayer = (self.currentPlayer + 1) % 2

            print("Player: " + str(self.currentPlayer))
            self.board.prnt()
            if(self.mode == 1):
                mv2 = self.readMove()
            else:
                mv2 = self.generateMove()
                #print("printing move")
                #mv2.prnt()
            self.board.erase(mv2)
            if (self.board.gameOver()):
                self.end()
                break;
            self.currentPlayer = (self.currentPlayer + 1) % 2
    def gameOver(self):
        return self.board.gameOver()
    def end(self):
        self.board.prnt()
        print("Game over: " + str(self.otherPlayer(self.currentPlayer)) + " wins")
    def otherPlayer(self,currentPlayer):
        return (self.currentPlayer + 1) % 2
    def readMove(self):
        print("Enter move: row, start, end")
        while True:
            r = input();
            s = input();
            e = input();
            m = move(r,s,e)
            if self.board.legalMove(m):
                return m
            else:
                print("Move not understood or illegal")
    def generateMove(self):
        #x = self.minmax(self.currentPlayer, self.board)[0]
        x = self.minmaxAB(self.currentPlayer, self.board, -10000000, 10000000)[0]
        #print(Bank)
        return x
    def minmax(self, player, state):
        global Bank
        if state.gameOver():
            #print("goal state")
            winner = player
            if winner == 0:
                #print("0 wins")
                return [None, 10]
            else:
                #print("1 wins")
                return [None, 0]
        legalMoves = state.getLegalMoves()
        states = [state.makeState(m) for m in legalMoves]
        if len(legalMoves) == 0:
            print("AAAAAAAA")
        if player == 0: #max
            candidates = []
            for i in range(0,len(legalMoves)):
                key = states[i].hashable(player)
                if key in Bank:
                    #print("AHA!")
                    candidates.append(Bank.get(key))
                else:
                    x = self.minmax(1, states[i])
                    candidates.append(x)
                    Bank[key] = x


            #find best candidate
            [best, bestscore] = candidates[0]
            for i in range(0,len(candidates)):
                if candidates[i][1] >= bestscore:
                    [best,bestscore] = [legalMoves[i],candidates[i][1]]
            #print bestscore
            return [best, bestscore]

        elif player == 1: #min
            candidates = []
            for i in range(0, len(legalMoves)):
                key = states[i].hashable(player)
                if key in Bank:
                    #print("AHA!")
                    candidates.append(Bank.get(key))
                else:
                    x = self.minmax(0, states[i])
                    candidates.append(x)
                    Bank[key] = x
            # find best candidate
            [best, bestscore] = candidates[0]
            for i in range(0, len(candidates)):
                if candidates[i][1] <= bestscore:
                    [best, bestscore] = [legalMoves[i], candidates[i][1]]
            print bestscore

            return [best, bestscore]

    def minmaxAB(self, player, state, a, b):
        global Bank
        if state.gameOver():
            #print("goal state")
            winner = player
            if winner == 0:
                return [None, 10]
            else:
                return [None, 0]
        legalMoves = state.getLegalMoves()
        states = [state.makeState(m) for m in legalMoves]
        if player == 0: #max
            candidates = []
            [best,bestscore] = [None,-100000]
            for i in range(0,len(legalMoves)):
                key = states[i].hashable(player)
                x = None
                if key in Bank:
                    #print("AHA!")
                    x = Bank.get(key)
                    candidates.append(x)
                else:
                    x = self.minmaxAB(1, states[i],a,b)
                    candidates.append(x)
                    Bank[key] = x
                if bestscore <= x[1]:
                    [best,bestscore] = [legalMoves[i],x[1]]
                if bestscore > b:
                    print("chop")
                    return [best,bestscore]
                a = max(a,bestscore)
            return [best, bestscore]
        elif player == 1: #min
            candidates = []
            [best, bestscore] = [None, 100000]
            for i in range(0, len(legalMoves)):
                key = states[i].hashable(player)
                x = None
                if key in Bank:
                    # print("AHA!")
                    x = Bank.get(key)
                    candidates.append(x)
                else:
                    x = self.minmaxAB(0, states[i], a, b)
                    candidates.append(x)
                    Bank[key] = x
                if bestscore >= x[1]:
                    [best, bestscore] = [legalMoves[i],x[1]]
                if bestscore < a:
                    print("chop")
                    return [best, bestscore]
                b = min(b, bestscore)
            return [best, bestscore]
#'''
Bank = {}
while True:
    mode = askForMode()
    if mode == 0:
        break
    G = Game(mode)
    G.play()
'''
b = Board(3)
b.erase(move(0,0,0))
b.erase(move(1,0,1))
b.erase(move(2,0,1))
b.prnt()
print(b.hashable())
'''
