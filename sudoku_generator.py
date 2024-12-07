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
                self.board[row_start + r][col_start + c] = nums[r * 3 + c]

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


def draw_button(screen, text, x, y, w, h, inactive_color, active_color, mouse, action_type):

    is_hovered = x + w > mouse[0] > x and y + h > mouse[1] > y
    color = active_color if is_hovered else inactive_color

    pygame.draw.rect(screen, color, (x, y, w, h), border_radius=10)
    pygame.draw.rect(screen, (255, 255, 255), (x, y, w, h), 2, border_radius=10)  # White border

    font = pygame.font.Font(None, 28)
    text_surf = font.render(text, True, (0, 33, 165))  # UF Blue text
    text_rect = text_surf.get_rect(center=(x + w / 2, y + h / 2))
    screen.blit(text_surf, text_rect)

    if is_hovered and pygame.mouse.get_pressed()[0]:
        return action_type
    return None


def display_message(screen, message, color):

    screen.fill((255, 255, 255))
    font = pygame.font.Font(None, 64)
    text_surf = font.render(message, True, color)
    text_rect = text_surf.get_rect(center=(270, 270))
    screen.blit(text_surf, text_rect)
    pygame.display.flip()
    pygame.time.wait(3000)


def start_screen(screen):
    running = True

    UF_ORANGE = (250, 70, 22)
    UF_BLUE = (0, 33, 165)

    alligator_img = pygame.image.load("alligator.png")
    alligator_img = pygame.transform.scale(alligator_img, (200, 200))
    alligator_rect = alligator_img.get_rect(center=(270, 400))

    while running:
        screen.fill(UF_BLUE)

        font = pygame.font.Font(None, 64)
        title_surf = font.render("Gator Sudoku!", True, UF_ORANGE)
        title_rect = title_surf.get_rect(center=(270, 100))
        screen.blit(title_surf, title_rect)

        font_sub = pygame.font.Font(None, 36)
        subtitle_surf = font_sub.render("Select Your Difficulty", True, (255, 255, 255))
        subtitle_rect = subtitle_surf.get_rect(center=(270, 160))
        screen.blit(subtitle_surf, subtitle_rect)

        mouse = pygame.mouse.get_pos()
        easy_button_rect = pygame.Rect(70, 220, 120, 50)
        med_button_rect = pygame.Rect(210, 220, 120, 50)
        hard_button_rect = pygame.Rect(350, 220, 120, 50)

        easy_clicked = draw_button(screen, "Easy", easy_button_rect.x, easy_button_rect.y, easy_button_rect.width,
                                   easy_button_rect.height, UF_ORANGE, (255, 150, 100), mouse, "easy")
        med_clicked = draw_button(screen, "Medium", med_button_rect.x, med_button_rect.y, med_button_rect.width,
                                  med_button_rect.height, UF_ORANGE, (255, 150, 100), mouse, "medium")
        hard_clicked = draw_button(screen, "Hard", hard_button_rect.x, hard_button_rect.y, hard_button_rect.width,
                                   hard_button_rect.height, UF_ORANGE, (255, 150, 100), mouse, "hard")

        screen.blit(alligator_img, alligator_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if easy_button_rect.collidepoint(event.pos):
                    return 30
                elif med_button_rect.collidepoint(event.pos):
                    return 40
                elif hard_button_rect.collidepoint(event.pos):
                    return 50

        pygame.display.flip()


def win_screen(screen):

    running = True
    while running:
        screen.fill((255, 255, 255))
        font = pygame.font.Font(None, 64)
        text_surf = font.render("You Win!", True, (0, 255, 0))
        text_rect = text_surf.get_rect(center=(270, 200))
        screen.blit(text_surf, text_rect)

        mouse = pygame.mouse.get_pos()
        exit_button = pygame.Rect(170, 350, 200, 50)
        exit_hovered = draw_button(screen, "Exit", exit_button.x, exit_button.y, exit_button.width, exit_button.height,
                                   (200, 200, 200), (170, 170, 170), mouse, "exit")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and exit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()


def game_over_screen(screen, restart_action):

    running = True
    while running:
        screen.fill((255, 255, 255))
        font = pygame.font.Font(None, 64)
        text_surf = font.render("Game Over!", True, (255, 0, 0))
        text_rect = text_surf.get_rect(center=(270, 200))
        screen.blit(text_surf, text_rect)

        mouse = pygame.mouse.get_pos()
        restart_button = pygame.Rect(170, 350, 200, 50)
        restart_hovered = draw_button(screen, "Restart", restart_button.x, restart_button.y, restart_button.width,
                                      restart_button.height, (200, 200, 200), (170, 170, 170), mouse, "restart")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and restart_button.collidepoint(event.pos):
                    restart_action()
                    return

        pygame.display.flip()


def draw_button(screen, text, x, y, w, h, inactive_color, active_color, mouse, action_type):
    button_rect = pygame.Rect(x, y, w, h)
    is_hovered = button_rect.collidepoint(mouse)
    color = active_color if is_hovered else inactive_color

    pygame.draw.rect(screen, color, button_rect, border_radius=10)
    pygame.draw.rect(screen, (255, 255, 255), button_rect, 2, border_radius=10)  # White border

    font = pygame.font.Font(None, 28)
    text_surf = font.render(text, True, (0, 33, 165))  # UF Blue text
    text_rect = text_surf.get_rect(center=button_rect.center)
    screen.blit(text_surf, text_rect)

    return is_hovered


def main():
    pygame.init()
    screen = pygame.display.set_mode((540, 600))
    pygame.display.set_caption("Gator Sudoku")

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
        screen.fill((240, 240, 245)) 
        board.draw()

        mouse = pygame.mouse.get_pos()
        reset_button = pygame.Rect(60, 560, 120, 40)
        restart_button = pygame.Rect(210, 560, 120, 40)
        exit_button = pygame.Rect(360, 560, 120, 40)

        reset_hovered = draw_button(screen, "Reset", reset_button.x, reset_button.y, reset_button.width,
                                    reset_button.height, (200, 200, 255), (170, 170, 255), mouse, "reset")
        restart_hovered = draw_button(screen, "Restart", restart_button.x, restart_button.y, restart_button.width,
                                      restart_button.height, (200, 255, 200), (170, 255, 170), mouse, "restart")
        exit_hovered = draw_button(screen, "Exit", exit_button.x, exit_button.y, exit_button.width, exit_button.height,
                                   (255, 200, 200), (255, 170, 170), mouse, "exit")

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
                if event.button == 1: 
                    pos = event.pos
                    if reset_button.collidepoint(pos):
                        for r, row in enumerate(initial_board_copy):
                            for c, value in enumerate(row):
                                board.cells[r][c].set_cell_value(value)
                        board.select(0, 0)
                    elif restart_button.collidepoint(pos):
                        main()
                        return
                    elif exit_button.collidepoint(pos):
                        running = False
                    else:
                        clicked_cell = board.click(pos[0], pos[1])
                        if clicked_cell:
                            board.select(*clicked_cell)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()

