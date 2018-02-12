import os
class move:
    def __init__(self, row, start, end):
        self.row = row
        self.start = start
        self. end = end
    def prnt(self):
        print(self.row, self.start, self.end)
    def tostr(self):
        s = str(self.row) + str(self.start) + str(self.end)
        return s


#state + player -> statehash
#statehash -> move
#move ->decoder(move, current state, state) -> current move

class Board:
    def __init__(self, rowsN):
        self.rows = [];
        self.size = rowsN
        self.count = rowsN * (rowsN - 1) / 2
        for i in range(0,rowsN):
            self.rows.append([1 for k in range(0,i+1)])
    def erase(self, move):
        if not self.legalMove(move):
            return False
        for i in range(move.start,move.end+1):
            self.rows[move.row][i] = 0
            self.count = self.count - 1
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
        import random
        random.shuffle(moves)
        return moves
    def getLegalMoves(self):
        availableMoves = self.getAvailableMoves()
        return [m for m in availableMoves if self.legalMove(m)]
    def prnt(self):
        for i in range(0,self.size):
            print([k for k in self.rows[i]])
    def hashable(self, player):
        #self.prnt()
        rows2 = self.rows
        #rows2.reverse()
        while True:

            all0 = True
            rowIndex = len(rows2)-1
            #print(rowIndex)
            for i in range(0,rowIndex+1):
                if rows2[rowIndex][i] == 1:
                    all0 = False
            if all0 :
                rows2 = rows2[:rowIndex]
                if len(rows2) == 0:
                    break
            else:
                #print("lsoop")
                break
        s = ""
        for i in range(0,len(rows2)):
            for j in range(0,i+1):
                s = s + str(rows2[i][j])
        s = s + str(player)
        return s
    def countUnits(self,B):
        count = 0

        for i in range(0, B.size):
            for j in range(0, i + 1):
                isUnit = False
                if B.rows[i][j] == 1:
                    if j > 0 and j < i:
                        if B.rows[i][j - 1] == 0 and B.rows[i][j + 1] == 0:
                            isUnit = True
                    elif j == 0:
                        if i == 0 or B.rows[i][j + 1] == 0:
                            isUnit = True
                    elif j == i:
                        if B.rows[i][j - 1] == 0:
                            isUnit = True
                if isUnit:
                    # print("a",i,j)
                    count = count + 1
        return count
    def hashable2(self,player):
        #make list of isolated units
        unitList = self.splitUnits()
        unitList.sort(key=len)
        s = ""
        for i in range(0,len(unitList)):
            for j in range(0,len(unitList[i])):
                s = s + str(unitList[i][j])
            s = s + "#"
        s = s + "@" + str(player)
        return s
    def recover(self,mv,state):
        '''
        #get unit number of move in state
        for i in range(0,len(state.rows)):
            inUnit = False
            unitCount = 0
            for j in range(0,i+1):
                if state.rows[i][j] == 1:
                    if inUnit is False:
                        unitCount = unitCount + 1
                    inUnit = True
                elif state.rows[i][j] == 0:
                    inUnit = False
                if move.row == i and move.start == j:
                    brk = True
                    break
            if brk:
                 break
        offset = move.end - move.start
        #find corresponding unit number of self
        r=None
        s=None
        e=None
        for i in range(0,len(self.rows)):
            inUnit = False
            unitCount1 = 0
            for j in range(0,i+1):
                if self.rows[i][j] == 1:
                    if inUnit is False:
                        unitCount1 = unitCount1 + 1
                    inUnit = True
                elif self.rows[i][j] == 0:
                    inUnit = False
                if unitCount1 == unitCount:
                    r = i
                    s = j
                    e = j + offset
                    return move(r,s,e)
        '''

        #find length of unit of move in state
        info = state.getMoveInfo(mv)
        unitLength = info[0]

        #play corresponding move in unit of same length in self
        [row,start] = self.getUnitWithLength(unitLength)
        return move(row,start + info[1], start + (mv.end-mv.start))
    def getUnitWithLength(self,length):
        for i in range(0,self.size):
            isUnit = False
            l = 0
            start = 0
            for j in range(0,i+1):
                if self.rows[i][j] == 1:
                    l = l + 1
                    if not isUnit:
                        start = j
                    isUnit = True

                else:
                    if l == length and isUnit:
                        row = i
                        return [i,start]
                    l = 0
                    isUnit = False
                if l == length and isUnit:
                    row = i
                    return [i, start]
    def getMoveInfo(self, move):
        i = move.row
        j = move.start
        k = move.end
        while True:
            if j==0 or self.rows[i][j-1] == 0:
                break
            else:
                j = j - 1
        while True:
            if k==i or self.rows[i][k+1] == 0:
                break
            else:
                k = k + 1
        return [(k-j+1), move.start - j]
    def splitUnits(self):
        unitList = []
        for i in range(0, self.size):
            unit = []
            for j in range(0, i + 1):
                x = self.rows[i][j]
                if x == 0:
                    if unit != []:
                        unitList.append(unit)
                        unit = []
                elif x == 1:
                    unit.append(x)
            if unit != []:
                unitList.append(unit)
        return unitList

class Game:
    def __init__(self, mode):
        self.mode = mode
        self.currentPlayer = 0
        self.Bank = loadBank()
        self.moveCount = 0
        print("Enter size (might be too slow for >5 )")
        while True:
            size = input()
            if size > 2:
                break
            else:
                print("Size must be more than 2")
        self.board = Board(size)
    def play(self):

        while(True):
            self.moveCount = self.moveCount + 1
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
                print("Generating move...")
                mv2 = self.generateMove()
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
        storeBank(self.Bank)
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
        #print(self.Bank)
        x = self.minmaxAB2(self.currentPlayer, self.board, -1000000,100000 )
        print("Generated move")
        return x[0]
    def minmax(self, player, state):
        Bank = self.Bank
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
    def minmaxAB2(self, player, state, a, b):

        if state.gameOver():
            # print("goal state")
            winner = player
            if winner == 0:
                # print("0 wins")
                return [None, 10]
            else:
                # print("1 wins")
                return [None, 0]
        legalMoves = state.getLegalMoves()
        states = [state.makeState(m) for m in legalMoves]
        if player == 0:  # max
            candidates = []
            [best,bestscore] = [None, -100000]
            for i in range(0, len(legalMoves)):
                key = states[i].hashable2(player)
                x = None
                if key in self.Bank:
                    # print("AHA!")
                    x = self.Bank.get(key)
                    candidates.append(x)
                else:
                    x = self.minmaxAB2(1, states[i],a,b)
                    candidates.append(x)
                    self.Bank[key] = x
                if x[1] >= bestscore:
                    [best, bestscore] = [legalMoves[i], x[1]]

                #ab part
                if bestscore > b:
                    return [best,bestscore]
                a = max(a,bestscore)

            return [best, bestscore]

        elif player == 1:  # min
            candidates = []
            [best,bestscore] = [None,100000]
            for i in range(0, len(legalMoves)):
                key = states[i].hashable2(player)
                x = None
                if key in self.Bank:
                    # print("AHA!")
                    x = self.Bank.get(key)[0:2]
                    candidates.append(x)
                else:
                    x = self.minmaxAB2(0, states[i],a,b)
                    candidates.append(x)
                    self.Bank[key] = x + [states[i]]
                if x[1] < bestscore:
                    [best, bestscore] = [legalMoves[i], x[1]]

                #ab part
                if bestscore < a:
                    return [best, bestscore]
                b = min(bestscore, b)
            return [best, bestscore]

class App:
    def programExit(self):
        print("exiting")
        exit()
    def run(self):
        while True:
            mode = self.askForMode()
            if mode == 0:
                self.programExit()
            G = Game(mode)
            G.play()
    def askForMode(self):
        print("Type 1 to play against a human, 2 for AI, 0 to exit")
        while True:
            inp = input()
            print(inp)
            if inp in [1, 2, 0]:
                break
            else:
                print("input not understood")
        return inp

def storeBank(Bank):
    print("storing")
    if os.path.isfile("data") and os.path.getsize("data") > 0:
        os.remove("data")
    file = open("data", "w+")
    for i in Bank:
        x = Bank.get(i)
        move = None
        if x[0] is None:
            move = "None"
        else:
            move = x[0].tostr()

        file.write(i + "?" + move + "$" + str(x[1]) + "\n")
    file.close()
def loadBank():
    print("loading")
    B = {}
    if not (os.path.isfile("data") and os.path.getsize("data") > 0):
        return {}
    file = open("data", "r")
    text = file.read()
    text = text.splitlines()
    for i in text:
        addEntry(B,i)
    #print B
    return B
def addEntry(B,i):
    index1 = i.find("?")
    statehash = i[:index1]

    index2 = i.find("$")

    movestr = i[(index1+1):index2]
    if movestr == "None":
        mv = None
    else:
        row = int(movestr[0])
        start = int(movestr[1])
        end = int(movestr[2])
        mv = move(row,start,end)
    score = int(i[index2+1:])
    B[statehash] = [mv,score]

'''
b = Board(5)
b.erase(move(0,0,0))
b.erase(move(1,0,1))
b.erase(move(2,0,2))
b.erase(move(3,2,3))
b.erase(move(4,0,2))
b.prnt()
#print(b.hashable2(0))
print(".........")
B = Board(3)
B.erase(move(0,0,0))
B.erase(move(2,0,0))
#B.erase(move(2,2,2))
B.prnt()
#print(b.hashable2(0))
#
x = B.recover(move(4,3,4),b)
print(x.row,x.start,x.end)
#print(B.getStartOfUnitWithLength(1))
'''
#print(os.getcwd())
A = App()
A.run()
#addEntry({}, "1000001?000$0")
#'''