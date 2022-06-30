import numpy as np

class GameState():
  def __init__(self):
    # b for black, w for white, -- for empty
    """
       ('w', 'w', 'w', 'w', 'w', 'w', 'w', 'w'),
      ('w', 'w', 'w', 'w', 'w', 'w', 'w', 'w')
    """
    self.board = np.array([
      ('b', 'b', 'b', 'b', 'b', 'b', 'b', 'b'),
      ('b', 'b', 'b', 'b', 'b', 'b', 'b', 'b'),
      ('--', '--', '--', '--', '--', '--', '--', '--'),
      ('--', '--', '--', '--', '--', '--', '--', '--'),
      ('--', '--', '--', '--', '--', '--', '--', '--'),
      ('--', '--', '--', '--', '--', '--', '--', '--'),
      ('w', 'w', 'w', 'w', 'w', 'w', 'w', 'w'),
      ('w', 'w', 'w', 'w', 'w', 'w', 'w', 'w'),
      ])
    self.whiteToMove = True
    self.movelog = []
    self.gameEnd = False
    
  # Takes a move and executes it
  def makeMove(self, move):
    self.board[move.startRow][move.startCol] = '--'
    self.board[move.endRow][move.endCol] = move.pieceMoved
    self.movelog.append(move) #display history
    self.whiteToMove = not self.whiteToMove #swap player

  # Undo the last move
  def undoMove(self):
    if len(self.movelog) != 0:
      move = self.movelog.pop()
      self.board[move.startRow][move.startCol] = move.pieceMoved
      self.board[move.endRow][move.endCol] = move.pieceCaptured
      self.whiteToMove = not self.whiteToMove
      self.gameEnd = False
  
  # All moves 
  def getValidMoves(self):
    moves = []
    for r in range(8):
      for c in range(8):
        piece = self.board[r][c][0]
        if (piece == 'w' and self.whiteToMove) or (piece == 'b' and not self.whiteToMove):
          self.getMoves(r, c, moves)
          #print(moves)
    return moves
    
  # Get all the moves for the piece located at r, c and add these moves to the list
  def getMoves(self, r, c, moves):
    if self.whiteToMove: #white moves
      if r-1 >= 0:
        if self.board[r-1][c] == "--": #1 square advance
          moves.append(Move((r, c), (r-1, c), self.board))
        if c-1 >= 0: #capture to left
          if self.board[r-1][c-1] != "w": #enemy piece to capture or valid move
            moves.append(Move((r, c), (r-1, c-1), self.board))
        if c+1 <= 7: #capture to right
          if self.board[r-1][c+1] != "w": #enemy piece to capture or valid move
            moves.append(Move((r, c), (r-1, c+1), self.board))
    else: #black moves
      if r+1 <= 7:
        if self.board[r+1][c] == "--": #1 square advance
          moves.append(Move((r, c), (r+1, c), self.board))
        if c-1 >= 0: #capture to left
          if self.board[r+1][c-1] != "b": #enemy piece to capture or valid move
            moves.append(Move((r, c), (r+1, c-1), self.board))
        if c+1 <= 7: #capture to right
          if self.board[r+1][c+1] != "b": #enemy piece to capture or valid move
            moves.append(Move((r, c), (r+1, c+1), self.board))
        
      
  
  #Check if there's winner
  def checkWinner(self):
    if self.whiteToMove:# Check black's state
      if 'w' not in self.board:
        self.gameEnd = True
        return
        
      blackAtEnd = False
      for r in range(8):
        for c in range(8):
          if self.board[r][c] == 'b' and r == 7:
            blackAtEnd = True
            break
         
      if blackAtEnd:
        self.gameEnd = True
    else:
      if 'b' not in self.board:
        self.gameEnd = True
        return
        
      whiteAtEnd = False
      for r in range(8):
        for c in range(8):
          if self.board[r][c] == 'w' and r == 0:
            whiteAtEnd = True
            break
          
      if whiteAtEnd:
        self.gameEnd = True
        
        
class Move():
  # maps keys to values
  # key : value
  ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
  rowsToRanks = {v: k for k, v in ranksToRows.items()}

  filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
  colsToFiles = {v: k for k, v in filesToCols.items()}
  
  def __init__(self, startSq, endSq, board):
    self.startRow = startSq[0]
    self.startCol = startSq[1]
    self.endRow = endSq[0]
    self.endCol = endSq[1]
    self.pieceMoved = board[self.startRow][self.startCol]
    self.pieceCaptured = board[self.endRow][self.endCol]
    self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
    #print(self.moveID)
  # Overriding the equals method
  def __eq__(self, other):
    if isinstance(other, Move):
      return self.moveID == other.moveID
    return False
  def getChessNotation(self):
    return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

  def getRankFile(self, r, c):
    return self.colsToFiles[c] + self.rowsToRanks[r]

  