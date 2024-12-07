import math, random
import pygame
import sys

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
        self.board = [[0 for i in range(self.row_length)] for _ in range(self.row_length)]
        self.box_length = int(math.sqrt(self.row_length))

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
        return num not in self.board[row]

    '''
    Determines if num is contained in the specified column (vertical) of the board
    If num is already in the specified col, return False. Otherwise, return True

    Parameters:
    col is the index of the column we are checking
    num is the value we are looking for in the column

    Return: boolean
    '''
    def valid_in_col(self, col, num):
        for i in range(self.row_length):
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

    def valid_in_box(self, box_row, box_col, num):
        row_start = box_row * 3
        col_start = box_col * 3
        for r in range(row_start, row_start + 3):
            for c in range(col_start, col_start + 3):
                if self.board[r][c] == num:
                    return False
        return True
    '''
    Determines if it is valid to enter num at (row, col) in the board
    This is done by checking that num is unused in the appropriate, row, column, and box

    Parameters:
    row and col are the row index and col index of the cell to check in the board
    num is the value to test if it is safe to enter in this cell

    Return: boolean
    '''

    def is_valid(self, row, col, num):
        if not self.valid_in_row(row, num):
            return False
        if not self.valid_in_col(col, num):
            return False
        if not self.valid_in_box(row // 3, col // 3, num):
            return False
        return True
    '''
    Fills the specified 3x3 box with values
    For each position, generates a random digit which has not yet been used in the box

    Parameters:
    row_start and col_start are the starting indices of the box to check
    i.e. the box is from (row_start, col_start) to (row_start+2, col_start+2)

    Return: None
    '''

    def fill_box(self, row_start, col_start):
        nums = list(range(1, 10))
        random.shuffle(nums)
        for r in range(3):
            for c in range(3):
                self.board[row_start + r][col_start + c] = nums[r * 3 + c]
    '''
    Fills the three boxes along the main diagonal of the board
    These are the boxes which start at (0,0), (3,3), and (6,6)

    Parameters: None
    Return: None
    '''

    def fill_diagonal(self):
        self.fill_box(0, 0)
        self.fill_box(3, 3)
        self.fill_box(6, 6)

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
            if col == int((row // self.box_length) * self.box_length):
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
        count = self.removed_cells
        while count > 0:
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            if self.board[row][col] != 0:
                self.board[row][col] = 0
                count -= 1


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
        self.sketch = 0

    def set_sketched_value(self, value):
        self.sketch = value

    def draw(self):
        cell_size = 60
        x = self.col * cell_size
        y = self.row * cell_size
        rect = pygame.Rect(x, y, cell_size, cell_size)
        pygame.draw.rect(self.screen, (255, 255, 255), rect)
        if self.is_selected:
            pygame.draw.rect(self.screen, (255, 0, 0), rect, 3)
        else:
            pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)

        if self.value != 0:
            font = pygame.font.Font(None, 74)
            text = font.render(str(self.value), True, (0, 0, 0))
            self.screen.blit(text, (x + 20, y + 5))

        if self.sketch != 0 and self.value == 0:
            font = pygame.font.Font(None, 34)
            sketch_text = font.render(str(self.sketch), True, (128, 128, 128))
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
        if 0 <= x < 540 and 0 <= y < 540:
            col = x // 60
            row = y // 60
            return row, col
        return None

    def clear(self):
        if self.selected_cell and self.selected_cell.value == 0:
            self.selected_cell.set_sketched_value(0)

    def sketch(self, value):
        if self.selected_cell and self.selected_cell.value == 0:
            self.selected_cell.set_sketched_value(value)

    def place_number(self):
        if self.selected_cell and self.selected_cell.sketch != 0:
            self.selected_cell.set_cell_value(self.selected_cell.sketch)

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
                box_vals = [self.cells[r][c].value for r in range(box_row * 3, box_row * 3 + 3)
                            for c in range(box_col * 3, box_col * 3 + 3)]
                if not self.check_unique(box_vals):
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

    def draw(self):
        cell_size = 60
        for i in range(10):
            thickness = 3 if i % 3 == 0 else 1
            pygame.draw.line(self.screen, (0, 0, 0), (i * cell_size, 0), (i * cell_size, 540), thickness)
            pygame.draw.line(self.screen, (0, 0, 0), (0, i * cell_size), (540, i * cell_size), thickness)
        for row in self.cells:
            for cell in row:
                cell.draw()
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

def generate_sudoku(size, removed):
    sudoku = SudokuGenerator(size, removed)
    sudoku.fill_values()
    board = sudoku.get_board()
    sudoku.remove_cells()
    board = sudoku.get_board()
    return board

def draw_button(screen, text, x, y, w, h, inactive_color, active_color, mouse):
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, active_color, (x, y, w, h))
    else:
        pygame.draw.rect(screen, inactive_color, (x, y, w, h))

    font = pygame.font.Font(None, 36)
    text_surf = font.render(text, True, (0, 0, 0))
    text_rect = text_surf.get_rect(center=(x + w / 2, y + h / 2))
    screen.blit(text_surf, text_rect)


def start_screen(screen):
    running = True
    while running:
        screen.fill((255, 255, 255))
        font = pygame.font.Font(None, 64)
        title_surf = font.render("Welcome to Sudoku!", True, (0, 0, 0))
        title_rect = title_surf.get_rect(center=(270, 100))
        screen.blit(title_surf, title_rect)

        font_sub = pygame.font.Font(None, 36)
        subtitle_surf = font_sub.render("Select Your Difficulty", True, (0, 0, 0))
        subtitle_rect = subtitle_surf.get_rect(center=(270, 160))
        screen.blit(subtitle_surf, subtitle_rect)

        mouse = pygame.mouse.get_pos()


        easy_button_rect = (120, 220, 100, 50)
        med_button_rect = (220, 220, 100, 50)
        hard_button_rect = (320, 220, 100, 50)


        draw_button(screen, "Easy", *easy_button_rect, (200, 200, 200), (170, 170, 170), mouse)
        draw_button(screen, "Medium", *med_button_rect, (200, 200, 200), (170, 170, 170), mouse)
        draw_button(screen, "Hard", *hard_button_rect, (200, 200, 200), (170, 170, 170), mouse)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                mx, my = event.pos

                if easy_button_rect[0] <= mx <= easy_button_rect[0] + easy_button_rect[2] and \
                        easy_button_rect[1] <= my <= easy_button_rect[1] + easy_button_rect[3]:
                    return 30

                if med_button_rect[0] <= mx <= med_button_rect[0] + med_button_rect[2] and \
                        med_button_rect[1] <= my <= med_button_rect[1] + med_button_rect[3]:
                    return 40
                if hard_button_rect[0] <= mx <= hard_button_rect[0] + hard_button_rect[2] and \
                        hard_button_rect[1] <= my <= hard_button_rect[1] + hard_button_rect[3]:
                    return 50

        pygame.display.flip()


def main():
    pygame.init()
    screen = pygame.display.set_mode((540, 540))
    pygame.display.set_caption("Sudoku")

    removed_cells = start_screen(screen)

    sudoku = SudokuGenerator(9, removed_cells)
    sudoku.fill_values()
    sudoku.remove_cells()
    initial_board = sudoku.get_board()

    board = Board(9, 9, screen, difficulty=removed_cells)
    for row in range(9):
        for col in range(9):
            board.cells[row][col].set_cell_value(initial_board[row][col])
    board.select(0, 0)

    running = True
    while running:
        screen.fill((255, 255, 255))
        board.draw()
        pygame.display.flip()

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
                elif event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE:
                    board.clear()
                elif event.key == pygame.K_RETURN:
                    board.place_number()
                    if board.is_full():
                        if board.check_board():
                            print("Congratulations! You solved the puzzle.")
                            running = False
                        else:
                            print("Incorrect solution. Keep trying!")
                elif pygame.K_1 <= event.key <= pygame.K_9:
                    value = event.key - pygame.K_0
                    board.sketch(value)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                clicked_cell = board.click(pos[0], pos[1])
                if clicked_cell:
                    board.select(*clicked_cell)

    pygame.quit()


if __name__ == "__main__":
    main()
