import pygame
import sys
import math
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 660, 750  # Increased height for scoreboard and buttons
LINE_WIDTH = 1
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3.5
CIRCLE_WIDTH = 4
CROSS_WIDTH = 4
SPACE = SQUARE_SIZE // 4

# Colors
BG_COLOR = '#161616'
LINE_COLOR = '#F9977B'
CIRCLE_COLOR = '#F9977B'
CROSS_COLOR = '#E2D2FE'
TEXT_COLOR = 142, 186, 187
BUTTON_COLOR_PLAY_AGAIN = 78, 112, 97
BUTTON_COLOR_CLOSE = 122, 36, 15
WIN_LINE_COLOR = 142, 186, 187 # Lighter red color for winning line 

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic Tac Toe')
screen.fill(BG_COLOR)

# Font
font = pygame.font.Font(None, 150)
small_font = pygame.font.Font(None, 30)

# Board representation
board = [[None] * BOARD_COLS for _ in range(BOARD_ROWS)]  # 3x3 board initialized to None
player_wins = {'Human': 0, 'AI': 0}  # Scoreboard

def draw_lines():
    # Horizontal
    pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH)
    # Vertical
    pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT - 100), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT - 100), LINE_WIDTH)

def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 'Human':
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), 
                                (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE), 
                                (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), CROSS_WIDTH)
            elif board[row][col] == 'AI':
                pygame.draw.circle(screen, CIRCLE_COLOR, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 
                                   CIRCLE_RADIUS, CIRCLE_WIDTH)

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

def draw_scoreboard():
    screen.fill(BG_COLOR, (0, HEIGHT - 50, WIDTH, 50))  # Clear previous score and buttons
    draw_text(f"Human: {player_wins['Human']}", small_font, CROSS_COLOR, screen, WIDTH // 2.5, HEIGHT - 50)  # Updated Human color
    draw_text(f"AI: {player_wins['AI']}", small_font, CIRCLE_COLOR, screen, 3 * WIDTH // 4.5, HEIGHT - 50)  # Updated AI color
    pygame.draw.rect(screen, BUTTON_COLOR_PLAY_AGAIN, (WIDTH - 150, HEIGHT - 90, 130, 60))
    draw_text("Play Again", small_font, TEXT_COLOR, screen, WIDTH - 85, HEIGHT - 60)
    pygame.draw.rect(screen, BUTTON_COLOR_CLOSE, (20, HEIGHT - 90, 130, 60))
    draw_text("Close", small_font, TEXT_COLOR, screen, 85, HEIGHT - 60)

def draw_winning_line(winning_combo):
    row, col, direction = winning_combo
    if direction == 'row':
        y_pos = row * SQUARE_SIZE + SQUARE_SIZE // 2
        pygame.draw.line(screen, WIN_LINE_COLOR, (15, y_pos), (WIDTH - 15, y_pos), 15)
    elif direction == 'col':
        x_pos = col * SQUARE_SIZE + SQUARE_SIZE // 2
        pygame.draw.line(screen, WIN_LINE_COLOR, (x_pos, 15), (x_pos, HEIGHT - 115), 15)
    elif direction == 'diag':
        if col == 0:  # Left to right
            pygame.draw.line(screen, WIN_LINE_COLOR, (15, 15), (WIDTH - 15, HEIGHT - 115), 15)
        elif col == 2:  # Right to left
            pygame.draw.line(screen, WIN_LINE_COLOR, (WIDTH - 15, 15), (15, HEIGHT - 115), 15)

def check_win(player):
    # Check for win in rows, columns, and diagonals
    for row in range(BOARD_ROWS):
        if all([spot == player for spot in board[row]]):
            return (row, 0, 'row')
    for col in range(BOARD_COLS):
        if all([board[row][col] == player for row in range(BOARD_ROWS)]):
            return (0, col, 'col')
    if all([board[i][i] == player for i in range(BOARD_ROWS)]):
        return (0, 0, 'diag')
    if all([board[i][BOARD_ROWS - i - 1] == player for i in range(BOARD_ROWS)]):
        return (0, 2, 'diag')
    return None

def minimax_alpha_beta(board, depth, is_maximizing, alpha, beta):
    if check_win('AI'):
        return 1
    elif check_win('Human'):
        return -1
    elif not any(None in row for row in board):
        return 0

    if is_maximizing:
        max_eval = -math.inf
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col] is None:
                    board[row][col] = 'AI'
                    eval = minimax_alpha_beta(board, depth + 1, False, alpha, beta)
                    board[row][col] = None
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
        return max_eval
    else:
        min_eval = math.inf
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col] is None:
                    board[row][col] = 'Human'
                    eval = minimax_alpha_beta(board, depth + 1, True, alpha, beta)
                    board[row][col] = None
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
        return min_eval

def best_move_alpha_beta():
    best_score = -math.inf
    move = None
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] is None:
                board[row][col] = 'AI'
                score = minimax_alpha_beta(board, 0, False, -math.inf, math.inf)
                board[row][col] = None
                if score > best_score:
                    best_score = score
                    move = (row, col)
    return move



def display_winner_message(message, color ):
    # Draw the final state of the board
    draw_figures()
    pygame.display.update()
    
    # Pause to show the final board state before the message
    time.sleep(0.5)
    
    # Display the winner message
    draw_text(message, font, color, screen, WIDTH // 2, HEIGHT // 2)
    pygame.display.update()
    
    # Pause to keep the message visible
    time.sleep(0.5)

def restart_game():
    global board, player, game_over
    board = [[None] * BOARD_COLS for _ in range(BOARD_ROWS)]
    player = 'Human'
    game_over = False
    screen.fill(BG_COLOR)
    draw_lines()
    draw_scoreboard()

# Main game loop
draw_lines()
draw_scoreboard()
player = 'Human'
game_over = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseX, mouseY = event.pos

            # Close button click
            if HEIGHT - 90 <= mouseY <= HEIGHT - 30 and 20 <= mouseX <= 150:
                pygame.quit()
                sys.exit()

            # Play Again button click
            if HEIGHT - 90 <= mouseY <= HEIGHT - 30 and WIDTH - 150 <= mouseX <= WIDTH - 20:
                restart_game()

            if not game_over:
                clicked_row = mouseY // SQUARE_SIZE
                clicked_col = mouseX // SQUARE_SIZE

                if player == 'Human' and clicked_row < 3 and board[clicked_row][clicked_col] is None:
                    board[clicked_row][clicked_col] = player
                    winning_combo = check_win(player)
                    if winning_combo:
                        draw_winning_line(winning_combo)
                        display_winner_message("Human Wins!", CROSS_COLOR)
                        player_wins['Human'] += 1
                        game_over = True
                    elif not any(None in row for row in board):
                        display_winner_message("It's a Tie!", TEXT_COLOR)
                        game_over = True
                    else:
                        player = 'AI'
                        draw_figures()

        if player == 'AI' and not game_over:
            pygame.display.update()  # Update display to show AI's last move
            move = best_move_alpha_beta()
            if move:
                board[move[0]][move[1]] = 'AI'
                winning_combo = check_win(player)
                if winning_combo:
                    draw_winning_line(winning_combo)
                    display_winner_message("AI Wins!", (142, 186, 187))
                    player_wins['AI'] += 1
                    game_over = True
                elif not any(None in row for row in board):
                    display_winner_message("It's a Tie!", 'Black')
                    game_over = True
                else:
                    player = 'Human'
                    draw_figures()

    pygame.display.update()