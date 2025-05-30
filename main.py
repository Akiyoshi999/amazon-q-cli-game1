#!/usr/bin/env python3
import pygame
import sys
from game import Game

def show_difficulty_menu_screen(screen, width, height):
    """難易度選択メニューを表示"""
    # Colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GRAY = (150, 150, 150)
    HIGHLIGHT = (100, 200, 255)
    
    # Font
    font_large = pygame.font.SysFont(None, 60)
    font_medium = pygame.font.SysFont(None, 40)
    
    # Button dimensions
    button_width = 200
    button_height = 50
    button_spacing = 20
    
    # Button positions
    easy_button = pygame.Rect((width - button_width) // 2, height // 2 - button_height - button_spacing,
                             button_width, button_height)
    normal_button = pygame.Rect((width - button_width) // 2, height // 2,
                               button_width, button_height)
    hard_button = pygame.Rect((width - button_width) // 2, height // 2 + button_height + button_spacing,
                             button_width, button_height)
    
    # Title
    title_text = font_large.render("Horizontal Shooter", True, WHITE)
    title_rect = title_text.get_rect(center=(width // 2, height // 4))
    
    # Subtitle
    subtitle_text = font_medium.render("Select Difficulty", True, WHITE)
    subtitle_rect = subtitle_text.get_rect(center=(width // 2, height // 3))
    
    # Button texts
    easy_text = font_medium.render("Easy", True, BLACK)
    normal_text = font_medium.render("Normal", True, BLACK)
    hard_text = font_medium.render("Hard", True, BLACK)
    
    # Mouse position for hover effect
    mouse_pos = pygame.mouse.get_pos()
    
    # Check button hover
    easy_hover = easy_button.collidepoint(mouse_pos)
    normal_hover = normal_button.collidepoint(mouse_pos)
    hard_hover = hard_button.collidepoint(mouse_pos)
    
    # Draw background
    screen.fill((0, 0, 50))  # Dark blue background
    
    # Draw title and subtitle
    screen.blit(title_text, title_rect)
    screen.blit(subtitle_text, subtitle_rect)
    
    # Draw buttons with hover effect
    pygame.draw.rect(screen, HIGHLIGHT if easy_hover else WHITE, easy_button, 0, 10)
    pygame.draw.rect(screen, HIGHLIGHT if normal_hover else WHITE, normal_button, 0, 10)
    pygame.draw.rect(screen, HIGHLIGHT if hard_hover else WHITE, hard_button, 0, 10)
    
    # Draw button text
    screen.blit(easy_text, easy_text.get_rect(center=easy_button.center))
    screen.blit(normal_text, normal_text.get_rect(center=normal_button.center))
    screen.blit(hard_text, hard_text.get_rect(center=hard_button.center))
    
    # Update display
    pygame.display.flip()

def check_button_click(mouse_pos, width, height):
    """難易度選択ボタンのクリックをチェック"""
    # Button dimensions
    button_width = 200
    button_height = 50
    button_spacing = 20
    
    # Button positions
    easy_button = pygame.Rect((width - button_width) // 2, height // 2 - button_height - button_spacing,
                             button_width, button_height)
    normal_button = pygame.Rect((width - button_width) // 2, height // 2,
                               button_width, button_height)
    hard_button = pygame.Rect((width - button_width) // 2, height // 2 + button_height + button_spacing,
                             button_width, button_height)
    
    # Check which button was clicked
    if easy_button.collidepoint(mouse_pos):
        return "easy"
    elif normal_button.collidepoint(mouse_pos):
        return "normal"
    elif hard_button.collidepoint(mouse_pos):
        return "hard"
    
    return None

def main():
    # Initialize pygame
    pygame.init()
    
    # Screen dimensions
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    
    # Game state
    current_state = "menu"  # "menu" or "game"
    game = None
    
    # Game loop
    clock = pygame.time.Clock()
    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if current_state == "menu":
                # Menu event handling
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    difficulty = check_button_click(mouse_pos, width, height)
                    if difficulty:
                        # Start game with selected difficulty
                        game = Game(width, height, difficulty)
                        current_state = "game"
            else:
                # Game event handling
                result = game.handle_event(event)
                if result == "menu":
                    current_state = "menu"  # Return to menu
        
        # Update and render
        if current_state == "menu":
            show_difficulty_menu_screen(screen, width, height)
        else:
            game.update()
            game.render()
        
        # Cap the frame rate
        clock.tick(60)

if __name__ == "__main__":
    main()
