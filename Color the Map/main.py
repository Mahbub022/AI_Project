import pygame
import sys
from interface import draw_board, draw_button, draw_info, draw_shapes, PLAYER1_COLOR, PLAYER2_COLOR, WHITE, BLACK, BOARD_SIZE, TILE_SIZE, SCREEN_SIZE, BUTTON_HEIGHT, INFO_WIDTH, WINDOW_WIDTH, WINDOW_HEIGHT
from rules import check_shapes, show_endgame_popup, best_move_for_ai, fuzzyLogic, geneticAlgo
from level import run_level_selection

# Initialize Pygame
pygame.init()

class Button:
    def __init__(self, text, x, y, width, height, color, hover_color):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, self.hover_color, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)

        font = pygame.font.Font(None, 36)
        text_surface = font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False

def show_score_popup(screen, winner, points):
    font = pygame.font.Font(None, 48)
    background = pygame.Surface(screen.get_size())
    # background.set_alpha(128)  # Semi-transparent overlay
    background.fill((255, 255, 255))  # White background
    screen.blit(background, (0, 0))

    # Display winner text

    if winner == PLAYER1_COLOR :
        win = "Player"
    elif winner == PLAYER2_COLOR:
        win = "AI"                    
    winner_text = f"{win} won!"
    points_text = f"Points: {points}"
    winner_surface = font.render(winner_text, True, (0, 0, 0))
    points_surface = font.render(points_text, True, (0, 0, 0))
    screen.blit(winner_surface, (300, 200))
    screen.blit(points_surface, (300, 250))

    # Define buttons
    restart_button = Button("Restart", 250, 300, 200, 50, (70, 130, 180), (100, 149, 237))
    menu_button = Button("Menu", 470, 300, 200, 50, (70, 130, 180), (100, 149, 237))

    pygame.display.flip()  # Update the display to show the pop-up

    # Event loop for the pop-up
    # flag = -1
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if restart_button.is_clicked(event):
                running = False
                return 1

            if menu_button.is_clicked(event):
                running = False
                return 0

        restart_button.draw(screen)
        menu_button.draw(screen)
        pygame.display.update()

# def reset_game():
#     main()  # Restart the game by calling main
    

# def return_to_menu():
#     screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
#     chosen_level = run_level_selection(screen)
#     if chosen_level is None:
#         sys.exit()  # Exit if no level is chosen


def wait_for_new_click():
    """Wait for the user to release the mouse button and click anew, preventing accidental game actions."""
    pygame.event.clear(pygame.MOUSEBUTTONDOWN)  # Clear existing mouse down events
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:  # Wait for mouse to be released
                return


def main():
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Color Board Game')

    # Run level selection
    chosen_level = run_level_selection(screen)
    if chosen_level is None:
        return  # If no level is chosen, exit
    
    # Wait for new click to prevent accidental actions
    wait_for_new_click()

    # Setup the game based on chosen level
    current_player = PLAYER1_COLOR
    running = True
    game_over = False
    board = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    player1_points = 0
    player2_points = 0
    empty = 100

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))  # White background
        draw_board(screen, board)
        stop_clicked = draw_button(screen, 'Stop', 0, SCREEN_SIZE + 60, SCREEN_SIZE // 2, BUTTON_HEIGHT)
        restart_clicked = draw_button(screen, 'Restart', SCREEN_SIZE // 2, SCREEN_SIZE + 60, SCREEN_SIZE // 2, BUTTON_HEIGHT)

        
        if stop_clicked:
            running = False

        if restart_clicked:
            board[:] = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
            current_player = PLAYER1_COLOR
            player1_points = 0
            player2_points = 0
            empty = 100
            game_over = False
            continue


        if not game_over:
            if current_player == PLAYER1_COLOR:
                if pygame.mouse.get_pressed()[0]:
                    x, y = pygame.mouse.get_pos()
                    if y >= 60 and y < SCREEN_SIZE + 60 and x < SCREEN_SIZE:
                        col = x // TILE_SIZE
                        row = (y - 60) // TILE_SIZE
                        if board[row][col] is None:
                            board[row][col] = current_player
                            empty -= 1
                            points = check_shapes(board, row, col, current_player)
                            player1_points += points
                            current_player = PLAYER2_COLOR
                            print("Player->", empty)
            else:
                move = fuzzyLogic(board, PLAYER2_COLOR, PLAYER1_COLOR, empty, abs(player1_points-player2_points))
                if move:
                    row, col = move
                    board[row][col] = PLAYER2_COLOR
                    empty -= 1
                    points = check_shapes(board, row, col, PLAYER2_COLOR)
                    player2_points += points
                    current_player = PLAYER1_COLOR
                    print("AI->", empty)

            if not empty or player1_points > 50 or player2_points > 50:
                print(empty)
                print(board)
                game_over = True
                winner = PLAYER1_COLOR if player1_points > player2_points else PLAYER2_COLOR if player2_points > player1_points else None
                # show_endgame_popup(screen, winner, player1_points, player2_points)
                winPoints = player1_points if winner == PLAYER1_COLOR else player2_points if winner == PLAYER2_COLOR else None
                flag = show_score_popup(screen, winner, winPoints)
                print (flag)

                if flag == 1:
                    wait_for_new_click()
                    board[:] = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
                    current_player = PLAYER1_COLOR
                    player1_points = 0
                    player2_points = 0
                    empty = 100
                    game_over = False
                    continue

                elif flag == 0:
                    main()
                    
        # Draw info and shapes
        y_offset = draw_info(screen, current_player, player1_points, player2_points)
        draw_shapes(screen, y_offset)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
