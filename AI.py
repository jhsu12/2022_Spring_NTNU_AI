import random

pieceScore = {"w": 1, "b": 1}
Win = 2000
DEPTH = 4
"""
Picks and returns a random move
"""
def findRandomMove(validMoves):
  if len(validMoves) == 0:
    return None
  return validMoves[random.randint(0, len(validMoves) - 1)]


"""
Find the best move based on the material alone

def findMoveMinMaxNoRecursion(gs, validMoves):
  turnMultipler = 1 if gs.whiteToMove else -1
  opponentMinMaxScore = 1000
  bestPlayerMove = None
  random.shuffle(validMoves)
  for playerMove in validMoves:
    gs.makeMove(playerMove)
    opponentsMoves = gs.getValidMoves()
    opponentMaxScore = -1000
    
    for opponentsMove in opponentsMoves:
      gs.makeMove(opponentsMove)
      # probably needs other method to evaluate board
      score = turnMultipler * scoreMaterial(gs.board)
      if score > opponentMaxScore:
        opponentMaxScore = score
      gs.undoMove()
      
    if opponentMaxScore < opponentMinMaxScore:
      bestPlayerMove = playerMove
    gs.undoMove()
  return bestPlayerMove
"""


"""
Helper method to make the first recursive call
"""
def findBestMove(gs, validMoves):
  global nextMove, counter
  nextMove = None
  random.shuffle(validMoves)
  counter = 0
  #findMoveNegaMax(gs, validMoves, DEPTH, 1 if gs.whiteToMove else -1)
  #findMoveMinMax(gs, validMoves, DEPTH, gs.whiteToMove)
  findMoveNegaMaxAlphaBeta(gs, validMoves, DEPTH, -Win, Win, 1 if gs.whiteToMove else -1)
  #print(counter)
  return nextMove
  
def findMoveMinMax(gs, validMoves, depth, whiteToMove):
  global nextMove, counter
  counter += 1
  if depth == 0:
    return scoreBoard(gs)
  
  if gs.whiteToMove:
    maxScore = -Win
    for move in validMoves:
      gs.makeMove(move)
      nextMoves = gs.getValidMoves()
      score = findMoveMinMax(gs, nextMoves, depth-1, False)
      if score > maxScore:
        maxScore = score
        if depth == DEPTH:
          nextMove = move
      gs.undoMove()
    return maxScore
    
  else:
      minScore = Win
      for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = findMoveMinMax(gs, nextMoves, depth-1, True)
        if score < minScore:
          minScore = score
          if depth == DEPTH:
            nextMove = move
        gs.undoMove()
      return minScore

def findMoveNegaMax(gs, validMoves, depth, turnMultiplier):
  global nextMove, counter
  counter += 1
  if depth == 0:
    return turnMultiplier * scoreBoard(gs)

  maxScore = -Win
  for move in validMoves:
    gs.makeMove(move)
    nextMoves = gs.getValidMoves()
    score = -findMoveNegaMax(gs, nextMoves, depth-1, -turnMultiplier)
    if score > maxScore:
      maxScore = score
      if depth == DEPTH:
        nextMove = move
    gs.undoMove()
  return maxScore



def findMoveNegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, turnMultiplier):
  global nextMove, counter
  counter += 1
  if depth == 0:
    return turnMultiplier * scoreBoard(gs)

  #move ordering -  implement later
  maxScore = -Win
  for move in validMoves:
    gs.makeMove(move)
    nextMoves = gs.getValidMoves()
    score = -findMoveNegaMaxAlphaBeta(gs, nextMoves, depth-1, -beta, -alpha, -turnMultiplier)
    if score > maxScore:
      maxScore = score
      if depth == DEPTH:
        nextMove = move
    gs.undoMove()
    if maxScore > alpha: #pruning happens
      alpha = maxScore
    if alpha >= beta:
      break
  return maxScore

"""
A positive score is good for white, a negative score is good for black
"""
def scoreBoard(gs):
  score = 0
  whitePieces = 0
  blackPieces = 0
  whiteLastRow = False
  blackLastRow = False
  whiteCheck = False
  blackCheck = False
  for r in range(8):
    for c in range(8):
      if gs.board[r][c] == 'w':
        score += pieceScore['w'] #piece value
        whitePieces += 1
        if r == 0:
          whiteLastRow = True
          break
        if r == 1:
          whiteCheck = True
          break
        if c > 0 and c < 7 and gs.board[r-1][c-1] != 'b' and gs.board[r-1][c+1] != 'b': #if move forward still alive
          score += 2**(7-r)  #location value
      elif gs.board[r][c] == 'b':
        score -= pieceScore['b']
        
        blackPieces += 1
        if r == 7:
          blackLastRow = True
          break
        if r == 6:
          blackCheck = True
          break
          
        if c > 0 and c < 7 and gs.board[r+1][c-1] != 'w' and gs.board[r+1][c+1] != 'w': #if move forward still alive
          score -= 2**r  #location value
        
  if (blackCheck or blackLastRow or whitePieces == 0 ) and gs.whiteToMove:
      return -Win #black wins
  elif (whiteCheck or whiteLastRow or blackPieces == 0 ) and not gs.whiteToMove:
      return Win #white wins
  return score