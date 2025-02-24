import pygame
import random

# Размеры игрового поля
BOARD_SIZE = 9
CELL_SIZE = 60
GRID_SIZE = CELL_SIZE * BOARD_SIZE
THICK_LINE_WIDTH = 4 # Толщина линий между девятками клетками
THIN_LINE_WIDTH = 1 # Толщина тонких линий

# Цвета
BACKGROUND_COLOR = (255, 255, 255)
LINE_COLOR = (0, 0, 0)
TEXT_COLOR = (0, 0, 0)
SELECTED_COLOR = (173, 216, 230) # Светло-синий цвет для выбранной клетки
HIGHLIGHT_COLOR = (173, 216, 230) # Светло-синий цвет для одинаковых чисел
INVALID_COLOR = (255, 0, 0) # Красный цвет для неправильных чисел
HIGHLIGHT_BOX_COLOR = (211, 211, 211) # Светло-серый цвет для области 3x3

# Инициализация Pygame
pygame.init()

# Создание окна
screen = pygame.display.set_mode((GRID_SIZE, GRID_SIZE))
pygame.display.set_caption('Судоку')

# Шрифт для цифр
font = pygame.font.SysFont('arial', 40)

# Статусы для ячеек
current_selected = None # Текущая выбранная ячейка
board = None # Игровое поле с убранными числами
original_board = None # Оригинальное полное поле
invalid_numbers = [[False for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]


def is_valid(board, row, col, num):
    for x in range(BOARD_SIZE):
        if board[row][x] == num or board[x][col] == num:
            return False

    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if board[i + start_row][j + start_col] == num:
                return False
    return True


def solve_sudoku(board):
    empty = find_empty_location(board)
    if not empty:
        return True
    row, col = empty

    for num in range(1, 10):
        if is_valid(board, row, col, num):
            board[row][col] = num
            if solve_sudoku(board):
                return True
            board[row][col] = 0
            
    return False


def find_empty_location(board):
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] == 0:
                return (i, j)
    return None


def generate_complete_board():
    board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    solve_sudoku(board)
    return board


def remove_numbers(board, difficulty_level=0.5):
    cells_to_remove = int(BOARD_SIZE * BOARD_SIZE * difficulty_level)
    while cells_to_remove > 0:
        i = random.randint(0, BOARD_SIZE - 1)
        j = random.randint(0, BOARD_SIZE - 1)
        if board[i][j] != 0:
            board[i][j] = 0
            cells_to_remove -= 1


def generate_sudoku(difficulty_level=0.5):
    complete_board = generate_complete_board()
    remove_numbers(complete_board, difficulty_level)
    return complete_board


def draw_grid():
    # Рисуем сетку
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            line_width = THIN_LINE_WIDTH
            if i % 3 == 0 and i > 0: # Толстые горизонтальные линии
                line_width = THICK_LINE_WIDTH
                pygame.draw.line(screen, LINE_COLOR, (0, i * CELL_SIZE), (GRID_SIZE, i * CELL_SIZE), line_width)
            if j % 3 == 0 and j > 0: # Толстые вертикальные линии
                line_width = THICK_LINE_WIDTH
                pygame.draw.line(screen, LINE_COLOR, (j * CELL_SIZE, 0), (j * CELL_SIZE, GRID_SIZE), line_width)
            # Рисуем тонкие линии вокруг клеток
            rect = pygame.Rect(j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, LINE_COLOR, rect, 1)


def draw_highlight(row, col):
    # Подсветка строки
    row_rect = pygame.Rect(0, row * CELL_SIZE, GRID_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, HIGHLIGHT_BOX_COLOR, row_rect)
    # Подсветка столбца
    col_rect = pygame.Rect(col * CELL_SIZE, 0, CELL_SIZE, GRID_SIZE)
    pygame.draw.rect(screen, HIGHLIGHT_BOX_COLOR, col_rect)
    # Подсветка области 3x3
    start_row = (row // 3) * 3
    start_col = (col // 3) * 3
    area_rect = pygame.Rect(start_col * CELL_SIZE, start_row * CELL_SIZE, 3 * CELL_SIZE, 3 * CELL_SIZE)
    pygame.draw.rect(screen, HIGHLIGHT_BOX_COLOR, area_rect)


def reset_board():
    global board, original_board, invalid_numbers
    original_board = generate_complete_board() # Генерируем полное поле
    board = generate_sudoku(0.5) # Уровень сложности 0.5 (50% убрано)
    invalid_numbers = [[False for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)] # Сброс статуса неправильных чисел


def draw_sudoku(board):
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            number = board[i][j]
            if number != 0:
                color = TEXT_COLOR
                # Если число было введено неверно, устанавливаем красный цвет
                if invalid_numbers[i][j]:
                    color = INVALID_COLOR
                text = font.render(str(number), True, color)
                screen.blit(text, (j * CELL_SIZE + 20, i * CELL_SIZE + 10))


def main():
    global current_selected, board, original_board, invalid_numbers
    clock = pygame.time.Clock()
    reset_board()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                current_selected = (y // CELL_SIZE, x // CELL_SIZE) # Определение выбранной ячейки
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4,
                                 pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]:
                    if current_selected is not None:
                        row, col = current_selected
                        num = int(event.unicode) # Получаем число, соответствующее нажатой клавише
                        # Проверяем правильность введенного значения с оригинальной таблицей
                        if original_board[row][col] == num:
                            board[row][col] = num # Если правильно, записываем его в игровое поле
                            invalid_numbers[row][col] = False # Сбрасываем статус неверного числа
                        else:
                            board[row][col] = num # Записываем число даже если оно неверно
                            invalid_numbers[row][col] = True # Устанавливаем статус неверного числа
                if event.key == pygame.K_r: # Сбросить поле
                    reset_board()
                    current_selected = None # Сброс выделения при сбросе игры
        screen.fill(BACKGROUND_COLOR)
        # 1. Подсветка строки и столбца выбранной клетки
        if current_selected is not None:
            row, col = current_selected
            draw_highlight(row, col) # Подсвечиваем строку и столбец, а также область 3x3
            # Подсветка выбранной ячейки (она становится светло-синей)
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            # Подсветка выбранной клетки, если она не пустая, тот подсветка клеток, имеющих такое же значение, как и выбранная
            if board[row][col] == 0:
                pygame.draw.rect(screen, HIGHLIGHT_COLOR, rect) # Подсветка пустой клетки
            else:
                pygame.draw.rect(screen, SELECTED_COLOR, rect) # Подсветка заполненной клетки
                # Подсветка всех ячеек с одинаковым числом
                number = board[row][col]
                highlighted_cells = [(r, c) for r in range(BOARD_SIZE) for c in range(BOARD_SIZE) if board[r][c] == number]
                for r, c in highlighted_cells:
                    highlighted_rect = pygame.Rect(c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                    pygame.draw.rect(screen, HIGHLIGHT_COLOR, highlighted_rect)
        # 2. Отрисовка сетки
        draw_grid()
        # 3. Отрисовка цифр
        draw_sudoku(board)
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()


if __name__ == "__main__":
    main()