import pygame

# Define constants
BOARD_SIZE = 10
TILE_SIZE = 50
SCREEN_SIZE = BOARD_SIZE * TILE_SIZE
BUTTON_HEIGHT = 50
INFO_WIDTH = 300
WINDOW_WIDTH = SCREEN_SIZE + INFO_WIDTH
WINDOW_HEIGHT = SCREEN_SIZE + BUTTON_HEIGHT + 60   # Increased height to fit the buttons and margin

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PLAYER1_COLOR = (255, 0, 0)  # Red
PLAYER2_COLOR = (0, 0, 255)  # Blue
BUTTON_COLOR = (0, 51, 51)
BUTTON_HOVER_COLOR = (0, 255, 128)
BUTTON_TEXT_COLOR = (255, 255, 255)
BUTTON_BORDER_COLOR = (0, 0, 0)  # Color for button borders
SHAPE_DISPLAY_TILE_SIZE = 20  # Smaller size for shape display
SHAPES = {
    'L*1:': [[(0, 0), (1, 0), (2, 0), (2, 1)], 4],
    'Box*2:': [[(0, 0), (0, 1), (1, 0), (1, 1)], 4],
    'T*3:': [[(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)], 5]
}

def draw_board(screen, board):
    """Draw the game board with the current state."""
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            color = WHITE if board[row][col] is None else board[row][col]
            pygame.draw.rect(screen, color, (col * TILE_SIZE, row * TILE_SIZE + 60, TILE_SIZE, TILE_SIZE))  # Adjusted Y position
            pygame.draw.rect(screen, BLACK, (col * TILE_SIZE, row * TILE_SIZE + 60, TILE_SIZE, TILE_SIZE), 1)  # Adjusted Y position

def draw_button(screen, text, x, y, width, height):
    """Draw a button and handle button click events."""
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    # Draw button background
    if x < mouse[0] < x + width and y < mouse[1] < y + height:
        pygame.draw.rect(screen, BUTTON_HOVER_COLOR, (x, y, width, height))
        if click[0] == 1:
            return True
    else:
        pygame.draw.rect(screen, BUTTON_COLOR, (x, y, width, height))
    
    # Draw button border
    pygame.draw.rect(screen, BUTTON_BORDER_COLOR, (x, y, width, height), 2)  # Border around the button

    # Draw button text
    font = pygame.font.Font(None, 36)
    text_surface = font.render(text, True, BUTTON_TEXT_COLOR)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surface, text_rect)
    
    return False

def draw_info(screen, current_player, player1_points, player2_points):
    """Draw the game title and player information."""
    font = pygame.font.Font(None, 36)
    
    # Draw the game title above the board
    title_text = "Color Board Game"
    title_surface = font.render(title_text, True, BLACK)
    title_rect = title_surface.get_rect(center=(SCREEN_SIZE // 2, 30))  # Centered above the board
    screen.blit(title_surface, title_rect)
    
    # Draw player turn information
    player_info_x = SCREEN_SIZE + 10
    y_offset = 60  # Starting Y position for the player info section, moved down for board
    
    info_text = f"Current Player: {'Player' if current_player == PLAYER1_COLOR else 'AI'}\n"
    info_text += f"Player: {player1_points}\nAI: {player2_points}\n"
    
    for line in info_text.split('\n'):
        text_surface = font.render(line, True, BLACK)
        screen.blit(text_surface, (player_info_x, y_offset))
        y_offset += 40
    
    # Draw "Allowed Shapes" title
    shapes_title_text = "Allowed Shapes"
    shapes_title_surface = font.render(shapes_title_text, True, BLACK)
    shapes_title_rect = shapes_title_surface.get_rect(topleft=(player_info_x, y_offset + 10))
    screen.blit(shapes_title_surface, shapes_title_rect)
    y_offset += 50  # Move below the "Allowed Shapes" title

    return y_offset  # Return the y offset after drawing shapes

def draw_shapes(screen, y_offset):
    """Draw the allowed shapes and their representation."""
    font = pygame.font.Font(None, 28)  # Smaller font size for shape names
    shape_offset_x = SCREEN_SIZE + 10
    
    for shape_name, (coords, base_points) in SHAPES.items():
        # Draw shape name
        shape_text = font.render(shape_name, True, BLACK)
        screen.blit(shape_text, (shape_offset_x, y_offset))
        
        # Draw shape
        for dr, dc in coords:
            pygame.draw.rect(screen, BLACK, (shape_offset_x + 70 + dc * SHAPE_DISPLAY_TILE_SIZE, y_offset + dr * SHAPE_DISPLAY_TILE_SIZE, SHAPE_DISPLAY_TILE_SIZE, SHAPE_DISPLAY_TILE_SIZE), 1)
        
        y_offset += 30  # Space between shape name and shape
        y_offset += SHAPE_DISPLAY_TILE_SIZE * 2  # Space for the shape itself
        y_offset += 20  # Space between different shapes
