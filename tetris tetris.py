import pygame
import random
import sys
import os

# --- Config ---
WIDTH, HEIGHT = 400, 600
GRID_SIZE = 30
COLS, ROWS = 10, 20
SIDE_PANEL = 150

pygame.init()
screen = pygame.display.set_mode((WIDTH + SIDE_PANEL, HEIGHT))
pygame.display.set_caption("Tetris Tetris")
clock = pygame.time.Clock()
font = pygame.font.SysFont("comicsansms", 20)
big_font = pygame.font.SysFont("comicsansms", 40)

# --- Colors ---
COLORS = [
    (0, 255, 255),
    (255, 0, 255),
    (0, 255, 0),
    (255, 165, 0),
    (255, 255, 0),
    (255, 0, 0),
    (0, 0, 255)
]
BG_COLOR = (20, 20, 30)
GRID_COLOR = (50, 50, 60)
BUTTON_COLOR = (50, 200, 50)
BUTTON_HOVER = (0, 255, 100)
TEXT_COLOR = (0, 0, 0)

# --- Shapes ---
SHAPES = [
    [[1,1,1,1]],                 # I
    [[1,1],[1,1]],               # O
    [[0,1,0],[1,1,1]],           # T
    [[1,0,0],[1,1,1]],           # L
    [[0,0,1],[1,1,1]],           # J
    [[1,1,0],[0,1,1]],           # S
    [[0,1,1],[1,1,0]]            # Z
]

# --- High Score ---
def load_high_score():
    if os.path.exists("highscore.txt"):
        with open("highscore.txt", "r") as f:
            return int(f.read())
    return 0

def save_high_score(score):
    with open("highscore.txt", "w") as f:
        f.write(str(score))

high_score = load_high_score()

# --- Grid ---
grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]

class Piece:
    def __init__(self, shape=None):
        if shape:
            self.matrix, self.color = shape
        else:
            self.matrix, self.color = random.choice(list(zip(SHAPES, COLORS)))
        self.x = COLS // 2 - len(self.matrix[0]) // 2
        self.y = 0

    def rotate(self):
        self.matrix = [list(row) for row in zip(*self.matrix[::-1])]

def valid_move(piece, dx, dy):
    for y, row in enumerate(piece.matrix):
        for x, cell in enumerate(row):
            if cell:
                nx = piece.x + x + dx
                ny = piece.y + y + dy
                if nx < 0 or nx >= COLS or ny >= ROWS:
                    return False
                if ny >= 0 and grid[ny][nx]:
                    return False
    return True

def merge(piece):
    for y, row in enumerate(piece.matrix):
        for x, cell in enumerate(row):
            if cell:
                grid[piece.y + y][piece.x + x] = piece.color

def clear_lines():
    global grid, score
    lines_cleared = 0
    new_grid = []
    for row in grid:
        if all(row):
            lines_cleared += 1
        else:
            new_grid.append(row)
    while len(new_grid) < ROWS:
        new_grid.insert(0, [0]*COLS)
    grid[:] = new_grid

    if lines_cleared == 1:
        score += 100
    elif lines_cleared == 2:
        score += 300
    elif lines_cleared == 3:
        score += 500
    elif lines_cleared == 4:
        score += 800

def draw_grid():
    for x in range(COLS):
        for y in range(ROWS):
            pygame.draw.rect(screen, GRID_COLOR,
                (x*GRID_SIZE, y*GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)

def draw_next_piece():
    label = font.render("Next:", True, (255,255,255))
    screen.blit(label, (WIDTH + 10, 20))
    for y, row in enumerate(next_piece.matrix):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, next_piece.color,
                    (WIDTH + 20 + x*GRID_SIZE,
                     60 + y*GRID_SIZE,
                     GRID_SIZE, GRID_SIZE))

def draw_buttons():
    mx, my = pygame.mouse.get_pos()
    
    # Restart Button
    restart_rect = pygame.Rect(WIDTH + 20, 500, 100, 40)
    restart_color = BUTTON_HOVER if restart_rect.collidepoint(mx, my) else BUTTON_COLOR
    pygame.draw.rect(screen, restart_color, restart_rect)
    restart_text = font.render("Restart", True, TEXT_COLOR)
    screen.blit(restart_text, (WIDTH + 30, 510))
    
    # Back to Home Button
    back_rect = pygame.Rect(WIDTH + 20, 440, 100, 40)
    back_color = BUTTON_HOVER if back_rect.collidepoint(mx, my) else BUTTON_COLOR
    pygame.draw.rect(screen, back_color, back_rect)
    back_text = font.render("Home", True, TEXT_COLOR)
    screen.blit(back_text, (WIDTH + 40, 450))
    
    return restart_rect, back_rect

def draw_game():
    screen.fill(BG_COLOR)
    for y in range(ROWS):
        for x in range(COLS):
            if grid[y][x]:
                pygame.draw.rect(screen, grid[y][x],
                                 (x*GRID_SIZE, y*GRID_SIZE, GRID_SIZE, GRID_SIZE))
    for y, row in enumerate(current.matrix):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, current.color,
                                 ((current.x + x)*GRID_SIZE,
                                  (current.y + y)*GRID_SIZE,
                                  GRID_SIZE, GRID_SIZE))
    draw_grid()
    draw_next_piece()
    restart_rect, back_rect = draw_buttons()
    score_text = font.render(f"Score: {score}", True, (255,255,255))
    high_score_text = font.render(f"High Score: {high_score}", True, (255,255,255))
    screen.blit(score_text, (WIDTH + 10, 200))
    screen.blit(high_score_text, (WIDTH + 10, 230))
    pygame.display.flip()
    return restart_rect, back_rect

def game_over_screen():
    screen.fill(BG_COLOR)
    text = big_font.render("GAME OVER", True, (255,0,0))
    screen.blit(text, (WIDTH//2 - 120, HEIGHT//2 - 40))
    pygame.display.flip()
    pygame.time.delay(3000)

def home_screen():
    while True:
        screen.fill(BG_COLOR)
        title = big_font.render("Tetris Tetris", True, (0,255,255))
        screen.blit(title, (WIDTH//2 - 120, HEIGHT//3))

        mx, my = pygame.mouse.get_pos()

        # Play Button
        play_rect = pygame.Rect(WIDTH//2 - 60, HEIGHT//2, 120, 50)
        play_color = BUTTON_HOVER if play_rect.collidepoint(mx,my) else BUTTON_COLOR
        pygame.draw.rect(screen, play_color, play_rect)
        play_text = font.render("Play", True, TEXT_COLOR)
        screen.blit(play_text, (WIDTH//2 - 20, HEIGHT//2 + 15))

        # Quit Button
        quit_rect = pygame.Rect(WIDTH//2 - 60, HEIGHT//2 + 80, 120, 50)
        quit_color = BUTTON_HOVER if quit_rect.collidepoint(mx,my) else BUTTON_COLOR
        pygame.draw.rect(screen, quit_color, quit_rect)
        quit_text = font.render("Quit", True, TEXT_COLOR)
        screen.blit(quit_text, (WIDTH//2 - 20, HEIGHT//2 + 95))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_rect.collidepoint(mx,my):
                    return  # start game
                if quit_rect.collidepoint(mx,my):
                    pygame.quit()
                    sys.exit()

# --- Game Setup ---
score = 0
fall_speed = 500
fall_time = 0
current = Piece()
next_piece = Piece()
grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]

# --- Start at Home Screen ---
home_screen()

running = True
game_over = False

# --- Game Loop ---
while running:
    dt = clock.tick(60)
    fall_time += dt

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            restart_rect, back_rect = draw_buttons()
            if restart_rect.collidepoint(mx, my):
                # Restart game
                grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
                score = 0
                fall_speed = 500
                fall_time = 0
                current = Piece()
                next_piece = Piece()
                game_over = False
            if back_rect.collidepoint(mx, my):
                # Back to home screen
                grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
                score = 0
                fall_speed = 500
                fall_time = 0
                current = Piece()
                next_piece = Piece()
                game_over = False
                home_screen()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and valid_move(current,-1,0):
                current.x -= 1
            if event.key == pygame.K_RIGHT and valid_move(current,1,0):
                current.x += 1
            if event.key == pygame.K_DOWN and valid_move(current,0,1):
                current.y += 1
            if event.key == pygame.K_UP:
                old_matrix = current.matrix
                current.rotate()
                if valid_move(current,0,0):
                    pass
                elif valid_move(current,1,0):
                    current.x += 1
                elif valid_move(current,-1,0):
                    current.x -= 1
                else:
                    current.matrix = old_matrix

    if fall_time > fall_speed:
        if valid_move(current,0,1):
            current.y += 1
        else:
            merge(current)
            clear_lines()
            current = next_piece
            next_piece = Piece()
            if not valid_move(current,0,0):
                game_over = True
                if score > high_score:
                    save_high_score(score)
                    high_score = score
            fall_speed = max(100, fall_speed - 5)
        fall_time = 0

    draw_game()
    if game_over:
        game_over_screen()
        grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        score = 0
        fall_speed = 500
        fall_time = 0
        current = Piece()
        next_piece = Piece()
        game_over = False
        home_screen()

pygame.quit()
sys.exit()
