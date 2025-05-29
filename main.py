#!/usr/bin/env python3
import pygame
import sys
from game import Game

def main():
    # Initialize pygame
    pygame.init()
    
    # Create game instance
    game = Game(800, 600)
    
    # Game loop
    clock = pygame.time.Clock()
    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            game.handle_event(event)
        
        # Update game state
        game.update()
        
        # Render game
        game.render()
        
        # Cap the frame rate
        clock.tick(60)

if __name__ == "__main__":
    main()
