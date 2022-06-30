import pygame
import sys
import numpy as np
import Engine
import AI

"""
  ChessMain
"""
BOARD_WIDTH = 512
BOARD_HEIGHT = 512
MOVE_LOG_PANEL_WIDTH = 250
MOVE_LOG_PANEL_HEIGHT = BOARD_HEIGHT
DIMENSION = 8
SQSIZE = BOARD_WIDTH // DIMENSION
MAX_FPS = 15
IMAGES = {}

LINE_WIDTH = 1

BG_COLOR = (252, 204, 116)
LINE_COLOR = (78,79,75)


"""
Highlight the square selected and moves for piece selected
"""
def highlightSquare(screen, gs, validMoves, sqSelected):
  if sqSelected != ():
    r, c = sqSelected
    if gs.board[r][c] == ('w' if gs.whiteToMove else 'b'): #sqSelected is a piece th at can be moved
      #highlight selected square
      s = pygame.Surface((SQSIZE, SQSIZE))
      s.set_alpha(100)#transparent
      s.fill(pygame.Color('blue'))
      screen.blit(s, (c*SQSIZE, r*SQSIZE))
      
      #highlight moves from that square
      for move in validMoves:
        if move.startRow == r and move.startCol == c:
          if move.pieceCaptured != '--': #Eat opponent
            s.fill(pygame.Color('red'))
            screen.blit(s, (SQSIZE*move.endCol, SQSIZE*move.endRow))
          else:#Normal moves
            s.fill(pygame.Color('yellow'))
            screen.blit(s, (SQSIZE*move.endCol, SQSIZE*move.endRow))

"""
Responsible for all graph
"""
def drawGameState(screen, gs, validMoves, sqSelected, moveLogFont):
  # draw squares on the board, suggestions
  drawBoard(screen)
  highlightSquare(screen, gs, validMoves, sqSelected)
  # draw pieces on top of the squares
  drawPieces(screen, gs.board)
  drawMoveLog(screen, gs, moveLogFont)
"""
Draw move log
"""
def drawMoveLog(screen, gs, font):
  moveLogRect = pygame.Rect(BOARD_WIDTH, 0, MOVE_LOG_PANEL_WIDTH, MOVE_LOG_PANEL_HEIGHT)
  pygame.draw.rect(screen, pygame.Color("black"), moveLogRect)
  moveLog = gs.movelog
  moveTexts = []
  for i in range(0, len(moveLog), 2):
    moveString = str(i//2 + 1) + ". " + moveLog[i].getChessNotation() + "  "
    if i+1 < len(moveLog): #make sure black made a move
      moveString += moveLog[i+1].getChessNotation() + "   "
      
    moveTexts.append(moveString)
    
  movesPerRow = 2
  padding = 5
  textY = padding
  lineSpacing = 2
  for i in range(0, len(moveTexts), movesPerRow):
    text = ""
    for j in range(movesPerRow):
      if i+j < len(moveTexts):
        text += moveTexts[i+j]
    textObject = font.render(text, True, pygame.Color('white'))
    textLocation = moveLogRect.move(padding , textY)
    screen.blit(textObject, textLocation)
    textY += textObject.get_height() + lineSpacing
  
"""
Draw board
"""
def drawBoard(screen):
  global colors
  colors = [pygame.Color("white"), pygame.Color("gray")]
  
  for r in range(DIMENSION):
    for c in range(DIMENSION):
      color = colors[(r+c)%2]
      pygame.draw.rect(screen, color, pygame.Rect(c*SQSIZE, r*SQSIZE, SQSIZE, SQSIZE))

"""
Draw the pieces on the board using the current GS board 
"""
def drawPieces(screen, board):
  for r in range(DIMENSION):
    for c in range(DIMENSION):
      piece = board[r][c]
      if piece != "--":
        screen.blit(IMAGES[piece], pygame.Rect((c*SQSIZE, r*SQSIZE, SQSIZE, SQSIZE)))
                    
def loadImages():
  IMAGES['b'] = pygame.transform.scale(pygame.image.load("images/b.png"), (SQSIZE, SQSIZE))
  IMAGES['w'] = pygame.transform.scale(pygame.image.load("images/w.png"), (SQSIZE, SQSIZE))

          
    
    
def main():
  
  # PYGAME SETUP
  pygame.init()
  screen = pygame.display.set_mode([BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, BOARD_HEIGHT])
  clock = pygame.time.Clock()
  pygame.display.set_caption('Breakthrough')
  screen.fill(BG_COLOR)

  

  # object
  gs = Engine.GameState()
  validMoves = gs.getValidMoves()
  moveMade = False #flag variable for when a move is made
  loadImages()
  moveLogFont = pygame.font.SysFont("Menlo", 12, False, False)
  
  #print(validMoves)

  # mainloop
  running = True
  sqSelected = () # keep track of the last click of the user
  playerClicks = [] # keep track of player clicks (two tuples: [(6, 4), (4, 4)])
  animate = False #flag variable for when we should animate not undo
  gameOver = False
  playerOne = True  #if a human is playing white, then True. AI is playing white then False 
  playerTwo = False #same but for black
  
  while running:
    humanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)
    
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
    
      elif event.type == pygame.MOUSEBUTTONDOWN:
        if not gameOver and humanTurn:
          pos = event.pos
          row = pos[1] // SQSIZE
          col = pos[0] // SQSIZE
          
          if sqSelected == (row, col) or col >= 8: # user clicked the same square twice or user clicked the move log
            sqSelected = () #deselect
            playerClicks = [] #clear player clicks
          else:
            sqSelected = (row, col)
            playerClicks.append(sqSelected) #append for 1st 2nd cicks
  
          if len(playerClicks) == 2: # after the 2nd clicks
            move = Engine.Move(playerClicks[0], playerClicks[1], gs.board)
            #print(move.getChessNotation())
            if move in validMoves:
              gs.makeMove(move)
              moveMade = True
              animate = True
              sqSelected = () #reset the user clicks
              playerClicks = []
            else:
              playerClicks = [sqSelected]
          
      #key handlers
      elif event.type == pygame.KEYDOWN:
        print("key")
        if event.key == pygame.K_z: #undo when z is pressed
          gs.undoMove()
          moveMade = True
          animate = False
          gameOver = False
        if event.key == pygame.K_r: #reset the board when 'r' is pressed
          gs = Engine.GameState()
          validMoves = gs.getValidMoves()
          sqSelected = ()
          playerClicks = []
          moveMade = False
          animate = False
          gameOver = False

    #AI move finder
    if not gameOver and not humanTurn:
      AIMove = AI.findBestMove(gs, validMoves)
      if AIMove is None:
        AIMove = AI.findRandomMove(validMoves)
      gs.makeMove(AIMove)
      moveMade = True
      animate = True

    
    if moveMade:
      if animate:
        animateMove(gs.movelog[-1], screen, gs.board, clock)
        
      validMoves = gs.getValidMoves()
      moveMade = False
      animate = False

    
    drawGameState(screen, gs, validMoves, sqSelected, moveLogFont)
    
    gs.checkWinner()
    
    
    if gs.gameEnd:
      gameOver = True
      if gs.whiteToMove:
        drawText(screen, "Black wins")
      else:
        drawText(screen, "White wins")
    clock.tick(MAX_FPS)
    pygame.display.flip()
    
"""
Animate a move
"""
def animateMove(move, screen, board, clock):
  global colors
  dR = move.endRow - move.startRow
  dC = move.endCol - move.startCol
  framesPerSquare = 10 #frames to move square
  frameCount = (abs(dR) + abs(dC)) * framesPerSquare
  
  for frame in range(frameCount + 1):
    r, c = (move.startRow + dR*frame/frameCount, move.startCol + dC*frame/frameCount)
    drawBoard(screen)
    drawPieces(screen, board)
    
    #erase the piece moved from its ending square
    color = colors[(move.endRow + move.endCol) % 2]
    endSquare = pygame.Rect(move.endCol*SQSIZE, move.endRow*SQSIZE, SQSIZE, SQSIZE)
    pygame.draw.rect(screen, color, endSquare)
    
    #draw captured piece onto rectangle
    if move.pieceCaptured != "--":
      screen.blit(IMAGES[move.pieceCaptured], endSquare)
      
    #draw moving piece
    screen.blit(IMAGES[move.pieceMoved], pygame.Rect(c*SQSIZE, r*SQSIZE, SQSIZE, SQSIZE))
    pygame.display.flip()
    clock.tick(60)

def drawText(screen, text):
  font = pygame.font.SysFont("Helvita", 32, True, False)
  textObject = font.render(text, 0, pygame.Color('Gray'))
  textLocation = pygame.Rect(0, 0, BOARD_WIDTH, BOARD_HEIGHT).move(BOARD_WIDTH/2 - textObject.get_width()/2, BOARD_HEIGHT/2 - textObject.get_height()/2)
  screen.blit(textObject, textLocation)
  textObject = font.render(text, 0, pygame.Color("Black"))
  screen.blit(textObject, textLocation.move(2, 2))
  
if __name__ == "__main__":
  main()