# Breakthrough AI

## Demo
[![Click here for the demo video](https://img.youtube.com/vi/Kb2qgpP9LrE/0.jpg)](https://youtu.be/Kb2qgpP9LrE)

## About The Project

This project is an implementation of the board game "Breakthrough" with an AI opponent powered by the alpha-beta pruning algorithm. The game is played on an 8x8 board where the objective is to be the first to move a piece to the opponent's home row.

### Built With

*   [Pygame](https://www.pygame.org/)
*   [NumPy](https://numpy.org/)
*   [Poetry](https://python-poetry.org/)

## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

Make sure you have Python 3.8 and Poetry installed on your system.

### Installation

1.  Clone the repo
    ```sh
    git clone https://github.com/your_username_/your_repository.git
    ```
2.  Install Python packages
    ```sh
    poetry install
    ```

## Usage

To start the game, run the following command:

```sh
poetry run python main.py
```

### How to Play

*   **Objective:** The goal is to be the first player to get one of your pieces to the opposite side of the board.
*   **Movement:**
    *   Pieces can move one space forward or diagonally forward to an empty square.
    *   Pieces can capture an opponent's piece by moving one space diagonally forward.
*   **Controls:**
    *   Use the mouse to select and move your pieces.
    *   Press the `Z` key to undo the last move.
    *   Press the `R` key to reset the game.

## File Descriptions

### `main.py`
This file serves as the main entry point for the game. It is responsible for:
- **Initialization**: Sets up the Pygame window, loads assets such as piece images, and initializes the game state.
- **Game Loop**: Contains the main loop that runs the game, capturing user input and updating the screen.
- **Event Handling**: Manages player inputs, including mouse clicks for piece selection and movement, and keyboard commands like `Z` to undo a move and `R` to reset the game.
- **Turn Management**: Determines whether it is the human player's or the AI's turn to move.
- **Rendering**: Handles all the drawing operations, such as displaying the board, the pieces, highlighting valid moves, and showing the move log.
- **AI Interaction**: Calls the AI to find the best move when it is the AI's turn.
- **Game State Updates**: Updates the game state based on player and AI moves and checks for a winner.

### `Engine.py`
This file contains the core mechanics and rules of the Breakthrough game.
- **`GameState` Class**: A central class that represents the current state of the game.
  - `board`: An 8x8 NumPy array that holds the positions of all pieces.
  - `whiteToMove`: A boolean flag to track which player's turn it is.
  - `movelog`: A list that records every move made, allowing for the undo functionality.
  - `getValidMoves()`: A method that determines all possible legal moves for the current player.
  - `makeMove()`: Applies a move to the board, updating the piece positions and switching the turn.
  - `undoMove()`: Reverts the last move made in the game.
  - `checkWinner()`: Checks if a player has won by reaching the opposite end of the board or by capturing all of the opponent's pieces.
- **`Move` Class**: Represents a single move in the game, storing the start and end positions, the piece moved, and any piece captured. It also includes a helper function to convert moves into chess notation (e.g., `a2a3`).

### `AI.py`
This file houses the logic for the artificial intelligence opponent.
- **`findBestMove()`**: The main function that the game calls to get the AI's next move. It uses the Negamax algorithm with alpha-beta pruning to search for the optimal move.
- **`findMoveNegaMaxAlphaBeta()`**: A recursive function that implements the Negamax search. It explores possible future moves up to a specified `DEPTH` to find the move that leads to the best possible outcome for the AI. Alpha-beta pruning is used to significantly cut down on the number of nodes the algorithm needs to evaluate in the game tree, making the search more efficient.
- **`scoreBoard()`**: The evaluation function that assigns a numerical score to a given board state from the AI's perspective. The score is calculated based on:
  - **Material Advantage**: The difference in the number of pieces.
  - **Positional Advantage**: Pieces are given a higher score the closer they are to the opponent's home row, encouraging the AI to advance its pieces.
  - **Win/Loss Condition**: A terminal state (a win or a loss) is given a very high or very low score to signify its importance.