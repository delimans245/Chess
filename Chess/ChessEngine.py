

#This class is responsible for storing all the information about the current state of the chess game, 
#it will also be responsible for determining the valid moves at the current state. It will also keep a move log.


class GameState():
    def __init__(self):
        #board is an 8x8 2d list, each element of the list has 2 characters.
        #The frst character represents the color of the piece, 'b', or 'w'
        #The second chraacter represents the type of the piece, 'K' 'Q', 'B', 'N', 'R'
        #"--" represents an empty space with no piece
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
        ]
        #make all functions

        self.moveFunctions = {'p':self.getPawnMoves, 'R':self.getRookMoves, 'Q':self.getQueenMoves, 'B':self.getBishopMoves, 'N':self.getNightMoves, 'K':self.getKingMoves}
        self.whiteToMove = True
        self.moveLog =[]
    
    '''
    Takes in a move as a parameter and executes it (this will not work for castling, pawn promotion and en-passant)
    '''
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) #log moves
        self.whiteToMove = not self.whiteToMove #swap players

    '''
    Undo the last move made
    '''
    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove
    
    '''
    All moves considering checks
    '''
    def getValidMoves(self):
        return self.getAllPossibleMoves()

    '''
    All moves without considering checks
    '''
    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):  # number of rows
            for c in range(len(self.board[r])):  # number of columns in given row
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    # Call the appropriate move function based on the piece
                    if piece == 'p':
                        self.getPawnMoves(r, c, moves)
                    elif piece == 'R':
                        self.getRookMoves(r, c, moves)
                    elif piece == 'B':
                        self.getBishopMoves(r, c, moves)
                    elif piece == 'N':
                        self.getNightMoves(r, c, moves)
                    elif piece == 'Q':
                        self.getQueenMoves(r, c, moves)
                    elif piece == 'K':
                        self.getKingMoves(r, c, moves)
        return moves

    
    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove:
            if self.board[r - 1][c] == "--":
                moves.append(Move((r, c), (r -1, c), self.board))
                if r == 6 and self.board[r-2][c] == "--":
                    moves.append(Move((r, c), (r-2, c), self.board))
            
            if c-1 >= 0:
                if self.board[r - 1][c - 1][0] == 'b':
                    moves.append(Move((r, c), (r-1, c-1), self.board))
            
            if c+1 <= 7:
                if self.board[r - 1][c + 1][0] == 'b':
                    moves.append(Move((r, c), (r-1, c+1), self.board))
            
        if not self.whiteToMove:
            if self.board[r+1][c] == "--":
                moves.append(Move((r, c), (r +1, c), self.board))
                if r == 1 and self.board[r+2][c] == "--":
                    moves.append(Move((r, c), (r+2, c), self.board))
            
            if c-1 >= 0:
                if self.board[r + 1][c - 1][0] == 'w':
                    moves.append(Move((r, c), (r+1, c-1), self.board))
            
            if c+1 <= 7:
                if self.board[r + 1][c + 1][0] == 'w':
                    moves.append(Move((r, c), (r+1, c+1), self.board))
        
    def getRookMoves(self, r, c, moves):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
        enemy_color = 'b' if self.whiteToMove else 'w'
        for d in directions:
            for i in range(1, 8):  # Max distance is 7 squares
                end_row = r + d[0] * i
                end_col = c + d[1] * i
                if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                    end_piece = self.board[end_row][end_col]
                    if end_piece == "--":  # Empty square
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                    elif end_piece[0] == enemy_color:  # Enemy piece
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                        break
                    else:  # Friendly piece
                        break
                else:
                    break

    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)  # Rook-like moves
        self.getBishopMoves(r, c, moves)  # Bishop-like moves

    def getBishopMoves(self, r, c, moves):
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # Diagonals
        enemy_color = 'b' if self.whiteToMove else 'w'

        for d in directions:
            for i in range(1, 8):  # Max distance is 7 squares
                end_row = r + d[0] * i
                end_col = c + d[1] * i
                if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                    end_piece = self.board[end_row][end_col]
                    if end_piece == "--":  # Empty square
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                    elif end_piece[0] == enemy_color:  # Enemy piece
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                        break
                    else:  # Friendly piece
                        break
                else:
                    break


    def getNightMoves(self, r, c, moves):
        knight_moves = [
            (-2, -1), (-2, 1), (2, -1), (2, 1), 
            (-1, -2), (-1, 2), (1, -2), (1, 2)
        ]
        ally_color = 'w' if self.whiteToMove else 'b'
        
        for m in knight_moves:
            end_row = r + m[0]
            end_col = c + m[1]
            if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                end_piece = self.board[end_row][end_col]
                if end_piece == "--" or end_piece[0] != ally_color:  # Empty or enemy
                    moves.append(Move((r, c), (end_row, end_col), self.board))


    def getKingMoves(self, r, c, moves):
        king_moves = [
            (-1, 0), (1, 0), (0, -1), (0, 1), 
            (-1, -1), (-1, 1), (1, -1), (1, 1)
        ]
        ally_color = 'w' if self.whiteToMove else 'b'

        for m in king_moves:
            end_row = r + m[0]
            end_col = c + m[1]
            if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                end_piece = self.board[end_row][end_col]
                if end_piece == "--" or end_piece[0] != ally_color:  # Empty or enemy
                    moves.append(Move((r, c), (end_row, end_col), self.board))


class Move():
    ranksToRows = {
        "1": 7, "2": 6, "3": 5, "4": 4, 
        "5": 3, "6": 2, "7": 1, "8": 0
    }

    rowsToRanks = {v: k for k, v in ranksToRows.items()}

    filesToCols = {
        "a": 0, "b" : 1, "c" : 2, "d" : 3, 
        "e": 4, "f" : 5, "g" : 6, "h" : 7
    }

    colsToFiles = {v: k for k, v in filesToCols.items()}



    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
        print(self.moveID)

    '''
    Overriding the equls method
    '''

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False
    
    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]

    








