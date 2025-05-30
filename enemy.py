import pygame
import random
import math

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 20  # 30から20に縮小
        self.height = 20  # 30から20に縮小
        self.speed = random.randint(2, 5)
        self.color = (255, 0, 0)  # Red
        
        # Random movement pattern
        self.move_pattern = random.choice(["straight", "sine", "zigzag"])
        self.amplitude = random.randint(20, 50)  # For sine and zigzag patterns
        self.frequency = random.uniform(0.05, 0.1)  # For sine pattern
        self.direction = 1  # For zigzag pattern
        self.zigzag_counter = 0  # For zigzag pattern
        self.original_y = y  # Store original y position for patterns
    
    def update(self):
        # Move left
        self.x -= self.speed
        
        # Apply movement pattern
        if self.move_pattern == "sine":
            # Sine wave movement
            self.y = self.original_y + self.amplitude * \
                     math.sin(self.frequency * self.x)
        elif self.move_pattern == "zigzag":
            # Zigzag movement
            self.zigzag_counter += 1
            if self.zigzag_counter >= 20:
                self.direction *= -1
                self.zigzag_counter = 0
            self.y += self.direction * (self.speed / 2)
    
    def draw(self, screen):
        # Draw enemy ship (circular with details)
        pygame.draw.circle(screen, self.color, (self.x + self.width // 2, self.y + self.height // 2), 
                          self.width // 2)
        
        # Draw enemy details
        pygame.draw.circle(screen, (150, 0, 0), (self.x + self.width // 2, self.y + self.height // 2), 
                          self.width // 3)
        pygame.draw.rect(screen, (100, 0, 0), 
                        (self.x + self.width // 2 - 5, self.y, 10, self.height))
