import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Level Selection")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BUTTON_COLOR = (70, 130, 180)
HOVER_COLOR = (100, 149, 237)

# Define fonts
title_font = pygame.font.Font(None, 74)
subtitle_font = pygame.font.Font(None, 50)
button_font = pygame.font.Font(None, 60)

# Button class
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

        text_surface = button_font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False

# Calculate positions
button_width = 300
button_height = 100
button_spacing = 50
center_x = screen.get_width() // 2
button_x = center_x - button_width // 2

title_y = 50
subtitle_y = title_y + 100

button1_y = subtitle_y + 100
button2_y = button1_y + button_height + button_spacing

# Create buttons
button1 = Button("Easy", button_x, button1_y, button_width, button_height, BUTTON_COLOR, HOVER_COLOR)
button2 = Button("Hard", button_x, button2_y, button_width, button_height, BUTTON_COLOR, HOVER_COLOR)

def run_level_selection(screen):
    running = True
    while running:
        screen.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return None  # Ensure proper exit

            if button1.is_clicked(event):
                print("Easy Level Selected")
                return 'easy'

            if button2.is_clicked(event):
                print("Hard Level Selected")
                return 'hard'

        # Draw title and subtitle
        title_surface = title_font.render("Game: Color the Map", True, BLACK)
        title_rect = title_surface.get_rect(center=(center_x, title_y))
        screen.blit(title_surface, title_rect)

        subtitle_surface = subtitle_font.render("Click the level to start the game", True, BLACK)
        subtitle_rect = subtitle_surface.get_rect(center=(center_x, subtitle_y))
        screen.blit(subtitle_surface, subtitle_rect)

        # Draw buttons
        button1.draw(screen)
        button2.draw(screen)

        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    screen = pygame.display.set_mode((800, 600))
    level = run_level_selection(screen)
    print("Level chosen:", level)
