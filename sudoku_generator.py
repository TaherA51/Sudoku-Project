import math,random

import pygame

"""
This was adapted from a GeeksforGeeks article "Program for Sudoku Generator" by Aarti_Rathi and Ankur Trisal
https://www.geeksforgeeks.org/program-sudoku-generator/

"""

class SudokuGenerator:
    '''
	create a sudoku board - initialize class variables and set up the 2D board
	This should initialize:
	self.row_length		- the length of each row
	self.removed_cells	- the total number of cells to be removed
	self.board			- a 2D list of ints to represent the board
	self.box_length		- the square root of row_length

	Parameters:
    row_length is the number of rows/columns of the board (always 9 for this project)
    removed_cells is an integer value - the number of cells to be removed

	Return:
	None
    '''
    def __init__(self, row_length, removed_cells):
        self.row_length = row_length
        self.removed_cells = removed_cells
        self.board = [[0 for i in range(self.row_length)] for i in range(self.row_length)]
        self.box_length = math.sqrt(self.row_length)
    '''
	Returns a 2D python list of numbers which represents the board

	Parameters: None
	Return: list[list]
    '''
    def get_board(self):
        return self.board

    '''
	Displays the board to the console
    This is not strictly required, but it may be useful for debugging purposes

	Parameters: None
	Return: None
    '''
    def print_board(self):
        for row in self.board:
            print(row)

    '''
	Determines if num is contained in the specified row (horizontal) of the board
    If num is already in the specified row, return False. Otherwise, return True

	Parameters:
	row is the index of the row we are checking
	num is the value we are looking for in the row
	
	Return: boolean
    '''
    def valid_in_row(self, row, num):
        if num in self.board[row]:
            return False
        else:
            return True

    '''
	Determines if num is contained in the specified column (vertical) of the board
    If num is already in the specified col, return False. Otherwise, return True

	Parameters:
	col is the index of the column we are checking
	num is the value we are looking for in the column
	
	Return: boolean
    '''
    def valid_in_col(self, col, num):
        for i in range(len(self.board)):
            if self.board[i][col] == num:
                return False
        return True

    '''
	Determines if num is contained in the 3x3 box specified on the board
    If num is in the specified box starting at (row_start, col_start), return False.
    Otherwise, return True

	Parameters:
	row_start and col_start are the starting indices of the box to check
	i.e. the box is from (row_start, col_start) to (row_start+2, col_start+2)
	num is the value we are looking for in the box

	Return: boolean
    '''
    def valid_in_box(self, row_start, col_start, num):
        pass
    
    '''
    Determines if it is valid to enter num at (row, col) in the board
    This is done by checking that num is unused in the appropriate, row, column, and box

	Parameters:
	row and col are the row index and col index of the cell to check in the board
	num is the value to test if it is safe to enter in this cell

	Return: boolean
    '''
    def is_valid(self, row, col, num):
        pass

    '''
    Fills the specified 3x3 box with values
    For each position, generates a random digit which has not yet been used in the box

	Parameters:
	row_start and col_start are the starting indices of the box to check
	i.e. the box is from (row_start, col_start) to (row_start+2, col_start+2)

	Return: None
    '''
    def fill_box(self, row_start, col_start):
        pass
    
    '''
    Fills the three boxes along the main diagonal of the board
    These are the boxes which start at (0,0), (3,3), and (6,6)

	Parameters: None
	Return: None
    '''
    def fill_diagonal(self):
        pass

    '''
    DO NOT CHANGE
    Provided for students
    Fills the remaining cells of the board
    Should be called after the diagonal boxes have been filled
	
	Parameters:
	row, col specify the coordinates of the first empty (0) cell

	Return:
	boolean (whether or not we could solve the board)
    '''
    def fill_remaining(self, row, col):
        if (col >= self.row_length and row < self.row_length - 1):
            row += 1
            col = 0
        if row >= self.row_length and col >= self.row_length:
            return True
        if row < self.box_length:
            if col < self.box_length:
                col = self.box_length
        elif row < self.row_length - self.box_length:
            if col == int(row // self.box_length * self.box_length):
                col += self.box_length
        else:
            if col == self.row_length - self.box_length:
                row += 1
                col = 0
                if row >= self.row_length:
                    return True
        
        for num in range(1, self.row_length + 1):
            if self.is_valid(row, col, num):
                self.board[row][col] = num
                if self.fill_remaining(row, col + 1):
                    return True
                self.board[row][col] = 0
        return False

    '''
    DO NOT CHANGE
    Provided for students
    Constructs a solution by calling fill_diagonal and fill_remaining

	Parameters: None
	Return: None
    '''
    def fill_values(self):
        self.fill_diagonal()
        self.fill_remaining(0, self.box_length)

    '''
    Removes the appropriate number of cells from the board
    This is done by setting some values to 0
    Should be called after the entire solution has been constructed
    i.e. after fill_values has been called
    
    NOTE: Be careful not to 'remove' the same cell multiple times
    i.e. if a cell is already 0, it cannot be removed again

	Parameters: None
	Return: None
    '''
    def remove_cells(self):
        pass

'''
DO NOT CHANGE
Provided for students
Given a number of rows and number of cells to remove, this function:
1. creates a SudokuGenerator
2. fills its values and saves this as the solved state
3. removes the appropriate number of cells
4. returns the representative 2D Python Lists of the board and solution

Parameters:
size is the number of rows/columns of the board (9 for this project)
removed is the number of cells to clear (set to 0)

Return: list[list] (a 2D Python list to represent the board)
'''

class Cell:
    def __init__(self, value, row, col, screen):
        self.value = value
        self.sketch = 0
        self.row = row
        self.col = col
        self.screen = screen
        self.is_selected = False
    def set_cell_value(self, value):
        self.value = value
    def set_sketched_value(self, value):
        self.sketch = value

    def draw(self):
        # Assuming each cell is 60x60 pixels
        x = self.col * 60
        y = self.row * 60
        rect = pygame.Rect(x, y, 60, 60)
        pygame.draw.rect(self.screen, (255, 255, 255), rect)
        if self.is_selected:
            pygame.draw.rect(self.screen, (255, 0, 0), rect, 3)
        pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)

        if self.value != 0:
            font = pygame.font.Font("Times New Roman", 74)
            text = font.render(str(self.value), True, (0, 0, 0))
            self.screen.blit(text, (x + 20, y + 10))

        if self.sketch != 0:
            font = pygame.font.Font("Times New Roman", 34)
            sketch_text = font.render(str(self.sketch), True, (255, 0, 0))
            self.screen.blit(sketch_text, (x + 5, y + 5))

class Board:
    def __init__(self, width, height, screen, difficulty):
        self.width = width
        self.height = height
        self.screen = screen
        self.difficulty = difficulty
        self.cells = [[Cell(0, row, col, screen) for col in range(9)] for row in range(9)]
        self.selected_cell = None

    def select(self, row, col):
        if self.selected_cell:
            self.selected_cell.is_selected = False
        self.selected_cell = self.cells[row][col]
        self.selected_cell.is_selected = True

    def click(self, x, y):
        col = x // 60
        row = y // 60
        return row, col

    def clear(self):
        if self.selected_cell:
            self.selected_cell.set_cell_value(0)

    def sketch(self, value):
        if self.selected_cell:
            self.selected_cell.set_sketched_value(value)

    def place_number(self, value):
        if self.selected_cell:
            self.selected_cell.set_cell_value(value)

    def is_full(self):
        for row in self.cells:
            for cell in row:
                if cell.value == 0:
                    return False
        return True

    def check_board(self):
        for row in self.cells:
            if not self.check_unique([cell.value for cell in row]):
                return False
        for col in range(9):
            if not self.check_unique([self.cells[row][col].value for row in range(9)]):
                return False
        for box_row in range(3):
            for box_col in range(3):
                if not self.check_unique([self.cells[row][col].value for row in range(box_row*3, (box_row+1)*3) for col in range(box_col*3,(box_col+1)*3)]):
                    return False
        return True
    def check_unique(self, values):
        seen = set()
        for value in values:
            if value != 0:
                if value in seen:
                    return False
                seen.add(value)
        return True

    def move_selection(self, direction):
        if self.selected_cell:
            row, col = self.selected_cell.row, self.selected_cell.col

            if direction == "UP" and row > 0:
                self.select(row - 1, col)
            elif direction == "DOWN" and row < 8:
                self.select(row + 1, col)
            elif direction == "LEFT" and col > 0:
                self.select(row, col - 1)
            elif direction == "RIGHT" and col < 8:
                self.select(row, col + 1)




def generate_sudoku(size, removed):
    sudoku = SudokuGenerator(size, removed)
    sudoku.fill_values()
    board = sudoku.get_board()
    sudoku.remove_cells()
    board = sudoku.get_board()
    return board

def main():
    pygame.init()
    screen = pygame.display.set_mode((540, 540))
    pygame.display.set_caption("Sudoku")

    board = Board(9, 9, screen, difficulty=1)

    running = True
    while running:
        screen.fill((255, 255, 255))
        board.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    board.move_selection("UP")
                elif event.key == pygame.K_DOWN:
                    board.move_selection("DOWN")
                elif event.key == pygame.K_LEFT:
                    board.move_selection("LEFT")
                elif event.key == pygame.K_RIGHT:
                    board.move_selection("RIGHT")
                elif event.key == pygame.K_DELETE:
                    board.clear()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                clicked_cell = board.click(x, y)
                if clicked_cell:
                    board.select(*clicked_cell)

        pygame.display.flip()

    pygame.quit()