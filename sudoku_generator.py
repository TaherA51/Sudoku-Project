import math, random
import pygame
import sys


class SudokuGenerator:
    def __init__(self, row_length, removed_cells):
        self.row_length = row_length
        self.removed_cells = removed_cells
        self.board = [[0 for i in range(self.row_length)] for _ in range(self.row_length)]
        self.box_length = int(math.sqrt(self.row_length))

    def get_board(self):
        return self.board

    def valid_in_row(self, row, num):
        return num not in self.board[row]

    def print_board(self):
        for row in self.board:
            print(row)

    def valid_in_col(self, col, num):
        for i in range(self.row_length):
            if self.board[i][col] == num:
                return False
        return True

    def valid_in_box(self, box_row, box_col, num):
        row_start = box_row * 3
        col_start = box_col * 3
        for r in range(row_start, row_start + 3):
            for c in range(col_start, col_start + 3):
                if self.board[r][c] == num:
                    return False
        return True
  
    def is_valid(self, row, col, num):
        if not self.valid_in_row(row, num):
            return False
        if not self.valid_in_col(col, num):
            return False
        if not self.valid_in_box(row // 3, col // 3, num):
            return False
        return True

    def fill_box(self, row_start, col_start):
        nums = list(range(1, 10))
        random.shuffle(nums)
        for r in range(3):
            for c in range(3):
                self.board[row_start + r][col_start + c] = nums[r*3 + c]

    def fill_diagonal(self):
        self.fill_box(0, 0)
        self.fill_box(3, 3)
        self.fill_box(6, 6)


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

    def fill_values(self):
        self.fill_diagonal()
        self.fill_remaining(0, self.box_length)

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
                box_vals = [self.cells[r][c].value for r in range(box_row*3, box_row*3+3)
                            for c in range(box_col*3, box_col*3+3)]

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
        grid_size = 540

        self.screen.fill((255, 255, 255))

        for row in self.cells:
            for cell in row:
                cell.draw()

        for row in range(3):
            for col in range(3):
                rect = pygame.Rect(col * 3 * cell_size, row * 3 * cell_size, 3 * cell_size, 3 * cell_size)
                pygame.draw.rect(self.screen, (0, 0, 0), rect, 4)

def generate_sudoku(size, removed):
    sudoku = SudokuGenerator(size, removed)
    sudoku.fill_values()
    sudoku.remove_cells()
    board = sudoku.get_board()
    return board

def draw_button(screen, text, x, y, w, h, inactive_color, active_color, mouse, action=None):
    """
    Draw a button and handle actions when clicked.
    """
    clicked = False
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen, active_color, (x, y, w, h))
        if pygame.mouse.get_pressed()[0] and action:
            clicked = action
    else:
        pygame.draw.rect(screen, inactive_color, (x, y, w, h))

    font = pygame.font.Font(None, 36)
    text_surf = font.render(text, True, (0, 0, 0))
    text_rect = text_surf.get_rect(center=(x+w/2, y+h/2))
    screen.blit(text_surf, text_rect)
    
    return clicked

def display_message(screen, message, color):
    """
    Display a large centered message on the screen.
    """
    screen.fill((255, 255, 255))
    font = pygame.font.Font(None, 64)
    text_surf = font.render(message, True, color)
    text_rect = text_surf.get_rect(center=(270, 270))
    screen.blit(text_surf, text_rect)
    pygame.display.flip()
    pygame.time.wait(3000)


def start_screen(screen):
    running = True
    while running:
        screen.fill((255,255,255))
        font = pygame.font.Font(None, 64)
        title_surf = font.render("Welcome to Sudoku!", True, (0,0,0))
        title_rect = title_surf.get_rect(center=(270,100))
        screen.blit(title_surf, title_rect)

        font_sub = pygame.font.Font(None, 36)
        subtitle_surf = font_sub.render("Select Your Difficulty", True, (0,0,0))

        subtitle_rect = subtitle_surf.get_rect(center=(270, 160))
        screen.blit(subtitle_surf, subtitle_rect)

        mouse = pygame.mouse.get_pos()

        easy_button_rect = (120, 220, 100, 50)
        med_button_rect = (220, 220, 100, 50)
        hard_button_rect = (320, 220, 100, 50)
        draw_button(screen, "Easy", *easy_button_rect, (200,200,200), (170,170,170), mouse)
        draw_button(screen, "Medium", *med_button_rect, (200,200,200), (170,170,170), mouse)
        draw_button(screen, "Hard", *hard_button_rect, (200,200,200), (170,170,170), mouse)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
        
                if easy_button_rect[0] <= mx <= easy_button_rect[0]+easy_button_rect[2] and \
                   easy_button_rect[1] <= my <= easy_button_rect[1]+easy_button_rect[3]:
                    return 30
                
                if med_button_rect[0] <= mx <= med_button_rect[0]+med_button_rect[2] and \
                   med_button_rect[1] <= my <= med_button_rect[1]+med_button_rect[3]:
                    return 40
                
                if hard_button_rect[0] <= mx <= hard_button_rect[0]+hard_button_rect[2] and \
                   hard_button_rect[1] <= my <= hard_button_rect[1]+hard_button_rect[3]:
                    return 50

        pygame.display.flip()

def game_over_screen(screen, restart_action):
    """
    Display the Game Over screen with a Restart button.
    """
    running = True
    while running:
        screen.fill((255, 255, 255))
        font = pygame.font.Font(None, 64)
        text_surf = font.render("Game Over!", True, (255, 0, 0))
        text_rect = text_surf.get_rect(center=(270, 200))
        screen.blit(text_surf, text_rect)

        mouse = pygame.mouse.get_pos()
        restart_clicked = draw_button(screen, "Restart", 170, 350, 200, 50, (200, 200, 200), (170, 170, 170), mouse, "restart")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif restart_clicked == "restart":
                restart_action()
                return

        pygame.display.flip()


def win_screen(screen):
    """
    Display the Win screen with an Exit button.
    """
    running = True
    while running:
        screen.fill((255, 255, 255))
        font = pygame.font.Font(None, 64)
        text_surf = font.render("You Win!", True, (0, 255, 0))
        text_rect = text_surf.get_rect(center=(270, 200))
        screen.blit(text_surf, text_rect)

        mouse = pygame.mouse.get_pos()
        exit_clicked = draw_button(screen, "Exit", 170, 350, 200, 50, (200, 200, 200), (170, 170, 170), mouse, "exit")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif exit_clicked == "exit":
                pygame.quit()
                sys.exit()

        pygame.display.flip()


def main():
    pygame.init()
    screen = pygame.display.set_mode((540, 600))
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

    initial_board_copy = [[cell.value for cell in row] for row in board.cells]


    running = True
    while running:
        screen.fill((255, 255, 255))
        board.draw()
        pygame.display.flip()

        mouse = pygame.mouse.get_pos()
        reset_clicked = draw_button(screen, "Reset", 60, 550, 100, 40, (200, 200, 200), (170, 170, 170), mouse, "reset")
        restart_clicked = draw_button(screen, "Restart", 220, 550, 100, 40, (200, 200, 200), (170, 170, 170), mouse, "restart")
        exit_clicked = draw_button(screen, "Exit", 380, 550, 100, 40, (200, 200, 200), (170, 170, 170), mouse, "exit")

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
                            win_screen(screen)
                            running = False
                        else:
                            game_over_screen(screen, main)
                            running = False

                elif pygame.K_1 <= event.key <= pygame.K_9:
                    value = event.key - pygame.K_0
                    board.sketch(value)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                clicked_cell = board.click(pos[0], pos[1])
                if clicked_cell:
                    board.select(*clicked_cell)

        if reset_clicked == "reset":
            for r, row in enumerate(initial_board_copy):
                for c, value in enumerate(row):
                    board.cells[r][c].set_cell_value(value)
            board.select(0, 0)

        if restart_clicked == "restart":
            main()
            return

        if exit_clicked == "exit":
            running = False

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()

