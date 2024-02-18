class Player:
    """Base player class"""
    def __init__(self, symbol):
        self.symbol = symbol

    def get_symbol(self):
        return self.symbol
    
    def get_move(self, board):
        raise NotImplementedError()



class HumanPlayer(Player):
    """Human subclass with text input in command line"""
    def __init__(self, symbol):
        Player.__init__(self, symbol)
        self.total_nodes_seen = 0

    def clone(self):
        return HumanPlayer(self.symbol)
        
    def get_move(self, board):
        col = int(input("Enter col:"))
        row = int(input("Enter row:"))
        return  (col, row)


class AlphaBetaPlayer(Player):
    """Class for Alphabeta AI: implement functions minimax, eval_board, get_successors, get_move
    eval_type: int
        0 for H0, 1 for H1, 2 for H2
    prune: bool
        1 for alpha-beta, 0 otherwise
    max_depth: one move makes the depth of a position to 1, search should not exceed depth
    total_nodes_seen: used to keep track of the number of nodes the algorithm has seearched through
    symbol: X for player 1 and O for player 2
    """
    def __init__(self, symbol, eval_type, prune, max_depth):
        Player.__init__(self, symbol)
        self.eval_type = eval_type
        self.prune = prune
        self.max_depth = int(max_depth) 
        self.max_depth_seen = 0
        self.total_nodes_seen = 0
        if symbol == 'X':
            self.oppSym = 'O'
        else:
            self.oppSym = 'X'


    def terminal_state(self, board):
        # If either player can make a move, it's not a terminal state
        for c in range(board.cols):
            for r in range(board.rows):
                if board.is_legal_move(c, r, "X") or board.is_legal_move(c, r, "O"):
                    return False 
        return True 


    def terminal_value(self, board):
        # Regardless of X or O, a win is float('inf')
        state = board.count_score(self.symbol) - board.count_score(self.oppSym)
        if state == 0:
            return 0
        elif state > 0:
            return float('inf')
        else:
            return -float('inf')


    def flip_symbol(self, symbol):
        # Short function to flip a symbol
        if symbol == "X":
            return "O"
        else:
            return "X"
    
    def getmaxBoard(self, board, a, b):
        #a modified max value designed to return the board
        #makes getting the move easier
        #and I can still get the value
        if self.terminal_state(board) == True:
            return board
        board.children = self.get_successors(board,self.symbol)
        if len(board.children) == 0:
            return board
        maxBoard = None
        maxValue = float('-inf')
        for child in board.children:
            minChild = self.getminBoard(child, a, b)
            if minChild.value > maxValue:
                maxBoard = minChild
                maxValue = minChild.value
            if maxValue > b:
                return maxBoard
            a = max(a, maxValue)
        return maxBoard
    
    def getminBoard(self, board, a, b):
        #a modified min value designed to return the board
        #makes getting the move easier
        #and I can still get the value
        if self.terminal_state(board) == True:
            return board
        board.children = self.get_successors(board,self.oppSym)
        if len(board.children) == 0:
            return board
        minBoard = None
        minValue = float('inf')
        for child in board.children:
            child.children = self.get_successors(child, self.symbol)
            maxChild = self.getmaxBoard(child, a, b)
            if maxChild.value < minValue:
                minBoard = maxChild
            if minValue < a:
                return minBoard
            b = min(b, minValue)
        return minBoard

    def alphabeta(self, board):
        # Write minimax function here using eval_board and get_successors
        # type:(board) -> (int, int)
        if board.value == None:
            board.value = self.eval_board(board)
        maxBoard = self.getmaxBoard(board, float('-inf'), float('inf'))
        board.value = maxBoard.value
        return maxBoard.move

    def eval_board(self, board):
        # Write eval function here
        # type:(board) -> (float)
        value = 0
        if self.eval_type == 0:
            value = board.count_score(self.symbol) - board.count_score(self.oppSym)
        elif self.eval_type == 1:
            value = 0
            for c in range (0, self.cols):
                for r in range(0, self.rows):
                    if board.is_cell_empty(c, r) and board.is_legal_move(c, r, self.symbol):
                        value += 1
            return value
        elif self.eval_type == 2:
            value = 2
        return value


    def get_successors(self, board, player_symbol):
        # Write function that takes the current state and generates all successors obtained by legal moves
        # type:(board, player_symbol) -> (list)
        successors = []
        for c in range (0, board.cols):
            for r in range (0, board.rows):
                if board.is_cell_empty(c, r) and board.is_legal_move(c, r, player_symbol):
                    possible_successor = board.cloneOBoard()
                    possible_successor.move = (c, r)
                    possible_successor.value = self.eval_board(possible_successor)
                    possible_successor.play_move(c, r, player_symbol)
                    successors.append(possible_successor)
        return successors 


    def get_move(self, board):
        # Write function that returns a move (column, row) here using minimax
        # type:(board) -> (int, int)
        return self.alphabeta(board)
