# Sudoku-Project

## Fork Repository Instructions
### Steps:
1. When you go to the github repository we provided, on the top right hand corner of the screen, there is a button that says "Fork". That will fork the repo to your own github 
2. Use the link https://github.com/new/import to clone your forked repo to make it private. You will work on the project by adding your own files to this private repository.


## Roles:

### Person 1: Sudoku Generator and Core Logic

**Specific Tasks:**
- Implement the SudokuGenerator class in sudoku_generator.py, including:
  - __init__ method with row_length and removed_cells parameters
  - get_board method to return the 2D board
  - valid_in_row, valid_in_col, and valid_in_box methods
  - is_valid method to check if a number can be placed in a cell
  - fill_box method to fill a 3x3 box with random numbers
  - fill_diagonal method to fill the three diagonal boxes
  - remove_cells method to clear the appropriate number of cells
- Implement the generate_sudoku function outside the class
- Write unit tests for the SudokuGenerator class methods

### Person 2: User Interface and PyGame Integration

**Specific Tasks:**
- Set up the PyGame environment and create the main game window
- Design and implement the Game Start screen with:
  - Title
  - Difficulty selection buttons (Easy, Medium, Hard)
- Create the game-in-progress screen with:
  - 9x9 Sudoku grid
  - Reset, Restart, and Exit buttons
- Implement the win and game over screens
- Handle PyGame events for mouse clicks and keyboard input
- Implement screen transitions between different game states

### Person 3: Game Mechanics and User Interaction

**Specific Tasks:**
- Implement the Cell class with methods:
  - __init__ method with value, row, col, and screen parameters
  - set_cell_value and set_sketched_value methods
  - draw method to render the cell and its value
- Implement the Board class with methods:
  - __init__ method with width, height, screen, and difficulty parameters
  - select method to mark the current cell
  - click method to handle cell selection
  - clear, sketch, and place_number methods for user input
  - is_full and check_board methods to verify game state
- Implement arrow key navigation between cells

### Person 4: Main Game Loop and Integration

**Specific Tasks:**
- Develop the main game loop in sudoku.py
- Implement difficulty selection logic with corresponding empty cell counts:
  - Easy: 30 empty cells
  - Medium: 40 empty cells
  - Hard: 50 empty cells
- Integrate SudokuGenerator with Board and Cell classes
- Implement the reset_to_original method in the Board class
- Create the update_board and find_empty methods in the Board class
- Ensure proper flow between different game states (start, play, win/lose)
- Coordinate with team members to integrate all components
- Set up and manage the GitHub repository for the project

Each team member should also contribute to:
- Writing the project report (max 4 pages)
- Creating the video demonstration
- Testing and debugging the entire application
- Providing peer feedback for team members
